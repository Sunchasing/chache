import datetime as dt
from typing import NoReturn

from src.cacheables.cacheable import Cacheable


class TimedCacheable(Cacheable):
    expires = True

    def __init__(self, value, expiration: dt.date):
        '''
        :param value: The value to be stored in this cacheable
        :param expiration: The expiration time
        '''
        super().__init__(value)
        self.expiration: dt.date = expiration

    def get_value(self):
        self.hits += 1
        return self.value

    def stats(self):
        return {
            "hits": self.hits,
            "expiry": self.expiration
        }

    def set_expiration_to(self, expiration_date: dt.datetime) -> NoReturn:
        '''
        Sets the expiration of this cacheable

        :param expiration_date: The new expiration of the cacheable
        '''
        self.expiration = expiration_date

    def update_expiration_by(self, time_span: dt.timedelta) -> NoReturn:
        '''
        Extends the cacheable's expiration

        :param time_span: The time to add to the current expiration
        '''
        self.expiration += time_span

    @property
    def __name(self):  # pragma: no cover
        return "TimedCacheable"
