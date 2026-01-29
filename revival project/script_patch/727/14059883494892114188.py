# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/FastSurvivalBattle.py
from __future__ import absolute_import
import six
import six_ex
import math3d
from logic.entities.Battle import Battle
from logic.entities.SurvivalBattle import SurvivalBattle
from logic.gcommon.common_utils import parachute_utils
from mobile.common.EntityManager import EntityManager
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.time_utility import time
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE, OPEN_CONDITION_OPEN, OPEN_CONDITION_AIM_OPEN

class FastSurvivalBattle(SurvivalBattle):

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_num = stage_dict.get('prepare_num', 0)
        player_num = stage_dict.get('fighter_num', 0)
        prepare_timestamp = stage_dict.get('prepare_timestamp', 0)
        flight_dict = stage_dict.get('flight_dict', {})
        poison_circle = stage_dict.get('poison_dict', {})
        self.update_prepare_num((prepare_num, player_num))
        self.flight_dict = flight_dict
        self.prepare_timestamp = prepare_timestamp
        self.poison_circle = poison_circle
        self.on_battle_status_changed(Battle.BATTLE_STATUS_PREPARE)
        self.init_top_nb_info(stage_dict)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def parachute_stage(self, stage_dict):
        prepare_num = stage_dict.get('prepare_num', 0)
        player_num = stage_dict.get('fighter_num', 0)
        poison_circle = stage_dict.get('poison_dict', {})
        flight_dict = stage_dict.get('flight_dict', {})
        self.poison_circle = poison_circle
        if not flight_dict:
            return
        lavatar = global_data.player.logic
        from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE
        from logic.comsys.accelerometer.AccInput import AccInput
        self.update_prepare_num((prepare_num, player_num))
        self.flight_dict = flight_dict
        AccInput().switch_acc_input_open_condition(OPEN_CONDITION_NONE)
        lavatar.send_event('E_INIT_PARACHUTE_COM')
        from logic.gutils import judge_utils
        is_ob = judge_utils.is_ob()
        exclude_list = [
         global_data.player.id]
        if not is_ob:
            exclude_list = global_data.player.logic.ev_g_groupmate() or exclude_list
            all_puppet = EntityManager.get_entities_by_type('Puppet')
            for k, v in six.iteritems(all_puppet):
                if k in exclude_list:
                    continue
                if not v.logic:
                    continue
                if not v.logic.ev_g_in_parachute_stage_idle():
                    exclude_list.append(k)

        else:
            all_puppet = EntityManager.get_entities_by_type('Puppet')
            p_list = six_ex.keys(all_puppet)
            p_list = list(p_list)
            exclude_list.extend(p_list)
        self.destroy_all_entities(exclude=exclude_list)
        psg_list = []
        if is_ob:
            exclude_list = exclude_list[1:]
        for eid in exclude_list:
            ent = EntityManager.getentity(eid)
            if ent and ent.logic:
                ent_stage = ent.logic.share_data.ref_parachute_stage
                if ent_stage in (STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE):
                    psg_list.append(eid)
                    ent.logic.reset()
                if ent_stage == STAGE_NONE or ent_stage == STAGE_MECHA_READY:
                    ent.logic.send_event('E_PLANE')
                    ent.logic.send_event('E_UNLIMIT_HEIGHT')

        self._check_create_plane()
        if self.plane and self.plane():
            global_data.emgr.plane_set_passenger_event.emit(psg_list)
            if lavatar.id == lavatar.ev_g_spectate_target_id():
                if lavatar.id in psg_list:
                    if plane.logic:
                        cur_plane_yaw = plane.logic.ev_g_plane_cur_yaw()
                        global_data.emgr.camera_set_yaw_event.emit(cur_plane_yaw)
            plane_start_timestamp = flight_dict['start_timestamp']
            dt = max(0, flight_dict['ready_time'] - max(0, time() - plane_start_timestamp))
            if dt > 0:
                import game3d
                game3d.delay_exec(dt * 1000, lambda : self.plane_stage_start())
            else:
                self.plane_stage_start()
        lavatar.send_event('E_CLEAN_JUMP')
        global_data.sound_mgr.play_music('flight')
        global_data.sound_mgr.poison_level = 0
        self.on_battle_status_changed(Battle.BATTLE_STATUS_PARACHUTE)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        player_num = stage_dict.get('fighter_num', 0)
        poison_circle = stage_dict.get('poison_dict', {})
        battle_mark = stage_dict.get('mark_dict', {})
        self.update_player_num((player_num,))
        self.on_battle_status_changed(Battle.BATTLE_STATUS_FIGHT)
        global_data.player.logic and global_data.player.logic.send_event('E_START_POSITION_CHECKER')
        stage = lavt.share_data.ref_parachute_stage
        if stage not in [parachute_utils.STAGE_NONE, parachute_utils.STAGE_PLANE]:
            self.init_poison_circle(poison_circle)
        self.poison_circle = poison_circle
        global_mark_dict = battle_mark.get('global_mark_dict', {})
        group_mark_dict = battle_mark.get('group_mark_dict', {})
        soul_mark_dict = battle_mark.get('soul_mark_dict', {})
        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(global_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(group_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(soul_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

    def on_player_parachute_stage_changed(self, stage):
        if stage == parachute_utils.STAGE_FREE_DROP and self.poison_circle:
            self.init_poison_circle(self.poison_circle)

    def init_poison_circle(self, poison_dict):
        from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_READY, POISON_CIRCLE_STATE_STABLE, POISON_CIRCLE_STATE_REDUCE, POISON_CIRCLE_STATE_OVER
        if not poison_dict:
            return
        state = poison_dict['state']
        refresh_time = poison_dict['refresh_time']
        last_time = poison_dict['last_time']
        level = poison_dict['level']
        poison_point = poison_dict['poison_point']
        safe_point = poison_dict['safe_point']
        reduce_type = poison_dict['reduce_type']
        if state in (POISON_CIRCLE_STATE_READY, POISON_CIRCLE_STATE_STABLE, POISON_CIRCLE_STATE_OVER):
            self.refresh_poison_circle((state, reduce_type, refresh_time, last_time, level, poison_point, safe_point))
        elif state == POISON_CIRCLE_STATE_REDUCE:
            self.refresh_poison_circle((state, reduce_type, 0, 0, level, poison_point, safe_point))
            self.reduce_poison_circle((state, reduce_type, refresh_time, last_time))
        global_data.emgr.scene_reset_poison_level.emit(level)