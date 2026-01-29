# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/Voice.py
from __future__ import absolute_import
from .Item import Item

class Voice(Item):
    __slots__ = ('in_use', )

    def __init__(self, item_id=None, create_time=None):
        super(Voice, self).__init__(item_id, create_time)
        self.in_use = True

    def get_persistent_dict(self):
        d = super(Voice, self).get_persistent_dict()
        d.update({'in_use': self.in_use
           })
        return d

    def get_client_dict(self):
        d = super(Voice, self).get_client_dict()
        d.update({'in_use': self.in_use
           })
        return d

    def is_in_use(self):
        return self.in_use