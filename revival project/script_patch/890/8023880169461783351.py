# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/GvgBattle.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gutils.CameraHelper import get_adaptive_camera_fov
from logic.entities.Battle import Battle
from logic.gcommon.common_utils import battle_utils
from mobile.common.EntityManager import EntityManager
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.client.const import game_mode_const
from logic.gcommon import time_utility
import world
import math3d
from logic.gcommon.common_utils.local_text import get_text_by_id

class GvgBattle(Battle):

    def __init__(self, entityid):
        super(GvgBattle, self).__init__(entityid)
        self.battle_cb = None
        self.process_event(True)
        self.my_group = None
        self.other_group = None
        self.observed_target_id = None
        self.eid_to_index = {}
        self.group_to_num = {}
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'gvg_enter_battle': self.gvg_enter_battle,
           'scene_observed_player_setted_event': self.update_observed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def boarding_movie_data(self):
        return None

    def init_from_dict(self, bdict):
        battle_srv_time = bdict.get('battle_srv_time', None)
        if battle_srv_time and time_utility.TYPE_BATTLE not in time_utility.g_success_flag:
            time_utility.on_sync_time(time_utility.TYPE_BATTLE, battle_srv_time)
        self.battle_bdict = bdict
        self.map_id = bdict.get('map_id')
        self.group_data = bdict.get('group_data', {})
        self.cur_round = bdict.get('cur_round', 0)
        self.round_end_ts = bdict.get('round_end_ts', 0)
        self.mecha_choose_dict = bdict.get('mecha_choose_dict', {})
        self.confirm_set = bdict.get('confirm_set', [])
        self.is_confirm = global_data.player.id in self.confirm_set
        self.choose_finished = bdict.get('choose_finished', False)
        self.area_id = str(bdict.get('area_id'))
        self._avatar_mecha_dict = bdict.get('mecha_dict', {})
        self._team_names = bdict.get('team_names', {})
        self.start_suicide_result((bdict.get('suicide_timestamp', 0),))
        self.init_eids()

        def _cb():
            global_data.ui_mgr.close_ui('GVGChooseMecha')
            global_data.ui_mgr.close_ui('GVGReadyUI')
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            global_data.emgr.reset_rotate_model_display.emit()
            super(GvgBattle, self).init_from_dict(self.battle_bdict)
            global_data.gvg_battle_data.set_area_id(str(bdict.get('area_id')))

        self.battle_cb = _cb
        if not self.choose_finished:
            scene = global_data.game_mgr.scene
            scene_type = None
            if scene:
                scene_type = scene.get_type()
            if scene_type == scene_const.SCENE_GVG_CHOOSE_MECHA:
                global_data.emgr.enter_choose_mecha.emit()
                return
            if not scene_type or scene_type == scene_const.SCENE_MAIN:

                def _scene_cb():
                    scene = global_data.game_mgr.scene
                    scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.GVG_CHOOSE_MECHA_SCENE)
                    cam_hanger = scene.get_preset_camera(scene_data.get('cam_key'))
                    cam = scene.active_camera
                    cam.rotation_matrix = math3d.rotation_to_matrix(math3d.matrix_to_rotation(cam_hanger.rotation))
                    cam.world_position = cam_hanger.translation
                    fov = scene_data.get('fov', 30)
                    fov, aspect = get_adaptive_camera_fov(fov)
                    cam.fov = fov
                    cam.aspect = aspect
                    global_data.emgr.camera_inited_event.emit()

                    def _switch_scene_cb(*args):
                        global_data.emgr.enter_choose_mecha.emit()

                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_GVG_CHOOSE_MECHA, lobby_model_display_const.GVG_CHOOSE_MECHA_SCENE, finish_callback=_switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_GVG_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
                global_data.ex_scene_mgr_agent.lobby_relatived_scene[scene_const.SCENE_GVG_CHOOSE_MECHA] = scene
            else:

                def _switch_scene_cb(*args):
                    global_data.emgr.enter_choose_mecha.emit()

                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_GVG_CHOOSE_MECHA, lobby_model_display_const.GVG_CHOOSE_MECHA_SCENE, finish_callback=_switch_scene_cb)
        else:
            self.battle_cb()
        return

    def init_eids(self):
        self.eid_to_group_id = {}
        self.eids = []
        for group_id, value in six.iteritems(self.group_data):
            for eid in six.iterkeys(value):
                self.eid_to_group_id[eid] = group_id
                self.eids.append(eid)

        if global_data.player:
            if global_data.player.is_in_global_spectate():
                self.init_eid_to_index(global_data.player.get_global_spectate_player_id())
            else:
                self.init_eid_to_index()

    def init_eid_to_index(self, target_id=None):
        if target_id is None:
            target_id = global_data.player.id
        self.my_group = self.eid_to_group_id.get(target_id)
        need_preserve_seq = self.get_need_preserve_group_sequence()
        if need_preserve_seq:
            sorted_group_id = sorted(six_ex.values(self.eid_to_group_id))
            if sorted_group_id:
                self.my_group = sorted_group_id[0]
        self.other_group = None
        self.observed_target_id = target_id
        self.eid_to_index = {}
        self.group_to_num = {}
        my_group_index = 0
        other_group_index = 0
        for eid in self.eids:
            if self.my_group == self.eid_to_group_id.get(eid):
                if not need_preserve_seq:
                    if target_id != eid:
                        self.eid_to_index[eid] = my_group_index
                        my_group_index += 1
                else:
                    self.eid_to_index[eid] = my_group_index
                    my_group_index += 1
            else:
                if self.other_group is None:
                    self.other_group = self.eid_to_group_id.get(eid)
                self.eid_to_index[eid] = other_group_index
                other_group_index += 1

        if not need_preserve_seq:
            self.eid_to_index[target_id] = my_group_index
            self.group_to_num[self.my_group] = my_group_index + 1
        else:
            self.group_to_num[self.my_group] = my_group_index
        if self.other_group is not None:
            self.group_to_num[self.other_group] = other_group_index
        return

    def is_observed_target_id(self, eid):
        return self.observed_target_id == eid

    def get_need_preserve_group_sequence(self):
        if global_data.is_judge_ob:
            return True
        else:
            return False

    def update_observed(self, ltarget):
        if not ltarget:
            return
        self.init_eid_to_index(target_id=ltarget.id)
        gvg_top_score_ui = global_data.ui_mgr.get_ui('GVGTopScoreUI')
        if gvg_top_score_ui:
            global_data.ui_mgr.close_ui('GVGTopScoreUI')
            global_data.ui_mgr.show_ui('GVGTopScoreUI', 'logic.comsys.battle.gvg')
        if global_data.ui_mgr.get_ui('GVGTopScoreJudgeUI'):
            global_data.ui_mgr.close_ui('GVGTopScoreJudgeUI')
            global_data.ui_mgr.show_ui('GVGTopScoreJudgeUI', 'logic.comsys.battle.gvg')
        gvg_score_details_ui = global_data.ui_mgr.get_ui('GVGScoreDetailsUI')
        if gvg_score_details_ui:
            global_data.ui_mgr.close_ui('GVGScoreDetailsUI')
            global_data.ui_mgr.show_ui('GVGScoreDetailsUI', 'logic.comsys.battle.gvg')

    def is_friend_group(self, eid):
        return self.my_group == self.eid_to_group_id.get(eid)

    def gvg_enter_battle(self):
        if self.battle_cb:
            self.battle_cb()

    def request_choose_mecha(self, round_idx, mecha_id):
        self.call_soul_method('request_choose_mecha', (round_idx, mecha_id))

    def confirm_choose_mecha(self, round_idx):
        self.call_soul_method('confirm_choose_mecha', (round_idx,))
        self.is_confirm = True

    def request_rank_data(self):
        self.call_soul_method('request_rank_data', (global_data.player,))

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(GvgBattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Uuid('eid'), Int('mecha_id')))
    def on_choose_mecha(self, round_idx, eid, mecha_id):
        if eid not in self.mecha_choose_dict:
            self.mecha_choose_dict[eid] = {}
        self.mecha_choose_dict[eid][round_idx] = mecha_id
        global_data.emgr.refresh_choose_mecha.emit(round_idx, eid, mecha_id)

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Float('round_end_ts')))
    def start_new_round(self, round_idx, round_end_ts):
        self.is_confirm = False
        self.cur_round = round_idx
        self.round_end_ts = round_end_ts
        self.confirm_set = []
        global_data.emgr.refresh_start_new_round.emit(round_idx, round_end_ts)

    @rpc_method(CLIENT_STUB, ())
    def choose_mecha_finished(self):
        if self.choose_finished:
            return
        self.choose_finished = True
        global_data.emgr.choose_mecha_finished.emit()

    @rpc_method(CLIENT_STUB, (Float('final_prate'),))
    def final_stage(self, final_prate):
        self.is_in_ace_state = True
        message = [
         {'i_type': battle_const.TDM_THREE_TIMES_POINT,'set_num_func': 'set_show_percent_num','show_num': int(max(0, final_prate - 1) * 100)
            }, {'i_type': battle_const.SECOND_ACE_TIME}]
        message_type = [
         battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), Dict('mecha_use_dict'), Dict('mecha_revice_ts_dict')))
    def update_battle_data(self, settle_timestamp, mecha_use_dict, mecha_revice_ts_dict):
        self.update_settle_timestamp((settle_timestamp,))
        global_data.gvg_battle_data.update_battle_data(mecha_use_dict, mecha_revice_ts_dict)
        global_data.gvg_battle_data.player_req_spectate()

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.gvg_battle_data.set_settle_timestamp(settle_timestamp)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('mecha_idx'), Dict('killer_info'), Float('mecha_revice_ts')))
    def on_mecha_destroyed(self, soul_id, mecha_idx, killer_info, mecha_revice_ts):
        global_data.gvg_battle_data.set_mecha_destroyed(soul_id, mecha_idx, mecha_revice_ts)
        global_data.emgr.gvg_mecha_destroyed.emit(soul_id, mecha_idx, killer_info, mecha_revice_ts)

    @rpc_method(CLIENT_STUB, (Dict('rank_data'),))
    def reply_rank_data(self, rank_data):
        if global_data.gvg_battle_data:
            global_data.gvg_battle_data.update_score_details_data(rank_data)

    @rpc_method(CLIENT_STUB, (Dict('left_player_dict'),))
    def update_score_msg(self, left_player_dict):
        global_data.emgr.update_score_msg.emit(left_player_dict)

    def start_combat(self):
        self.call_soul_method('start_combat', ())

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('DeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (List('prompt_id_list'), Str('eid'), Str('name'), Dict('short_kill_info')))
    def on_kill_prompt(self, prompt_id_list, eid, name, short_kill_info):
        killer_mecha_id = short_kill_info.get('killer_mecha_fashion', {}).get(FASHION_POS_SUIT)
        mecha_eid = short_kill_info.get('mecha_eid')
        mecha_id = short_kill_info.get('mecha_fasion', {}).get(FASHION_POS_SUIT)
        mecha_entity = EntityManager.getentity(mecha_eid)
        cam_lctarget = global_data.cam_lctarget
        for prompt_id in prompt_id_list:
            if cam_lctarget and mecha_entity and mecha_entity.logic:
                if cam_lctarget.ev_g_is_campmate(mecha_entity.logic.ev_g_camp_id()):
                    frd_mecha_id = mecha_id
                    eny_mecha_id = killer_mecha_id
                    frd_is_killer = False
                else:
                    frd_mecha_id = killer_mecha_id
                    eny_mecha_id = mecha_id
                    frd_is_killer = True
                if frd_mecha_id and eny_mecha_id:
                    msg = battle_utils.get_kill_prompt_msg(prompt_id, frd_mecha_id, eny_mecha_id, frd_is_killer, name)
                    global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def start_suicide(self):
        self.call_soul_method('start_suicide', ())

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Uuid('soul_id')))
    def on_confirm_choose_mecha(self, round_idx, soul_id):
        self.confirm_set.append(soul_id)
        global_data.emgr.refresh_confirm_choose_mecha.emit(soul_id)

    def get_suicide_timestamp(self):
        return self.suicide_timestamp

    def get_competition_team_names(self):
        return self._team_names

    def destroy(self, clear_cache=True):
        self.process_event(False)
        if clear_cache:
            global_data.ui_mgr.close_ui('GVGChooseMecha')
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            global_data.emgr.reset_rotate_model_display.emit()
        super(GvgBattle, self).destroy(clear_cache)

    @rpc_method(CLIENT_STUB, ())
    def on_force_finish_battle(self):
        global_data.game_mgr.show_tip(get_text_by_id(19712))
        self.destroy()

    def report_soul_load_prog(self, prog):
        self.call_soul_method('report_soul_load_prog', (prog,))

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('prog')))
    def update_player_load_prog(self, soul_id, prog):
        global_data.emgr.gvg_player_loading_update.emit(soul_id, prog)

    @rpc_method(CLIENT_STUB, (Int('spawn_id'), Int('faction_id'), Float('rebirth_ts')))
    def update_spawn_rebirth(self, spawn_id, faction_id, rebirth_ts):
        global_data.gvg_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])