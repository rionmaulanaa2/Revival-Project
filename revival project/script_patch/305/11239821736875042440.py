# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/UnitShareData.py
from __future__ import absolute_import
import six
from mobile.common.mobilecommon import singleton

def dummy_func(*args, **kwargs):
    return None


class UnitShareData(object):

    def __init__(self):
        self.ecs_mask = 0

    def __getattr__(self, item):
        if item.startswith('ev_g'):
            setattr(self, item, dummy_func)
        elif item.startswith('ref_'):
            setattr(self, item, None)
        else:
            name = self.__class__.__name__
            raise AttributeError("'%s' object has no attribute '%s'" % (name, item))
        return self.__dict__[item]

    def merge(self, other):
        for key, val in six.iteritems(other.__dict__):
            if key.startswith('ref_') or key.startswith('ev_g'):
                if getattr(self, key, None) is not None and val is None:
                    continue
                setattr(self, key, val)

        return


@singleton
class UnitShareDataDummy(object):

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        return None


DUMMY_SHARE_DATA = UnitShareDataDummy()