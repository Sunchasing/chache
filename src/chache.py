import datetime as dt
import threading
import time
from typing import Text, Dict, Any, Union, NoReturn, KeysView, ValuesView, ItemsView, Callable, Tuple

from src.cacheables import ICacheable, NOTEXISTS, new_cacheable
from utils import NumberType


class Chache:
    # chacha was taken

    __func_chaches: Dict[Text, 'Chache'] = {}

    def __init__(self, max_size: int, cleaning_frequency_s: NumberType):
        '''
        Setting max_size to None will set the cache max size to infinite.

        :param max_size: The maximum number of cacheables to store
        :param cleaning_frequency_s: The delay between checks for removing cacheables
        '''
        self.__data: Dict[Any, ICacheable] = {}
        self.size: int = 0
        self.max_size: int = max_size
        self.last_cleaned: Union[dt.timedelta, None] = None
        self._clean_now: bool = True
        self.hits: int = 0
        self.misses: int = 0
        self.lru: Any = None
        self.mru: Any = None
        self.cleaner_thread: threading.Thread = self._create_cleaner_thread(cleaning_frequency_s)

    @classmethod
    def _get_func_cache(cls, func: Callable,
                        max_size: int,
                        cleaning_frequency_s: NumberType) -> 'Chache':
        '''
        Instantiates the Cache class for the decorated function, if one doesn't already exist.

        :param func: The function that we decorate
        :param max_size: The maximum size for the function's cache
        :param cleaning_frequency_s: The delay between checks for removing cacheables
        :return: The functions' cache
        '''
        ret = cls.__func_chaches.get(func.__name__)
        if not ret:
            ret = Chache(max_size=max_size, cleaning_frequency_s=cleaning_frequency_s)
            cls.__func_chaches[func.__name__] = ret
        return ret

    @classmethod
    def sized_func_cache(cls, expiry: dt.date = None,
                         max_size: int = None,
                         cleaning_frequency_s: NumberType = 120) -> Callable:
        '''
        The external function decorator and API for the Cache.
        Injects cache functions into the passed function.

        :param expiry: The time when the cacheable will be flagged for cleaning
        :param max_size: The maximum number of cacheables to be stored
        :param cleaning_frequency_s: The delay between checks for removing cacheables
        :return: The decorated function with injected functionality
        '''

        def inner(func: Callable) -> Callable:
            cache = cls._get_func_cache(func, max_size, cleaning_frequency_s)

            def wrapper(*args, **kwargs):
                key = args + tuple(kwargs.values())
                rv = cache.get(key)
                if rv == NOTEXISTS:
                    rv = func(*args, **kwargs)
                    cache.put(key, rv, expiry)
                if not hasattr(wrapper, 'wipe_cache'):
                    wrapper.cache = cache
                return rv

            return wrapper

        return inner

    def _create_cleaner_thread(self, cleaning_frequency_s: NumberType) -> threading.Thread:
        '''
        Creates and starts a cleaner thread that checks if any cacheables should be deleted at set intervals.

        :param cleaning_frequency_s: Cleaning interval
        :return: The cleaning thread
        '''
        mister_clean = threading.Thread(target=self.clean,
                                        name="cache_cleaner_thread",
                                        args=(cleaning_frequency_s,),
                                        daemon=True)
        mister_clean.start()
        return mister_clean

    @property
    def accesses(self) -> int:
        '''
        :return: Total times the cache has been queried
        '''
        return self.hits + self.misses

    @property
    def data(self) -> Dict[Any, ICacheable]:
        '''
        :return: Dictionary of currently stored cacheables
        '''
        return self.__data

    def get(self, key: Any) -> Any:
        '''
        Gets the value stored in a cacheable and updates the links between in, the lru and the mru.

        :param key: The key to the cacheable we want
        :return: The value that said cacheable contains or NOTEXISTS, if it doesn't exist
        '''

        if self.exists(key):
            key = self._get_hashable_key(key)
            current_cacheable = self.__data[key]
            cc_previous_key = current_cacheable.previous_key
            cc_next_key = current_cacheable.next_key

            if cc_previous_key:
                previous_cacheable = self.__data.get(cc_previous_key)
                previous_cacheable.next_key = cc_next_key if cc_next_key is not None else key
            else:
                self.lru = cc_next_key if cc_next_key is not None else key

            if cc_next_key:
                next_cacheable = self.__data.get(cc_next_key)
                next_cacheable.previous_key = cc_previous_key
                current_cacheable.previous_key = self.mru
                current_cacheable.next_key = None
                mru_value = self.__data.get(self.mru)
                mru_value.next_key = key
                self.mru = key

            self.hits += 1
            return current_cacheable.get_value()

        else:
            self.misses += 1
            return NOTEXISTS

    def _put(self, key: Any, value: Any, expiry: Union[dt.date, None] = None) -> NoReturn:
        '''
        Internal insertion method.

        :param key: The key to the cacheable
        :param value: The value of the cacheable
        :param expiry: The expiration of the cacheable. Setting it to None will make it persistent.
        '''

        new_item = new_cacheable(value, expiry)

        if self.lru is None:
            self.lru = key

        if self.mru is not None:
            mru_value = self.__data.get(self.mru)
            mru_value.next_key = key
            new_item.previous_key = self.mru

        self.mru = key
        self.__data[key] = new_item

    def put(self, key: Any, value: Any, expiry: Union[dt.date, None] = None) -> bool:
        '''
        Inserts a new cacheable in the Cache, updates relevant links, and current size var.
        If max_size has been reached, the lru gets deleted before the insertion.

        :param key: The key to the cacheable
        :param value: The value of the cacheable
        :param expiry: The expiration of the cacheable. Setting it to None will make it persistent.

        :return: Success (cacheable didn't already exist)
        '''
        key = self._get_hashable_key(key)
        if self.exists(key):
            return False
        if self.max_size == self.size:
            self.delete(self.lru)
        self._put(key, value, expiry)
        self.size += 1
        return True

    def update(self, key: Any, value: Any, expiry: Union[dt.date, None] = None) -> bool:
        key = self._get_hashable_key(key)
        if not self.exists(key):
            return False

        self._put(key, value, expiry)
        return True

    def delete(self, key: Any) -> bool:
        '''
        Deletes a specified cacheable and updates relevant links.

        :param key: The key for the cacheable to delete

        :returns: Deletion success (it existed)
        '''

        if not self.exists(key):
            return False

        if self.size == 1: # TODO: Unhardcode this
            self.mru = None

        key = self._get_hashable_key(key)
        current_cacheable: ICacheable = self.__data[key]
        cc_previous_key = current_cacheable.previous_key
        cc_next_key = current_cacheable.next_key
        if cc_previous_key:
            previous_value = self.__data.get(cc_previous_key)
            previous_value.next_key = cc_next_key
        else:
            self.lru = cc_next_key

        if cc_next_key:
            next_value = self.__data.get(cc_next_key)
            next_value.previous_key = cc_previous_key
        else:

            self.mru = cc_previous_key

        del self.__data[key]
        self.size -= 1
        return True

    def exists(self, key: Any) -> bool:
        '''
        Checks if the specified cacheable is in the Cache

        :param key: Key for the cacheable to check
        :return: Does it exist
        '''

        key = self._get_hashable_key(key)

        return key in self.__data.keys()

    def pop(self, key: Any) -> Tuple[Any, bool]:
        '''
        Pops the specified cacheable

        :param key: Key for the cacheable to pop
        :return: the cacheable's value, deletion success (if it existed)
        '''
        cached_val = self.get(key)
        deleted = self.delete(key)
        return cached_val, deleted

    def wipe(self) -> int:
        '''
        Removes all data in the Cache, but keeps statistics

        :return: size of the cache before being wiped
        '''
        pre_wipe_size: int = self.size
        self.__data = {}
        self.lru = None
        self.mru = None
        self.size = 0
        return pre_wipe_size

    def stats(self) -> Dict[Text, NumberType]:
        '''
        Gets the Cache's statistics

        :return: Statistics
        '''
        return {
            "hits": self.hits,
            "misses": self.misses,
            "accesses": self.accesses,
            "last_cleaned": self.last_cleaned,
        }

    def get_cacheable_stats(self, key: Any) -> Dict[Text, Any]:
        '''
        Gets the statistics for the specified cacheable

        :param key: Key to the cacheable we want to get the stats from
        :return: Cacheable's stats
        '''
        key = self._get_hashable_key(key)

        got_cacheable = self.__data.get(key)
        return got_cacheable.stats() if got_cacheable else {}

    def resize(self, new_size: int) -> int:
        '''
        Changes the Cache's maximum size.
        If the new size is less than the current size, lrus get deleted, until they are equal

        :param new_size: New max size to set the Cache to
        :return: Number of items that we deleted to make room
        '''
        num_deleted_items: int = 0

        while new_size < self.size:
            self.delete(self.lru)
            num_deleted_items += 1

        self.max_size = new_size

        return num_deleted_items

    def keys(self) -> KeysView[Any]:  # pragma: no cover
        '''
        :return: A view of the caches' keys
        '''
        return self.__data.keys()

    def values(self) -> ValuesView[Any]:  # pragma: no cover
        '''
        :return: A view of the cacheable values
        '''
        return self.__data.values()

    def items(self) -> ItemsView[Any, ICacheable]:  # pragma: no cover
        '''
        :return: A view of the cache items
        '''
        return self.__data.items()

    def clean(self, cleaning_frequency_s: NumberType) -> NoReturn:
        '''
        Deletes all expired cacheables. Runs in separate thread.

        :param cleaning_frequency_s: Delay between cleaning checks
        '''
        while self._clean_now:
            time.sleep(cleaning_frequency_s)
            current_time = dt.datetime.now()
            for key, cacheable in self.items():
                if cacheable.expires:
                    if cacheable.expiration <= current_time:
                        self.delete(key)
            self.last_cleaned = current_time

    @staticmethod
    def _get_hashable_key(key: Any):
        '''
        Internal hash check. Attempts to hash the key. Casts the key to str(), if the hash fails.

        :param key: The cacheable's key
        :return: A unique string representation of the key
        '''
        try:
            hash(key)
        except TypeError:
            key = str(key)
        return key

    def __repr__(self) -> Text:  # pragma: no cover
        return str(self)

    def __str__(self) -> Text:  # pragma: no cover
        return f"Cache(size=({self.size}/{self.max_size or 'NOMAX'}))"
