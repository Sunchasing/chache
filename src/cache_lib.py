import datetime as dt
from typing import Text, Dict, Any, Tuple, Union, NoReturn, Set, Iterable

from src.cacheables import ICacheable
from utils import NumberType


class Cache():

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

    @property
    def accesses(self) -> int:
        return self.hits + self.misses

    @property
    def data(self) -> Dict[Tuple[Any]: ICacheable]:
        return self.__data
    
    def get(self, key: Tuple[Any]) -> Any:
        raise NotImplementedError

    def put(self, key: Tuple[Any], value: Any) -> NoReturn:
        raise NotImplementedError

    def clean(self) -> int:
        raise NotImplementedError

    def delete(self, key: Tuple[Any]) -> NoReturn:
        raise NotImplementedError

    def exists(self, key: Tuple[Any]) -> bool:
        raise NotImplementedError

    def pop(self, key: Tuple[Any]) -> Any:
        raise NotImplementedError

    def wipe(self) -> NoReturn:
        raise NotImplementedError

    def stats(self) -> Dict[Text: NumberType]:
        raise NotImplementedError

    def keys(self) -> Set[Tuple[Any]]:
        raise NotImplementedError

    def values(self) -> Set[Any]:
        raise NotImplementedError

    def items(self) -> Iterable[Tuple[Tuple[Any], Any]]:
        raise NotImplementedError
