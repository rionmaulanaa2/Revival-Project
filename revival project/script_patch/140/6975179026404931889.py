# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComShieldBloodSimUI.py
from __future__ import absolute_import
import math3d
import world
import render
from ..UnitCom import UnitCom
from logic.gcommon.item.item_const import DRESS_POS_SHIELD
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref

class ComShieldBloodSimUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_ARMOR_DATA_CHANGED': 'on_armor_data_changed'
       }

    def __init__(self):
        super(ComShieldBloodSimUI, self).__init__()
        self._simui = None
        self._model_ref = None
        self._hide_timer = None
        self.last_percent = 1.0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComShieldBloodSimUI, self).init_from_dict(unit_obj, bdict)

    def cache(self):
        self._clear_shield_hp_ui()
        self._model_ref = None
        super(ComShieldBloodSimUI, self).cache()
        return

    def destroy(self):
        self._clear_shield_hp_ui()
        self._model_ref = None
        super(ComShieldBloodSimUI, self).destroy()
        return

    def tick(self, delta):
        if self._simui and self.scene and self.scene.active_camera:
            if self._model_ref:
                model = self._model_ref() if 1 else None
                if model:
                    cam = self.scene.active_camera
                    pos = model.position
                    fov = cam.fov
                    dist = cam.position - pos
                    dist = dist.length / NEOX_UNIT_SCALE
                    if dist <= 2:
                        scale = 1.0
                    elif dist <= 10:
                        scale = 0.4 + 0.6 * (10 - dist) / 10
                    elif dist <= 20:
                        scale = 0.2 + 0.2 * (20 - dist) / 10
                    elif dist <= 50:
                        scale = 0.1 + 0.1 * (50 - dist) / 30
                    else:
                        scale = 0.1
                    if dist > 40:
                        scale = min(scale * 62 / fov / 1.5, 1.0)
                    else:
                        scale = min(scale * 62 / fov, 1.0)
                    self._simui.scale = (
                     scale, scale)
                    direction = pos - cam.position
                    direction.y = 0
                    direction.is_zero or direction.normalize()
                    up = math3d.vector(0, 1, 0)
                    right = up.cross(direction)
                    offset = 6 + 2.5 * fov / 62
                    self._simui.position = math3d.vector(0, 13, 0) + right * offset - direction * 5.0
        return

    def on_model_loaded(self, model, box=None):
        self._model_ref = weakref.ref(model)
        if not global_data.player:
            return
        if global_data.player.logic and global_data.player.logic.ev_g_is_groupmate(self.unit_obj.id):
            return
        self._create_shield_hp_ui(model, box)

    def _create_shield_hp_ui(self, model, box=None):
        self.scene.simui_enable_post_process(True)
        self._simui = world.simuiobject(render.texture('gui/ui_res_2/simui/sim_shield_hp.png'))
        self._hp_bg = self._simui.add_image_ui(0, 0, 18, 150, 0, 0)
        self._hp = self._simui.add_image_ui(20, 2, 12, 144, 0, 0)
        attr_list = ('_hp', '_hp_bg')
        for name_attr in attr_list:
            ui_inst = getattr(self, name_attr, None)
            if ui_inst:
                self._simui.set_ui_align(ui_inst, 0.5, 0.5)
                self._simui.set_ui_fill_z(ui_inst, True)
                self._simui.set_imageui_verpercent(ui_inst, 0.0, 1.0)

        self._simui.set_parent(model)
        self._simui.inherit_flag = world.INHERIT_TRANSLATION
        self._simui.position = math3d.vector(0, 10, 0)
        self._simui.visible = False
        self._simui.set_ui_color(self._hp_bg, (230, 255, 255, 255))
        return

    def _clear_shield_hp_ui(self):
        self._try_release_hide_timer()
        if self._simui and self._simui.valid:
            try:
                self._simui.destroy()
            except:
                pass

            self._simui = None
        return

    def _hide_shield_hp_ui(self):
        self._hide_simui()
        self._hide_timer = None
        return

    def _hide_simui(self):
        self._simui.visible = False
        self.need_update = False

    def _try_release_hide_timer(self):
        if self._hide_timer:
            global_data.game_mgr.unregister_logic_timer(self._hide_timer)
            self._hide_timer = None
            return True
        else:
            return False

    def on_armor_data_changed(self, pos, armor):
        if pos == DRESS_POS_SHIELD and self._simui and self._simui.valid:
            if not armor:
                self._try_release_hide_timer()
                self._hide_simui()
                return
            percent = armor.get_duration_percent()
            if percent < self.last_percent:
                if percent > 0.0:
                    if not self._try_release_hide_timer():
                        self.tick(0.0)
                        self._simui.visible = True
                        self.need_update = True
                    self._hide_timer = global_data.game_mgr.register_logic_timer(self._hide_shield_hp_ui, interval=1, times=1, mode=CLOCK)
                else:
                    self._try_release_hide_timer()
                    self._hide_simui()
                    return
                self._simui.set_imageui_verpercent(self._hp, 1.0 - percent, 1.0)
                if percent < 0.5:
                    self._simui.set_ui_color(self._hp, (120, 255, 20, 0))
                else:
                    self._simui.set_ui_color(self._hp, (120, 255, 255, 255))
            self.last_percent = percent