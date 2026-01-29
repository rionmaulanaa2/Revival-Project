# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleFightCapacityPC.py
from __future__ import absolute_import
from .BattleFightCapacity import BattleFightCapacityBase
from logic.gcommon.cdata import driver_lv_data
from logic.gcommon.common_const import battle_const

class BattleFightCapacityPC(BattleFightCapacityBase):
    PANEL_CONFIG_NAME = 'battle/fight_point_pc'

    def leave_screen(self):
        super(BattleFightCapacityPC, self).leave_screen()
        global_data.ui_mgr.close_ui('BattleFightCapacityPC')