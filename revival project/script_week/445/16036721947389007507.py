# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/gdata.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from collections import OrderedDict
import os
import C_file
import six.moves.builtins

def get_gdata():
    return global_data.lobby_player


class GData(object):

    def __init__(self):
        import world
        import game3d
        import sys
        self.clime_smooth_duration = 0
        self.clime_delay_time = 0
        self.clime_scale1 = 1
        self.clime_scale2 = 1
        self.debug_ar_ui = 0
        self.debug_gpu_skin = 1
        self.debug_water_motorcycle = 0
        self.debug_motorcycle = False
        self.debug_motorcycle_shake = 0
        self._test_motorcycle_anim = False
        self._global_data_keys = []
        self.singleton_map = OrderedDict()
        self.alias_map = {}
        __builtins__['global_data'] = self
        self.owner_entity = None
        self.ar_debug_two_tex_in_one_sprite = 1
        self.debug_ui = False
        self.user_name = ''
        self.cam_lplayer = None
        self.cam_lctarget = None
        self.lobby_player = None
        self.player = None
        self.cocos_scene = None
        self.battle = None
        self.battle_idx = 0
        self.player_sd = None
        self.ctrl_target_id = 0
        self.mecha = None
        self.uid_prefix = 0
        self.abtest_group = False
        self.war_lrobots = {}
        self.war_puppets = {}
        self.war_noteam_puppets = {}
        self.war_mechas = {}
        self.war_noteam_mechas = {}
        self.war_non_explosion_dis_objs = {}
        self.war_mecha_aim_objs = {}
        self.war_ignored_shoot_col = set()
        self.battle_ready_box_col_ids = set()
        self.in_game_setting = {}
        self.replacable = False
        self.keys = {}
        self.init_internal_flag()
        self.debug_vehicle = False
        self.v = False
        self.show_sideways_check_line = False
        self.is_allow_sideways = False
        self.climb_err_code = 1
        self.is_debug_check_off_pos = False
        self._last_report_send_timestamp = 0
        if hasattr(world, 'get_2d_sfx_window_size'):
            self.really_sfx_window_size = tuple([ int(x) for x in world.get_2d_sfx_window_size() ]) + game3d.get_window_size()[2:]
        else:
            self.really_sfx_window_size = game3d.get_window_size()
        from logic.gutils.screen_effect_utils import refresh_screen_effect_scale_value
        refresh_screen_effect_scale_value(self.really_sfx_window_size)
        self.really_window_size = game3d.get_window_size()
        self.really_window_ratio = None
        from logic.vscene import scene_type
        self.scene_type = scene_type.SCENE_TYPE_LOGIN
        self.is_inner_server = 0
        self.last_bat_disconnect_time = None
        global_data.can_show_cockpit_decor = True
        self.enable_scn_detail = True
        self.enable_scn_lod_chunk = True
        self.enable_cache_animation = False
        self.enable_mecha_cache_animation = True
        self.show_trk_debug_info = False
        self.is_show_status_out_of_time = game3d.get_platform() == game3d.PLATFORM_WIN32
        self.cur_platform = game3d.get_platform()
        self.low_mem_mode_threshold = 1100
        self.low_mem_mode_threshold_pc = 1100
        self.med_mem_mode_threshold_ios = 2100
        self.low_mem_mode_threshold_ios = 1100
        self.low_mem_mode_threshold_android = 2100
        self.is_low_mem_mode = False
        self.is_med_mem_mode = False
        self.is_low_perf_mode = False
        self.cur_thermal_state = 0
        self.last_thermal_state = 0
        self.cur_thermal_state_debug = -1
        self.preload_dynamic_check_tick = 15
        self.preload_extend_dist = 19500.0
        self.preload_alway_y_min = 1300.0
        self.cur_preload_extend_dist = self.preload_extend_dist
        self.cur_preload_alway_y_min = self.preload_alway_y_min
        self.preload_extend_dist_high = 5200.0
        self.preload_alway_y_min_high = 1300.0
        self.preload_extend_dist_normal = 3900.0
        self.preload_alway_y_min_normal = 780.0
        self.preload_extend_dist_low = 1950.0
        self.preload_alway_y_min_low = 13000.0
        self.cur_preload_extend_dist = self.preload_extend_dist_normal
        self.cur_preload_alway_y_min = self.preload_alway_y_min_normal
        self.preload_extend_dist_for_new_lod = 2600.0
        self.preload_alway_y_min_for_new_lod = 13000000.0
        self.preload_dynamic_change_height = 900.0
        self.view_range_fix = 1.0
        self.near_view_range_fix = 1.0
        self.far_view_range_fix = 1.0
        self.pymod_inited = False
        self.is_enable_shader_warmup = False
        self.is_enable_shader_record = False
        self.enable_perform_sdk = False
        self.effect_cache_behavior = six.moves.builtins.__dict__.get('G_EFFECT_CACHE_BEHAVIOR', 0)
        self.block_render_info = not __debug__
        self.enable_scale_resolution = False
        self.enable_resolution_switch = False
        self.limit_resolution_height = (900, 1080)
        self.current_msaa_num = 0
        self.sound_mgr_optimization = True
        self.enable_other_model_shadowmap = False
        self.cam_world_transform = None
        self.enable_lobby_scene_only = True
        self.enable_naver_cafe = True
        self.enable_text_check = False
        self.is_renderer2 = hasattr(world, 'get_renderer_ver') and world.get_renderer_ver() == 2
        self._logfiles = {}
        self.is_32bit = False
        self.is_32bit_analog_64bit = False
        self.enable_high_fps = True
        self.enable_144 = True
        self.enable_res_ref_cache = False
        self.enable_ui_custom_cfg = False
        self.enable_assemble_model_style = False
        self.force_replace_lightmap = False
        self.force_replace_lightmap_path = 'textures/lightmap_8x8.png'
        self.enable_parachute_view_range_optimize = False
        self.enable_parachute_range_circle = False
        self.force_disable_model_cache = False
        self.force_disable_sfx_cache = False
        self.logic_real_dt = 0
        self.post_logic_real_dt = 0
        self.enable_ui_add_image_async = False
        self.enable_ccuiimageview = True
        self.enable_pop_lru_conf = False
        self.enable_light_effect = True
        self.server_enable_low_fps = True
        self.low_fps_switch_on = False
        self.enable_model_vertex_half = False
        if game3d.get_render_device() == game3d.DEVICE_METAL and not game3d.support_vertex_format_half():
            self.model_vertex_half_mode = 0
        else:
            self.model_vertex_half_mode = 2
        self.enable_landscape_patch_vertex_half = False
        self.enable_landscape_detail_vertex_half = False
        self.enable_sfx_lod = False
        self.enable_fx_target = False
        self.enable_soft_particle = True
        self.enable_fast_material = True
        self.min_adaptive_near = 2.0
        self.enable_pc_eye_adapt = False
        self.enable_animator_reg_event = True
        self.enable_index_buffer_sub_visible = False
        self.enable_shader_complexity_view = False
        self.is_mumu = False
        self.is_google_pc = False
        self.is_android_pc = False
        self.is_in_mumu = False
        is_pc_mode_by_magic = six.moves.builtins.__dict__.get('pc_mode_by_magic', None)
        import social
        if social.get_channel():
            app_name = social.get_channel().distribution_channel
        else:
            app_name = ''
        if hasattr(game3d, 'is_google_play_pc') and game3d.get_platform() == game3d.PLATFORM_ANDROID:
            self.is_google_pc = game3d.is_google_play_pc()
        print('MJY magic:', is_pc_mode_by_magic)
        self.is_mumu = app_name == 'netease.wyzymnqsd_cps_dev'
        if game3d.get_platform() == game3d.PLATFORM_WIN32 or self.is_mumu or self.is_google_pc:
            if is_pc_mode_by_magic is not None:
                self.is_pc_mode = is_pc_mode_by_magic
            elif C_file.find_res_file('no_pc_mode_config', '') > 0:
                from logic.client.const import pc_const
                if pc_const.PC_NO_CONFIG_MODE_CONTENT_TEXT == six.ensure_str(C_file.get_res_file('no_pc_mode_config', '')):
                    self.is_pc_mode = False
                else:
                    self.is_pc_mode = True
            else:
                self.is_pc_mode = True
        else:
            self.is_pc_mode = False
        if C_file.find_res_file('pc_editor_package_flag.flag', ''):
            self.is_pc_mode = False
        if self.is_mumu or self.is_google_pc:
            self.is_android_pc = True
        if hasattr(game3d, 'get_musdk_value') and hasattr(game3d, 'mumu_keymousemod') and game3d.get_platform() == game3d.PLATFORM_ANDROID:
            is_in_mumu = game3d.get_musdk_value(844) == 36662
            self.is_mumu_pc_control = is_in_mumu and game3d.mumu_keymousemod()
            self.is_in_mumu = is_in_mumu
            if self.is_mumu_pc_control:
                self.is_pc_mode = True
        self.is_share_show = not self.is_google_pc
        if is_pc_mode_by_magic is not None:
            del six.moves.builtins.__dict__['pc_mode_by_magic']
        self.enable_debug_key_in_inner_server = __debug__
        self.enable_debug_key_in_inner_server_filepath = os.path.join(game3d.get_doc_dir(), 'enable_debug_key_in_inner_server')
        if os.path.isfile(self.enable_debug_key_in_inner_server_filepath):
            self.enable_debug_key_in_inner_server = True
        self.is_key_mocking_ui_event = False
        self.reshow_settings_after_reload = False
        self.debug_perf_switch_global = False
        self.debug_perf_switch_group = {'enable_landscape_render': None,
           'enable_post_process': None,
           'texture_skip_level_scene': None,
           'texture_skip_level_player': None,
           'enable_ui_render': None,
           'enable_vertex_half': None,
           'sfx_render_level': None,
           'shader_lod_cfg': None,
           'enable_all_sfx': None,
           'resolution_width': None,
           'resolution_height': None,
           'enable_avatar_model': None
           }
        self.enable_save_energy_mode = True
        self.in_save_energy_mode = False
        self.save_energy_duration = 120
        self.enable_csm_range_center = False
        self.shadowmap_range_pc_scalar = 4.0
        self.game_time = 0
        self.game_time_server = 0
        self.game_time_battle = 0
        self.game_time_wrapped = 0
        self.tpa_launch_data = {}
        self.stale_tpa_launch_data = set()
        self.last_scene_is_lottery = False
        self.enable_split_script = False
        self.custon_battle_scene = None
        self.is_ue_model = True
        self.is_multi_pass_support = not self.is_ue_model or game3d.get_platform() != game3d.PLATFORM_IOS or game3d.get_render_device() == game3d.DEVICE_METAL
        self.on_post_logic = False
        self.enable_island_chushengtai = True
        self.enable_island_chushengtai_ui_refresh = True
        self.use_scan_pay = True
        self.use_artist_test_scne = False
        self.enable_meadow = True
        self.game_server_svr_type = ''
        self.rank_web_dict = {}
        self.micro_service_url = ''
        self.disable_low_model = True
        self.enable_battle_ui_cache = True
        self.enable_camera_state_cache = True
        self.had_enter_lobby = False
        self.test_hair_animator_blend = False
        self.is_neox_editor = False
        self.debug_draw_model_value = 0.0
        self.is_show_battery_current = False
        self.debug_replace_res_dict = {}
        self.enable_cocos_csb = True
        self.enable_check_lottery = False
        self.use_occlusion = False
        self.enable_45fps = False
        self.server_enable_vlm = True
        self.enable_collect_ui = False
        self.enable_clan_quit_advise = True
        self.enable_skate_cross_window = True
        self.enable_check_pos = True
        self.enable_ignore_effect_behind_camera = True
        self.use_soc = False
        self.is_editor_mode = False
        self.is_local_editor_mode = False
        self.artcheck_scene = False
        self.artcheck_human_display_editor = None
        self.force_mecha_shiny_weapon_rarity = -1
        self.use_sunshine = False
        self.enable_pve = False
        self.enable_pve_lobby = True
        self.is_pve_lobby = False
        self.enable_ragdoll_explosion = True
        self.refresh_pve_settle_tag = False
        self.rematch_pve_tag = 0
        self.has_show_rematch_dialog = False
        self.enter_pve_with_archive = False
        self.enable_pve_test_mecha = False
        self.enable_ray_test_eye_adapt = __debug__
        self.enable_mecha_lightmap = True
        return

    def get_debug_perf_val(self, key, old_val):
        if not self.debug_perf_switch_global:
            return old_val
        else:
            new_val = self.debug_perf_switch_group.get(key, None)
            if new_val is None:
                return old_val
            return new_val

    def apply_debug_perf_switch(self, enable):
        self.debug_perf_switch_global = enable
        if not enable:
            return
        else:
            enable_ui_render = self.get_debug_perf_val('enable_ui_render', None)
            if enable_ui_render is not None:
                import cocosui
                cocosui.enable_render(enable_ui_render)
            enable_vertex_half = self.get_debug_perf_val('enable_vertex_half', None)
            if enable_vertex_half is not None:
                import world
                import game3d
                if hasattr(world, 'use_vertex_half') and game3d.get_platform() != game3d.PLATFORM_WIN32:
                    world.use_vertex_half(enable_vertex_half)
            enable_all_sfx = self.get_debug_perf_val('enable_all_sfx', None)
            if enable_all_sfx is not None:
                import world
                if hasattr(world, 'enable_all_sfx'):
                    world.enable_all_sfx(enable_all_sfx)
            return

    def set_interal_flag(self, attr_name):
        flag = C_file.find_res_file('%s.flag' % attr_name, '') > 0
        setattr(self, attr_name, flag)

    def init_internal_flag(self):
        self.set_interal_flag('is_debug_mode')
        self.set_interal_flag('is_animator_debug')
        self.set_interal_flag('is_skip_patch')
        self.set_interal_flag('is_internal')
        self.set_interal_flag('is_artist_animation_test')

    def __getattr__(self, key, default=None):
        val = self.alias_map.get(key, default)
        if val:
            setattr(self, key, val)
        return val

    def __getitem__(self, key, default=None):
        return self.alias_map.get(key, default)

    def clear(self):
        self.finalize_all_singleton()
        self.remove_all_global_data()

    def finalize_all_singleton(self):
        smap = self.singleton_map
        singleton_list_keys = six_ex.keys(smap)
        singleton_list_keys.reverse()
        for skey in singleton_list_keys:
            sobj = smap.get(skey, None)
            if sobj is None:
                continue
            if hasattr(sobj, '_KEEP_ALIVE_WHEN_RELOAD'):
                print('not finalize obj for _KEEP_ALIVE_WHEN_RELOAD')
                print(sobj)
                continue
            if hasattr(sobj, 'destroy'):
                sobj.destroy()
            else:
                sobj.finalize()

        self.singleton_map.clear()
        return

    def set_global_data(self, name, data, force_replace=False):
        if name in __builtins__:
            if not self.replacable and not force_replace:
                raise Exception('[set_global_data]duplicate global data==>%s' % name)
            else:
                self.del_global_data(name)
        __builtins__[name] = data
        self._global_data_keys.append(name)

    def get_global_data_byname(self, name):
        if name in self._global_data_keys:
            return __builtins__[name]
        else:
            return None

    def del_global_data(self, name):
        if not name.startswith('global_') and not name.startswith('log_'):
            raise Exception('[del_global_data]global name[%s] must startswith "global_"' % name)
        if name in __builtins__:
            del __builtins__[name]
            self._global_data_keys.remove(name)

    def remove_all_global_data(self):
        keys = self._global_data_keys[:]
        for key in keys:
            self.del_global_data(key)

        keys = None
        return

    def is_key_down(self, keycode):
        if keycode in self.keys:
            return self.keys[keycode]
        return False

    def log(self, filename, content):
        fp = self._logfiles.get(filename)
        if fp is None:
            import game3d
            import os.path
            fp = open(os.path.join(game3d.get_doc_dir(), filename + '.txt'), 'w')
            self._logfiles[filename] = fp
        fp.write(content + '\n')
        return

    def save_all_log(self):
        for fp in six.itervalues(self._logfiles):
            fp.close()

    def is_32bit_system(self):
        import sys
        return sys.maxsize <= 4294967296L

    def run_client_cmd(self, cmd, args):

        def show_test_ui():
            global_data.ui_mgr.show_ui('BattleSettingUI', 'logic.comsys.setting_ui')
            a = global_data.ui_mgr.get_ui('MobileInfoUI')
            if a:
                a.panel.btn_test.setVisible(True)

        def apply_dof(enable, nearPlane, farPlane, focusDist, focusRange):
            import render
            global_data.display_agent.set_post_effect_active('dof_mobile', enable)
            if enable:
                dof_mat = global_data.display_agent.get_post_effect_pass_mtl('dof_mobile', 1)
                dof_mat.set_var('farPlane', farPlane)
                dof_mat.set_var('nearPlane', nearPlane)
                dof_mat.set_var('focusDist', focusDist)
                dof_mat.set_var('focusRange', focusRange)

        def apply_distortion(enable):
            import render
            global_data.display_agent.set_post_effect_active('distortion', enable)

        CLIENT_CMD_DICT = {'show_test_ui': lambda : show_test_ui(),
           'apply_dof': lambda enable, nearPlane, farPlane, focusDist, focusRange: apply_dof(enable, nearPlane, farPlane, focusDist, focusRange),
           'apply_distortion': lambda enable: apply_distortion(enable)
           }
        if cmd in CLIENT_CMD_DICT:
            cmd_func = CLIENT_CMD_DICT.get(cmd)
            if callable(cmd_func):
                cmd_func(*args)