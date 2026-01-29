# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTargetBloodUI.py
from __future__ import absolute_import
import math3d
from logic.gcommon.component.client.ComBloodUI import ComBloodUI
import time
TEXTURE_PATH = 'model_new/others/xuetiao/'

class ComTargetBloodUI(ComBloodUI):
    NORMAL_HP_TEXTURE = TEXTURE_PATH + 'jijiaxueliangshouji.tga'
    DEAD_ANIMATION = False
    Z_AIM_MIN = 300

    def __init__(self):
        super(ComTargetBloodUI, self).__init__()
        self.force_hide = False
        self._target_bias = 0
        self._cur_bias = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComTargetBloodUI, self).init_from_dict(unit_obj, bdict)
        self.init_ui_event()

    def init_ui_event(self):
        global_data.emgr.ui_enter_aim += self._try_aim
        global_data.emgr.ui_leave_aim += self._quit_aim

    def _blood_bar_load_callback(self, model, *args):
        super(ComTargetBloodUI, self)._blood_bar_load_callback(model, *args)

    def _get_socket(self):
        return ('empty', 0)

    def tick(self, dt):
        super(ComTargetBloodUI, self).tick(dt)

    def tick_model_ui(self, model):
        super(ComTargetBloodUI, self).tick_model_ui(model)
        if not self.showing_model_ui:
            return
        delta = self._target_bias - self._cur_bias
        if delta == 0:
            return
        if delta > 0:
            self._cur_bias += 1
        else:
            self._cur_bias -= 1
        model.position = math3d.vector(0, self._cur_bias, 0)

    def _try_aim(self, *args):
        model = self.get_model()
        if not model:
            return
        self.set_var('ZMin', self.Z_AIM_MIN, model, -1)

    def _quit_aim(self, *args):
        model = self.get_model()
        if not model:
            return
        self.set_var('ZMin', self.Z_MIN, model, -1)

    def _on_show_hp_info(self):
        if self.force_hide:
            return
        else:
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                self.showing_model_ui or self.check_in_danger(model)
                if self._cur_bias != self._target_bias:
                    self._cur_bias = self._target_bias
                    model.position = math3d.vector(0, self._cur_bias, 0)
                self.showing_model_ui = model.visible = True
                self.need_update = True
            self._hide_time = time.time() + self._get_visible_time()
            return

    def check_in_danger(self, model=None):
        in_danger = self._hp < self._hp_max * 0.25
        if self._in_danger ^ in_danger:
            self._in_danger = in_danger
            texture = self.DANGER_BAR_TEXTURE if in_danger else self.NORMAL_BAR_TEXTURE
            self.set_texture('_TexBackGround', texture, model)

    def _on_hp_change(self, hp, mod):
        if self.showing_model_ui:
            model = self._model() if self._model else None
            if model:
                self.check_in_danger(model)
        super(ComTargetBloodUI, self)._on_hp_change(hp, mod)
        return

    def destroy(self):
        super(ComTargetBloodUI, self).destroy()