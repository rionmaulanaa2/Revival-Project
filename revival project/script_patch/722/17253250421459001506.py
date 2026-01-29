# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/VehicleSkin.py
from .Item import Item

class VehicleSkin(Item):
    __slots__ = ('glide_effect', )

    def __init__(self, item_id=None, create_time=None):
        super(VehicleSkin, self).__init__(item_id, create_time)
        self.glide_effect = None
        return

    def get_persistent_dict(self):
        pd = super(VehicleSkin, self).get_persistent_dict()
        pd.update({'glide_effect': self.glide_effect})
        return pd

    def get_client_dict(self):
        cd = super(VehicleSkin, self).get_client_dict()
        cd.update({'glide_effect': self.glide_effect})
        return cd

    def get_glide_effect(self):
        return self.glide_effect