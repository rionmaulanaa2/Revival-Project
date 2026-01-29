# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/CloneBattle.py
from __future__ import absolute_import
import six
from logic.gcommon import time_utility as tutil
from logic.entities.DeathBattle import DeathBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Uuid, Dict, Float, Str
import math3d
from logic.gcommon.common_const import scene_const
from logic.gutils.CameraHelper import get_adaptive_camera_fov
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon import time_utility

class CloneBattle(DeathBattle):

    def __init__(self, entityid):
        super(CloneBattle, self).__init__(entityid)
        self.mecha_vote_callback = None
        self.eid_2_group_id = {}
        self.my_group = None
        self.waiting = False
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self.update_observed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, bdict):
        self.sync_battle_time(bdict)
        self.battle_bdict = bdict
        self.map_id = bdict.get('map_id')
        self.area_id = bdict.get('area_id')
        self.group_data = bdict.get('group_data', {})
        self.group_confirmed_list = bdict.get('group_confirmed_list', [])
        self.group_mecha_vote_info = bdict.get('group_mecha_vote_info', {})
        self.mecha_use_dict = bdict.get('mecha_use_dict', {})
        self.group_mecha_fashion = bdict.get('group_mecha_fashion', {})
        self.group_chat_history = bdict.get('group_chat_history', [])
        self.waiting_group = bdict.get('waiting_group')
        self.mecha_vote_end_ts = bdict.get('mecha_vote_end_ts', 0)
        self.mecha_vote_finished = bdict.get('mecha_vote_finished', False)
        self.mecha_vote_callback = self._get_mecha_vote_callback()
        self.init_eid_2_group_id()
        if global_data.player:
            if global_data.player.is_in_global_spectate():
                self.init_eid_2_index(global_data.player.get_global_spectate_player_id())
            else:
                self.init_eid_2_index()
        if self.my_group == self.waiting_group:
            self.waiting = True
        if self.mecha_vote_finished:
            self.mecha_vote_callback()
        else:
            self.load_vote_mecha()

    def sync_battle_time(self, bdict):
        battle_srv_time = bdict.get('battle_srv_time', None)
        if battle_srv_time and time_utility.TYPE_BATTLE not in time_utility.g_success_flag:
            time_utility.on_sync_time(time_utility.TYPE_BATTLE, battle_srv_time)
        return

    def load_vote_mecha(self):
        scene = global_data.game_mgr.scene
        scene_type = scene.get_type() if scene else None
        if scene_type == scene_const.SCENE_CLONE_VOTE_MECHA:
            global_data.emgr.enter_clone_vote_mecha.emit()
            return
        else:
            if not scene_type or scene_type == scene_const.SCENE_MAIN:

                def _scene_cb():
                    scene = global_data.game_mgr.scene
                    scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.CLONE_VOTE_MECHA_SCENE)
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
                        if global_data.battle:
                            global_data.emgr.enter_clone_vote_mecha.emit()

                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_CLONE_VOTE_MECHA, lobby_model_display_const.CLONE_VOTE_MECHA_SCENE, finish_callback=_switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_MECHA_DEATH_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
            else:

                def _switch_scene_cb(*args):
                    if global_data.battle:
                        global_data.emgr.enter_clone_vote_mecha.emit()

                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_CLONE_VOTE_MECHA, lobby_model_display_const.CLONE_VOTE_MECHA_SCENE, finish_callback=_switch_scene_cb)
            return

    def _get_mecha_vote_callback(self):

        def _mecha_vote_callback():
            global_data.ui_mgr.close_ui('CloneVoteMecha')
            global_data.ui_mgr.close_ui('CloneMechaSkillDetail')
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            global_data.emgr.reset_rotate_model_display.emit()
            super(CloneBattle, self).init_from_dict(self.battle_bdict)

        return _mecha_vote_callback

    def boarding_movie_data(self):
        return None

    def destroy(self, clear_cache=True):
        self.process_event(False)
        super(CloneBattle, self).destroy(clear_cache)

    def update_observed(self, ltarget):
        if not ltarget:
            return
        self.init_eid_2_index(target_id=ltarget.id)

    def init_eid_2_group_id(self):
        self.eid_2_group_id = {}
        for group_id, data in six.iteritems(self.group_data):
            for eid in six.iterkeys(data):
                self.eid_2_group_id[eid] = group_id

    def init_eid_2_index(self, target_id=None):
        if not target_id:
            target_id = global_data.player.id
        self.my_group = self.eid_2_group_id.get(target_id)
        for group, data in six.iteritems(self.group_data):
            first_pos_eid = None
            for index, eid in enumerate(data):
                data[eid]['index'] = index
                if index == 0 and eid != target_id:
                    first_pos_eid = eid
                if eid == target_id and first_pos_eid:
                    data[eid]['index'] = 0
                    data[first_pos_eid]['index'] = index
                    first_pos_eid = eid

        return

    def request_vote_mecha(self, mecha_id):
        self.group_mecha_vote_info[global_data.player.id] = (
         mecha_id, {})
        self.call_soul_method('request_vote_mecha', (mecha_id,))

    def confirm_vote_mecha(self):
        self.group_confirmed_list.append(global_data.player.id)
        self.call_soul_method('confirm_vote_mecha', ())

    def cancel_confirm_vote_mecha(self):
        if global_data.player.id in self.group_confirmed_list:
            self.group_confirmed_list.remove(global_data.player.id)
        self.call_soul_method('cancel_confirm_vote_mecha', ())

    def send_message(self, message):
        self.call_soul_method('send_message', (message,))

    def clone_enter_battle(self):
        if self.mecha_vote_callback:
            self.mecha_vote_callback()

    def get_my_group_use_mecha(self):
        if self.mecha_use_dict:
            return self.mecha_use_dict.get(self.my_group)
        else:
            return None

    @rpc_method(CLIENT_STUB, (Int('end_ts'),))
    def on_start_vote_mecha(self, end_ts):
        self.mecha_vote_end_ts = end_ts
        global_data.emgr.start_clone_vote_mecha.emit()

    @rpc_method(CLIENT_STUB, (Uuid('eid'), Int('mecha_id'), Dict('mecha_fashion')))
    def on_vote_mecha(self, eid, mecha_id, mecha_fashion):
        self.group_mecha_vote_info[eid] = (
         mecha_id, mecha_fashion)
        global_data.emgr.refresh_vote_mecha.emit(eid, mecha_id, mecha_fashion)

    @rpc_method(CLIENT_STUB, (Uuid('eid'),))
    def on_confirm_vote_mecha(self, eid):
        self.group_confirmed_list.append(eid)
        global_data.emgr.refresh_confirm_vote_mecha.emit(eid)

    @rpc_method(CLIENT_STUB, (Uuid('eid'),))
    def on_cancel_confirm_vote_mecha(self, eid):
        if eid in self.group_confirmed_list:
            self.group_confirmed_list.remove(eid)
        global_data.emgr.refresh_cancel_confirm_vote_mecha.emit(eid)

    @rpc_method(CLIENT_STUB, ())
    def on_wait_vote_mecha(self):
        self.waiting = True
        global_data.emgr.clone_wait_vote_mecha.emit()

    @rpc_method(CLIENT_STUB, (Dict('group_mecha_use'), Dict('group_mecha_fashion')))
    def on_vote_mecha_finished(self, group_mecha_use, group_mecha_fashion):
        self.mecha_vote_finished = True
        self.mecha_use_dict.update(group_mecha_use)
        self.group_mecha_fashion.update(group_mecha_fashion)
        global_data.emgr.clone_vote_mecha_finished.emit()

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Dict('killer_info'), Float('mecha_revice_ts')))
    def on_mecha_destroy(self, soul_id, killer_info, mecha_revice_ts):
        global_data.emgr.clone_mecha_destroyed.emit(soul_id, killer_info, mecha_revice_ts)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(CloneBattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Uuid('eid'), Str('message')))
    def receive_teammate_message(self, eid, message):
        self.group_chat_history.append((eid, message))
        global_data.emgr.receive_teammate_message.emit(eid, message)