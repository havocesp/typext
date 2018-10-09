# -*- coding: utf-8 -*-
"""
    ===========================================================================
                            @@@[ PyExt ]@@@
    ===========================================================================
    Author:       Daniel J. Umpierrez
    Version:      0.1.3
    License:      UNLICENSE
    Created:      01-01-2017
    GitHub:       https://github.com/havocesp/typext
    ===========================================================================
    Description: builtin extended version/typext
    ===========================================================================
"""
import re
from decimal import Decimal
from typing import Union, Callable, Iterable, Mapping

from decorator import decorator
from term import green, red, dim, format as fmt

ctype = isinstance


def lfmt(self, fmt_):
    return fmt_.format(self)


def is_none(self=None):
    return self is None


def not_none(self=None):
    return self is not None


def is_str(self):
    return str(self)


@decorator
def saferun(fn: Callable, *args, **kwargs):
    """
    Decorator to intercept possible Exceptions types (supplied as args) raised on decorated function.

    :param fn: the callable decorated by this function
    :param args: Exceptions to catch during callable execution
    :param kwargs:  Exceptions to catch during callable execution

    """
    result = None
    exceptions = list()

    if args and len(args) > 0:

        for exception in args:

            if isinstance(exception, BaseException):
                exceptions = [exception]

        if len(exceptions) > 0:
            try:
                result = fn(*args, **kwargs)
            except exceptions as err:
                errmsg = kwargs.get('errmsg')
                print(errmsg if errmsg else str(err))
        else:
            result = fn(*args, **kwargs)
    return result


@saferun
def redneg(value, fmt_: str) -> str:
    """
    Takes a value and return a it colored as red if value is negative or green if positive.
    :param value: value to be colored
    :param fmt_: overrides default return format string
    :return: value as red string if negative or green if positive
    """
    result = round(float(value), 8)

    if result > 0.0:
        result = fmt(fmt_.format(result), green)

    elif result < 0.0:
        result = fmt(fmt_.format(result), red)

    elif result == 0.0:
        result = fmt(fmt_.format(result), dim)

    else:
        result = value

    return result


def strfmt_check(strfmt: str) -> bool:
    """
    String modern string format validator
        - Ex. {:.2f} or {:_^})

    :param strfmt: format to be validate
    :return: True if no errors
    """
    regex = r'^{(:(.[><^]|[><^])?(\+?[0-9]*(\.[0-9]+f|d)?|[0-9]*)?)?}$'
    return re.fullmatch(regex, strfmt) is not None


def is_int(value: int) -> bool:
    """
    Integer built-in checker.

    :param value: value to be checked
    :return: True if value is type int
    """
    return ctype(value, int)


def is_flt(value: float) -> bool:
    """
    Float built-in checker.

    :param value: value to be checked
    :return: True if value is type float
    """
    return ctype(value, float)


def is_num(value: Union[float, int]) -> bool:
    """
    Check if value is a number or not.

    :param value: value to be checked
    :return: True if value is a num type (int, float)
    """
    return ctype(value, (float, int, Decimal))


def _num_parser(value, ndecims: 8):
    if isinstance(value, Decimal):
        value = float(value)
    strval = str(value)
    try:
        if '.' in strval or 'e' in strval.lower():
            r = round(float(strval), ndecims)
        else:
            try:
                r = int(strval)
            except ValueError:
                r = round(float(strval), ndecims)
    except ValueError:
        r = value
    return r


def cnum(data: Union[Iterable, int, float, Decimal], ndecims: int = 8) -> Union[Iterable, Mapping, float, int]:
    """
    Data type infer and parser.

    Accept any Iterable (dict, list, tuple, set, ...) or built-in data types int, float, str, ... and try  to
    convert it a number data type (int, float)
    """
    r = None

    if isinstance(data, str):
        r = _num_parser(data, ndecims)
    elif isinstance(data, Mapping):
        for k, v in data.items():
            r = v
            if isinstance(v, Iterable):
                r = {k: cnum(v, ndecims)}
    elif isinstance(data, Iterable):
        for n in data:
            r = [*n]
            if isinstance(n, Iterable):
                r = [*cnum(n, ndecims)]
    else:
        r = _num_parser(str(data), ndecims)
    return r
