# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/Fashion.py
from __future__ import absolute_import
from .Item import Item

class Fashion(Item):
    __slots__ = ('wsfx', )

    def __init__(self, item_id=None, create_time=None):
        super(Fashion, self).__init__(item_id, create_time)
        self.wsfx = None
        return

    def get_persistent_dict(self):
        d = super(Fashion, self).get_persistent_dict()
        if self.wsfx:
            d.update({'wsfx': self.wsfx
               })
        return d

    def get_client_dict(self):
        d = super(Fashion, self).get_client_dict()
        if self.wsfx:
            d.update({'wsfx': self.wsfx
               })
        return d

    def set_weapon_sfx(self, weapon_sfx):
        self.wsfx = weapon_sfx

    def get_weapon_sfx(self):
        return self.wsfx

    def update_degree(self):
        from data import role_data
        from data.lobby_item_data import get_rare_degree
        skin_config = role_data.GetRoleSkin().get(self.item_no, None)
        if skin_config:
            sfx_item_no = skin_config.get('improved_skin_sfx_item')
            if sfx_item_no and self.wsfx == sfx_item_no:
                self.rare_degree = skin_config.get('improved_skin_rare_degree') or get_rare_degree(self.item_no)
                return
        self.rare_degree = get_rare_degree(self.item_no)
        return