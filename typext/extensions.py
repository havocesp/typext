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
import json
import operator as op
import sys
from collections import OrderedDict
from functools import reduce, partial
from itertools import dropwhile, cycle, repeat, takewhile
from math import nan
from typing import Iterable
from urllib.parse import urljoin

import requests
from forbiddenfruit import curse as improve
from term import (
    red, green, bold, dim, reverse, white, blue, black, yellow, blink, hide, off, magenta, cyan, bgcyan, underscore,
    bgwhite, bgyellow, bgred, bgmagenta, bggreen, bgblue, bgblack, format as fmt
)

from .utils import cnum, redneg

_JSON_ROOT_TYPES = [dict, list]
_ITERABLE = {tuple, list, set, str, dict, range, map, filter, zip}
_SEQUENCE = {tuple, list, str}
_SIZED = {tuple, list, set, str, dict, range}
_NUMERIC = {int, float, str}
_FMT_LIKE_LIST = {tuple, list, set, dict, range, map, filter, zip}
_FMT_LIKE_NUM = {int, float, str}
_ALL = {tuple, list, set, str, dict, range, map, filter, zip, int, float, type(None)}

# aliases
ctype = isinstance

__all__ = ['red', 'green', 'bold', 'dim', 'reverse', 'white', 'blue', 'black',
           'yellow', 'blink', 'hide', 'off', 'magenta', 'cyan', 'underscore',
           'bgwhite', 'bgyellow', 'bgred', 'bgmagenta', 'bggreen', 'bgblue',
           'bgblack', 'bgcyan', 'install']

TERMFMT = OrderedDict({k: (k, v) for k, v in zip(__all__[:-1], [globals()[c] for c in __all__[:-1]])})

DEFAULT_FEATURES = ['common', 'better_formatting', 'functional_iterables', 'numbers']
EXTRA_FEATURES = ['easter_eggs', 'json', 'requests']


class Installer(list):
    """
    Manages installed features.
    """
    _debug_mode = False

    def install(self, feature, debug: bool = False):

        self._debug_mode = debug

        if feature not in self:

            try:
                installer = getattr(sys.modules[__name__], '_' + feature)

            except AttributeError:
                raise ValueError('Invalid feature: {}'.format(feature))

            installer()
            self.append(feature)

    @property
    def debug(self):
        return self._debug_mode

    @debug.setter
    def debug(self, modeflag: bool):
        self._debug_mode = modeflag


installer = Installer()


def _common():
    """
    Generic extensions usable by most types
    """
    for t in _ALL:
        improve(t, 'isnull', lambda self=None: self is None)
        improve(t, 'isnone', lambda self=None: self is None)
        improve(t, 'is_none', lambda self=None: self is None)
        improve(t, 'notnull', lambda self=None: self is not None)
        improve(t, 'notnone', lambda self=None: self is not None)
        improve(t, 'not_none', lambda self=None: self is not None)
        improve(t, 'is_null', lambda self=None: self is not None)
        improve(t, 'not_null', lambda self=None: self is not None)
        improve(t, 'null', lambda self=None: self is None)
        improve(t, 'cstr', lambda self: str(self))
        improve(t, 'tostr', lambda self: str(self))
        improve(t, 'to_str', lambda self: str(self))
        improve(t, 'to_string', lambda self: str(self))
        improve(t, 'as_string', lambda self: str(self))
        improve(t, 'as_str', lambda self: str(self))
        improve(t, 'istype', lambda self, tp: isinstance(self, tp))
        improve(t, 'type', lambda self, tp: isinstance(self, tp))
        improve(t, 'notype', lambda self, tp: not isinstance(self, tp))
        improve(t, 'nontype', lambda self, tp: not isinstance(self, tp))


def generate_colors_funcs():
    """
    Generate color extensions functions dynamically
    :return:
    """
    fn_colors_template = """
def {fname}(
    value, 
    set_bold=False, 
    set_uline=False, 
    set_dim=False, 
    fmt_='{fmt}'):

        modifiers = list()

        if set_bold:
            modifiers.append(bold)

        elif set_dim:
            modifiers.append(dim)

        if set_uline:
            modifiers.append(underscore)

        modifiers.append({color})
        return fmt(fmt_.format(value), {color}, *modifiers)
"""

    for c in __all__:  # TODO comprobar si va __all__[:-1] en lugar de __all__

        fname = c.title()

        if fname.startswith('Bg'):
            fname = 'Bg{}'.format(fname[2:].title())
        fncode = fn_colors_template.format(fname=fname, color=c, fmt='{}')

        exec(fncode, globals())

        improve(str, fname, globals()[fname])
        improve(float, fname, globals()[fname])
        improve(int, fname, globals()[fname])


def _better_formatting():
    # Generate colors extensios like 'mi_string_var.Blue()'
    generate_colors_funcs()

    improve(str, 'rnd', lambda self, ndecims=2: str('{:.' + '{}'.format(ndecims) + 'f}').format(float(self)))
    improve(int, 'cflt', lambda self, ndecims=5: cnum(str(self), ndecims=ndecims))
    improve(str, 'cflt', lambda self, ndecims=5: cnum(self, ndecims=ndecims))
    improve(float, 'cflt', lambda self, ndecims=5: cnum(str(self), ndecims=ndecims))
    improve(float, 'cint', lambda self: int(self))
    improve(float, 'cstr', lambda self, fmt_='{:.f}': fmt_.format(self))
    improve(int, 'cstr', lambda self, fmt_='{:d}': fmt_.format(self))
    improve(float, 'fmt', lambda self, fmt_='{:8f}': fmt_.format(self))
    improve(str, 'fmt',
            lambda self, fmt_='{}': fmt_.format(cnum(self)) if fmt_.rtrim()[:-2] in ['f}', 'd}'] else fmt_.format(self))
    improve(int, 'fmt', lambda self, fmt_='{:d}': fmt_.format(self))

    for t in _FMT_LIKE_NUM:
        improve(t, 'fail2color',
                lambda self, cond, tcolor=green, fcolor=red: fmt(self, tcolor) if cond else fmt(self, fcolor))
        improve(t, 'fraction', lambda self, other: cnum('{}.{}'.format(self, other)))
        improve(t, 'redneg', lambda self, fmt_='{.f}': redneg(cnum(self), fmt_=fmt_))
        improve(t, 'percent', lambda self, ndecims=2: str('{.' + str(ndecims) + 'f}%').format(self))
        improve(t, 'pct', lambda self, ndecims=2: str('{.' + str(ndecims) + 'f}%').format(self))
        improve(t, 'symb', lambda self, symb: '{} {}'.format(self, symb))

    for t in _FMT_LIKE_LIST:
        improve(t, 'fmt', lambda self, fmt_: list(map(lambda q: fmt_.format(q), self)))


def _numbers():
    _NUMERIC.add(str)
    for t in _NUMERIC:
        improve(t, 'isneg', lambda self: cnum(self) < 0.0)
        improve(t, 'neg', lambda self: cnum(self) < 0.0)
        improve(t, 'ispos', lambda self: cnum(self) > 0.0)
        improve(t, 'pos', lambda self: cnum(self) > 0.0)
        improve(t, 'iszero', lambda self: cnum(self) == 0.0)
        improve(t, 'zero', lambda self: cnum(self) == 0.0)
        improve(t, 'nonzero', lambda self: cnum(self) != 0.0)
        improve(t, 'nozero', lambda self: cnum(self) != 0.0)
        improve(t, 'percent', lambda self, percent, precision=5: cnum(self) * (1.0 + cnum(percent, precision)))
        improve(t, 'rnd', lambda self, ndecims=8: cnum(self, ndecims))
        improve(t, 'abs', lambda self: cnum(self) * -1.0 if cnum(self) < 0.0 else cnum(self))


def _functional_iterables():
    improve(dict, 'merge', lambda self, other: {**self, **other})

    for t in _SIZED:
        improve(t, 'count', lambda self: len(self) if hasattr(self, '__len__') else len(list(self)))
        improve(t, 'size', lambda self: len(self) if hasattr(self, '__len__') else len(list(self)))
        improve(t, 'len', lambda self: len(self) if hasattr(self, '__len__') else len(list(self)))
        improve(t, 'length', lambda self: len(self) if hasattr(self, '__len__') else len(list(self)))
        improve(t, 'empty', lambda self: len(self) <= 0)
        improve(t, 'notempty', lambda self: len(self) > 0)
        improve(t, 'noempty', lambda self: len(self) > 0)
        improve(t, 'no_empty', lambda self: len(self) > 0)
        improve(t, 'not_empty', lambda self: len(self) > 0)

    for t in _ITERABLE:
        improve(t, 'map', lambda self, f: map(f, self))
        improve(t, 'filter', lambda self, f: filter(f, self))
        improve(t, 'reduce', lambda self, f: reduce(f, self))
        improve(t, 'any', lambda self, f=None: any(self) if f is None else any(map(f, self)))
        improve(t, 'exists', lambda self, f=None: any(self) if f is None else any(map(f, self)))
        improve(t, 'all', lambda self, f=None: all(self) if f is None else all(map(f, self)))
        improve(t, 'every', lambda self, f=None: all(self) if f is None else all(map(f, self)))
        improve(t, 'contains', lambda self, q=None: q in self)
        improve(t, 'min', lambda self: min(self))
        improve(t, 'max', lambda self: max(self))
        improve(t, 'avg', lambda self: sum(self) / len(self) if len(self) > 0 else nan)
        improve(t, 'sum', lambda self: reduce(op.add, self))
        improve(t, 'product', lambda self: reduce(op.mul, self))

    for t in _SEQUENCE:
        improve(t, 'head', lambda self: self[0])
        improve(t, 'first', lambda self: self[0])
        improve(t, 'last', lambda self: self[-1])
        improve(t, 'init', lambda self: self[:-1])
        improve(t, 'tail', lambda self: self[1:])
        improve(t, 'drop', lambda self, n: self[n:])
        improve(t, 'take', lambda self, n: self[:n])
        improve(t, 'dropwhile', lambda self, f: dropwhile(f, self))
        improve(t, 'takewhile', lambda self, f: takewhile(f, self))
        improve(t, 'cycle', lambda self: cycle(self))
        improve(t, 'repeat', lambda self, n=None: repeat(self, None))
        improve(t, 'reversed', lambda self: reversed(self))
        improve(t, 'sorted', lambda self: sorted(self))
        improve(t, 'zip', lambda self, other: zip(self, other))
        improve(t, 'unzip', lambda self: zip(*self))
        improve(t, 'index_zip', lambda self, other: zip(range(len(self)), self))
        improve(t, 'traspose', lambda self: [zip(*self)] if ctype(self, Iterable) else self)


def _json():
    improve(str, 'json', property(lambda self: cnum(json.loads(self))))
    for t in _JSON_ROOT_TYPES:
        improve(t, 'to_json', property(lambda self: json.dumps(self)))
        improve(t, 'as_json', property(lambda self: json.dumps(self)))


def _requests():
    class RequestsWrapper:

        def __init__(self, url: str, **params):
            self.url = urljoin(url, params)

        get = property(lambda self: partial(requests.get, self.url))
        post = property(lambda self, **kwargs: partial(requests.post, self.url, **kwargs))
        head = property(lambda self: partial(requests.head, self.url))
        options = property(lambda self: partial(requests.options, self.url))

    improve(str, 'request', property(lambda self: RequestsWrapper(self)))
    improve(str, 'fetch', property(lambda self: requests.get(self).text))
    improve(str, 'get_json', property(lambda self: cnum(requests.get(self).json())))


def install(extras=False):
    features = DEFAULT_FEATURES[:]

    if isinstance(extras, bool):
        if extras:
            features += EXTRA_FEATURES[:]

    elif isinstance(extras, (tuple, list)):
        features += extras[:]

    elif isinstance(extras, str):
        features += [extras]

    else:
        raise ValueError('Extras must be either bool or list')

    for feature in features:
        if feature not in DEFAULT_FEATURES + EXTRA_FEATURES:
            raise ValueError('Unknown feature: {}'.format(feature))

        installer.install(feature)
