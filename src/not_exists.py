from src.cacheable_interface import ICacheable
from typing import Any, Dict, Text
from utils import Singleton


class NotExists(ICacheable, metaclass=Singleton):

    def __init__(self):
        super().__init__(None)

    def get(self) -> Any:
        raise NotImplementedError

    def stats(self) -> Dict[Text: Any]:
        raise NotImplementedError


NOTEXISTS = NotExists()
