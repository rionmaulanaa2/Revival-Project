# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/BaseDataType.py
from __future__ import absolute_import
import six

class BaseDataType(object):

    def __init__(self):
        super(BaseDataType, self).__init__()

    def init_from_dict(self, bdict=None):
        if bdict is None:
            bdict = {}
        for k, v in six.iteritems(bdict):
            if not hasattr(self, k):
                continue
            setattr(self, k, v)

        return

    def to_dict(self):
        d = {}
        for k, v in six.iteritems(self.__dict__):
            if hasattr(v, '__call__'):
                continue
            d[k] = v

        return d