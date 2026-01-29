# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/effect/screen_effect.py
from __future__ import absolute_import
import six
from common.framework import Singleton
SCREEN_EFFECT_MODEL = 0
SCREEN_EFFECT_FX = 1
import math3d
import game3d
import render
import logic.gcommon.const as g_const
from logic.gutils.screen_effect_utils import SCREEN_EFFECT_SCALE

class Effect(Singleton):

    def init(self, info_dict={}):
        pass

    def show(self):
        pass

    def hide(self):
        pass

    def isVisible(self):
        return False

    def destroy(self):
        self.finalize()

    def show_with_parameters(self, info_dict):
        raise NotImplementedError('effect %s need this', self.__class__.__name__)


class ScreenEffect(Effect):
    EFFECT_FILE_PATH = ''
    EFFECT_TYPE = ''
    MOUNTED = 1
    UNMOUNTED = 4
    FULL_SCREEN_SFX = False

    def init(self, info_dict={}):
        self.status = ScreenEffect.UNMOUNTED
        self.effect_inst = None
        self.model_task = None
        self.render_vars_dict = info_dict.get('render_vars', {})
        self.effect_pos = info_dict.get('position', math3d.vector(0, 0, 10))
        self.sfx_loop = info_dict.get('loop', False)
        self.init_visible = True
        self._var_name_hash = {}
        self.show()
        return

    def show(self):
        self.init_visible = True
        if self.effect_inst and self.effect_inst.valid:
            self.effect_inst.visible = True
            if self.EFFECT_TYPE == SCREEN_EFFECT_FX:
                self.effect_inst.loop = self.sfx_loop
                self.effect_inst.restart()
            return
        else:
            if self.model_task:
                return
            import world
            if self.EFFECT_TYPE == SCREEN_EFFECT_MODEL:
                self.model_task = world.create_model_async(self.EFFECT_FILE_PATH, self._load_model_callback)
            else:
                self.model_task = world.create_sfx_async(self.EFFECT_FILE_PATH, self._load_model_callback, None, game3d.ASYNC_HIGH)
            return

    def _load_model_callback(self, model, user_data, current_task=None):
        if self.model_task is None:
            model.destroy()
            return
        else:
            self.effect_inst = model
            self.model_task = None
            import world
            try:
                camera = world.get_active_scene().active_camera
            except:
                log_error("can't find camera when create screen effect")
                return

            self.effect_inst.set_parent(camera)
            if self.effect_pos:
                self.effect_inst.position = self.effect_pos
            self.status = ScreenEffect.MOUNTED
            if self.render_vars_dict:
                self.set_render_parameters(self.render_vars_dict)
            if self.EFFECT_TYPE == SCREEN_EFFECT_FX:
                self.effect_inst.loop = self.sfx_loop
            self.show() if self.init_visible else self.hide()
            if self.FULL_SCREEN_SFX:
                self.effect_inst.scale = SCREEN_EFFECT_SCALE
            return

    def isVisible(self):
        if self.effect_inst and self.effect_inst.valid:
            return self.effect_inst.visible
        else:
            return False

    def hide(self):
        self.init_visible = False
        if self.effect_inst and self.effect_inst.valid:
            self.effect_inst.visible = False
            if self.EFFECT_TYPE == SCREEN_EFFECT_FX:
                self.effect_inst.shutdown()

    def destroy(self):
        if self.model_task:
            try:
                self.model_task.cancel()
            except Exception:
                pass

            self.model_task = None
        if self.effect_inst and self.effect_inst.valid:
            self.effect_inst.destroy()
        self.effect_inst = None
        super(ScreenEffect, self).destroy()
        return

    def set_render_parameter(self, var_name, var_val):
        if self.status == ScreenEffect.UNMOUNTED:
            log_error('try to set_effect_parameter but effect not loaded!')
            return
        if self.EFFECT_TYPE == SCREEN_EFFECT_MODEL:
            if self.effect_inst and self.effect_inst.valid:
                if var_name not in self._var_name_hash:
                    self._var_name_hash[var_name] = game3d.calc_string_hash(var_name)
                self.effect_inst.all_materials.set_var(self._var_name_hash[var_name], var_name, var_val)

    def set_render_parameters(self, render_dict):
        for k, v in six.iteritems(render_dict):
            self.set_render_parameter(k, v)

    def show_with_parameters(self, info_dict):
        if not self.isVisible():
            self.show()
        render_vars_dict = info_dict.get('render_vars', {})
        if self.effect_inst and self.effect_inst.valid:
            self.set_render_parameters(render_vars_dict)
        else:
            self.render_vars_dict = render_vars_dict


class PostProcessEffect(ScreenEffect):
    KEY = ''

    def init(self, info_dict):
        self._postprocess_key = self.KEY
        super(PostProcessEffect, self).init(info_dict)
        self.show_with_parameters(info_dict)

    def show(self):
        global_data.display_agent.set_post_effect_active(self._postprocess_key, True)

    def hide(self):
        global_data.display_agent.set_post_effect_active(self._postprocess_key, False)

    def set_render_parameter(self, var_name, var_val):
        if var_name not in self._var_name_hash:
            self._var_name_hash[var_name] = game3d.calc_string_hash(var_name)
        post_effect = global_data.display_agent.get_post_effect_pass_mtl(self._postprocess_key, 0)
        if post_effect:
            post_effect.set_var(self._var_name_hash[var_name], var_name, var_val)

    def show_with_parameters(self, info_dict):
        self.show()
        render_vars_dict = info_dict.get('render_vars', {})
        self.set_render_parameters(render_vars_dict)

    def destroy(self):
        self.hide()


class DarkCornerEffect(PostProcessEffect):
    KEY = 'dark_corner'

    def init(self, info_dict):
        super(DarkCornerEffect, self).init(info_dict)


class ParachuteSlow(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/robot/robot_qishi/qishi_fly_pm.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX

    def init(self, *args, **kwargs):
        super(ParachuteSlow, self).init(*args, **kwargs)
        self.show()


class ParachuteFast(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/tiaosan/huaxiang_kuai.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX


class MechaChongCiEffect(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/robot/autobot/autobot_pinmujiasu.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX


class HumanRushEffect(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/renwu/rw_chongci_speedline.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX


class MeleeRushEffect(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/robot/robot_qishi/robot_qishi_penqi_jump_distortion.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX


class ScreenShakeMeta(ScreenEffect):
    EFFECT_FILE_PATH = ''
    EFFECT_TYPE = SCREEN_EFFECT_FX


class ScreenWhite(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/pingmu/jicang_baiping_distortion.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX
    FULL_SCREEN_SFX = True


class ScreenMapStart(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/scenes/common/map/start_02.sfx'
    EFFECT_TYPE = True
    FULL_SCREEN_SFX = True


class ScreenMapEnd(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/scenes/common/map/map_end.sfx'
    EFFECT_TYPE = True
    FULL_SCREEN_SFX = True


class ScreenSpeedLine(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/robot/robot_qishi/robot_suduxian_pinmu2.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX

    def init(self, *args, **kwargs):
        super(ScreenSpeedLine, self).init(*args, **kwargs)
        self.sfx_loop = True
        self.show()


class ScreenNBombPlaced(ScreenEffect):
    EFFECT_FILE_PATH = 'effect/fx/niudan/hedanwanfa/hd_sky_pm.sfx'
    EFFECT_TYPE = SCREEN_EFFECT_FX
    FULL_SCREEN_SFX = True

    def init(self, *args, **kwargs):
        super(ScreenNBombPlaced, self).init(*args, **kwargs)
        self.sfx_loop = True
        self.show()


class GrayEffect(Effect):
    _HASH_gray_factor = game3d.calc_string_hash('gray_factor')

    def init(self, info_dict):
        super(GrayEffect, self).init(info_dict)
        self.show_with_parameters(info_dict)

    def show(self):
        import render
        global_data.display_agent.set_post_effect_active('gray', True)

    def hide(self):
        import render
        global_data.display_agent.set_post_effect_active('gray', False)

    def set_render_parameter(self, var_val):
        import render
        post_effect = global_data.display_agent.get_post_effect_pass_mtl('gray', 0)
        if post_effect:
            post_effect.set_var(GrayEffect._HASH_gray_factor, 'gray_factor', var_val)

    def show_with_parameters(self, info_dict):
        self.show()
        self.set_render_parameter(info_dict.get('gray_factor', 1.0))

    def destroy(self):
        self.hide()


class GaussanBlurEffect(Effect):

    def init(self, info_dict):
        super(GaussanBlurEffect, self).init(info_dict)
        self.show_with_parameters(info_dict)

    def show(self):
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def hide(self):
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def show_with_parameters(self, info_dict):
        self.show()

    def destroy(self):
        self.hide()