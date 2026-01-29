# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/AimScopeAdjust/AimScopeM82AdjustUI.py
from __future__ import absolute_import
from logic.comsys.battle.AimScopeAdjust.CommonAimScopeAdjustUI import CommonAimScopeAdjustUI

class AimScopeM82AdjustUI(CommonAimScopeAdjustUI):
    PANEL_CONFIG_NAME = 'battle/fight_hit_sniper_adjust'
    PROG_ADJUST_FLOOR = 72
    PROG_ADJUST_CEIL = 81
    TURN_ADJUST_FLOOR = -18
    TURN_ADJUST_CEIL = 22

    def _populate_nodes(self, *args, **kwargs):
        self.nd_adjust = self.panel.nd_adjust
        self.btn_adjust = self.panel.btn_adjust
        self.prog_adjust = self.panel.prog_adjust
        self.nd_btn_turn = self.panel.nd_btn_turn