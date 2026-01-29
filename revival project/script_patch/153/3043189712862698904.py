# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crystal/CrystalTopScoreUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import math
from logic.gutils.template_utils import init_crystal_icon_list

class CrystalTopScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_crystal/crystal_top_score'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_score.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        if self.end_time_count_down_player_id:
            global_data.sound_mgr.stop_playing_id(self.end_time_count_down_player_id)
        self.panel.lab_time.StopTimerAction()
        self.process_event(False)

    def init_parameters(self):
        self.is_warning = False
        self.left_10_seconds = False
        self.end_time_count_down_player_id = None
        self.update_name(None)
        return

    def init_event(self):
        self.process_event(True)

    def init_panel(self):
        self.panel.RecordAnimationNodeState('alarm')
        self.init_crystal_list_widget()
        if global_data.death_battle_data:
            self.update_timestamp()
        if global_data.battle:
            self.update_group_crystal_points(global_data.battle.get_group_crystal_points())
        global_data.emgr.ask_update_crystal_hp.emit()

    def init_crystal_list_widget(self):
        self.panel.list_icon_blue.SetNumPerUnit(1, False)
        self.panel.list_icon_blue.SetInitCount(3)
        self.panel.list_icon_red.SetNumPerUnit(1, False)
        self.panel.list_icon_red.SetInitCount(3)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_timestamp': self.update_timestamp,
           'do_update_crystal_hp': self.update_crystal_hp,
           'update_crystal_points_event': self.update_group_crystal_points,
           'scene_observed_player_setted_event': self.on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('CrystalScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('CrystalScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('CrystalScoreDetailsUI', 'logic.comsys.battle.Crystal')

    def update_name(self, ltarget):
        if global_data.player and global_data.player.logic:
            self.group_id = global_data.player.logic.ev_g_group_id()
        if ltarget:
            self.group_id = ltarget.ev_g_group_id()

    def on_scene_observed_player_setted(self, ltarget):
        self.update_name(ltarget)
        if global_data.death_battle_data:
            self.update_group_score(global_data.death_battle_data.get_group_score_data())

    def update_group_score(self, data):
        bat = global_data.player.get_battle()
        if not bat:
            return
        total_point = bat.get_settle_point()
        if not total_point:
            return
        for g_id in six.iterkeys(data):
            if g_id == self.group_id:
                self.panel.nd_score.lab_score_blue.SetString(str(data[g_id]))
            else:
                self.panel.nd_score.lab_score_red.SetString(str(data[g_id]))

    def update_crystal_hp(self, group_id, hp_percent):
        hp_percent = int(min(math.ceil(100.0 * hp_percent), 100))
        hp_percent_str = '{}%'.format(str(hp_percent))
        if group_id == self.group_id:
            self.panel.lab_prog_blue.SetString(hp_percent_str)
            self.panel.prog_blue.SetPercentage(hp_percent)
        else:
            self.panel.lab_prog_red.SetString(hp_percent_str)
            self.panel.prog_red.SetPercentage(hp_percent)

    def update_group_crystal_damage(self, group_crystal_damage):
        bat = global_data.player.get_battle()
        if not bat:
            return
        crystal_max_hp = bat.get_crystal_max_hp()
        if not crystal_max_hp:
            return
        for group_id in six.iterkeys(group_crystal_damage):
            crystal_damage = group_crystal_damage[group_id]
            left_percent = int(100.0 * (crystal_max_hp - crystal_damage) / crystal_max_hp)
            left_percent_str = '{}%'.format(str(left_percent))
            if group_id == self.group_id:
                self.panel.lab_prog_red.SetString(left_percent_str)
                self.panel.prog_red.SetPercentage(left_percent)
            else:
                self.panel.lab_prog_blue.SetString(left_percent_str)
                self.panel.prog_blue.SetPercentage(left_percent)

    def update_group_round(self, group_round):
        for group_id, round in six.iteritems(group_round):
            if group_id == self.group_id:
                self.update_crystal_list(round, self.panel.list_icon_blue)
            else:
                self.update_crystal_list(round, self.panel.list_icon_red)

    def update_group_crystal_points(self, group_crystal_points):
        self_group_crystal_point = group_crystal_points.get(self.group_id, 0)
        other_group_crystal_point = 0
        for group_id, crystal_point in six.iteritems(group_crystal_points):
            if group_id != self.group_id:
                other_group_crystal_point = crystal_point

        init_crystal_icon_list(3, other_group_crystal_point, self.panel.list_icon_blue)
        init_crystal_icon_list(3, self_group_crystal_point, self.panel.list_icon_red)

    def update_crystal_list(self, round, crystal_list):
        for idx, crystal_ui in enumerate(crystal_list.GetAllItem()):
            if idx >= round:
                crystal_ui.icon.setOpacity(255)
            else:
                crystal_ui.icon.setOpacity(int(127.5))

    def update_timestamp(self, *args):
        if global_data.player and global_data.player.in_local_battle():
            return
        self.on_count_down()

    def on_count_down(self):
        revive_time = BattleUtils.get_battle_left_time()

        def refresh_time(pass_time):
            if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
                return
            left_time = revive_time - pass_time
            if left_time <= 30 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif left_time > 30 and self.is_warning:
                self.panel.lab_time.SetColor('##BC')
                self.panel.StopAnimation('alarm')
                self.panel.RecoverAnimationNodeState('alarm')
                self.is_warning = False
            if left_time <= 10 and not self.left_10_seconds:
                ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(left_time)
                self.left_10_seconds = True
                from logic.client.const.game_mode_const import GAME_MODE_DEATH
                if global_data.game_mode.get_mode_type() == GAME_MODE_DEATH:
                    self.end_time_count_down_player_id = global_data.sound_mgr.play_sound('Play_time_countdown')
            left_time = int(math.ceil(left_time))
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.SetColor('#BC')
        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=1)

    def set_init_time(self):
        left_time = global_data.game_mode.get_cfg_data('play_data').get('battle_duration', 0)
        left_time = int(math.ceil(left_time))
        left_time = tutil.get_delta_time_str(left_time)[3:]
        self.panel.lab_time.SetString(left_time)
        self.panel.lab_time_vx.SetString(left_time)