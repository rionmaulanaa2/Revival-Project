# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveCoin.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComPveCoin(UnitCom):
    BIND_EVENT = {'E_ON_UPDATE_PVE_COIN': 'on_update_pve_coin',
       'G_PVE_COIN_NUM': 'get_pve_coin_num'
       }

    def __init__(self):
        super(ComPveCoin, self).__init__()
        self.coin_num = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveCoin, self).init_from_dict(unit_obj, bdict)
        self.coin_num = bdict.get('pve_coin_num', 0)

    def on_update_pve_coin(self, bag_num):
        self.coin_num = bag_num
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            global_data.emgr.pve_update_coin_num.emit(bag_num)

    def get_pve_coin_num(self):
        return self.coin_num