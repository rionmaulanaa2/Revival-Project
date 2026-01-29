# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ZombieFFABattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Float, Bool, Uuid, Dict, List, Str
from logic.gcommon.common_const import battle_const
from logic.entities.Battle import Battle
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gcommon import time_utility as tutils
import world

class ZombieFFABattle(Battle):

    def __init__(self, entity_id):
        super(ZombieFFABattle, self).__init__(entity_id)

    def init_from_dict(self, bdict):
        self.battle_bdict = bdict
        self.sync_battle_time()
        self.area_id = bdict.get('area_id')
        self.map_id = bdict.get('map_id')
        self.choose_mecha_finish = bdict.get('choose_mecha_finished', False)
        self.mecha_usage_dict = bdict.get('mecha_usage_dict', {})
        self.confirmed_player_list = bdict.get('confirmed_player_list', [])
        self.choose_mecha_end_ts = bdict.get('choose_mecha_end_ts', 0)
        self.refresh_mecha_times = bdict.get('refresh_mecha_times', 0)
        self.refresh_mecha_cost = bdict.get('refresh_mecha_cost', 0)
        self.choose_mecha_player_names = bdict.get('choose_mecha_player_names', {})
        self.is_mutated = bdict.get('is_mutated', False)
        self.enable_mutation = bdict.get('enable_mutation', False)
        self.start_suicide_result((bdict.get('suicide_timestamp', 0),))
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
        global_data.ui_mgr.close_ui('ZombieFFAChooseMechaUI')
        super(ZombieFFABattle, self).init_from_dict(self.battle_bdict)

    def load_choose_mecha(self):
        import math3d
        from logic.gcommon.common_const import scene_const
        from logic.gutils.CameraHelper import get_adaptive_camera_fov
        from logic.gutils import lobby_model_display_utils
        from logic.client.const import lobby_model_display_const
        scene = global_data.game_mgr.scene
        scene_type = scene.get_type() if scene else None
        if scene_type == scene_const.SCENE_ZOMBIEFFA_CHOOSE_MECHA:
            global_data.emgr.enter_zombieffa_choose_mecha.emit()
            return
        else:

            def enable_mirror():
                scene = world.get_active_scene()
                scene_type = scene.get_type() if scene else None
                global_data.emgr.check_cur_scene_mirror_model_event.emit((scene, scene_type))
                return

            def switch_scene_cb(_scene_type):
                enable_mirror()
                global_data.emgr.enter_zombieffa_choose_mecha.emit()
                self.call_soul_method('on_client_choose_mecha_load_finish', ())

            if scene_type is None or scene_type == scene_const.SCENE_MAIN:

                def _scene_cb():
                    scene = global_data.game_mgr.scene
                    enable_mirror()
                    scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.ZOMBIEFFA_CHOOSE_MECHA_SCENE)
                    cam_hanger = scene.get_preset_camera(scene_data.get('cam_key'))
                    cam = scene.active_camera
                    cam.rotation_matrix = math3d.rotation_to_matrix(math3d.matrix_to_rotation(cam_hanger.rotation))
                    cam.world_position = cam_hanger.translation
                    fov = scene_data.get('fov', 55)
                    fov, aspect = get_adaptive_camera_fov(fov)
                    cam.fov = fov
                    cam.aspect = aspect
                    global_data.emgr.camera_inited_event.emit()
                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_ZOMBIEFFA_CHOOSE_MECHA, lobby_model_display_const.ZOMBIEFFA_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_FFA_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
            else:
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_ZOMBIEFFA_CHOOSE_MECHA, lobby_model_display_const.ZOMBIEFFA_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)
            return

    def boarding_movie_data(self):
        return None

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

    def start_suicide(self):
        self.call_soul_method('start_suicide', ())

    def get_suicide_timestamp(self):
        return self.suicide_timestamp

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(ZombieFFABattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.zombieffa_battle_data.set_settle_timestamp(settle_timestamp)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_battle_data(self, settle_timestamp):
        self.update_settle_timestamp((settle_timestamp,))

    @rpc_method(CLIENT_STUB, (Float('ratio'),))
    def on_weaken_buff(self, ratio):
        message = {'i_type': battle_const.ZOMBIEFFA_ACE_TIME,'content_txt': 19789}
        message_type = battle_const.MAIN_NODE_COMMON_INFO
        push_to_head = True
        global_data.emgr.show_battle_main_message.emit(message, message_type, push_to_head)

    @rpc_method(CLIENT_STUB, (List('group_rank_data'),))
    def update_group_points(self, group_rank_data):
        global_data.zombieffa_battle_data.set_group_rank_data(group_rank_data)

    @rpc_method(CLIENT_STUB, (List('details_data'),))
    def reply_rank_data(self, details_data):
        global_data.zombieffa_battle_data.set_score_details_data(details_data)

    @rpc_method(CLIENT_STUB, (Int('group_id'), Dict('soul_pos')))
    def notify_top_group_info(self, group_id, soul_data):
        global_data.zombieffa_battle_data.notify_top_group_info(group_id, soul_data)

    def request_rank_data(self):
        self.call_soul_method('request_rank_data', ())

    @rpc_method(CLIENT_STUB, (List('prompt_id_list'), Str('eid'), Str('name'), Dict('short_kill_info')))
    def on_kill_prompt(self, prompt_id_list, eid, name, short_kill_info):
        from logic.gutils import mecha_skin_utils
        f_default_fashion = lambda mecha_id: mecha_skin_utils.get_original_skin_lst(mecha_id)[0]
        killer_mecha_id = short_kill_info.get('killer_mecha_id')
        dead_mecha_id = short_kill_info.get('mecha_id')
        killer_mecha_fashion = short_kill_info.get('killer_mecha_fashion', {}).get(FASHION_POS_SUIT) or f_default_fashion(killer_mecha_id)
        dead_mecha_fashion = short_kill_info.get('mecha_fashion', {}).get(FASHION_POS_SUIT) or f_default_fashion(dead_mecha_id)
        mecha_entity = EntityManager.getentity(short_kill_info.get('mecha_eid'))
        cam_lctarget = global_data.cam_lctarget
        for prompt_id in prompt_id_list:
            if cam_lctarget and mecha_entity and mecha_entity.logic:
                if cam_lctarget.ev_g_is_campmate(mecha_entity.logic.ev_g_camp_id()):
                    frd_mecha_id = dead_mecha_fashion
                    eny_mecha_id = killer_mecha_fashion
                    frd_is_killer = False
                else:
                    frd_mecha_id = killer_mecha_fashion
                    eny_mecha_id = dead_mecha_fashion
                    frd_is_killer = True
                if frd_mecha_id and eny_mecha_id:
                    msg = battle_utils.get_kill_prompt_msg(prompt_id, frd_mecha_id, eny_mecha_id, frd_is_killer, name)
                    global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Dict('killer_info'), Float('revive_time')))
    def on_mecha_destroy(self, killer_info, revive_time):
        global_data.emgr.zombieffa_mecha_destroyed.emit(killer_info, revive_time)

    def start_combat(self, mutation=False):
        self.call_soul_method('start_combat', (mutation,))

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('DeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (List('camp_status'),))
    def update_camp_status(self, camp_status):
        if global_data.zombieffa_battle_data:
            global_data.zombieffa_battle_data.update_camp_status(camp_status)

    def request_change_mecha(self):
        self.call_soul_method('request_change_mecha', ())

    def confirm_mecha_usage(self):
        if not self.choose_mecha_end_ts:
            return
        self.call_soul_method('confirm_mecha_usage', ())

    @rpc_method(CLIENT_STUB, (Float('end_ts'),))
    def on_zombieffa_choose_mecha_start(self, end_ts):
        global_data.emgr.zombieffa_choose_mecha_start.emit(end_ts)

    @rpc_method(CLIENT_STUB, (Bool('success'), Int('mecha_id')))
    def request_change_mecha_result(self, success, mecha_id):
        if not success:
            return
        eid = global_data.player.id
        self.mecha_usage_dict[eid] = mecha_id
        self.refresh_mecha_times += 1
        global_data.emgr.zombieffa_change_mecha_result.emit(success, mecha_id)

    @rpc_method(CLIENT_STUB, (Uuid('eid'), Int('mecha_id')))
    def on_player_refresh_mecha(self, eid, mecha_id):
        self.mecha_usage_dict[eid] = mecha_id
        global_data.emgr.zombieffa_on_player_mecha_change.emit(eid, mecha_id)

    @rpc_method(CLIENT_STUB, (Int('total_cost'),))
    def on_cost_refresh_mecha(self, total_cost):
        self.refresh_mecha_cost = total_cost

    @rpc_method(CLIENT_STUB, (Uuid('eid'),))
    def on_player_confirm_mecha_usage(self, eid):
        self.confirmed_player_list.append(eid)
        global_data.emgr.zombieffa_on_player_confirmed.emit(eid)

    @rpc_method(CLIENT_STUB, ())
    def on_zombieffa_choose_mecha_finish(self):
        self.choose_mecha_finish = True
        global_data.emgr.zombieffa_choose_mecha_finish.emit()

    @rpc_method(CLIENT_STUB, (Int('mecha_id'),))
    def on_mecha_extinction(self, mecha_id):
        mecha_name = item_utils.get_mecha_name_by_id(mecha_id)
        mecha_default_skin_no = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id=None)
        message = {'i_type': battle_const.ZOMBIEFFA_MECHA_EXTINCTION,'set_attr_dict': [
                           {'node_name': 'lab_1',
                              'func_name': 'SetString',
                              'args': (
                                     get_text_by_id(19790, args={'name': mecha_name}),)
                              },
                           {'node_name': 'img_1',
                              'func_name': 'SetDisplayFrameByPath',
                              'args': (
                                     '', 'gui/ui_res_2/item/mecha_skin/{}.png'.format(mecha_default_skin_no))
                              }]
           }
        global_data.emgr.show_battle_main_message.emit(message, battle_const.MAIN_NODE_COMMON_INFO)
        return

    @rpc_method(CLIENT_STUB, ())
    def on_enable_mutation(self):
        self.enable_mutation = True

    @rpc_method(CLIENT_STUB, (Int('mecha_id'),))
    def on_mecha_mutation(self, mecha_id):
        self.is_mutated = True

    @rpc_method(CLIENT_STUB, (Int('spawn_id'), Int('faction_id'), Float('rebirth_ts')))
    def update_spawn_rebirth(self, spawn_id, faction_id, rebirth_ts):
        global_data.zombieffa_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])