# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/SurviveWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils import battle_utils

class SurviveWidget(object):

    def __init__(self, kill_num_change_callback=None, kill_mecha_num_change_cb=None, assist_mecha_num_change_cb=None, assist_human_num_change_cb=None, team_kill_num_changed=None, team_kill_mecha_num_changed=None):
        self.cur_survive_num = 0
        self.my_kill_num = 0
        self.team_kill_num = 0
        self.kill_mecha_num = 0
        self.team_kill_mecha_num = 0
        self.assist_mecha_num = 0
        self.assist_human_num = 0
        self._kill_mecha_num_change_callback = kill_mecha_num_change_cb
        self.kill_num_change_cb = kill_num_change_callback
        self._assist_mecha_num_change_cb = assist_mecha_num_change_cb
        self._assist_human_num_change_cb = assist_human_num_change_cb
        self._team_kill_num_changed = team_kill_num_changed
        self._team_kill_mecha_num_changed = team_kill_mecha_num_changed
        self.process_event(True)
        self.on_camera_player_setted()

    def destroy(self):
        self.process_event(False)
        self.kill_num_change_cb = None
        self._kill_mecha_num_change_callback = None
        return

    def process_event(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'show_battle_report_event': self.show_battle_report,
           'scene_camera_player_setted_event': self.on_camera_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def check_relate_kill(self, report_dict):
        my_kill_num, team_kill_num = battle_utils.parse_battle_report_player_kill(global_data.cam_lplayer, report_dict)
        my_mecha_kill_num, team_mecha_kill_num, assist_mecha_num, assist_human_num = battle_utils.parse_battle_report_mecha_player_kill(global_data.cam_lplayer, report_dict)
        self.update_my_kill_num(self.my_kill_num + my_kill_num)
        self.update_team_kill_num(self.team_kill_num + team_kill_num)
        self.update_team_kill_mecha_num(self.team_kill_mecha_num + team_mecha_kill_num)
        self.update_kill_mecha_num(self.kill_mecha_num + my_mecha_kill_num)
        self.update_assist_mecha_num(self.assist_mecha_num + assist_mecha_num)
        self.update_assist_human_num(self.assist_human_num + assist_human_num)

    def show_battle_report(self, report_dict):
        self.check_relate_kill(report_dict)

    def update_my_kill_num(self, my_kill_num):
        self.my_kill_num = my_kill_num
        if self.kill_num_change_cb:
            self.kill_num_change_cb(my_kill_num)

    def update_team_kill_num(self, team_kill_num):
        self.team_kill_num = team_kill_num
        if callable(self._team_kill_num_changed):
            self._team_kill_num_changed(team_kill_num)

    def update_team_kill_mecha_num(self, num):
        self.team_kill_mecha_num = num
        if callable(self._team_kill_mecha_num_changed):
            self._team_kill_mecha_num_changed(num)

    def update_assist_mecha_num(self, assist_mecha_num):
        self.assist_mecha_num = assist_mecha_num
        if self._assist_mecha_num_change_cb:
            self._assist_mecha_num_change_cb(assist_mecha_num)

    def update_assist_human_num(self, assist_human_num):
        self.assist_human_num = assist_human_num
        if self._assist_human_num_change_cb:
            self._assist_human_num_change_cb(assist_human_num)

    def update_all_kill_num(self, player_id, teammate_ids):
        battle = global_data.player.get_joining_battle() or global_data.player.get_battle()
        battle_stat = {} if battle is None else battle.statistics
        player_statistics = battle_stat.get(player_id, {})
        self.update_my_kill_num(player_statistics.get('kill', 0))
        self.update_kill_mecha_num(player_statistics.get('kill_mecha', 0))
        self.update_assist_mecha_num(player_statistics.get('assist_mecha', 0))
        self.update_assist_human_num(player_statistics.get('assist_human', 0))
        tmp_team_kill_num = 0
        tmp_team_kill_mecha_num = 0
        for t_id in teammate_ids:
            tmp_team_kill_num += battle_stat.get(t_id, {}).get('kill', 0)
            tmp_team_kill_mecha_num += battle_stat.get(t_id, {}).get('kill_mecha', 0)

        self.update_team_kill_num(tmp_team_kill_num)
        self.update_team_kill_mecha_num(tmp_team_kill_mecha_num)
        return

    def on_camera_player_setted(self):
        if global_data.cam_lplayer:
            self.update_all_kill_num(global_data.cam_lplayer.id, global_data.cam_lplayer.ev_g_groupmate())

    def update_kill_mecha_num(self, kill_mecha_num):
        self.kill_mecha_num = kill_mecha_num
        if self._kill_mecha_num_change_callback:
            self._kill_mecha_num_change_callback(kill_mecha_num)