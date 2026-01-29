# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/SpectateMgr.py
from __future__ import absolute_import
from logic.entities.BaseClientEntity import BaseClientEntity
from logic.gcommon.common_const import spectate_const
from mobile.common.EntityFactory import EntityFactory
from logic.gcommon import time_utility
from collections import deque
import logic.gcommon.time_utility as time_util
from mobile.common.EntityManager import Dynamic
from mobile.common.IdManager import IdManager
import time as sys_time
from logic.gutils import spectate_utils
import math3d
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from mobile.common.RpcIndex import RpcIndexer
from logic.gcommon.common_const import battle_const

@Dynamic
class SpectateMgr(BaseClientEntity):

    def __init__(self):
        super(SpectateMgr, self).__init__()
        self._start_time = None
        self._msg_cache = None
        self._battle_loaded = False
        self._start_load_time = sys_time.time()
        self._load_from_file = False
        self._is_speed_up = False
        self._manual_switch_obj_uid = None
        self._last_manual_switch_time = None
        self._for_ob = False
        self._cached_top_soul_infos = None
        self._all_player_info_dict = {}
        self._all_team_info_dict = {}
        self._timeout_times = 0
        self._init_max_wait_time = 0
        self._last_sync_time = 0
        self._soul_direct_rpc_names = set()
        self._delay_switch_load_timer = None
        self._delay_switch_load_entities = []
        self._msg_adder = {spectate_const.GLOBAL_SPECTATE_SYNC_SNAPSHOT: self._on_snapshot,
           spectate_const.GLOBAL_SPECTATE_SYNC_METHOD: self._on_method,
           spectate_const.GLOBAL_SPECTATE_SWITCH_OBJ: self._on_switch,
           spectate_const.GLOBAL_SPECTATE_BATTLE_FINISH: self._on_method,
           spectate_const.GLOBAL_SPECTATE_BATTLE_RPC: self._on_method,
           spectate_const.GLOBAL_SPECTATE_SYNC_CANDIDATES: self._on_method,
           spectate_const.GLOBAL_SPECTATE_SYNC_PLAYER_INFO_FOR_OB: self._on_ob_sync_player_info,
           spectate_const.GLOBAL_SPECTATE_OB_BATTLE_FINISH: self._on_method,
           spectate_const.GLOBAL_SPECTATE_UPDATE_PLAYER_INFO_FOR_OB: self._on_method,
           spectate_const.GLOBAL_SPECTATE_OB_ENTER_GOD_CAMERA: self._on_method,
           spectate_const.GLOBAL_SPECTATE_SOUL_DIRECT_SYNC: self._on_soul_direct_method
           }
        self._msg_handler = {spectate_const.GLOBAL_SPECTATE_SYNC_METHOD: self._handler_do_method,
           spectate_const.GLOBAL_SPECTATE_SWITCH_OBJ: self._handler_switch,
           spectate_const.GLOBAL_SPECTATE_BATTLE_FINISH: self._handler_battle_finish,
           spectate_const.GLOBAL_SPECTATE_BATTLE_RPC: self._handler_battle_rpc,
           spectate_const.GLOBAL_SPECTATE_SYNC_CANDIDATES: self._handler_candidates,
           spectate_const.GLOBAL_SPECTATE_SYNC_PLAYER_INFO_FOR_OB: self._handler_player_info_for_ob,
           spectate_const.GLOBAL_SPECTATE_OB_BATTLE_FINISH: self._handler_ob_battle_finish,
           spectate_const.GLOBAL_SPECTATE_UPDATE_PLAYER_INFO_FOR_OB: self._handler_update_player_info_for_ob,
           spectate_const.GLOBAL_SPECTATE_OB_ENTER_GOD_CAMERA: self._handler_enter_god_camera,
           spectate_const.GLOBAL_SPECTATE_SOUL_DIRECT_SYNC: self._handler_soul_direct_sync
           }
        time_utility.reset_stamp_delta_battle()
        return

    def load_battle(self, battle_id, battle_entity_type, battle_init_dict, obj_id, from_file=False, for_ob=False):
        self._battle_id = IdManager.str2id(battle_id)
        self._obj_id = IdManager.str2id(obj_id) if obj_id else None
        self._obj_uid = None
        self._load_from_file = from_file
        self._battle = EntityFactory.instance().create_entity(str(battle_entity_type), self._battle_id)
        battle_init_dict['is_spectate'] = True
        self._battle.init_from_dict(battle_init_dict)
        self._for_ob = for_ob
        global_data.is_judge_ob = for_ob
        self._init_max_wait_time = self._get_battle_init_max_wait_time()
        raw_all_player_info = battle_init_dict.get('all_player_info', {})
        player_info_dict = spectate_utils.parse_all_spectate_ob_player_info(raw_all_player_info)
        self._all_player_info_dict = player_info_dict
        self._all_team_info_dict = spectate_utils.transform_to_group_dict(player_info_dict)
        self._timeout_times = 0
        return

    def destroy(self):
        if self._battle:
            self._battle.destroy()
            self._battle = None
        if self._msg_cache:
            self._msg_cache.clear()
            self._msg_cache = None
        self._msg_adder = None
        self._msg_handler = None
        self._obj_uid = None
        self._cached_top_soul_infos = None
        self._all_player_info_dict.clear()
        self._all_team_info_dict.clear()
        self._soul_direct_rpc_names.clear()
        self.clear_delay_switch_load_timer()
        time_utility.reset_stamp_delta_battle()
        super(SpectateMgr, self).destroy()
        global_data.is_judge_ob = False
        return

    def get_battle_id(self):
        return self._battle_id

    def add_msg(self, msg_type, msg_time, msg):
        if msg_type == spectate_const.GLOBAL_SPECTATE_SYNC_SNAPSHOT and self._manual_switch_obj_uid is not None and self._manual_switch_obj_uid > 0:
            snapshot_info = msg
            obj_id, obj_uid = snapshot_info[2]
            if obj_uid == self._manual_switch_obj_uid:
                self._start_time = None
                self._start_load_time = sys_time.time()
                self.clear_delay_switch_load_timer()
                self._battle.destroy_all_entities((global_data.player.id,))
                global_data.emgr.judge_ob_destroy_all_entities.emit()
                self._msg_cache = None
        self._msg_adder[msg_type](msg_type, msg_time, msg)
        return

    def _on_snapshot(self, msg_type, msg_time, msg):
        if self._msg_cache is None:
            self._msg_cache = deque()
        self._msg_cache.appendleft((msg_type, msg_time, msg))
        return

    def _on_switch(self, msg_type, msg_time, msg):
        if self._msg_cache is None:
            return
        else:
            self._msg_cache.appendleft((msg_type, msg_time, msg))
            return

    def _on_method(self, msg_type, msg_time, msg):
        if self._msg_cache is None:
            return
        else:
            self._msg_cache.appendleft((msg_type, msg_time, msg))
            return

    def _on_soul_direct_method(self, msg_type, msg_time, msg):
        self._handler_soul_direct_sync(msg)

    def _on_ob_sync_player_info(self, msg_type, msg_time, msg):
        self._handler_player_info_for_ob(msg)

    def start(self):
        if self._battle is None:
            return
        else:
            self._battle_loaded = True
            return

    def _get_battle_init_max_wait_time(self):
        if self._for_ob:
            battle_type = self._battle.get_battle_tid()
            if not battle_type:
                return spectate_const.GLOBAL_SPECTATE_MAX_INIT_TIME * 6
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(battle_type))
            prepare_time = battle_info.get('prepare_time', 0)
            flight_time = self._battle.get_flight_time()
            if prepare_time > 0:
                if flight_time > 0:
                    return prepare_time + 4 * flight_time
                return prepare_time * 4
            return spectate_const.GLOBAL_SPECTATE_MAX_INIT_TIME * 6
        return spectate_const.GLOBAL_SPECTATE_MAX_INIT_TIME

    def _do_battle_init(self):
        if self._msg_cache is None:
            if sys_time.time() - self._start_load_time > self._init_max_wait_time:
                global_data.player.on_global_spectate_timeout(self._for_ob, self._timeout_times)
                self._timeout_times += 1
            return
        else:
            if not self._msg_cache or len(self._msg_cache) <= 0:
                return
            msg_type, msg_time, snapshot_info = self._msg_cache.pop()
            init_dict = snapshot_info[0]
            init_dict.update({'init_max_hp': 200,
               'uid': global_data.player.uid,
               'faction_id': 1
               })
            self._battle.add_entity((global_data.player.id, 10000000000L, init_dict))
            for one_msg in snapshot_info[1]:
                self._handler_battle_rpc(one_msg)

            self._obj_id, self._obj_uid = snapshot_info[2]
            if not self._load_from_file and len(self._msg_cache):
                self._start_time = self._msg_cache[0][1] if 1 else msg_time
                self._start_time -= spectate_const.SPECTATE_DELAY_PUBLISH_TICK_INTERVAL + 1
                time_util.trans_to_battle()
                if not self._load_from_file and self._for_ob:
                    time_utility.reset_stamp_delta_battle()
                else:
                    time_util.on_sync_time(time_utility.TYPE_BATTLE, self._start_time, True)
                global_data.player.stop_battle_sync_time()
                for entity_type, entityid, aoi_id, client_dict in snapshot_info[3]:
                    e = self._battle.create_entity(entity_type, entityid, aoi_id, client_dict)
                    if entity_type == 'Mecha':
                        if e.logic:
                            logic = e.logic
                            if not logic.get_com('ComMoveSyncReceiver2Stash'):
                                com = logic.add_com('ComMoveSyncReceiver2Stash', 'client')
                                if com:
                                    com.init_from_dict(logic, client_dict)

                global_data.player.logic.send_event('E_SPECTATE_OBJ', self._obj_id)
                is_manual_switch = self._load_from_file or False
                if self._manual_switch_obj_uid == self._obj_uid:
                    is_manual_switch = True
                    self._manual_switch_obj_uid = None
                    self._last_manual_switch_time = None
                    global_data.player.reset_spectate_can_req_manual_switch()
                    global_data.emgr.spectate_manual_switch_succeed.emit()
                global_data.player.call_server_method('on_global_spectate_switch', (self._obj_uid, is_manual_switch))
            self._timeout_times = 0
            return

    def delay_load_entities_after_switch(self, entities_list):
        from common.utils.timer import CLOCK
        self._delay_switch_load_entities = list(entities_list)
        obj_id_idx = 0
        for idx, entity_info in enumerate(entities_list):
            entity_type, entityid, aoi_id, client_dict = entity_info
            if entityid == self._obj_id:
                obj_id_idx = idx
                break

        entity_info = self._delay_switch_load_entities.pop(obj_id_idx)
        self._delay_switch_load_entities.append(entity_info)
        self.load_one_entity_after_switch()
        self._delay_switch_load_timer = global_data.game_mgr.register_logic_timer(self.load_one_entity_after_switch, interval=0.2, mode=CLOCK)

    def load_one_entity_after_switch(self):
        if not self._delay_switch_load_entities:
            global_data.game_mgr.unregister_logic_timer(self._delay_switch_load_timer)
            self._delay_switch_load_timer = None
            return
        else:
            entity_info = self._delay_switch_load_entities.pop()
            entity_type, entityid, aoi_id, client_dict = entity_info
            entity = self._battle.create_entity(entity_type, entityid, aoi_id, client_dict)
            if entity_type == 'Mecha':
                if entity.logic:
                    logic = entity.logic
                    if not logic.get_com('ComMoveSyncReceiver2Stash'):
                        com = logic.add_com('ComMoveSyncReceiver2Stash', 'client')
                        if com:
                            com.init_from_dict(logic, client_dict)
            return

    def clear_delay_switch_load_timer(self):
        if self._delay_switch_load_timer:
            global_data.game_mgr.unregister_logic_timer(self._delay_switch_load_timer)
            self._delay_switch_load_timer = None
        return

    def tick(self, delta):
        if self._manual_switch_obj_uid is not None and self._manual_switch_obj_uid > 0 and self._last_manual_switch_time:
            if sys_time.time() - self._last_manual_switch_time > spectate_const.GLOBAL_SPECTATE_MANUAL_SWITCH_MAX_WAIT_TIME:
                global_data.player.on_global_spectate_switch_timeout(self._for_ob)
                error_content = 'SpectateMgr on_global_spectate_switch_timeout passed interval=%s, self._manual_switch_obj_uid=%s' % (sys_time.time() - self._last_manual_switch_time, self._manual_switch_obj_uid)
                log_error(error_content)
                import exception_hook
                exception_hook.post_error(error_content)
                return
        if self._start_time is None:
            if self._battle_loaded:
                self._do_battle_init()
            return
        else:
            if self._msg_cache is None:
                return
            if self._load_from_file and self._is_speed_up:
                return
            if self._msg_cache and self._for_ob:
                msg_type, msg_time, msg = self._msg_cache[0]
                self._fix_local_time(msg_time)
            now = time_util.time()
            while self._msg_cache and len(self._msg_cache) != 0:
                msg_type, msg_time, msg = self._msg_cache[-1]
                if msg_time > now:
                    break
                self._msg_cache.pop()
                handler_method = self._msg_handler.get(msg_type)
                if handler_method:
                    if handler_method(msg):
                        break

            return

    def _fix_local_time(self, msg_time):
        if msg_time and sys_time.time() - self._last_sync_time > time_util.BATTLE_HEART_BEAT_ITVL:
            time_util.on_sync_time(time_util.TYPE_BATTLE, msg_time)
            self._last_sync_time = sys_time.time()

    def _handler_switch(self, msg):
        self._start_time = None
        self.clear_delay_switch_load_timer()
        self._battle.destroy_all_entities((global_data.player.id,))
        global_data.emgr.judge_ob_destroy_all_entities.emit()
        self._start_load_time = sys_time.time()
        return True

    def _handler_candidates(self, msg):
        if not msg:
            return
        self._cached_top_soul_infos = msg
        global_data.emgr.update_spectate_top_player_infos.emit(self._battle_id, msg)

    def _handler_player_info_for_ob(self, msg):
        if msg:
            alive_player_info = msg[0] if 1 else None
            return alive_player_info or None
        else:
            any_is_alive_state_changed = False
            for eid in self._all_player_info_dict:
                pinfo = self._all_player_info_dict[eid]
                prev_is_alive = pinfo.get('is_alive', None)
                pinfo['is_alive'] = eid in alive_player_info
                is_alive_changed = prev_is_alive != pinfo['is_alive']
                if is_alive_changed:
                    any_is_alive_state_changed = True
                if eid in alive_player_info:
                    self._update_alive_player_info_for_ob(eid, alive_player_info.get(eid))

            if any_is_alive_state_changed:
                global_data.emgr.judge_global_players_dead_state_changed.emit()
            return

    def _update_alive_player_info_for_ob(self, entity_id, player_info):
        pinfo = self._all_player_info_dict.get(entity_id, None)
        if not pinfo or not player_info:
            return
        else:
            for key in spectate_const.SPECTATE_OB_UPDATE_PLAYER_INFO_KEYS:
                if key not in player_info:
                    continue
                raw_key = key
                if key == 'recall_left_time':
                    key = 'recall_cd_end_ts'
                old = pinfo[key] if key in pinfo else None
                if key == 'position':
                    pinfo['position'] = math3d.vector(*player_info['position'])
                elif key == 'recall_cd_end_ts':
                    left_time = player_info[raw_key]
                    from logic.gcommon.time_utility import get_server_time_battle
                    pinfo[key] = get_server_time_battle() + left_time
                else:
                    pinfo[key] = player_info[key]
                if old != pinfo[key]:
                    if key == 'mecha_id':
                        global_data.emgr.judge_global_player_bind_mecha_changed.emit(entity_id, pinfo[key])
                    elif key == 'in_mecha_type':
                        global_data.emgr.judge_global_player_in_mecha_type_changed.emit(entity_id, pinfo[key])
                    elif key == 'recall_cd_type':
                        global_data.emgr.judge_global_player_mecha_cd_type_changed.emit(entity_id, pinfo[key])
                    elif key == 'recall_cd_end_ts':
                        global_data.emgr.judge_global_player_recall_cd_end_ts_changed.emit(entity_id, pinfo[key])
                if key == 'is_attacking':
                    global_data.emgr.judge_global_player_attacking_changed.emit(entity_id, pinfo[key])

            return

    def _handler_update_player_info_for_ob(self, msg):
        if msg:
            update_dict = msg[0] if 1 else None
            return update_dict or None
        else:
            entity_id = update_dict.get('entity_id', None)
            update_info = update_dict.get('update_info', {})
            if entity_id and update_info:
                self._update_alive_player_info_for_ob(entity_id, update_info)
            return

    def _handler_do_method(self, msg):
        for msg_pack in msg:
            if self._for_ob:
                sync_type = msg_pack[0]
                if sync_type == battle_const.SYNC_TYPE_BATTLE:
                    method_index, parameters = msg_pack[1:]
                    method_name = RpcIndexer.INDEX2RPC[method_index]
                    if method_name in self._soul_direct_rpc_names:
                        continue
            self._battle._sync_handler[msg_pack[0]](*msg_pack[1:])

        return False

    def _handler_battle_finish(self, msg):
        global_data.emgr.spectate_battle_finish_event.emit(*msg)
        if global_data.player and self._load_from_file:
            global_data.player.battle_replay_stop()
        return False

    def _handler_ob_battle_finish(self, msg):
        if global_data.is_judge_ob:
            if global_data.judge_camera_mgr:
                global_data.judge_camera_mgr.remove_ui_block()
        from logic.gcommon.common_utils import battle_utils
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH, PLAY_TYPE_CHICKEN, PLAY_TYPE_GVG, PLAY_TYPE_SNIPE, PLAY_TYPE_HTDM, PLAY_TYPE_RANDOMDEATH, PLAY_TYPE_ARMRACE, PLAY_TYPE_CLONE, PLAY_TYPE_CONTROL, PLAY_TYPE_FLAG, PLAY_TYPE_CROWN, PLAY_TYPE_SCAVENGE, PLAY_TYPE_FLAG2, PLAY_TYPE_DEATH_IMBA, PLAY_TYPE_DEATH_AGRAVITY, PLAY_TYPE_DUEL, PLAY_TYPE_TRAIN
        battle_type = msg[0]['battle_type'] if msg else None
        settle_info = msg[0]['settle_info'] if msg else None
        if not battle_type or not settle_info:
            return
        else:
            if global_data.player and global_data.player.is_in_judge_ob():
                global_data.emgr.try_switch_judge_camera_event.emit(False)
            mode_type = battle_utils.get_play_type_by_battle_id(battle_type)
            if mode_type == PLAY_TYPE_CHICKEN:
                self._battle.on_settle_info_for_ob(settle_info)
            else:
                self._battle.on_settle_stage_msg(*settle_info)
            return

    def _handler_battle_rpc(self, msg):
        method_name, params = msg
        method = getattr(self._battle, method_name)
        if self._for_ob and method_name in self._soul_direct_rpc_names:
            return
        method(params)
        return False

    def _handler_soul_direct_sync(self, msg):
        method_name, params, entity_id = msg
        entity = EntityManager.getentity(entity_id) if entity_id else self._battle
        if not entity:
            return False
        else:
            method = getattr(entity, method_name, None)
            if not method:
                return False
            if entity.id == self._battle.id:
                self._soul_direct_rpc_names.add(method_name)
            method(params)
            return False

    def on_reconnected(self):
        sp_obj = self._battle.get_entity(self._obj_id)
        if sp_obj:
            global_data.emgr.scene_observed_player_setted_for_cam.emit(sp_obj.logic)
            global_data.emgr.scene_observed_player_setted_event.emit(sp_obj.logic)
            if sp_obj.logic:
                sp_obj.logic.send_event('E_ON_BEING_OBSERVE', True)

    def get_start_time(self):
        return self._start_time

    def get_cached_msg_size(self):
        if self._msg_cache:
            return len(self._msg_cache)
        return 0

    def get_spectate_target_uid(self):
        return self._obj_uid

    def get_spectate_target_id(self):
        return self._obj_id

    def do_manual_switch(self, new_obj_uid):
        if not new_obj_uid or self._obj_uid == new_obj_uid:
            return
        self._manual_switch_obj_uid = new_obj_uid
        self._last_manual_switch_time = sys_time.time()
        if not self._for_ob:
            global_data.game_mgr.show_tip(get_text_by_id(19607))

    def get_top_player_infos(self):
        return self._cached_top_soul_infos

    def get_switching_obj_uid(self):
        return self._manual_switch_obj_uid

    def _handler_enter_god_camera(self, msg):
        entity_type, entity_id, aoi_id, client_dict = msg
        if self._battle.get_entity(entity_id):
            return
        e = self._battle.create_entity(entity_type, entity_id, aoi_id, client_dict)
        if not e:
            log_error('++++ _handler_enter_god_camera msg=%s, failed to create camera entity.', msg)

    def is_judge_spectate(self):
        return self._for_ob

    def get_player_info_for_ob(self, soul_id, attr_name, default=None):
        return self._all_player_info_dict.get(soul_id, {}).get(attr_name, default)

    def get_all_player_info_for_ob(self):
        return self._all_player_info_dict

    def get_all_team_info_for_ob(self):
        return self._all_team_info_dict

    def speed_up(self, key_frame_num):
        if not self._load_from_file:
            return 0
        else:
            snapshot_num = 0
            for msg_type, msg_time, msg in self._msg_cache:
                if msg_type == spectate_const.GLOBAL_SPECTATE_SYNC_SNAPSHOT:
                    snapshot_num += 1
                    if snapshot_num >= key_frame_num:
                        break

            key_frame_num = min(key_frame_num, snapshot_num)
            if key_frame_num <= 0:
                return 0
            self._is_speed_up = True
            skip_num = 0
            skip_key_frame_num = 0
            while self._msg_cache and len(self._msg_cache) != 0:
                msg_type, msg_time, msg = self._msg_cache[-1]
                if msg_type != spectate_const.GLOBAL_SPECTATE_SYNC_SNAPSHOT:
                    self._msg_cache.pop()
                    skip_num += 1
                else:
                    skip_key_frame_num += 1
                    if skip_key_frame_num < key_frame_num:
                        skip_num += 1
                        self._msg_cache.pop()
                    else:
                        self._handler_switch(None)
                        self._is_speed_up = False
                        return skip_num

            self._is_speed_up = False
            return 0