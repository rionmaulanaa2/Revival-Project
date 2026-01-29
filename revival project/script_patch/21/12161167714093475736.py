# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/global_display_setting.py
from __future__ import absolute_import
from __future__ import print_function
import six
import world
import game3d
from common.framework import Singleton
from world import SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_2
from logic.gcommon.common_const import ui_operation_const as uoc
import render
import six.moves.builtins
from common.utils import pc_platform_utils
from common.utils.timer import CLOCK
from common.utils.time_utils import get_time
from logic.gutils import device_utils
from logic.manager_agents.manager_decorators import sync_exec
if pc_platform_utils.is_pc_hight_quality_simple() and hasattr(world, 'SHADER_LOD_LEVEL_10'):
    SHADER_LOD_LEVEL_TOP = world.SHADER_LOD_LEVEL_10
else:
    SHADER_LOD_LEVEL_TOP = SHADER_LOD_LEVEL_0
from common.platform import is_win32
import version
from logic.gcommon.common_const.ui_operation_const import QUALITY_MECHA_EFFECT_LEVEL_KEY, MECHA_EFFECT_LEVEL_ULTRA
FAST = 0
NORMAL = 1
FINE = 2
FANTASY = 3
FANTASY_PC = 4
SWITCHER = {'SCENE_DETAIL': [
                  False, True, True, True, True],
   'SHADOWMAP_ENABLE': [
                      False, False, False, False, False],
   'SHADOW_QUALITY': [
                    2, 2, 2, 2, 2],
   'FOG_ENABLE': [
                True, True, True, True, True],
   'FOGTEX_ENABLE': [
                   False, True, True, True, True],
   'TERRAIN_DETAIL_ENABLE': [
                           True, True, True, True, True],
   'RENDER_PATCH_WATER_LEVEL': [
                              2, 2, 2, 2, 2],
   'VEGETATION_ENABLE': [
                       False, False, True, True, True],
   'VEGETATION_RANGE': [
                      0.1, 0.5, 0.8, 1.0, 1.0],
   'MAX_LOD_MESH_OFFSET': [
                         0, 0, 0, 0, 0],
   'TEXTURE_SKIP_LEVEL_SCENE': [
                              1, 0, 0, 0, 0],
   'TEXTURE_SKIP_LEVEL_SCENE_L1': [
                                 1, 0, 0, 0, 0],
   'TEXTURE_SKIP_LEVEL_PLAYER': [
                               1, 0, 0, 0, 0],
   'EFFECT_SHADER_LEVEL': [
                         2, 1, 0, 0, 0],
   'SFX_RENDER_LEVEL': [
                      0, 2, 2, 4, 4],
   'SFX_RENDER_PERCENTAGE': [
                           1.0, 0.5, 0.7, 1.0, 1.0],
   'SFX_RENDER_LEVEL_LOD': (
                          (
                           (650, 4), (1300, 2), (1300000, 0)),
                          (
                           (650, 4), (1300, 2), (1300000, 0)),
                          (
                           (650, 4), (1300, 2), (1300000, 0)),
                          (
                           (650, 4), (1300, 2), (1300000, 0)),
                          (
                           (650, 4), (1300, 2), (1300000, 0))),
   'SFX_UPDATE_FRAME_LOD': (
                          (
                           (1300, 1), (2600, 3), (1300000, 5)),
                          (
                           (1300, 1), (2600, 3), (1300000, 5)),
                          (
                           (1300, 1), (2600, 3), (1300000, 5)),
                          (
                           (1300, 1), (2600, 3), (1300000, 5)),
                          (
                           (1300, 1), (2600, 3), (1300000, 5))),
   'RESOLUTION': [
                0.5, 0.67, 0.8, 0.84, 0.84],
   'RESOLUTION_KONGDAO': [
                        0.5, 0.67, 0.8, 0.84, 0.84],
   'MODEL_FADE_IN': [
                   False, False, False, False, False],
   'LARGE_VIEW_RANGE': [
                      20000, 40000, 40000, 40000, 40000],
   'NEAR_VIEW_RANGE_FIX': [
                         1.0, 1.0, 1.0, 1.0, 1.0],
   'FAR_VIEW_RANGE_FIX': [
                        1.0, 1.0, 1.0, 1.0, 1.0],
   'LANDSCAPE_RANGE': [
                     832, 832, 1248.0, 1248.0, 1248.0],
   'HIGH_FRAME_RATE': [
                     0, 0, 0, 0, 0],
   'ENABLE_SHADING_RATE': [
                         True, True, True, False, False]
   }
GLOBAL_POSTEFFECT = [
 set(['tone_mapping']),
 set(['tone_mapping']),
 set(['tone_mapping']),
 set(['hdr', 'msaa4x']),
 set(['hdr', 'msaa4x'])]
FPS_STRATEGY = {'FORCE_HIGH_FPS': True,
   'FORCE_LIMITED_FPS': False
   }
DEVICE_TYPE_PC = 1
DEVICE_TYPE_IOS_NORMAL = 2
DEVICE_TYPE_IOS_LOW_PPI = 3
DEVICE_TYPE_ANDROID_NORMAL = 4
DEVICE_TYPE_LOW_PERF = 5
DEVICE_TYPE_SAVE_ENERGY = 6
DEVICE_TYPE_THERMAL_STATE_HOT = 7
DEVICE_TYPE_ANDROID_LOW_PPI = 8
RESO_SCENE_TYPE_SHOW = 1
RESO_SCENE_TYPE_LOBBY = 2
RESO_SCENE_TYPE_GAME = 3
RESO_SCENE_TYPE_GAME_DEATH_MATCH = 4
RESOLUTION_CONFIG = {DEVICE_TYPE_PC: {RESO_SCENE_TYPE_SHOW: {0: 580,1: 720,2: 1080,3: -1},RESO_SCENE_TYPE_LOBBY: {0: 580,1: 720,2: 1080,3: -1},RESO_SCENE_TYPE_GAME: {0: 580,1: 720,2: 1080,3: -1},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 580,1: 720,2: 1080,3: -1}},DEVICE_TYPE_IOS_NORMAL: {RESO_SCENE_TYPE_SHOW: {0: 720,1: 900,2: 900,3: 1080},RESO_SCENE_TYPE_LOBBY: {0: 720,1: 900,2: 900,3: 1080},RESO_SCENE_TYPE_GAME: {0: 580,1: 720,2: 720,3: 900},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 580,1: 720,2: 720,3: 900}},DEVICE_TYPE_IOS_LOW_PPI: {RESO_SCENE_TYPE_SHOW: {0: 720,1: 900,2: 1080,3: 1080},RESO_SCENE_TYPE_LOBBY: {0: 720,1: 900,2: 1080,3: 1080},RESO_SCENE_TYPE_GAME: {0: 720,1: 900,2: 1080,3: 1080},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 720,1: 900,2: 900,3: 900}},DEVICE_TYPE_ANDROID_NORMAL: {RESO_SCENE_TYPE_SHOW: {0: 580,1: 720,2: -1,3: -1},RESO_SCENE_TYPE_LOBBY: {0: 580,1: 720,2: 900,3: 900},RESO_SCENE_TYPE_GAME: {0: 580,1: 720,2: 720,3: 900},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 580,1: 580,2: 720,3: 900}},DEVICE_TYPE_ANDROID_LOW_PPI: {RESO_SCENE_TYPE_SHOW: {0: 720,1: 900,2: 1080,3: 1080},RESO_SCENE_TYPE_LOBBY: {0: 720,1: 900,2: 1080,3: 1080},RESO_SCENE_TYPE_GAME: {0: 720,1: 900,2: 1080,3: 1080},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 720,1: 900,2: 900,3: 900}},DEVICE_TYPE_LOW_PERF: {RESO_SCENE_TYPE_SHOW: {0: 580,1: 580,2: 720,3: 720},RESO_SCENE_TYPE_LOBBY: {0: 580,1: 580,2: 720,3: 720},RESO_SCENE_TYPE_GAME: {0: 580,1: 580,2: 720,3: 720},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 580,1: 580,2: 580,3: 720}},DEVICE_TYPE_SAVE_ENERGY: {RESO_SCENE_TYPE_SHOW: {0: 580,1: 580,2: 580,3: 580},RESO_SCENE_TYPE_LOBBY: {0: 580,1: 580,2: 580,3: 580},RESO_SCENE_TYPE_GAME: {0: 580,1: 580,2: 580,3: 580},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 580,1: 580,2: 580,3: 580}},DEVICE_TYPE_THERMAL_STATE_HOT: {RESO_SCENE_TYPE_SHOW: {0: 580,1: 580,2: 720,3: 720},RESO_SCENE_TYPE_LOBBY: {0: 580,1: 580,2: 720,3: 720},RESO_SCENE_TYPE_GAME: {0: 580,1: 580,2: 720,3: 720},RESO_SCENE_TYPE_GAME_DEATH_MATCH: {0: 580,1: 580,2: 580,3: 720}}}
LOW_MEM_MODE_SETTINGS = {game3d.PLATFORM_IOS: {'TEXTURE_SKIP_LEVEL_SCENE': 2,
                         'TEXTURE_SKIP_LEVEL_SCENE_L1': 2,
                         'TEXTURE_SKIP_LEVEL_PLAYER': 1,
                         'simple_vertex_stream_tech_names': ('shader\\lightmap.fx::TShader', 'shader\\lightmap_high.fx::TShader', 'shader\\lightmap93.fx::TShader',
 'shader\\lightmap93_rock.fx::TShader', 'shader\\common_terrain_lightmap.fx::TShader',
 'shader\\xc_landscape_detail.fx::TerrainTech', 'shader\\impostor.fx::TShader', 'shader\\common_emission.fx::TShader',
 'shader\\common_lightmap.fx::TShader', 'shader\\common_ball_nx2_mobile.fx::TShader',
 'shader\\common_ball.fx::TShader'),
                         'SFX_RENDER_LEVEL': 0,
                         'SFX_RENDER_PERCENTAGE': 1.0,
                         'SCENE_DETAIL': False,
                         'NEAR_VIEW_RANGE_FIX': 0.6,
                         'FAR_VIEW_RANGE_FIX': 0.6
                         },
   game3d.PLATFORM_ANDROID: {'TEXTURE_SKIP_LEVEL_SCENE': 2,
                             'TEXTURE_SKIP_LEVEL_SCENE_L1': 2,
                             'TEXTURE_SKIP_LEVEL_PLAYER': 1,
                             'simple_vertex_stream_tech_names': ('shader\\lightmap.fx::TShader', 'shader\\lightmap_high.fx::TShader', 'shader\\lightmap93.fx::TShader',
 'shader\\lightmap93_rock.fx::TShader', 'shader\\common_terrain_lightmap.fx::TShader',
 'shader\\xc_landscape_detail.fx::TerrainTech', 'shader\\impostor.fx::TShader', 'shader\\common_emission.fx::TShader',
 'shader\\common_lightmap.fx::TShader', 'shader\\common_ball_nx2_mobile.fx::TShader',
 'shader\\common_ball.fx::TShader'),
                             'SFX_RENDER_LEVEL': 0,
                             'SFX_RENDER_PERCENTAGE': 1.0,
                             'SCENE_DETAIL': False,
                             'NEAR_VIEW_RANGE_FIX': 0.6,
                             'FAR_VIEW_RANGE_FIX': 0.6
                             }
   }
LOW_PERF_MODE_SETTINGS = {game3d.PLATFORM_IOS: {'preload_extend_dist': 1950.0,
                         'preload_alway_y_min': 13000.0,
                         'SFX_RENDER_LEVEL': 0,
                         'SFX_RENDER_PERCENTAGE': 1.0,
                         'SCENE_DETAIL': False,
                         'NEAR_VIEW_RANGE_FIX': 1.0,
                         'FAR_VIEW_RANGE_FIX': 1.0
                         },
   game3d.PLATFORM_ANDROID: {'preload_extend_dist': 1950.0,
                             'preload_alway_y_min': 13000.0,
                             'SFX_RENDER_LEVEL': 0,
                             'SFX_RENDER_PERCENTAGE': 1.0,
                             'SCENE_DETAIL': False,
                             'NEAR_VIEW_RANGE_FIX': 1.0,
                             'FAR_VIEW_RANGE_FIX': 1.0
                             }
   }
SHADER_LOD_LEVEL_TYPES_LOW = {world.SHADER_LOD_TYPE_NORMAL: [
                                SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_LANDSCAPE: [
                                   SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_WATER: [
                               SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_SCENE_OBJ: [
                                   SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_CHAR: [
                              SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_PLAYER: [
                                SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_INVALID: [
                                 SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP]
   }
SHADER_LOD_LEVEL_TYPES_MED = {world.SHADER_LOD_TYPE_NORMAL: [
                                SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_LANDSCAPE: [
                                   SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_WATER: [
                               SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_SCENE_OBJ: [
                                   SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_CHAR: [
                              SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_PLAYER: [
                                SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_INVALID: [
                                 SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP]
   }
SHADER_LOD_LEVEL_TYPES_DEFAULT = {world.SHADER_LOD_TYPE_NORMAL: [
                                SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_LANDSCAPE: [
                                   SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_WATER: [
                               SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_SCENE_OBJ: [
                                   SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_CHAR: [
                              SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_PLAYER: [
                                SHADER_LOD_LEVEL_2, SHADER_LOD_LEVEL_1, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP],
   world.SHADER_LOD_TYPE_INVALID: [
                                 SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_0, SHADER_LOD_LEVEL_TOP]
   }
if game3d.get_platform() == game3d.PLATFORM_ANDROID:
    SWITCHER.update({'SFX_RENDER_LEVEL': [0, 0, 2, 4, 4]})
    if global_data.enable_scale_resolution:
        SWITCHER.update({'RESOLUTION': [0.6, 0.7, 0.8, 1.0, 1.0]})
    else:
        SWITCHER.update({'RESOLUTION': [0.4, 0.5, 0.7, 0.8, 0.8]})
elif game3d.get_platform() == game3d.PLATFORM_IOS:
    import device_compatibility
    if device_compatibility.ios_need_reduce_resolution():
        print('Some iOS device need to reduce resolution...')
        if global_data.enable_scale_resolution:
            SWITCHER.update({'RESOLUTION': [0.6, 0.7, 0.84, 1.0, 1.0]})
        else:
            SWITCHER.update({'RESOLUTION': [0.5, 0.67, 0.73, 0.73, 0.73]})
else:
    print('PC dont need to scale resolution, enable_scale_resolution:%s' % global_data.enable_scale_resolution)
print('RESOLUTION config:%s =====' % SWITCHER.get('RESOLUTION', None))
USER_CUSTOM_DEFAULT_SETTINGS = {uoc.QUALITY_RESOLUTION_KEY: (0, 1, 2, 3, 4),
   uoc.QUALITY_RESOLUTION_KEY_KONGDAO: (0, 0, 0, 0, 0),
   uoc.QUALITY_SHADOWMAP_KEY: (0, 0, 0, 0, 0),
   uoc.QUALITY_HDR_KEY: (0, 0, 0, 1, 1),
   uoc.QUALITY_MSAA_KEY: (0, 0, 0, 0, 0),
   uoc.QUALITY_RADIAL_BLUR_KEY: (1, 1, 1, 1, 1),
   uoc.QUALITY_MEADOW_KEY: (0, 1, 2, 3, 3)
   }
USER_PC_CUSTOM_DEFAULT_SETTINGS = {uoc.QUALITY_RESOLUTION_KEY: (0, 1, 2, 3, 4),
   uoc.QUALITY_RESOLUTION_KEY_KONGDAO: (0, 1, 2, 3, 4),
   uoc.QUALITY_SHADOWMAP_KEY: (0, 0, 0, 1, 1),
   uoc.QUALITY_HDR_KEY: (0, 0, 0, 1, 1),
   uoc.QUALITY_MSAA_KEY: (0, 0, 0, 2, 2),
   uoc.QUALITY_RADIAL_BLUR_KEY: (1, 1, 1, 1, 1),
   uoc.QUALITY_MEADOW_KEY: (1, 2, 3, 3, 3)
   }
USER_CUSTOM_SETTINGS = {'RESOLUTION': SWITCHER.get('RESOLUTION'),
   'MSAA': (1, 2, 4)
   }
USER_CUSTOM_MAP = {'RESOLUTION': uoc.QUALITY_RESOLUTION_KEY,
   'RESOLUTION_KONGDAO': uoc.QUALITY_RESOLUTION_KEY_KONGDAO,
   'SHADOWMAP_ENABLE': uoc.QUALITY_SHADOWMAP_KEY,
   'hdr': uoc.QUALITY_HDR_KEY,
   'msaa2x': uoc.QUALITY_MSAA_KEY,
   'msaa4x': uoc.QUALITY_MSAA_KEY,
   'HIGH_FRAME_RATE': uoc.QUALITY_HIGH_FRAME_RATE_KEY,
   'radial_blur': uoc.QUALITY_RADIAL_BLUR_KEY
   }
LOD_NAME_MAP = {'h': 'h_low',
   'l': 'l_low',
   'l1': 'l1_low',
   'l2': 'l2_low',
   'l3': 'l3_low',
   'l4': 'l4_low'
   }
CUR_FIX_WIDTH = -1
CUR_FIX_HEIGHT = -1

class GlobalDisplaySeting(Singleton):
    ALIAS_NAME = 'gsetting'

    def init(self):
        super(GlobalDisplaySeting, self).init()
        self.init_platform_setting()
        self._inited = False
        self._scn_setup_inited = False
        self.resolution_level = 2
        self._is_in_pve_scene = False
        self._quality = self.get_default_quality()
        self.actual_quality = self.get_default_quality()
        self._pve_quality = self.get_default_quality()
        self.actual_pve_quality = self.get_default_quality()
        self._cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_DEFAULT
        self._actual_shadowmap_enable = False
        self._shadowmap_inited = False
        self.resolution_last_set = None
        self._check_resolution_timer = None
        self._load_from_disk()
        self.set_actual_quality()
        self.set_ignore_mtl_ctrl_list()
        render.load_image_meta('img.meta')
        self._func_default_tex_quality = self.high_quality_tex_off
        if global_data.feature_mgr.is_model_lod_offset_ready():
            SWITCHER['MAX_LOD_MESH_OFFSET'][0] = 1
        self.init_event()
        self.init_meadow_quality()
        self.last_user_op_time = get_time()
        self.save_energy_timer = global_data.game_mgr.get_logic_timer().register(func=self.check_save_energy_mode, interval=5.0, mode=CLOCK)
        if game3d.get_platform() == game3d.PLATFORM_ANDROID or game3d.get_platform() == game3d.PLATFORM_IOS:
            self.detect_reset_resolution_timer = global_data.game_mgr.get_logic_timer().register(func=self.detect_reset_resolution, interval=10.0, mode=CLOCK)
        return

    def set_in_pve_scene(self, is_in_pve_scene):
        self._is_in_pve_scene = is_in_pve_scene

    def init_event(self):
        global_data.emgr.avatar_finish_create_event += self.on_avatar_finish_create
        global_data.emgr.set_mecha_effect_level += self.on_mecha_effect_level

    def check_save_energy_mode(self):
        if not global_data.enable_save_energy_mode:
            return
        clock = get_time()
        if clock - self.last_user_op_time > global_data.save_energy_duration:
            self.set_save_energy_mode(True)

    def set_save_energy_mode(self, enable):
        if not global_data.enable_save_energy_mode:
            return
        if pc_platform_utils.is_pc_hight_quality_simple():
            return
        if not enable:
            self.last_user_op_time = get_time()
        if enable == global_data.in_save_energy_mode:
            return
        if enable and global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_in_spectate():
            return
        if enable:
            pass
        global_data.in_save_energy_mode = enable
        scn = world.get_active_scene()
        if scn and hasattr(scn, 'force_setup_posteffect'):
            scn.force_setup_posteffect()
        global_data.display_agent.do_check_reset_resolution()

    def detect_reset_resolution(self):
        if not self.is_resolution_consistency():
            global_data.display_agent.do_check_reset_resolution()

    def on_avatar_finish_create(self):
        if self._shadowmap_inited:
            return
        fps_level = self.quality_value('HIGH_FRAME_RATE')
        enable_shadow = self.quality_value('SHADOWMAP_ENABLE')
        enable_shadow = True if enable_shadow and (fps_level < 2 or pc_platform_utils.is_pc_hight_quality_simple()) else False
        print('No rebuild for shadowmap...')
        world.enable_shadowmap(enable_shadow, False, False)
        self.actual_shadowmap_enabled = enable_shadow
        self._shadowmap_inited = True
        print('GlobalDisplaySeting EnableShadowMap:%s...' % self.actual_shadowmap_enabled)
        enable_radial_blur = global_data.player.get_setting(uoc.QUALITY_RADIAL_BLUR_KEY)
        global_data.display_agent.set_radial_blur_active(enable_radial_blur)

    def is_scn_setup_inited(self):
        return self._scn_setup_inited

    def set_scn_setup_inited(self, flag):
        self._scn_setup_inited = flag

    @property
    def actual_shadowmap_enabled(self):
        return self._actual_shadowmap_enable

    @actual_shadowmap_enabled.setter
    def actual_shadowmap_enabled(self, enable):
        self._actual_shadowmap_enable = enable

    def set_actual_quality(self):
        device_warning = six.moves.builtins.__dict__.get('DEVICE_WARNING', False)
        is_pc_quality = pc_platform_utils.is_pc_hight_quality_simple()
        if game3d.get_frame_rate() >= 90 and not is_pc_quality:
            LIMIT = FAST
        elif global_data.is_low_mem_mode:
            LIMIT = FAST
        else:
            LIMIT = FINE if device_warning else FANTASY_PC
        act_value = min(LIMIT, max(0, self._quality))
        self.actual_quality = act_value
        act_value = min(LIMIT, max(0, self._pve_quality))
        self.actual_pve_quality = act_value

    def _load_from_disk(self):
        conf = global_data.achi_mgr.get_general_archive_data()
        self._quality = conf.get_field('quality', self._quality)
        self._pve_quality = conf.get_field('pve_quality', self._quality)

    def _save_to_disk(self):
        conf = global_data.achi_mgr.get_general_archive_data()
        conf.set_field('quality', self._quality)
        conf.set_field('pve_quality', self._pve_quality)

    def quality_process(self):
        self.process_low_device_settings()
        self.set_actual_quality()
        if self._is_in_pve_scene:
            global_data.emgr.display_quality_change.emit(self.actual_pve_quality)
        else:
            global_data.emgr.display_quality_change.emit(self.actual_quality)
        self._save_to_disk()
        self.apply_scene_quality()
        self.apply_shader_lod()
        if self._is_in_pve_scene:
            quality = self.actual_pve_quality
        else:
            quality = self.actual_quality
        global_data.sound_mgr.set_sound_quality(quality)
        if hasattr(render, 'enable_shading_rate') and global_data.player:
            cur_mecha_effect_level = global_data.player.get_setting_2(QUALITY_MECHA_EFFECT_LEVEL_KEY)
            if cur_mecha_effect_level != MECHA_EFFECT_LEVEL_ULTRA and SWITCHER['ENABLE_SHADING_RATE'][quality]:
                render.enable_shading_rate(True)
            else:
                render.enable_shading_rate(False)

    def on_mecha_effect_level(self, cur_mecha_effect_level, is_avatar=True):
        if hasattr(render, 'enable_shading_rate') and is_avatar:
            if self._is_in_pve_scene:
                quality = self.actual_pve_quality
            else:
                quality = self.actual_quality
            if cur_mecha_effect_level != MECHA_EFFECT_LEVEL_ULTRA and SWITCHER['ENABLE_SHADING_RATE'][quality]:
                render.enable_shading_rate(True)
            else:
                render.enable_shading_rate(False)

    def set_quality(self, value, force=False):
        value = min(FANTASY_PC, max(0, value))
        print('set display quality to ', value, 'current quality', self._quality)
        if self._quality != value or not self._inited or force:
            self._quality = value
            self.quality_process()
            self._inited = True

    def set_pve_quality(self, value, force=False):
        value = min(FANTASY_PC, max(0, value))
        print('set display quality to ', value, 'current quality', self._quality)
        if self._pve_quality != value or not self._inited or force:
            self._pve_quality = value
            self.quality_process()
            self._inited = True

    def get_quality(self):
        return self._quality

    def get_pve_quality(self):
        return self._pve_quality

    def get_actual_quality(self):
        if self._is_in_pve_scene:
            return self.actual_pve_quality
        else:
            return self.actual_quality

    def get_seting_quality(self):
        if self._is_in_pve_scene:
            return self._pve_quality
        else:
            return self._quality

    def get_normal_type_lod_level(self):
        now_lod_level_lst = self._cur_shader_lod_level.get(world.SHADER_LOD_TYPE_NORMAL, [])
        quality = self.get_actual_quality()
        if quality < len(now_lod_level_lst):
            return now_lod_level_lst[quality]
        else:
            return SHADER_LOD_LEVEL_0

    def get_default_quality(self):
        import device_compatibility
        default_quality, default_reso, fps = device_compatibility.get_default_quality_and_resolution()
        default_val = default_quality
        return default_val

    def apply_scene_quality(self, scene=None, postprocess=True):
        import world
        import device_compatibility
        quality = self.get_actual_quality()
        enable_detail = self.quality_value('SCENE_DETAIL')
        if enable_detail:
            world.show_scene_detail()
        else:
            world.hide_scene_detail()
        world.set_model_fadein_when_load(self.quality_value('MODEL_FADE_IN'))
        self.apply_scene_sfx(scene)
        if not self._inited:
            self._func_default_tex_quality()
        world.enable_fogtex_shader(self.quality_value('FOGTEX_ENABLE'))
        scn = world.get_active_scene() if scene is None else scene
        if scn and hasattr(scn, 'is_battle_scene') and scn.is_battle_scene() and global_data.game_mode and global_data.game_mode.get_enviroment() == 'kongdao':
            world.set_model_lod_offset(0)
        else:
            world.set_model_lod_offset(self.quality_value('MAX_LOD_MESH_OFFSET'))
        if scn is None:
            return
        else:
            if hasattr(scn, 'setup_display'):
                scn.setup_display(postprocess)
            world.set_effect_quality(self.quality_value('EFFECT_SHADER_LEVEL'), False)
            return

    def reset_lodoffset(self):
        world.set_model_lod_offset(self.quality_value('MAX_LOD_MESH_OFFSET'))

    def apply_shader_lod(self, scene=None, display_tag=False):
        import device_compatibility
        scn = world.get_active_scene() if scene is None else scene
        if scn is None:
            return
        else:
            display_switch = False
            perf_flag = device_compatibility.get_device_perf_flag()
            cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_DEFAULT
            if perf_flag in (device_compatibility.PERF_FLAG_ANDROID_LOW, device_compatibility.PERF_FLAG_IOS_LOW):
                cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_LOW
                display_switch = False
            elif perf_flag in (device_compatibility.PERF_FLAG_ANDROID_MED,):
                cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_MED
                display_switch = False
            else:
                cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_DEFAULT
                display_switch = True
            if global_data.debug_perf_switch_global:
                shader_lod_cfg = global_data.get_debug_perf_val('shader_lod_cfg', cur_shader_lod_level)
                if shader_lod_cfg == 0:
                    cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_LOW
                elif shader_lod_cfg == 1:
                    cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_MED
                elif shader_lod_cfg == 2:
                    cur_shader_lod_level = SHADER_LOD_LEVEL_TYPES_DEFAULT
            quality_temple = self.get_actual_quality()
            if display_switch and display_tag:
                display_quality = 2
                quality = max(display_quality, quality_temple)
            else:
                quality = quality_temple
            self._cur_shader_lod_level = cur_shader_lod_level
            for lod_type, lod_confs in six.iteritems(cur_shader_lod_level):
                scn.set_shader_lod_level(lod_type, lod_confs[quality])

            fast_mode = False
            if hasattr(scn, 'is_battle_scene') and scn.is_battle_scene():
                if global_data.enable_fast_material and (not is_win32() or version.get_tag() == 'trunk'):
                    fast_mode = self.get_actual_quality() < FANTASY
            scn.set_macros({'ENABLE_FAST_MODE': '1' if fast_mode else '0'})
            return

    def apply_sfx_lod_config(self, enable):
        if not global_data.enable_sfx_lod:
            return
        if global_data.feature_mgr.is_support_sfx_lod() and hasattr(world, 'set_sfx_update_frame_lod'):
            if enable:
                cfg = self.quality_value('SFX_UPDATE_FRAME_LOD')
            else:
                cfg = ()
            if cfg:
                world.set_sfx_update_frame_lod(cfg)
        if global_data.feature_mgr.is_support_sfx_lod() and hasattr(world, 'set_sfx_render_level_lod'):
            if enable:
                cfg = self.quality_value('SFX_RENDER_LEVEL_LOD')
            else:
                cfg = ()
            if cfg:
                world.set_sfx_render_level_lod(cfg)

    def apply_scene_sfx(self, scene=None):
        from logic.gutils.scene_utils import is_in_lobby, is_lobby_relatived_scene
        sfx_lv = self.quality_value('SFX_RENDER_LEVEL')
        if global_data.debug_perf_switch_global:
            sfx_lv = global_data.get_debug_perf_val('sfx_render_level', sfx_lv)
        world.set_sfx_render_level(sfx_lv)
        if scene and (is_in_lobby(scene.scene_type) or is_lobby_relatived_scene(scene.scene_type)):
            self.apply_sfx_lod_config(False)
        else:
            self.apply_sfx_lod_config(True)
        value = self.quality_value('SFX_RENDER_PERCENTAGE')
        if not global_data.feature_mgr.is_emitter_show_nothing_fixed():
            if scene and is_lobby_relatived_scene(scene.scene_type):
                value = 1.0
        world.set_sprites_percent(value)

    def is_posteffect_enable(self, name):
        custom_key = USER_CUSTOM_MAP.get(name, None)
        if custom_key and global_data.player:
            setting_val = global_data.player.get_setting(custom_key)
            if name == 'msaa2x':
                return setting_val == 1
            if name == 'msaa4x':
                return setting_val == 2
            if name == 'hdr':
                return setting_val == 1 and game3d.get_frame_rate() < 90
        quality = self.get_actual_quality()
        return name in GLOBAL_POSTEFFECT[quality]

    def quality_value(self, key):
        import device_compatibility
        from logic.comsys.setting_ui.SettingWidget import QualitySettingWidget
        custom_key = USER_CUSTOM_MAP.get(key, None)
        if custom_key:
            if global_data.player:
                setting_val = global_data.player.get_setting(custom_key, False)
                if custom_key == uoc.QUALITY_HIGH_FRAME_RATE_KEY:
                    setting_val = QualitySettingWidget.cal_ios_fps_level(setting_val)
                if custom_key in [uoc.QUALITY_RESOLUTION_KEY, uoc.QUALITY_RESOLUTION_KEY_KONGDAO]:
                    if global_data.enable_resolution_switch:
                        return setting_val
                    setting_val = USER_CUSTOM_SETTINGS.get('RESOLUTION', (1.0, 1.0,
                                                                          1.0, 1.0))[setting_val]
                return setting_val
            print('No player now, get quality value failed......', key, custom_key)
            if global_data.enable_resolution_switch:
                if custom_key == uoc.QUALITY_RESOLUTION_KEY:
                    return 2
                else:
                    if custom_key == uoc.QUALITY_RESOLUTION_KEY_KONGDAO:
                        return 0
                    return 2

        low_mem_val = LOW_MEM_MODE_SETTINGS.get(global_data.cur_platform, {}).get(key, None)
        if global_data.is_low_mem_mode and low_mem_val is not None:
            return low_mem_val
        else:
            low_perf_val = LOW_PERF_MODE_SETTINGS.get(global_data.cur_platform, {}).get(key, None)
            if global_data.is_low_perf_mode and low_perf_val is not None:
                return low_perf_val
            quality = self.get_actual_quality()
            return SWITCHER[key][quality]

    def process_low_device_settings(self):
        import profiling
        import device_compatibility
        from logic.client.const import game_mode_const
        mem = profiling.get_total_memory()
        vcard = profiling.get_video_card_name().strip().lower()
        self.apply_low_memory_setting()
        if not global_data.is_low_mem_mode:
            if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
                self.apply_low_performance_setting(True, vcard)
            elif device_compatibility.is_device_gpu_qualified():
                self.apply_low_performance_setting(False, vcard)
            else:
                self.apply_low_performance_setting(True, vcard)

    def apply_low_performance_setting(self, enable, vcard):
        if enable:
            print('The device gpu:%s has low performace, enter Low-Performance Mode......' % vcard)
        global_data.is_low_perf_mode = enable
        if enable:
            cur_preload_extend_dist = global_data.preload_extend_dist_low
            cur_preload_alway_y_min = global_data.preload_alway_y_min_low
        else:
            cur_preload_extend_dist = global_data.preload_extend_dist_normal
            cur_preload_alway_y_min = global_data.preload_alway_y_min_normal
        scn = world.get_active_scene()
        if scn:
            scn.set_preload_dynamic_args(cur_preload_extend_dist, cur_preload_alway_y_min)
        global_data.sfx_mgr.enable_sfx_pool = True
        global_data.model_mgr.enable_model_pool = True
        self._func_default_tex_quality()
        if game3d.get_render_device() != game3d.DEVICE_METAL:
            world.enable_vertex_stream(0, True)
            world.enable_vertex_stream(1, True)
            world.enable_vertex_stream(2, True)

    def apply_low_memory_setting(self):
        enable = global_data.is_low_mem_mode
        if enable:
            print('The device has low memory capacity, enter Low-Mem Mode......')
        global_data.sfx_mgr.enable_sfx_pool = not enable
        global_data.model_mgr.enable_model_pool = not enable
        if enable:
            cur_preload_extend_dist = global_data.preload_extend_dist_low
            cur_preload_alway_y_min = global_data.preload_alway_y_min_low
        else:
            cur_preload_extend_dist = global_data.preload_extend_dist_normal
            cur_preload_alway_y_min = global_data.preload_alway_y_min_normal
        scn = world.get_active_scene()
        if scn:
            scn.set_preload_dynamic_args(cur_preload_extend_dist, cur_preload_alway_y_min)
        if global_data.is_low_mem_mode:
            print('No discard_vertex_streams for some crashes.')
            discard_vertex_streams = False
            if game3d.get_platform() == game3d.PLATFORM_IOS and global_data.is_med_mem_mode:
                discard_vertex_streams = False
            if game3d.get_render_device() == game3d.DEVICE_METAL:
                discard_vertex_streams = False
        else:
            discard_vertex_streams = False
        if discard_vertex_streams:
            world.enable_vertex_stream(0, not enable)
            world.enable_vertex_stream(1, not enable)
            world.enable_vertex_stream(2, not enable)
            if enable:
                simple_techs = LOW_MEM_MODE_SETTINGS.get(global_data.cur_platform, {}).get('simple_vertex_stream_tech_names', ())
                for tech_name in simple_techs:
                    print('use simple vertex stream in low-mem mode for tech:%s......' % tech_name)
                    world.add_simple_stream_tech_name(tech_name)

        if enable:
            if hasattr(render, 'add_simple_stream_ignore_texture'):
                import logic.client.const.simple_stream_ignore_textures as ignore
                for tex_path in ignore.ignore_list:
                    render.add_simple_stream_ignore_texture(tex_path)

    def init_platform_setting(self):
        import C_file
        if C_file.find_res_file('__artist__', ''):
            render.set_texture_suffix('')
            game3d.set_res_object_cache(False)
            if hasattr(game3d, 'set_resource_cache'):
                game3d.set_resource_cache(False)
            game3d.clear_resource_cache()
        if hasattr(render, 'enable_texture_merge'):
            render.enable_texture_merge(False)
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            render.set_texture_suffix('.ktx')

    def set_detail_setting_resolution(self, level):
        info = USER_CUSTOM_SETTINGS.get('RESOLUTION', None)
        print('set detail setting resolution', level, info)
        self.resolution_level = level
        if info:
            global_data.display_agent.do_check_reset_resolution()
        return

    def set_detail_setting_msaa(self, level):
        if pc_platform_utils.is_pc_hight_quality() and global_data.is_ue_model:
            global_data.display_agent.set_aa_level(level)
        else:
            import device_compatibility
            scn = world.get_active_scene()
            if not scn:
                return
            if not device_compatibility.can_use_msaa():
                scn.set_msaa(1)
                self.refresh_hdr()
                return
            info = USER_CUSTOM_SETTINGS.get('MSAA', None)
            if info:
                msaa_level = info[level]
                scn.set_msaa(msaa_level)
                self.refresh_hdr()
            return
        return

    def refresh_hdr(self):
        scn = world.get_active_scene()
        if scn:
            if global_data.cur_thermal_state >= 3:
                scn.enable_hdr(False)
            elif self.is_posteffect_enable('hdr'):
                scn.enable_hdr(True)
            else:
                scn.enable_hdr(False)

    def set_default_quality_to_high(self, enable):
        if enable:
            self._func_default_tex_quality = self.high_quality_tex_on
        else:
            self._func_default_tex_quality = self.high_quality_tex_off

    def high_quality_tex_on(self):
        import data.image_tag
        skip_level_player = self.quality_value('TEXTURE_SKIP_LEVEL_PLAYER')
        if global_data.debug_perf_switch_global:
            skip_level_player = global_data.get_debug_perf_val('texture_skip_level_player', skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_TEX_2048, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_TEX, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_MATERIAL, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_NORMAL, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_TEX_2048, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_TEX, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_MATERIAL, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_NORMAL, 0 + skip_level_player)
        skip_level_scene = self.quality_value('TEXTURE_SKIP_LEVEL_SCENE')
        skip_level_scene_l = self.quality_value('TEXTURE_SKIP_LEVEL_SCENE_L1')
        if global_data.is_low_mem_mode and global_data.game_mode and not global_data.game_mode.is_kongdao_scene():
            skip_level_scene = min(1, skip_level_scene)
            skip_level_scene_l = min(1, skip_level_scene_l)
            print('[On] No low mem mip skip for non-kongdao...', skip_level_scene, skip_level_scene_l)
        if global_data.debug_perf_switch_global:
            skip_level_scene = global_data.get_debug_perf_val('texture_skip_level_scene', skip_level_scene)
            skip_level_scene_l = global_data.get_debug_perf_val('texture_skip_level_scene', skip_level_scene_l)
        render.set_texture_skip_level_by_tag(data.image_tag.SCENE_TEX, skip_level_scene)
        if hasattr(data.image_tag, 'SCENE_TEX_L1'):
            render.set_texture_skip_level_by_tag(data.image_tag.SCENE_TEX_L1, skip_level_scene_l)

    def high_quality_tex_off(self):
        import data.image_tag
        if pc_platform_utils.is_pc_hight_quality():
            self.high_quality_tex_on()
            return
        skip_level_player = self.quality_value('TEXTURE_SKIP_LEVEL_PLAYER')
        if global_data.debug_perf_switch_global:
            skip_level_player = global_data.get_debug_perf_val('texture_skip_level_player', skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_TEX, 0 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_TEX_2048, 1 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_MATERIAL, 1 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.MECHA_NORMAL, 1 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_TEX, 1 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_TEX_2048, 2 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_MATERIAL, 1 + skip_level_player)
        render.set_texture_skip_level_by_tag(data.image_tag.CHAR_NORMAL, 0 + skip_level_player)
        skip_level_scene = self.quality_value('TEXTURE_SKIP_LEVEL_SCENE')
        skip_level_scene_l = self.quality_value('TEXTURE_SKIP_LEVEL_SCENE_L1')
        if global_data.is_low_mem_mode and global_data.game_mode and not global_data.game_mode.is_kongdao_scene():
            skip_level_scene = min(1, skip_level_scene)
            skip_level_scene_l = min(1, skip_level_scene_l)
            print('[Off] No low mem mip skip for non-kongdao...', skip_level_scene, skip_level_scene_l)
        if global_data.debug_perf_switch_global:
            skip_level_scene = global_data.get_debug_perf_val('texture_skip_level_scene', skip_level_scene)
            skip_level_scene_l = global_data.get_debug_perf_val('texture_skip_level_scene', skip_level_scene_l)
        render.set_texture_skip_level_by_tag(data.image_tag.SCENE_TEX, skip_level_scene)
        if hasattr(data.image_tag, 'SCENE_TEX_L1'):
            render.set_texture_skip_level_by_tag(data.image_tag.SCENE_TEX_L1, skip_level_scene_l)

    def get_resolution_device_type(self):
        import device_compatibility
        dev_type = DEVICE_TYPE_PC
        if global_data.is_android_pc or global_data.is_in_mumu:
            return DEVICE_TYPE_PC
        if not device_compatibility.is_device_gpu_qualified():
            dev_type = DEVICE_TYPE_LOW_PERF
        elif game3d.get_platform() == game3d.PLATFORM_ANDROID and not global_data.is_android_pc:
            if device_compatibility.is_ppi_qualified() or not device_compatibility.is_device_highend():
                dev_type = DEVICE_TYPE_ANDROID_NORMAL
            else:
                dev_type = DEVICE_TYPE_ANDROID_LOW_PPI
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            if device_compatibility.is_ppi_qualified():
                dev_type = DEVICE_TYPE_IOS_NORMAL
            else:
                dev_type = DEVICE_TYPE_IOS_LOW_PPI
        else:
            dev_type = DEVICE_TYPE_PC
        return dev_type

    def get_resolution_scene_type(self):
        from logic.gutils.scene_utils import is_lobby_relatived_scene, is_in_lobby
        from logic.client.const import game_mode_const
        cur_scene = global_data.game_mgr.scene
        if cur_scene != world.get_active_scene():
            pass
        if not cur_scene:
            return RESO_SCENE_TYPE_GAME
        if cur_scene.scene_type == 'Main':
            return RESO_SCENE_TYPE_GAME
        if is_lobby_relatived_scene(cur_scene.scene_type):
            return RESO_SCENE_TYPE_SHOW
        if is_in_lobby(cur_scene.scene_type):
            return RESO_SCENE_TYPE_LOBBY
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
            return RESO_SCENE_TYPE_GAME_DEATH_MATCH
        return RESO_SCENE_TYPE_GAME

    def switch_device_resolution(self, force_set=False):
        global CUR_FIX_HEIGHT
        global CUR_FIX_WIDTH
        dev_type = self.get_resolution_device_type()
        if global_data.in_save_energy_mode:
            dev_type = DEVICE_TYPE_SAVE_ENERGY
        elif global_data.cur_thermal_state >= 3:
            dev_type = DEVICE_TYPE_THERMAL_STATE_HOT
        reso_scene_type = self.get_resolution_scene_type()
        quality = self.quality_value('RESOLUTION')
        if global_data.game_mode and global_data.game_mode.is_kongdao_scene() and not device_utils.check_vivo_device():
            quality = self.quality_value('RESOLUTION_KONGDAO')
            fix_height = RESOLUTION_CONFIG.get(dev_type, {}).get(reso_scene_type, {}).get(quality, -1)
        else:
            fix_height = RESOLUTION_CONFIG.get(dev_type, {}).get(reso_scene_type, {}).get(quality, -1)
        orig_width = global_data.really_window_size[0]
        orig_height = global_data.really_window_size[1]
        orig_ratio = global_data.really_window_ratio or float(orig_width) / float(orig_height)
        if fix_height == -1:
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                fix_height = game3d.get_window_size()[1]
            else:
                fix_height = orig_height
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            pass
        else:
            fix_height = int(min(orig_height, fix_height))
        fix_width = int(fix_height * orig_ratio)
        cur_width, cur_height, _, _, _ = game3d.get_window_size()
        if global_data.debug_perf_switch_global:
            fix_width = global_data.get_debug_perf_val('resolution_width', fix_width)
            fix_height = global_data.get_debug_perf_val('resolution_height', fix_height)
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if hasattr(game3d, 'set_window_size_force') and force_set:
                game3d.set_window_size_force(fix_width, fix_height + 3, 32, 1, 0, False)
                game3d.set_window_size_force(fix_width, fix_height, 32, 1, 0, False)
            else:
                ret = game3d.set_window_size(fix_width, fix_height, 32, 1, 0, False)
                print('switch_device_resolution == ret:', ret)
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            if fix_width != CUR_FIX_WIDTH or fix_height != CUR_FIX_HEIGHT:
                self.set_resolution_sync(fix_width, fix_height)
                CUR_FIX_WIDTH = fix_width
                CUR_FIX_HEIGHT = fix_height
        elif game3d.get_platform() == game3d.PLATFORM_WIN32:
            pass
        else:
            game3d.set_resolution(fix_width, fix_height)
        self.reset_frame_rate()
        self.resolution_last_set = (
         fix_width, fix_height)

    @sync_exec
    def set_resolution_sync(self, fix_width, fix_height):
        game3d.set_resolution(fix_width, fix_height)

    def reset_frame_rate(self):
        import device_compatibility
        scn = world.get_active_scene()
        fps_level = self.quality_value('HIGH_FRAME_RATE')
        if hasattr(scn, 'get_fps_strategy'):
            fps_strategy = scn.get_fps_strategy()
            is_high_fps = FPS_STRATEGY.get(fps_strategy, fps_level)
            fps_value = 30
            old_fps_value = game3d.get_frame_rate()
            if not is_high_fps:
                fps_value = 30
            elif fps_level >= 2:
                fps_value = pc_platform_utils.FPS_MODE[fps_level]
                if fps_value == 144:
                    if not global_data.is_pc_mode:
                        max_value = device_compatibility.get_max_screen_refresh_rate()
                        fps_value = min(max_value, fps_value)
            else:
                fps_value = 60
            if old_fps_value != fps_value:
                flag = fps_value <= 60
                if flag is False:
                    flag = global_data.feature_mgr.is_support_anim_thread_for_ik()
                world.enable_animation_thread(flag)
                global_data.game_mgr.set_frame_rate(fps_value)
                self.set_quality(self.get_quality(), True)

    def get_resolution_last_set(self):
        return self.resolution_last_set

    def is_resolution_consistency(self):
        cur_w, cur_h, _, _, _ = game3d.get_window_size()
        if self.resolution_last_set:
            if abs(self.resolution_last_set[0] - cur_w) > 0.3 or abs(self.resolution_last_set[1] - cur_h) > 0.3:
                print('Resolution is not consistency.... last_set:(%s, %s), cur:(%s, %s)' % (
                 self.resolution_last_set[0], self.resolution_last_set[1], cur_w, cur_h))
                return False
        return True

    def process_switch_resolution_consistency(self):
        if self._check_resolution_timer is not None:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(self._check_resolution_timer)
            self._check_resolution_timer = None
        self._check_resolution_timer = global_data.game_mgr.get_logic_timer().register(func=lambda : self.switch_device_resolution(), times=3, mode=CLOCK, interval=0.5)
        return

    def set_ignore_mtl_ctrl_list(self):
        if hasattr(render, 'add_ignore_mtl_ctrl_tech'):
            import logic.client.const.ignore_mtl_controller_list as ignore
            for tech_path in ignore.ignore_list:
                render.add_ignore_mtl_ctrl_tech(tech_path)

    def get_graphics_style(self):
        return global_data.player.get_setting(uoc.GRAPHICS_STYLE_TYPE)

    def get_real_graphics_style(self):
        if not global_data.player:
            return 2
        graphics_style = global_data.player.get_setting(uoc.GRAPHICS_STYLE_TYPE)
        if hasattr(global_data.game_mode, 'is_snow_res') and global_data.game_mode.is_snow_res() and graphics_style == 3:
            graphics_style = 2
        return graphics_style

    def get_cur_redict_scale(self):
        if global_data.player:
            redirect_scale_level = global_data.player.get_setting(uoc.PC_REDIRECT_SCALE)
            redirect_scale = uoc.PC_REDIRECT_RANGE[redirect_scale_level]
        else:
            redirect_scale = 1.0
        return redirect_scale

    def get_aa_level(self):
        if global_data.player:
            aa_level = global_data.player.get_setting(uoc.QUALITY_MSAA_KEY)
        else:
            aa_level = 0
        return aa_level

    def set_graphics_style(self, style):
        global_data.player.write_setting(uoc.GRAPHICS_STYLE_TYPE, style)
        self.refresh_graphics()

    def refresh_graphics(self):
        scn = world.get_active_scene()
        if scn:
            scn.refresh_graphics_style()

    def init_meadow_quality(self):
        self._meadow_quality = 0
        conf = global_data.achi_mgr.get_general_archive_data()
        self._meadow_quality = conf.get_field('meadow_quality', None)
        if self._meadow_quality is not None:
            return
        else:
            self._meadow_quality = self.get_default_meadow_quality()
            return

    def set_meadow_quality(self, quality):
        if not global_data.enable_meadow:
            return
        if global_data.player:
            global_data.player.write_setting(uoc.QUALITY_MEADOW_KEY, quality)
        global_data.emgr.set_meadow_quality.emit(quality)

    def get_meadow_quality(self):
        if global_data.player:
            val = global_data.player.get_setting(uoc.QUALITY_MEADOW_KEY, default=self.get_default_meadow_quality())
        else:
            val = self.get_default_meadow_quality()
        return val

    def get_default_meadow_quality(self):
        default_setting = pc_platform_utils.is_pc_hight_quality() or USER_CUSTOM_DEFAULT_SETTINGS if 1 else USER_PC_CUSTOM_DEFAULT_SETTINGS
        return default_setting.get(uoc.QUALITY_MEADOW_KEY, self.get_actual_quality())

    def mapping_mecha_lod_name(self, name):
        quality = self.get_actual_quality()
        if quality >= NORMAL or global_data.disable_low_model:
            return name
        return LOD_NAME_MAP[name]