from abc import ABCMeta, abstractmethod
from typing import Any, Union, Dict, Text


class ICacheable(metaclass=ABCMeta):
    expires: bool

    def __init__(self, value: Any):
        '''

        :param value: The value to be stored in this cacheable
        '''
        self.value: Any = value
        self.hits: int = 0
        self.previous_key: Union[Any, None] = None
        self.next_key: Union[Any, None] = None

    @abstractmethod
    def get_value(self) -> Any:
        '''
        Updates stats and returns the value stored in this cacheable

        :return: The value in this cacheable
        '''
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> Dict[Text, Any]:
        '''
        Returns cache statistics

        :return: The times this cacheable's value has been called and the expiration
        '''
        raise NotImplementedError

    @property
    def __name(self) -> Text:
        raise NotImplementedError

    def __str__(self) -> Text:
        return f"{self.__name}(value={self.value}, expires={self.expires})"
