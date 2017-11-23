from typing import Union

ctype = isinstance

lfmt = lambda self, fmt_: fmt_.format(self)
lcnum = lambda self, ndecims=5: cnum(str(self), ndecims=ndecims)
lnone = lambda self=None: self is None
lnotnone = lambda self=None: self is not None
lcstr = lambda self: str(self)
lctype = lambda self, tp: isinstance(self, tp)


def fmt(self, fmt_: str = '{}'):
    return fmt_.format(self)


def is_strnum(num_as_str):
    import re
    return re.fullmatch(r'[+-]?[0-9]+\.?[0-9]*', str(num_as_str)) is not None


def isint(value: int) -> bool:
    return ctype(value, int)


def isflt(value: float) -> bool:
    return ctype(value, float)


def isnum(value: Union[float, int]) -> bool:
    return ctype(value, (float, int))


def cflt(value: Union[float, int, str]):
    value = str(value).strip()
    if is_strnum(value):
        try:
            value = float(str(value).strip().replace(',', '.'))
        except (ValueError, TypeError) as err:
            value = 0.0
        finally:
            return float(value)
    else:
        raise ValueError('{} is not a valid num'.format(value))


def cnum(value: str, infer_int: bool = True, ndecims: int = 5) -> Union[float, int]:
    _num = round(float(value), ndecims)
    if int(_num) != 0:
        if infer_int and _num % int(_num) == 0:
            _num = int(_num)
    return _num
