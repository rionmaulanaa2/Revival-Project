# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/DisplayAgent.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.framework import SingletonBase
import render
import world
import game3d
from common.platform import is_win32, is_android, is_ios
import version
from logic.vscene.global_display_setting import GlobalDisplaySeting
from logic.manager_agents.manager_decorators import sync_exec
from common.utils import pc_platform_utils
INITED_PIPELINE = {}
_ENABLE_FX_TARGET = game3d.calc_string_hash('enable_fx_target')
_HASH_ENABLE = game3d.calc_string_hash('Enable')

class PostProcessItem(object):

    def __init__(self, name):
        super(PostProcessItem, self).__init__()
        self.dirty = False
        self.name = name
        self.params = {}
        self.active = False


class DisplayAgent(SingletonBase):
    ALIAS_NAME = 'display_agent'

    def init(self):
        super(DisplayAgent, self).init()
        self._msaa_old = 1
        self._msaa_new = self._msaa_old
        self._redirect_scale_old = 1.0
        self._redirect_scale_new = self._redirect_scale_old
        self._pipeline_old = 'common/pipeline/pipeline.xml'
        self._pipeline_new = self._pipeline_old
        if global_data.is_ue_model:
            if pc_platform_utils.is_pc_hight_quality():
                self._pipeline_ingame_path = 'common/pipeline/pipeline_ingame_xc_taa.xml'
            else:
                self._pipeline_ingame_path = 'common/pipeline/pipeline_ingame_xc.xml'
        self._pipeline_ingame_finished = False
        self._postprocesslist = {}
        self._pp_dirty = False
        self.reset_enable_fx_target(global_data.enable_fx_target)

    def on_resume(self):
        self._pipeline_old = 'common/pipeline/pipeline.xml'
        if global_data.enable_resolution_switch and global_data.game_mgr.is_ingame_scene():
            self.do_check_reset_resolution(True)

    def do_check_reset_resolution(self, force_set=False):
        if global_data.enable_resolution_switch:
            check_reset_resolution_ex(force_set)
        else:
            check_reset_resolution()

    def refresh_hdr(self):
        gds = GlobalDisplaySeting()
        gds.refresh_hdr()

    def set_msaa(self, num):
        self._msaa_new = num

    def set_redirect_scale(self, factor):
        from logic.gcommon.common_const import ui_operation_const as uoc
        if pc_platform_utils.is_pc_hight_quality() and global_data.is_ue_model:
            if not pc_platform_utils.is_redirect_scale_enable() and factor > 1.0:
                factor = 1.0
            self._redirect_scale_new = factor
            aa_level = global_data.gsetting.get_aa_level()
            downsample_enable = True if aa_level == 0 else False
            self.set_longtime_post_process_active('downsample_to_backbuff', downsample_enable)

    def set_aa_level(self, level):
        if pc_platform_utils.is_pc_hight_quality() and global_data.is_ue_model:
            flag = False if level == 0 else True
            if global_data.enable_shader_complexity_view:
                flag = False
            self.enable_taa(flag)

    def enable_taa(self, enable):
        if global_data.game_mgr:
            active_camera = global_data.game_mgr.scene.active_camera
            if enable:
                samplesx = ()
                samplesy = ()
                active_camera.set_taa_jitter(8, samplesx, samplesy)
                flag = True
            else:
                active_camera.set_taa_jitter(0, (), ())
                flag = False
            self.set_longtime_post_process_active('taa', flag)
            self.set_longtime_post_process_active('downsample_to_backbuff', not flag)

    def set_longtime_post_process_active(self, key, enable, params=None):
        self.update_longtime_post_process_params(key, params)
        item = self._postprocesslist.get(key, PostProcessItem(key))
        item.active = enable

    def update_longtime_post_process_params(self, key, params=None):
        item = self._postprocesslist.get(key, PostProcessItem(key))
        self._postprocesslist[key] = item
        item.dirty = True
        if params:
            item_params = item.params
            for k, values in six.iteritems(params):
                old_values = item_params.get(k, {})
                old_values.update(values)
                item_params[k] = old_values

        self._pp_dirty = True

    def set_pipeline(self, pipeline):
        if self._pipeline_new != pipeline:
            self._postprocesslist = {}
        self._pipeline_new = pipeline

    @sync_exec
    def set_post_effect_active(self, effect_name, enable):
        if global_data.debug_perf_switch_global:
            switch = global_data.get_debug_perf_val('enable_post_process', True)
            if not switch:
                enable = False
        if global_data.is_renderer2:
            world.set_post_effect_active(effect_name, enable)
        else:
            render.set_post_process_active(effect_name, enable)

    def get_post_effect_pass_mtl(self, effect_name, pass_idx):
        if global_data.is_renderer2:
            try:
                return world.get_post_effect_pass_mtl(effect_name, pass_idx)
            except TypeError:
                print('get post effect pass failed', effect_name, pass_idx)
                return None

        else:
            return render.get_post_process_material(effect_name, pass_idx)
        return None

    def reload_post_process(self):
        if hasattr(render, 'reload_post_process'):
            render.reload_post_process()

    def reload_post_process_with_path(self, path):
        if hasattr(render, 'reload_post_process_with_path'):
            render.reload_post_process_with_path(path)
        elif hasattr(world, 'reset_post_process_config'):
            path = path.replace('.xml', '_render2.xml')
            world.reset_post_process_config(path)

    def flush_setting(self):
        need_reload_pipeline = False
        need_rescale = False
        if self._msaa_old != self._msaa_new:
            self._msaa_old = self._msaa_new
            if global_data.is_ue_model:
                self.set_smaa_active(self._msaa_new)
            elif self._msaa_new > 1:
                self.set_longtime_post_process_active('fxaa', True)
                log_error_fmt('[IMPORTANT] DO SET FXAA ENABLE TO {}', self._msaa_new)
            else:
                self.set_longtime_post_process_active('fxaa', False)
                log_error_fmt('[IMPORTANT] DO SET FXAA DISABLE TO {}', self._msaa_new)
            need_reload_pipeline = True
        if self._pipeline_old != self._pipeline_new:
            self._pipeline_old = self._pipeline_new
            need_reload_pipeline = True
        if self._redirect_scale_old != self._redirect_scale_new:
            self._redirect_scale_old = self._redirect_scale_new
            need_rescale = True
            need_reload_pipeline = True
        if need_reload_pipeline:
            self._do_reload_pipeline(need_rescale)
            self._pp_dirty = True
            for item in six.itervalues(self._postprocesslist):
                item.dirty = True

        if self._pp_dirty:
            self._check_apply_pp()

    def set_smaa_active(self, factor):
        if factor == 1:
            log_error_fmt('[IMPORTANT] CLOSE SMAA {}', factor)
            self.set_longtime_post_process_active('smaa', False)
        elif factor == 2 or factor == 4:
            self.set_longtime_post_process_active('smaa', True)
            mat0 = global_data.display_agent.get_post_effect_pass_mtl('smaa', 0)
            mat1 = global_data.display_agent.get_post_effect_pass_mtl('smaa', 1)
            mat2 = global_data.display_agent.get_post_effect_pass_mtl('smaa', 2)
            if factor == 2:
                log_error_fmt('[IMPORTANT] DO SET SMAA LOW QUALITY ENABLE {}', factor)
                for mat in (mat0, mat1, mat2):
                    if mat:
                        mat.set_macro('SMAA_PRESET_LOW', '1')
                        mat.rebuild_tech()

            else:
                log_error_fmt('[IMPORTANT] DO SET SMAA HIGH QUALITY ENABLE {}', factor)
                for mat in (mat0, mat1, mat2):
                    if mat:
                        mat.set_macro('SMAA_PRESET_LOW', '0')
                        mat.rebuild_tech()

    def set_radial_blur_active(self, flag):
        self.update_longtime_post_process_params('radial_blur', {0: {_HASH_ENABLE: ('var', 'Enable', 1.0 if flag else 0.0)}})

    @sync_exec
    def _do_reload_pipeline(self, need_rescale):
        global INITED_PIPELINE
        if not INITED_PIPELINE.get(self._pipeline_new, False):
            old_scale = render.get_redirect_scale()
            if old_scale != 1.0:
                render.set_redirect_scale(1.0)
                need_rescale = True
            global_data.display_agent.reload_post_process_with_path(self._pipeline_new)
            INITED_PIPELINE[self._pipeline_new] = True
        if need_rescale:
            render.set_redirect_scale(self._redirect_scale_new)
        global_data.display_agent.reload_post_process_with_path(self._pipeline_new)
        if self._pipeline_new == self._pipeline_ingame_path:
            self._pipeline_ingame_finished = True

    def _flush_pp(self, pp_item):
        pp_item.dirty = False
        key = pp_item.name
        global_data.display_agent.set_post_effect_active(key, pp_item.active)
        if (pp_item.active or key == 'radial_blur') and pp_item.params:
            for mtl_id, paramdict in six.iteritems(pp_item.params):
                mtl = global_data.display_agent.get_post_effect_pass_mtl(key, mtl_id)
                if mtl is None:
                    continue
                funs = {'var': mtl.set_var,
                   'texture': mtl.set_texture
                   }
                for hash_name, args in six.iteritems(paramdict):
                    arg_type, name, val = args
                    funs[arg_type](hash_name, name, val)

        return

    def reset_enable_fx_target(self, enable):
        if not global_data.feature_mgr.is_support_fx_offscreen():
            print('Not support fx_offscreen!')
            return
        if not self._pipeline_ingame_finished:
            print('reset_enable_fx_target failed for pipeline_ingame is not finished yet.')
            return
        if hasattr(render, 'enable_fx_target'):
            print('render.enable_fx_target:%s...' % enable)
            render.enable_fx_target(enable)
            if enable:
                factor = 1.0 if 1 else 0.0
                global_data.is_ue_model or global_data.display_agent.update_longtime_post_process_params('hdr_tonemap', {0: {_ENABLE_FX_TARGET: ('var', 'enable_fx_target', factor)},1: {_ENABLE_FX_TARGET: ('var', 'enable_fx_target', factor)}})
                global_data.display_agent.update_longtime_post_process_params('hdr', {5: {_ENABLE_FX_TARGET: ('var', 'enable_fx_target', factor)},6: {_ENABLE_FX_TARGET: ('var', 'enable_fx_target', factor)}})
            else:
                global_data.display_agent.update_longtime_post_process_params('hdr_tonemap', {0: {_ENABLE_FX_TARGET: ('var', 'enable_fx_target', factor)}})

    @sync_exec
    def _check_apply_pp(self):
        if self._pp_dirty:
            self._pp_dirty = False
            for item in six.itervalues(self._postprocesslist):
                if item.dirty:
                    self._flush_pp(item)

            global_data.emgr.check_apply_postprocess.emit()

    def stop_radial_blur(self):
        self.set_post_effect_active('radial_blur', False)

    def enable_tonemap(self, enable, params=None):
        from logic.vscene.global_display_setting import GlobalDisplaySeting, FINE
        gds = GlobalDisplaySeting()
        low_mode = pc_platform_utils.is_pc_hight_quality() is False and gds.get_actual_quality() <= FINE
        if params is not None:
            self.update_tonemap(params)
        self.set_longtime_post_process_active('hdr_tonemap', False)
        self.set_longtime_post_process_active('hdr', False)
        self.set_longtime_post_process_active('hdr' if low_mode else 'hdr_tonemap', enable)
        return

    def update_tonemap(self, params):
        self.update_longtime_post_process_params('hdr_tonemap', params)
        self.update_longtime_post_process_params('hdr', params)

    def update_bloom(self, params):
        self.update_longtime_post_process_params('bloom', params)
        subs = params.pop(5)
        subs.update(params.pop(6))
        params[2] = subs
        self.update_longtime_post_process_params('bloom_low', params)

    def enable_bloom(self, enable, params=None):
        from logic.vscene.global_display_setting import GlobalDisplaySeting, FINE
        gds = GlobalDisplaySeting()
        low_mode = pc_platform_utils.is_pc_hight_quality() is False and gds.get_actual_quality() <= FINE
        if params is not None:
            self.update_bloom(params)
        self.set_longtime_post_process_active('bloom', False)
        self.set_longtime_post_process_active('bloom_low', False)
        self.set_longtime_post_process_active('bloom_low' if low_mode else 'bloom', enable)
        return


def get_calc_scale():
    from logic.vscene.global_display_setting import GlobalDisplaySeting
    gds = GlobalDisplaySeting()
    min_scale = 0.1
    if is_win32():
        min_scale = 0.98
    elif is_ios():
        size = game3d.get_window_size()
        min_size = 750.0
        min_scale = min(min_size / size[1], 1.0)
    elif is_android():
        size = game3d.get_window_size()
        min_size = 540.0
        min_scale = min(min_size / size[1], 1.0)
    return max(min_scale, gds.quality_value('RESOLUTION'))


def check_pipeline_ingame_inited():
    global_data.display_agent.set_pipeline(global_data.display_agent._pipeline_ingame_path)


def check_reset_resolution():
    check_pipeline_ingame_inited()
    if version.get_tag() == 'trunk':
        game3d.show_render_info(not global_data.block_render_info, 10, 400)
        import cc
        cc.Director.getInstance().setDisplayStats(not global_data.block_render_info)
        if hasattr(game3d, 'renderdoc_show_overlay'):
            game3d.renderdoc_show_overlay(not global_data.block_render_info)
    else:
        game3d.show_render_info(False, 10, 10)
    gds = GlobalDisplaySeting()
    gds.reset_frame_rate()
    h_scale = get_calc_scale()
    cur_scale = render.get_redirect_scale()
    if abs(cur_scale - h_scale) < 0.001:
        print('no need to set_redirect_scale')
        return
    size = game3d.get_window_size()
    w = int(size[0] * h_scale)
    h = int(size[1] * h_scale)
    print('Resolution set_redirect_scale scale:%s, origin:%s*%s, new:%s*%s=====' % (h_scale, size[0], size[1], w, h))
    global_data.display_agent.set_redirect_scale(h_scale)


def check_reset_resolution_ex(force_set=False):
    print('Run check_reset_resolution_ex...', force_set)
    check_pipeline_ingame_inited()
    gds = GlobalDisplaySeting()
    gds.switch_device_resolution(force_set)
    do_reload_postprocess_ingame()
    gds.process_switch_resolution_consistency()
    if version.get_tag() == 'trunk':
        game3d.show_render_info(not global_data.block_render_info, 10, 400)
        import cc
        cc.Director.getInstance().setDisplayStats(not global_data.block_render_info)
        if hasattr(game3d, 'renderdoc_show_overlay'):
            game3d.renderdoc_show_overlay(not global_data.block_render_info)
    else:
        game3d.show_render_info(False, 10, 10)


def do_reload_postprocess_ingame():
    check_pipeline_ingame_inited()