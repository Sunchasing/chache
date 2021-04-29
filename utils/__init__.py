from decimal import Decimal
from typing import Union, Type
import datetime as dt

NumberType: Type = Union[float, int, complex, Decimal, dt.timedelta]


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls)(*args, **kwargs)
        return cls.__instances[cls]
