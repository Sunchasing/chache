from decimal import Decimal
from typing import Union, Type
import datetime as dt

NumberType: Type = Union[float, int, complex, Decimal, dt.timedelta]
