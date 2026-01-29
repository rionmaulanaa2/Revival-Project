# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBloodSimUI.py
from __future__ import absolute_import
import math3d
import world
import render
from ..UnitCom import UnitCom
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref

class ComBloodSimUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_HEALTH_HP_CHANGE': '_on_hp_changed',
       'E_SHOW_BLOOD_SIM_UI': '_show_hp_info',
       'E_HIDE_BLOOD_SIM_UI': 'on_hide_sim_ui',
       'E_MAX_HP_CHANGED': 'on_max_hp_changed'
       }
    UI_ATTR_LIST = ('_hp_back', '_hp_trail', '_hp_low', '_hp', '_hp_head_line')

    def __init__(self):
        super(ComBloodSimUI, self).__init__()
        self._simui = None
        self._hp_cur = 0
        self._hp_max = 100
        self.tm = None
        self._hp_head_line_timer = None
        self._hp_trail_timer = None
        self._hp_show_timer = None
        self._hp_head_line_alpha = 0
        self._blood_trail = 0
        self._hp_show_cnt = 0
        self._model_ref = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBloodSimUI, self).init_from_dict(unit_obj, bdict)
        self.tm = global_data.game_mgr.get_logic_timer()
        self._hp_max = bdict.get('max_hp', 100)
        self._hp_cur = bdict.get('hp', self._hp_max)

    def cache(self):
        self._clear_ui()
        self._model_ref = None
        self._blood_trail = 0
        self._hp_head_line_alpha = 0
        super(ComBloodSimUI, self).cache()
        return

    def on_max_hp_changed(self, max_hp, hp, *args):
        self._hp_max = max_hp

    def get_simui_fill_z(self):
        return True

    def on_model_loaded(self, model, box=None):
        self._model_ref = weakref.ref(model)
        self._create_hp_ui(model, box)

    def on_hide_sim_ui(self):
        self._simui.visible = False

    def tick(self, delta):
        if self._simui and self.scene and self.scene.active_camera:
            model = self._model_ref() if self._model_ref else None
            if model:
                pos = model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                max_dist = 300
                scale = (max_dist - dist) * 1.0 / max_dist
                self._simui.scale = (scale, scale)
        return

    def _show_hp_info(self):
        self._hp_show_cnt = 3
        if self._simui and self._simui.valid and not self.need_update:
            self._simui.visible = True
            self.need_update = True
            if not self._hp_show_timer:

                def cb(*args):
                    if not self or not self.is_enable():
                        return
                    else:
                        self._hp_show_cnt -= 1
                        if self._hp_show_cnt <= 0:
                            self.tm.unregister(self._hp_show_timer)
                            self._hp_show_timer = None
                            self._simui.visible = False
                            self.need_update = False
                        return

                self._hp_show_timer = self.tm.register(func=cb, interval=1, times=-1, mode=CLOCK)

    def _create_hp_ui(self, model, box=None):
        self.scene.simui_enable_post_process(True)
        self._simui = world.simuiobject(render.texture('gui/ui_res_2/simui/sim_mech_hp.png'))
        self._hp_back = self._simui.add_image_ui(0, 0, 150, 18, 0, 0)
        self._hp_trail = self._simui.add_image_ui(2, 34, 144, 12, 0, 0)
        self._hp = self._simui.add_image_ui(2, 20, 144, 12, 0, 0)
        self._hp_low = self._simui.add_image_ui(2, 48, 144, 12, 0, 0)
        self._hp_head_line = self._simui.add_image_ui(10, 90, 6, 24, -75, 0)
        self._head_line_begin_x = -75
        self._head_line_width = 146
        self._head_line_y = 0
        for ui_attr in ComBloodSimUI.UI_ATTR_LIST:
            ui_inst = getattr(self, ui_attr, None)
            if ui_inst:
                self._simui.set_ui_align(ui_inst, 0.5, 0.5)
                self._simui.set_ui_skew(ui_inst, 0.27, 0)
                self._simui.set_ui_fill_z(ui_inst, self.get_simui_fill_z())
                self._simui.set_imageui_horpercent(ui_inst, 0.0, 1.0)

        self._simui.set_imageui_horpercent(self._hp_low, 0.0, 0.0)
        self._simui.set_ui_alpha(self._hp_head_line, 0)
        self._simui.set_parent(model)
        self._simui.inherit_flag = world.INHERIT_TRANSLATION
        simui_pos = self.get_simui_pos()
        if not simui_pos:
            if box is None:
                box = model.bounding_box
            scale_y = model.scale.y
            self._simui.position = math3d.vector(0, box.y * 2 * scale_y + 10, 0)
        else:
            self._simui.position = simui_pos
        self._simui.visible = False
        self._blood_trail = self._hp_cur
        hp_percent = self._blood_trail * 1.0 / self._hp_max
        self._simui.set_imageui_horpercent(self._hp, 0.0, hp_percent)
        self._simui.set_imageui_horpercent(self._hp_trail, 0.0, hp_percent)
        return

    def get_simui_pos(self):
        pass

    def _on_hp_changed(self, hp, mod=0):
        self._show_hp_info()
        old_hp = self._hp_cur
        self._hp_cur = hp
        if self._simui and self._simui.valid and self._hp_max:
            percent = hp * 1.0 / self._hp_max
            if hp <= 0:
                self._simui.visible = False
            self._simui.set_imageui_horpercent(self._hp, 0.0, percent)
            self._simui.set_imageui_horpercent(self._hp_low, 0.0, 0.0)
            if self._hp_cur < old_hp:

                def hp_diff_cb(*args):
                    if not self or not self.is_enable():
                        return
                    else:
                        if not self._simui or not self._simui.valid:
                            return
                        self._blood_trail -= (old_hp - self._hp_cur) / 30.0
                        self._hp_trail_alpha -= 8
                        if self._blood_trail <= self._hp_cur:
                            self._blood_trail = self._hp_cur
                        blood_trail_percent = self._blood_trail * 1.0 / self._hp_max
                        self._simui.set_imageui_horpercent(self._hp_trail, 0, blood_trail_percent)
                        self._simui.set_ui_alpha(self._hp_trail, self._hp_trail_alpha)
                        if self._blood_trail == self._hp_cur:
                            self.tm.unregister(self._hp_trail_timer)
                            self._hp_trail_timer = None
                        return

                if self._hp_trail_timer:
                    self.tm.unregister(self._hp_trail_timer)
                    self._hp_trail_timer = None
                    self._blood_trail = old_hp
                    blood_trail_percent = old_hp * 1.0 / self._hp_max
                    self._simui.set_ui_alpha(self._hp_trail, 0)
                    self._simui.set_imageui_horpercent(self._hp_trail, 0.0, blood_trail_percent)
                self._hp_trail_alpha = 255
                self._simui.set_ui_alpha(self._hp_trail, self._hp_trail_alpha)
                self._hp_trail_timer = self.tm.register(func=hp_diff_cb, interval=0.033, times=-1, mode=CLOCK)

                def hp_head_line_cb(*args):
                    if not self or not self.is_enable():
                        return
                    else:
                        if not self._simui or not self._simui.valid:
                            return
                        self._hp_head_line_alpha -= 8
                        if self._hp_head_line_alpha < 0:
                            self._hp_head_line_alpha = 0
                        self._simui.set_ui_alpha(self._hp_head_line, self._hp_head_line_alpha)
                        if self._hp_head_line_alpha == 0:
                            self.tm.unregister(self._hp_head_line_timer)
                            self._hp_head_line_timer = None
                        return

                if self._hp_head_line_timer:
                    self.tm.unregister(self._hp_head_line_timer)
                    self._hp_head_line_timer = None
                    self._simui.set_ui_alpha(self._hp_head_line, 0)
                cur_head_line_x = percent * self._head_line_width + self._head_line_begin_x
                self._simui.set_ui_pos(self._hp_head_line, cur_head_line_x, self._head_line_y)
                self._hp_head_line_alpha = 255
                self._simui.set_ui_alpha(self._hp_head_line, self._hp_head_line_alpha)
                self._hp_head_line_timer = self.tm.register(func=hp_head_line_cb, interval=0.033, times=-1, mode=CLOCK)
            else:
                self._blood_trail = self._hp_cur
                self._simui.set_imageui_horpercent(self._hp_trail, 0.0, percent)
        return

    def _clear_ui(self):
        if self._hp_head_line_timer:
            self.tm.unregister(self._hp_head_line_timer)
            self._hp_head_line_timer = None
        if self._hp_trail_timer:
            self.tm.unregister(self._hp_trail_timer)
            self._hp_trail_timer = None
        if self._hp_show_timer:
            self.tm.unregister(self._hp_show_timer)
            self._hp_show_timer = None
        if self._simui and self._simui.valid:
            try:
                self._simui.destroy()
            except:
                pass

            self._simui = None
        return

    def destroy(self):
        self._clear_ui()
        super(ComBloodSimUI, self).destroy()