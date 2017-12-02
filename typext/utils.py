import re
from typing import Union, Callable

from term import green, red, dim, format as fmt
from decorator import decorator


ctype = isinstance

lfmt = lambda self, fmt_: fmt_.format(self)
lcnum = lambda self, ndecims = 5: cnum(str(self), ndecims = ndecims)
lnone = lambda self = None: self is None
lnotnone = lambda self = None: self is not None
lcstr = lambda self: str(self)
lctype = lambda self, tp: isinstance(self, tp)


@decorator
def saferun(fn: Callable, *args, **kwargs):
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
def _redneg(value, fmt_: str) -> str:
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


def strfmt_check(strftm: str):
    regex = r'^{(:(.[><^]|[><^])?(\+?[0-9]*(\.[0-9]+f|d)?|[0-9]*)?)?}$'

    return re.fullmatch(regex, strftm) is not None


def isint(value: int) -> bool:
    return ctype(value, int)


def isflt(value: float) -> bool:
    return ctype(value, float)


def isnum(value: Union[float, int]) -> bool:
    return ctype(value, (float, int))


def cnum(value: str, infer_int: bool = True, ndecims: int = 5) -> Union[float, int]:
    _num = round(float(value), ndecims)

    if int(_num) != 0:
        if infer_int and _num % int(_num) == 0:
            _num = int(_num)
    return _num
