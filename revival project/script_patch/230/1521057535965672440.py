# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/ExSceneManagerAgent.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.manager_agents import ManagerAgentBase
from logic.vscene.scene import Scene
import world
import gc
import math3d
from logic.comsys.archive import archive_manager
from logic.comsys.archive import archive_key_const
import six.moves.builtins
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
import game3d
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2, TopLevelConfirmUI2
from common.cfg import confmgr
import logic.gcommon.common_const.scene_const as scene_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.pve_const import PVE_END_BG_PATH
BACKGROUND_MODEL_NAME = 'zhanshi_pifu_chunjie'
BACKGROUND_MODEL_NAME_SAIJIKA = 'jiemian_zhanshi_s4'
BACKGROUND_SFX_MODEL_NAME = 'sfx_model'
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
_HASH_TEX1 = game3d.calc_string_hash('Tex1')
_HASH_TEX2 = game3d.calc_string_hash('Tex2')
_HASH_LERP_SMOOTH = game3d.calc_string_hash('lerpSmooth')
_HASH_LERP_SPEED = game3d.calc_string_hash('lerpSpeed')
MTRL_KEY2HASH = {'Tex1': _HASH_TEX1,'Tex2': _HASH_TEX2,
   'lerpSmooth': _HASH_LERP_SMOOTH,
   'lerpSpeed': _HASH_LERP_SPEED
   }

class ExSceneManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'ex_scene_mgr_agent'

    def init(self, *args):
        super(ExSceneManagerAgent, self).init()
        self.extra_scene_map = dict()
        self.extra_scene_loaded = dict()
        self.extra_scene_added = dict()
        self.scene_stack = []
        self.scene_ui_map = {}
        self.scene_ui_stack = []
        self.lobby_relatived_scene = {}

    def update_scene_logic(self, dt):
        for ext_scn in six.itervalues(self.extra_scene_map):
            if ext_scn.is_loaded():
                ext_scn.logic(dt)

    def update_scene_fix_logic(self, dt):
        for ext_scn in six.itervalues(self.extra_scene_map):
            if ext_scn.is_loaded():
                ext_scn.fix_logic(dt)

    def is_extra_scene_loaded(self, scene_type):
        return self.extra_scene_map.get(scene_type, None) and self.extra_scene_map[scene_type].is_loaded()

    def _do_special_extra_scene_load_logic(self, scene_type):
        if scene_type in (scene_const.SCENE_NORMAL_SETTLE, scene_const.SCENE_NIGHT_SETTLE):
            if global_data.game_mode.is_snow_res() and global_data.is_ue_model:
                global_data.game_mode.set_enviroment(battle_const.BATTLE_ENV_SUMMER)
                cur_scene = global_data.game_mgr.scene
                cur_scene.set_macros({'SNOW_ENABLE': '0'})
                cur_scene.set_macros({'ENV_TYPE': str(battle_const.SHADER_EVN_NORMAL)})

    def load_extra_scene_background(self, scene_type, scene_data=None, callback=None):
        if scene_type not in self.extra_scene_map:
            self.extra_scene_added[scene_type] = False
            self.extra_scene_loaded[scene_type] = False
            self._do_special_extra_scene_load_logic(scene_type)

            def loaded_cb():
                self.extra_scene_loaded[scene_type] = True
                if self.extra_scene_added.get(scene_type, False):
                    self.add_extra_scene(scene_type)
                callback and callable(callback) and callback()

            self.extra_scene_map[scene_type] = Scene(scene_type, scene_data, loaded_cb, back_load=True, force_sync=True)

    def _do_special_extra_scene_add_logic(self, scene_type, scene_data=None):
        if scene_type in (scene_const.SCENE_NORMAL_SETTLE, scene_const.SCENE_NIGHT_SETTLE):
            battle_scene = global_data.game_mgr.scene
            if battle_scene:
                global_data.emgr.camera_stop_update_event.emit()
                battle_scene.set_view_range(0, 1)
                battle_scene.set_view_range(1, 1)
                battle_scene.set_view_range(2, 1)
                if global_data.player and global_data.player.logic:
                    global_data.player.logic.send_event('E_FORCE_DEACTIVE')
                    target = global_data.player.logic.ev_g_control_target()
                    if target and target.logic:
                        target.logic.send_event('E_FORCE_DEACTIVE')
                        target.logic.send_event('E_VEHICLE_ENABLE_PHYSICS', False)
                viewer_position = math3d.vector(-26442, 28, -25976)
                battle_scene.viewer_position = viewer_position
                if hasattr(battle_scene, 'enable_auto_update'):
                    battle_scene.enable_auto_update(True)
            from logic.gutils import scene_utils
            scene_utils.set_outline_process_enable(False, scene_utils.HERO_OUTLINE_MASK)
            scene_utils.set_outline_process_enable(False, scene_utils.INFRARED_DETECTOR_MASK)
            scene_utils.set_outline_process_enable(False, scene_utils.GAME_MODE_OUTLINE_MASK)
        elif scene_type == scene_const.SCENE_PVE_END_UI:
            if scene_data:
                ext_scn = self.extra_scene_map.get(scene_type, None)
                if ext_scn:
                    scene_res_config = confmgr.get('lobby_model_display_conf', 'SceneConfig', 'Content', str(scene_type), default={})
                    bg_model_name = scene_res_config.get('bg_model_name')
                    if bg_model_name:
                        background_model = ext_scn.get_model(bg_model_name)
                        if background_model:
                            chapter = scene_data.get('chapter')
                            difficulty = scene_data.get('difficulty')
                            scene_background_texture = PVE_END_BG_PATH.format(chapter, difficulty)
                            material = background_model.get_sub_material(0)
                            material.set_texture(_HASH_DIFFUSE, 'Tex0', scene_background_texture)
        return

    def add_extra_scene(self, scene_type, scene_data=None):
        if self.extra_scene_map.get(scene_type, None):
            if self.extra_scene_loaded.get(scene_type, False):

                def actually_add_extra_scene():
                    scn = self.extra_scene_map.get(scene_type, None)
                    if scn and scn != world.get_active_scene():
                        world.set_active_scene(scn)
                        scn.on_enter()
                        global_data.emgr.extra_scene_added.emit(scene_type)
                        self._do_special_extra_scene_add_logic(scene_type, scene_data=scene_data)
                    return

                global_data.game_mgr.post_exec(actually_add_extra_scene)
            self.extra_scene_added[scene_type] = True
        return

    def pop_extra_scene(self, scene_type, call_enter=False):
        ext_scn = self.extra_scene_map.get(scene_type, None)
        if ext_scn:
            self.extra_scene_loaded[scene_type] = False
            self.extra_scene_added[scene_type] = False
            ext_scn.on_exit()
            world.set_active_scene(None)
            ext_scn.destroy()
            self.extra_scene_map.pop(scene_type)
            global_data.game_mgr.active_cur_scene(call_enter)
        return

    def check_settle_scene_active(self):
        for scene_type in (scene_const.SCENE_NORMAL_SETTLE, scene_const.SCENE_NIGHT_SETTLE):
            if scene_type in self.extra_scene_map:
                return True

        return False

    def pop_settle_scene(self):
        for scene_type in (scene_const.SCENE_NORMAL_SETTLE, scene_const.SCENE_NIGHT_SETTLE, scene_const.SCENE_PVE_END_UI):
            self.pop_extra_scene(scene_type)

    def do_load_scene(self, scn_cls, scene_type, scene_data, callback, async_load, back_load, release):
        if scene_type == 'Lobby':
            print('scene manager agent begin load lobby')
            archive_manager.ArchiveManager().save_general_archive_data_value(archive_key_const.KEY_LAST_BATTLE_SERVER_VERSION, str(-1))
            reverted_before = six.moves.builtins.__dict__.get('WEEK_PATCH_REVERTED', False)
            if reverted_before:

                def on_confirm_clicked():
                    global_data.game_mgr.try_restart_app()

                def delay_confirm_quit():
                    TopLevelConfirmUI2(content=196, on_confirm=on_confirm_clicked)

                game3d.delay_exec(1000, delay_confirm_quit)
                return
        same_path_scene = False
        cur_scene = global_data.game_mgr.scene
        if cur_scene:
            same_path_scene = cur_scene.is_same_scene_path(scene_data)
            self.pop_all_lobby_relative_scene()
            cur_scene = global_data.game_mgr.scene
            if release:
                cur_scene.on_exit()
                if hasattr(cur_scene, 'is_battle_scene') and cur_scene.is_battle_scene():
                    if global_data.battle and global_data.battle.map_id is not None:
                        CGameModeManager().set_map(global_data.battle.map_id, global_data.battle.battle_tid)
                        from logic.vscene.parts.camera.camera_controller.CameraData import CameraData
                        CameraData()
                if not same_path_scene:
                    global_data.game_mgr.release_cur_scene()
                    cur_scene = None
            else:
                self.scene_stack.append(cur_scene)
                self.scene_ui_stack.append(None)
        if not same_path_scene:
            world.set_active_scene(None)
        gc.collect()
        print('same_path_scene', same_path_scene)
        if not same_path_scene:
            print('scene data is', scene_data)
            cur_scene = scn_cls(scene_type, scene_data, callback, async_load, back_load)
            print('cur scene', cur_scene)
            print('active cur scene')
            global_data.game_mgr.active_cur_scene(False, cur_scene)
        else:
            cur_scene.reinit_scene(scene_type, scene_data, callback)
        return

    def pop_all_lobby_relative_scene(self):
        if self.scene_stack:
            self.scene_stack = self.scene_stack[:1]
            self.scene_ui_stack = self.scene_ui_stack[:1]
            self.scene_ui_map = {}
            self.return_scene()
        for relatived_scene in six.itervalues(self.lobby_relatived_scene):
            if relatived_scene is not None:
                relatived_scene.on_exit()
                relatived_scene.destroy()

        self.lobby_relatived_scene = {}
        return

    def return_scene(self, release=False, reset_resolution=True):
        if not self.scene_stack:
            return
        else:
            cur_scene = global_data.game_mgr.scene
            if release:
                scene_type = cur_scene.get_type()
                cur_scene.on_exit()
                world.set_active_scene(None)
                cur_scene.destroy()
                if scene_type in self.lobby_relatived_scene:
                    self.lobby_relatived_scene[scene_type] = None
            else:
                cur_scene.on_pause(True)
            new_scene = self.scene_stack.pop(-1)
            self.scene_ui_stack.pop(-1)
            cur_scene in self.scene_ui_map and self.scene_ui_map.pop(cur_scene)
            global_data.game_mgr.active_cur_scene(False, new_scene)
            new_scene.on_pause(False)
            if global_data.enable_resolution_switch and reset_resolution:
                global_data.display_agent.do_check_reset_resolution()
            return

    def add_disposable_lobby_relatived_scene(self, scene_type, scene_data, belong_ui_name=None):
        old_scene = self.lobby_relatived_scene.get(scene_type)
        world.set_model_fadein_when_load(False)
        scene_id = 0
        scene_res_config = None
        scene_path = None
        if scene_data:
            scene_path = scene_data['scene_path']
            if scene_path.isdigit():
                scene_id = int(scene_path)
                scene_res_config = confmgr.get('lobby_model_display_conf', 'ReflectSceneType', 'Content', str(scene_id), default={})
                scene_data['scene_path'] = scene_res_config['scene_path']
        if scene_data is not None:
            scene_conf = scene_data if 1 else confmgr.get('scenes', scene_type)
            if scene_res_config:
                sfx_list = scene_res_config.get('sfx_list', [])
            else:
                sfx_list = []
            is_same_scene = False
            if old_scene and old_scene.is_same_scene_path(scene_data):
                new_scene = old_scene
                is_same_scene = False
            else:
                new_scene = Scene(scene_type, scene_conf, back_load=False, force_sync=True)
            if scene_id and scene_res_config:
                background_model = new_scene.get_model(BACKGROUND_MODEL_NAME)
                background_pos = scene_res_config.get('background_pos', None)
                background_scale = scene_res_config.get('background_scale', None)
                mtrl_param = scene_res_config.get('mtrl_param')
                if scene_res_config.get('model_texture') and not background_model:
                    import traceback
                    traceback.print_stack()
                if background_model and background_model.valid and scene_res_config.get('model_texture'):
                    material = background_model.get_sub_material(0)
                    material.set_texture(_HASH_DIFFUSE, 'Tex0', scene_res_config['model_texture'])
                    if background_pos:
                        background_model.world_position = math3d.vector(*background_pos)
                    if background_scale:
                        background_model.scale = math3d.vector(*background_scale)
                    if mtrl_param:
                        for key, value in six.iteritems(mtrl_param):
                            if key not in MTRL_KEY2HASH:
                                continue
                            if 'Tex' in key:
                                material.set_texture(MTRL_KEY2HASH[key], key, value)
                            else:
                                material.set_var(MTRL_KEY2HASH[key], key, value)

                sfx_list = is_same_scene or scene_res_config.get('sfx_list', [])
                for sfx_info in sfx_list:
                    source_path = sfx_info.get('source_path', '')
                    socket = sfx_info.get('socket', None)
                    pos = sfx_info.get('pos', [0, 0, 0])
                    if source_path.endswith('.sfx'):
                        sfxs = world.sfx(source_path)
                        if socket and background_model:
                            background_model.bind(socket, sfxs)
                        else:
                            sfxs.world_position = math3d.vector(*pos)
                            new_scene.add_object(sfxs)
                    else:
                        model = world.model(source_path, new_scene)
                        model.world_position = math3d.vector(*pos)

        elif 'bg_model_name' in scene_data and 'scene_background_texture' in scene_data:
            background_model = new_scene.get_model(scene_data['bg_model_name'])
            texture_path = scene_data['scene_background_texture']
            if background_model and background_model.valid and texture_path:
                material = background_model.get_sub_material(0)
                material.set_texture(_HASH_DIFFUSE, 'Tex0', texture_path)
        self.lobby_relatived_scene[scene_type] = new_scene
        self.switch_scene(new_scene, belong_ui_name)
        global_data.emgr.update_jiemian_scene_content.emit(scene_id, scene_type)
        return new_scene

    def add_lobby_relatived_scene(self, scene_type, finish_callback=None, belong_ui_name=None, scene_content_type=None, scene_background_texture=None, sfx_list=None, change_saijika_background=False):
        if self.lobby_relatived_scene.get(scene_type) is None:

            def load_complete():
                self.add_lobby_relatived_scene(scene_type, finish_callback, belong_ui_name=belong_ui_name, scene_content_type=scene_content_type, scene_background_texture=scene_background_texture, sfx_list=sfx_list, change_saijika_background=change_saijika_background)

            self.load_lobby_relatived_scene(scene_type, load_complete)
            return
        else:
            relatived_scene = self.lobby_relatived_scene[scene_type]
            scene_res_config = lobby_model_display_utils.get_scene_res_config(scene_type)
            if not relatived_scene.loading_wrapper or relatived_scene.loading_wrapper.get_percentage() == 100:
                cur_scene = global_data.game_mgr.scene
                if cur_scene != relatived_scene:
                    self.switch_scene(relatived_scene, belong_ui_name)
                relatived_scene.scene_content_type = scene_content_type
                global_data.emgr.update_jiemian_scene_content.emit(scene_type, scene_content_type)
                content_scene_res_config = confmgr.get('lobby_model_display_conf', 'SceneConfig', 'Content', str(scene_content_type), default={})
                bg_model_name = content_scene_res_config.get('bg_model_name')
                background_model = bg_model_name or relatived_scene.get_model(BACKGROUND_MODEL_NAME_SAIJIKA if change_saijika_background else BACKGROUND_MODEL_NAME)
            else:
                background_model = relatived_scene.get_model(bg_model_name)
            if scene_res_config or scene_background_texture:
                texture_path = scene_background_texture if scene_background_texture else scene_res_config['model_texture']
                background_pos = scene_res_config.get('background_pos', None) if scene_res_config else None
                background_scale = scene_res_config.get('background_scale', None)
                mtrl_param = scene_res_config.get('mtrl_param')
                if background_model and background_model.valid and texture_path:
                    material = background_model.get_sub_material(0)
                    material.set_texture(_HASH_DIFFUSE, 'Tex0', texture_path)
                    if background_pos:
                        background_model.world_position = math3d.vector(*background_model)
                    if background_scale:
                        background_model.scale = math3d.vector(*background_scale)
                    if mtrl_param:
                        for key, value in six.iteritems(mtrl_param):
                            if key not in MTRL_KEY2HASH:
                                continue
                            if 'Tex' in key:
                                material.set_texture(MTRL_KEY2HASH[key], key, value)
                            else:
                                material.set_var(MTRL_KEY2HASH[key], key, value)

            if scene_res_config or sfx_list:
                if sfx_list:
                    sfx_list = sfx_list if 1 else scene_res_config.get('sfx_list', [])
                    for sfx_info in sfx_list:
                        source_path = sfx_info.get('source_path', '')
                        socket = sfx_info.get('socket', None)
                        pos = sfx_info.get('pos', [0, 0, 0])
                        if source_path.endswith('.sfx'):
                            sfxs = world.sfx(source_path)
                            if socket and background_model:
                                background_model.bind(socket, sfxs)
                            else:
                                sfxs.world_position = math3d.vector(*pos)
                                new_scene.add_object(sfxs)
                        else:
                            model = world.model(source_path, new_scene)
                            model.world_position = math3d.vector(*pos)

                if finish_callback:
                    finish_callback(scene_type, relatived_scene)
                return relatived_scene
            return

    def load_lobby_relatived_scene(self, scene_type, callback=None, scene_data=None):
        if self.lobby_relatived_scene.get(scene_type) is None:
            scene_conf = scene_data if scene_data is not None else confmgr.get('scenes', scene_type)
            scene_res_config = lobby_model_display_utils.get_scene_res_config(scene_type)
            if scene_res_config and scene_res_config.get('scene_path', None):
                scene_conf = scene_conf.copy()
                scene_conf['scene_path'] = scene_res_config['scene_path']
            loaded = False
            assigned_to_dict = False

            def loaded_cb():
                loaded = True
                if assigned_to_dict:
                    if callable(callback):
                        callback()

            new_scene = Scene(scene_type, scene_conf, loaded_cb, back_load=True, force_sync=True)
            self.lobby_relatived_scene[scene_type] = new_scene
            assigned_to_dict = True
            if loaded:
                if callable(callback):
                    callback()
        return

    def get_lobby_relatived_scene(self, scene_type):
        return self.lobby_relatived_scene.get(scene_type)

    def is_cur_lobby_relatived_scene(self, scene_type):
        cur_scene = global_data.game_mgr.get_cur_scene()
        if cur_scene.get_type() == scene_type or cur_scene.get_type() == scene_const.SCENE_JIEMIAN_COMMON and cur_scene.scene_content_type == scene_type:
            return True
        return False

    def _check_scene_in_stack(self, scn, ui_name):
        if scn in self.scene_stack:
            return self.scene_stack.index(scn)
        if ui_name and ui_name in self.scene_ui_stack:
            return self.scene_ui_stack.index(ui_name)
        return -1

    def switch_scene(self, new_scene, belong_ui_name=None):
        cur_scene = global_data.game_mgr.scene
        if new_scene:
            self.scene_stack.append(cur_scene)
            self.scene_ui_stack.append(self.scene_ui_map.get(cur_scene, None))
            index = self._check_scene_in_stack(new_scene, belong_ui_name)
            if index != -1:
                remove_scene = self.scene_stack.pop(index)
                remove_scene in self.scene_ui_map and self.scene_ui_map.pop(remove_scene)
                self.scene_ui_stack.pop(index)
            self.scene_ui_map[new_scene] = belong_ui_name
            cur_scene.on_pause(True)
            world.set_model_fadein_when_load(False)
            global_data.game_mgr.active_cur_scene(False, new_scene)
            new_scene.on_pause(False)
            if not new_scene.is_loaded():
                new_scene.on_enter()
            if global_data.enable_resolution_switch:
                global_data.display_agent.do_check_reset_resolution()
        else:
            log_error('ModelDisplay is not loaded!')
        return