# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainTopProgUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import battle_const
from common.cfg import confmgr
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import math
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
TRAIN_TRK_FIRST = 1
TRAIN_TRK_SECOND = 2
TRAIN_TRK_THIRD = 3
TRAIN_TRK_FORTH = 4
ARRIVE_STATION_2 = 'arrive_station_2'
ARRIVE_STATION_3 = 'arrive_station_3'

class TrainTopProgUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_push_train/fight_push_train_top_score'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_score.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_panel()
        self.init_timer()
        self.init_event()

    def init_parameters(self):
        self.prog = 0
        self.is_atk = False
        self.is_warning = False
        self.force_speed_up = False
        self.left_10_seconds = False
        train_node_data = global_data.train_battle_mgr.get_all_station_node()
        self.train_node_dis = [ train_node_data[i + 1].get('track_dis') for i in range(len(train_node_data)) ]
        self.train_length = global_data.train_battle_mgr.get_rail_length()
        self.timer = None
        self.train_station_pass = -1
        self.last_round_dis = -1
        return

    def init_panel(self):
        self.update_group_state_ui()
        self.update_last_round_info()
        self.update_round_timestamp(0)
        self.panel.lab_time.SetColor('#SW')
        self.panel.temp_locate_1.bar_state.SetSelect(True)
        self.panel.temp_locate_1.bar_state.SetText(str(1))
        self.panel.temp_locate_2.bar_state.SetText(str(2))
        self.panel.temp_locate_3.bar_state.SetText(str(3))
        self.panel.temp_locate_2.RecordAnimationNodeState('tips')
        self.panel.temp_locate_3.RecordAnimationNodeState('tips')
        if global_data.battle.is_battle_prepare_stage():
            self.panel.nd_prog.setVisible(False)
        else:
            self.panel.nd_prog.setVisible(True)

    def init_event(self):
        self.process_event(True)

    def init_timer(self):
        self.timer = global_data.game_mgr.get_logic_timer().register(func=self.update_train_prog, interval=0.2, mode=CLOCK)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'crystal_round_settle_timestamp_event': self.update_round_timestamp,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'update_train_around_state': self.update_partner_and_emeny,
           'show_last_round_info_event': self.update_last_round_info,
           'train_use_skill_succeed': self.train_use_skill_succeed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def train_use_skill_succeed(self, soul, skill_id, player_name):
        self.force_speed_up = True
        if int(skill_id) == 4:
            self.panel.temp_red.SetInitCount(1)
            self.panel.temp_blue.SetInitCount(0)
        if int(skill_id) == 1:
            self.panel.temp_blue.SetInitCount(3)

    def train_use_skill_end(self, soul, skill_id):
        self.force_speed_up = False
        if int(skill_id) == 4:
            self.panel.temp_red.SetInitCount(0)

    def _on_scene_observed_player_setted(self, ltarget):
        self.update_group_state_ui()

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('TrainScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('TrainScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('TrainScoreDetailsUI', 'logic.comsys.battle.Train')

    def update_round_timestamp(self, timestamp):
        if not global_data.battle:
            return
        if not global_data.battle.is_battle_prepare_stage():
            target_round_time = global_data.battle.get_round_time()
            round_time = target_round_time - tutil.time()
        else:
            target_round_time = BattleUtils.get_prepare_left_time()
            round_time = target_round_time

        def refresh_time(pass_time):
            round_left_time = round_time - pass_time
            if round_left_time <= 30 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif round_left_time > 30 and self.is_warning:
                self.panel.StopAnimation('alarm')
                self.panel.RecoverAnimationNodeState('alarm')
                self.is_warning = False
                self.panel.lab_time.SetColor('#SW')
            if round_left_time <= 10 and not self.left_10_seconds:
                if not global_data.battle:
                    return
                if not global_data.battle.is_battle_prepare_stage():
                    ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
                    ui.on_delay_close(round_left_time)
                    self.left_10_seconds = True
                self.panel.lab_time.SetColor('#SR')
            left_time = int(math.ceil(round_left_time))
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_end():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, round_time, callback=refresh_time_end, interval=1)

    def stop_timer(self):
        if self.timer:
            global_data.game_mgr.get_logic_timer().unregister(self.timer)
        self.panel.lab_time.StopTimerAction()

    def update_group_state_ui(self):
        if not global_data.battle:
            return
        self.is_atk = global_data.battle.get_atk_group_id() == global_data.battle.get_my_group_id()
        if self.is_atk:
            self.panel.line.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/img_battle_push_score_line_blue.png')
            self.panel.bar_time.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_time_blue.png')
            self.panel.temp_red.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_red.png')
            self.panel.temp_blue.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_blue.png')
            self.panel.lab_camp.SetColor('#SW')
            if not global_data.battle.is_battle_prepare_stage():
                self.panel.lab_camp.SetString(17475)
            else:
                self.panel.lab_camp.SetString(634793)
        else:
            self.panel.line.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/img_battle_push_score_line_red.png')
            self.panel.bar_time.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_time_red.png')
            self.panel.temp_red.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_blue.png')
            self.panel.temp_blue.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_red.png')
            self.panel.lab_camp.SetColor('#SW')
            if not global_data.battle.is_battle_prepare_stage():
                self.panel.lab_camp.SetString(17474)
            else:
                self.panel.lab_camp.SetString(634792)

    def update_partner_and_emeny(self, num_atk, num_def):
        if num_atk == 0 and num_def == 0:
            self.panel.nd_fight.setVisible(False)
            self.panel.temp_blue.setVisible(False)
            self.panel.temp_red.setVisible(False)
            if self.is_atk:
                self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_battle_push_score_blue.png')
                self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
                self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
            else:
                self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_battle_push_score_red.png')
                self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
                self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
            return
        if num_atk != 0:
            self.panel.temp_blue.setVisible(True)
            self.panel.temp_blue.lab_num.SetString(str(num_atk))
        else:
            self.panel.temp_blue.setVisible(False)
        if num_def != 0:
            self.panel.temp_red.setVisible(True)
            self.panel.temp_red.lab_num.SetString(str(num_def))
        else:
            self.panel.temp_red.setVisible(False)
        if num_def and num_atk:
            self.panel.nd_fight.setVisible(True)
        else:
            self.panel.nd_fight.setVisible(False)
        if not self.force_speed_up:
            add_count = int(num_atk - num_def if num_atk - num_def >= 0 else 0)
            self.panel.temp_blue.SetInitCount(add_count)
        if num_atk == num_def:
            self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_push_train_state_yellow.png')
            if self.is_atk:
                self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
                self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
            else:
                self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
                self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
        elif num_atk > num_def:
            if self.is_atk:
                self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_battle_push_score_blue.png')
                self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
                self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
            else:
                self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_battle_push_score_red.png')
                self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
                self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
        elif self.is_atk:
            self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_battle_push_score_red.png')
            self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
            self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_red.png')
        else:
            self.panel.icon_train.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/icon_battle_push_score_blue.png')
            self.panel.prog_1.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')
            self.panel.prog_2.LoadTexture('gui/ui_res_2/battle_push_train/prog_battle_push_score_blue.png')

    def update_train_prog(self):
        if not global_data.train_battle_mgr:
            return
        carriage = global_data.train_battle_mgr.get_train_carriage()
        if not carriage or not carriage.sd.ref_target_dis:
            return
        if not global_data.battle.is_battle_prepare_stage():
            self.panel.nd_prog.setVisible(True)
        train_dis = carriage.sd.ref_target_dis
        last_stat, forward_stat, stat_idx = self.get_between_node_dis(train_dis)
        total_dis = forward_stat + last_stat
        if total_dis < 0:
            prog = 0
        else:
            prog = last_stat / float(total_dis)
        prog *= 100
        if prog < 0:
            prog = 0
        if prog > 100:
            prog = 100
        if stat_idx != self.train_station_pass:
            self.train_station_pass = stat_idx
            global_data.train_battle_mgr.update_route_sfx_state(stat_idx)
        if stat_idx == 1:
            pic_offset = 0
            if forward_stat < 100:
                self.panel.temp_locate_2.nd_tips.setVisible(True)
                self.panel.temp_locate_2.lab_distance.SetString('<{}m'.format(int(forward_stat)))
                time_stamp = global_data.achi_mgr.get_cur_user_archive_data(ARRIVE_STATION_2, -1)
                if time_stamp == -1 or tutil.time() - time_stamp > 30.0:
                    global_data.achi_mgr.set_cur_user_archive_data(ARRIVE_STATION_2, tutil.time())
                    message_data = {'i_type': battle_const.TRAIN_ARRIVE_STATION,'content_txt': 17848,'show_num': 1,'ext_message_func': lambda node: self.set_lab_2(node, get_text_by_id(17847).format(2))}
                    global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)
            else:
                self.panel.temp_locate_2.nd_tips.setVisible(False)
            self.panel.temp_locate_3.nd_tips.setVisible(False)
            self.panel.temp_locate_2.PlayAnimation('tips')
            self.panel.temp_locate_3.StopAnimation('tips')
            self.panel.temp_locate_3.RecoverAnimationNodeState('tips')
            self.panel.prog_2.SetPercentage(0)
            self.panel.prog_1.SetPercentage(prog)
            if global_data.battle and not global_data.battle.get_is_show_next_station_tips(0):
                message_data = {'i_type': battle_const.TRAIN_ARRIVE_STATION,'content_txt': 17861,'show_num': 1,'ext_message_func': lambda node: self.set_lab_2(node, get_text_by_id(17599))
                   }
                global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)
        elif stat_idx == 2:
            pic_offset = 50
            if forward_stat < 100:
                self.panel.temp_locate_3.nd_tips.setVisible(True)
                self.panel.temp_locate_3.lab_distance.SetString('<{}m'.format(int(forward_stat)))
                time_stamp = global_data.achi_mgr.get_cur_user_archive_data(ARRIVE_STATION_3, -1)
                if time_stamp == -1 or tutil.time() - time_stamp > 30.0:
                    global_data.achi_mgr.set_cur_user_archive_data(ARRIVE_STATION_3, tutil.time())
                    message_data = {'i_type': battle_const.TRAIN_ARRIVE_STATION,'content_txt': 17849,'show_num': 1,'ext_message_func': lambda node: self.set_lab_2(node, get_text_by_id(17847).format(3))}
                    global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)
            else:
                self.panel.temp_locate_3.nd_tips.setVisible(False)
            self.panel.temp_locate_2.nd_tips.setVisible(False)
            self.panel.temp_locate_2.bar_state.SetSelect(True)
            self.panel.temp_locate_3.PlayAnimation('tips')
            self.panel.temp_locate_2.StopAnimation('tips')
            self.panel.temp_locate_2.RecoverAnimationNodeState('tips')
            self.panel.prog_1.SetPercentage(100)
            self.panel.prog_2.SetPercentage(prog)
            if global_data.battle and not global_data.battle.get_is_show_next_station_tips(1):
                message_data = {'i_type': battle_const.TRAIN_ARRIVE_STATION,'content_txt': 17862,'show_num': 1,'ext_message_func': lambda node: self.set_lab_2(node, get_text_by_id(17851))
                   }
                global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)
        elif stat_idx > 2:
            pic_offset = 50
            prog = 100
            self.panel.prog_1.SetPercentage(100)
            self.panel.prog_2.SetPercentage(100)
        else:
            pic_offset = 0
            prog = 0
            self.panel.prog_1.SetPercentage(0)
            self.panel.prog_2.SetPercentage(0)
        self.prog = pic_offset + prog / 2.0
        self.update_last_round_info()
        self.panel.icon_train.SetPosition('{}%'.format(pic_offset + prog / 2.0), '50%18')

    def update_last_round_info(self):
        if not global_data.battle:
            self.panel.nd_tips.setVisible(False)
            return
        self.update_group_state_ui()
        last_round_left_time = global_data.battle.get_last_round_left_time()
        last_round_dis = global_data.battle.get_last_round_dis()
        max_length = global_data.train_battle_mgr.get_mode_max_length()
        if last_round_dis == -1 and last_round_left_time == -1:
            self.panel.nd_tips.setVisible(False)
            self.panel.icon_last_pos.setVisible(False)
            return
        if self.last_round_dis > last_round_dis:
            return
        self.last_round_dis = last_round_dis
        station_lengths = global_data.train_battle_mgr.get_station_lengths()
        if self.last_round_dis <= station_lengths[0]:
            prog = float(self.last_round_dis) / float(station_lengths[0]) * 50.0
        else:
            prog = 50.0 + float(self.last_round_dis - station_lengths[0]) / float(station_lengths[1]) * 50.0
        self.panel.icon_last_pos.setVisible(True)
        self.panel.icon_last_pos.SetPosition('{}%'.format(prog), '50%-24')
        if last_round_left_time != 0:
            left_time = tutil.get_delta_time_str(last_round_left_time)[3:]
            self.panel.lab_title.SetString(17476)
            self.panel.lab_remaining_time.SetString(left_time)
            return
        self.panel.lab_title.SetString(17829)
        self.panel.lab_remaining_time.SetString('{}%'.format(int(last_round_dis / max_length * 100.0)))

    def get_between_node_dis(self, train_dis):
        last_stat_idx = -1
        for idx in range(len(self.train_node_dis) - 1):
            if train_dis >= self.train_node_dis[idx] and train_dis < self.train_node_dis[idx + 1]:
                return (train_dis - self.train_node_dis[idx], self.train_node_dis[idx + 1] - train_dis, idx + 1)
            if self.train_node_dis[idx] > self.train_node_dis[idx + 1] and (self.train_node_dis[idx + 1] >= train_dis or self.train_node_dis[idx] <= train_dis):
                last_stat_idx = idx

        if last_stat_idx == -1:
            return (1.0, 1.0, 3)
        last_stat = train_dis - self.train_node_dis[last_stat_idx]
        forward_stat = self.train_node_dis[last_stat_idx + 1] - train_dis
        last_stat = last_stat + self.train_length if last_stat < 0 else last_stat
        forward_stat = forward_stat + self.train_length if forward_stat < 0 else forward_stat
        return (
         last_stat, forward_stat, last_stat_idx + 1)

    def set_lab_2(self, node, text_id):
        if not node or not node.lab_2:
            return
        node.lab_2.SetString(text_id)

    def on_finalize_panel(self):
        self.stop_timer()
        self.process_event(False)