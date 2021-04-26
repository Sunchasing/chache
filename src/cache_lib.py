import datetime as dt
import json
from typing import Text, Dict, Any, Tuple, Union, NoReturn, Set, Iterable

from src.cacheables import ICacheable, NOTEXISTS
from utils import NumberType


class Cache:

    def __init__(self, max_size: Union[int, None] = None, max_mem_size: Union[float, None] = None):
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
                current_cacheable.previous.next = current_cacheable.next or current_cacheable
            else:
                self.lru = current_cacheable.next or current_cacheable

            if current_cacheable.next:
                current_cacheable.next.previous = current_cacheable.previous
                current_cacheable.previous = self.mru
                current_cacheable.next = None
                self.mru.next = current_cacheable
                self.mru = current_cacheable

            self.hits += 1
            return current_cacheable.get_value()
        else:
            self.misses += 1
            return NOTEXISTS

    def put(self, key: Tuple[Any], value: Any) -> NoReturn:
        if self.max_size == self.size:
            self.delete(self.lru)
        self.__data[key] = value
        self.size += 1

    def clean(self) -> int:
        raise NotImplementedError

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
        raise NotImplementedError

    def keys(self) -> Set[Tuple[Any]]:
        raise NotImplementedError

    def values(self) -> Set[Any]:
        raise NotImplementedError

    def items(self) -> Iterable[Tuple[Tuple[Any], Any]]:
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __str__(self) -> Text:
        return json.dumps(self.stats(), indent=4)
