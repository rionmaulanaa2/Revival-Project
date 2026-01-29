# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/IngameManagerAgent.py
from __future__ import absolute_import
from __future__ import print_function
import os
from logic.manager_agents import ManagerAgentBase
import world
import render
import game3d
import version
import profiling
import C_file
from common.cfg import confmgr
from common.platform import is_win32, is_ios
from patch import patch_path

class IngameManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'ingame_mgr_agent'

    def init(self, *args):
        super(IngameManagerAgent, self).init()
        self.init_ingame_event()
        from common.utils.sfxmgr import SfxMgr, BulletSfxMgr
        SfxMgr()
        BulletSfxMgr()
        from common.utils.modelmgr import ModelMgr
        ModelMgr()
        from logic.gcommon.component.system.ComSystemMgr import g_com_sysmgr
        g_com_sysmgr.setup_all_system()
        self.init_move_mgr()
        self.init_red_point()
        self.init_voice()
        self.init_game_voice()
        self.init_ui_rt()
        self.init_hubble()
        self.init_caches()
        if global_data.sound_mgr:
            global_data.sound_mgr.reload()
        self.init_game_collision()
        self.init_ui_distor_helper()
        self.init_ccmini()
        self.init_message_data()
        from logic.gcommon.const import SKELETON_LOD_DIST
        world.set_skeleton_distances(SKELETON_LOD_DIST[0], SKELETON_LOD_DIST[1])
        from logic.gutils.dress_utils import init_dress_merge_sys
        init_dress_merge_sys()
        self.init_share_manager()
        self._init_perform_sdk()
        if type(world.enable_async_animation_loading) != bool:
            world.enable_async_animation_loading()
        if hasattr(world, 'enable_animation_thread'):
            if not global_data.feature_mgr.is_support_animation_thread():
                flag = False
            elif is_win32():
                flag = True
            elif is_ios():
                flag = True
            else:
                flag = True
            from common.platform.dctool import interface
            if not global_data.feature_mgr.is_support_debug_multi_thread_anim():
                flag = False
            print('world.enable_animation_thread go force closed %s...' % flag)
            world.enable_animation_thread(flag)
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            world.set_acl_anim_mode(True)
        if hasattr(world, 'set_lod_fade_info'):
            print('world.set_lod_fade_info run...')
            if global_data.feature_mgr.is_support_preload_lod():
                world.set_lod_fade_info(True, 0, 0, 0, 0, 0, 0)
            else:
                world.set_lod_fade_info(True, 0.5, 0.5, 0.5, 0.25, 0.5, 0.25)
        if hasattr(world, 'set_model_culling_screen_ratio'):
            print('world.set_model_culling_screen_ratio forbid run...')
            world.set_model_culling_screen_ratio(0, 0)
        if global_data.enable_csm_range_center and hasattr(render, 'enable_csm_range_center'):
            from logic.gcommon.const import NEOX_UNIT_SCALE
            print('render.enable_csm_range_center run...')
            render.enable_csm_range_center(True)
            scale = 1.0
            if is_win32():
                scale = global_data.shadowmap_range_pc_scalar
            csm_range_args = (5.0 * NEOX_UNIT_SCALE, 5.0 * NEOX_UNIT_SCALE, 5.0 * NEOX_UNIT_SCALE,
             15.0 * NEOX_UNIT_SCALE, 15.0 * NEOX_UNIT_SCALE, 15.0 * NEOX_UNIT_SCALE,
             15.0 * NEOX_UNIT_SCALE * scale, 10.0 * NEOX_UNIT_SCALE * scale, 15.0 * NEOX_UNIT_SCALE * scale,
             30.0 * NEOX_UNIT_SCALE * scale, 12.0 * NEOX_UNIT_SCALE * scale, 30.0 * NEOX_UNIT_SCALE * scale)
            render.set_csm_range_center_info(csm_range_args)
        if hasattr(world, 'replace_lightmap_path'):
            if global_data.force_replace_lightmap:
                print('world.replace_lightmap_path in low_mem_mode...', global_data.force_replace_lightmap_path)
                world.replace_lightmap_path(global_data.force_replace_lightmap_path)
        if global_data.feature_mgr.is_support_async_load_prior():
            prior = 1
            enable = True
            print('world.set_dynamic_preload_priority...', prior)
            world.set_dynamic_preload_priority(prior)
            print('world.enable_async_load_dist_prior...', enable)
            world.enable_async_load_dist_prior(enable)
        if global_data.feature_mgr.is_support_preload_lod():
            if hasattr(world, 'enable_preload_lod_chunk_visible'):
                world.enable_preload_lod_chunk_visible(True)
        self.init_win_hotkey()
        self.init_anticheat_utils()
        if global_data.ui_mgr:
            global_data.ui_mgr.reset_clear_tex_timer()
        render.enable_dynamic_culling(global_data.feature_mgr.is_support_dyculling())
        print('ENABLE DYNAMIC CULLING', global_data.feature_mgr.is_support_dyculling())
        self.init_thermal_check()

    def init_anticheat_utils(self):
        from common.utils.anticheat_utils import AnticheatUtils
        AnticheatUtils()

    def init_sfx_data_and_mesh_vertex_data_lru_cache_enabled(self):
        if global_data.is_editor_mode:
            return
        if global_data.feature_mgr.is_support_sfx_data_and_mesh_vertex_data_lru_cache():
            import profiling
            mem = profiling.get_total_memory()
            platform = game3d.get_platform()
            if platform == game3d.PLATFORM_ANDROID or platform == game3d.PLATFORM_IOS:
                if mem >= 6144:
                    world.enable_sfx_data_cache(True, 25)
                    world.enable_mesh_vertex_data_cache(100)
                elif mem >= 4096:
                    world.enable_sfx_data_cache(True, 10)
                    world.enable_mesh_vertex_data_cache(True, 50)
                else:
                    world.enable_sfx_data_cache(False)
                    world.enable_mesh_vertex_data_cache(False)
            elif platform == game3d.PLATFORM_WIN32:
                if mem >= 8192:
                    world.enable_sfx_data_cache(True, 400)
                    world.enable_mesh_vertex_data_cache(True, 120)
                elif mem >= 6144:
                    world.enable_sfx_data_cache(True, 200)
                    world.enable_mesh_vertex_data_cache(True, 60)
                elif mem >= 4096:
                    world.enable_sfx_data_cache(True, 100)
                    world.enable_mesh_vertex_data_cache(True, 30)
                else:
                    world.enable_sfx_data_cache(False)
                    world.enable_mesh_vertex_data_cache(False)
            else:
                world.enable_sfx_data_cache(False)
                world.enable_mesh_vertex_data_cache(False)

    def init_move_mgr(self):
        from logic.vscene.parts.keyboard.MoveKeyboardMgr import MoveKeyboardMgr
        MoveKeyboardMgr()

    def init_ingame_event(self):
        from logic import gevent

    def init_ccmini(self):
        from common.audio.ccmini_mgr import CCMiniMgr
        CCMiniMgr()

    def init_thermal_check(self):
        try:
            from common.utils.timer import CLOCK
            if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                if hasattr(game3d, 'set_thermal_status_listener_enable'):
                    enable = game3d.set_thermal_status_listener_enable(True)
                    if enable:
                        print('start_thermal_check for android succeed!')
                    else:
                        print('start_thermal_check failed for not supported!!')
            self._check_thermal_timer = global_data.game_mgr.register_logic_timer(self.on_check_thermal, interval=10, times=-1, mode=CLOCK)
            print('start_thermal_check started ...')
        except Exception as e:
            print('start_thermal_check exception:%s ...' % str(e))

    def init_voice(self):
        from logic.gutils.chat_utils import get_voice_mgr_type
        voice_mgr_type = get_voice_mgr_type()
        voice_mgr_type()

    def init_red_point(self):
        from common.utils.ui_redpoint_mgr import RedPointMgr
        RedPointMgr()

    def init_game_voice(self):
        from common.audio.game_voice_mgr import GameVoiceMgr
        GameVoiceMgr()

    def init_ui_rt(self):
        from common.uisys.UIRTManager import UIRTManager
        UIRTManager()

    def init_caches(self):
        from logic import caches
        caches.TrackCache()
        from logic.gutils.effect_cache import EffectCache
        EffectCache().init_behavior()
        from logic.vscene.parts.camera.CameraStatePool import CameraStatePool
        CameraStatePool()
        if not global_data.is_low_mem_mode:
            from logic.gutils.record_sprite_usage import UsageRecorder
            UsageRecorder()

    def init_hubble(self):
        from common.platform.hubble import Hubble
        Hubble()

    def init_game_collision(self):
        import collision
        from logic.gcommon.common_const.collision_const import TERRAIN_GROUP, WATER_GROUP, WATER_MASK, ROAD_GROUP, TERRAIN_MASK, ROAD_MASK
        collision.set_terrain_group_and_filter(TERRAIN_GROUP, TERRAIN_MASK)
        collision.set_road_group_and_filter(ROAD_GROUP, ROAD_MASK)
        if hasattr(collision, 'set_water_group_and_filter'):
            collision.set_water_group_and_filter(WATER_GROUP, WATER_MASK)
        collision.set_default_group_and_filter(-1, -1)
        collision.set_default_visible_model_group_and_filter(-1, -1)
        collision.set_default_invisible_model_group_and_filter(-1, -1)
        collision.enable_collision_group(True)
        collision.write_mask_and_group(True)

    def init_ui_distor_helper(self):
        from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
        UIDistorterHelper()

    def init_message_data(self):
        from logic.comsys.message.message_data import MessageData
        MessageData()
        global_data.message_data.reset()

    def init_share_manager(self):
        from logic.comsys.share.ShareManager import ShareManager
        ShareManager()

    def init_win_hotkey(self):
        if is_win32():
            from common.utils import hotkey
            hotkey.set_hotkey()
            import logic.gutils.hiding_edit
            logic.gutils.hiding_edit.register_keys()

    def _init_perform_sdk(self):
        if global_data.enable_perform_sdk:
            from common.platform.perform_sdk import query_perform_sdk_valid
            query_perform_sdk_valid()

    def on_check_thermal(self):
        if global_data.cur_thermal_state_debug > 0:
            thermal_state = global_data.cur_thermal_state_debug
            global_data.last_thermal_state = global_data.cur_thermal_state
            global_data.cur_thermal_state = thermal_state
        else:
            thermal_state = self.get_thermal_state()
            global_data.last_thermal_state = global_data.cur_thermal_state
            global_data.cur_thermal_state = thermal_state
        if thermal_state >= 3:
            self.on_damn_hot(thermal_state)
        elif thermal_state <= 1:
            self.on_cool_down(thermal_state)

    def get_thermal_state(self):
        thermal_state = 0
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            if hasattr(profiling, 'get_thermal_state'):
                thermal_state = profiling.get_thermal_state()
        elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if hasattr(game3d, 'get_current_thermal_status'):
                thermal_state = game3d.get_current_thermal_status()
        else:
            thermal_state = 0
        return thermal_state

    def is_thermal_changed(self):
        return global_data.cur_thermal_state != global_data.last_thermal_state

    def on_damn_hot(self, thermal_state):
        if not self.is_thermal_changed():
            return
        print('[Thermal State go too hot] === %s ===' % thermal_state)
        if global_data.display_agent:
            global_data.display_agent.do_check_reset_resolution()
            global_data.display_agent.refresh_hdr()

    def on_cool_down(self, thermal_state):
        if not self.is_thermal_changed():
            return
        print('[Thermal State cool down] === %s ===' % thermal_state)
        if global_data.display_agent:
            global_data.display_agent.do_check_reset_resolution()
            global_data.display_agent.refresh_hdr()