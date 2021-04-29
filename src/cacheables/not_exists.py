from typing import Any, Dict, Text

from src.cacheables.cacheable_interface import ICacheable


class NotExists(ICacheable):

    def __init__(self):
        super().__init__(None)

    def get_value(self) -> Any:
        raise NotImplementedError

    def stats(self) -> Dict[Text, Any]:
        raise NotImplementedError
