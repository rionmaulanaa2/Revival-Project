# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/RefBool.py
from __future__ import print_function

class RefBool(object):

    def __init__(self, default):
        self._ref = 0
        self._default = default

    def __nonzero__(self):
        if self._ref >= 0:
            return self._default
        return not self._default

    def __bool__(self):
        if self._ref >= 0:
            return self._default
        return not self._default

    def ref(self):
        return self._ref

    def enable(self, flag):
        ref = 1 if self._default == flag else -1
        self._ref += ref


class RefTrue(RefBool):

    def __init__(self):
        super(RefTrue, self).__init__(True)


class RefFalse(RefBool):

    def __init__(self):
        super(RefFalse, self).__init__(False)


if __name__ == '__main__':
    a = RefFalse()
    a.enable(False)
    a.enable(False)
    print(bool(a))
    if not a:
        print(111)
    a.enable(True)
    print(bool(a))
    if not a:
        print(222)
    a.enable(True)
    print(bool(a))
    if not a:
        print(333)
    print(bool(a))
    if a:
        print(444)