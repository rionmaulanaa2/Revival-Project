# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/SurvivalBattlePrepare.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gcommon.common_utils import parachute_utils
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from logic.entities.Battle import Battle
from logic.gcommon.common_const import battle_const
import logic.vscene.parts.battleprepare.BattlePrepare as BattlePrepare
from logic.vscene.parts.battleprepare.BestSkinShow import BwBestSkinShow, KongdaoBestSkinShow, SKIN_TYPE_ROLE, SKIN_TYPE_MECHA
from common.utils.timer import RELEASE, CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.const import SKELETON_LOD_DIST
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_const import ui_operation_const as uoc
from .LaunchBoostAppearance import LaunchBoostAppearance, INTRP_ENTER, INTRP_EXIT
from .launch_lobby_sfx_info import SFX_INFO_LIST
from logic.gutils.screen_effect_utils import create_screen_effect_directly
import device_compatibility
import exception_hook
import math3d
import math
import game3d
import world
import time
from common.platform.dctool import interface
DEFAULT_POS = math3d.vector(0, 8000, 0)
RES_LOAD_PRIORITY = game3d.ASYNC_HIGH
PREPARE_ZMIN = device_compatibility.IS_DX or 10 if 1 else 7
PREPARE_ZMIN_FLYING = device_compatibility.IS_DX or 15 if 1 else 9
PREPARE_ZMAX = 150000

def update_view_range_3(scn):
    scn.set_view_range(3, 100000)


class SurvivalBattlePrepare(BattlePrepare.BattlePrepareBase):

    def __init__(self, parent):
        super(SurvivalBattlePrepare, self).__init__(parent)
        self.range_mgr = None
        self.init_mgr()
        self.is_in_prepare_status = False
        self.scene_loading_tasks = []
        self.scene_model_list = []
        self.scene_model_size = 0
        self.launch_boost_appearance = None
        self.launch_boost_appearance_destroyed = False
        self.launch_boost_appearance_destroyed_reason = ''
        self.log_posted = False
        self.is_first_valid_update = False
        self.camera_ctrl = None
        self._update_timer = None
        self.res_prepared = False
        self.is_3d_map_camera = False
        self.trk_start_time = 0
        self.model_move_timer_list = []
        self.effect_id_list = []
        self.ready_is_first = True
        self.had_preload_cockpit = False
        self.init_data()
        self._view_range_cooking = False
        self._udpate_prepare_timer = None
        self.best_role_skin_show = None
        self.best_mecha_skin_show = None
        self.boost_sfx_id = None
        self.role_model_visible_set = False
        self.stage_plane_sound = None
        self.guangqi_car_model = None
        self.load_guangqi_car_task = None
        self.guangqi_car_taizi_model = None
        self.load_guangqi_car_taizi_task = None
        return

    def init_mgr(self):
        if hasattr(global_data.battle, 'area_id') and global_data.battle.area_id:
            self.range_mgr = BattlePrepare.BattleRangeMgr()

    def get_event_conf(self):
        event_conf = {'on_battle_status_changed': self.on_battle_status_changed,
           'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'island_top_skin_change': self.on_island_top_skin_change,
           'net_reconnect_event': self.on_reconnect,
           'start_preload_cockpit': self.on_start_preload_cockpit,
           'is_battle_prepare_data_finish': self.is_res_prepared,
           'scene_camera_target_setted_event': self.on_camera_target_setted,
           'rotate_stage_plane_camera': self.rotate_stage_plane_camera,
           'groupmate_parachute_mecha_disappear': self.groupmate_mecha_disappear,
           'is_launch_boost_updating_camera': self.is_updating_camera,
           'mecha_control_main_ui_event': self._forbid_mecha_weapon,
           'test_fly_emote': self.test_fly_emote
           }
        return event_conf

    def update_outline_process(self, flag):
        from logic.gutils import scene_utils
        if flag:
            scene_utils.reset_outline_process()
        else:
            scene_utils.pause_outline_process()

    def remove_range(self):
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        return

    def on_exit(self):
        self.reset_prepare_stage()
        self.reset_scene_data()
        if self.launch_boost_appearance:
            self.launch_boost_appearance.destroy()
            self.launch_boost_appearance = None
            self.launch_boost_appearance_destroyed = True
            self.launch_boost_appearance_destroyed_reason += 'exit ' + str(get_server_time()) + ' '
        self.camera_ctrl = None
        self._stop_update()
        self.remove_island_relative()
        self.stop_playing_sound()
        super(SurvivalBattlePrepare, self).on_exit()
        return

    def init_data(self):
        parachute_conf = confmgr.get('parachute_conf').get_conf()
        self.launch_fov = parachute_conf['LAUNCH_FOV']
        self.free_drop_fov = parachute_conf['FREE_DROP_FOV']

    def get_scene(self):
        return self.battle_prepare.scene()

    def add_update_prepare_timer(self):
        self.stop_update_prepare_timer()
        self._udpate_prepare_timer = global_data.game_mgr.register_logic_timer(self.update_prepare_time, interval=1, times=-1, mode=CLOCK)

    def stop_update_prepare_timer(self):
        if self._udpate_prepare_timer:
            global_data.game_mgr.unregister_logic_timer(self._udpate_prepare_timer)
            self._udpate_prepare_timer = None
        return

    def load_chushengtai_model(self):
        if global_data.enable_island_chushengtai:
            if not self.best_role_skin_show:
                if global_data.battle.get_scene_name() == battle_const.BATTLE_SCENE_KONGDAO:
                    self.best_role_skin_show = KongdaoBestSkinShow(self, SKIN_TYPE_ROLE)
                else:
                    self.best_role_skin_show = BwBestSkinShow(self, SKIN_TYPE_ROLE)
            else:
                self.best_role_skin_show.refresh()
            if not self.best_mecha_skin_show:
                if global_data.battle.get_scene_name() == battle_const.BATTLE_SCENE_KONGDAO:
                    self.best_mecha_skin_show = KongdaoBestSkinShow(self, SKIN_TYPE_MECHA)
                else:
                    self.best_mecha_skin_show = BwBestSkinShow(self, SKIN_TYPE_MECHA)
            else:
                self.best_mecha_skin_show.refresh()

    def clear_effect(self):
        for effect_id in self.effect_id_list:
            global_data.sfx_mgr.remove_sfx_by_id(effect_id)

        self.effect_id_list = []

    def create_fireworks_sfx(self):
        from logic.gutils import scene_utils
        self.clear_effect()
        if global_data.player:
            pos = global_data.player.logic.ev_g_position()
            sfx_paths = scene_utils.get_fireworks_path()
            for paths in sfx_paths:
                for path in paths:
                    fireworks_sfx = global_data.sfx_mgr.create_sfx_in_scene(path, pos=pos)
                    self.effect_id_list.append(fireworks_sfx)

    def destory_chushengtai(self):
        if self.best_role_skin_show:
            self.best_role_skin_show.destroy()
            self.best_role_skin_show = None
        if self.best_mecha_skin_show:
            self.best_mecha_skin_show.destroy()
            self.best_mecha_skin_show = None
        return

    def load_guangqi_car(self):
        taizi_res_path = confmgr.get('script_gim_ref')['guangqi_car_taizi']
        data = [False, [-216.33, 810.37, 18032.66], [0, 0, 0], [0.473754, 0.414415, 0.473754]]
        self.load_guangqi_car_taizi_task = world.create_model_async(taizi_res_path, self.on_guangqi_car_model_loaded, data, game3d.ASYNC_HIGH)
        car_res_path = confmgr.get('script_gim_ref')['guangqi_car']
        data = [True, [-216.336, 814.331726, 18032.66], [0, 0, 0], [0.17, 0.17, 0.17]]
        self.load_guangqi_car_task = world.create_model_async(car_res_path, self.on_guangqi_car_model_loaded, data, game3d.ASYNC_HIGH)

    def on_guangqi_car_model_loaded(self, model, data, task, *args):
        model.world_position = math3d.vector(*data[1])
        rot = [ math.radians(i) for i in data[2] ]
        rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
        model.world_rotation_matrix = rotation_matrix
        model.world_scale = math3d.vector(*data[3])
        scn = self.get_scene()
        if scn and scn.valid:
            scn.add_object(model)
            model.active_collision = True
            if data[0]:
                self.guangqi_car_model = model
                self.guangqi_car_model.cast_shadow = True
                self.guangqi_car_model.receive_shadow = True
            else:
                self.guangqi_car_taizi_model = model
                self.guangqi_car_taizi_model.receive_shadow = True

    def destory_guangqi_car(self):
        if self.guangqi_car_model:
            self.guangqi_car_model.destroy()
            self.guangqi_car_model = None
        if self.load_guangqi_car_task:
            self.load_guangqi_car_task.cancel()
            self.load_guangqi_car_task = None
        if self.guangqi_car_taizi_model:
            self.guangqi_car_taizi_model.destroy()
            self.guangqi_car_taizi_model = None
        if self.load_guangqi_car_taizi_task:
            self.load_guangqi_car_taizi_task.cancel()
            self.load_guangqi_car_taizi_task = None
        return

    def start_parachute_loading(self):
        global_data.emgr.camera_inited_event.emit()
        self.remove_island_relative()
        self.perform_ready()

    def update_prepare_time(self):
        if global_data.battle:
            if not global_data.battle.is_in_island():
                if not global_data.cam_lplayer:
                    self.stop_update_prepare_timer()
                else:
                    self.start_parachute_loading()

    def remove_island_relative(self):
        self.remove_range()
        self.destory_chushengtai()
        self.destory_guangqi_car()
        self.stop_update_prepare_timer()
        global_data.ui_mgr.close_ui('BornIslandUI')
        global_data.ui_mgr.close_ui('FightPrepareInteractUI')

    def on_pre_load(self):
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        scn = self.get_scene()
        need_cockpit = scn.get_scene_data('preload_cockpit', False)
        if need_cockpit:
            scn.set_view_range(0, 1)
            scn.set_view_range(1, 1)
            scn.set_view_range(2, 1)
            update_view_range_3(scn)
            if not hasattr(world, 'enable_merge_submesh_in_model'):
                world.set_max_merge_vertex(23000)
            scn.set_preload_dynamic_level(1)
            self._view_range_cooking = True

    def _view_range_medium(self, in_stage_plane):
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        if hasattr(world, 'is_async_scene_loader_use_g93_mode'):
            is_use_g93_mode = world.is_async_scene_loader_use_g93_mode()
        else:
            is_use_g93_mode = False
        scn = self.get_scene()
        if is_use_g93_mode:
            if in_stage_plane:
                scn.set_view_range(0, 1)
                scn.set_view_range(1, 1)
            else:
                scn.set_view_range(0, 850.0)
                scn.set_view_range(1, 2288.0)
            scn.set_view_range(2, display_setting.quality_value('LARGE_VIEW_RANGE') * 0.312)
            update_view_range_3(scn)
        else:
            if in_stage_plane:
                scn.set_view_range(0, 1)
                scn.set_view_range(1, 1)
            else:
                scn.set_view_range(0, 1000)
                scn.set_view_range(1, 4000)
            scn.set_view_range(2, display_setting.quality_value('LARGE_VIEW_RANGE'))
            update_view_range_3(scn)
        if not hasattr(world, 'enable_merge_submesh_in_model'):
            world.set_max_merge_vertex(3000)
        self._view_range_cooking = True

    def _view_range_well(self):
        scn = self.get_scene()
        view_range = scn.get_scene_data('view_range')
        scn.modify_view_range(view_range, True)
        if not hasattr(world, 'enable_merge_submesh_in_model'):
            world.set_max_merge_vertex(3000)
        self._view_range_cooking = False

    def call_launch_boost_appearance_func(self, func_name, *args, **kwargs):
        if not self.launch_boost_appearance:
            pass
        else:
            func = getattr(self.launch_boost_appearance, func_name)
            return func(*args)

    def start_choose_parachute_point(self):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.share_data.ref_parachute_stage == parachute_utils.STAGE_PLANE:
            self._setup_update()
            global_data.emgr.camera_on_start_nearclip.emit()

    def _begin_mecha_ready_animation(self, left_anim_time):
        global_data.emgr.camera_on_stop_nearclip.emit()
        world.set_skeleton_distances(1000000, 10000000)
        anim_init_time = 0.0
        screen_effect_path = 'effect/fx/scenes/common/fashecang/fsc_xq4_002.sfx'
        create_screen_effect_directly(screen_effect_path)
        for model in self.scene_model_list:
            model.play_animation('fashe')

            def load_boost_effect--- This code section failed: ---

 381       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'sfx_mgr'
           6  LOAD_ATTR             2  'create_sfx_on_model'
           9  LOAD_CONST            1  'effect/fx/scenes/common/fashecang/fsc_xq1_wmg.sfx'
          12  LOAD_CONST            2  'waimianguangyun'
          15  CALL_FUNCTION_3       3 
          18  LOAD_DEREF            0  'self'
          21  STORE_ATTR            3  'boost_sfx_id'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15

            model.register_anim_key_event('fashe', 'fx_waimianguangyun', load_boost_effect)
            fx_screen = 'effect/fx/scenes/common/fashecang/fsc_baiping.sfx'
            model.register_anim_key_event('fashe', 'dahuohua_end', lambda m, anim_name, event_name, path=fx_screen: create_screen_effect_directly(path))

        self.call_launch_boost_appearance_func('begin_mecha_ready_anim', DEFAULT_POS, self.scene_model_list[0].world_rotation_matrix if self.scene_model_list else None)
        return

    def perform_ready(self):
        global_data.cam_lplayer.send_event('E_MECHA_BORDING')
        global_data.sound_mgr.play_music('flight')
        global_data.sound_mgr.play_sound_2d('Play_ui_prepare', ('ui_prepare', 'ui_confirm_match'))
        self.set_ui_visible(False)
        if self.ready_is_first:
            self.ready_is_first = False
            now = get_server_time()
            prepare_timestamp = 0
            battle = global_data.battle
            if battle:
                prepare_timestamp = getattr(battle, 'prepare_timestamp', 0)
            if prepare_timestamp - now > 0.5:
                self._begin_mecha_ready_animation(prepare_timestamp - now)
            else:
                self.start_choose_parachute_point()
        else:
            self.start_choose_parachute_point()

    def reset_scene_data(self):
        if self.boost_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.boost_sfx_id)
            self.boost_sfx_id = None
        for model in self.scene_model_list:
            model.destroy()

        self.scene_model_list = []
        self.scene_model_size = 0
        for task in self.scene_loading_tasks:
            task.cancel()

        self.scene_loading_tasks = []
        return

    def reset_prepare_stage(self):
        if CGameModeManager().get_enviroment() == 'night':
            env_name = 'competition_bw_06_night.xml'
        elif CGameModeManager().get_enviroment() == 'granbelm':
            env_name = 'competition_bw_06_granbelm.xml'
        else:
            env_name = 'competition_bw_06.xml'
        self.get_scene().load_env(env_name)
        global_data.emgr.scene_tigger_auto_fog.emit(True)
        for _timer in self.model_move_timer_list:
            global_data.game_mgr.unregister_logic_timer(_timer)

        self.model_move_timer_list = []
        self.clear_effect()
        self.res_prepared = False
        self.trk_start_time = 0
        self.is_in_prepare_status = False

    def check_scene_model_state(self, parachute_stage):
        if parachute_stage == parachute_utils.STAGE_NONE:
            for model in self.scene_model_list:
                model.visible = True

        elif parachute_stage == parachute_utils.STAGE_PLANE:
            return
        if parachute_stage == parachute_utils.STAGE_ISLAND:
            for model in self.scene_model_list:
                model.visible = False

        elif self.scene_model_list:
            self.reset_scene_data()

    def check_camera_inited(self):
        if self.launch_boost_appearance and self.launch_boost_appearance.own_mecha_model_loaded() and self.scene_model_list and self.get_models_count() == self.scene_model_size:
            self.res_prepared = True
            if self.had_preload_cockpit and global_data.battle:
                global_data.battle.on_preload_cockpit_complete()

    def set_ui_visible(self, show_ui):
        if show_ui:
            global_data.ui_mgr.set_all_ui_visible(True)
            global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
        else:
            from logic.gutils import judge_utils
            if judge_utils.is_ob():
                global_data.ui_mgr.set_all_ui_visible(True)
                wl_for_judge = ('JudgeLoadingUI', 'BigMapUI')
                wl = []
                wl.extend(wl_for_judge)
                global_data.ui_mgr.add_ui_show_whitelist(wl, self.__class__.__name__)
            else:
                global_data.ui_mgr.set_all_ui_visible(False)

    def update(self, dt):
        if not global_data.cam_lplayer:
            return
        if not global_data.battle:
            return
        lplayer = global_data.cam_lplayer
        cur_parachute_stage = lplayer.share_data.ref_parachute_stage
        if cur_parachute_stage in (parachute_utils.STAGE_PLANE, parachute_utils.STAGE_PRE_PARACHUTE):
            plane = global_data.battle.get_entity(global_data.battle.plane_id)
            if not (plane and plane.logic):
                prepare_timestamp = getattr(global_data.battle, 'prepare_timestamp', 0)
                if prepare_timestamp and get_server_time() > prepare_timestamp:
                    lplayer.send_event('E_OPEN_PARACHUTE')
                return
            pos = plane.logic.ev_g_position()
            forward = plane.logic.ev_g_plane_direction()
            if pos:
                if self.is_first_valid_update:
                    self.is_first_valid_update = False
                    self.call_launch_boost_appearance_func('stop_mecha_ready_anim')
                    self.call_launch_boost_appearance_func('own_mecha_play_fly_animation')
                    self.reset_scene_data()
                scn = self.get_scene()
                scn.viewer_position = pos
                camera = scn.active_camera
                mecha_position, cam_mat, cam_pos = pos, camera.world_rotation_matrix, camera.world_position
                ret = self.call_launch_boost_appearance_func('update', camera, forward, pos, dt)
                if ret:
                    mecha_position, cam_mat, cam_pos = ret
                part_cam = scn.get_com('PartCamera')
                part_cam.cam_target_manager.set_yaw_and_pitch(cam_mat.yaw, cam_mat.pitch)
                part_cam.cam_target_manager.refresh_yaw_range()
                lplayer.send_event('E_ACTION_SET_YAW', cam_mat.yaw)
                lplayer.send_event('E_CAM_PITCH', cam_mat.pitch)
                camera.world_position = cam_pos
                global_data.player.logic.send_event('E_FOOT_POSITION', mecha_position)
                if G_POS_CHANGE_MGR:
                    global_data.player.logic.notify_pos_change(mecha_position)
                else:
                    global_data.player.logic.send_event('E_POSITION', mecha_position)
                if cur_parachute_stage == parachute_utils.STAGE_PRE_PARACHUTE:
                    if self.launch_boost_appearance:
                        exit_intrp_left_time = self.launch_boost_appearance.cam_intrp_left_time
                    else:
                        exit_intrp_left_time = 0.0
                    if exit_intrp_left_time <= 0.0:
                        lplayer.send_event('E_OPEN_PARACHUTE')
                    else:
                        if exit_intrp_left_time <= 0.5:
                            player_pos = math3d.vector(mecha_position.x, mecha_position.y - 0.5 * NEOX_UNIT_SCALE, mecha_position.z)
                            lplayer.send_event('E_FOOT_POSITION', player_pos)
                            if not self.role_model_visible_set:
                                self.role_model_visible_set = True
                                lplayer.send_event('E_SHOW_MODEL')
                        if lplayer.share_data.ref_character and lplayer.share_data.ref_character.verticalVelocity == 0.0:
                            lplayer.share_data.ref_character.verticalVelocity = -130

    def get_models_count(self):
        return len(self.scene_model_list)

    def on_scene_data_loaded(self, model, data, cnt_task, *args):
        scene = self.get_scene()
        if not (scene and scene.valid):
            return
        if cnt_task not in self.scene_loading_tasks:
            return
        self.scene_loading_tasks.remove(cnt_task)
        model.world_position = DEFAULT_POS
        self.scene_model_list.append(model)
        scene.add_object(model)
        if G_IS_NA_PROJECT:

            def load_sfx_on_model(m, sockets, path):
                for socket in sockets:
                    global_data.sfx_mgr.create_sfx_on_model(path, m, socket)

            for sfx_info in SFX_INFO_LIST:
                event_name = sfx_info['event_name']
                socket_list = sfx_info['socket_list']
                sfx_path = sfx_info['sfx_path']
                model.register_anim_key_event('fashe', event_name, lambda m, anim_name, evt_name, sockets=socket_list, path=sfx_path: load_sfx_on_model(m, sockets, path))

        elif hasattr(model, 'unlimit_socket_obj'):
            model.unlimit_socket_obj(True)
        if self.get_models_count() == self.scene_model_size:
            self.check_camera_inited()

    def load_launch_scene(self):
        path_list = [
         confmgr.get('script_gim_ref')['fashedating']]
        for index, path in enumerate(path_list):
            self.scene_loading_tasks.append(world.create_model_async(path, self.on_scene_data_loaded, (index == 0,), RES_LOAD_PRIORITY))

        self.scene_model_size = len(path_list)

    def init_prepare_stage(self):
        import render
        import logic.vscene.global_display_setting as gds
        global_data.emgr.scene_tigger_auto_fog.emit(False)
        scene = self.get_scene()
        if not (scene and scene.valid):
            return
        scene.load_env('prepare_env.xml')
        display_setting = gds.GlobalDisplaySeting()
        if display_setting.quality_value('FOG_ENABLE'):
            i_type, mode, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent = scene.get_fog()
            offset_y = DEFAULT_POS.y + 500
            height_begin += offset_y
            height_end += offset_y
            scene.set_fog(i_type, mode, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent)
        else:
            i_type, mode, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent = scene.get_fog()
            scene.set_fog(i_type, render.RS_FOG_NONE, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent)
        self.is_in_prepare_status = True
        camera = scene.active_camera
        camera.fov = self.launch_fov
        camera.z_range = (PREPARE_ZMIN, PREPARE_ZMAX)

    def _setup_update(self):
        if self._update_timer is None:
            self.is_first_valid_update = True
            self._update_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self.update, timedelta=True)
        return

    def _stop_update(self):
        if self._update_timer is not None:
            global_data.game_mgr.get_fix_logic_timer().unregister(self._update_timer)
            self._update_timer = None
        return

    def stop_playing_sound(self):
        if self.stage_plane_sound:
            global_data.sound_mgr.stop_playing_id(self.stage_plane_sound)
            self.stage_plane_sound = None
        return

    def _forbid_mecha_weapon(self):
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not ui:
            return
        is_in_island = global_data.battle.is_in_island()
        if not is_in_island:
            return
        for action in ('action1', 'action2', 'action3', 'action4', 'action6', 'action7',
                       'action8'):
            ui.on_set_action_forbidden(action, True)
            ui.on_set_action_nb_visible(action, False)

    def on_battle_status_changed(self, status):
        if status == Battle.BATTLE_STATUS_PREPARE:
            if global_data.battle.is_in_island():
                scn = self.get_scene()
                scn.modify_view_range(1000)
                if self.range_mgr:
                    self.range_mgr.create_all_range_model()
                self.load_chushengtai_model()
                self.create_fireworks_sfx()
                if not global_data.ui_mgr.get_ui('BornIslandUI'):
                    global_data.ui_mgr.show_ui('BornIslandUI', 'logic.comsys.prepare')
                battle = global_data.battle
                if not battle.is_single_person_battle():
                    if not global_data.ui_mgr.get_ui('FightPrepareInteractUI'):
                        global_data.ui_mgr.show_ui('FightPrepareInteractUI', 'logic.comsys.prepare')
                self.add_update_prepare_timer()
                self.update_outline_process(False)
                global_data.emgr.scene_sound_visible.emit(False)
            else:
                self.start_parachute_loading()
        elif status == Battle.BATTLE_STATUS_PARACHUTE:
            global_data.emgr.camera_inited_event.emit()
            self.remove_island_relative()
            self.update_outline_process(True)
            global_data.emgr.scene_sound_visible.emit(True)
            self.start_choose_parachute_point()

    def on_player_parachute_stage_changed(self, *args):
        if self.get_scene() is None:
            return
        else:
            if not global_data.cam_lplayer:
                return
            if global_data.is_judge_ob:
                return
            parachute_stage = global_data.cam_lplayer.share_data.ref_parachute_stage
            is_prepare = global_data.cam_lplayer.ev_g_is_parachute_prepare()
            if is_prepare and not self.is_in_prepare_status:
                self.init_prepare_stage()
            if not is_prepare and self.is_in_prepare_status:
                self.reset_prepare_stage()
            if parachute_stage in (parachute_utils.STAGE_NONE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_PLANE, parachute_utils.STAGE_LAUNCH_PREPARE):
                global_data.emgr.camera_stop_update_event.emit()
                self.call_launch_boost_appearance_func('load_groupmate_mecha_model')
            elif parachute_stage == parachute_utils.STAGE_PRE_PARACHUTE:
                global_data.emgr.camera_stop_update_event.emit()
            else:
                global_data.emgr.camera_refresh_update_event.emit()
            if parachute_stage == parachute_utils.STAGE_PLANE:
                if self.boost_sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self.boost_sfx_id)
                    self.boost_sfx_id = None
                if global_data.player.get_setting(uoc.AUTO_SHOW_PLANE_BIG_MAP):
                    global_data.emgr.scene_show_big_map_event.emit()
                world.set_skeleton_distances(SKELETON_LOD_DIST[0], SKELETON_LOD_DIST[1])
                self.stage_plane_sound = global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                                                'ui_mecha_drop'))
                if global_data.cam_lplayer:
                    global_data.cam_lplayer.send_event('E_TRY_CANCEL_RUN_LOCK')
                    global_data.cam_lplayer.send_event('E_FORBID_RUN_LOCK', True)
                global_data.emgr.camera_on_start_nearclip.emit()
                self.call_launch_boost_appearance_func('set_cam_intrp_state', INTRP_ENTER)
                self.role_model_visible_set = False
                self._setup_update()
            elif parachute_stage == parachute_utils.STAGE_PRE_PARACHUTE:
                self.call_launch_boost_appearance_func('set_cam_intrp_state', INTRP_EXIT)
                global_data.emgr.enable_camera_yaw.emit(False)
                self.role_model_visible_set = False
                if self.stage_plane_sound:
                    global_data.sound_mgr.stop_playing_id(self.stage_plane_sound)
                    self.stage_plane_sound = None
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'ui_mecha_drop_end'))
                character = global_data.cam_lplayer.share_data.ref_character
                if not character:
                    return
                character.setGravity(390 * global_data.cam_lplayer.sd.ref_gravity_scale)
                global_data.cam_lplayer.send_event('E_FALL_SPEED', 130)
                global_data.cam_lplayer.send_event('E_FORBID_RUN_LOCK', False)
                if not self._update_timer:
                    global_data.cam_lplayer.send_event('E_OPEN_PARACHUTE')
            else:
                global_data.emgr.enable_camera_yaw.emit(True)
                self._stop_update()
            if parachute_stage in (parachute_utils.STAGE_PARACHUTE_DROP, parachute_utils.STAGE_PLANE):
                self._view_range_cooking = True
                self._view_range_medium(parachute_stage == parachute_utils.STAGE_PLANE)
            elif parachute_stage == parachute_utils.STAGE_LAND and self._view_range_cooking:
                self._view_range_well()
            self.check_scene_model_state(parachute_stage)
            self.launch_boost_appearance and self.launch_boost_appearance.check_mecha_model_state()
            if not is_prepare:
                global_data.ui_mgr.set_all_ui_visible(True)
                global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
                global_data.mouse_mgr and global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)
            else:
                global_data.mouse_mgr and global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
            if parachute_stage == parachute_utils.STAGE_LAND:
                self._stop_update()
            return

    def on_island_top_skin_change(self):
        if self.best_role_skin_show:
            self.best_role_skin_show.refresh()
        if self.best_mecha_skin_show:
            self.best_mecha_skin_show.refresh()

    def on_reconnect(self):
        self.launch_boost_appearance and self.launch_boost_appearance.on_reconnect()

    def on_start_preload_cockpit(self):
        self.had_preload_cockpit = True
        self.load_launch_scene()
        self.launch_boost_appearance = LaunchBoostAppearance(self, self.check_camera_inited)

    def is_res_prepared(self):
        return self.res_prepared

    def on_camera_target_setted(self):
        if global_data.player and global_data.player.logic:
            if global_data.cam_lplayer == global_data.player.logic:
                return
        self.on_player_parachute_stage_changed()

    def rotate_stage_plane_camera(self, rot_vec):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.share_data.ref_parachute_stage != parachute_utils.STAGE_PLANE:
            return
        delta_yaw, delta_pitch = rot_vec.x, -rot_vec.y
        self.call_launch_boost_appearance_func('set_cam_delta_yaw_and_pitch', delta_yaw * 0.0033, delta_pitch * 0.0033)

    def groupmate_mecha_disappear(self, eid):
        self.launch_boost_appearance and self.launch_boost_appearance.groupmate_mecha_disappear(eid)

    def is_updating_camera(self):
        return self._update_timer is not None

    def test_fly_emote(self, emote_anim_name):
        if global_data.cam_lplayer.share_data.ref_parachute_stage != parachute_utils.STAGE_PLANE:
            return
        self.launch_boost_appearance and self.launch_boost_appearance.test_fly_emote(emote_anim_name)