# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/msgpack/__init__.py
from __future__ import absolute_import
from ._version import version
from .exceptions import *
from .embed import *
from collections import namedtuple

class ExtType(namedtuple('ExtType', 'code data')):

    def __new__(cls, code, data):
        if not isinstance(code, int):
            raise TypeError('code must be int')
        if not isinstance(data, bytes):
            raise TypeError('data must be bytes')
        if not 0 <= code <= 127:
            raise ValueError('code must be 0~127')
        return super(ExtType, cls).__new__(cls, code, data)