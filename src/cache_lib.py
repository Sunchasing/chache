import datetime as dt
import threading
import time
from typing import Text, Dict, Any, Tuple, Union, NoReturn, KeysView, ValuesView, ItemsView

from src.cacheables import ICacheable, NOTEXISTS
from utils import NumberType


class Cache:

    def __init__(self, max_size: Union[int, None] = None,
                 max_mem_size: Union[float, None] = None,
                 cleaning_frequency_s: NumberType = 120):

        self.__data: Dict[Tuple[Any]: ICacheable] = {}
        self.size: Union[int, None] = 0
        self.mem_size: float = 0.
        self.max_mem_size: Union[float, None] = max_mem_size
        self.max_size: int = max_size
        self.last_cleaned: Union[dt.timedelta, None] = None
        self.hits: int = 0
        self.misses: int = 0
        self.lru: Union[Tuple[Any], None] = None
        self.mru: Union[Tuple[Any], None] = None
        self.cleaner_thread: threading.Thread = self._create_cleaner_thread(cleaning_frequency_s)

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
    def data(self) -> Dict[Tuple[Any]: ICacheable]:
        return self.__data

    def get(self, key: Tuple[Any]) -> Any:
        if self.exists(key):
            current_cacheable: ICacheable = self.__data[key]

            if current_cacheable.previous:
                current_cacheable.previous.next = current_cacheable.next if current_cacheable.next is not None else key
            else:
                self.lru = current_cacheable.next if current_cacheable.next is not None else key

            if current_cacheable.next:
                current_cacheable.next.previous = current_cacheable.previous
                current_cacheable.previous = self.mru
                current_cacheable.next = None
                self.mru.next = key
                self.mru = key

            self.hits += 1
            return current_cacheable.get_value()
        else:
            self.misses += 1
            return NOTEXISTS

    def put(self, key: Tuple[Any], value: Any) -> NoReturn:
        if self.max_size == self.size:
            self.delete(self.lru)

        if self.lru is None:
            self.lru = key

        if self.mru is not None:
            self.mru.next = key
        self.mru = key

        self.__data[key] = value
        self.size += 1

    def delete(self, key: Tuple[Any]) -> NoReturn:
        if self.exists(key):
            current_cacheable: ICacheable = self.__data[key]
            if current_cacheable.previous:
                current_cacheable.previous.next = current_cacheable.next
            else:
                self.lru = current_cacheable.next

            if current_cacheable.next:
                current_cacheable.next.previous = current_cacheable.previous
            else:
                self.mru = current_cacheable.previous

            del self.__data[key]
            self.size -= 1

    def exists(self, key: Tuple[Any]) -> bool:
        return key in self.__data.keys()

    def pop(self, key: Tuple[Any]) -> Any:
        cached_val = self.get(key)
        self.delete(key)
        return cached_val

    def wipe(self) -> NoReturn:
        self.__data = {}
        self.lru = None
        self.mru = None
        self.size = 0

    def stats(self) -> Dict[Text: NumberType]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "accesses": self.accesses,
            "last_cleaned": self.last_cleaned,
        }

    def keys(self) -> KeysView[Tuple[Any]]:
        return self.__data.keys()

    def values(self) -> ValuesView[Any]:
        return self.__data.values()

    def items(self) -> ItemsView[Tuple[Tuple[Any], Any]]:
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
        return f"Cache(size=({self.size}/{self.max_size}), memory size=({self.mem_size}/{self.max_mem_size}))"
