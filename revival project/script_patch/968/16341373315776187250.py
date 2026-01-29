# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/DuelBattle.py
from __future__ import absolute_import
from __future__ import print_function
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
from logic.gcommon import time_utility
import world
import math3d
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import game_mode_const
from logic.comsys.battle import BattleUtils
INTERVAL_HIDE_UI_LIST = [
 'MechaUI',
 'FireRockerUI',
 'PostureControlUI',
 'MoveRockerUI',
 'MoveRockerTouchUI',
 'BulletReloadUI',
 'FightLeftShotUI',
 'HpInfoUI']
ROUND_WIN = 1
ROUND_DRAW = 0
ROUND_LOSE = -1
LOADING_CLOSE_TIME = 4

class DuelBattle(Battle):

    def __init__(self, entityid):
        super(DuelBattle, self).__init__(entityid)
        self.battle_cb = None
        self.process_event(True)
        self.my_group = None
        self.other_group = None
        self.observed_target_id = None
        self.eid_to_index = {}
        self.group_to_num = {}
        self.loading_timer_id = None
        self.ready_box_anim_time = 1
        self.ui_start_diff_time = -2
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'gvg_enter_battle': self.gvg_enter_battle,
           'scene_observed_player_setted_event': self.update_observed,
           'mecha_control_main_ui_event': self.on_mecha_control_main_setted
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
        self.max_choose_round = bdict.get('max_choose_round', 0)
        self.cur_choose_round = bdict.get('cur_choose_round', 0)
        self.choose_round_end_ts = bdict.get('choose_round_end_ts', 0)
        self.mecha_choose_dict = bdict.get('mecha_bp_dict', {}).get('mecha_choose_dict', {})
        self.max_ban_round = bdict.get('max_ban_round', 0)
        self.cur_ban_round = bdict.get('cur_ban_round', 0)
        self.ban_round_end_ts = bdict.get('ban_round_end_ts', 0)
        self.mecha_ban_dict = bdict.get('mecha_bp_dict', {}).get('mecha_ban_dict', {})
        self.soul_round_record = bdict.get('soul_round_record', {})
        self.cur_battle_round = bdict.get('cur_round', 0)
        self.round_settle_timestamp = bdict.get('round_settle_timestamp', 0)
        self._round_prepare_timestamp = bdict.get('round_prepare_timestamp', 0)
        self.confirm_set = bdict.get('confirm_set', [])
        self.is_confirm = global_data.player.id in self.confirm_set
        self.choose_finished = bdict.get('choose_finished', False)
        self.area_id = str(bdict.get('area_id'))
        self._avatar_mecha_dict = bdict.get('mecha_dict', {})
        self._team_names = bdict.get('team_names', {})
        self.start_suicide_result((bdict.get('suicide_timestamp', 0),))
        self.duel_win_cnt_dict = bdict.get('duel_win_cnt_dict', {})
        self._round_status = bdict.get('round_status')
        self.init_eids()

        def _cb():
            global_data.ui_mgr.close_ui('DuelChooseMecha')
            global_data.ui_mgr.close_ui('GVGReadyUI')
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            global_data.emgr.reset_rotate_model_display.emit()
            super(DuelBattle, self).init_from_dict(self.battle_bdict)
            global_data.gvg_battle_data.set_area_id(str(bdict.get('area_id')))

        self.battle_cb = _cb
        if not self.choose_finished:
            scene = global_data.game_mgr.scene
            scene_type = None
            if scene:
                scene_type = scene.get_type()
            if scene_type == scene_const.SCENE_GVG_CHOOSE_MECHA:
                global_data.emgr.enter_choose_mecha.emit(game_mode_const.GAME_MODE_DUEL)
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
                        global_data.emgr.enter_choose_mecha.emit(game_mode_const.GAME_MODE_DUEL)

                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_GVG_CHOOSE_MECHA, lobby_model_display_const.GVG_CHOOSE_MECHA_SCENE, finish_callback=_switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_GVG_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
                global_data.ex_scene_mgr_agent.lobby_relatived_scene[scene_const.SCENE_GVG_CHOOSE_MECHA] = scene
            else:

                def _switch_scene_cb(*args):
                    global_data.emgr.enter_choose_mecha.emit(game_mode_const.GAME_MODE_DUEL)

                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_GVG_CHOOSE_MECHA, lobby_model_display_const.GVG_CHOOSE_MECHA_SCENE, finish_callback=_switch_scene_cb)
        else:
            self.battle_cb()
        return

    def is_ban_stage(self):
        if self.cur_ban_round <= self.max_ban_round and self.cur_choose_round == 0 and self.choose_round_end_ts == 0:
            return True
        else:
            return False

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
        print('TTTT prepare_stage', stage_dict)
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(DuelBattle, self).prepare_stage((stage_dict,))
        self.check_loading_register_timer()

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Uuid('eid'), Int('mecha_id')))
    def on_choose_mecha(self, round_idx, eid, mecha_id):
        if eid not in self.mecha_choose_dict:
            self.mecha_choose_dict[eid] = {}
        self.mecha_choose_dict[eid][round_idx] = mecha_id
        global_data.emgr.refresh_choose_mecha.emit(round_idx, eid, mecha_id)

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Float('round_end_ts')))
    def start_new_choose_round(self, round_idx, round_end_ts):
        self.is_confirm = False
        self.cur_choose_round = round_idx
        self.choose_round_end_ts = round_end_ts
        self.confirm_set = []
        global_data.emgr.refresh_start_new_round.emit(round_idx, round_end_ts)

    @rpc_method(CLIENT_STUB, ())
    def choose_mecha_finished(self):
        if self.choose_finished:
            return
        self.choose_finished = True
        for eid in self.eids:
            if eid not in self.confirm_set:
                self.confirm_set.append(eid)
                global_data.emgr.choose_mecha_finished_pre.emit(eid)

        global_data.game_mgr.delay_exec(3.0, lambda : global_data.emgr.choose_mecha_finished.emit())

    @rpc_method(CLIENT_STUB, (Float('final_prate'),))
    def final_stage(self, final_prate):
        self.is_in_ace_state = True
        message = [
         {'i_type': battle_const.TDM_THREE_TIMES_POINT,'set_num_func': 'set_show_percent_num','show_num': int(max(0, final_prate - 1) * 100)
            }, {'i_type': battle_const.SECOND_ACE_TIME}]
        message_type = [
         battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Uuid('eid'), Int('mecha_id')))
    def on_ban_mecha(self, round_idx, eid, mecha_id):
        if eid not in self.mecha_ban_dict:
            self.mecha_ban_dict[eid] = {}
        self.mecha_ban_dict[eid][round_idx] = mecha_id
        global_data.emgr.refresh_ban_mecha_event.emit(round_idx, eid, mecha_id)

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Float('round_end_ts')))
    def start_new_ban_round(self, round_idx, round_end_ts):
        self.is_confirm = False
        self.cur_ban_round = round_idx
        self.ban_round_end_ts = round_end_ts
        self.confirm_set = []
        global_data.emgr.refresh_start_new_ban.emit(round_idx, round_end_ts)

    def request_ban_mecha(self, round_idx, mecha_id):
        self.call_soul_method('request_ban_mecha', (round_idx, mecha_id))

    def confirm_ban_mecha(self, round_idx):
        self.call_soul_method('confirm_ban_mecha', (round_idx,))
        self.is_confirm = True

    @rpc_method(CLIENT_STUB, (Int('round_idx'), Uuid('soul_id')))
    def on_confirm_ban_mecha(self, round_idx, soul_id):
        self.confirm_set.append(soul_id)
        global_data.emgr.refresh_confirm_ban_mecha_event.emit(soul_id)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), Dict('exta_dict')))
    def update_battle_data(self, settle_timestamp, exta_dict):
        print('TTTT update_battle_data', settle_timestamp, exta_dict)
        self.round_settle_timestamp = exta_dict.get('round_settle_timestamp')
        self.cur_battle_round = exta_dict.get('cur_round')
        self.soul_round_record = exta_dict.get('soul_round_record', {})
        self.update_settle_timestamp((settle_timestamp,))
        global_data.emgr.update_battle_data.emit()
        global_data.gvg_battle_data.player_req_spectate()

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = self.round_settle_timestamp
        global_data.gvg_battle_data.set_settle_timestamp(self.settle_timestamp)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('mecha_idx'), Dict('killer_info'), Float('mecha_revice_ts')))
    def on_mecha_destroyed(self, soul_id, mecha_idx, killer_info, mecha_revice_ts):
        global_data.gvg_battle_data.set_mecha_destroyed(soul_id, mecha_idx, mecha_revice_ts)
        global_data.emgr.gvg_mecha_destroyed.emit(soul_id, mecha_idx, killer_info, mecha_revice_ts)

    @rpc_method(CLIENT_STUB, (Dict('rank_data'),))
    def reply_rank_data(self, rank_data):
        if global_data.gvg_battle_data:
            global_data.gvg_battle_data.update_score_details_data(rank_data)

    @rpc_method(CLIENT_STUB, (Dict('soul_round_record'),))
    def update_score_msg(self, soul_round_record):
        self.soul_round_record = soul_round_record

    def get_round_record(self, soul_id):
        return self.soul_round_record.get(soul_id, [-1, -1, -1])

    def get_is_in_round_interval(self):
        return self._round_status == battle_const.ROUND_STATUS_INTERVAL

    def get_eid_win_cnt(self, soul_id):
        soul_list = self.soul_round_record.get(soul_id, [-1, -1, -1])
        return len([ ret for ret in soul_list if ret == 1 ])

    def get_eid_round_ret(self, soul_id, round_idx):
        soul_list = self.soul_round_record.get(soul_id, [-1, -1, -1])
        if round_idx < len(soul_list):
            return soul_list[round_idx]
        else:
            return -1

    def start_combat(self):
        self.call_soul_method('start_combat', ())

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('DeathPlayBackUI')

    @rpc_method(CLIENT_STUB, ())
    def start_set_out_all_soul(self):
        print('TTTT start_set_out_all_soul')
        self.show_interval_count_down()
        self.exit_interval_view()
        global_data.emgr.duel_round_interval_event.emit()

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
        self.unregister_timer()
        self.process_event(False)
        if clear_cache:
            global_data.ui_mgr.close_ui('DuelChooseMecha')
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            global_data.emgr.reset_rotate_model_display.emit()
        super(DuelBattle, self).destroy(clear_cache)

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

    @rpc_method(CLIENT_STUB, (Dict('round_data'),))
    def duel_round_begin(self, round_data):
        print('TTTT duel_round_begin', round_data)
        self.round_settle_timestamp = round_data.get('round_settle_timestamp', 0)
        self.settle_timestamp = round_data.get('round_settle_timestamp', 0)
        self._round_status = round_data.get('round_status')
        self.cur_battle_round = round_data.get('cur_round', 0)
        global_data.gvg_battle_data.set_settle_timestamp(self.settle_timestamp)
        self.set_mecha_button_forbid(False)

    def show_round_begin_tip(self, round_no=None):
        if not (self._battle_status == Battle.BATTLE_STATUS_PREPARE or self._round_status == battle_const.ROUND_STATUS_INTERVAL):
            return
        else:
            if round_no is None:
                round_no = self.cur_battle_round + 1
            from logic.gcommon.common_const import battle_const as bconst
            text = get_text_by_id(17945, [round_no + 1])
            tip_type = bconst.DUEL_ROUND_TIP
            message = {'i_type': tip_type,'content_txt': text,'in_anim': 'appear','out_anim': 'disappear'}
            global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
            tip_type = bconst.DUEL_ROUND_TIP2
            message = {'i_type': tip_type,'in_anim': 'appear','out_anim': 'disappear'}
            global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
            return

    def test_start(self):
        self._round_status = battle_const.ROUND_STATUS_INTERVAL
        self._round_prepare_timestamp = time_utility.get_server_time() + 14
        global_data.emgr.update_battle_timestamp.emit()
        self.show_interval_count_down()
        global_data.emgr.duel_round_interval_event.emit()

    @rpc_method(CLIENT_STUB, (Dict('interval_data'),))
    def duel_round_interval(self, interval_data):
        print('TTTT duel_round_interval', interval_data)
        self._round_prepare_timestamp = interval_data.get('round_prepare_timestamp')
        self._round_status = interval_data.get('round_status')
        if global_data.cam_lplayer:
            cur_round = interval_data.get('cur_round', 0)
            if self.get_round_record(global_data.cam_lplayer.id)[cur_round] >= 0:
                self.enter_interval_view()
        self.settle_timestamp = self._round_prepare_timestamp
        global_data.emgr.update_battle_timestamp.emit()

    def show_interval_count_down(self):
        import logic.gcommon.time_utility as t_util
        from logic.comsys.battle import BattleUtils
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_prepare_timestamp)
        if self._round_status != battle_const.ROUND_STATUS_INTERVAL:
            return
        revive_time = BattleUtils.get_prepare_left_time() + self.ui_start_diff_time
        if revive_time >= 0:
            ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
            ui.on_delay_close(revive_time, self.show_round_begin_tip)

    def enter_interval_view(self):
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.send_event('E_PLAY_VICTORY_CAMERA')
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_PLAY_VICTORY_CAMERA')
        global_data.ui_mgr.hide_all_ui_by_key('duelbattle', INTERVAL_HIDE_UI_LIST)

    def exit_interval_view(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_EXIT_FOCUS_CAMERA')
            if global_data.mecha and global_data.mecha.logic:
                global_data.mecha.logic.send_event('E_EXIT_FOCUS_CAMERA')
        global_data.ui_mgr.revert_hide_all_ui_by_key_action('duelbattle', INTERVAL_HIDE_UI_LIST)

    def get_prepare_left_time(self):
        print('TTTT get_prepare_left_time', self._round_status, self._round_prepare_timestamp, self._battle_status, self.prepare_timestamp)
        if self._round_status == battle_const.ROUND_STATUS_INTERVAL:
            return self._round_prepare_timestamp - self.ready_box_anim_time
        else:
            if self._battle_status == Battle.BATTLE_STATUS_PREPARE:
                return self.prepare_timestamp - self.ready_box_anim_time
            return 0

    def need_skip_end_exp_ui(self):
        return True

    def on_mecha_control_main_setted(self, *args):
        forbid = self._round_status != battle_const.ROUND_STATUS_PLAYING
        self.set_mecha_button_forbid(forbid)

    def set_mecha_button_forbid(self, forbid):
        now = time_utility.get_server_time()
        if self._round_status == battle_const.ROUND_STATUS_INTERVAL:
            prepare_end = now > self._round_prepare_timestamp
        elif self._battle_status == Battle.BATTLE_STATUS_PREPARE:
            prepare_end = now > self.prepare_timestamp
        else:
            prepare_end = now > self._round_prepare_timestamp or now > self.prepare_timestamp
        if prepare_end and forbid:
            return
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not ui:
            return
        for action in ('action4', 'action6'):
            ui.on_set_action_forbidden(action, forbid)

    def check_loading_register_timer(self):
        if self._battle_status == Battle.BATTLE_STATUS_PREPARE:
            if BattleUtils.get_prepare_left_time() + self.ui_start_diff_time > LOADING_CLOSE_TIME:
                self.register_timer()

    def register_timer(self):
        from logic.comsys.battle import BattleUtils
        from common.utils.timer import CLOCK
        self.unregister_timer()
        close_time = BattleUtils.get_prepare_left_time() + self.ui_start_diff_time - LOADING_CLOSE_TIME
        if close_time > 0:
            self.loading_timer_id = global_data.game_mgr.get_logic_timer().register(func=self.loading_close_func, interval=0.3, times=-1, mode=CLOCK)

    def loading_close_func(self):
        if self.is_can_close_loading():
            self.unregister_timer()
            global_data.emgr.custom_loading_close_event.emit()

    def unregister_timer(self):
        if self.loading_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self.loading_timer_id)
        self.loading_timer_id = None
        return

    def is_can_close_loading(self):
        if self._battle_status == Battle.BATTLE_STATUS_PREPARE:
            if BattleUtils.get_prepare_left_time() + self.ui_start_diff_time - LOADING_CLOSE_TIME <= 0.05:
                return True
            else:
                return False

        else:
            return True