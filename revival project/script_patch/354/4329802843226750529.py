# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FightStateUIPC.py
from __future__ import absolute_import
from .FightStateUI import FightStateBaseUI

class FightStateUIPC(FightStateBaseUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_state_pc'

    def leave_screen(self):
        super(FightStateUIPC, self).leave_screen()
        global_data.ui_mgr.close_ui('FightStateUIPC')

    def switch_to_mecha(self):
        if not self._in_mecha_state:
            self.panel.StopAnimation('switch_to_people')
            self.panel.nd_module_group.stopAllActions()
            self.panel.PlayAnimation('switch_to_mech')
        super(FightStateUIPC, self).switch_to_mecha()

    def switch_to_non_mecha(self):
        if self._in_mecha_state:
            self.panel.StopAnimation('switch_to_mech')
            self.panel.nd_module_group.stopAllActions()
            self.panel.PlayAnimation('switch_to_people')
        super(FightStateUIPC, self).switch_to_non_mecha()

    def init_mecha_tips_com(self):
        self.mecha_tips_com_0 = None
        self.mecha_tips_com_1 = None
        return