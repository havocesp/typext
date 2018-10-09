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
from .extensions import install, DEFAULT_FEATURES, EXTRA_FEATURES
from .utils import (cnum, is_flt, is_int, is_num, strfmt_check, redneg, saferun, ctype, fmt, is_str, is_none, not_none)

__all__ = ['cnum', 'is_flt', 'is_int', 'is_num', 'strfmt_check', 'redneg', 'saferun', 'ctype', 'fmt', 'is_str',
           'is_none', 'not_none', 'install', 'DEFAULT_FEATURES', 'EXTRA_FEATURES']
