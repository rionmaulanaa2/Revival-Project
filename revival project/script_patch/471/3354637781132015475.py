# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ADCrystal/ADCrystalBattleData.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData

class ADCrystalBattleData(DeathBattleData):

    def init_parameters(self):
        super(ADCrystalBattleData, self).init_parameters()
        self.group_crystal_damage_dict = {}

    def update_group_crystal_damage(self, group_crystal_damage):
        for group_id in six.iterkeys(group_crystal_damage):
            self.group_crystal_damage_dict[group_id] = group_crystal_damage[group_id]

        global_data.emgr.update_group_crystal_damage.emit(self.group_crystal_damage_dict)