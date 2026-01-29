# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/feature_mgr.py
from __future__ import absolute_import
import game3d
import render
import version
from common.framework import Singleton

class FeatureMgr(Singleton):
    ALIAS_NAME = 'feature_mgr'

    def init(self):
        self._use_engine_feature_mgr = hasattr(game3d, 'is_feature_ready')
        self._feature_cache = {}

    def _convert_verion_into_number(self, ver_str):
        num0, num1, num2 = ver_str.split('.')
        const_factor = 100000
        return int(num0) * const_factor * const_factor + int(num1) * const_factor + int(num2)

    def _is_engine_version_ge_to(self, cmp_ver):
        cmp_ver_num = self._convert_verion_into_number(cmp_ver)
        eng_ver = version.get_engine_version()
        eng_ver_num = self._convert_verion_into_number(eng_ver)
        return eng_ver_num >= cmp_ver_num

    def _is_engine_version_eq_to(self, cmp_ver):
        cmp_ver_num = self._convert_verion_into_number(cmp_ver)
        eng_ver = version.get_engine_version()
        eng_ver_num = self._convert_verion_into_number(eng_ver)
        return eng_ver_num == cmp_ver_num

    def _is_feature_ready(self, feature, version=None):
        if feature in self._feature_cache:
            return self._feature_cache[feature]
        else:
            if self._use_engine_feature_mgr:
                is_ready = game3d.is_feature_ready(feature)
            elif version is not None:
                is_ready = self._is_engine_version_ge_to(version)
            else:
                is_ready = False
            self._feature_cache[feature] = is_ready
            return is_ready

    def is_richtext_for_Japanese_fixed(self):
        feature = 'FixRichTextForJapanese_1_0'
        version = '1.0.5219'
        return self._is_feature_ready(feature, version)

    def is_new_landscape_detail_ready(self):
        feature = 'NewLandscapeDetail_1_0'
        version = '1.0.5280'
        return self._is_feature_ready(feature, version)

    def is_async_loader_g93_mode_ready(self):
        feature = 'AsyncLoaderG93Mode_1_0'
        return self._is_feature_ready(feature)

    def is_road_async_batching_ready(self):
        feature = 'RoadAsyncBatching_3_0'
        return self._is_feature_ready(feature)

    def is_share_line_simple_ready(self):
        feature = 'ShareLineSimple_1_0'
        version = '1.0.5442'
        return self._is_feature_ready(feature, version)

    def is_linegame_ready(self):
        from common.platform.dctool import interface
        feature = 'LineGame_1_0'
        if 'GLOBAL' != interface.get_package_type():
            return False
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            version = '1.0.7548'
            return self._is_feature_ready(feature, version)
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            version = '1.0.7630'
            return self._is_feature_ready(feature, version)
        return False

    def is_model_lod_offset_ready(self):
        feature = 'ModelOffsetEable_1_0'
        return self._is_feature_ready(feature)

    def is_postprocess_residual_in_partical_fixed(self):
        feature = 'FixPostprocessFxInEmitterBug_1_0'
        return self._is_feature_ready(feature)

    def is_g93natw_new_mobileprovision(self):
        feature = 'g93natw_new_mobileprovision'
        return self._is_feature_ready(feature)

    def is_range_check_func_ready(self):
        feature = 'RangeCheckReady_1_0'
        return self._is_feature_ready(feature)

    def is_support_naver_cafe(self):
        feature = 'NaverCafe_1_0'
        return self._is_feature_ready(feature)

    def is_support_on_real_resolution_changed(self):
        feature = 'OnRealResolutionChanged_1_0'
        return self._is_feature_ready(feature)

    def is_emitter_show_nothing_fixed(self):
        feature = 'FixEmitterShowNothingBug_1_0'
        return self._is_feature_ready(feature)

    def is_support_boundary_word(self):
        feature = 'BoundaryWordSupport_1_0'
        return self._is_feature_ready(feature)

    def is_support_insert_file_cache(self):
        feature = 'InsertFileCache_1_0'
        return self._is_feature_ready(feature)

    def is_support_dynamic_texture_map(self):
        feature = 'DynamicTextureMap_1_0'
        return self._is_feature_ready(feature)

    def is_support_android_high_fps(self):
        feature = 'AndroidHighRate'
        return self._is_feature_ready(feature)

    def is_support_pc_eye_adapt(self):
        feature = 'pc_eye_adapt_1_0'
        return self._is_feature_ready(feature)

    def is_support_dynamic_res_map(self):
        feature = 'DynamicResMap_1_0'
        return self._is_feature_ready(feature)

    def is_support_fallback_font_list(self):
        feature = 'SupportFallbackFontList_1_0'
        version = '1.0.5765'
        is_ready = self._is_engine_version_ge_to(version)
        return is_ready

    def is_support_scene_ignore_group_names(self):
        feature = 'SceneIgnoreGroupNames'
        return self._is_feature_ready(feature)

    def is_support_share_culling(self):
        feature = 'share_culling_1_0'
        version = '1.0.5783'
        is_ready = self._is_engine_version_ge_to(version)
        return is_ready

    def is_support_precise_spring_anim_col(self):
        feature = 'PreciseSpringAnimCol_1_0'
        return self._is_feature_ready(feature)

    def is_support_impostor(self):
        feature = 'ImpostorLOD_1_0'
        return self._is_feature_ready(feature)

    def is_support_yidun_simulator_detect(self):
        feature = 'YiDunSimulatorDetect'
        return self._is_feature_ready(feature)

    def is_support_sfx_lod(self):
        feature = 'Sfx_Lod_1_0'
        return self._is_feature_ready(feature)

    def is_support_dx11(self):
        feature = 'DirectX11_1_0'
        return self._is_feature_ready(feature)

    def is_support_async_load_prior(self):
        feature = 'AsyncLoadPriorityByDist_1_0'
        return self._is_feature_ready(feature)

    def is_support_scene_pick_bounding_box_offset(self):
        feature = 'ScenePickBoundingBoxOffSet'
        return self._is_feature_ready(feature)

    def is_particlepolytube_node_count_fixed(self):
        feature = 'ParticlepolytubeNodeCountFix_1_0'
        return self._is_feature_ready(feature)

    def is_scale9sprite_scripting_blendable(self):
        feature = 'Scale9SpriteScriptingBlendable'
        return self._is_feature_ready(feature)

    def is_neox_trans_cocos_rendertexture_fixed(self):
        feature = 'NeoxTransCocosRenderTextureFix_1_0'
        return self._is_feature_ready(feature)

    def is_support_fx_offscreen(self):
        render_flag = True
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            render_flag = False
        render_system_name = render.get_render_system_name()
        if render_system_name in ('DirectX 9', 'DirectX 11'):
            render_flag = False
        feature = 'Fx_Offscreen_1_4'
        return self._is_feature_ready(feature) and render_flag and version.get_tag() in ('trunk',
                                                                                         'effect_optimize')

    def is_support_soft_particle(self):
        if game3d.get_platform() != game3d.PLATFORM_WIN32 and not global_data.is_android_pc:
            return False
        feature = 'Fx_Offscreen_1_5'
        return self._is_feature_ready(feature) and global_data.enable_soft_particle

    def is_support_animation_thread(self):
        feature = 'Animation_Thread_1_0'
        return self._is_feature_ready(feature)

    def is_support_model_decal(self):
        if global_data.is_32bit:
            return False
        feature = 'ModelDecal_1_0'
        return self._is_feature_ready(feature)

    def is_support_render_texture_blend_state_1_0(self):
        feature = 'RenderTextureSetBlendState_1_0'
        return self._is_feature_ready(feature)

    def is_support_new_foot_ik(self):
        feature = 'SupportNewFootIK'
        return self._is_feature_ready(feature)

    def is_support_debug_multi_thread_anim(self):
        feature = 'SupportDebugMultiThreadAnim'
        return self._is_feature_ready(feature)

    def is_support_pc_mouse_hover(self):
        feature = 'CocosUI_MouseHover_Event_1_0'
        return self._is_feature_ready(feature)

    def is_support_neox_renderer1(self):
        feature = 'Renderer_1_0'
        return self._is_feature_ready(feature)

    def is_support_neox_renderer2(self):
        feature = 'Renderer_2_0'
        return self._is_feature_ready(feature)

    def is_support_preload_lod(self):
        feature = 'Preload_Lod_1_0'
        return self._is_feature_ready(feature) and global_data.is_ue_model

    def is_support_ntd(self):
        feature = 'SupportDisplayThread'
        return self._is_feature_ready(feature)

    def is_dynamic_ue_env_config(self):
        feature = 'Dynamic_UE_Env_1_0'
        return self._is_feature_ready(feature)

    def is_support_collision_bind_model(self):
        return False

    def is_support_push_channel_2(self):
        feature = 'push_channel_2_0'
        return self._is_feature_ready(feature)

    def is_support_video_share(self):
        feature = 'SupportVideoShare'
        return self._is_feature_ready(feature)

    def is_support_spine_3_8(self):
        feature = 'spine_3_8'
        return self._is_feature_ready(feature)

    def is_support_scene_mirror_enable(self):
        feature = 'SceneMirrorEnable'
        return self._is_feature_ready(feature)

    def is_fix_cocos_clip(self):
        version = '1.0.8779'
        is_ready = self._is_engine_version_ge_to(version)
        return is_ready

    def is_support_sfx_set_var_float(self):
        feature = 'SfxSetVarFloat_0_1'
        return self._is_feature_ready(feature)

    def is_support_mini_program_share(self):
        feature = 'SupportMiniProgramShare'
        return self._is_feature_ready(feature)

    def is_support_sfx_set_tex(self):
        if global_data.is_inner_server:
            if global_data.no_support_sfx_set_tex:
                return False
        feature = 'SfxSetTex_0_1'
        return self._is_feature_ready(feature)

    def is_support_meadow(self):
        feature = 'Meadow_1_0'
        return self._is_feature_ready(feature) and game3d.get_render_device() != game3d.DEVICE_D3D9

    def is_support_ext_tech_fix(self):
        feature = 'EXT_TECH_FIX'
        return self._is_feature_ready(feature)

    def is_support_huya_ios_live(self):
        feature = 'SupportHuyaBroadcast'
        return self._is_feature_ready(feature)

    def is_support_rt_skip_boundingbox_check(self):
        feature = 'RTSkipBoundingChecking'
        return self._is_feature_ready(feature)

    def is_vivo_inputview_wrong_position_fixed(self):
        return False

    def is_support_TextWithCarriageReturn_Shrink(self):
        feature = 'TextWithCarriageReturn_Shrink'
        return self._is_feature_ready(feature)

    def is_support_qq_mini_program(self):
        feature = 'SupportQQMiniProgramShare'
        return self._is_feature_ready(feature)

    def is_support_open_aim_in_house(self):
        feature = 'SupportOpenAimInHouse'
        return self._is_feature_ready(feature)

    def is_support_share_tag(self):
        feature = 'SupportShareTag'
        return self._is_feature_ready(feature)

    def is_support_anim_thread_for_ik(self):
        feature = 'Fix_IK_In_HFPS_2.0'
        return self._is_feature_ready(feature)

    def is_support_grid_map_to_auto_obj(self):
        feature = 'GridMapToAutoObj'
        return self._is_feature_ready(feature)

    def is_support_face_recognition(self):
        feature = 'FaceRecognition'
        return self._is_feature_ready(feature)

    def is_support_cocos_tex_async_load(self):
        feature = 'CocosUI_Tex_Async_Load_3_0'
        return self._is_feature_ready(feature)

    def is_support_debug_view_shader_complexity(self):
        feature = 'DebugViewShaderComplexity_1_0'
        return self._is_feature_ready(feature)

    def is_need_force_up_package(self, channel_name):
        if channel_name == 'fanyou' and not self.is_support_myapp_11():
            return True
        else:
            channel_up_info = {'bilibili_sdk': '1.0.11226'
               }
            if channel_name not in channel_up_info:
                return False
            check_version = channel_up_info[channel_name]
            return not self._is_engine_version_ge_to(check_version)

    def is_bilibili_sdk_specific_version(self, channel_name):
        channel_up_info = {'bilibili_sdk': '1.0.13076'
           }
        if channel_name not in channel_up_info:
            return False
        check_version = channel_up_info[channel_name]
        return self._is_engine_version_eq_to(check_version)

    def is_support_cocos_csb(self):
        return False
        feature = 'Support_Cocos_CSB_3_0'
        return self._is_feature_ready(feature) and global_data.enable_cocos_csb

    def is_support_dyculling(self):
        feature = 'DyOccFix_1_0'
        return self._is_feature_ready(feature)

    def is_support_channel_login_time_ctrl(self):
        feature = 'ChannelLoginTimeCtrl'
        return self._is_feature_ready(feature)

    def is_support_prefect_mirror(self):
        feature = 'PrefectMirror'
        return self._is_feature_ready(feature)

    def is_support_shader_compile_async(self):
        feature = 'CompileShaderAsync_2_0'
        return self._is_feature_ready(feature)

    def landscapel3enable(self):
        feature = 'landscapel3enable'
        return self._is_feature_ready(feature)

    def is_fix_impostor_bug(self):
        feature = 'FixImpostorBug'
        return self._is_feature_ready(feature)

    def is_fix_rt_savefile_png_alpha(self):
        feature = 'FixRtSaveFilePngAlpha'
        return self._is_feature_ready(feature)

    def is_support_set_dynamic_static_triggers_1_0(self):
        feature = 'SupportSetDynamicStaticTriggers_1_0'
        return self._is_feature_ready(feature)

    def is_support_metal_and_ubo(self):
        feature = 'MetalAndUBOEnable'
        return self._is_feature_ready(feature)

    def is_support_qsec_new_emulator_detect(self):
        feature = 'QsecEmulatorDetect'
        return self._is_feature_ready(feature)

    def is_fix_ios_framerate(self):
        feature = 'iOSFrameRateFix'
        return self._is_feature_ready(feature)

    def is_use_depth_fetch(self):
        feature = 'usedepthfetch'
        return self._is_feature_ready(feature)

    def is_use_metal_framebuffer_fetch(self):
        feature = 'useMetalFramebufferFetch'
        return self._is_feature_ready(feature)

    def is_support_soc(self):
        feature = 'soc_2_2'
        ver = '1.0.15701'
        forbid_ver = '1.0.15979'
        return self._is_feature_ready(feature) and self._is_engine_version_ge_to(ver) and not self._is_engine_version_eq_to(forbid_ver)

    def is_support_set_frametime(self):
        feature = 'SetFrameTime'
        return self._is_feature_ready(feature)

    def is_support_oodle(self):
        feature = 'oodlenetwork'
        return self._is_feature_ready(feature)

    def is_support_oodle_v2(self):
        if global_data.is_32bit:
            return False
        else:
            feature = 'oodlenetworkv2'
            import asiocore
            if self._is_feature_ready(feature):
                if not hasattr(asiocore, 'is_enable_oodle'):
                    return False
                return asiocore.is_enable_oodle()
            return False

    def is_support_cs(self):
        feature = 'support_cs'
        return self._is_feature_ready(feature)

    def is_wwise_big_default_pools(self):
        feature = 'wwiseBigDefaultPools'
        return self._is_feature_ready(feature)

    def is_support_set_animator_blend_node_children_parameter_position(self):
        feature = 'SupportSetAnimatorBlendNodeChildrenParameterPositions'
        return self._is_feature_ready(feature)

    def is_support_mecha_foot_ik(self):
        feature = 'SupportMechaFootIK_1_1'
        return self._is_feature_ready(feature)

    def is_support_anim_assemble(self):
        feature = 'AnimAssemble_1_0'
        return self._is_feature_ready(feature)

    def is_supoort_ragdoll_normal_scale(self):
        feature = 'RagdollNormalScale'
        return self._is_feature_ready(feature)

    def is_support_crash_hunter_thread(self):
        feature = 'CrashHunterThread'
        return self._is_feature_ready(feature)

    def is_support_sfx_data_and_mesh_vertex_data_lru_cache(self):
        feature = 'SfxDataAndMeshVertexDataLRUCache'
        return self._is_feature_ready(feature)

    def is_support_spine_unleak(self):
        version = '1.0.17030'
        is_ready = self._is_engine_version_ge_to(version)
        return is_ready

    def is_support_myapp_11(self):
        feature = 'support_myapp_11'
        return self._is_feature_ready(feature)