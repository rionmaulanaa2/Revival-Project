# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewBiePassLevelUp.py
from __future__ import absolute_import
from logic.comsys.battle_pass.BpLevelUpBaseUI import BpLevelUpBaseUI

class NewBiePassLevelUp(BpLevelUpBaseUI):
    PANEL_CONFIG_NAME = 'battle_pass/new_pass_level_up'

    def on_click_receive_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.close()
        ui = global_data.ui_mgr.get_ui('NewbiePassUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('NewbiePassUI', 'logic.comsys.battle_pass')
        ui.show()