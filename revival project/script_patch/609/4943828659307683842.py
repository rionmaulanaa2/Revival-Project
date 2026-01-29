# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETeamBloodUI.py
from __future__ import absolute_import
from logic.comsys.battle.TeamBloodUI import TeamBloodBaseUI

class PVETeamBloodUI(TeamBloodBaseUI):
    PANEL_CONFIG_NAME = 'pve/i_pve_teammate'

    def on_click_ui(self):
        super(PVETeamBloodUI, self).on_click_ui()
        ui = global_data.ui_mgr.get_ui('PVEInfoUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('PVEInfoUI', 'logic.comsys.control_ui')
        ui.appear()

    def del_player(self, player_id):
        super(PVETeamBloodUI, self).del_player(player_id)
        teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
        if teammate_infos:
            char_name = teammate_infos.get(player_id, {}).get('char_name', None)
            if char_name:
                global_data.emgr.pve_teammate_quit_event.emit(char_name)
        return