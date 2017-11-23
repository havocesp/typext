#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    ===========================================================================
                            @@@[ TYPEXT ]@@@
    ===========================================================================
    Author:       Daniel J. Umpierrez
    Version:      0.0.1
    License:      MIT
    Created:      23-11-2017
    GitHub:       https://github.com/havocesp/typext
    ===========================================================================
    Description: New methods for some builtin types
    ===========================================================================
"""

import sys
from cmath import nan
from functools import reduce, partial
from itertools import dropwhile, cycle, repeat, takewhile
import operator as op
import json
from collections import OrderedDict as oDict
import re

from term import (red, green, bold, dim, reverse, white, blue, black, yellow, blink, hide, off, magenta, cyan, bgcyan,
                  underscore, bgwhite, bgyellow, bgred, bgmagenta, bggreen, bgblue, bgblack, format as fmt)
from forbiddenfruit import curse as improve
# import all the modules before extending types
import requests

from utils import ctype, lfmt, lcnum, lnone, lnotnone, lcstr, lctype

_JSON_ROOT_TYPES = [dict, list]

_ITERABLE = {tuple, list, set, str, dict, range, map, filter, zip}
_SEQUENCE = {tuple, list, str}
_SIZED = {tuple, list, set, str, dict, range}
_NUMERIC = {int, float}

_FMT_LIKE_LIST = {tuple, list, set, dict, range, map, filter, zip}
_FMT_LIKE_NUM = {int, float, str}

_ALL = {tuple, list, set, str, dict, range, map, filter, zip, int, float, type(None)}

__all__ = ["red", "green", "bold", "dim", "reverse", "white", "blue", "black", "yellow", "blink", "hide",
           "off", "magenta", "cyan", "underscore", "bgwhite", "bgyellow", "bgred", "bgmagenta", "bggreen", "bgblue",
           "bgblack", "bgcyan", 'install']

TERMFMT = oDict({k: (k, v) for k, v in zip(__all__[:-1], [globals()[c] for c in __all__[:-1]])})


def _common():
    """
    Applied to all types.
    """
    for t in _ALL:
        improve(t, "isnull", lnone)
        improve(t, "isnone", lnone)
        improve(t, "is_none", lnone)
        improve(t, "notnull", lnotnone)
        improve(t, "notnone", lnotnone)
        improve(t, "not_none", lnotnone)
        improve(t, "is_null", lnotnone)
        improve(t, "not_null", lnotnone)
        improve(t, "null", lnone)
        improve(t, "cstr", lcstr)
        improve(t, "tostr", lcstr)
        improve(t, "to_str", lcstr)
        improve(t, "to_string", lcstr)
        improve(t, "as_string", lcstr)
        improve(t, "as_str", lcstr)
        improve(t, "istype", lctype)
        improve(t, "type", lctype)
        improve(t, "notype", lambda self, tp: not isinstance(self, tp))
        improve(t, "nontype", lambda self, tp: not isinstance(self, tp))


def generate_colors_funcs():
    """
    Color and format function builder.
    """
    fn_colors_template = """def {fname}(value, b=False):
            _r = fmt(value, {color})
            if b:
                _r = fmt(value, {color}, bold)
            return _r
            """

    for c in __all__:
        fname = c.title()
        if fname.startswith('Bg'):
            fname = 'Bg{}'.format(fname[2:].title())
        exec(fn_colors_template.format(fname=fname, color=c), globals())
        improve(str, fname, globals()[fname])


def _better_formatting():
    generate_colors_funcs()

    improve(str, "cflt", lcnum)
    improve(str, "rnd", lambda self, ndecims=5: round(float(self), ndecims))
    improve(int, "cflt", lcnum)
    improve(float, "cflt", lcnum)
    improve(float, "cint", lambda self: int(self))
    improve(int, "cstr", lambda self: '{:d}'.format(self))
    improve(float, "fmt", lfmt)
    improve(str, "fmt", lfmt)
    improve(int, "fmt", lfmt)

    for t in _FMT_LIKE_NUM:
        improve(t, "fail2color",
                lambda self, cond, tcolor=green, fcolor=red:
                fmt(self, tcolor)
                if cond
                else
                fmt(self, fcolor)
                )
        improve(t, "fraction", lambda self, other: float("{}.{}".format(self, other)))
        improve(t, "redneg", lambda self, fmt_: self.fmt(fmt_).Green() if self.cflt(8) > 0.0 else self.fmt(fmt_).Red())
        improve(t, "percent", lambda self: '{}%'.format(self))
        improve(t, "pct", lambda self: '{}%'.format(self))
        improve(t, "symb", lambda self, symb: '{} {}'.format(self, symb))

    for t in _FMT_LIKE_LIST:
        improve(t, "fmt", lambda self, fmt_: list(map(lambda q: fmt_.format(q), self)))


def _numbers():
    for t in _NUMERIC:
        improve(t, "isneg", lambda self: float(self) < 0.0)
        improve(t, "ispos", lambda self: float(self) > 0.0)
        improve(t, "iszero", lambda self: float(self) == 0.0)
        improve(t, "nonzero", lambda self: float(self) != 0.0)
        improve(t, "rnd", lambda self, ndecims=2: round(self, ndecims) if ctype(self, float) else self)


def _functional_iterables():
    improve(dict, "merge", lambda self, other: {**self, **other})

    for t in _SIZED:
        improve(t, "size", lambda self: len(self) if hasattr(self, "__len__") else len(list(self)))
        improve(t, "len", lambda self: len(self) if hasattr(self, "__len__") else len(list(self)))
        improve(t, "length", lambda self: len(self) if hasattr(self, "__len__") else len(list(self)))
        improve(t, "empty", lambda self: len(self) <= 0)
        improve(t, "notempty", lambda self: len(self) > 0)
        improve(t, "noempty", lambda self: len(self) > 0)
        improve(t, "no_empty", lambda self: len(self) > 0)
        improve(t, "not_empty", lambda self: len(self) > 0)

    for t in _ITERABLE:
        improve(t, "map", lambda self, f: map(f, self))
        improve(t, "filter", lambda self, f: filter(f, self))
        improve(t, "reduce", lambda self, f: reduce(f, self))

        # improve(t, "join", lambda self, sep: reduce(lambda a, b: a + [sep] + b, self).reduce(op.add))

        improve(t, "any", lambda self, f=None: any(self) if f is None else any(map(f, self)))
        improve(t, "exists", lambda self, f=None: any(self) if f is None else any(map(f, self)))
        improve(t, "all", lambda self, f=None: all(self) if f is None else all(map(f, self)))
        improve(t, "every", lambda self, f=None: all(self) if f is None else all(map(f, self)))

        improve(t, "contains", lambda self, q=None: q in self)

        improve(t, "min", lambda self: min(self))
        improve(t, "max", lambda self: max(self))
        improve(t, "avg", lambda self: sum(self) / len(self) if len(self) > 0 else nan)

        improve(t, "sum", lambda self: reduce(op.add, self))
        improve(t, "product", lambda self: reduce(op.mul, self))

    for t in _SEQUENCE:
        improve(t, "head", lambda self: self[0])
        improve(t, "first", lambda self: self[0])
        improve(t, "last", lambda self: self[-1])

        improve(t, "init", lambda self: self[:-1])
        improve(t, "tail", lambda self: self[1:])

        improve(t, "drop", lambda self, n: self[n:])
        improve(t, "take", lambda self, n: self[:n])

        improve(t, "dropwhile", lambda self, f: dropwhile(f, self))
        improve(t, "takewhile", lambda self, f: takewhile(f, self))

        improve(t, "cycle", lambda self: cycle(self))
        improve(t, "repeat", lambda self, n=None: repeat(self, None))

        improve(t, "reversed", lambda self: reversed(self))
        improve(t, "sorted", lambda self: sorted(self))

        improve(t, "zip", lambda self, other: zip(self, other))
        improve(t, "unzip", lambda self: zip(*self))
        improve(t, "index_zip", lambda self, other: zip(range(len(self)), self))
        improve(t, "traspose",
                lambda self: [zip(**self)] if ctype(self, list) and ctype(self[0], (dict, tuple)) else self)


def _json():
    improve(str, "json", property(lambda self: json.loads(self)))
    for t in _JSON_ROOT_TYPES:
        improve(t, "asjson", property(lambda self: json.dumps(self)))


def _requests():
    class RequestsWrapper(object):

        def __init__(self, url):
            self.url = url

        get = property(lambda self: partial(requests.get, self.url))
        post = property(lambda self: partial(requests.post, self.url))
        head = property(lambda self: partial(requests.head, self.url))
        options = property(lambda self: partial(requests.options, self.url))

    improve(str, "request", property(lambda self: RequestsWrapper(self)))
    improve(str, "fetch", property(lambda self: requests.get(self).text))


DEFAULT_FEATURES = [
    "common",
    "better_formatting",
    "functional_iterables",
    "numbers"
]
EXTRA_FEATURES = [
    "easter_eggs",
    "json",
    "requests",
]


class Installer(list):
    """Manages installed features."""

    def install(self, feature):
        if feature not in self:
            try:
                installer = getattr(sys.modules[__name__], "_" + feature)
            except AttributeError:
                raise ValueError("Invalid feature: '{}'".format(feature))
            installer()
            self.append(feature)


installer = Installer()


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
        raise ValueError("Extras must be either bool or list")
    for feature in features:
        if feature not in DEFAULT_FEATURES + EXTRA_FEATURES:
            raise ValueError("Unknown feature: '{}'".format(feature))
        installer.install(feature)


def strfmt_check(strftm: str):
    regex = r'^{(:(.[><^]|[><^])?(\+?[0-9]*(\.[0-9]+f|d)?|[0-9]*)?)?}$'
    return re.fullmatch(regex, strftm) is not None


if __name__ == '__main__':
    install()
    a = 1
    print(a.fmt('{:+d}'))
