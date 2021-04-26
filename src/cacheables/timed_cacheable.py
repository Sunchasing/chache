from typing import NoReturn
import datetime as dt
from src.cacheables.cacheable import Cacheable


class TimedCacheable(Cacheable):
    expires = True

    def __init__(self, value, expiration: dt.date):
        super().__init__(value)
        self.expiration: dt.date = expiration

    def get_value(self):
        self.hits += 1
        return self.value

    def stats(self):
        return {
            "hits": self.hits,
            "mem_size": self.mem_size,
            "val_size": self.value_mem_size,
            "expiry": None
            }

    def set_expiration_to(self, expiration_date: dt.datetime) -> NoReturn:
        self.expiration = expiration_date

    def update_expiration_by(self, time_span: dt.timedelta) -> NoReturn:
        self.expiration += time_span

    def _compute_mem_sizes(self):
        ...
