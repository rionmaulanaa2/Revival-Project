# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComCrystalStone.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComCrystalStone(UnitCom):
    BIND_EVENT = {'E_ON_CRYSTAL_STONE_UPDATE': '_on_update_crystal_stone',
       'G_CRYSTAL_STONE': '_get_crystal_stone',
       'E_ON_COST_CRYSTAL_STONE': '_on_cost',
       'E_CRYSTAL_STONE_DEBT_LIMIT': '_on_update_debt_limit',
       'G_CRYSTAL_STONE_DEBT_LIMIT': '_get_crystal_stone_debt_limit'
       }

    def __init__(self):
        super(ComCrystalStone, self).__init__()
        self._bag_num = 0
        self._debt_limit = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComCrystalStone, self).init_from_dict(unit_obj, bdict)
        self._bag_num = bdict.get('crystal_bag_num', 0)
        self._debt_limit = bdict.get('debt_limit', 0)

    def _on_update_crystal_stone(self, bag_num, add):
        self._bag_num = bag_num
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            global_data.emgr.pve_update_crystal_num.emit(bag_num, add)

    def _on_cost(self, bag_num):
        self._bag_num = bag_num
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            global_data.emgr.pve_cost_crystal_stone.emit()

    def _get_crystal_stone(self):
        return self._bag_num

    def _get_crystal_stone_debt_limit(self):
        return self._debt_limit

    def _on_update_debt_limit(self, debt_limit):
        self._debt_limit = debt_limit