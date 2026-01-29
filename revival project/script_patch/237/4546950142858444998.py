# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/FFABattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.gcommon.common_const import battle_const
from logic.entities.Battle import Battle
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutils
import world

class FFABattle(Battle):

    def __init__(self, entityid):
        super(FFABattle, self).__init__(entityid)

    def init_from_dict(self, bdict):
        self.battle_bdict = bdict
        self.sync_battle_time()
        self.area_id = bdict.get('area_id')
        self.map_id = bdict.get('map_id')
        self.choose_mecha_end_ts = bdict.get('choose_mecha_end_ts', 0)
        self.choose_mecha_finish = bdict.get('choose_mecha_finish', False)
        self.chosen_mecha_id = bdict.get('chosen_mecha_id')
        self.choose_mecha_confirm = bdict.get('choose_mecha_confirm', False)
        self.choose_mecha_confirmed_cnt = bdict.get('confirmed_cnt', 0)
        self.choose_mecha_player_cnt = bdict.get('player_cnt', 0)
        self.start_suicide_result((bdict.get('suicide_timestamp', 0),))
        self.rechoose_mecha_end_timestamp = bdict.get('rechoose_mecha_end_timestamp', 0)
        self.rechoose_mecha_flag = bdict.get('rechoose_mecha_flag', False)
        self.rechoose_mecha_enable_timestamp = 0
        self._avatar_mecha_dict = bdict.get('mecha_dict', {})
        if self.choose_mecha_finish:
            self.enter_battle()
        else:
            self.load_choose_mecha()

    def sync_battle_time(self):
        battle_srv_time = self.battle_bdict.get('battle_srv_time', None)
        if battle_srv_time and tutils.TYPE_BATTLE not in tutils.g_success_flag:
            tutils.on_sync_time(tutils.TYPE_BATTLE, battle_srv_time)
        return

    def enter_battle(self):
        global_data.ui_mgr.close_ui('FFAChooseMechaUI')
        super(FFABattle, self).init_from_dict(self.battle_bdict)

    def load_choose_mecha(self):
        import math3d
        from logic.gcommon.common_const import scene_const
        from logic.gutils.CameraHelper import get_adaptive_camera_fov
        from logic.gutils import lobby_model_display_utils
        from logic.client.const import lobby_model_display_const
        scene = global_data.game_mgr.scene
        scene_type = scene.get_type() if scene else None
        if scene_type == scene_const.SCENE_FFA_CHOOSE_MECHA:
            global_data.emgr.enter_ffa_choose_mecha.emit()
            return
        else:

            def enable_mirror():
                scene = world.get_active_scene()
                scene_type = scene.get_type() if scene else None
                global_data.emgr.check_cur_scene_mirror_model_event.emit((scene, scene_type))
                return

            def switch_scene_cb(_scene_type):
                enable_mirror()
                global_data.emgr.enter_ffa_choose_mecha.emit()
                self.call_soul_method('on_client_choose_mecha_load_finish', ())

            if scene_type is None or scene_type == scene_const.SCENE_MAIN:

                def _scene_cb():
                    scene = global_data.game_mgr.scene
                    enable_mirror()
                    scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.FFA_CHOOSE_MECHA_SCENE)
                    cam_hanger = scene.get_preset_camera(scene_data.get('cam_key'))
                    cam = scene.active_camera
                    cam.rotation_matrix = math3d.rotation_to_matrix(math3d.matrix_to_rotation(cam_hanger.rotation))
                    cam.world_position = cam_hanger.translation
                    fov = scene_data.get('fov', 55)
                    fov, aspect = get_adaptive_camera_fov(fov)
                    cam.fov = fov
                    cam.aspect = aspect
                    global_data.emgr.camera_inited_event.emit()
                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_FFA_CHOOSE_MECHA, lobby_model_display_const.FFA_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_FFA_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
            else:
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_FFA_CHOOSE_MECHA, lobby_model_display_const.FFA_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)
            return

    def boarding_movie_data(self):
        return None

    def init_rechoose_mecha_ui(self):
        now = tutils.get_server_time()
        if now < self.rechoose_mecha_end_timestamp and not self.rechoose_mecha_flag:
            from logic.comsys.battle.MechaDeath.MechaDeathRechooseMechaUI import MechaDeathRechooseMechaUI
            MechaDeathRechooseMechaUI(None, global_data.cam_lplayer)
        return

    @rpc_method(CLIENT_STUB, (List('group_rank_data'),))
    def update_group_points(self, group_rank_data):
        global_data.ffa_battle_data.set_group_score_data(group_rank_data)

    @rpc_method(CLIENT_STUB, (List('rank_data'),))
    def reply_rank_data(self, rank_data):
        global_data.ffa_battle_data.set_score_details_data(rank_data)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.ffa_battle_data.set_settle_timestamp(settle_timestamp)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_battle_data(self, settle_timestamp):
        self.update_settle_timestamp((settle_timestamp,))

    @rpc_method(CLIENT_STUB, (Int('group_id'), Dict('soul_data')))
    def notify_top_group_info(self, group_id, soul_data):
        global_data.ffa_battle_data.notify_top_group_info(group_id, soul_data)

    @rpc_method(CLIENT_STUB, (Int('install_index'),))
    def module_auto_install(self, install_index):
        self.on_module_auto_install(install_index)

    def on_module_auto_install(self, install_index):
        info_dict = {1: (
             'gui/ui_res_2/item/9912.png', '#SG', get_text_by_id(17028), 17017),
           2: (
             'gui/ui_res_2/item/9913.png', '#SB', get_text_by_id(17014), 17017),
           3: (
             'gui/ui_res_2/item/9908.png', '#SP', get_text_by_id(17015), 17017),
           4: (
             'gui/ui_res_2/item/9911.png', '#SO', get_text_by_id(17016), 17018)
           }
        if install_index not in info_dict:
            return
        sprite_path, color_str, name, content_id = info_dict.get(install_index)
        msg = {'i_type': battle_const.TDM_ABOUT_TO_GET_MODULE_UPGRADE,
           'icon_path': sprite_path,
           'content_txt': get_text_by_id(content_id, {'color': color_str,'module_name': name})
           }
        if msg and global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(FFABattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        super(FFABattle, self).fight_stage((stage_dict,))
        self.rechoose_mecha_enable_timestamp = stage_dict.get('rechoose_mehca_enable_timestamp', 0)

    @rpc_method(CLIENT_STUB, (Float('final_prate'),))
    def final_stage(self, final_prate):
        self.is_in_ace_state = True
        message = [{'i_type': battle_const.TDM_THREE_TIMES_POINT,'set_num_func': 'set_show_percent_num','show_num': int(max(0, final_prate - 1) * 100)}, {'i_type': battle_const.SECOND_ACE_TIME}]
        message_type = [
         battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)

    @rpc_method(CLIENT_STUB, (Dict('killer_info'), Float('revive_time')))
    def on_mecha_destroy(self, killer_info, revive_time):
        global_data.emgr.ffa_mecha_destroyed.emit(killer_info, revive_time)

    def start_combat(self):
        self.call_soul_method('start_combat', ())

    def start_suicide(self):
        self.call_soul_method('start_suicide', ())

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()

    def get_suicide_timestamp(self):
        return self.suicide_timestamp

    @rpc_method(CLIENT_STUB, (Int('end_ts'),))
    def on_ffa_choose_mecha_start(self, end_ts):
        self.choose_mecha_end_ts = end_ts
        global_data.emgr.start_ffa_choose_mecha.emit()

    def request_choose_mecha(self, mecha_id):
        self.chosen_mecha_id = mecha_id
        self.call_soul_method('request_choose_mecha', (mecha_id,))

    def confirm_choose_mecha(self):
        self.choose_mecha_confirm = True
        self.call_soul_method('confirm_choose_mecha', ())

    @rpc_method(CLIENT_STUB, ())
    def on_choose_mecha_success(self):
        pass

    @rpc_method(CLIENT_STUB, (Int('confirm_cnt'),))
    def on_update_confirmed_cnt(self, confirmed_cnt):
        self.choose_mecha_confirmed_cnt = confirmed_cnt
        global_data.emgr.ffa_confirmed_cnt_update.emit()

    @rpc_method(CLIENT_STUB, ())
    def on_ffa_choose_mecha_finish(self):
        self.choose_mecha_finish = True
        global_data.emgr.ffa_choose_mecha_finish.emit()

    def try_rechoose_mecha(self):
        self.call_soul_method('try_rechoose_mecha', ())

    def do_rechoose_mecha(self, mecha_id):
        self.call_soul_method('do_rechoose_mecha', (mecha_id,))

    def give_up_rechoose_mecha(self):
        self.rechoose_mecha_end_timestamp = 0
        self.call_soul_method('give_up_rechoose_mecha', ())

    @rpc_method(CLIENT_STUB, (Bool('result'), Int('rechoose_mecha_end_timestamp')))
    def rechoose_mecha_result(self, result, rechoose_mecha_end_timestamp):
        if result:
            self.rechoose_mecha_end_timestamp = rechoose_mecha_end_timestamp
            global_data.ui_mgr.hide_ui('MechaDeathPlayBackUI')
            if global_data.ui_mgr.get_ui('MechaDeathRechooseMechaUI'):
                return
            from logic.comsys.battle.MechaDeath.MechaDeathRechooseMechaUI import MechaDeathRechooseMechaUI
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
        global_data.ffa_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])