import datetime as dt
from typing import Any, Union

from src.cacheables.cacheable import Cacheable
from src.cacheables.cacheable_interface import ICacheable
from src.cacheables.not_exists import NotExists
from src.cacheables.timed_cacheable import TimedCacheable


NOTEXISTS = NotExists()


def new_cacheable(value: Any, expiring: Union[dt.date, None] = None) -> ICacheable:
    '''
    Factory method for the type of cacheable.

    :param value: The value to cache
    :param expiring: The expiration of the cacheable. None for persistent
    :return: An instance of the cacheable type
    '''
    return TimedCacheable(value, expiring) if expiring else Cacheable(value)
