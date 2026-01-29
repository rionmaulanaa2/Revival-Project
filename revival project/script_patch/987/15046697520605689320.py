# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/StateChangeUIPC.py
from __future__ import absolute_import
from .StateChangeUI import StateChangeBaseUI

class StateChangeUIPC(StateChangeBaseUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_change_pc'

    def set_human_btn_selected(self, flag):
        path = 'gui/ui_res_2_pc/battle/mech_main/pnl_mech_driverbg_pc.png'
        self.panel.img_bg.SetDisplayFrameByPath('', path)

    def on_hot_key_opened_state(self):
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                return
        super(StateChangeUIPC, self).on_hot_key_opened_state()

    def on_player_setted(self, player):
        super(StateChangeUIPC, self).on_player_setted(player)
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                self.on_switch_off_hot_key()