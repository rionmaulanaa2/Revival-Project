# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComHandyShieldAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import weakref
from logic.gcommon.common_const.mecha_const import DEFEND_OFF, DEFEND_ON
import math3d
import world
import render
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
SHIELD_BREAK_SOUND = 'Play_universal_skill_yandun'

class ComHandyShieldAppearance(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_HANDY_SHIELD_HP': 'on_shield_hp_change',
       'E_ENTER_DEFEND': 'on_enter_defend',
       'E_EXIT_DEFEND': 'on_exit_defend'
       }

    def __init__(self):
        super(ComHandyShieldAppearance, self).__init__()
        self._simui = None
        self._hide_timer = None
        self.need_update = True
        self.max_shield_hp = 1
        self.defend_state = DEFEND_OFF
        self.mecha_model = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHandyShieldAppearance, self).init_from_dict(unit_obj, bdict)
        self.init_params(bdict)

    def init_params(self, bdict):
        self.mecha_id = bdict['mecha_id']
        self.mecha_model = None
        self.model = None
        self.model_id = None
        self.max_shield_hp = bdict.get('max_shield_hp', 1)
        self.defend_state = bdict.get('defend_state', DEFEND_OFF)
        return

    def _on_model_loaded(self, model):
        self.mecha_model = weakref.ref(model)
        self.send_event('E_ON_LOAD_SHIELD_MODEL', None, self.mecha_model)
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        else:
            driver_id = self.sd.ref_driver_id
            is_self = driver_id == cam_lplayer.id
            is_groupmate = cam_lplayer.ev_g_is_groupmate(driver_id)
            need_show_hp_ui = not is_self and not is_groupmate
            if not need_show_hp_ui:
                return
            self._create_shield_hp_ui(model)
            return

    def cache(self):
        self._clear_shield_hp_ui()
        self.mecha_model = None
        super(ComHandyShieldAppearance, self).cache()
        return

    def destroy(self):
        self._clear_shield_hp_ui()
        self.mecha_model = None
        super(ComHandyShieldAppearance, self).destroy()
        return

    def on_enter_defend(self):
        self.defend_state = DEFEND_ON

    def on_exit_defend(self):
        self.defend_state = DEFEND_OFF

    def _create_shield_hp_ui(self, model, box=None):
        self.scene.simui_enable_post_process(True)
        self._simui = world.simuiobject(render.texture('gui/ui_res_2/simui/sim_shield_hp_s.png'))
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
        self._simui.position = math3d.vector(10, 20, 0)
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

    def on_shield_hp_change(self, hp):
        if hp <= 0.0 and global_data.cam_lplayer and self.unit_obj.sd.ref_driver_id == global_data.cam_lplayer.id:
            global_data.sound_mgr.post_event_2d(SHIELD_BREAK_SOUND, None)
        if not self._simui or not self._simui.valid:
            return
        else:
            if self.defend_state == DEFEND_OFF:
                return
            percent = hp / self.max_shield_hp
            percent = max(0, min(percent, 1))
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
            if percent < 0.3:
                self._simui.set_ui_color(self._hp, (120, 255, 0, 0))
            else:
                self._simui.set_ui_color(self._hp, (120, 0, 0, 255))
            return

    def tick(self, delta):
        if not self._simui or not self.scene or not self.scene.active_camera:
            return
        else:
            if self.mecha_model:
                model = self.mecha_model() if 1 else None
                if not model:
                    return
                if self.defend_state == DEFEND_OFF:
                    return
                cam = self.scene.active_camera
                pos = model.position
                fov = cam.fov
                dist = cam.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                if dist <= 40:
                    scale = 1 - 0.015 * dist
                elif dist <= 70:
                    scale = 0.7 - 0.007 * dist
                elif dist <= 120:
                    scale = 0.2
                else:
                    scale = 0.1
                fov_scale = 54.0 / fov
                scale = scale * fov_scale
                self._simui.scale = (scale, scale)
                direction = pos - self.scene.active_camera.position
                direction.y = 0
                direction.is_zero or direction.normalize()
                up = math3d.vector(0, 1, 0)
                right = up.cross(direction)
                self._simui.position = -direction * 10 + math3d.vector(0, 40, 0) + -right * 50
            else:
                self._simui.position = math3d.vector(0, 40, 0)
            return