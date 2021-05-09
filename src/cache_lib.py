import datetime as dt
import threading
import time
from typing import Text, Dict, Any, Union, NoReturn, KeysView, ValuesView, ItemsView, Callable

from src.cacheables import ICacheable, NOTEXISTS, new_cacheable
from utils import NumberType


class Cache:

    __func_caches: Dict[Text, 'Cache'] = {}

    def __init__(self, max_size: int, cleaning_frequency_s: NumberType):

        self.__data: Dict[Any, ICacheable] = {}
        self.size: int = 0
        self.max_size: Union[int, None] = max_size
        self.last_cleaned: Union[dt.timedelta, None] = None
        self.hits: int = 0
        self.misses: int = 0
        self.lru: Union[Any, None] = None
        self.mru: Union[Any, None] = None
        self.cleaner_thread: threading.Thread = self._create_cleaner_thread(cleaning_frequency_s)

    @classmethod
    def _get_func_cache(cls, func: Callable,
                        max_size: Union[int, None],
                        cleaning_frequency_s: NumberType) -> 'Cache':
        ret = cls.__func_caches.get(func.__name__)
        if not ret:
            ret = Cache(max_size=max_size, cleaning_frequency_s=cleaning_frequency_s)
            cls.__func_caches[func.__name__] = ret
        return ret

    @classmethod
    def sized_func_cache(cls, expiry: dt.date = None,
                         max_size: Union[int, None] = None,
                         cleaning_frequency_s: NumberType = 120) -> Callable:

        def inner(func: Callable) -> Callable:
            cache = cls._get_func_cache(func, max_size, cleaning_frequency_s)

            def wrapper(*args, **kwargs):
                key = args + tuple(kwargs.values())
                rv = cache.get(key)
                if rv == NOTEXISTS:
                    rv = func(*args, **kwargs)
                    cache.put(key, rv, expiry)
                wrapper.cache_stats = cache.stats()
                if not hasattr(wrapper, 'wipe_cache'):
                    wrapper.wipe_cache = cache.wipe
                return rv

            return wrapper
        return inner

    def _create_cleaner_thread(self, cleaning_frequency_s: NumberType) -> threading.Thread:
        mister_clean = threading.Thread(target=self.clean,
                                        name="cache_cleaner_thread",
                                        args=(cleaning_frequency_s,),
                                        daemon=True)
        mister_clean.start()
        return mister_clean

    @property
    def accesses(self) -> int:
        return self.hits + self.misses

    @property
    def data(self) -> Dict[Any, ICacheable]:
        return self.__data

    def get(self, key: Any) -> Any:
        if self.exists(key):
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

    def put(self, key: Any, value: Any, expiry: Union[dt.date, None] = None) -> NoReturn:
        new_item = new_cacheable(value, expiry)

        if self.max_size == self.size:
            self.delete(self.lru)

        if self.lru is None:
            self.lru = key

        if self.mru is not None:
            mru_value = self.__data.get(self.mru)
            mru_value.next_key = key
            new_item.previous_key = self.mru

        self.mru = key
        self.__data[key] = new_item
        self.size += 1

    def delete(self, key: Any) -> NoReturn:
        if self.exists(key):
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

    def exists(self, key: Any) -> bool:
        return key in self.__data.keys()

    def pop(self, key: Any) -> Any:
        cached_val = self.get(key)
        self.delete(key)
        return cached_val

    def wipe(self) -> NoReturn:
        self.__data = {}
        self.lru = None
        self.mru = None
        self.size = 0

    def stats(self) -> Dict[Text, NumberType]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "accesses": self.accesses,
            "last_cleaned": self.last_cleaned,
        }

    def resize(self, new_size: int) -> NoReturn:
        while new_size < self.size:
            self.delete(self.lru)
        self.max_size = new_size

    def keys(self) -> KeysView[Any]:
        return self.__data.keys()

    def values(self) -> ValuesView[Any]:
        return self.__data.values()

    def items(self) -> ItemsView[Any, ICacheable]:
        return self.__data.items()

    def clean(self, cleaning_frequency_s: NumberType) -> NoReturn:
        time.sleep(cleaning_frequency_s)
        current_time = dt.datetime.now()
        for key, cacheable in self.__data.items():
            if cacheable.expires:
                if cacheable.expiration >= current_time:
                    self.delete(key)
        self.last_cleaned = current_time

    def __repr__(self) -> Text:
        return str(self)

    def __str__(self) -> Text:
        return f"Cache(size=({self.size}/{self.max_size or 'NOMAX'}))"
