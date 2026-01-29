# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag2/Flag2ThrowUI.py
from __future__ import absolute_import
from logic.comsys.battle.Flag.FlagThrowUI import FlagThrowUI

class Flag2ThrowUI(FlagThrowUI):

    def _on_click_drop_btn(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            player_g_id = global_data.player.logic.ev_g_group_id()
            flag_id = global_data.death_battle_data.flag_ent_id_dict.get(player_g_id, None)
            if not global_data.battle:
                return
            flag = global_data.battle.get_entity(flag_id)
            if flag:
                flag.logic.send_event('E_TRY_DROP_FLAG')
            return

    def _on_flag_recover(self, holder_id, holder_faction, reason):
        player_g_id = global_data.player.logic.ev_g_group_id()
        if player_g_id == holder_faction:
            self.panel.nd_squat.setVisible(False)