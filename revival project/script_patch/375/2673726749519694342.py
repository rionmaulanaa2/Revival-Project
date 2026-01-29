# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Improvise/ImproviseBattleData.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from common.cfg import confmgr
from logic.gcommon.common_const.battle_const import ROUND_TYPE_PURE_HUMAN, ROUND_TYPE_MECHA

class ImproviseBattleData(Singleton):
    ALIAS_NAME = 'improvise_battle_data'

    def init(self):
        self.init_parameters()
        global_data.emgr.improvise_battle_data_initted.emit()

    def init_parameters(self):
        self.settle_timestamp = None
        self._group_points_dict = {}
        self._score_details_data = {}
        self.round_number = 0
        self.round_type = 0
        self.round_begin_ts = 0.0
        self.round_ready_ts = 0.0
        self.round_end_ts = 0.0
        self.round_end_finish_ts = 0.0
        self.round_weapon_data_index = 0
        self.round_mecha_id = 0
        self._group_hp_dict = {}
        self._cur_round_win_group_id = -1
        self.weapon_plan_data = global_data.game_mode.get_cfg_data('weapon_plan_data')
        self._notified_end_round = 0
        self._avatar_adjusted_yaw = False
        return

    def on_finalize(self):
        self.init_parameters()

    def set_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.emgr.update_battle_timestamp.emit(settle_timestamp)

    def set_avatar_adjust_yaw(self, sync_already):
        is_in_global_spectate = global_data.player and global_data.player.is_in_global_spectate()
        if is_in_global_spectate:
            return
        if not global_data.player:
            return
        self._avatar_adjusted_yaw = sync_already
        if not sync_already:
            if global_data.battle and hasattr(global_data.battle, 'notify_avatar_adjust_yaw_already'):
                self._adjust_avatar_yaw()
                global_data.battle.notify_avatar_adjust_yaw_already(global_data.player)
            else:
                log_error("battle doesn't have notify_avatar_adjust_yaw_already.")

    def _adjust_avatar_yaw(self):
        born_data = global_data.game_mode.get_born_data()
        base_center_pos = born_data.get(str(global_data.battle.area_id), {}).get('map_center')
        if base_center_pos:
            if global_data.player and global_data.player.logic:
                import math3d
                position = math3d.vector(*base_center_pos)
                self._rotate_avatar_to_look_at(global_data.player.logic, position)
            else:
                log_error('_adjust_avatar_yaw, no avatar logic.')
        else:
            log_error('_adjust_avatar_yaw, no map center to look at.')

    def _rotate_avatar_to_look_at(self, lplayer, target_pos):
        if not lplayer:
            return
        lpos = lplayer.ev_g_position()
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = lplayer.ev_g_yaw() or 0
                global_data.emgr.camera_set_yaw_event.emit(target_yaw)
                global_data.emgr.camera_set_pitch_event.emit(0)
                lplayer.send_event('E_CAM_PITCH', 0)
                lplayer.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def get_move_range(self):
        if self.round_type == ROUND_TYPE_MECHA:
            return global_data.game_mode.get_born_data(str(global_data.battle.area_id), 'move_range_mecha', default={})
        else:
            return global_data.game_mode.get_born_data(str(global_data.battle.area_id), 'move_range', default={})

    def update_group_points_data(self, data):
        self._group_points_dict = data
        global_data.emgr.update_battle_group_points_dict.emit(data)

    def update_group_hp_data(self, data):
        self._group_hp_dict = data
        global_data.emgr.update_improvise_battle_group_hp_dict.emit(data)

    def update_score_details_data(self, data):
        self._score_details_data = data
        global_data.emgr.update_score_details.emit(data)

    def get_cur_round_begin_ready_duration(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        return cfg.get('round_begin_count_down_time', 3)

    def update_cur_round_data(self, round_index, round_type, round_begin_ts, weapon_data_index):
        prev_round_index = self.round_number
        self.round_number = round_index
        self.round_begin_ts = round_begin_ts
        ready_duration = self.get_cur_round_begin_ready_duration()
        self.round_ready_ts = round_begin_ts + ready_duration
        self.round_type = round_type
        self.round_weapon_data_index = weapon_data_index
        duration = self.get_cur_round_duration()
        self.update_cur_round_end_ts(round_begin_ts + duration, notify=False)
        mecha_conf = self.weapon_plan_data.get(str(weapon_data_index), {}).get('mecha_conf', {})
        self.round_mecha_id = 0
        for mecha_id, modules in six.iteritems(mecha_conf):
            self.round_mecha_id = int(mecha_id)
            break

        from logic.gcommon.time_utility import get_server_time_battle
        cur_time = get_server_time_battle()
        ready_ts = self.round_ready_ts
        if cur_time < ready_ts:
            left_time = ready_ts - cur_time
            inst = global_data.ui_mgr.show_ui('ImproviseBeginCountDown', 'logic.comsys.battle.Improvise')
            inst.on_delay_close(left_time)
            global_data.emgr.improvise_highlight_reenterable.emit(left_time)
        if prev_round_index != round_index:
            global_data.ui_mgr.show_ui('ImproviseTopScoreUI', 'logic.comsys.battle.Improvise')
            from logic.client.const import game_mode_const
            global_data.emgr.battle_new_round.emit(prev_round_index, round_index, game_mode_const.GAME_MODE_IMPROVISE)
        if round_index > 0:
            global_data.emgr.update_battle_round_end_ts.emit(self.round_end_ts)
        global_data.emgr.battle_change_prepare_timestamp.emit()

    def update_cur_round_end_ts(self, end_ts, notify=True):
        self.round_end_ts = end_ts
        self.round_end_finish_ts = self.round_end_ts + self.get_cur_round_end_duration()
        if notify:
            global_data.emgr.update_battle_round_end_ts.emit(self.round_end_ts)

    def update_cur_round_settle_data(self, end_ts, win_group_id, group_points_dict):
        self.update_cur_round_end_ts(end_ts)
        self._cur_round_win_group_id = win_group_id
        self.update_group_points_data(group_points_dict)
        self._check_cur_round_end()

    def get_cur_round_duration(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        duration = cfg.get('human_round_last_time', 90) if self.round_type == ROUND_TYPE_PURE_HUMAN else cfg.get('mecha_round_last_time', 180)
        return duration

    def get_cur_round_end_duration(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        duration = cfg.get('round_settle_stay_time', 5)
        return duration

    def get_cur_round_ready_ts(self):
        return self.round_ready_ts

    def get_cur_round_ready_left_time(self):
        from logic.gcommon.time_utility import get_server_time_battle
        cur_time = get_server_time_battle()
        left_time = max(0.0, self.round_ready_ts - cur_time)
        return left_time

    def get_cur_round_end_ts(self):
        return self.round_end_ts

    def get_round_type(self):
        return self.round_type

    def get_cur_round_mecha_type_id(self):
        return self.round_mecha_id

    def get_group_points_dict(self):
        return self._group_points_dict

    def get_score_details_data(self):
        return self._score_details_data

    def get_group_hp_dict(self):
        return self._group_hp_dict

    def get_cur_round_no(self):
        return self.round_number

    def get_total_round_cnt(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        return cfg.get('total_round_count', 9)

    def get_max_win_round_cnt(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        return cfg.get('champion_need_win_round', 5)

    def is_operable(self):
        from logic.gcommon.time_utility import get_server_time_battle
        cur_time = get_server_time_battle()
        if self.round_ready_ts and cur_time < self.round_ready_ts or self.round_end_ts and cur_time > self.round_end_ts:
            return False
        return True

    def _in_cur_round_end_stage(self, cur_time):
        return cur_time >= self.round_end_ts and cur_time < self.round_end_finish_ts

    def _check_cur_round_end(self):
        if self._notified_end_round == self.round_number:
            return
        else:
            from logic.gcommon.time_utility import get_server_time_battle
            cur_time = get_server_time_battle()
            if self._in_cur_round_end_stage(cur_time):
                left_time = max(0.0, self.round_end_finish_ts - cur_time)
                if left_time > 0:
                    self_group_id = None
                    if global_data.player:
                        if global_data.player.is_in_global_spectate():
                            if global_data.cam_lplayer:
                                self_group_id = global_data.cam_lplayer.ev_g_group_id()
                        elif global_data.player.logic:
                            self_group_id = global_data.player.logic.ev_g_group_id()
                    from logic.comsys.battle.Improvise.ImproviseRoundSettleUI import SETTLE_WIN, SETTLE_DRAW, SETTLE_LOSE
                    if self._cur_round_win_group_id < 0:
                        settle_result = SETTLE_DRAW
                    elif self_group_id == self._cur_round_win_group_id:
                        settle_result = SETTLE_WIN
                    else:
                        settle_result = SETTLE_LOSE
                    from logic.comsys.battle.Improvise.ImproviseRoundSettleUI import ImproviseRoundSettleUI
                    ImproviseRoundSettleUI(None, settle_result, self._group_points_dict, self_group_id, delay_close_time=left_time)
                self._notified_end_round = self.round_number
            return