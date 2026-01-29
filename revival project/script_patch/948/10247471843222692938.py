# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartGroup.py
from __future__ import absolute_import
from . import ScenePart
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const

class PartGroup(ScenePart.ScenePart):
    ENTER_EVENT = {'add_teammate_name_event': 'on_add_player',
       'scene_observed_player_setted_event': 'on_enter_observe',
       'scene_player_setted_event': 'on_player_setted'
       }

    def __init__(self, scene, name):
        super(PartGroup, self).__init__(scene, name)
        self.group_info = {}

    def on_enter(self):
        scn = self.scene()
        player = scn.get_player()
        self.cur_observe_target = None
        if player:
            self.on_player_setted(player)
        return

    def on_player_setted(self, player):
        from logic.comsys.battle.TeammateUI import TeammateUI
        TeammateUI()
        self.check_show_team_blood_ui()
        if player is None:
            return
        else:
            teammate_ids = player.ev_g_groupmate()
            if teammate_ids:
                teammate_ids.sort()
                for t_id in teammate_ids:
                    if t_id not in self.group_info:
                        self.group_info[t_id] = ('', 1)

            self.group_info[player.id] = (
             player.get_owner().get_name(), player.get_owner().lv)
            return

    def on_add_player(self, player, name):
        if player:
            if player.id in self.group_info:
                self.group_info[player.id] = (
                 name, player.get_owner().lv)
                if player.id != global_data.player.id:
                    if self.cur_observe_target and self.cur_observe_target.id == player.id:
                        return

    def on_exit(self):
        self.group_info = None
        global_data.ui_mgr.close_ui('TeammateUI')
        global_data.ui_mgr.close_ui('TeamBloodUI')
        global_data.ui_mgr.close_ui('PVETeamBloodUI')
        global_data.ui_mgr.close_ui('JudgeTeamBloodUI')
        self.cur_observe_target = None
        return

    def on_enter_observe(self, ltarget):
        cur_tar = self.cur_observe_target
        from logic.comsys.battle.TeammateUI import TeammateUI
        TeammateUI()
        self.cur_observe_target = ltarget
        if ltarget:
            self.check_show_team_blood_ui()

    @execute_by_mode(False, (game_mode_const.GAME_MODE_EXERCISE,))
    def check_show_team_blood_ui(self):
        if not global_data.player:
            return
        bat = global_data.player.get_battle()
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            global_data.ui_mgr.show_ui('JudgeTeamBloodUI', 'logic.comsys.observe_ui')
            return
        if bat and not bat.is_single_person_battle():
            if global_data.game_mode.is_pve():
                global_data.ui_mgr.show_ui('PVETeamBloodUI', 'logic.comsys.battle.pve')
            else:
                global_data.ui_mgr.show_ui('TeamBloodUI', 'logic.comsys.battle')