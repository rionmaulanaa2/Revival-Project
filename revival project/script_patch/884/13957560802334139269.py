# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ADCrystal/ADCrystalTopScoreUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
import math
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import ROUND_STATUS_INTERVAL
INIT_LEFT_DIE_CNT = 50

class ADCrystalTopScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_crystal/crystal2_top_score'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_score.OnClick': 'toggle_score_details'
       }
    GLOBAL_EVENT = {'scene_observed_player_setted_event': 'on_scene_observed_player_setted',
       'crystal_round_settle_timestamp_event': 'update_round_settle_timestamp',
       'do_update_crystal_hp': 'update_crystal_hp',
       'update_group_left_die_count_event': 'update_left_die_cnt',
       'show_last_round_info_event': 'show_last_round_info'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.update_group_id(None)
        self.init_widgets()
        return

    def init_parameters(self):
        self.is_warning = False
        self.left_10_seconds = False
        self.group_id = None
        return

    def on_finalize_panel(self):
        self.stop_count_down()

    def init_widgets(self):
        self.panel.RecordAnimationNodeState('alarm')
        self.start_count_down()
        self.init_top_score()
        self.show_last_round_info()

    def start_count_down(self):
        if not global_data.battle:
            return
        round_left_time = global_data.battle.get_round_left_time()
        if round_left_time <= 0:
            return
        if global_data.battle.get_round_status() == ROUND_STATUS_INTERVAL:
            return

        def refresh_time(pass_time):
            if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
                return
            cur_left_time = round_left_time - pass_time
            if cur_left_time <= 30 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif cur_left_time > 30 and self.is_warning:
                self.panel.StopAnimation('alarm')
                self.panel.RecoverAnimationNodeState('alarm')
                self.is_warning = False
            if cur_left_time <= 10 and not self.left_10_seconds:
                ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(cur_left_time)
                self.left_10_seconds = True
            left_time = int(math.ceil(cur_left_time))
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_finish():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, round_left_time, callback=refresh_time_finish, interval=1)

    def stop_count_down(self):
        self.panel.lab_time.StopTimerAction()

    def init_top_score(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            if self.group_id is None:
                return
            crystal_hp_percent = battle.get_def_crystal_hp_percent()
            crystal_hp_percent_display = int(min(math.ceil(100.0 * crystal_hp_percent), 100))
            crystal_hp_percent_str = '{}%'.format(str(crystal_hp_percent_display))
            left_die_cnt = max(0, battle.get_atk_left_die_count())
            left_die_cnt_percent = max(0.0, min(1.0, 1.0 * left_die_cnt / INIT_LEFT_DIE_CNT))
            left_die_cnt_percent_dispaly = int(left_die_cnt_percent * 100)
            if self.group_id == battle.get_atk_group_id():
                blue_icon_path = 'gui/ui_res_2/battle_crystal/icon_battle_crystal_team_blue.png'
                blue_name = get_text_by_id(17473)
                blue_value = left_die_cnt
                blue_prog = left_die_cnt_percent_dispaly
                red_icon_path = 'gui/ui_res_2/battle_crystal/icon_battle_crystal_tips_red.png'
                red_name = get_text_by_id(17472)
                red_value = crystal_hp_percent_str
                red_prog = crystal_hp_percent_display
                self.panel.lab_title.SetString(get_text_by_id(17475))
                self.panel.lab_title.SetColor(16749229)
            else:
                blue_icon_path = 'gui/ui_res_2/battle_crystal/icon_battle_crystal_tips_blue.png'
                blue_name = get_text_by_id(17472)
                blue_value = crystal_hp_percent_str
                blue_prog = crystal_hp_percent_display
                red_icon_path = 'gui/ui_res_2/battle_crystal/icon_battle_crystal_team_red.png'
                red_name = get_text_by_id(17473)
                red_value = left_die_cnt
                red_prog = left_die_cnt_percent_dispaly
                self.panel.lab_title.SetString(get_text_by_id(17474))
                self.panel.lab_title.SetColor(1763317)
            self.panel.icon_blue.SetDisplayFrameByPath('', blue_icon_path)
            self.panel.lab_blue.SetString(blue_name)
            self.panel.lab_prog_blue.SetString(str(blue_value))
            self.panel.prog_blue.SetPercentage(blue_prog)
            self.panel.icon_red.SetDisplayFrameByPath('', red_icon_path)
            self.panel.lab_red.SetString(red_name)
            self.panel.lab_prog_red.SetString(str(red_value))
            self.panel.prog_red.SetPercentage(red_prog)
            return

    def update_round_settle_timestamp(self, settle_timestamp):
        self.start_count_down()

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('CrystalScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('CrystalScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('CrystalScoreDetailsUI', 'logic.comsys.battle.Crystal')

    def update_crystal_hp(self, group_id, hp_percent):
        battle = global_data.battle
        if not battle:
            return
        if group_id != battle.get_def_group_id():
            return
        hp_percent = int(min(math.ceil(100.0 * hp_percent), 100))
        hp_percent_str = '{}%'.format(str(hp_percent))
        if group_id == self.group_id:
            self.panel.lab_prog_blue.SetString(hp_percent_str)
            self.panel.prog_blue.SetPercentage(hp_percent)
        else:
            self.panel.lab_prog_red.SetString(hp_percent_str)
            self.panel.prog_red.SetPercentage(hp_percent)

    def update_left_die_cnt(self, group_id, left_die_cnt):
        battle = global_data.battle
        if not battle:
            return
        if group_id != battle.get_atk_group_id():
            return
        left_die_cnt = max(0, left_die_cnt)
        left_percent = max(0.0, min(100.0, 1.0 * left_die_cnt / INIT_LEFT_DIE_CNT * 100))
        if group_id == self.group_id:
            self.panel.lab_prog_blue.SetString(str(left_die_cnt))
            self.panel.prog_blue.SetPercentage(left_percent)
        else:
            self.panel.lab_prog_red.SetString(str(left_die_cnt))
            self.panel.prog_red.SetPercentage(left_percent)

    def on_scene_observed_player_setted(self, ltarget):
        self.update_group_id(ltarget)
        self.init_top_score()

    def update_group_id(self, ltarget):
        if global_data.player and global_data.player.logic:
            self.group_id = global_data.player.logic.ev_g_group_id()
        elif ltarget:
            self.group_id = ltarget.ev_g_group_id()

    def show_last_round_info(self):
        self.panel.nd_info.setVisible(False)
        battle = global_data.battle
        if not battle:
            return
        if battle.get_crystal_round() <= 0:
            self.panel.nd_info.setVisible(False)
            return
        group_id = battle.get_old_atk_group_id()
        crystal_point = battle.get_group_crystal_points(group_id)
        if crystal_point > 0:
            self.panel.nd_info.lab_info.SetString(get_text_by_id(17476))
            left_time = battle.get_group_left_time(group_id)
            left_time_str = tutil.get_delta_time_str(int(left_time))[3:]
            self.panel.nd_info.lab_value.SetString(left_time_str)
        else:
            self.panel.nd_info.lab_info.SetString(get_text_by_id(17477))
            old_def_group_id = battle.get_old_def_group_id()
            hp_percent = battle.get_group_crystal_hp_percent(old_def_group_id)
            hp_percent = int(min(math.ceil(100.0 * hp_percent), 100))
            hp_percent_str = '{}%'.format(str(hp_percent))
            self.panel.nd_info.lab_value.SetString(hp_percent_str)
        self.panel.nd_info.setVisible(True)