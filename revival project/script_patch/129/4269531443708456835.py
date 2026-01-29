# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/MechaDeathBattle.py
from __future__ import absolute_import
import six_ex
from logic.entities.DeathBattle import DeathBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Uuid, Dict, List, Float, Str, Bool
import math3d
from logic.gcommon.common_const import scene_const
from logic.gutils.CameraHelper import get_adaptive_camera_fov
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon import time_utility
import world

class MechaDeathBattle(DeathBattle):

    def __init__(self, entityid):
        super(MechaDeathBattle, self).__init__(entityid)
        self.process_event(True)

    def destroy(self, clear_cache=True):
        self.process_event(False)
        super(MechaDeathBattle, self).destroy(clear_cache)

    def init_from_dict(self, bdict):
        self.sync_battle_time(bdict)
        self.init_parameters(bdict)

    def init_parameters(self, bdict):
        self.battle_bdict = bdict
        self.map_id = bdict.get('map_id')
        self.area_id = bdict.get('area_id')
        self.brief_group_data = bdict.get('brief_group_data', {})
        self.chosen_mecha_dict = bdict.get('chosen_mecha_dict', {})
        self.chosen_fashion_dict = bdict.get('chosen_fashion_dict', {})
        self.confirmed_soul_list = bdict.get('confirmed_soul_list', [])
        self.chosen_mecha_list = six_ex.values(self.chosen_mecha_dict)
        self.choose_mecha_end_timpstamp = bdict.get('choose_mecha_end_timestamp', 0)
        self.is_choose_finished = bdict.get('is_choose_finished', False)
        self.rechoose_mecha_end_timestamp = bdict.get('rechoose_mecha_end_timestamp', 0)
        self.rechoose_mecha_flag = bdict.get('rechoose_mecha_flag', False)
        self.rechoose_mecha_enable_timestamp = -1
        self.group_chat_history = bdict.get('group_chat_history', [])
        self._avatar_mecha_dict = bdict.get('mecha_dict', {})
        self._settle_point = bdict.get('settle_point', 50)
        self.settle_timestamp = 0
        if self.is_choose_finished:
            self.mecha_death_enter_battle()
        else:
            self.load_choose_mecha_scene()

    def get_settle_point(self):
        return self._settle_point

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self.update_observed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_observed(self, ltarget):
        if not ltarget:
            return

    def boarding_movie_data(self):
        return None

    def sync_battle_time(self, bdict):
        battle_srv_time = bdict.get('battle_srv_time', None)
        if battle_srv_time and time_utility.TYPE_BATTLE not in time_utility.g_success_flag:
            time_utility.on_sync_time(time_utility.TYPE_BATTLE, battle_srv_time)
        return

    def load_choose_mecha_scene(self):
        scene = global_data.game_mgr.scene
        scene_type = scene.get_type() if scene else None
        if scene_type == scene_const.SCENE_MECHA_DEATH_CHOOSE_MECHA:
            global_data.emgr.enter_mecha_death_choose_mecha.emit()
            return
        else:
            if scene_type == scene_const.SCENE_LOBBY:
                part_mecha_display = scene.get_com('PartMechaDisplay')
                if part_mecha_display:
                    part_mecha_display.hide_all_teammate_tip_ui()

            def enable_mirror():
                scene = world.get_active_scene()
                scene_type = scene.get_type() if scene else None
                global_data.emgr.check_cur_scene_mirror_model_event.emit((scene, scene_type))
                return

            def switch_scene_cb(_scene_type):
                enable_mirror()
                global_data.emgr.enter_mecha_death_choose_mecha.emit()
                self.ask_is_choose_finished()

            if scene_type is None or scene_type == scene_const.SCENE_MAIN:

                def _scene_cb():
                    scene = global_data.game_mgr.scene
                    enable_mirror()
                    scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE)
                    cam_hanger = scene.get_preset_camera(scene_data.get('cam_key'))
                    cam = scene.active_camera
                    cam.rotation_matrix = math3d.rotation_to_matrix(math3d.matrix_to_rotation(cam_hanger.rotation))
                    cam.world_position = cam_hanger.translation
                    fov = scene_data.get('fov', 55)
                    fov, aspect = get_adaptive_camera_fov(fov)
                    cam.fov = fov
                    cam.aspect = aspect
                    global_data.emgr.camera_inited_event.emit()
                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_MECHA_DEATH_CHOOSE_MECHA, lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_MECHA_DEATH_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
            else:
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_MECHA_DEATH_CHOOSE_MECHA, lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)
            return

    def mecha_death_enter_battle(self):
        global_data.ui_mgr.close_ui('MechaDeathChooseMechaUI')
        global_data.ui_mgr.close_ui('MechaDeathSkillDetail')
        super(MechaDeathBattle, self).init_from_dict(self.battle_bdict)

    def init_rechoose_mecha_ui(self):
        now = time_utility.get_server_time()
        if now < self.rechoose_mecha_end_timestamp and not self.rechoose_mecha_flag:
            from logic.comsys.battle.MechaDeath.MechaDeathRechooseMechaUI import MechaDeathRechooseMechaUI
            MechaDeathRechooseMechaUI(None, global_data.cam_lplayer)
        return

    def try_choose_mecha(self, mecha_id, force=False):
        self.call_soul_method('try_choose_mecha', (mecha_id, force))

    def confirm_choose_mecha(self):
        self.call_soul_method('confirm_choose_mecha', ())

    def try_rechoose_mecha(self):
        self.call_soul_method('try_rechoose_mecha', ())

    def do_rechoose_mecha(self, mecha_id):
        self.call_soul_method('do_rechoose_mecha', (mecha_id,))

    def give_up_rechoose_mecha(self):
        self.rechoose_mecha_end_timestamp = 0
        self.call_soul_method('give_up_rechoose_mecha', ())

    def send_message(self, message):
        self.call_soul_method('send_message', (message,))

    def ask_is_choose_finished(self):
        self.call_soul_method('ask_is_choose_finished', ())

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (Int('end_timestamp'),))
    def on_start_choose_mecha(self, end_timestamp):
        self.choose_mecha_end_timpstamp = end_timestamp

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('mecha_id'), Dict('fashion_dict'), List('chosen_mecha_list')))
    def choose_mecha_result(self, soul_id, mecha_id, fashion_dict, chosen_mecha_list):
        global_data.emgr.refresh_mecha_death_chosen_mecha.emit(soul_id, mecha_id, fashion_dict, chosen_mecha_list)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), List('confirmed_soul_list')))
    def confirm_mecha_result(self, soul_id, confirmed_soul_list):
        self.confirmed_soul_list = confirmed_soul_list
        global_data.emgr.refresh_mecha_death_confirm_mecha.emit(soul_id, self.confirmed_soul_list)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Str('message')))
    def receive_teammate_message(self, soul_id, message):
        global_data.emgr.receive_teammate_message.emit(soul_id, message)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(MechaDeathBattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Bool('ret'),))
    def on_choose_mecha_finished(self, ret):
        self.is_choose_finished = ret
        if ret:
            global_data.emgr.mecha_death_choose_mecha_finished.emit()

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Dict('killer_info'), Float('mecha_revice_ts')))
    def on_mecha_destroy(self, soul_id, killer_info, mecha_revice_ts):
        global_data.emgr.mecha_death_mecha_destroyed.emit(soul_id, killer_info, mecha_revice_ts)

    @rpc_method(CLIENT_STUB, (Bool('result'), Int('rechoose_mecha_end_timestamp')))
    def rechoose_mecha_result(self, result, rechoose_mecha_end_timestamp):
        if result:
            from logic.comsys.battle.MechaDeath.MechaDeathRechooseMechaUI import MechaDeathRechooseMechaUI
            self.rechoose_mecha_end_timestamp = rechoose_mecha_end_timestamp
            global_data.ui_mgr.hide_ui('MechaDeathPlayBackUI')
            if global_data.ui_mgr.get_ui('MechaDeathRechooseMechaUI'):
                return
            MechaDeathRechooseMechaUI(None, global_data.cam_lplayer)
            global_data.ui_mgr.hide_ui('MechaDeathPlayBackUI')
        return

    @rpc_method(CLIENT_STUB, ())
    def rechoose_mecha_succ(self):
        self.rechoose_mecha_flag = True
        self.rechoose_mecha_end_timestamp = 0
        global_data.ui_mgr.close_ui('MechaDeathRechooseMechaUI')
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (Int('spawn_id'), Int('faction_id'), Float('rebirth_ts')))
    def update_spawn_rebirth(self, spawn_id, faction_id, rebirth_ts):
        global_data.death_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])