# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/Mecha.py
from __future__ import absolute_import
from .Item import Item

class Mecha(Item):
    __slots__ = ('fashion', 'sfx', 'action')

    def __init__(self, item_id=None, create_time=None):
        super(Mecha, self).__init__(item_id, create_time)
        self.fashion = {}
        self.sfx = None
        self.action = None
        return

    def get_persistent_dict(self):
        d = super(Mecha, self).get_persistent_dict()
        d.update({'fashion': self.fashion,
           'sfx': self.sfx,
           'action': self.action
           })
        return d

    def get_client_dict(self):
        d = super(Mecha, self).get_client_dict()
        d.update({'fashion': self.fashion,
           'sfx': self.sfx,
           'action': self.action
           })
        return d

    def get_fashion(self):
        if not G_IS_CLIENT:
            return self.fashion
        else:
            from ext_package.ext_decorator import get_mecha_default_fashion
            mecha_item_id = self.item_no
            return get_mecha_default_fashion(mecha_item_id, self.fashion)

    def get_sfx(self):
        return self.sfx

    def get_action(self):
        return self.action