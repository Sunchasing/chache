from abc import ABCMeta, abstractmethod
from typing import Any, Tuple, Union, Dict, Text


class ICacheable(metaclass=ABCMeta):

    expires: bool

    def __init__(self, value: Any):
        self.value: Any = value
        self.hits: int = 0
        self.mem_size: float
        self.value_mem_size: float
        self._previous: Union[Tuple[Any], None] = None
        self._next: Union[Tuple[Any], None] = None

    @abstractmethod
    def get(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> Dict[Text: Any]:
        raise NotImplementedError
