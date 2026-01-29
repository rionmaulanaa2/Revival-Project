# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/scene.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
import math3d
import world
import render
import time
import game3d
import game
from logic.gcommon.common_const import battle_const
from common.algorithm import resloader
from common.cfg import confmgr
from common.platform import is_win32
from common.utilities import color_int, color_int_srgb
from common.utils import ui_utils
from logic.comsys.loading import loadwrapper
from patch.patch_utils import is_artist_package
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_utils import parachute_utils
from logic.gutils import scene_utils
from logic.client.const import game_mode_const
import device_limit
import device_compatibility
from . import progress
import json
import C_file
import math
import random
import collision
from logic.gcommon.common_const.collision_const import WATER_GROUP, WATER_MASK
from exception_hook import traceback_uploader
from common.utils import pc_platform_utils
from logic.gcommon.const import SKELETON_LOD_DIST
from logic.manager_agents.manager_decorators import sync_exec
import exception_hook
import version
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from logic.gcommon.common_const.battle_const import BATTLE_SCENE_NORMAL, BATTLE_SCENE_KONGDAO, INVALID_LANDSCAPE_SCENE
from logic.gutils.scene_utils import is_in_lobby
from logic.gutils.shader_warmup import DEFAULT_LOD_MAPPING
_HASH_ToneFactor = game3d.calc_string_hash('ToneFactor')
_HASH_BloomWidth = game3d.calc_string_hash('BloomWidth')
_HASH_BloomLayer = game3d.calc_string_hash('bloomlayer')
_HASH_BloomCoeff = game3d.calc_string_hash('BloomCoeff')
_HASH_BloomCoeff2 = game3d.calc_string_hash('BloomCoeff2')
_HASH_tex_lut = game3d.calc_string_hash('TexLut')
_HASH_enable_sky_box_ignore_tonemapper = game3d.calc_string_hash('enable_sky_box_ignore_tonemapper')
_HASH_intensity_x = game3d.calc_string_hash('intensity_x')
_HASH_intensity_y = game3d.calc_string_hash('intensity_y')
_HASH_BloomSize = game3d.calc_string_hash('BloomSize')
_HASH_BlurFactor = game3d.calc_string_hash('BlurFactor')
_HASH_SizeScale = game3d.calc_string_hash('SizeScale')
_HASH_BloomThreshold = game3d.calc_string_hash('BloomThreshold')
_HASH_Offset = game3d.calc_string_hash('Offset')
_HASH_SkyBoxBloomThreshold = game3d.calc_string_hash('SkyBoxBloomThreshold')
_HASH_ExposureScale = game3d.calc_string_hash('ExposureScale')
_HASH_BloomIntensity1 = game3d.calc_string_hash('BloomIntensity1')
_HASH_BloomColor1 = game3d.calc_string_hash('BloomColor1')
_HASH_BloomIntensity2 = game3d.calc_string_hash('BloomIntensity2')
_HASH_BloomColor2 = game3d.calc_string_hash('BloomColor2')
_HASH_BloomIntensity3 = game3d.calc_string_hash('BloomIntensity3')
_HASH_BloomColor3 = game3d.calc_string_hash('BloomColor3')
_HASH_enable_bloom = game3d.calc_string_hash('enable_bloom')
_HASH_AddBloomColor = game3d.calc_string_hash('AddBloomColor')
_HASH_u_sky_box_fog_factor = game3d.calc_string_hash('u_sky_box_fog_factor')
_HASH_u_skyline_power = game3d.calc_string_hash('u_skyline_power')
_HASH_u_skyline_intensity = game3d.calc_string_hash('u_skyline_intensity')
_HASH_u_skyline_color = game3d.calc_string_hash('u_skyline_color')
_HASH_TexLut = game3d.calc_string_hash('TexLut')
DEFAULT_CHUNK_SIZE = 832
ENABLE_CHECK_LEAK = False
LUT_MAP = {0: 'shader/texture_raw/style_1.bmp',
   1: 'shader/texture_raw/style_2.bmp',
   2: 'shader/texture_raw/lut_log.bmp',
   3: 'shader/texture_raw/style_4.bmp',
   4: 'shader/texture_raw/style_5.bmp'
   }
G_CUR_HDR_CONF_NAME = None

def update_view_range_3(self):
    self.set_view_range(3, 100000)


class GCTest(object):

    def __init__(self, obj):
        self.objid = id(obj)

    def __del__(self):
        pass


class Scene(world.scene):
    DETOUR_MESH = 'default_mesh'
    LOAD_DIST_TIME_2_VIS_DIST = 1.5
    DEFAULT_DETAIL_DIST = 1920
    ENABLE_PRELOAD_DYNAMIC = True
    PRELOAD_DYNAMIC_EXCLUDE_MODELS = ('sun', 'sun_flare')
    EXCLUDE_SHADOWMAP_MODELS = ('sun', 'sun_flare')
    ENABLE_PRELOAD_MODEL_SHADOWMAP = False
    ENABLE_BREAK_MODEL_SHADOWMAP = True
    FORBID_RECEIVCE_SHADOW_MODELS = ('shangcheng_beijing_03_8', 'shangcheng_beijing_03_11',
                                     'shangcheng_beijing_04_5', 'shangcheng_beijing_04_9',
                                     'shangcheng_beijing_04_6', 'shangcheng_beijing_03_9')
    ECONF = {'net_login_reconnect_event': 'on_login_reconnect',
       'display_quality_change': 'on_display_quality_change'
       }

    def __init__(self, scene_type, scene_data=None, callback=None, async_load=True, back_load=False, force_sync=False, notify_loading_ui=True):
        super(Scene, self).__init__()
        self.async_load = None
        self.init_scene_info(scene_type, scene_data, callback)
        self.enable_shadow_tex = False
        if global_data.feature_mgr.is_support_async_load_prior():
            print('set road_async_priority low...')
            self.road_async_priority = game3d.ASYNC_LOW
        if global_data.is_32bit and not G_IS_NA_PROJECT:
            if hasattr(self, 'enable_load_mirrors'):
                print('forbid to load mirrors for 32bit...')
                self.enable_load_mirrors(False)
        self.last_touch_end_location = None
        self._percent_st = progress.ST_PERCENT_NONE
        self._check_logic = self.check_st_percent
        self._detail_done = 0
        self.is_detour_enable = False
        self.map_uv_cache = None
        self._map_uv_para_cache = None
        self.enable_scene_custom_map_uv = False
        self.realtime_shadow_light = None
        self.original_light_dir = None
        self._env_file = None
        if global_data.is_low_mem_mode:
            self.enable_vlm = False
        else:
            self.enable_vlm = True
        self.enable_vlm = global_data.server_enable_vlm and self.enable_vlm
        self._ui_panels = {}
        self._cur_ui_panel = None
        self._ui_rt = None
        self.scene_content_type = None
        self.is_hdr_enable = None
        self._notify_loading_ui = notify_loading_ui
        self._gen_landscape_diffuse = None
        self.had_load_l2 = False
        self.load_l2_second_time = False
        self.save_enable_shadow = None
        self.load_parts()
        self.init_loading(back_load)
        print('load scene id', id(self), scene_type)
        self.camera_move_enable = True
        self.viewer_position = math3d.vector(0, 0, 0)
        self.view_range = 100
        self.tick_cnt = 0
        self.dynamic_preload_dist_level = 0
        self.create_camera(True)
        self.preload_model_names = []
        self.breakable_hp_obj = {}
        self.model_prefix_info = {}
        self.model_to_hide = set([])
        self.model_enable_lightmap = set([])
        self.model_enable_preload_visible = set([])
        self.track_cache = {}
        self.fish_eye_scalars = [
         1.0, 1.0]
        self.smooth_outline_pp_info = {}
        self.hero_outline_pp_info = {}
        self.detector_outline_pp_info = {}
        global_data.display_agent.set_longtime_post_process_active('smooth_outline', False)
        self.collision_check_count = 0
        self.refresh_camera_follow_target_pos_flag = 0
        self.camera_follow_target_pos_refreshed_count = 0
        self.camera_follow_target_pos_refreshed_ret = None
        self.preload_check_count = 0
        self._touch_move_vec = None
        self._touch_move_pos = None
        game.on_chunk_loaded = self.on_chunk_loaded
        if self.ENABLE_PRELOAD_DYNAMIC:
            self.enable_preload_dynamic(True)
            if hasattr(self, 'enable_preload_dynamic_by_chunk'):
                if global_data.feature_mgr.is_support_preload_lod():
                    print('scene.enable_preload_dynamic_by_chunk = False, Use new preload lod.')
                    self.enable_preload_dynamic_by_chunk(False)
                else:
                    print('scene.enable_preload_dynamic_by_chunk = True')
                    self.enable_preload_dynamic_by_chunk(True)
            for name in self.PRELOAD_DYNAMIC_EXCLUDE_MODELS:
                self.add_preload_dynamic_exclude(name)

            self.set_preload_dynamic_level(1)
        self._is_waiting_to_load_scene = True
        self.support_impostor_lod = global_data.feature_mgr.is_support_impostor()
        self.is_fix_impostor_bug = global_data.feature_mgr.is_fix_impostor_bug()
        if force_sync:
            self.load_scene(callback, async_load, back_load)
        else:
            global_data.game_mgr.next_exec(lambda : self.load_scene(callback, async_load, back_load))
        self.cur_chunks = set([])
        self.impostor_detect_cnt = 0
        self.refresh_mirror_enable()
        self._sky_light_scale = 1.0
        self._indirect_light_scale = 1.0
        self._enable_lightmap_thres = True
        return

    def init_loading(self, back_load):
        self.loading_wrapper = loadwrapper.LoadingWrapper(self._notify_loading_ui)
        self.loading_wrapper.init_from_dict({'use_loading_ui': self._get_scene_data('use_loading_ui', True),
           'loading_images': back_load or self._get_scene_data('loading_images', []) if 1 else [],
           'is_battle': self._get_scene_data('is_battle', False),
           'group_data': self._get_scene_data('group_data', None),
           'map_id': self._get_scene_data('map_id', 0)
           })
        if not global_data.is_32bit:
            self._init_preload_data()
        return

    def do_set_viewer_position(self, pos, delay=True):
        self._temp_viewer_pos = pos
        if not delay:
            self.update_viewer_pos()

    def update_viewer_pos(self):
        if self._temp_viewer_pos is not None:
            self.viewer_position = self._temp_viewer_pos
            self._temp_viewer_pos = None
        return

    def is_kongdao(self):
        return self.scene_name == BATTLE_SCENE_KONGDAO

    def is_normal(self):
        return self.scene_name == BATTLE_SCENE_NORMAL

    def init_scene_info(self, scene_type, scene_data, callback):
        self.is_exit_destroy = False
        self._temp_viewer_pos = None
        self.valid = True
        self._listenerkey = 'Scene{0}'.format(id(self))
        self.scene_type = scene_type
        self.scene_conf = confmgr.get('scenes', scene_type)
        self.scene_data = {} if scene_data is None else scene_data
        self.scene_name = self.scene_data.get('scene_name', BATTLE_SCENE_NORMAL)
        self.has_landscape = not (self.scene_name in INVALID_LANDSCAPE_SCENE or self.scene_name.startswith('pve'))
        is_test = False
        if scene_type in ('Test', 'TestFly', 'TestSimple', 'SkinDefineTest'):
            is_test = True
        if self.scene_conf and self.scene_conf.get('test', False):
            is_test = True
        if is_test:
            global_data.game_mgr.init_ingame_env()
        guofu_scene_dict = {'scene/jiemain_mingwen/jijia_mingwen.scn': 'scene/jijia_mingwen_01/jijia_mingwen_01.scn'
           }
        if global_data.is_ue_model and self.scene_data.get('scene_path'):
            scene_path = guofu_scene_dict.get(self.scene_data['scene_path'], self.scene_data['scene_path'])
            self.scene_data['scene_path'] = scene_path
        if self.scene_type == 'Traning' and global_data.custon_battle_scene:
            self.scene_data['scene_path'] = global_data.custon_battle_scene
        self._loaded = False
        self._last_click_time = 0
        self._touches_distance = None
        self.loading_callback = lambda _: global_data.emgr.scene_chunk_loaded_event.emit()
        self.parts = {}
        self.update_part_list = set()
        self._player = None
        self._prev_touch_move = []
        self._prev_touch_size = 3
        self._overlap_check_info = {}
        self._preload_check_info = {}
        if global_data.gsetting:
            global_data.gsetting.set_in_pve_scene(self.is_pve_scene())
        import os
        scene_dir = os.path.dirname(self._get_scene_data('scene_path', ''))
        scene_overlap_file = os.path.join(scene_dir, 'scene_config', 'scene_overlap_info.json').replace('\\', '/')
        if C_file.find_res_file(scene_overlap_file, ''):
            self._overlap_check_info = json.loads(C_file.get_res_file(scene_overlap_file, ''))
        preload_overlap_file = os.path.join(scene_dir, 'scene_config', 'preload_overlap_info.json').replace('\\', '/')
        if C_file.find_res_file(preload_overlap_file, ''):
            self._preload_check_info = json.loads(C_file.get_res_file(preload_overlap_file, ''))
        self.init_event()
        return

    def set_preload_dynamic_args(self, extend_dist, always_y_min):
        if not self.ENABLE_PRELOAD_DYNAMIC:
            return
        if global_data.feature_mgr.is_support_preload_lod():
            extend_dist = global_data.preload_extend_dist_for_new_lod
            always_y_min = global_data.preload_alway_y_min_for_new_lod
        global_data.cur_preload_extend_dist = extend_dist
        global_data.cur_preload_alway_y_min = always_y_min
        self.set_preload_dynamic_info(global_data.preload_dynamic_check_tick, extend_dist, always_y_min)
        print('[DYNAMIC PRELOAD] set_preload_dynamic_args: extend_dist:%s, always_y_min:%s' % (extend_dist, always_y_min))

    def set_preload_dynamic_level(self, level):
        if level == self.dynamic_preload_dist_level:
            return
        self.dynamic_preload_dist_level = level
        if global_data.is_low_mem_mode or global_data.is_low_perf_mode:
            self.set_preload_dynamic_args(global_data.preload_extend_dist_low, global_data.preload_alway_y_min_low)
        elif level == 1:
            self.set_preload_dynamic_args(global_data.preload_extend_dist_normal, global_data.preload_alway_y_min_normal)
        elif level == 2:
            self.set_preload_dynamic_args(global_data.preload_extend_dist_high, global_data.preload_alway_y_min_high)
        else:
            print('ERROR: wrong dynamic_preload_level:%s' % level)

    def __str__(self):
        path = self._get_scene_data('scene_path')
        return '{{Scene:{},{},{}}}'.format(self.scene_type, id(self), path)

    def _init_preload_data(self):
        import logic.gcommon.common_const.preload_data_const as PDC
        for json_path in PDC.PRELOAD_JSON_DATA:
            confmgr.get(json_path)

        for py_path in PDC.PRELOAD_PY_DATA:
            __import__(py_path, fromlist=[''])

        if global_data.uisystem:
            for ui_json_path in PDC.PRELOAD_UI_JSON_DATA:
                global_data.uisystem.load_template(ui_json_path)

    def reset_data(self):
        self.valid = False
        self.unbind_event()
        self.scene_data = {}
        self.scene_conf = {}
        self._player = None
        self.parts = {}
        self.update_part_list = set()
        self._objects = None
        self.loading_callback = None
        self.cancel_hdr_timer()
        self.cur_hdr_val = 1.0
        self.model_prefix_info = {}
        self._check_logic = None
        self.refresh_camera_follow_target_pos_flag = 0
        self.camera_follow_target_pos_refreshed_count = 0
        self.camera_follow_target_pos_refreshed_ret = None
        return

    def reinit_scene(self, scene_type, scene_data, callback):
        if self.parts:
            log_error('Try to reinit a unrelease scene!!!!')
        self.reset_data()
        self.init_scene_info(scene_type, scene_data, callback)
        self.load_parts()
        self.loading_wrapper = loadwrapper.LoadingWrapper(self._notify_loading_ui)
        self.loading_wrapper.init_from_dict({'use_loading_ui': self._get_scene_data('use_loading_ui', True),
           'loading_images': self._get_scene_data('loading_images', [])
           })
        self._on_before_load()
        self._on_pre_enter()
        for cname, com in six.iteritems(self.parts):
            com.on_load()

        self.on_enter()
        if callback:
            callback()

        def close_loadingui():
            self.loading_wrapper = None
            return

        self.loading_wrapper.preload_resource(close_loadingui, self, [], [])

    def destroy(self):
        if not self.valid:
            return
        else:
            if self._loaded:
                raise Exception('destroy without calling scene.on_exit()')
            if self._gen_landscape_diffuse:
                self._gen_landscape_diffuse.destroy()
            self._gen_landscape_diffuse = None
            if not self.is_exit_destroy and self._is_waiting_to_load_scene:
                import traceback
                error_content = 'destroy in the same frame of create. scene_type:%s, scene_path:%s, scene_data:%s\n' % (self.get_type(), self.get_scene_path(), self.scene_data)
                error_content += '\n'.join(traceback.format_stack())
                exception_hook.post_error(error_content)
            self.reset_data()
            super(Scene, self).destroy()
            resloader.clear_cache()
            global_data.sfx_mgr.clean_up_invalid()
            global_data.model_mgr.clean_up_invalid()
            for name, panel in six.iteritems(self._ui_panels):
                panel.release()

            self._ui_panels = {}
            self._cur_ui_panel = None
            if self._ui_rt:
                self._ui_rt.destroy()
            self._ui_rt = None
            return

    def in_which_trunk(self, pos, trunk_size=DEFAULT_CHUNK_SIZE):
        inv_chunk_size = 1.0 / trunk_size
        x = int(math.floor(pos.x * inv_chunk_size + 0.5))
        z = int(math.floor(pos.z * inv_chunk_size + 0.5))
        return (
         x, z)

    def on_chunk_loaded(self, *args):
        chunk_name = ''
        x = 0
        z = 0
        if len(args) == 2:
            x, z = args
        elif len(args) == 3:
            chunk_name, x, z = args
        else:
            print('on_chunk_loaded error.........', args)
            return
        self.process_models_in_chunk(chunk_name, x, z)
        if not self.support_impostor_lod and chunk_name.startswith('l2'):
            self.hide_impostors()
        if chunk_name.startswith('l2'):
            self.had_load_l2 = True
        elif not chunk_name.startswith('l') and self.had_load_l2:
            self.load_l2_second_time = True

    def get_type(self):
        return self.scene_type

    def is_same_scene(self, scene_type, scene_data):
        if self.scene_type != scene_type:
            return False
        return self.is_same_scene_path(scene_data)

    def get_scene_path(self):
        return self.scene_data.get('scene_path', None)

    def is_same_scene_path(self, scene_data):
        scene_path = scene_data.get('scene_path', None)
        if scene_path:
            return scene_path == self._get_scene_data('scene_path', None)
        else:
            return False

    def _get_scene_data(self, key, default=None):
        return self.scene_data.get(key, self.scene_conf.get(key, default))

    def get_scene_data(self, key, default=None):
        return self.scene_data.get(key, self.scene_conf.get(key, default))

    def load_scene(self, callback=None, async_load=True, back_load=False):
        if not self.valid:
            return
        else:

            def _load_finish_cb():
                self.refresh_mirror_enable()
                self.loading_wrapper = None
                if not self.valid:
                    return
                else:
                    for cname, com in six.iteritems(self.parts):
                        com.on_load()

                    if back_load:
                        self._loaded = True
                        self.logic(0.1)
                        self.post_logic(0.1)
                        self._loaded = False
                    elif self.scene_data.get('preload_cockpit', False):
                        global_data.emgr.start_preload_cockpit.emit()
                    else:
                        self.on_enter()
                    if callback:
                        callback()
                    return

            self._is_waiting_to_load_scene = False
            if global_data.gsetting:
                global_data.gsetting.reset_lodoffset()
            lod_mem_str = '1' if global_data.is_low_mem_mode else '0'
            self.set_macros({'IS_LOW_MEM_MODE': lod_mem_str})
            if self.is_battle_scene():
                self.battle_res_prepare()
                self.set_macros({'IS_IN_BATTLE': '1'})
            else:
                self.set_macros({'IS_IN_BATTLE': '0'})
            if pc_platform_utils.is_pc_hight_quality():
                self.set_macros({'IS_PC_PLATFORM': '1'})
            if global_data.is_ue_model and global_data.game_mode:
                self.set_macros({'ENV_TYPE': str(global_data.game_mode.get_shader_env_type())})
            self.load_detail(self._get_scene_data('scene_detail', True))
            scn_path = self._get_scene_data('scene_path', None)
            async_load = self._get_scene_data('async_load', async_load)
            if scn_path is None:
                self._on_before_load()
                self._on_pre_enter()
                _load_finish_cb()
                return
            self._on_before_load()
            if 'scene/test_display_01/test_display_01.scn' == scn_path:
                async_load = False
            self.async_load = async_load
            is_suc, layer_id = self.load(scn_path, None, async_load)
            self.enable_lod_chunk = global_data.enable_scn_lod_chunk
            self.viewer_position = math3d.vector(*self._get_scene_data('view_position', (0,
                                                                                         0,
                                                                                         0)))
            self.active_camera.world_position = self.viewer_position
            if self.landscape:
                self.landscape.set_LandscapeViewRange(100000)
                if hasattr(self.landscape, 'enable_vertex_half') and game3d.get_platform() != game3d.PLATFORM_WIN32:
                    enable_landscape_patch_vertex_half = global_data.enable_landscape_patch_vertex_half
                    enable_landscape_detail_vertex_half = global_data.enable_landscape_detail_vertex_half
                    if global_data.debug_perf_switch_global:
                        enable_landscape_patch_vertex_half = global_data.get_debug_perf_val('enable_vertex_half', enable_landscape_patch_vertex_half)
                        enable_landscape_detail_vertex_half = global_data.get_debug_perf_val('enable_vertex_half', enable_landscape_detail_vertex_half)
                    self.landscape.enable_vertex_half(enable_landscape_patch_vertex_half, enable_landscape_detail_vertex_half)
                if global_data.debug_perf_switch_global:
                    if hasattr(self.landscape, 'enable_render'):
                        switch = global_data.get_debug_perf_val('enable_landscape_render', True)
                        self.landscape.enable_render(switch)
            elif is_artist_package():
                self.view_range = 10000
            self._on_pre_enter()
            import os.path
            scn_file = os.path.splitext(scn_path)[0]
            nav_file = '{0}.nav'.format(scn_file)
            if C_file.find_res_file(nav_file, ''):
                self.load_detour(nav_file)
            gims = resloader.get_preload_gims()
            gims.extend(self._get_scene_data('preload_gims', []))
            gims.extend(resloader.get_preload_sfxs())
            texs = self._get_scene_data('preload_textures', [])
            need_warmup = False
            need_preload_effect = False
            self.loading_wrapper.preload_resource(_load_finish_cb, self, gims, texs, need_warmup=need_warmup, preload_effect_cache=need_preload_effect)
            resloader.clear_preload_list()
            self.gctest = GCTest(self)
            if global_data.inner_debug_soc:
                if global_data.inner_debug_soc_tag and self.is_kongdao():
                    self.set_software_rasterization_culling_enable(True, True, False)
                    self.set_software_rasterization_culling_lodmodels_enable(True)
            elif global_data.use_soc and self.is_kongdao():
                self.set_software_rasterization_culling_lodmodels_enable(False)
            return

    def start_gen_landscape_diffuse(self):
        import render
        from logic.gutils.GenLandscapeDiffuse import GenLandscapeDiffuse
        _, _, _, _, gpu_desc, gpu_driver = render.get_adapter_info()
        if True:
            self._gen_landscape_diffuse = GenLandscapeDiffuse()
            self._gen_landscape_diffuse.start()

    def modify_view_range_to_default(self):
        self.modify_view_range(self._get_scene_data('view_range', 300), False, True)

    def modify_view_range(self, view_range, force=False, skip_check=False):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        import logic.vscene.global_display_setting as gds
        if hasattr(world, 'is_async_scene_loader_use_g93_mode'):
            is_use_g93_mode = world.is_async_scene_loader_use_g93_mode()
        else:
            is_use_g93_mode = False
        if global_data.enable_parachute_view_range_optimize:
            if self.scene_type in (scene_const.SCENE_TRANING,):
                if global_data.player and global_data.player.logic:
                    parachute_stage = global_data.player.logic.share_data.ref_parachute_stage
                    if parachute_stage in (parachute_utils.STAGE_NONE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_PLANE, parachute_utils.STAGE_LAUNCH_PREPARE):
                        print('modify_view_range with player to minimize for scene_training..........')
                        self.set_view_range(0, 1)
                        self.set_view_range(1, 1)
                        self.set_view_range(2, 1)
                        update_view_range_3(self)
                        return
                    print('modify_view_range with player to normal for scene_training..........')
                else:
                    if not skip_check:
                        print('modify_view_range to minimize for scene_training..........')
                        self.set_view_range(0, 1)
                        self.set_view_range(1, 1)
                        self.set_view_range(2, 1)
                        update_view_range_3(self)
                        return
                    print('modify_view_range to normal for scene_training..........')
        if global_data.game_mode:
            game_mode_id = game_mode_const.GAME_MODE_INDEX_MAP.get(global_data.game_mode.get_mode_type(), battle_const.PLAY_TYPE_DEATH)
        else:
            game_mode_id = battle_const.PLAY_TYPE_DEATH
        conf = confmgr.get('scene_lod_config', str(game_mode_id))
        if conf:
            if global_data.is_low_mem_mode:
                device_type = game_mode_const.DEVICE_TYPE_LOW_MEM
            elif pc_platform_utils.is_pc_hight_quality():
                device_type = game_mode_const.DEVICE_TYPE_PC
            else:
                device_type = game_mode_const.DEVICE_TYPE_MOBILE
            ds = gds.GlobalDisplaySeting()
            quality = ds.get_actual_quality()
            fix_key = game_mode_const.SCENE_LOD_MAP.get((device_type, quality), 'cSuperLowMobile')
            game_mode_view_range_fix = conf[fix_key]
        else:
            game_mode_view_range_fix = (1.0, 1.0, 1.0)
        if is_use_g93_mode:
            range_modes = (view_range * 0.85 * game_mode_view_range_fix[0],
             view_range * 1.8 * game_mode_view_range_fix[1],
             view_range * 2.6 * game_mode_view_range_fix[2])
            if force or abs(self.view_range - range_modes[0]) > 1:
                print('scene game_mode_view_range_fix:%s, range_modes:%s....' % (game_mode_view_range_fix, range_modes))
                self.set_view_range(0, range_modes[0])
                self.set_view_range(1, range_modes[1])
                self.set_view_range(2, range_modes[2])
                update_view_range_3(self)
        elif force or self.view_range != view_range:
            self.set_view_range(0, view_range)
            if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS) and global_data.game_mode.get_mode_type() != game_mode_const.GAME_MODE_SNIPE:
                self.set_view_range(1, min(view_range * 4, 600.0 * NEOX_UNIT_SCALE))
                self.set_view_range(2, min(view_range * 8, 600.0 * NEOX_UNIT_SCALE))
            else:
                self.set_view_range(1, view_range * 4)
                self.set_view_range(2, view_range * 8)
                update_view_range_3(self)

    def is_loaded(self):
        return self._loaded

    def init_event(self):
        einfo = {}
        for event_name, func_name in six.iteritems(self.ECONF):
            einfo[event_name] = getattr(self, func_name)

        emgr = global_data.emgr
        emgr.bind_events(einfo)

    def unbind_event(self):
        einfo = {}
        for event_name, func_name in six.iteritems(self.ECONF):
            einfo[event_name] = getattr(self, func_name)

        emgr = global_data.emgr
        emgr.unbind_events(einfo)

    def refresh_mirror_enable(self, quality=None):
        mirror_model = self.get_model('shangcheng_jingzi_01')
        if global_data.is_32bit:
            mirror_reflect = False
            if mirror_model:
                mirror_model.visible = False
        else:
            if not global_data.is_ue_model:
                return
            if mirror_model:
                if quality is None:
                    mirror_reflect = global_data.game_mgr.gds.get_actual_quality() > 1
                else:
                    mirror_reflect = quality > 1
            else:
                mirror_reflect = False
        if global_data.feature_mgr.is_support_scene_mirror_enable():
            self.mirror_enable = mirror_reflect
        return

    def on_display_quality_change(self, quality):
        self.refresh_mirror_enable(quality)

    def _on_before_load(self):
        import logic.vscene.global_display_setting as gds
        ds = gds.GlobalDisplaySeting()
        ds.set_default_quality_to_high(self._get_scene_data('high_quality_tex', False))
        ds.process_low_device_settings()
        ds.apply_shader_lod(self, self._get_scene_data('display_tag', False))
        for cname, com in six.iteritems(self.parts):
            com.on_before_load()

        if hasattr(world, 'remove_empty_async_loader_cached_item'):
            world.remove_empty_async_loader_cached_item(world.RES_TYPE_MESH)
            world.remove_empty_async_loader_cached_item(world.RES_TYPE_SKELANIM)
        if is_win32() and global_data.is_neox_editor:
            self.set_macros({'NEOX_EDITOR': '1'})
            self.set_global_uniform('DebugDrawModeFloat', global_data.debug_draw_model_value)
        self.set_macros({'ASTC_ON': '1' if device_compatibility.is_support_astc() else '0'
           })
        if self.scene_type in scene_const.DISPLAY_SCENES_LIST:
            self.set_macros({'ENABLE_RIM_NOL': '0'})

    def _on_pre_enter--- This code section failed: ---

 940       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'feature_mgr'
           6  LOAD_ATTR             2  'is_async_loader_g93_mode_ready'
           9  CALL_FUNCTION_0       0 
          12  POP_JUMP_IF_FALSE    31  'to 31'

 941      15  LOAD_GLOBAL           3  'world'
          18  LOAD_ATTR             4  'set_async_scene_loader_use_g93_mode'
          21  LOAD_GLOBAL           5  'True'
          24  CALL_FUNCTION_1       1 
          27  POP_TOP          
          28  JUMP_FORWARD         31  'to 62'

 942      31  LOAD_GLOBAL           6  'hasattr'
          34  LOAD_GLOBAL           3  'world'
          37  LOAD_CONST            1  'set_async_scene_loader_use_g93_mode'
          40  CALL_FUNCTION_2       2 
          43  POP_JUMP_IF_FALSE    62  'to 62'

 943      46  LOAD_GLOBAL           3  'world'
          49  LOAD_ATTR             4  'set_async_scene_loader_use_g93_mode'
          52  LOAD_GLOBAL           7  'False'
          55  CALL_FUNCTION_1       1 
          58  POP_TOP          
          59  JUMP_FORWARD          0  'to 62'
        62_0  COME_FROM                '59'
        62_1  COME_FROM                '28'

 945      62  LOAD_FAST             0  'self'
          65  LOAD_ATTR             8  'landscape'
          68  POP_JUMP_IF_FALSE   137  'to 137'

 946      71  LOAD_GLOBAL           0  'global_data'
          74  LOAD_ATTR             1  'feature_mgr'
          77  LOAD_ATTR             9  'is_new_landscape_detail_ready'
          80  CALL_FUNCTION_0       0 
          83  POP_JUMP_IF_FALSE   101  'to 101'

 947      86  LOAD_GLOBAL           5  'True'
          89  LOAD_FAST             0  'self'
          92  LOAD_ATTR             8  'landscape'
          95  STORE_ATTR           10  'use_new_detail'
          98  JUMP_ABSOLUTE       137  'to 137'

 948     101  LOAD_GLOBAL           6  'hasattr'
         104  LOAD_FAST             0  'self'
         107  LOAD_ATTR             8  'landscape'
         110  LOAD_CONST            2  'use_new_detail'
         113  CALL_FUNCTION_2       2 
         116  POP_JUMP_IF_FALSE   137  'to 137'

 949     119  LOAD_GLOBAL           7  'False'
         122  LOAD_FAST             0  'self'
         125  LOAD_ATTR             8  'landscape'
         128  STORE_ATTR           10  'use_new_detail'
         131  JUMP_ABSOLUTE       137  'to 137'
         134  JUMP_FORWARD          0  'to 137'
       137_0  COME_FROM                '134'

 951     137  LOAD_GLOBAL           0  'global_data'
         140  LOAD_ATTR             1  'feature_mgr'
         143  LOAD_ATTR            11  'is_road_async_batching_ready'
         146  CALL_FUNCTION_0       0 
         149  POP_JUMP_IF_FALSE   164  'to 164'

 952     152  LOAD_GLOBAL           5  'True'
         155  LOAD_FAST             0  'self'
         158  STORE_ATTR           12  'road_use_async_batching'
         161  JUMP_FORWARD         24  'to 188'

 953     164  LOAD_GLOBAL           6  'hasattr'
         167  LOAD_GLOBAL           3  'world'
         170  CALL_FUNCTION_2       2 
         173  POP_JUMP_IF_FALSE   188  'to 188'

 954     176  LOAD_GLOBAL           7  'False'
         179  LOAD_FAST             0  'self'
         182  STORE_ATTR           12  'road_use_async_batching'
         185  JUMP_FORWARD          0  'to 188'
       188_0  COME_FROM                '185'
       188_1  COME_FROM                '161'

 957     188  SETUP_LOOP           42  'to 233'
         191  LOAD_GLOBAL          13  'six'
         194  LOAD_ATTR            14  'iteritems'
         197  LOAD_FAST             0  'self'
         200  LOAD_ATTR            15  'parts'
         203  CALL_FUNCTION_1       1 
         206  GET_ITER         
         207  FOR_ITER             22  'to 232'
         210  UNPACK_SEQUENCE_2     2 
         213  STORE_FAST            1  'cname'
         216  STORE_FAST            2  'com'

 958     219  LOAD_FAST             2  'com'
         222  LOAD_ATTR            16  'on_pre_load'
         225  CALL_FUNCTION_0       0 
         228  POP_TOP          
         229  JUMP_BACK           207  'to 207'
         232  POP_BLOCK        
       233_0  COME_FROM                '188'

 960     233  LOAD_FAST             0  'self'
         236  LOAD_ATTR            17  '_get_scene_data'
         239  LOAD_CONST            4  'display_setting'
         242  LOAD_GLOBAL           5  'True'
         245  CALL_FUNCTION_2       2 
         248  STORE_FAST            3  'display_setting'

 961     251  LOAD_FAST             3  'display_setting'
         254  POP_JUMP_IF_FALSE   273  'to 273'

 962     257  LOAD_FAST             0  'self'
         260  LOAD_ATTR            18  '_setup_global_display'
         263  LOAD_GLOBAL           7  'False'
         266  CALL_FUNCTION_1       1 
         269  POP_TOP          
         270  JUMP_FORWARD         25  'to 298'

 964     273  LOAD_FAST             0  'self'
         276  LOAD_ATTR            19  'modify_view_range'
         279  LOAD_FAST             0  'self'
         282  LOAD_ATTR            17  '_get_scene_data'
         285  LOAD_CONST            5  'view_range'
         288  LOAD_CONST            6  300
         291  CALL_FUNCTION_2       2 
         294  CALL_FUNCTION_1       1 
         297  POP_TOP          
       298_0  COME_FROM                '270'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 170

    def on_enter(self):
        print('Mjy on enter scene', self.scene_type, id(self))
        self._loaded = True
        if self.scene_col:
            from logic.gcommon.const import NEOX_UNIT_SCALE
            self.scene_col.gravity = math3d.vector(0, -9.8 * NEOX_UNIT_SCALE * 2, 0)
        global_data.display_agent.do_check_reset_resolution()
        for com in six.itervalues(self.parts):
            com.enter()

        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.register_touch_event(self._listenerkey, (self.on_touch_begin, self.on_touch_move, self.on_touch_end, self.on_touch_end))
        touch_mgr.register_wheel_event(self._listenerkey, self.on_mouse_wheel)
        self.logic(0.1)
        self.post_logic(0.1)
        global_data.emgr.fireEvent('scene_after_enter_event')
        self.preload_model_names = self.get_preload_names()
        global_data.uisystem.RecordUsedSpritePaths()
        import cc
        cc.Director.getInstance().purgeCachedData()
        display_setting = self._get_scene_data('display_setting', True)
        if display_setting:
            self._setup_global_display(True)
        if is_in_lobby(self.scene_type):
            world.set_skeleton_distances(1000000, 10000000)
        else:
            world.set_skeleton_distances(SKELETON_LOD_DIST[0], SKELETON_LOD_DIST[1])
        self.process_models_in_single_scene()
        print('Mjy finished enter scene', self.scene_type, id(self))

    def apply_global_display_setting(self):
        display_setting = self._get_scene_data('display_setting', True)
        if display_setting:
            self._setup_global_display(True)

    def is_battle_scene(self):
        return self.scene_type in scene_const.BATTLE_SCENE_TYPES

    def is_pve_scene(self):
        return self.scene_type == scene_const.SCENE_PVE

    def on_exit(self):
        if game.on_chunk_loaded and game.on_chunk_loaded == self.on_chunk_loaded:
            game.on_chunk_loaded = None
        global_data.emgr.fireEvent('scene_before_exit_event')
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.unregister_touch_event(self._listenerkey)
        touch_mgr.unregister_wheel_event(self._listenerkey)
        if global_data.human_fire_keyboard_mgr:
            global_data.human_fire_keyboard_mgr.stop_shot()
        if self.loading_wrapper:
            self.loading_wrapper.loading_cancel()
            self.loading_wrapper = None
        self.recover_effects()
        from cocosui import ccs
        ccs.ActionManagerEx.getInstance().releaseActions()
        resloader.clear_cache()
        resloader.stop_async_res()
        if global_data.camera_state_pool:
            global_data.camera_state_pool.clear()
        if global_data.ui_pool:
            global_data.ui_pool.clear()
        if global_data.is_low_mem_mode:
            ui_utils.clear_ui_all_cache()
        self.breakable_hp_obj = {}
        self.model_prefix_info = {}
        self.model_to_hide = set([])
        self.model_enable_lightmap = set([])
        self.model_enable_preload_visible = set([])
        self.smooth_outline_pp_info = {}
        self.hero_outline_pp_info = {}
        self.detector_outline_pp_info = {}
        for com in six.itervalues(self.parts):
            com.exit()

        for com in six.itervalues(self.parts):
            com.after_exit()

        if self.is_battle_scene():
            global_data.game_mode and global_data.game_mode.finalize()
            global_data.cam_data and global_data.cam_data.finalize()
        if self.parts:
            del com
        part_types = six_ex.keys(self.parts)
        self.parts = {}
        self.update_part_list = set()
        self._loaded = False
        if self.check_leak(part_types) and ENABLE_CHECK_LEAK:
            raise Exception('LEAK!!!!!!!!! Check the log above!')
        return

    def on_pause(self, flag):
        for com in six.itervalues(self.parts):
            com.pause(flag)

        touch_mgr = global_data.touch_mgr_agent
        if flag:
            touch_mgr.unregister_touch_event(self._listenerkey)
            touch_mgr.unregister_wheel_event(self._listenerkey)
            self.setup_realtime_shadow_light(False)
        else:
            touch_mgr.register_touch_event(self._listenerkey, (self.on_touch_begin, self.on_touch_move, self.on_touch_end, self.on_touch_end))
            touch_mgr.register_wheel_event(self._listenerkey, self.on_mouse_wheel)
            self.setup_realtime_shadow_light()
            self.reset_bloom()
            self.reset_tonemapping()
        self.recover_effects()

    def check_leak(self, part_types):
        if not ENABLE_CHECK_LEAK or not is_win32():
            return False
        import gc
        gc.collect()
        import objgraph
        has_leak = False
        for part_type in part_types:
            ret = objgraph.by_type(part_type)
            if ret:
                log_error('LEAK Scene Part:{}'.format(part_type))
                has_leak = True
                refs = gc.get_referrers(ret[0])
                for ref in refs:
                    log_error('\tLEAK Refference {}'.format(ret))
                    parent_refs = gc.get_referrers(ret)
                    for pr in parent_refs:
                        log_error('\t\tLEAK Refference {}'.format(pr))

        return has_leak

    def get_com(self, name):
        com = self.parts.get(name, None)
        return com

    def get_sub_sys(self, com_name, sys_name):
        com = self.get_com(com_name)
        if not com:
            return None
        else:
            return com._sub_sys.get(sys_name, None)

    def post_logic(self, dt):
        if not self._loaded:
            return

    def py_render(self, dt):
        if not self._loaded:
            return

    def set_player(self, player):
        if self._player == player:
            return
        else:
            self._player = player
            global_data.emgr.fireEvent('scene_player_setted_event', player)
            if global_data.is_debug_mode and global_data.is_animator_debug:
                from common.animate import animator
                if player:
                    control_target = player.ev_g_control_target()
                    from logic.gutils.client_unit_tag_utils import preregistered_tags
                    if control_target and control_target.logic.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
                        animator.Player = control_target.logic.get_com('ComMechaModel')
                    else:
                        animator.Player = player.get_com('ComHumanAppearance')
                else:
                    animator.Player = None
            return

    def get_player(self):
        return self._player

    def recover_effects(self):
        global_data.game_mgr.set_global_speed_rate(1)
        for pp in ['gaussian_blur', 'radial_blur', 'gray', 'screen_filter']:
            global_data.display_agent.set_longtime_post_process_active(pp, False)

    def load_detour(self, nav_file):
        if self.scene_detour.add_mesh(self.DETOUR_MESH):
            self.scene_detour.load_mesh(self.DETOUR_MESH, nav_file)
            self.is_detour_enable = True
        else:
            print('[ERROR] load detour file failed:', nav_file)
            self.is_detour_enable = False

    def detour_height(self, x, z):
        return self.scene_detour.get_height(self.DETOUR_MESH, x, z)

    def detour_path(self, pos_begin, pos_end):
        return self.scene_detour.get_path(self.DETOUR_MESH, pos_begin, pos_end, 256)

    def detour_cast(self, pos_begin, pos_end):
        return self.scene_detour.ray_cast(self.DETOUR_MESH, pos_begin, pos_end)

    def fix_logic(self, dt=1 / 30.0):
        if not self._loaded:
            return
        else:
            if self._touch_move_vec is not None:
                dx = self._touch_move_vec.x
                dy = self._touch_move_vec.y
                for com in six.itervalues(self.parts):
                    try:
                        com.on_touch_slide(dx, dy, None, self._touch_move_pos)
                    except:
                        traceback_uploader()

                self._touch_move_vec = None
                self._touch_move_pos = None
            return

    def logic(self, dt=1 / 30.0):
        self.tick_cnt += 1
        if not self._loaded:
            return
        self.update_viewer_pos()
        self.update_parts(dt)
        if self._check_logic:
            self._check_logic()
        if self.ENABLE_PRELOAD_MODEL_SHADOWMAP:
            self._preload_shadowmap_process()
        self._process_dynamic_load_by_height()
        self.show_impostors()
        self.fix_impostors_bug()

    def _process_dynamic_load_by_height(self):
        target = global_data.cam_lctarget
        if not target:
            self.set_preload_dynamic_level(1)
            return
        pos = target.ev_g_position()
        if not pos:
            return
        if target.share_data.ref_parachute_stage not in (parachute_utils.STAGE_LAND, parachute_utils.STAGE_FREE_DROP, parachute_utils.STAGE_PARACHUTE_DROP):
            return
        if pos.y > global_data.preload_dynamic_change_height:
            self.set_preload_dynamic_level(2)
        else:
            self.set_preload_dynamic_level(1)

    def update_parts(self, dt):
        update_list = self.update_part_list
        update_list_clone = list(self.update_part_list)
        for part in update_list_clone:
            try:
                ret = part.on_update(dt)
            except:
                traceback_uploader()
                ret = None

            if ret == part.REMOVE_UPDATE_AFTER_LOOP:
                update_list.remove(part)

        return

    def load_parts(self):
        import logic.vscene.parts.factory as factory
        config_coms = self.scene_conf.get('coms', [])
        for com_type in config_coms:
            print(factory.load_com(self, com_type))

    def _preload_shadowmap_process(self):
        camera = self.active_camera
        if not camera:
            return
        pos = camera.world_position
        for model_name in self.preload_model_names:
            model = self.get_model(model_name)
            if not (model and model.valid):
                continue
            is_chunk_visible = self._check_preload_model_visibility(model, pos)
            if is_chunk_visible:
                if model.name not in self.model_enable_lightmap:
                    if model.name not in self.EXCLUDE_SHADOWMAP_MODELS:
                        model.cast_shadow = True
                    self.model_enable_lightmap.add(model.name)
            elif model.name in self.model_enable_lightmap:
                model.cast_shadow = False
                self.model_enable_lightmap.discard(model.name)

    def _check_preload_model_visibility(self, m, player_pos):
        if not (m and m.valid):
            return False
        max_axis = max(max(m.bounding_box_w.x * 2.0, m.bounding_box_w.y * 2.0), m.bounding_box_w.z * 2.0) + global_data.cur_preload_extend_dist
        return (player_pos - m.center_w).length < max_axis

    def on_mouse_wheel(self, msg, delta, key_state):
        for com in six.itervalues(self.parts):
            com.on_mouse_wheel(msg, delta, key_state)

    def on_touch_begin(self, touches, event):
        if len(touches) == 1:
            self._prev_touch_move = []
        for com in six.itervalues(self.parts):
            com.on_touch_begin(touches)

    def on_touch_move(self, touches, event):
        len_touch = len(touches)
        if len_touch == 1:
            if not self.camera_move_enable:
                return
            delta = touches[0].getDelta()
            delta = math3d.vector2(delta.x, delta.y)
            length = delta.length
            if length == 0:
                return
                if self._prev_touch_move:
                    delta = self._prev_touch_move[-1]
                    delta.normalize()
                else:
                    return
            else:
                if self._prev_touch_move:
                    delta.normalize()
                    last_vec = self._prev_touch_move[-1]
                    last_vec.normalize()
                    if delta.dot(last_vec) >= 0:
                        delta = delta + last_vec * 0.5
                    delta.normalize()
                    delta = delta * length
                else:
                    delta.normalize()
                self._prev_touch_move.append(delta)
                if len(self._prev_touch_move) > self._prev_touch_size:
                    self._prev_touch_move = self._prev_touch_move[1:]
            self.on_touch_slide(delta.x, delta.y, touches)
        elif len_touch == 2:
            t0 = touches[0]
            t1 = touches[1]
            dis = t0.getLocation().distance(t1.getLocation())
            if not self._touches_distance:
                self._touches_distance = dis
            else:
                delta = dis - self._touches_distance
                self._touches_distance = dis
                self.on_touch_scale(delta, touches)

    def on_touch_end(self, touches, event):
        for com in six.itervalues(self.parts):
            com.on_touch_end(touches)

        len_touch = len(touches)
        if len_touch > 1:
            return
        t = touches[0]
        touch_end_location = t.getLocation()
        if t.getLocation().distance(t.getStartLocation()) < 10:
            import time
            cur_click_time = time.time()
            if cur_click_time - self._last_click_time < 0.5 and self.last_touch_end_location and touch_end_location.distance(self.last_touch_end_location) < 20:
                self.on_touch_doubletap(t)
            else:
                self.on_touch_tap(t)
            self._last_click_time = cur_click_time
        self.last_touch_end_location = touch_end_location

    def on_touch_slide(self, dx, dy, touches):
        if self._touch_move_vec:
            self._touch_move_vec += math3d.vector2(dx, dy)
        else:
            self._touch_move_vec = math3d.vector2(dx, dy)
        self._touch_move_pos = touches[0].getLocation()

    def on_touch_scale(self, delta, touches):
        for com in six.itervalues(self.parts):
            com.on_touch_scale(delta, touches)

    def on_touch_tap(self, touch):
        for com in six.itervalues(self.parts):
            com.on_touch_tap(touch)

    def on_touch_doubletap(self, touch):
        for com in six.itervalues(self.parts):
            com.on_touch_doubletap(touch)

    def pause(self):
        if self._is_pause:
            return
        self._is_pause = True

    def resume(self):
        if self._is_pause is False:
            return
        self._is_pause = False

    def hide_async_model(self, model_name):
        self.model_to_hide.add(model_name)

    def setup_display(self, posteffect=True):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        DEFAULT_COL_DIST = 300 * NEOX_UNIT_SCALE
        self.modify_view_range(self._get_scene_data('view_range', 300))
        self.setup_realtime_shadow_light()
        self._setup_landscape(display_setting.quality_value('LANDSCAPE_RANGE'), DEFAULT_COL_DIST)
        self._setup_vegetation()
        self._setup_fog()
        if posteffect:
            self._setup_posteffect()
        self.road_view_range_offset = 570
        self.set_lod_checkcount(20, 5)
        display_setting.set_scn_setup_inited(True)
        display_setting.set_default_quality_to_high(self._get_scene_data('high_quality_tex', False))
        if self._get_scene_data('high_quality_tex', False):
            display_setting.high_quality_tex_on()
        else:
            display_setting.high_quality_tex_off()

    def _setup_global_display(self, enable_pp):
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        display_setting.apply_scene_quality(self, enable_pp)

    def _setup_vegetation(self):
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        self.vegetation_far_density = 1.0
        self.vegetation_render_level = -7
        self.set_vegetation_visible_range(self.view_range * display_setting.quality_value('VEGETATION_RANGE'))
        self.vegetation_enable = display_setting.quality_value('VEGETATION_ENABLE')

    def recover_vegetation_enable(self):
        if global_data.game_mode.is_snow_res():
            self.vegetation_enable = False
        else:
            self.vegetation_enable = global_data.gsetting.quality_value('VEGETATION_ENABLE')

    def disable_vegetation(self):
        self.vegetation_enable = False
        print('==============disable_vegetation===================================')

    def force_setup_posteffect(self):
        self._setup_posteffect()

    def _setup_posteffect(self):
        import logic.vscene.global_display_setting as gds
        import device_compatibility
        display_setting = gds.GlobalDisplaySeting()
        if pc_platform_utils.is_pc_hight_quality() and global_data.is_ue_model:
            redirect_scale = global_data.gsetting.get_cur_redict_scale()
            global_data.display_agent.set_redirect_scale(redirect_scale)
            aa_level = global_data.gsetting.get_aa_level()
            global_data.display_agent.set_aa_level(aa_level)
        elif global_data.enable_shader_complexity_view:
            self.set_msaa(1)
        elif not device_compatibility.can_use_msaa():
            self.set_msaa(1)
        elif global_data.in_save_energy_mode:
            self.set_msaa(1)
        elif display_setting.is_posteffect_enable('msaa4x'):
            self.set_msaa(4)
        elif display_setting.is_posteffect_enable('msaa2x'):
            self.set_msaa(2)
        else:
            self.set_msaa(1)
        if global_data.in_save_energy_mode:
            from logic.gcommon.common_const.scene_const import SCENE_AR
            if self.scene_type != SCENE_AR:
                self.enable_hdr(False)
        elif display_setting.is_posteffect_enable('hdr') or self.scene_type == 'TestFly':
            self.enable_hdr(True)
        else:
            self.enable_hdr(False)
        global_data.emgr.set_up_posteffect.emit()

    def set_msaa(self, samples):
        if True:
            log_error('[IMPORTANT] TRYING SET FXAA TO %d, SCENE TYPE %s' % (samples, self.scene_type))
            active_scn = world.get_active_scene()
            if not self == active_scn:
                return
            if not is_in_lobby(self.scene_type):
                log_error('[IMPORTANT] NOT IN LOBBY, CHANGE FXAA TO 1')
                global_data.display_agent.set_msaa(1)
                return
            from logic.gcommon.common_const import ui_operation_const as uoc
            import logic.vscene.global_display_setting as gds
            display_setting = gds.GlobalDisplaySeting()
            quality_level = display_setting.get_actual_quality()
            if global_data.in_save_energy_mode:
                samples = 1
        if global_data.enable_shader_complexity_view:
            samples = 1
        global_data.display_agent.set_msaa(samples)

    @sync_exec
    def _setup_fog(self):
        if not self.valid:
            return
        else:
            import render
            import logic.vscene.global_display_setting as gds
            display_setting = gds.GlobalDisplaySeting()
            if not display_setting.quality_value('FOG_ENABLE'):
                print('Disable Fog in scene....')
                if global_data.is_ue_model:
                    self.enable_fog(False)
                else:
                    i_type, mode, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent = self.get_fog()
                    self.set_fog(i_type, render.RS_FOG_NONE, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent)
            else:
                conf_name = self._get_scene_data('fog_config')
                if global_data.is_ue_model:
                    if conf_name is None:
                        conf = None
                    else:
                        conf = confmgr.get('c_env_config', 'fog', conf_name, 'on_ground')
                elif conf_name is None or conf_name == 'default':
                    conf = None
                else:
                    conf = confmgr.get('c_env_config', 'fog', conf_name, 'on_ground')
                if conf:
                    params = {}
                    params.update(conf['native'])
                    params.update(conf['extra'])
                    if global_data.is_ue_model:
                        self.set_all_fog_info(params.get('fog_color', [91, 126, 202]), params.get('sun_fog_color', [120, 120, 120]), params.get('sun_fog_pow', 12.0), params.get('dis_start', 0), params.get('dis_end', 2000), params.get('height_begin', 330), params.get('fog_height_decay_speed', 0.02), params.get('fog_height_density', 1.1), params.get('fog_dis_density', 0.5), params.get('fog_acc_density_in_height', 1.0), params.get('fog_exposure_level', 1.8), params.get('sky_box_fog_factor', 1.0), params.get('skyline_power', 100.0), params.get('skyline_intensity', 3.0), params.get('skyline_color', [120, 0, 0]), params.get('clip_fog_dis', 10000.0), params.get('clip_fog_factor', 7000.0))
                    else:
                        self.set_fog(render.RS_FOG_VERTEX, render.RS_FOG_LINEAR, color_int(*params['color']), params['start'], params['end'], params['density'], params['height_begin'], params['height_end'], params['density'])
                elif global_data.is_ue_model:
                    self.enable_fog(False)
            return

    def set_all_fog_info(self, fog_color, sun_fog_color, sun_fog_pow, dis_start, dis_end, height_begin, fog_height_decay_speed, fog_height_density, fog_dis_density, fog_acc_density_in_height, fog_exposure_level, sky_box_fog_factor, skyline_power, skyline_intensity, skyline_color, clip_fog_dis, clip_fog_factor):
        self.set_fog(render.RS_FOG_VERTEX, render.RS_FOG_EXP2, color_int_srgb(*fog_color), dis_start, dis_end, 0, height_begin, fog_height_decay_speed, fog_dis_density, fog_exposure_level, fog_height_density, sun_fog_pow)
        self.set_global_uniform('SunFogColor', color_int_srgb(*sun_fog_color))
        self.set_global_uniform('FogAccDensityInHeight', fog_acc_density_in_height)
        self.set_global_uniform('ClipFogDis', clip_fog_dis)
        self.set_global_uniform('ClipFogFactor', clip_fog_factor)
        for i in range(2):
            mtl = self.get_sky_mtl(i)
            if mtl:
                mtl.set_var(_HASH_u_sky_box_fog_factor, 'u_sky_box_fog_factor', sky_box_fog_factor)
                mtl.set_var(_HASH_u_skyline_power, 'u_skyline_power', skyline_power)
                mtl.set_var(_HASH_u_skyline_intensity, 'u_skyline_intensity', skyline_intensity)
                mtl.set_var(_HASH_u_skyline_color, 'u_skyline_color', (skyline_color[0] / 255.0, skyline_color[1] / 255.0, skyline_color[2] / 255.0, 0.0))

    def enable_fog(self, enable):
        fog_type = enable and render.RS_FOG_EXP2 if 1 else render.RS_FOG_NONE
        i_type, mode, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent = self.get_fog()
        self.set_fog(i_type, fog_type, color, start, end, density, height_begin, height_end, shader_density, bright, height_fog_density, exponent)

    @sync_exec
    def setup_realtime_shadow_light--- This code section failed: ---

1779       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'valid'
           6  POP_JUMP_IF_TRUE     13  'to 13'

1780       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

1781      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             1  'set_global_uniform'
          19  LOAD_CONST            1  'BrightnessSkyIBL'
          22  LOAD_CONST            2  100.01
          25  CALL_FUNCTION_2       2 
          28  POP_TOP          

1783      29  LOAD_CONST            3  ''
          32  LOAD_CONST            4  ('NEOX_UNIT_SCALE',)
          35  IMPORT_NAME           2  'logic.gcommon.const'
          38  IMPORT_FROM           3  'NEOX_UNIT_SCALE'
          41  STORE_FAST            2  'NEOX_UNIT_SCALE'
          44  POP_TOP          

1784      45  LOAD_CONST            3  ''
          48  LOAD_CONST            0  ''
          51  IMPORT_NAME           4  'logic.vscene.global_display_setting'
          54  LOAD_ATTR             5  'vscene'
          57  LOAD_ATTR             6  'global_display_setting'
          60  STORE_FAST            3  'gds'

1786      63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             7  '_get_scene_data'
          69  LOAD_CONST            5  'light_config'
          72  CALL_FUNCTION_1       1 
          75  STORE_FAST            4  'conf_name'

1787      78  LOAD_FAST             4  'conf_name'
          81  LOAD_CONST            0  ''
          84  COMPARE_OP            8  'is'
          87  POP_JUMP_IF_FALSE    99  'to 99'

1788      90  LOAD_CONST            0  ''
          93  STORE_FAST            5  'conf'
          96  JUMP_FORWARD         24  'to 123'

1790      99  LOAD_GLOBAL           9  'confmgr'
         102  LOAD_ATTR            10  'get'
         105  LOAD_CONST            6  'c_env_config'
         108  LOAD_CONST            7  'light'
         111  LOAD_FAST             4  'conf_name'
         114  LOAD_CONST            8  'on_ground'
         117  CALL_FUNCTION_4       4 
         120  STORE_FAST            5  'conf'
       123_0  COME_FROM                '96'

1792     123  LOAD_FAST             0  'self'
         126  LOAD_ATTR            11  'get_light'
         129  LOAD_CONST            9  'game_light'
         132  CALL_FUNCTION_1       1 
         135  LOAD_FAST             0  'self'
         138  STORE_ATTR           12  'realtime_shadow_light'

1793     141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            12  'realtime_shadow_light'
         147  POP_JUMP_IF_TRUE    171  'to 171'

1794     150  LOAD_FAST             0  'self'
         153  LOAD_ATTR            11  'get_light'
         156  LOAD_CONST           10  'dir_light'
         159  CALL_FUNCTION_1       1 
         162  LOAD_FAST             0  'self'
         165  STORE_ATTR           12  'realtime_shadow_light'
         168  JUMP_FORWARD          0  'to 171'
       171_0  COME_FROM                '168'

1796     171  LOAD_FAST             0  'self'
         174  LOAD_ATTR            12  'realtime_shadow_light'
         177  POP_JUMP_IF_FALSE   773  'to 773'

1797     180  LOAD_FAST             3  'gds'
         183  LOAD_ATTR            13  'GlobalDisplaySeting'
         186  CALL_FUNCTION_0       0 
         189  STORE_FAST            6  'display_setting'

1801     192  LOAD_FAST             6  'display_setting'
         195  LOAD_ATTR            14  'actual_shadowmap_enabled'
         198  STORE_FAST            7  'cur_enable'

1803     201  LOAD_FAST             1  'force_flag'
         204  LOAD_CONST            0  ''
         207  COMPARE_OP            9  'is-not'
         210  POP_JUMP_IF_FALSE   222  'to 222'

1804     213  LOAD_FAST             1  'force_flag'
         216  STORE_FAST            7  'cur_enable'
         219  JUMP_FORWARD          0  'to 222'
       222_0  COME_FROM                '219'

1807     222  LOAD_FAST             0  'self'
         225  LOAD_ATTR            15  'save_enable_shadow'
         228  LOAD_FAST             7  'cur_enable'
         231  COMPARE_OP            3  '!='
         234  POP_JUMP_IF_FALSE   428  'to 428'

1808     237  LOAD_FAST             7  'cur_enable'
         240  LOAD_FAST             0  'self'
         243  STORE_ATTR           15  'save_enable_shadow'

1809     246  LOAD_FAST             7  'cur_enable'
         249  POP_JUMP_IF_FALSE   353  'to 353'

1812     252  LOAD_FAST             0  'self'
         255  LOAD_ATTR            16  'setup_csm_info'
         258  LOAD_FAST             0  'self'
         261  LOAD_ATTR            12  'realtime_shadow_light'
         264  LOAD_FAST             4  'conf_name'
         267  CALL_FUNCTION_2       2 
         270  POP_TOP          

1813     271  LOAD_FAST             0  'self'
         274  LOAD_ATTR            12  'realtime_shadow_light'
         277  LOAD_ATTR            17  'enable_shadow'
         280  POP_JUMP_IF_FALSE   310  'to 310'

1814     283  LOAD_GLOBAL          18  'False'
         286  LOAD_FAST             0  'self'
         289  LOAD_ATTR            12  'realtime_shadow_light'
         292  STORE_ATTR           17  'enable_shadow'

1815     295  LOAD_GLOBAL          19  'True'
         298  LOAD_FAST             0  'self'
         301  LOAD_ATTR            12  'realtime_shadow_light'
         304  STORE_ATTR           17  'enable_shadow'
         307  JUMP_FORWARD         12  'to 322'

1817     310  LOAD_GLOBAL          19  'True'
         313  LOAD_FAST             0  'self'
         316  LOAD_ATTR            12  'realtime_shadow_light'
         319  STORE_ATTR           17  'enable_shadow'
       322_0  COME_FROM                '307'

1818     322  LOAD_GLOBAL          20  'is_in_lobby'
         325  LOAD_FAST             0  'self'
         328  LOAD_ATTR            21  'scene_type'
         331  CALL_FUNCTION_1       1 
         334  POP_JUMP_IF_FALSE   365  'to 365'

1819     337  LOAD_FAST             0  'self'
         340  LOAD_ATTR            22  'forbid_receive_shadows'
         343  CALL_FUNCTION_0       0 
         346  POP_TOP          
         347  JUMP_ABSOLUTE       365  'to 365'
         350  JUMP_FORWARD         12  'to 365'

1823     353  LOAD_GLOBAL          18  'False'
         356  LOAD_FAST             0  'self'
         359  LOAD_ATTR            12  'realtime_shadow_light'
         362  STORE_ATTR           17  'enable_shadow'
       365_0  COME_FROM                '350'

1825     365  LOAD_CONST           11  0.97
         368  LOAD_FAST             0  'self'
         371  LOAD_ATTR            12  'realtime_shadow_light'
         374  STORE_ATTR           23  'shadow_alpha'

1827     377  LOAD_GLOBAL          24  'pc_platform_utils'
         380  LOAD_ATTR            25  'is_pc_hight_quality_simple'
         383  CALL_FUNCTION_0       0 
         386  POP_JUMP_IF_FALSE   404  'to 404'

1828     389  LOAD_CONST           12  3
         392  LOAD_FAST             0  'self'
         395  LOAD_ATTR            12  'realtime_shadow_light'
         398  STORE_ATTR           26  'shadow_quality'
         401  JUMP_ABSOLUTE       428  'to 428'

1830     404  LOAD_FAST             6  'display_setting'
         407  LOAD_ATTR            27  'quality_value'
         410  LOAD_CONST           13  'SHADOW_QUALITY'
         413  CALL_FUNCTION_1       1 
         416  LOAD_FAST             0  'self'
         419  LOAD_ATTR            12  'realtime_shadow_light'
         422  STORE_ATTR           26  'shadow_quality'
         425  JUMP_FORWARD          0  'to 428'
       428_0  COME_FROM                '425'

1832     428  LOAD_FAST             5  'conf'
         431  POP_JUMP_IF_FALSE   773  'to 773'

1834     434  LOAD_FAST             5  'conf'
         437  LOAD_CONST           14  'MainLightIntensity'
         440  BINARY_SUBSCR    
         441  LOAD_FAST             0  'self'
         444  LOAD_ATTR            12  'realtime_shadow_light'
         447  STORE_ATTR           28  'intensity'

1835     450  LOAD_GLOBAL          29  'color_int'
         453  LOAD_FAST             5  'conf'
         456  LOAD_CONST           15  'MainLightColor'
         459  BINARY_SUBSCR    
         460  CALL_FUNCTION_VAR_0     0 
         463  LOAD_FAST             0  'self'
         466  LOAD_ATTR            12  'realtime_shadow_light'
         469  STORE_ATTR           30  'diffuse'

1836     472  LOAD_GLOBAL          29  'color_int'
         475  LOAD_FAST             5  'conf'
         478  LOAD_CONST           16  'Ambient'
         481  BINARY_SUBSCR    
         482  CALL_FUNCTION_VAR_0     0 
         485  LOAD_FAST             0  'self'
         488  STORE_ATTR           31  'ambient_color'

1838     491  LOAD_GLOBAL          32  'global_data'
         494  LOAD_ATTR            33  'is_ue_model'
         497  POP_JUMP_IF_FALSE   770  'to 770'

1839     500  LOAD_GLOBAL          34  'getattr'
         503  LOAD_GLOBAL          17  'enable_shadow'
         506  LOAD_CONST            0  ''
         509  CALL_FUNCTION_3       3 
         512  POP_JUMP_IF_FALSE   560  'to 560'

1840     515  LOAD_FAST             0  'self'
         518  LOAD_ATTR            35  'set_sky_light'
         521  BUILD_LIST_0          0 
         524  LOAD_FAST             5  'conf'
         527  LOAD_CONST           18  'SkyLightColor'
         530  BINARY_SUBSCR    
         531  GET_ITER         
         532  FOR_ITER             18  'to 553'
         535  STORE_FAST            8  'x'
         538  LOAD_GLOBAL          36  'int'
         541  LOAD_FAST             8  'x'
         544  CALL_FUNCTION_1       1 
         547  LIST_APPEND           2  ''
         550  JUMP_BACK           532  'to 532'
         553  CALL_FUNCTION_VAR_0     0 
         556  POP_TOP          
         557  JUMP_FORWARD          0  'to 560'
       560_0  COME_FROM                '557'

1841     560  LOAD_GLOBAL          34  'getattr'
         563  LOAD_GLOBAL          19  'True'
         566  LOAD_CONST            0  ''
         569  CALL_FUNCTION_3       3 
         572  POP_JUMP_IF_FALSE   608  'to 608'

1842     575  LOAD_FAST             0  'self'
         578  LOAD_ATTR            37  'set_sky_light_intensity'
         581  LOAD_GLOBAL          38  'float'
         584  LOAD_FAST             5  'conf'
         587  LOAD_CONST           20  'SkyLightIntensity'
         590  BINARY_SUBSCR    
         591  CALL_FUNCTION_1       1 
         594  LOAD_FAST             0  'self'
         597  LOAD_ATTR            39  '_sky_light_scale'
         600  BINARY_MULTIPLY  
         601  CALL_FUNCTION_1       1 
         604  POP_TOP          
         605  JUMP_FORWARD          0  'to 608'
       608_0  COME_FROM                '605'

1845     608  LOAD_GLOBAL          34  'getattr'
         611  LOAD_GLOBAL          21  'scene_type'
         614  LOAD_CONST            0  ''
         617  CALL_FUNCTION_3       3 
         620  POP_JUMP_IF_FALSE   767  'to 767'

1846     623  LOAD_FAST             0  'self'
         626  LOAD_ATTR            40  'set_second_dir_light_enable'
         629  LOAD_GLOBAL          38  'float'
         632  LOAD_FAST             5  'conf'
         635  LOAD_CONST           22  'SecondDirLightEnable'
         638  BINARY_SUBSCR    
         639  CALL_FUNCTION_1       1 
         642  CALL_FUNCTION_1       1 
         645  POP_TOP          

1847     646  LOAD_FAST             0  'self'
         649  LOAD_ATTR            41  'set_second_dir_light_dir'
         652  BUILD_LIST_0          0 
         655  LOAD_FAST             5  'conf'
         658  LOAD_CONST           23  'SecondDirLightDir'
         661  BINARY_SUBSCR    
         662  LOAD_CONST           24  -1
         665  SLICE+2          
         666  GET_ITER         
         667  FOR_ITER             18  'to 688'
         670  STORE_FAST            8  'x'
         673  LOAD_GLOBAL          38  'float'
         676  LOAD_FAST             8  'x'
         679  CALL_FUNCTION_1       1 
         682  LIST_APPEND           2  ''
         685  JUMP_BACK           667  'to 667'
         688  CALL_FUNCTION_VAR_0     0 
         691  POP_TOP          

1848     692  LOAD_FAST             0  'self'
         695  LOAD_ATTR            42  'set_second_dir_light_color'
         698  BUILD_LIST_0          0 
         701  LOAD_FAST             5  'conf'
         704  LOAD_CONST           25  'SecondDirLightColor'
         707  BINARY_SUBSCR    
         708  GET_ITER         
         709  FOR_ITER             22  'to 734'
         712  STORE_FAST            8  'x'
         715  LOAD_GLOBAL          38  'float'
         718  LOAD_FAST             8  'x'
         721  LOAD_CONST           26  255
         724  BINARY_DIVIDE    
         725  CALL_FUNCTION_1       1 
         728  LIST_APPEND           2  ''
         731  JUMP_BACK           709  'to 709'
         734  CALL_FUNCTION_VAR_0     0 
         737  POP_TOP          

1849     738  LOAD_FAST             0  'self'
         741  LOAD_ATTR            43  'set_second_dir_light_intensity'
         744  LOAD_GLOBAL          38  'float'
         747  LOAD_FAST             5  'conf'
         750  LOAD_CONST           27  'SecondDirLightIntensity'
         753  BINARY_SUBSCR    
         754  CALL_FUNCTION_1       1 
         757  CALL_FUNCTION_1       1 
         760  POP_TOP          
         761  JUMP_ABSOLUTE       767  'to 767'
         764  JUMP_ABSOLUTE       770  'to 770'
         767  JUMP_ABSOLUTE       773  'to 773'
         770  JUMP_FORWARD          0  'to 773'
       773_0  COME_FROM                '770'

1851     773  LOAD_FAST             5  'conf'
         776  POP_JUMP_IF_FALSE  1201  'to 1201'

1853     779  LOAD_GLOBAL          32  'global_data'
         782  LOAD_ATTR            33  'is_ue_model'
         785  POP_JUMP_IF_FALSE   839  'to 839'

1854     788  LOAD_CONST           14  'MainLightIntensity'
         791  LOAD_CONST           16  'Ambient'
         794  LOAD_CONST           15  'MainLightColor'
         797  LOAD_CONST           20  'SkyLightIntensity'
         800  LOAD_CONST           18  'SkyLightColor'

1855     803  LOAD_CONST           22  'SecondDirLightEnable'
         806  LOAD_CONST           23  'SecondDirLightDir'
         809  LOAD_CONST           25  'SecondDirLightColor'

1856     812  LOAD_CONST           27  'SecondDirLightIntensity'
         815  LOAD_CONST           28  'IndirectIntensity'
         818  LOAD_CONST           29  'ToonIndirectIntensity'

1857     821  LOAD_CONST           30  'IndirectIntensityLow'
         824  LOAD_CONST           31  'ToonIndirectIntensityLow'
         827  LOAD_CONST           32  'LightmapThres'
         830  BUILD_SET_14         14 
         833  STORE_FAST            9  'skip_set'
         836  JUMP_FORWARD         30  'to 869'

1859     839  LOAD_CONST           14  'MainLightIntensity'
         842  LOAD_CONST           16  'Ambient'
         845  LOAD_CONST           15  'MainLightColor'
         848  LOAD_CONST           28  'IndirectIntensity'

1860     851  LOAD_CONST           29  'ToonIndirectIntensity'
         854  LOAD_CONST           30  'IndirectIntensityLow'
         857  LOAD_CONST           31  'ToonIndirectIntensityLow'

1861     860  LOAD_CONST           32  'LightmapThres'
         863  BUILD_SET_8           8 
         866  STORE_FAST            9  'skip_set'
       869_0  COME_FROM                '836'

1863     869  SETUP_LOOP           93  'to 965'
         872  LOAD_GLOBAL          44  'six'
         875  LOAD_ATTR            45  'iteritems'
         878  LOAD_FAST             5  'conf'
         881  CALL_FUNCTION_1       1 
         884  GET_ITER         
         885  FOR_ITER             76  'to 964'
         888  UNPACK_SEQUENCE_2     2 
         891  STORE_FAST           10  'k'
         894  STORE_FAST           11  'v'

1864     897  LOAD_FAST            10  'k'
         900  LOAD_FAST             9  'skip_set'
         903  COMPARE_OP            6  'in'
         906  POP_JUMP_IF_FALSE   915  'to 915'

1865     909  CONTINUE            885  'to 885'
         912  JUMP_FORWARD          0  'to 915'
       915_0  COME_FROM                '912'

1866     915  LOAD_GLOBAL          46  'isinstance'
         918  LOAD_FAST            11  'v'
         921  LOAD_GLOBAL          47  'list'
         924  CALL_FUNCTION_2       2 
         927  POP_JUMP_IF_FALSE   945  'to 945'

1867     930  LOAD_GLOBAL          29  'color_int'
         933  LOAD_FAST            11  'v'
         936  CALL_FUNCTION_VAR_0     0 
         939  STORE_FAST           11  'v'
         942  JUMP_FORWARD          0  'to 945'
       945_0  COME_FROM                '942'

1868     945  LOAD_FAST             0  'self'
         948  LOAD_ATTR             1  'set_global_uniform'
         951  LOAD_FAST            10  'k'
         954  LOAD_FAST            11  'v'
         957  CALL_FUNCTION_2       2 
         960  POP_TOP          
         961  JUMP_BACK           885  'to 885'
         964  POP_BLOCK        
       965_0  COME_FROM                '869'

1872     965  LOAD_GLOBAL          32  'global_data'
         968  LOAD_ATTR            48  'gsetting'
         971  LOAD_ATTR            49  'get_actual_quality'
         974  CALL_FUNCTION_0       0 
         977  STORE_FAST           12  'quality'

1873     980  LOAD_GLOBAL          50  'DEFAULT_LOD_MAPPING'
         983  LOAD_ATTR            10  'get'
         986  LOAD_FAST            12  'quality'
         989  LOAD_CONST           33  2
         992  CALL_FUNCTION_2       2 
         995  STORE_FAST           13  'lod_level'

1874     998  LOAD_FAST            13  'lod_level'
        1001  LOAD_GLOBAL          51  'world'
        1004  LOAD_ATTR            52  'SHADER_LOD_LEVEL_0'
        1007  COMPARE_OP            2  '=='
        1010  POP_JUMP_IF_FALSE  1019  'to 1019'
        1013  LOAD_GLOBAL          19  'True'
        1016  JUMP_FORWARD          3  'to 1022'
        1019  LOAD_GLOBAL          18  'False'
      1022_0  COME_FROM                '1016'
        1022  STORE_FAST           14  'is_hight_quality'

1876    1025  LOAD_FAST            14  'is_hight_quality'
        1028  POP_JUMP_IF_FALSE  1088  'to 1088'

1877    1031  LOAD_FAST             0  'self'
        1034  LOAD_ATTR             1  'set_global_uniform'
        1037  LOAD_CONST           28  'IndirectIntensity'
        1040  LOAD_FAST             5  'conf'
        1043  LOAD_CONST           28  'IndirectIntensity'
        1046  BINARY_SUBSCR    
        1047  LOAD_FAST             0  'self'
        1050  LOAD_ATTR            53  '_indirect_light_scale'
        1053  BINARY_MULTIPLY  
        1054  CALL_FUNCTION_2       2 
        1057  POP_TOP          

1878    1058  LOAD_FAST             0  'self'
        1061  LOAD_ATTR             1  'set_global_uniform'
        1064  LOAD_CONST           29  'ToonIndirectIntensity'
        1067  LOAD_FAST             5  'conf'
        1070  LOAD_CONST           29  'ToonIndirectIntensity'
        1073  BINARY_SUBSCR    
        1074  LOAD_FAST             0  'self'
        1077  LOAD_ATTR            53  '_indirect_light_scale'
        1080  BINARY_MULTIPLY  
        1081  CALL_FUNCTION_2       2 
        1084  POP_TOP          
        1085  JUMP_FORWARD         54  'to 1142'

1881    1088  LOAD_FAST             0  'self'
        1091  LOAD_ATTR             1  'set_global_uniform'
        1094  LOAD_CONST           28  'IndirectIntensity'
        1097  LOAD_FAST             5  'conf'
        1100  LOAD_CONST           30  'IndirectIntensityLow'
        1103  BINARY_SUBSCR    
        1104  LOAD_FAST             0  'self'
        1107  LOAD_ATTR            53  '_indirect_light_scale'
        1110  BINARY_MULTIPLY  
        1111  CALL_FUNCTION_2       2 
        1114  POP_TOP          

1882    1115  LOAD_FAST             0  'self'
        1118  LOAD_ATTR             1  'set_global_uniform'
        1121  LOAD_CONST           29  'ToonIndirectIntensity'
        1124  LOAD_FAST             5  'conf'
        1127  LOAD_CONST           31  'ToonIndirectIntensityLow'
        1130  BINARY_SUBSCR    
        1131  LOAD_FAST             0  'self'
        1134  LOAD_ATTR            53  '_indirect_light_scale'
        1137  BINARY_MULTIPLY  
        1138  CALL_FUNCTION_2       2 
        1141  POP_TOP          
      1142_0  COME_FROM                '1085'

1884    1142  LOAD_FAST             0  'self'
        1145  LOAD_ATTR            54  '_enable_lightmap_thres'
        1148  POP_JUMP_IF_FALSE  1182  'to 1182'

1885    1151  LOAD_FAST             0  'self'
        1154  LOAD_ATTR             1  'set_global_uniform'
        1157  LOAD_CONST           32  'LightmapThres'
        1160  LOAD_FAST             5  'conf'
        1163  LOAD_ATTR            10  'get'
        1166  LOAD_CONST           32  'LightmapThres'
        1169  LOAD_CONST           34  ''
        1172  CALL_FUNCTION_2       2 
        1175  CALL_FUNCTION_2       2 
        1178  POP_TOP          
        1179  JUMP_ABSOLUTE      1201  'to 1201'

1887    1182  LOAD_FAST             0  'self'
        1185  LOAD_ATTR             1  'set_global_uniform'
        1188  LOAD_CONST           32  'LightmapThres'
        1191  LOAD_CONST           34  ''
        1194  CALL_FUNCTION_2       2 
        1197  POP_TOP          
        1198  JUMP_FORWARD          0  'to 1201'
      1201_0  COME_FROM                '1198'
        1201  LOAD_CONST            0  ''
        1204  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 509

    def change_realtime_shadow_light_dir(self, dir):
        if not self.realtime_shadow_light and not self.original_light_dir:
            return
        else:
            if dir is None:
                if self.original_light_dir is None:
                    return
                self.realtime_shadow_light.direction = self.original_light_dir
            else:
                if self.original_light_dir is None:
                    self.original_light_dir = self.realtime_shadow_light.direction
                self.realtime_shadow_light.direction = dir
            return

    def setup_csm_info(self, realtime_shadow_light, conf_name):
        if is_in_lobby(self.scene_type):
            shadow_dist = 150.0
            shadow_ratio = (0.2, 0.4, 0.6, 1.0)
        else:
            shadow_dist = 600.0
            shadow_ratio = (0.15, 0.3, 0.6, 1.0)
            if is_win32():
                shadow_dist = shadow_dist * global_data.shadowmap_range_pc_scalar
                shadow_ratio = (90.0 / shadow_dist, 180.0 / shadow_dist, 0.6, 1.0)
        realtime_shadow_light.shadow_dist = shadow_dist
        if conf_name == 'zhanshi':
            realtime_shadow_light.set_csm_info(shadow_ratio, (0, 999999, 999999, 999999), (0,
                                                                                           0,
                                                                                           0,
                                                                                           0))
        else:
            realtime_shadow_light.set_csm_info(shadow_ratio, (0, 0, 0, 0), (0, 0, 0,
                                                                            0))

    @sync_exec
    def setup_env_light_info--- This code section failed: ---

1933       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'valid'
           6  POP_JUMP_IF_TRUE     13  'to 13'

1934       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

1936      13  LOAD_GLOBAL           1  'confmgr'
          16  LOAD_ATTR             2  'get'
          19  LOAD_CONST            1  'c_env_config'
          22  LOAD_CONST            2  'light'
          25  LOAD_FAST             1  'conf_name'
          28  LOAD_FAST             2  'sub_name'
          31  CALL_FUNCTION_4       4 
          34  STORE_FAST            4  'conf'

1938      37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             3  'realtime_shadow_light'
          43  POP_JUMP_IF_TRUE     50  'to 50'

1939      46  LOAD_CONST            0  ''
          49  RETURN_END_IF    
        50_0  COME_FROM                '43'

1941      50  LOAD_FAST             4  'conf'
          53  POP_JUMP_IF_FALSE   646  'to 646'

1943      56  LOAD_FAST             0  'self'
          59  LOAD_ATTR             4  'scene_data'
          62  LOAD_ATTR             2  'get'
          65  LOAD_CONST            3  'light_config'
          68  CALL_FUNCTION_1       1 
          71  LOAD_FAST             1  'conf_name'
          74  COMPARE_OP            2  '=='
          77  POP_JUMP_IF_FALSE    91  'to 91'
          80  LOAD_FAST             3  'force'
          83  UNARY_NOT        
        84_0  COME_FROM                '77'
          84  POP_JUMP_IF_FALSE    91  'to 91'

1944      87  LOAD_CONST            0  ''
          90  RETURN_END_IF    
        91_0  COME_FROM                '84'

1946      91  LOAD_FAST             1  'conf_name'
          94  LOAD_FAST             0  'self'
          97  LOAD_ATTR             4  'scene_data'
         100  LOAD_CONST            3  'light_config'
         103  STORE_SUBSCR     

1949     104  LOAD_FAST             4  'conf'
         107  LOAD_CONST            4  'MainLightIntensity'
         110  BINARY_SUBSCR    
         111  LOAD_FAST             0  'self'
         114  LOAD_ATTR             3  'realtime_shadow_light'
         117  STORE_ATTR            5  'intensity'

1950     120  LOAD_GLOBAL           6  'color_int'
         123  LOAD_FAST             4  'conf'
         126  LOAD_CONST            5  'MainLightColor'
         129  BINARY_SUBSCR    
         130  CALL_FUNCTION_VAR_0     0 
         133  LOAD_FAST             0  'self'
         136  LOAD_ATTR             3  'realtime_shadow_light'
         139  STORE_ATTR            7  'diffuse'

1951     142  LOAD_GLOBAL           6  'color_int'
         145  LOAD_FAST             4  'conf'
         148  LOAD_CONST            6  'Ambient'
         151  BINARY_SUBSCR    
         152  CALL_FUNCTION_VAR_0     0 
         155  LOAD_FAST             0  'self'
         158  STORE_ATTR            8  'ambient_color'

1953     161  LOAD_GLOBAL           9  'global_data'
         164  LOAD_ATTR            10  'is_ue_model'
         167  POP_JUMP_IF_FALSE   473  'to 473'

1955     170  LOAD_GLOBAL          11  'getattr'
         173  LOAD_GLOBAL           7  'diffuse'
         176  LOAD_CONST            0  ''
         179  CALL_FUNCTION_3       3 
         182  POP_JUMP_IF_FALSE   230  'to 230'

1956     185  LOAD_FAST             0  'self'
         188  LOAD_ATTR            13  'set_sky_light'
         191  BUILD_LIST_0          0 
         194  LOAD_FAST             4  'conf'
         197  LOAD_CONST            8  'SkyLightColor'
         200  BINARY_SUBSCR    
         201  GET_ITER         
         202  FOR_ITER             18  'to 223'
         205  STORE_FAST            5  'x'
         208  LOAD_GLOBAL          14  'int'
         211  LOAD_FAST             5  'x'
         214  CALL_FUNCTION_1       1 
         217  LIST_APPEND           2  ''
         220  JUMP_BACK           202  'to 202'
         223  CALL_FUNCTION_VAR_0     0 
         226  POP_TOP          
         227  JUMP_FORWARD          0  'to 230'
       230_0  COME_FROM                '227'

1957     230  LOAD_GLOBAL          11  'getattr'
         233  LOAD_GLOBAL           9  'global_data'
         236  LOAD_CONST            0  ''
         239  CALL_FUNCTION_3       3 
         242  POP_JUMP_IF_FALSE   278  'to 278'

1958     245  LOAD_FAST             0  'self'
         248  LOAD_ATTR            15  'set_sky_light_intensity'
         251  LOAD_GLOBAL          16  'float'
         254  LOAD_FAST             4  'conf'
         257  LOAD_CONST           10  'SkyLightIntensity'
         260  BINARY_SUBSCR    
         261  CALL_FUNCTION_1       1 
         264  LOAD_FAST             0  'self'
         267  LOAD_ATTR            17  '_sky_light_scale'
         270  BINARY_MULTIPLY  
         271  CALL_FUNCTION_1       1 
         274  POP_TOP          
         275  JUMP_FORWARD          0  'to 278'
       278_0  COME_FROM                '275'

1961     278  LOAD_GLOBAL          11  'getattr'
         281  LOAD_GLOBAL          11  'getattr'
         284  LOAD_CONST            0  ''
         287  CALL_FUNCTION_3       3 
         290  POP_JUMP_IF_FALSE   434  'to 434'

1962     293  LOAD_FAST             0  'self'
         296  LOAD_ATTR            18  'set_second_dir_light_enable'
         299  LOAD_GLOBAL          16  'float'
         302  LOAD_FAST             4  'conf'
         305  LOAD_CONST           12  'SecondDirLightEnable'
         308  BINARY_SUBSCR    
         309  CALL_FUNCTION_1       1 
         312  CALL_FUNCTION_1       1 
         315  POP_TOP          

1963     316  LOAD_FAST             0  'self'
         319  LOAD_ATTR            19  'set_second_dir_light_dir'
         322  BUILD_LIST_0          0 
         325  LOAD_FAST             4  'conf'
         328  LOAD_CONST           13  'SecondDirLightDir'
         331  BINARY_SUBSCR    
         332  LOAD_CONST           14  -1
         335  SLICE+2          
         336  GET_ITER         
         337  FOR_ITER             18  'to 358'
         340  STORE_FAST            5  'x'
         343  LOAD_GLOBAL          16  'float'
         346  LOAD_FAST             5  'x'
         349  CALL_FUNCTION_1       1 
         352  LIST_APPEND           2  ''
         355  JUMP_BACK           337  'to 337'
         358  CALL_FUNCTION_VAR_0     0 
         361  POP_TOP          

1964     362  LOAD_FAST             0  'self'
         365  LOAD_ATTR            20  'set_second_dir_light_color'
         368  BUILD_LIST_0          0 
         371  LOAD_FAST             4  'conf'
         374  LOAD_CONST           15  'SecondDirLightColor'
         377  BINARY_SUBSCR    
         378  GET_ITER         
         379  FOR_ITER             22  'to 404'
         382  STORE_FAST            5  'x'
         385  LOAD_GLOBAL          16  'float'
         388  LOAD_FAST             5  'x'
         391  LOAD_CONST           16  255
         394  BINARY_DIVIDE    
         395  CALL_FUNCTION_1       1 
         398  LIST_APPEND           2  ''
         401  JUMP_BACK           379  'to 379'
         404  CALL_FUNCTION_VAR_0     0 
         407  POP_TOP          

1965     408  LOAD_FAST             0  'self'
         411  LOAD_ATTR            21  'set_second_dir_light_intensity'
         414  LOAD_GLOBAL          16  'float'
         417  LOAD_FAST             4  'conf'
         420  LOAD_CONST           17  'SecondDirLightIntensity'
         423  BINARY_SUBSCR    
         424  CALL_FUNCTION_1       1 
         427  CALL_FUNCTION_1       1 
         430  POP_TOP          
         431  JUMP_FORWARD          0  'to 434'
       434_0  COME_FROM                '431'

1967     434  LOAD_CONST            4  'MainLightIntensity'
         437  LOAD_CONST            6  'Ambient'
         440  LOAD_CONST            5  'MainLightColor'
         443  LOAD_CONST            8  'SkyLightColor'
         446  LOAD_CONST           10  'SkyLightIntensity'

1968     449  LOAD_CONST           12  'SecondDirLightEnable'
         452  LOAD_CONST           13  'SecondDirLightDir'
         455  LOAD_CONST           15  'SecondDirLightColor'

1969     458  LOAD_CONST           17  'SecondDirLightIntensity'
         461  LOAD_CONST           18  'LightmapThres'
         464  BUILD_SET_10         10 
         467  STORE_FAST            6  'skip_set'
         470  JUMP_FORWARD         18  'to 491'

1971     473  LOAD_CONST            4  'MainLightIntensity'
         476  LOAD_CONST            6  'Ambient'
         479  LOAD_CONST            5  'MainLightColor'
         482  LOAD_CONST           18  'LightmapThres'
         485  BUILD_SET_4           4 
         488  STORE_FAST            6  'skip_set'
       491_0  COME_FROM                '470'

1973     491  SETUP_LOOP           93  'to 587'
         494  LOAD_GLOBAL          22  'six'
         497  LOAD_ATTR            23  'iteritems'
         500  LOAD_FAST             4  'conf'
         503  CALL_FUNCTION_1       1 
         506  GET_ITER         
         507  FOR_ITER             76  'to 586'
         510  UNPACK_SEQUENCE_2     2 
         513  STORE_FAST            7  'k'
         516  STORE_FAST            8  'v'

1974     519  LOAD_FAST             7  'k'
         522  LOAD_FAST             6  'skip_set'
         525  COMPARE_OP            6  'in'
         528  POP_JUMP_IF_FALSE   537  'to 537'

1975     531  CONTINUE            507  'to 507'
         534  JUMP_FORWARD          0  'to 537'
       537_0  COME_FROM                '534'

1976     537  LOAD_GLOBAL          24  'isinstance'
         540  LOAD_FAST             8  'v'
         543  LOAD_GLOBAL          25  'list'
         546  CALL_FUNCTION_2       2 
         549  POP_JUMP_IF_FALSE   567  'to 567'

1977     552  LOAD_GLOBAL           6  'color_int'
         555  LOAD_FAST             8  'v'
         558  CALL_FUNCTION_VAR_0     0 
         561  STORE_FAST            8  'v'
         564  JUMP_FORWARD          0  'to 567'
       567_0  COME_FROM                '564'

1978     567  LOAD_FAST             0  'self'
         570  LOAD_ATTR            26  'set_global_uniform'
         573  LOAD_FAST             7  'k'
         576  LOAD_FAST             8  'v'
         579  CALL_FUNCTION_2       2 
         582  POP_TOP          
         583  JUMP_BACK           507  'to 507'
         586  POP_BLOCK        
       587_0  COME_FROM                '491'

1980     587  LOAD_FAST             0  'self'
         590  LOAD_ATTR            27  '_enable_lightmap_thres'
         593  POP_JUMP_IF_FALSE   627  'to 627'

1981     596  LOAD_FAST             0  'self'
         599  LOAD_ATTR            26  'set_global_uniform'
         602  LOAD_CONST           18  'LightmapThres'
         605  LOAD_FAST             4  'conf'
         608  LOAD_ATTR             2  'get'
         611  LOAD_CONST           18  'LightmapThres'
         614  LOAD_CONST           19  ''
         617  CALL_FUNCTION_2       2 
         620  CALL_FUNCTION_2       2 
         623  POP_TOP          
         624  JUMP_ABSOLUTE       646  'to 646'

1983     627  LOAD_FAST             0  'self'
         630  LOAD_ATTR            26  'set_global_uniform'
         633  LOAD_CONST           18  'LightmapThres'
         636  LOAD_CONST           19  ''
         639  CALL_FUNCTION_2       2 
         642  POP_TOP          
         643  JUMP_FORWARD          0  'to 646'
       646_0  COME_FROM                '643'
         646  LOAD_CONST            0  ''
         649  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 179

    def forbid_receive_shadows(self):
        for mname in self.FORBID_RECEIVCE_SHADOW_MODELS:
            model = self.get_model(mname)
            if model and model.valid:
                model.receive_shadow = False

    def is_scene_light_enable_shadowmap(self):
        if not self.realtime_shadow_light:
            return False
        return self.realtime_shadow_light.enable_shadow

    def process_models_in_chunk(self, chunk_name, x, z):
        from logic.gutils.scene_utils import get_break_obj_prefix_auto, is_break_obj, get_break_info_by_full_name
        from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
        if chunk_name.startswith('l'):
            return
        all_models = self.get_models_in_chunk(x, z)
        if not all_models:
            return
        for m in all_models:
            model_name = getattr(m, 'name', '')
            if model_name in self.model_to_hide:
                m.visible = False
                m.destroy()
                continue
            prefix_name = get_break_obj_prefix_auto(model_name)
            self.model_prefix_info.setdefault(prefix_name, set([]))
            self.model_prefix_info[prefix_name].add(model_name)
            if is_break_obj(model_name):
                if self.ENABLE_BREAK_MODEL_SHADOWMAP:
                    m.cast_shadow = True
                m.set_col_group_mask(GROUP_SHOOTUNIT, GROUP_SHOOTUNIT)
                col_id = m.get_col_id()
                self.add_breakable_hp_obj_cid(m.name, col_id)
                break_info = get_break_info_by_full_name(model_name)
                if break_info and not break_info.get('iHaveImpact', 0):
                    m.set_static_col_vehicle_hurt(True)

    def process_models_in_single_scene(self):
        from logic.gutils.scene_utils import get_break_obj_prefix_auto, is_break_obj, get_break_info_by_full_name
        from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
        all_models = self.get_models()
        if not all_models:
            return
        for m in all_models:
            model_name = getattr(m, 'name', '')
            if model_name in self.model_to_hide:
                m.visible = False
                m.destroy()
                continue
            prefix_name = get_break_obj_prefix_auto(model_name)
            self.model_prefix_info.setdefault(prefix_name, set([]))
            self.model_prefix_info[prefix_name].add(model_name)
            if is_break_obj(model_name):
                if self.ENABLE_BREAK_MODEL_SHADOWMAP:
                    m.cast_shadow = True
                m.set_col_group_mask(GROUP_SHOOTUNIT, GROUP_SHOOTUNIT)
                col_id = m.get_col_id()
                self.add_breakable_hp_obj_cid(m.name, col_id)
                break_info = get_break_info_by_full_name(model_name)
                if break_info and not break_info.get('iHaveImpact', 0):
                    m.set_static_col_vehicle_hurt(True)

    def get_models_by_prefix(self, prefix_name):
        return self.model_prefix_info.get(prefix_name, None)

    def _setup_landscape(self, detail_dis=1920, col_dis=1920):
        import logic.vscene.global_display_setting as gds
        if not self.landscape:
            return
        self.landscape.set_LandscapeColRange(col_dis)
        self.landscape.screen_space_error_bound = 1500.0
        if hasattr(self.landscape, 'replace_lightmap_path'):
            if global_data.force_replace_lightmap:
                print('landscape.replace_lightmap_path in low_mem_mode...', global_data.force_replace_lightmap_path)
                self.landscape.replace_lightmap_path(global_data.force_replace_lightmap_path)
        display_setting = gds.GlobalDisplaySeting()
        self.landscape.enable_detail_simplify = not display_setting.quality_value('TERRAIN_DETAIL_ENABLE')
        self.landscape.render_patch_water_level = display_setting.quality_value('RENDER_PATCH_WATER_LEVEL')
        if detail_dis < 1.0:
            self.landscape.enable_blend(False)
            self.landscape.enable_shadowmap(False)
            self.landscape.set_EnableDetail(False)
        else:
            self.landscape.enable_blend(True)
            self.landscape.enable_shadowmap(True)
            self.landscape.set_EnableDetail(self.enable_detail)
            self.landscape.set_dis_param(detail_dis + 640, detail_dis * self.LOAD_DIST_TIME_2_VIS_DIST)
        if hasattr(self.landscape, 'release_detail_directly'):
            self.landscape.release_detail_directly = True
        if global_data.feature_mgr.is_new_landscape_detail_ready():
            self.landscape.use_new_detail = True
        elif hasattr(self.landscape, 'use_new_detail'):
            self.landscape.use_new_detail = False

    def load_detail(self, value):
        self.enable_detail = value and global_data.enable_scn_detail
        if self.landscape:
            self.landscape.set_EnableDetail(value)
        if self.terrain or self.landscape:
            if value:
                self._percent_st = progress.ST_PERCENT_UP
                self._check_logic = self.check_st_percent

    def check_st_percent(self):
        if self._percent_st == progress.ST_PERCENT_OVER:
            self.check_cur_chunk_loaded()
            return
        if self._percent_st != progress.ST_PERCENT_NONE:
            pg = self.get_progress()
            self._percent_st = progress.HANDLE[self._percent_st](pg)

    def recheck_st_percent(self):
        self._check_logic = self.check_cur_chunk_loaded

    def check_preload_loaded(self, pos, reset_check_count=False):
        x, z = self.in_which_trunk(pos)
        key = '(%d, %d)' % (x, z)
        if key in self._preload_check_info and self.preload_check_count < 60:
            for v in self._preload_check_info[key]:
                if not self.get_model(v):
                    self.preload_check_count += 1
                    return False

        if reset_check_count:
            self.preload_check_count = 0
        return True

    def check_landscape_has_load_detail_collision(self, position):
        if self.has_landscape:
            return self.landscape and self.landscape.has_load_detail_collision(position)
        else:
            return self.check_scene_node(position)

    def _try_refresh_camera_follow_target_pos(self, pos):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.share_data.ref_parachute_stage not in (parachute_utils.STAGE_PARACHUTE_DROP, parachute_utils.STAGE_LAND):
            return
        origin_pos = self.in_which_trunk(pos)
        viewer_pos = self.in_which_trunk(self.viewer_position)
        cam_pos = self.in_which_trunk(self.active_camera.world_position)
        if origin_pos != viewer_pos or viewer_pos != cam_pos:
            self.refresh_camera_follow_target_pos_flag += 1
            if self.refresh_camera_follow_target_pos_flag >= 50:
                ret = global_data.emgr.refresh_camera_follow_target_position.emit(pos)
                if ret and ret[0]:
                    self.camera_follow_target_pos_refreshed_ret = ret
                    self.refresh_camera_follow_target_pos_flag = 0
                    self.camera_follow_target_pos_refreshed_count += 1
        else:
            self.refresh_camera_follow_target_pos_flag = 0

    def check_collision_loaded--- This code section failed: ---

2188       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'async_load'
           6  POP_JUMP_IF_TRUE     13  'to 13'

2189       9  LOAD_GLOBAL           1  'True'
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

2191      13  LOAD_GLOBAL           2  'False'
          16  STORE_FAST            4  'check_node_res'

2192      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             3  'in_which_trunk'
          25  LOAD_FAST             1  'pos'
          28  CALL_FUNCTION_1       1 
          31  STORE_FAST            5  'xz'

2193      34  LOAD_CONST            1  '(%d, %d)'
          37  LOAD_FAST             5  'xz'
          40  BINARY_MODULO    
          41  STORE_FAST            6  'key'

2195      44  LOAD_GLOBAL           4  'global_data'
          47  LOAD_ATTR             5  'feature_mgr'
          50  LOAD_ATTR             6  'is_range_check_func_ready'
          53  CALL_FUNCTION_0       0 
          56  POP_JUMP_IF_FALSE    80  'to 80'

2196      59  LOAD_FAST             0  'self'
          62  LOAD_ATTR             7  'is_range_loaded'
          65  LOAD_FAST             1  'pos'
          68  LOAD_CONST            2  ''
          71  CALL_FUNCTION_2       2 
          74  STORE_FAST            4  'check_node_res'
          77  JUMP_FORWARD          0  'to 80'
        80_0  COME_FROM                '77'

2197      80  LOAD_FAST             4  'check_node_res'
          83  POP_JUMP_IF_TRUE   1229  'to 1229'

2198      86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             8  'check_scene_node'
          92  LOAD_FAST             1  'pos'
          95  CALL_FUNCTION_1       1 
          98  STORE_FAST            4  'check_node_res'

2199     101  LOAD_FAST             4  'check_node_res'
         104  POP_JUMP_IF_TRUE    150  'to 150'

2200     107  LOAD_FAST             0  'self'
         110  DUP_TOP          
         111  LOAD_ATTR             9  'collision_check_count'
         114  LOAD_CONST            3  1
         117  INPLACE_ADD      
         118  ROT_TWO          
         119  STORE_ATTR            9  'collision_check_count'

2201     122  LOAD_FAST             0  'self'
         125  LOAD_ATTR             9  'collision_check_count'
         128  LOAD_CONST            4  120
         131  COMPARE_OP            0  '<'
         134  POP_JUMP_IF_FALSE   141  'to 141'

2203     137  LOAD_GLOBAL           2  'False'
         140  RETURN_END_IF    
       141_0  COME_FROM                '134'

2205     141  LOAD_GLOBAL           1  'True'
         144  STORE_FAST            4  'check_node_res'
         147  JUMP_FORWARD          0  'to 150'
       150_0  COME_FROM                '147'

2207     150  LOAD_FAST             0  'self'
         153  LOAD_ATTR             3  'in_which_trunk'
         156  LOAD_FAST             1  'pos'
         159  CALL_FUNCTION_1       1 
         162  UNPACK_SEQUENCE_2     2 
         165  STORE_FAST            7  'x'
         168  STORE_FAST            8  'z'

2208     171  LOAD_CONST            1  '(%d, %d)'
         174  LOAD_FAST             7  'x'
         177  LOAD_FAST             8  'z'
         180  BUILD_TUPLE_2         2 
         183  BINARY_MODULO    
         184  STORE_FAST            6  'key'

2209     187  LOAD_CONST            5  1.3
         190  LOAD_GLOBAL          10  'DEFAULT_CHUNK_SIZE'
         193  BINARY_MULTIPLY  
         194  STORE_FAST            9  'trunk_distance_gap'

2210     197  LOAD_FAST             6  'key'
         200  LOAD_FAST             0  'self'
         203  LOAD_ATTR            11  '_overlap_check_info'
         206  COMPARE_OP            6  'in'
         209  POP_JUMP_IF_FALSE  1229  'to 1229'
         212  LOAD_FAST             0  'self'
         215  LOAD_ATTR             9  'collision_check_count'
         218  LOAD_CONST            4  120
         221  COMPARE_OP            0  '<'
       224_0  COME_FROM                '209'
         224  POP_JUMP_IF_FALSE  1229  'to 1229'

2211     227  SETUP_LOOP          996  'to 1226'
         230  LOAD_FAST             0  'self'
         233  LOAD_ATTR            11  '_overlap_check_info'
         236  LOAD_FAST             6  'key'
         239  BINARY_SUBSCR    
         240  GET_ITER         
         241  FOR_ITER            978  'to 1222'
         244  STORE_FAST           10  'v'

2212     247  LOAD_GLOBAL          12  'int'
         250  LOAD_FAST            10  'v'
         253  LOAD_CONST            6  ''
         256  BINARY_SUBSCR    
         257  CALL_FUNCTION_1       1 
         260  LOAD_GLOBAL          12  'int'
         263  LOAD_FAST            10  'v'
         266  LOAD_CONST            3  1
         269  BINARY_SUBSCR    
         270  CALL_FUNCTION_1       1 
         273  ROT_TWO          
         274  STORE_FAST           11  'delta_x'
         277  STORE_FAST           12  'delta_z'

2213     280  LOAD_FAST             7  'x'
         283  LOAD_FAST            11  'delta_x'
         286  BINARY_ADD       
         287  LOAD_FAST             8  'z'
         290  LOAD_FAST            12  'delta_z'
         293  BINARY_ADD       
         294  ROT_TWO          
         295  STORE_FAST           13  'new_trunk_x'
         298  STORE_FAST           14  'new_trunk_z'

2214     301  LOAD_FAST            13  'new_trunk_x'
         304  LOAD_GLOBAL          10  'DEFAULT_CHUNK_SIZE'
         307  BINARY_MULTIPLY  
         308  LOAD_FAST            14  'new_trunk_z'
         311  LOAD_GLOBAL          10  'DEFAULT_CHUNK_SIZE'
         314  BINARY_MULTIPLY  
         315  ROT_TWO          
         316  STORE_FAST           15  'new_trunk_center_x'
         319  STORE_FAST           16  'new_trunk_center_z'

2215     322  LOAD_GLOBAL          13  'abs'
         325  LOAD_FAST            15  'new_trunk_center_x'
         328  LOAD_FAST             1  'pos'
         331  LOAD_ATTR            14  'x'
         334  BINARY_SUBTRACT  
         335  CALL_FUNCTION_1       1 
         338  LOAD_FAST             9  'trunk_distance_gap'
         341  COMPARE_OP            4  '>'
         344  POP_JUMP_IF_TRUE    241  'to 241'
         347  LOAD_GLOBAL          13  'abs'
         350  LOAD_FAST            16  'new_trunk_center_z'
         353  LOAD_FAST             1  'pos'
         356  LOAD_ATTR            15  'z'
         359  BINARY_SUBTRACT  
         360  CALL_FUNCTION_1       1 
         363  LOAD_FAST             9  'trunk_distance_gap'
         366  COMPARE_OP            4  '>'
       369_0  COME_FROM                '344'
         369  POP_JUMP_IF_FALSE   378  'to 378'

2216     372  CONTINUE            241  'to 241'
         375  JUMP_FORWARD          0  'to 378'
       378_0  COME_FROM                '375'

2217     378  LOAD_GLOBAL          16  'math3d'
         381  LOAD_ATTR            17  'vector'
         384  LOAD_FAST             1  'pos'
         387  CALL_FUNCTION_1       1 
         390  STORE_FAST           17  'new_pos'

2218     393  LOAD_FAST            17  'new_pos'
         396  DUP_TOP          
         397  LOAD_ATTR            14  'x'
         400  LOAD_FAST            11  'delta_x'
         403  LOAD_GLOBAL          10  'DEFAULT_CHUNK_SIZE'
         406  BINARY_MULTIPLY  
         407  INPLACE_ADD      
         408  ROT_TWO          
         409  STORE_ATTR           14  'x'

2219     412  LOAD_FAST            17  'new_pos'
         415  DUP_TOP          
         416  LOAD_ATTR            15  'z'
         419  LOAD_FAST            12  'delta_z'
         422  LOAD_GLOBAL          10  'DEFAULT_CHUNK_SIZE'
         425  BINARY_MULTIPLY  
         426  INPLACE_ADD      
         427  ROT_TWO          
         428  STORE_ATTR           15  'z'

2220     431  LOAD_FAST             0  'self'
         434  LOAD_ATTR             8  'check_scene_node'
         437  LOAD_FAST            17  'new_pos'
         440  CALL_FUNCTION_1       1 
         443  STORE_FAST            4  'check_node_res'

2221     446  LOAD_FAST             4  'check_node_res'
         449  POP_JUMP_IF_TRUE    241  'to 241'

2223     452  LOAD_FAST             3  'need_refresh'
         455  JUMP_IF_FALSE_OR_POP   470  'to 470'
         458  LOAD_FAST             0  'self'
         461  LOAD_ATTR            18  '_try_refresh_camera_follow_target_pos'
         464  LOAD_FAST             1  'pos'
         467  CALL_FUNCTION_1       1 
       470_0  COME_FROM                '455'
         470  POP_TOP          

2224     471  LOAD_FAST             0  'self'
         474  DUP_TOP          
         475  LOAD_ATTR             9  'collision_check_count'
         478  LOAD_CONST            3  1
         481  INPLACE_ADD      
         482  ROT_TWO          
         483  STORE_ATTR            9  'collision_check_count'

2225     486  LOAD_FAST             0  'self'
         489  LOAD_ATTR             9  'collision_check_count'
         492  LOAD_CONST            7  500
         495  COMPARE_OP            2  '=='
         498  POP_JUMP_IF_FALSE  1215  'to 1215'

2226     501  LOAD_FAST             0  'self'
         504  LOAD_ATTR             3  'in_which_trunk'
         507  LOAD_FAST            17  'new_pos'
         510  CALL_FUNCTION_1       1 
         513  UNPACK_SEQUENCE_2     2 
         516  STORE_FAST            7  'x'
         519  STORE_FAST            8  'z'

2227     522  LOAD_FAST             0  'self'
         525  LOAD_ATTR             3  'in_which_trunk'
         528  LOAD_FAST             1  'pos'
         531  CALL_FUNCTION_1       1 
         534  STORE_FAST           18  'origin_pos'

2228     537  LOAD_FAST             0  'self'
         540  LOAD_ATTR             3  'in_which_trunk'
         543  LOAD_FAST             0  'self'
         546  LOAD_ATTR            19  'viewer_position'
         549  CALL_FUNCTION_1       1 
         552  STORE_FAST           19  'viewer_pos'

2229     555  LOAD_FAST             0  'self'
         558  LOAD_ATTR             3  'in_which_trunk'
         561  LOAD_FAST             0  'self'
         564  LOAD_ATTR            20  'active_camera'
         567  LOAD_ATTR            21  'world_position'
         570  CALL_FUNCTION_1       1 
         573  STORE_FAST           20  'cam_pos'

2230     576  LOAD_FAST            18  'origin_pos'
         579  LOAD_FAST            19  'viewer_pos'
         582  COMPARE_OP            3  '!='
         585  POP_JUMP_IF_TRUE    600  'to 600'
         588  LOAD_FAST            19  'viewer_pos'
         591  LOAD_FAST            20  'cam_pos'
         594  COMPARE_OP            3  '!='
       597_0  COME_FROM                '585'
         597  POP_JUMP_IF_FALSE   606  'to 606'
         600  LOAD_CONST            8  '[WRONG POS]'
         603  JUMP_FORWARD          3  'to 609'
         606  LOAD_CONST            9  ''
       609_0  COME_FROM                '603'
         609  STORE_FAST           21  'prefix'

2231     612  LOAD_FAST            21  'prefix'
         615  POP_JUMP_IF_TRUE    622  'to 622'

2233     618  LOAD_GLOBAL           2  'False'
         621  RETURN_END_IF    
       622_0  COME_FROM                '615'

2234     622  LOAD_GLOBAL           4  'global_data'
         625  LOAD_ATTR            22  'game_mode'
         628  POP_JUMP_IF_FALSE   656  'to 656'
         631  LOAD_GLOBAL           4  'global_data'
         634  LOAD_ATTR            22  'game_mode'
         637  LOAD_ATTR            23  'get_mode_type'
         640  CALL_FUNCTION_0       0 
         643  LOAD_CONST           22  ('death', 'randomdeath')
         646  COMPARE_OP            6  'in'
       649_0  COME_FROM                '628'
         649  POP_JUMP_IF_FALSE   656  'to 656'

2236     652  LOAD_GLOBAL           2  'False'
         655  RETURN_END_IF    
       656_0  COME_FROM                '649'

2237     656  LOAD_GLOBAL           4  'global_data'
         659  LOAD_ATTR            24  'cam_lplayer'
         662  POP_JUMP_IF_FALSE   690  'to 690'
         665  LOAD_GLOBAL           4  'global_data'
         668  LOAD_ATTR            24  'cam_lplayer'
         671  LOAD_ATTR            25  '__class__'
         674  LOAD_ATTR            26  '__name__'
         677  LOAD_CONST           12  'LAvatar'
         680  COMPARE_OP            3  '!='
       683_0  COME_FROM                '662'
         683  POP_JUMP_IF_FALSE   690  'to 690'

2239     686  LOAD_CONST            0  ''
         689  RETURN_END_IF    
       690_0  COME_FROM                '683'

2240     690  LOAD_GLOBAL           4  'global_data'
         693  LOAD_ATTR            24  'cam_lplayer'
         696  POP_JUMP_IF_TRUE    703  'to 703'

2241     699  LOAD_CONST            0  ''
         702  RETURN_END_IF    
       703_0  COME_FROM                '696'

2242     703  LOAD_GLOBAL           4  'global_data'
         706  LOAD_ATTR            27  'ex_scene_mgr_agent'
         709  LOAD_ATTR            28  'check_settle_scene_active'
         712  CALL_FUNCTION_0       0 
         715  POP_JUMP_IF_FALSE   722  'to 722'

2244     718  LOAD_CONST            0  ''
         721  RETURN_END_IF    
       722_0  COME_FROM                '715'

2245     722  LOAD_FAST             3  'need_refresh'
         725  POP_JUMP_IF_TRUE    732  'to 732'

2247     728  LOAD_CONST            0  ''
         731  RETURN_END_IF    
       732_0  COME_FROM                '725'

2248     732  LOAD_GLOBAL           4  'global_data'
         735  LOAD_ATTR            29  'cam_data'
         738  LOAD_ATTR            30  'camera_state_type'
         741  LOAD_CONST           13  '5'
         744  COMPARE_OP            2  '=='
         747  POP_JUMP_IF_FALSE   754  'to 754'

2250     750  LOAD_CONST            0  ''
         753  RETURN_END_IF    
       754_0  COME_FROM                '747'

2251     754  LOAD_CONST            0  ''
         757  STORE_FAST           22  'player_pos'

2252     760  LOAD_GLOBAL           4  'global_data'
         763  LOAD_ATTR            32  'player'
         766  POP_JUMP_IF_FALSE   826  'to 826'
         769  LOAD_GLOBAL           4  'global_data'
         772  LOAD_ATTR            32  'player'
         775  LOAD_ATTR            33  'logic'
       778_0  COME_FROM                '766'
         778  POP_JUMP_IF_FALSE   826  'to 826'

2253     781  LOAD_GLOBAL           4  'global_data'
         784  LOAD_ATTR            32  'player'
         787  LOAD_ATTR            33  'logic'
         790  LOAD_ATTR            34  'ev_g_position'
         793  CALL_FUNCTION_0       0 
         796  STORE_FAST           22  'player_pos'

2254     799  LOAD_FAST            22  'player_pos'
         802  POP_JUMP_IF_FALSE   826  'to 826'

2255     805  LOAD_FAST             0  'self'
         808  LOAD_ATTR             3  'in_which_trunk'
         811  LOAD_FAST            22  'player_pos'
         814  CALL_FUNCTION_1       1 
         817  STORE_FAST           22  'player_pos'
         820  JUMP_ABSOLUTE       826  'to 826'
         823  JUMP_FORWARD          0  'to 826'
       826_0  COME_FROM                '823'

2256     826  LOAD_GLOBAL           4  'global_data'
         829  LOAD_ATTR            24  'cam_lplayer'
         832  LOAD_ATTR            35  'ev_g_rb_pos_log'
         835  CALL_FUNCTION_0       0 
         838  STORE_FAST           23  'rb_pos_log'

2257     841  LOAD_FAST            23  'rb_pos_log'
         844  POP_JUMP_IF_FALSE   911  'to 911'

2258     847  LOAD_FAST            23  'rb_pos_log'
         850  UNPACK_SEQUENCE_4     4 
         853  STORE_FAST           24  'rb_time'
         856  STORE_FAST           25  'rb_pos'
         859  STORE_FAST           26  'reason'
         862  STORE_FAST           27  'rb_cam_pos'

2259     865  LOAD_GLOBAL           4  'global_data'
         868  LOAD_ATTR            36  'game_time'
         871  LOAD_FAST            24  'rb_time'
         874  BINARY_SUBTRACT  
         875  STORE_FAST           28  'rb_time_interval'

2260     878  LOAD_FAST             0  'self'
         881  LOAD_ATTR             3  'in_which_trunk'
         884  LOAD_FAST            25  'rb_pos'
         887  CALL_FUNCTION_1       1 
         890  STORE_FAST           25  'rb_pos'

2261     893  LOAD_FAST             0  'self'
         896  LOAD_ATTR             3  'in_which_trunk'
         899  LOAD_FAST            27  'rb_cam_pos'
         902  CALL_FUNCTION_1       1 
         905  STORE_FAST           27  'rb_cam_pos'
         908  JUMP_FORWARD         18  'to 929'

2263     911  LOAD_CONST           23  (-1, None, 0, None)
         914  UNPACK_SEQUENCE_4     4 
         917  STORE_FAST           28  'rb_time_interval'
         920  STORE_FAST           25  'rb_pos'
         923  STORE_FAST           26  'reason'
         926  STORE_FAST           27  'rb_cam_pos'
       929_0  COME_FROM                '908'

2264     929  LOAD_GLOBAL          37  'game3d'
         932  LOAD_ATTR            38  'post_hunter_message'

2265     935  LOAD_CONST           15  'Player stuck'
         938  LOAD_FAST            21  'prefix'
         941  LOAD_CONST           16  '[TEST LOG] WAITING CHUNK LOAD {} {} {}, PLAYER_POS({}), ORIGIN POS({}), VIEWER_POS({}), CAM_POS({}), PARACHUTE_STAGE({}), CAM_MGR_ATTR({}), GAME_MODE({}), CTARGET({}), REFRESHED({}, {}), PLAYER_STATE({}), CAM_MODE({}), FOLLOWING({}), RB_LOG({})'
         944  LOAD_ATTR            39  'format'

2268     947  LOAD_FAST             0  'self'
         950  LOAD_ATTR            40  'scene_data'
         953  LOAD_ATTR            41  'get'
         956  LOAD_CONST           17  'scene_name'
         959  LOAD_CONST            9  ''
         962  CALL_FUNCTION_2       2 

2269     965  LOAD_FAST             7  'x'
         968  LOAD_FAST             8  'z'
         971  LOAD_FAST            22  'player_pos'
         974  LOAD_FAST            18  'origin_pos'
         977  LOAD_FAST            19  'viewer_pos'
         980  LOAD_FAST            20  'cam_pos'

2270     983  LOAD_GLOBAL           4  'global_data'
         986  LOAD_ATTR            24  'cam_lplayer'
         989  POP_JUMP_IF_FALSE  1007  'to 1007'
         992  LOAD_GLOBAL           4  'global_data'
         995  LOAD_ATTR            24  'cam_lplayer'
         998  LOAD_ATTR            42  'share_data'
        1001  LOAD_ATTR            43  'ref_parachute_stage'
        1004  JUMP_FORWARD          3  'to 1010'
        1007  LOAD_CONST            9  ''
      1010_0  COME_FROM                '1004'

2271    1010  LOAD_GLOBAL           4  'global_data'
        1013  LOAD_ATTR            44  'emgr'
        1016  LOAD_ATTR            45  'get_camera_ctrl_view_pos_enabled'
        1019  LOAD_ATTR            46  'emit'
        1022  CALL_FUNCTION_0       0 
        1025  LOAD_CONST            6  ''
        1028  BINARY_SUBSCR    

2272    1029  LOAD_GLOBAL           4  'global_data'
        1032  LOAD_ATTR            22  'game_mode'
        1035  POP_JUMP_IF_FALSE  1053  'to 1053'
        1038  LOAD_GLOBAL           4  'global_data'
        1041  LOAD_ATTR            22  'game_mode'
        1044  LOAD_ATTR            23  'get_mode_type'
        1047  CALL_FUNCTION_0       0 
        1050  JUMP_FORWARD          3  'to 1056'
        1053  LOAD_CONST            9  ''
      1056_0  COME_FROM                '1050'

2273    1056  LOAD_GLOBAL          47  'str'
        1059  LOAD_GLOBAL           4  'global_data'
        1062  LOAD_ATTR            48  'cam_lctarget'
        1065  CALL_FUNCTION_1       1 
        1068  LOAD_CONST           18  ' '
        1071  BINARY_ADD       
        1072  LOAD_GLOBAL          47  'str'
        1075  LOAD_GLOBAL           4  'global_data'
        1078  LOAD_ATTR            24  'cam_lplayer'
        1081  CALL_FUNCTION_1       1 
        1084  BINARY_ADD       
        1085  LOAD_CONST           18  ' '
        1088  BINARY_ADD       
        1089  LOAD_GLOBAL          47  'str'
        1092  LOAD_GLOBAL           4  'global_data'
        1095  LOAD_ATTR            24  'cam_lplayer'
        1098  LOAD_ATTR            49  'ev_g_model'
        1101  CALL_FUNCTION_0       0 
        1104  CALL_FUNCTION_1       1 
        1107  BINARY_ADD       

2274    1108  LOAD_FAST             0  'self'
        1111  LOAD_ATTR            50  'camera_follow_target_pos_refreshed_ret'
        1114  LOAD_FAST             0  'self'
        1117  LOAD_ATTR            51  'camera_follow_target_pos_refreshed_count'

2275    1120  LOAD_GLOBAL           4  'global_data'
        1123  LOAD_ATTR            24  'cam_lplayer'
        1126  LOAD_ATTR            52  'ev_g_cur_state'
        1129  CALL_FUNCTION_0       0 

2276    1132  LOAD_GLOBAL           4  'global_data'
        1135  LOAD_ATTR            29  'cam_data'
        1138  LOAD_ATTR            30  'camera_state_type'

2277    1141  LOAD_GLOBAL           4  'global_data'
        1144  LOAD_ATTR            24  'cam_lplayer'
        1147  LOAD_ATTR            42  'share_data'
        1150  LOAD_ATTR            53  'ref_parachute_follow_target'

2278    1153  LOAD_GLOBAL          47  'str'
        1156  LOAD_FAST            28  'rb_time_interval'
        1159  CALL_FUNCTION_1       1 
        1162  LOAD_CONST           18  ' '
        1165  BINARY_ADD       
        1166  LOAD_GLOBAL          47  'str'
        1169  LOAD_FAST            26  'reason'
        1172  CALL_FUNCTION_1       1 
        1175  BINARY_ADD       
        1176  LOAD_CONST           18  ' '
        1179  BINARY_ADD       
        1180  LOAD_GLOBAL          47  'str'
        1183  LOAD_FAST            25  'rb_pos'
        1186  CALL_FUNCTION_1       1 
        1189  BINARY_ADD       
        1190  LOAD_CONST           18  ' '
        1193  BINARY_ADD       
        1194  LOAD_GLOBAL          47  'str'
        1197  LOAD_FAST            27  'rb_cam_pos'
        1200  CALL_FUNCTION_1       1 
        1203  BINARY_ADD       
        1204  CALL_FUNCTION_17     17 
        1207  BINARY_ADD       
        1208  CALL_FUNCTION_2       2 
        1211  POP_TOP          
        1212  JUMP_FORWARD          0  'to 1215'
      1215_0  COME_FROM                '1212'

2298    1215  LOAD_GLOBAL           2  'False'
        1218  RETURN_END_IF    
      1219_0  COME_FROM                '449'
        1219  JUMP_BACK           241  'to 241'
        1222  POP_BLOCK        
      1223_0  COME_FROM                '227'
        1223  JUMP_ABSOLUTE      1229  'to 1229'
        1226  JUMP_FORWARD          0  'to 1229'
      1229_0  COME_FROM                '1226'

2300    1229  LOAD_FAST             6  'key'
        1232  LOAD_FAST             0  'self'
        1235  LOAD_ATTR            54  '_preload_check_info'
        1238  COMPARE_OP            6  'in'
        1241  POP_JUMP_IF_FALSE  1381  'to 1381'
        1244  LOAD_FAST             0  'self'
        1247  LOAD_ATTR             9  'collision_check_count'
        1250  LOAD_CONST           19  60
        1253  COMPARE_OP            0  '<'
      1256_0  COME_FROM                '1241'
        1256  POP_JUMP_IF_FALSE  1381  'to 1381'

2301    1259  LOAD_FAST             0  'self'
        1262  LOAD_ATTR             9  'collision_check_count'
        1265  LOAD_CONST           20  59
        1268  COMPARE_OP            2  '=='
        1271  POP_JUMP_IF_FALSE  1320  'to 1320'

2303    1274  SETUP_LOOP           43  'to 1320'
        1277  LOAD_FAST             0  'self'
        1280  LOAD_ATTR            54  '_preload_check_info'
        1283  LOAD_FAST             6  'key'
        1286  BINARY_SUBSCR    
        1287  GET_ITER         
        1288  FOR_ITER             25  'to 1316'
        1291  STORE_FAST           10  'v'

2304    1294  LOAD_FAST             0  'self'
        1297  LOAD_ATTR            55  'get_model'
        1300  LOAD_FAST            10  'v'
        1303  CALL_FUNCTION_1       1 
        1306  POP_JUMP_IF_TRUE   1288  'to 1288'

2306    1309  BREAK_LOOP       
        1310  JUMP_BACK          1288  'to 1288'
        1313  JUMP_BACK          1288  'to 1288'
        1316  POP_BLOCK        
      1317_0  COME_FROM                '1274'
        1317  JUMP_FORWARD          0  'to 1320'
      1320_0  COME_FROM                '1274'

2309    1320  SETUP_LOOP           58  'to 1381'
        1323  LOAD_FAST             0  'self'
        1326  LOAD_ATTR            54  '_preload_check_info'
        1329  LOAD_FAST             6  'key'
        1332  BINARY_SUBSCR    
        1333  GET_ITER         
        1334  FOR_ITER             40  'to 1377'
        1337  STORE_FAST           10  'v'

2310    1340  LOAD_FAST             0  'self'
        1343  LOAD_ATTR            55  'get_model'
        1346  LOAD_FAST            10  'v'
        1349  CALL_FUNCTION_1       1 
        1352  POP_JUMP_IF_TRUE   1334  'to 1334'

2311    1355  LOAD_FAST             0  'self'
        1358  DUP_TOP          
        1359  LOAD_ATTR             9  'collision_check_count'
        1362  LOAD_CONST            3  1
        1365  INPLACE_ADD      
        1366  ROT_TWO          
        1367  STORE_ATTR            9  'collision_check_count'

2312    1370  LOAD_GLOBAL           2  'False'
        1373  RETURN_END_IF    
      1374_0  COME_FROM                '1352'
        1374  JUMP_BACK          1334  'to 1334'
        1377  POP_BLOCK        
      1378_0  COME_FROM                '1320'
        1378  JUMP_FORWARD          0  'to 1381'
      1381_0  COME_FROM                '1320'

2313    1381  LOAD_FAST             0  'self'
        1384  LOAD_ATTR            56  'landscape'
        1387  POP_JUMP_IF_FALSE  1451  'to 1451'
        1390  LOAD_FAST             2  'include_landscape'
      1393_0  COME_FROM                '1387'
        1393  POP_JUMP_IF_FALSE  1451  'to 1451'

2314    1396  LOAD_FAST             4  'check_node_res'
        1399  POP_JUMP_IF_FALSE  1421  'to 1421'

2315    1402  LOAD_FAST             0  'self'
        1405  LOAD_ATTR            56  'landscape'
        1408  LOAD_ATTR            57  'is_loading_detail_collision'
        1411  CALL_FUNCTION_0       0 
        1414  UNARY_NOT        
        1415  STORE_FAST            4  'check_node_res'
        1418  JUMP_FORWARD          0  'to 1421'
      1421_0  COME_FROM                '1418'

2316    1421  LOAD_FAST             4  'check_node_res'
        1424  POP_JUMP_IF_FALSE  1451  'to 1451'

2317    1427  LOAD_FAST             0  'self'
        1430  LOAD_ATTR            56  'landscape'
        1433  LOAD_ATTR            58  'has_load_detail_collision'
        1436  LOAD_FAST             1  'pos'
        1439  CALL_FUNCTION_1       1 
        1442  STORE_FAST            4  'check_node_res'
        1445  JUMP_ABSOLUTE      1451  'to 1451'
        1448  JUMP_FORWARD          0  'to 1451'
      1451_0  COME_FROM                '1448'

2318    1451  LOAD_GLOBAL          59  'hasattr'
        1454  LOAD_GLOBAL          21  'world_position'
        1457  CALL_FUNCTION_2       2 
        1460  POP_JUMP_IF_FALSE  1490  'to 1490'

2319    1463  LOAD_FAST             4  'check_node_res'
        1466  POP_JUMP_IF_FALSE  1490  'to 1490'

2320    1469  LOAD_FAST             0  'self'
        1472  LOAD_ATTR            60  'is_road_collision_loaded'
        1475  LOAD_FAST             1  'pos'
        1478  CALL_FUNCTION_1       1 
        1481  STORE_FAST            4  'check_node_res'
        1484  JUMP_ABSOLUTE      1490  'to 1490'
        1487  JUMP_FORWARD          0  'to 1490'
      1490_0  COME_FROM                '1487'

2321    1490  LOAD_FAST             4  'check_node_res'
        1493  POP_JUMP_IF_FALSE  1508  'to 1508'

2322    1496  LOAD_CONST            6  ''
        1499  LOAD_FAST             0  'self'
        1502  STORE_ATTR            9  'collision_check_count'
        1505  JUMP_FORWARD          0  'to 1508'
      1508_0  COME_FROM                '1505'

2323    1508  LOAD_FAST             4  'check_node_res'
        1511  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 1457

    def check_cur_chunk_loaded(self):
        pos = self.viewer_position
        if global_data.player and global_data.player.logic:
            parachute_stage = global_data.player.logic.share_data.ref_parachute_stage
            from logic.gcommon.common_utils.parachute_utils import STAGE_LAND
            if parachute_stage == STAGE_LAND:
                pos = global_data.player.logic.ev_g_position() or pos
        if self.check_collision_loaded(pos, True):
            if global_data.player and global_data.player.logic:
                player_position = global_data.player.logic.ev_g_position() or ''
            global_data.emgr.emit('event_finish_detail', None)
            self._detail_done = 1
            self._check_logic = None
            self._percent_st = progress.ST_PERCENT_NONE
        return

    def get_detail_done(self):
        return self._detail_done

    def on_login_reconnect(self, *args):
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.unregister_touch_event(self._listenerkey)
        touch_mgr.unregister_wheel_event(self._listenerkey)
        touch_mgr.register_touch_event(self._listenerkey, (self.on_touch_begin, self.on_touch_move, self.on_touch_end, self.on_touch_end))
        touch_mgr.register_wheel_event(self._listenerkey, self.on_mouse_wheel)

    def on_camera_move_enable(self, flag):
        self.camera_move_enable = flag

    def change_hdr_factor_to--- This code section failed: ---

2358       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'cancel_hdr_timer'
           6  CALL_FUNCTION_0       0 
           9  POP_TOP          

2359      10  LOAD_FAST             2  'duration'
          13  LOAD_FAST             0  'self'
          16  STORE_ATTR            1  '_hdr_change_duration'

2360      19  LOAD_GLOBAL           2  'time'
          22  LOAD_ATTR             2  'time'
          25  CALL_FUNCTION_0       0 
          28  LOAD_FAST             0  'self'
          31  STORE_ATTR            3  '_start_time'

2361      34  LOAD_GLOBAL           4  'getattr'
          37  LOAD_GLOBAL           1  '_hdr_change_duration'
          40  LOAD_CONST            2  1.0
          43  CALL_FUNCTION_3       3 
          46  LOAD_FAST             0  'self'
          49  STORE_ATTR            5  '_start_val'

2362      52  LOAD_FAST             1  'target'
          55  LOAD_FAST             0  'self'
          58  STORE_ATTR            6  '_hdr_target_val'

2363      61  LOAD_GLOBAL           7  'global_data'
          64  LOAD_ATTR             8  'game_mgr'
          67  LOAD_ATTR             9  'get_render_timer'
          70  CALL_FUNCTION_0       0 
          73  STORE_FAST            3  'tm'

2364      76  LOAD_FAST             3  'tm'
          79  LOAD_ATTR            10  'register'
          82  LOAD_CONST            3  'func'
          85  LOAD_FAST             0  'self'
          88  LOAD_ATTR            11  'handle_hdr_factor'
          91  CALL_FUNCTION_256   256 
          94  LOAD_FAST             0  'self'
          97  STORE_ATTR           12  '_render_timer_id'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 43

    def handle_hdr_factor(self):
        cur_time = time.time()
        dtime = cur_time - self._start_time
        per = min(1.0, dtime / self._hdr_change_duration)
        self.cur_hdr_val = self._start_val * (1.0 - per) + per * self._hdr_target_val
        if per >= 1.0:
            self.cancel_hdr_timer()

    def cancel_hdr_timer--- This code section failed: ---

2384       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'game_mgr'
           6  LOAD_ATTR             2  'get_render_timer'
           9  CALL_FUNCTION_0       0 
          12  STORE_FAST            1  'tm'

2385      15  LOAD_GLOBAL           3  'hasattr'
          18  LOAD_GLOBAL           1  'game_mgr'
          21  CALL_FUNCTION_2       2 
          24  POP_JUMP_IF_FALSE    46  'to 46'

2386      27  LOAD_FAST             1  'tm'
          30  LOAD_ATTR             4  'unregister'
          33  LOAD_FAST             0  'self'
          36  LOAD_ATTR             5  '_render_timer_id'
          39  CALL_FUNCTION_1       1 
          42  POP_TOP          
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21

    def enable_debug_shader_complexity--- This code section failed: ---

2389       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'feature_mgr'
           6  LOAD_ATTR             2  'is_support_debug_view_shader_complexity'
           9  CALL_FUNCTION_0       0 
          12  POP_JUMP_IF_TRUE     19  'to 19'

2390      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

2392      19  LOAD_CONST            1  'DirectX 11'
          22  LOAD_GLOBAL           3  'render'
          25  LOAD_ATTR             4  'get_render_system_name'
          28  CALL_FUNCTION_0       0 
          31  COMPARE_OP            7  'not-in'
          34  POP_JUMP_IF_FALSE    57  'to 57'

2393      37  LOAD_GLOBAL           0  'global_data'
          40  LOAD_ATTR             5  'game_mgr'
          43  LOAD_ATTR             6  'show_tip'
          46  LOAD_CONST            2  '\xe6\x9c\xac\xe5\x8a\x9f\xe8\x83\xbd\xe4\xbb\x85\xe5\x9c\xa8DX11\xe4\xb8\x8b\xe6\x89\x8d\xe8\x83\xbd\xe5\xbc\x80\xe5\x90\xaf,\xe8\xaf\xb7\xe5\x88\x87\xe6\x8d\xa2!'
          49  CALL_FUNCTION_1       1 
          52  POP_TOP          

2394      53  LOAD_CONST            0  ''
          56  RETURN_END_IF    
        57_0  COME_FROM                '34'

2396      57  LOAD_FAST             1  'flag'
          60  POP_JUMP_IF_FALSE   188  'to 188'

2397      63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             7  'set_msaa'
          69  LOAD_CONST            3  1
          72  CALL_FUNCTION_1       1 
          75  POP_TOP          

2398      76  LOAD_GLOBAL           0  'global_data'
          79  LOAD_ATTR             8  'display_agent'
          82  LOAD_ATTR             9  'set_aa_level'
          85  LOAD_CONST            4  ''
          88  CALL_FUNCTION_1       1 
          91  POP_TOP          

2400      92  LOAD_GLOBAL          10  'hasattr'
          95  LOAD_GLOBAL           3  'render'
          98  LOAD_CONST            5  'set_shader_complexity_info'
         101  CALL_FUNCTION_2       2 
         104  POP_JUMP_IF_FALSE   129  'to 129'

2401     107  LOAD_GLOBAL           3  'render'
         110  LOAD_ATTR            11  'set_shader_complexity_info'
         113  LOAD_CONST            6  2
         116  LOAD_CONST            7  300
         119  LOAD_CONST            7  300
         122  CALL_FUNCTION_3       3 
         125  POP_TOP          
         126  JUMP_FORWARD          0  'to 129'
       129_0  COME_FROM                '126'

2403     129  LOAD_GLOBAL          10  'hasattr'
         132  LOAD_GLOBAL           8  'display_agent'
         135  CALL_FUNCTION_2       2 
         138  POP_JUMP_IF_FALSE   157  'to 157'

2404     141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            12  'enable_shader_complexity_view'
         147  LOAD_FAST             1  'flag'
         150  CALL_FUNCTION_1       1 
         153  POP_TOP          
         154  JUMP_FORWARD          0  'to 157'
       157_0  COME_FROM                '154'

2406     157  LOAD_GLOBAL           0  'global_data'
         160  LOAD_ATTR             8  'display_agent'
         163  LOAD_ATTR            13  'set_longtime_post_process_active'
         166  LOAD_CONST            9  'DebugShaderComplexity'
         169  LOAD_FAST             1  'flag'
         172  CALL_FUNCTION_2       2 
         175  POP_TOP          

2408     176  LOAD_GLOBAL          14  'True'
         179  LOAD_GLOBAL           0  'global_data'
         182  STORE_ATTR           12  'enable_shader_complexity_view'
         185  JUMP_FORWARD         93  'to 281'

2411     188  LOAD_GLOBAL          10  'hasattr'
         191  LOAD_GLOBAL           3  'render'
         194  LOAD_CONST            5  'set_shader_complexity_info'
         197  CALL_FUNCTION_2       2 
         200  POP_JUMP_IF_FALSE   225  'to 225'

2412     203  LOAD_GLOBAL           3  'render'
         206  LOAD_ATTR            11  'set_shader_complexity_info'
         209  LOAD_CONST            4  ''
         212  LOAD_CONST            7  300
         215  LOAD_CONST            7  300
         218  CALL_FUNCTION_3       3 
         221  POP_TOP          
         222  JUMP_FORWARD          0  'to 225'
       225_0  COME_FROM                '222'

2414     225  LOAD_GLOBAL          10  'hasattr'
         228  LOAD_GLOBAL           8  'display_agent'
         231  CALL_FUNCTION_2       2 
         234  POP_JUMP_IF_FALSE   253  'to 253'

2415     237  LOAD_FAST             0  'self'
         240  LOAD_ATTR            12  'enable_shader_complexity_view'
         243  LOAD_FAST             1  'flag'
         246  CALL_FUNCTION_1       1 
         249  POP_TOP          
         250  JUMP_FORWARD          0  'to 253'
       253_0  COME_FROM                '250'

2417     253  LOAD_GLOBAL           0  'global_data'
         256  LOAD_ATTR             8  'display_agent'
         259  LOAD_ATTR            13  'set_longtime_post_process_active'
         262  LOAD_CONST            9  'DebugShaderComplexity'
         265  LOAD_FAST             1  'flag'
         268  CALL_FUNCTION_2       2 
         271  POP_TOP          

2419     272  LOAD_GLOBAL          15  'False'
         275  LOAD_GLOBAL           0  'global_data'
         278  STORE_ATTR           12  'enable_shader_complexity_view'
       281_0  COME_FROM                '185'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 135

    def enable_hdr(self, enable, refresh=False):
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        actual_quality = display_setting.get_actual_quality()
        force_enable = False
        if is_in_lobby(self.scene_type) and actual_quality >= 2 and not global_data.in_save_energy_mode:
            force_enable = True
        if self._get_scene_data('display_tag', False):
            perf_flag = device_compatibility.get_device_perf_flag()
            if perf_flag in (device_compatibility.PERF_FLAG_ANDROID_LOW, device_compatibility.PERF_FLAG_IOS_LOW):
                pass
            elif perf_flag in (device_compatibility.PERF_FLAG_ANDROID_MED,):
                pass
            else:
                force_enable = True
        if refresh:
            confmgr.refresh('c_env_config')
        if is_in_lobby(self.scene_type):
            enable_sky_box_ignore_tonemapper = 1.0 if 1 else 0.0
            conf_name = self._get_scene_data('hdr_config', 'default')
            if conf_name in ('zhanshi_human', 'zhanshi_mecha'):
                enable_sky_box_ignore_tonemapper = 0.0
            if global_data.is_pc_mode and global_data.feature_mgr.is_support_pc_eye_adapt() and global_data.enable_pc_eye_adapt:
                global_data.display_agent.set_longtime_post_process_active('eyeadapt', True)
                render.enable_pc_eye_adapt(True)
                render.set_pc_eye_adapt_params(0, 0, 0.2, 0.6, 0.7, 0.9, 1, 1)
            if not global_data.is_ue_model:
                lut_tex = render.texture('shader/texture_raw/lut_log.bmp')
                if device_limit.is_running_gles2():
                    global_data.display_agent.set_longtime_post_process_active('hdr', False)
                    global_data.display_agent.enable_tonemap(False)
                elif not device_compatibility.can_use_hdr():
                    self.set_tone_factor(0.25)
                    hdr_params = {}
                    hdr_params[1] = {_HASH_tex_lut: (
                                     'texture', 'TexLut', lut_tex),
                       _HASH_enable_sky_box_ignore_tonemapper: (
                                                              'var', 'enable_sky_box_ignore_tonemapper', enable_sky_box_ignore_tonemapper)
                       }
                    global_data.display_agent.set_longtime_post_process_active('hdr', False)
                    global_data.display_agent.enable_tonemap(True, hdr_params)
                elif enable or force_enable:
                    self.set_tone_factor(0.25)
                    conf_name = self._get_scene_data('hdr_config', 'default')
                    conf = confmgr.get('c_env_config', 'hdr', conf_name)
                    hdr_params = {}
                    mtl0 = {_HASH_BloomThreshold: (
                                            'var', 'BloomThreshold', conf['BloomThreshold'])
                       }
                    hdr_params[0] = mtl0
                    for i in range(1, 5):
                        mat_i = {}
                        hdr_params[i] = mat_i
                        mat_i[_HASH_BloomWidth] = (
                         'var', 'BloomWidth', conf['BloomWidth'])
                        mat_i[_HASH_BloomCoeff] = ('var', 'BloomCoeff', conf.get('BloomCoeff', 1.0))
                        mat_i[_HASH_BloomCoeff2] = ('var', 'BloomCoeff2', conf.get('BloomCoeff2', 1.0))

                    mtl5 = {_HASH_BloomLayer: (
                                        'var', 'bloomlayer', conf['bloomlayer'])
                       }
                    hdr_params[5] = mtl5
                    hdr_params[6] = {_HASH_tex_lut: (
                                     'texture', 'TexLut', lut_tex),
                       _HASH_enable_sky_box_ignore_tonemapper: (
                                                              'var', 'enable_sky_box_ignore_tonemapper', enable_sky_box_ignore_tonemapper)
                       }
                    global_data.display_agent.enable_tonemap(False)
                    global_data.display_agent.set_longtime_post_process_active('hdr', True, hdr_params)
                else:
                    self.set_tone_factor(0.25)
                    hdr_params = {}
                    hdr_params[1] = {_HASH_tex_lut: (
                                     'texture', 'TexLut', lut_tex),
                       _HASH_enable_sky_box_ignore_tonemapper: (
                                                              'var', 'enable_sky_box_ignore_tonemapper', enable_sky_box_ignore_tonemapper)
                       }
                    global_data.display_agent.set_longtime_post_process_active('hdr', False)
                    global_data.display_agent.enable_tonemap(True, hdr_params)
                self.is_hdr_enable = enable or force_enable
                scene_utils.reset_outline_process()
                global_data.display_agent.reset_enable_fx_target(global_data.enable_fx_target)
                return
            self.is_hdr_enable = device_compatibility.can_use_hdr() and (enable or force_enable)
            self.enable_bloom(self.is_hdr_enable)
            if self.is_hdr_enable:
                conf_name = self._get_scene_data('hdr_config', 'default')
                conf_name == 'zhanshi_mecha' or self.set_bloom_c_env(conf_name, True)
        self.set_tone_factor(0.25)
        if self.is_battle_scene():
            graphics_style = global_data.gsetting.get_real_graphics_style()
            lut_path = LUT_MAP.get(graphics_style, 'shader/texture_raw/lut_log.bmp')
        else:
            lut_path = 'shader/texture_raw/lut_log.bmp'
        params = {0: {_HASH_enable_sky_box_ignore_tonemapper: (
                                                      'var', 'enable_sky_box_ignore_tonemapper', enable_sky_box_ignore_tonemapper),
               _HASH_tex_lut: (
                             'texture', 'TexLut', lut_path)
               }
           }
        global_data.display_agent.enable_tonemap(True, params)
        scene_utils.reset_outline_process()
        global_data.display_agent.reset_enable_fx_target(global_data.enable_fx_target)

    @sync_exec
    def refresh_graphics_style(self):
        if not global_data.is_ue_model:
            return
        enable_sky_box_ignore_tonemapper = 1.0 if is_in_lobby(self.scene_type) else 0.0
        if self.is_battle_scene():
            graphics_style = global_data.gsetting.get_real_graphics_style()
            lut_path = LUT_MAP.get(graphics_style, 'shader/texture_raw/lut_log.bmp')
        else:
            lut_path = 'shader/texture_raw/lut_log.bmp'
        params = {0: {_HASH_enable_sky_box_ignore_tonemapper: (
                                                      'var', 'enable_sky_box_ignore_tonemapper', enable_sky_box_ignore_tonemapper),
               _HASH_tex_lut: (
                             'texture', 'TexLut', lut_path)
               }
           }
        global_data.display_agent.enable_tonemap(True, params)

    def reset_bloom(self):
        global G_CUR_HDR_CONF_NAME
        G_CUR_HDR_CONF_NAME = None
        if global_data.is_ue_model:
            conf_name = self._get_scene_data('hdr_config', 'default')
            if conf_name in ('dating', 'zhanshi_human', 'zhanshi_mecha'):
                self.set_bloom_c_env(conf_name)
        return

    def reset_tonemapping(self):
        global G_CUR_HDR_CONF_NAME
        G_CUR_HDR_CONF_NAME = None
        if global_data.is_ue_model and self.is_hdr_enable:
            conf_name = self._get_scene_data('hdr_config', 'default')
            if conf_name in ('dating', 'zhanshi_human', 'zhanshi_mecha'):
                enable_sky_box_ignore_tonemapper = 1.0 if conf_name == 'dating' else 0.0
                hdr_params = {}
                hdr_params[0] = {_HASH_enable_sky_box_ignore_tonemapper: (
                                                          'var', 'enable_sky_box_ignore_tonemapper', enable_sky_box_ignore_tonemapper)
                   }
                global_data.display_agent.update_tonemap(hdr_params)
        return

    def set_bloom_c_env(self, hdr_conf_name, force=False):
        global G_CUR_HDR_CONF_NAME
        if G_CUR_HDR_CONF_NAME == hdr_conf_name and not force:
            return
        G_CUR_HDR_CONF_NAME = hdr_conf_name
        conf = confmgr.get('c_env_config', 'hdr', hdr_conf_name)
        if not conf:
            return
        self.set_bloom_info(conf.get('bloom_threshold', -1.0), conf.get('sky_box_bloom_threshold', -1.0), conf.get('exposure_scale', 2.0), conf.get('bloom_size_scale', 1.0), conf.get('bloom2_size', 2.0), conf.get('bloom3_size', 4.0), conf.get('bloom1_intensity', 1.0), conf.get('bloom2_intensity', 1.0), conf.get('bloom3_intensity', 1.0), conf.get('bloom1_color', [255, 255, 255]), conf.get('bloom2_color', [255, 255, 255]), conf.get('bloom3_color', [255, 255, 255]))

    @sync_exec
    def set_bloom_info(self, bloom_threshold, sky_box_bloom_threshold, exposure_scale, bloom_size_scale, bloom2_size, bloom3_size, bloom1_intensity, bloom2_intensity, bloom3_intensity, bloom1_color, bloom2_color, bloom3_color):
        bloom1_color_f = (
         bloom1_color[0] / 255.0, bloom1_color[1] / 255.0, bloom1_color[2] / 255.0, 0.0)
        bloom2_color_f = (bloom2_color[0] / 255.0, bloom2_color[1] / 255.0, bloom2_color[2] / 255.0, 0.0)
        bloom3_color_f = (bloom3_color[0] / 255.0, bloom3_color[1] / 255.0, bloom3_color[2] / 255.0, 0.0)
        enable_sky_box_ignore_tonemapper = 1.0 if is_in_lobby(self.scene_type) else 0.0
        bloom_32_key = 5
        bloom_1_key = 6
        params = {0: {_HASH_BloomThreshold: (
                                    'var', 'BloomThreshold', bloom_threshold),
               _HASH_SkyBoxBloomThreshold: (
                                          'var', 'SkyBoxBloomThreshold', sky_box_bloom_threshold)
               },
           bloom_32_key: {_HASH_BloomIntensity3: (
                                                'var', 'BloomIntensity3', bloom3_intensity * exposure_scale),
                          _HASH_BloomColor3: (
                                            'var', 'BloomColor3', bloom3_color_f),
                          _HASH_BloomIntensity2: (
                                                'var', 'BloomIntensity2', bloom2_intensity * exposure_scale),
                          _HASH_BloomColor2: (
                                            'var', 'BloomColor2', bloom2_color_f)
                          },
           bloom_1_key: {_HASH_BloomIntensity1: (
                                               'var', 'BloomIntensity1', bloom1_intensity * exposure_scale),
                         _HASH_BloomColor1: (
                                           'var', 'BloomColor1', bloom1_color_f)
                         }
           }
        global_data.display_agent.update_bloom(params)
        r = (bloom1_color_f[0] * bloom1_color_f[0] * bloom1_intensity + bloom2_color_f[0] * bloom2_color_f[0] * bloom2_intensity + bloom3_color_f[0] * bloom3_color_f[0] * bloom3_intensity) * exposure_scale
        g = (bloom1_color_f[1] * bloom1_color_f[1] * bloom1_intensity + bloom2_color_f[1] * bloom2_color_f[1] * bloom2_intensity + bloom3_color_f[1] * bloom3_color_f[1] * bloom3_intensity) * exposure_scale
        b = (bloom1_color_f[2] * bloom1_color_f[2] * bloom1_intensity + bloom2_color_f[2] * bloom2_color_f[2] * bloom2_intensity + bloom3_color_f[2] * bloom3_color_f[2] * bloom3_intensity) * exposure_scale
        bloom_all_color = (
         r * r, g * g, b * b)
        tonemap_params = {0: {_HASH_BloomThreshold: (
                                    'var', 'BloomThreshold', bloom_threshold),
               _HASH_SkyBoxBloomThreshold: (
                                          'var', 'SkyBoxBloomThreshold', sky_box_bloom_threshold),
               _HASH_AddBloomColor: (
                                   'var', 'AddBloomColor', bloom_all_color)
               }
           }
        global_data.display_agent.update_tonemap(tonemap_params)

    def enable_bloom(self, enable):
        global_data.display_agent.enable_bloom(enable)
        enable_bloom = 1.0 if enable else 0.0
        params = {0: {_HASH_enable_bloom: (
                                  'var', 'enable_bloom', enable_bloom)
               }
           }
        global_data.display_agent.update_tonemap(params)

    def mat_set_var(self, mat, name, value):
        _HASH_name = game3d.calc_string_hash(name)
        mat.set_var(_HASH_name, name, value)

    def set_tonemap_info(self, Slope, Toe, Shoulder, BlackClip, WhiteClip, WhiteTemp, WhiteTint, Saturation, Contrast, Gamma, Gain, Offset, SaturationShadows, ContrastShadows, GammaShadows, GainShadows, OffsetShadows, CorrectionShadowsMax, SaturationMidtones, ContrastMidtones, GammaMidtones, GainMidtones, OffsetMidtones, SaturationHighlights, ContrastHighlights, GammaHighlights, GainHighlights, OffsetHighlights, CorrectionHighlightsMin, BlueCorrection, ExpandGamut, SceneColorTint, ColorGradingLut, LutSize, LutWeight):
        mat = global_data.display_agent.get_post_effect_pass_mtl('hdr_tonemap', 0)
        mat.set_macro('USE_LUT_TONEMAP', 'FALSE')
        lut_enable = 'TRUE' if ColorGradingLut else 'FALSE'
        mat.set_macro('USE_COLOR_GRADING_LUT', lut_enable)
        mat.rebuild_tech()
        self.mat_set_var(mat, 'Slope', Slope)
        self.mat_set_var(mat, 'Toe', Toe)
        self.mat_set_var(mat, 'Shoulder', Shoulder)
        self.mat_set_var(mat, 'BlackClip', BlackClip)
        self.mat_set_var(mat, 'WhiteClip', WhiteClip)
        self.mat_set_var(mat, 'WhiteTemp', WhiteTemp)
        self.mat_set_var(mat, 'WhiteTint', WhiteTint)
        self.mat_set_var(mat, 'ColorSaturation', Saturation)
        self.mat_set_var(mat, 'ColorContrast', Contrast)
        self.mat_set_var(mat, 'ColorGamma', Gamma)
        self.mat_set_var(mat, 'ColorGain', Gain)
        self.mat_set_var(mat, 'ColorOffset', Offset)
        self.mat_set_var(mat, 'ColorSaturationShadows', SaturationShadows)
        self.mat_set_var(mat, 'ColorContrastShadows', ContrastShadows)
        self.mat_set_var(mat, 'ColorGammaShadows', GammaShadows)
        self.mat_set_var(mat, 'ColorGainShadows', GainShadows)
        self.mat_set_var(mat, 'ColorOffsetShadows', OffsetShadows)
        self.mat_set_var(mat, 'ColorCorrectionShadowsMax', CorrectionShadowsMax)
        self.mat_set_var(mat, 'ColorSaturationMidtones', SaturationMidtones)
        self.mat_set_var(mat, 'ColorContrastMidtones', ContrastMidtones)
        self.mat_set_var(mat, 'ColorGammaMidtones', GammaMidtones)
        self.mat_set_var(mat, 'ColorGainMidtones', GainMidtones)
        self.mat_set_var(mat, 'ColorOffsetMidtones', OffsetMidtones)
        self.mat_set_var(mat, 'ColorSaturationHighlights', SaturationHighlights)
        self.mat_set_var(mat, 'ColorContrastHighlights', ContrastHighlights)
        self.mat_set_var(mat, 'ColorGammaHighlights', GammaHighlights)
        self.mat_set_var(mat, 'ColorGainHighlights', GainHighlights)
        self.mat_set_var(mat, 'ColorOffsetHighlights', OffsetHighlights)
        self.mat_set_var(mat, 'ColorCorrectionHighlightsMin', CorrectionHighlightsMin)
        self.mat_set_var(mat, 'BlueCorrection', BlueCorrection)
        self.mat_set_var(mat, 'ExpandGamut', ExpandGamut)
        self.mat_set_var(mat, 'SceneColorTint', (SceneColorTint[0] / 255.0, SceneColorTint[1] / 255.0, SceneColorTint[2] / 255.0))
        self.mat_set_var(mat, 'LutWeight', LutWeight)
        self.mat_set_var(mat, 'LutSize', LutSize)
        if ColorGradingLut:
            _HASH_ColorGradingLut = game3d.calc_string_hash('ColorGradingLut')
            lut_tex = render.texture(ColorGradingLut)
            mat.set_texture(_HASH_ColorGradingLut, 'ColorGradingLut', lut_tex)

    def enable_tonemap(self, enable):
        if not enable:
            self.enable_bloom(enable)
            self.set_tone_factor(1.0)
        else:
            self.set_tone_factor(0.25)
        global_data.display_agent.enable_tonemap(enable)

    def enable_distortion(self, enable):
        global_data.display_agent.set_longtime_post_process_active('distortion', enable)

    def enable_blur_with_mask(self, enable, texture=''):
        size = game3d.get_window_size()
        params = {}
        vss = [
         size[0] / 2.0, size[1] / 2.0]
        _HASH_PixelKernelOffset1 = game3d.calc_string_hash('PixelKernelOffset1')
        _HASH_PixelKernelOffset2 = game3d.calc_string_hash('PixelKernelOffset2')
        _HASH_PixelKernelWeight1 = game3d.calc_string_hash('PixelKernelWeight1')
        _HASH_PixelKernelWeight2 = game3d.calc_string_hash('PixelKernelWeight2')
        _HASH_tex_lut = game3d.calc_string_hash('TexMask')
        for i in range(2):
            params[i] = {_HASH_PixelKernelOffset1: ('var', 'PixelKernelOffset1', (-3.0 / vss[i], -2.0 / vss[i], -1.0 / vss[i], 0.0 / vss[i])),_HASH_PixelKernelOffset2: (
                                        'var', 'PixelKernelOffset2', (1.0 / vss[i], 2.0 / vss[i], 3.0 / vss[i], 0.0)),
               _HASH_PixelKernelWeight1: (
                                        'var', 'PixelKernelWeight1', (0.036633, 0.111281, 0.216745, 0.270682)),
               _HASH_PixelKernelWeight2: (
                                        'var', 'PixelKernelWeight2', (0.216745, 0.111281, 0.036633, 0.0))
               }

        if texture:
            params[1][_HASH_tex_lut] = (
             'texture', 'TexMask', render.texture(texture))
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur_with_mask', enable, params)

    def enable_fish_eye(self, enable):
        if enable:
            conf = confmgr.get('c_env_config', 'fisheye', 'default')
            mtl = {0: {_HASH_intensity_x: (
                                     'var', 'intensity_x', conf['FishEyeIntensityX']),
                   _HASH_intensity_y: (
                                     'var', 'intensity_y', conf['FishEyeIntensityY'])
                   }
               }
        else:
            mtl = None
        global_data.display_agent.set_longtime_post_process_active('fish_eye', enable, mtl)
        return

    def set_fish_eye_scalar_y(self, pos_y):
        return
        mat = global_data.display_agent.get_post_effect_pass_mtl('fish_eye', 0)
        if mat:
            conf = confmgr.get('c_env_config', 'fisheye', 'default')
            intensity_x = conf['FishEyeIntensityX']
            intensity_y = conf['FishEyeIntensityY']
            min_height = conf['FishEyeHeightEnd']
            max_height = conf['FishEyeHeightStart']
            scalar = (pos_y - min_height) / (max_height - min_height)
            scalar = min(1.0, max(0.0, scalar))
            self.fish_eye_scalars[0] = scalar
            if scalar <= 0:
                self.enable_fish_eye(False)
                return
            mat.set_var(_HASH_intensity_x, 'intensity_x', intensity_x * self.fish_eye_scalars[0] * self.fish_eye_scalars[1])
            mat.set_var(_HASH_intensity_y, 'intensity_y', intensity_y * self.fish_eye_scalars[0] * self.fish_eye_scalars[1])

    def set_fish_eye_scalar_pitch(self, pitch):
        return
        mat = global_data.display_agent.get_post_effect_pass_mtl('fish_eye', 0)
        if mat:
            conf = confmgr.get('c_env_config', 'fisheye', 'default')
            intensity_x = conf['FishEyeIntensityX']
            intensity_y = conf['FishEyeIntensityY']
            scalar = max(0.0, min(1.0, abs(1.0 - abs(pitch))))
            self.fish_eye_scalars[1] = scalar
            mat.set_var(_HASH_intensity_x, 'intensity_x', intensity_x * self.fish_eye_scalars[0] * self.fish_eye_scalars[1])
            mat.set_var(_HASH_intensity_y, 'intensity_y', intensity_y * self.fish_eye_scalars[0] * self.fish_eye_scalars[1])

    def enable_hero_outline(self, flag, uid):
        if flag:
            self.hero_outline_pp_info[uid] = 1
            scene_utils.set_outline_process_enable(True, scene_utils.HERO_OUTLINE_MASK)
        else:
            self.hero_outline_pp_info.pop(uid, None)
            if len(self.hero_outline_pp_info) == 0:
                scene_utils.set_outline_process_enable(False, scene_utils.HERO_OUTLINE_MASK)
        return

    def enable_detector_outline(self, flag, uid):
        if flag:
            self.detector_outline_pp_info[uid] = 1
            scene_utils.set_outline_process_enable(True, scene_utils.INFRARED_DETECTOR_MASK)
        else:
            self.detector_outline_pp_info.pop(uid, None)
            if len(self.detector_outline_pp_info) == 0:
                scene_utils.set_outline_process_enable(False, scene_utils.INFRARED_DETECTOR_MASK)
        return

    def enable_smooth_outline(self, flag, trigger_id):
        if flag:
            self.smooth_outline_pp_info[trigger_id] = 1
            global_data.display_agent.set_longtime_post_process_active('smooth_outline', True)
        else:
            self.smooth_outline_pp_info.pop(trigger_id, None)
            if len(self.smooth_outline_pp_info) == 0:
                global_data.display_agent.set_longtime_post_process_active('smooth_outline', False)
        return

    def add_breakable_hp_obj_unit_obj(self, bid, unit_obj_weak):
        if bid not in self.breakable_hp_obj:
            self.breakable_hp_obj[bid] = (
             unit_obj_weak, None)
        else:
            old_unit_obj_weak, cid = self.breakable_hp_obj[bid]
            self.breakable_hp_obj[bid] = (unit_obj_weak, cid)
            if unit_obj_weak and unit_obj_weak() and cid:
                global_data.emgr.scene_add_common_shoot_obj.emit(cid, unit_obj_weak())
        return

    def add_breakable_hp_obj_cid(self, bid, cid):
        if bid not in self.breakable_hp_obj:
            self.breakable_hp_obj[bid] = (
             None, cid)
        else:
            unit_obj_weak, old_cid = self.breakable_hp_obj[bid]
            self.breakable_hp_obj[bid] = (unit_obj_weak, cid)
            if unit_obj_weak and unit_obj_weak() and cid:
                global_data.emgr.scene_add_common_shoot_obj.emit(cid, unit_obj_weak())
        return

    def enable_scene_custom_map_uv_parameters(self, left_trk_idx, right_trk_idx, bottom_trk_idx, up_trk_idx, trunk_size):
        self.enable_scene_custom_map_uv = True
        self.map_uv_cache = (left_trk_idx, right_trk_idx, bottom_trk_idx, up_trk_idx, trunk_size)
        l_idx, r_idx, btm_idx, up_idx, trunk_size = (left_trk_idx, right_trk_idx, bottom_trk_idx, up_trk_idx, trunk_size)
        a_u = 1.0 / trunk_size / (r_idx - l_idx + 1.0)
        b_u = -(l_idx - 0.5) / (r_idx - l_idx + 1.0)
        a_v = 1.0 / trunk_size / (up_idx - btm_idx + 1.0)
        b_v = -(btm_idx - 0.5) / (up_idx - btm_idx + 1.0)
        self._map_uv_para_cache = (a_u, b_u, a_v, b_v)

    def disable_scene_custom_map_uv_parameters(self):
        self.enable_scene_custom_map_uv = False
        self.map_uv_cache = None
        self._map_uv_para_cache = None
        return

    def get_scene_map_uv_with_checking_script_logic(self, x, z):
        if not self.enable_scene_custom_map_uv:
            return self.get_scene_map_uv(x, z)
        else:
            a_u, b_u, a_v, b_v = self.get_safe_scene_map_uv_middle_parameters()
            u = a_u * x + b_u
            v = a_v * z + b_v
            res = (u, v)
            return res

    def get_safe_scene_map_uv_parameters(self):
        LEFT_TRK_IDX, RIGHT_TRK_IDX, BOTTOM_TRK_IDX, UP_TRK_IDX, TRUNK_SIZE = (-32.0,
                                                                               31.0,
                                                                               -32.0,
                                                                               31.0,
                                                                               832.0)
        if not self.map_uv_cache:
            self.map_uv_cache = self.get_scene_map_uv_parameters()
        res = self.map_uv_cache or (LEFT_TRK_IDX, RIGHT_TRK_IDX, BOTTOM_TRK_IDX, UP_TRK_IDX, TRUNK_SIZE)
        return res

    def get_safe_scene_map_uv_middle_parameters(self):
        if not self._map_uv_para_cache:
            l_idx, r_idx, btm_idx, up_idx, trunk_size = self.get_safe_scene_map_uv_parameters()
            a_u = 1.0 / trunk_size / (r_idx - l_idx + 1.0)
            b_u = -(l_idx - 0.5) / (r_idx - l_idx + 1.0)
            a_v = 1.0 / trunk_size / (up_idx - btm_idx + 1.0)
            b_v = -(btm_idx - 0.5) / (up_idx - btm_idx + 1.0)
            self._map_uv_para_cache = (a_u, b_u, a_v, b_v)
        return self._map_uv_para_cache

    @sync_exec
    def load_env(self, path):
        if not self.valid:
            return
        if global_data.is_ue_model:
            if global_data.feature_mgr.is_dynamic_ue_env_config():
                if path.startswith('competition_bw_06') or path.startswith('prepare_env'):
                    return
                env_file = scene_utils.env_path('default_nx2_mobile.xml')
                self.load_env_new(env_file)
                return
        env_file = scene_utils.env_path(path)
        if self._env_file != env_file and env_file:
            super(Scene, self).load_env(env_file)
            self._env_file = env_file
            if global_data.is_ue_model:
                if global_data.game_mode:
                    self.set_global_uniform('EnvType', global_data.game_mode.get_shader_env_type())
            else:
                snow_weather = global_data.game_mode.is_snow_res()
                self.set_global_uniform('SnowEnable', 1.0 if snow_weather else 0.0)

    def get_env(self):
        return self._env_file

    def get_fps_strategy(self):
        val = self._get_scene_data('fps_strategy', 'DEFAULT')
        return val

    def create_ui_panel(self, ui_template, size=None):
        from common.uisys import render_target
        ui_panel = self._ui_panels.get(ui_template, None)
        if not ui_panel:
            ui_panel = global_data.uisystem.load_template_create(ui_template, force_json=True)
            ui_panel.retain()
            self._ui_panels[ui_template] = ui_panel
        self._cur_ui_panel = ui_panel
        if not self._ui_rt:
            self._ui_rt = render_target.CocosRenderTarget(ui_panel, size=size)
        self._ui_rt.set_panel(ui_panel)
        return

    def get_ui_panel(self):
        return self._cur_ui_panel

    def get_ui_rt_obj(self):
        return self._ui_rt

    def get_ui_rt(self):
        if not self._ui_rt:
            return None
        else:
            return self._ui_rt.get_texture()

    def battle_res_prepare(self):
        render.insert_dynamic_texture_name_map('scene\\bw_all06_xc\\bw_all06_content\\probe\\skybox.dds', '\res\\textures\\become_rich.png')
        self.snow_mode_prepare()
        self.water_fog_prepare()
        self.sky_box_prepare()
        self.model_prepare()
        self.other_res_process()
        if global_data.game_mode:
            global_data.game_mode.replace_model_by_mode()
            enviroment = global_data.game_mode.get_enviroment()
            conf = confmgr.get('c_env_config', 'preload_dynamic_exclude', enviroment, default=[])
            for name in conf:
                self.add_preload_dynamic_exclude(name)

            if self.is_kongdao():
                world.set_model_lod_offset(0)

    def model_prepare(self):
        model_conf = {battle_const.BATTLE_ENV_NIGHT: confmgr.get('script_gim_ref')['model_night'],battle_const.BATTLE_ENV_GRANBELM: confmgr.get('script_gim_ref')['model_night']
           }
        if global_data.feature_mgr.is_support_dynamic_res_map():
            enviroment = global_data.game_mode.get_enviroment()
            model_paths = model_conf.get(enviroment, {})
            if model_paths:
                old_models = model_paths.get('old')
                new_models = model_paths.get('new')
                for index, model in enumerate(new_models):
                    world.set_res_object_filemap(old_models[index].replace('/', '\\'), model.replace('/', '\\'))

    def sky_box_prepare(self):
        sky_box_conf = {battle_const.BATTLE_ENV_NIGHT: confmgr.get('script_gim_ref')['sky_box_night'],
           battle_const.BATTLE_ENV_SNOW: confmgr.get('script_gim_ref')['sky_box_snow'],
           battle_const.BATTLE_ENV_SNOW_NIGHT: confmgr.get('script_gim_ref')['sky_box_night'],
           battle_const.BATTLE_ENV_NEUTRAL_SHOP: confmgr.get('script_gim_ref')['sky_box_s4'],
           battle_const.BATTLE_ENV_SUMMER: confmgr.get('script_gim_ref')['sky_box_s5']
           }
        ue_sky_box_conf = {battle_const.BATTLE_ENV_NIGHT: confmgr.get('script_gim_ref')['sky_box_night'],
           battle_const.BATTLE_ENV_SNOW_NIGHT: confmgr.get('script_gim_ref')['sky_box_night'],
           battle_const.BATTLE_ENV_SUMMER: confmgr.get('script_gim_ref')['sky_box_s5'],
           battle_const.BATTLE_ENV_GRANBELM: confmgr.get('script_gim_ref')['sky_box_granbelm'],
           battle_const.BATTLE_ENV_SNOW: confmgr.get('script_gim_ref')['sky_box_snow'],
           battle_const.BATTLE_ENV_AJLD_NIGHT: confmgr.get('script_gim_ref')['sky_box_night_aj'],
           battle_const.BATTLE_ENV_KONGDAO: confmgr.get('script_gim_ref')['sky_box_kongdao'],
           battle_const.BATTLE_ENV_BOUNTY: confmgr.get('script_gim_ref')['sky_box_bounty']
           }
        if global_data.feature_mgr.is_support_dynamic_res_map():
            enviroment = global_data.game_mode.get_enviroment()
            new_sky_box = ''
            if global_data.is_ue_model:
                new_sky_box = ue_sky_box_conf.get(enviroment, '')
            else:
                new_sky_box = sky_box_conf.get(enviroment, '')
            if new_sky_box:
                default_sky_box = confmgr.get('script_gim_ref')['default_sky_box'].replace('/', '\\')
                print(('-------new_sky_box---------', new_sky_box))
                world.set_res_object_filemap(default_sky_box, new_sky_box.replace('/', '\\'))

    def water_fog_prepare(self):
        water_fog_enable = '1' if self.is_normal() else '0'
        self.set_macros({'CALC_WATER_FOG_ENABLE': water_fog_enable})

    def snow_mode_prepare(self):
        import render
        snow_res = global_data.game_mode.is_snow_res()
        if snow_res:
            snow_enable = '1' if 1 else '0'
            self.set_macros({'SNOW_ENABLE': snow_enable})
            if global_data.feature_mgr.is_support_dynamic_texture_map() and global_data.feature_mgr.is_support_dynamic_res_map():
                render.clear_dynamic_texture_name_map()
                world.reset_res_object_filemap()
                if snow_res:
                    self.snow_mode_replace_res()
                else:
                    render.insert_dynamic_texture_name_map('textures\\snow_alpha_01.tga', 'textures\\empty.tga')
                self.set_macros({'OLD_ENGINE_SNOW_ENABLE': '0'})
            else:
                self.set_macros({'OLD_ENGINE_SNOW_ENABLE': snow_enable})
            if not snow_res:
                snow_col_name = ('snow_col_17098', 'snow_01_col_20494', 'snow_col_74839',
                                 'snow_01_col_62885', 'snow_col_62906', 'snow_col_72984',
                                 'snow_01_col_19212', 'snow_01_col_18151', 'snow_01_col_28101',
                                 'snow_01_col_61516', 'snow_01_col_19345', 'snow_01_col_17819',
                                 'snow_01_col_28097', 'snow_col_10036', 'snow_col_8773',
                                 'snow_col_8889', 'snow_col_9206', 'snow_col_37932',
                                 'snow_col_60672', 'snow_01_col_22531', 'snow_01_col_22170',
                                 'snow_col_30377', 'snow_col_40102', 'snow_col_46404',
                                 'snow_col_51336', 'snow_col_60349', 'snow_col_55603',
                                 'snow_col_64222', 'snow_01_col_23867', 'snow_col_60249',
                                 'snow_col_64984', 'snow_col_60203', 'snow_col_58312',
                                 'snow_01_col_23848', 'snow_01_col_23560', 'snow_01_col_23861',
                                 'snow_col_60094', 'snow_col_61322', 'snow_col_61141',
                                 'snow_col_61190', 'snow_col_42429', 'snow_col_60073',
                                 'snow_col_25623', 'snow_01_col_22788')
                for name in snow_col_name:
                    self.add_preload_dynamic_exclude(name)

            if snow_res:
                water_g = 0
                water_m = 0
                snow_uniform_enable = 1.0
            else:
                water_g = WATER_GROUP
                water_m = WATER_MASK
                snow_uniform_enable = 0.0
            global_data.is_ue_model or self.set_global_uniform('SnowEnable', snow_uniform_enable)
        if hasattr(collision, 'set_water_group_and_filter'):
            collision.set_water_group_and_filter(water_g, water_m)
        self.snow_night_mode_replace_res()

    def snow_mode_replace_res(self):
        import render
        render.set_dynamic_texture_name_map_enable(True)
        if global_data.is_ue_model:
            old_name1 = 'scene\\bw_all06_xc\\bw_all06_content\\landscape\\bw_all06\\%s'
            new_name1 = 'scene\\bw_all06_xc\\bw_all06_content\\snow_mode_res\\%s'
        else:
            old_name1 = 'scene\\bw_all06\\bw_all06_content\\landscape\\bw_all06\\%s'
            new_name1 = 'scene\\bw_all06\\bw_all06_content\\snow_mode_res\\%s'
        landscape_basemap = confmgr.get('snow_mode_file_replace', 'landscape_basemap')
        for file_name in landscape_basemap:
            render.insert_dynamic_texture_name_map(old_name1 % file_name, new_name1 % file_name)

        render.insert_dynamic_texture_name_map('textures\\scene\\all_01_alpha_01.tga', 'textures\\scene\\all_01_alpha_01_snow.tga')
        render.insert_dynamic_texture_name_map('textures\\scene\\all_01_alpha_n.tga', 'textures\\scene\\all_01_alpha_n_snow.tga')
        render.insert_dynamic_texture_name_map('model_new\\scene\\plant\\textures\\lod\\plant_tree_01_lod3.tga', 'model_new\\scene\\plant\\textures\\lod\\plant_tree_01_lod3_snow.tga')
        render.insert_dynamic_texture_name_map('model_new\\scene\\plant\\textures\\lod\\plant_tree_01_new_lod3.tga', 'model_new\\scene\\plant\\textures\\lod\\plant_tree_01_new_lod3_snow.tga')
        render.insert_dynamic_texture_name_map('model_new\\scene\\plant\\textures\\lod\\plant_tree_02_lod3.tga', 'model_new\\scene\\plant\\textures\\lod\\plant_tree_02_lod3_snow.tga')
        render.insert_dynamic_texture_name_map('model_new\\scene\\plant\\textures\\plant_baihuashu_02.tga', 'model_new\\scene\\plant\\textures\\plant_baihuashu_02_snow.tga')

    def snow_night_mode_replace_res(self):
        is_snow_night = global_data.game_mode.is_snow_night_weather()
        if is_snow_night:
            replace_scene_gim_map = confmgr.get('snow_night_res', 'replace_scene_gim_map')
            for k, v in six.iteritems(replace_scene_gim_map):
                world.set_res_object_filemap(k, v)

            replace_textures_list = confmgr.get('snow_night_res', 'replace_textures_list')
            for texture_name in replace_textures_list:
                old_texture = 'model_new\\scene\\' + texture_name
                new_texture = 'model_new\\scene_snow_night\\' + texture_name
                render.insert_dynamic_texture_name_map(old_texture, new_texture)

            lod_replace_texture_dict = confmgr.get('snow_night_res', 'replace_lod_texture_dict')
            for k, v in six.iteritems(lod_replace_texture_dict):
                render.insert_dynamic_texture_name_map(k, v)

            ignore_gim_list = confmgr.get('snow_night_res', 'ignore_gim_list')
            for ignore_gim in ignore_gim_list:
                world.set_res_object_filemap(ignore_gim, 'model_new\\scene\\box\\empty_kong_01.gim')

        else:
            ignore_snow_night_gim_list = confmgr.get('snow_night_res', 'ignore_snow_night_gim_list')
            for ignore_gim in ignore_snow_night_gim_list:
                world.set_res_object_filemap(ignore_gim, 'model_new\\scene\\box\\empty_kong_01.gim')

    def other_res_process(self):
        if not global_data.feature_mgr.is_support_dynamic_res_map():
            return
        if global_data.game_mode.is_neutral_shop_env():
            default_tree_08 = confmgr.get('script_gim_ref')['default_tree_08'].replace('/', '\\')
            s4_tree_08 = confmgr.get('script_gim_ref')['s4_tree_08'].replace('/', '\\')
            world.set_res_object_filemap(default_tree_08, s4_tree_08)
        for src, dst in six.iteritems(global_data.debug_replace_res_dict):
            world.set_res_object_filemap(src, dst)

        if hasattr(render, 'insert_dynamic_texture_name_map'):
            if self.is_kongdao() and device_compatibility.is_not_good_memory_size_device():
                render.set_dynamic_texture_name_map_enable(True)
                for src in confmgr.get('replaceable_res_kongdao', 'lightmap'):
                    render.insert_dynamic_texture_name_map(src, global_data.force_replace_lightmap_path)

    def hide_impostors(self, rang_c=3, range_r=3):
        if global_data.cam_lplayer:
            ctrl = global_data.cam_lplayer.ev_g_control_target()
            if ctrl and ctrl.logic:
                scene = global_data.game_mgr.scene
                c, r = scene.in_which_trunk(ctrl.logic.ev_g_position())
                new_chunks = set([])
                for _c in range(c - rang_c, c + rang_c):
                    for _r in range(r - range_r, r + range_r):
                        pos = math3d.vector(_c * DEFAULT_CHUNK_SIZE, 0, _r * DEFAULT_CHUNK_SIZE)
                        res = self.check_scene_node(pos)
                        if res:
                            new_chunks.add((_c, _r))

                for x, z in new_chunks:
                    idx = 0
                    while 1:
                        model = scene.get_model('impostor_l2_{0}_{1}_{2}'.format(x, z, idx))
                        idx += 1
                        if model and model.valid:
                            model.visible = False
                        else:
                            break

    def fix_impostors_bug(self):
        if self.is_fix_impostor_bug:
            return
        if not self.support_impostor_lod:
            return
        need_refresh = False
        if global_data.battle:
            if not CGameModeManager().is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                need_refresh = True
            if global_data.battle.is_in_island():
                need_refresh = True
        if global_data.had_enter_lobby and not need_refresh:
            return
        if self.load_l2_second_time:
            return
        self.impostor_detect_cnt += 1
        if self.impostor_detect_cnt < 3:
            return
        self.impostor_detect_cnt = 0
        self.hide_impostors(4, 4)

    def show_impostors(self):
        if self.support_impostor_lod:
            return
        self.impostor_detect_cnt += 1
        if self.impostor_detect_cnt < 3:
            return
        self.impostor_detect_cnt = 0
        c, r = self.in_which_trunk(self.active_camera.world_position)
        new_chunks = set([])
        for _c in range(c - 3, c + 3):
            for _r in range(r - 3, r + 3):
                pos = math3d.vector(_c * DEFAULT_CHUNK_SIZE, 0, _r * DEFAULT_CHUNK_SIZE)
                res = self.check_scene_node(pos)
                if res:
                    new_chunks.add((_c, _r))

        add_chunks = new_chunks - self.cur_chunks
        del_chunks = self.cur_chunks - new_chunks
        self.cur_chunks = new_chunks
        for x, z in del_chunks:
            idx = 0
            while 1:
                model = self.get_model('impostor_l2_{0}_{1}_{2}'.format(x, z, idx))
                idx += 1
                if model and model.valid:
                    model.visible = True
                else:
                    break

        for x, z in add_chunks:
            idx = 0
            while 1:
                model = self.get_model('impostor_l2_{0}_{1}_{2}'.format(x, z, idx))
                idx += 1
                if model and model.valid:
                    model.visible = False
                else:
                    break

    def set_light_config_finetune(self, sky_light_scale, indirect_light_scale, enable_lightmap_thres):
        self._sky_light_scale = sky_light_scale
        self._indirect_light_scale = indirect_light_scale
        self._enable_lightmap_thres = enable_lightmap_thres

    def get_light_config_finetune(self):
        return (
         self._sky_light_scale, self._indirect_light_scale, self._enable_lightmap_thres)