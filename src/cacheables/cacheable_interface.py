from abc import ABCMeta, abstractmethod
from typing import Any, Tuple, Union, Dict, Text, NoReturn


class ICacheable(metaclass=ABCMeta):

    expires: bool

    def __init__(self, value: Any):
        self.value: Any = value
        self.hits: int = 0
        self.previous: Union[Tuple[Any], None] = None
        self.next: Union[Tuple[Any], None] = None

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> Dict[Text: Any]:
        raise NotImplementedError
