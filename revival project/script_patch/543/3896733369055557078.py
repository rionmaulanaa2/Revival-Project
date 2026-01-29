# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaUIPC.py
from __future__ import absolute_import
from .MechaUI import MechaBaseUI

class MechaUIPC(MechaBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_mech_call_pc'
    HOT_KEY_FUNC_MAP_SHOW = {'summon_call_mecha': {'node': 'temp_pc'}}

    def on_hot_key_opened_state(self):
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                return
        super(MechaUIPC, self).on_hot_key_opened_state()

    def on_player_setted(self):
        super(MechaUIPC, self).on_player_setted()
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                self.on_switch_off_hot_key()