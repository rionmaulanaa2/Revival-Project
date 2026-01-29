# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/msgpack/exceptions.py


class UnpackException(Exception):
    pass


class BufferFull(UnpackException):
    pass


class OutOfData(UnpackException):
    pass


class UnpackValueError(UnpackException, ValueError):
    pass


class ExtraData(ValueError):

    def __init__(self, unpacked, extra):
        self.unpacked = unpacked
        self.extra = extra

    def __str__(self):
        return 'unpack(b) received extra data.'


class PackException(Exception):
    pass


class PackValueError(PackException, ValueError):
    pass