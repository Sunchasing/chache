import datetime
from typing import Text, NoReturn

debug_enabled = True


def _log(statement: Text, severity: Text) -> NoReturn:
    print(f'[{datetime.datetime.now()}][{severity}] {statement}')


def debug(statement: Text):
    if debug_enabled:
        _log(statement=statement, severity='DEBUG')


def error(statement: Text):
    _log(statement=statement, severity='ERROR')


def info(statement: Text):
    _log(statement=statement, severity='INFO')
