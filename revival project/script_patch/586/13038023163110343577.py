# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ImproviseBattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.entities.Battle import Battle
from logic.gcommon.common_const.battle_const import ROUND_TYPE_PURE_HUMAN, ROUND_TYPE_MECHA
import logic.gcommon.time_utility as t_util

class ImproviseBattle(Battle):

    def init_from_dict(self, bdict):
        self.area_id = bdict.get('area_id')
        super(ImproviseBattle, self).init_from_dict(bdict)
        self.map_id = bdict.get('map_id')
        self.group_data = bdict.get('group_data', {})

    def boarding_movie_data(self):
        return None

    def get_move_range(self):
        return global_data.improvise_battle_data.get_move_range()

    @rpc_method(CLIENT_STUB, (Dict('group_points_dict'),))
    def update_group_points(self, group_points_dict):
        global_data.improvise_battle_data.update_group_points_data(group_points_dict)

    def request_rank_data(self):
        self.call_soul_method('request_rank_data', (global_data.player,))

    @rpc_method(CLIENT_STUB, (Dict('rank_data'),))
    def reply_rank_data(self, rank_data):
        global_data.improvise_battle_data.update_score_details_data(rank_data)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.improvise_battle_data.set_settle_timestamp(settle_timestamp)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), Int('cur_round'), Int('round_type'), Float('round_begin_ts'), Int('weapon_data_index'), Dict('group_born_index'), Dict('group_points_dict'), Bool('has_sync_yaw')))
    def update_battle_data(self, settle_timestamp, cur_round, round_type, round_begin_ts, weapon_data_index, group_born_index, group_points_dict, has_sync_yaw):
        self.update_settle_timestamp((settle_timestamp,))
        global_data.improvise_battle_data.update_cur_round_data(cur_round, round_type, round_begin_ts, weapon_data_index)
        global_data.improvise_battle_data.update_group_points_data(group_points_dict)
        global_data.improvise_battle_data.set_avatar_adjust_yaw(has_sync_yaw)
        if t_util.get_server_time_battle() > global_data.improvise_battle_data.round_begin_ts > 0:
            self._check_and_show_mecha_ui()

    def notify_avatar_adjust_yaw_already(self, entity):
        if entity is None:
            return
        else:
            self.call_soul_method('sync_soul_yaw', (entity,))
            return

    @rpc_method(CLIENT_STUB, (Int('cur_round'), Int('round_type'), Float('round_begin_ts'), Int('weapon_data_index'), Dict('group_born_index'), Dict('sync_yaw_record'), Bool('is_early_begin')))
    def notify_round_begin(self, cur_round, round_type, round_begin_ts, weapon_data_index, group_born_index, sync_yaw_record, is_early_begin):
        global_data.improvise_battle_data.update_cur_round_data(cur_round, round_type, round_begin_ts, weapon_data_index)
        if global_data.player and global_data.player.logic:
            has_sync_yaw = sync_yaw_record.get(global_data.player.logic.id, False)
            global_data.improvise_battle_data.set_avatar_adjust_yaw(has_sync_yaw)
            global_data.player.logic.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')
        self._check_and_show_mecha_ui()
        from logic.gcommon.time_utility import get_server_time_battle
        cur_time = get_server_time_battle()
        ready_duration = global_data.improvise_battle_data.get_cur_round_begin_ready_duration()
        ready_ts = round_begin_ts + ready_duration
        left_ready_time = ready_ts - cur_time
        if cur_round > 1:
            from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
            from common.const.uiconst import NORMAL_LAYER_ZORDER_1

            def finish_cb():
                self.play_round_prompt_ui(cur_round, weapon_data_index, is_early_begin)
                global_data.emgr.improvise_highlight_on_time.emit(left_ready_time)

            EndTransitionUI(None, callback=finish_cb, need_close_self=True, zorder=NORMAL_LAYER_ZORDER_1)
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_RECOVER_KILLER_CAM')
                global_data.player.logic.send_event('E_TO_THIRD_PERSON_CAMERA')
        elif cur_round == 1:
            self.play_round_prompt_ui(cur_round, weapon_data_index, is_early_begin)
            global_data.emgr.improvise_highlight_on_time.emit(left_ready_time)
        return

    @staticmethod
    def play_round_prompt_ui(round_index, weapon_data_index, is_early_begin=False):
        theme_text_id = global_data.game_mode.get_cfg_data('weapon_plan_data', str(weapon_data_index), 'text_id', default=None)
        if theme_text_id is None:
            if global_data.is_inner_server:
                pass
        else:
            inst = global_data.ui_mgr.show_ui('ImproviseRoundPrompUI', 'logic.comsys.battle.Improvise')
            inst.update(round_index, theme_text_id)
            inst.set_early_begin(is_early_begin)
        return

    @rpc_method(CLIENT_STUB, (Int('cur_round'), Float('round_end_ts'), Int('win_group_id'), Dict('group_points_dict')))
    def notify_round_end(self, cur_round, round_end_ts, win_group_id, group_points_dict):
        if global_data.improvise_battle_data.get_cur_round_no() != cur_round:
            return
        global_data.improvise_battle_data.update_cur_round_settle_data(round_end_ts, win_group_id, group_points_dict)
        if global_data.improvise_battle_data.round_type == ROUND_TYPE_MECHA:
            global_data.ui_mgr.close_ui('StateChangeUI')
        from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
        stop_self_fire_and_movement()

    def _check_and_show_mecha_ui(self):
        if global_data.improvise_battle_data.round_type == ROUND_TYPE_MECHA and global_data.improvise_battle_data.round_mecha_id > 0:
            ui = global_data.ui_mgr.get_ui('StateChangeUI')
            if not ui:
                ui = global_data.ui_mgr.show_ui('StateChangeUI', 'logic.comsys.battle')
            if ui:
                ui.set_bind_mecha(global_data.improvise_battle_data.round_mecha_id)
        else:
            global_data.ui_mgr.close_ui('StateChangeUI')

    @rpc_method(CLIENT_STUB, (Bool('from_defeated'),))
    def notify_begin_spectate(self, from_defeated):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_RECOVER_KILLER_CAM')
            global_data.player.logic.send_event('E_REQ_SPECTATE')

    @rpc_method(CLIENT_STUB, (Dict('group_hp_data'),))
    def reply_group_hp_data(self, group_hp_data):
        global_data.improvise_battle_data.update_group_hp_data(group_hp_data)