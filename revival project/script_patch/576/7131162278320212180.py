# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComHumanTransparentCam.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import render
import math

class ComHumanTransparentCam(UnitCom):
    BIND_EVENT = {'E_DRESS_CHANGED_FINISHED': 'on_finish_change_dress',
       'E_ON_CONTROL_TARGET_CHANGE': 'on_switch_control_target'
       }

    def __init__(self):
        super(ComHumanTransparentCam, self).__init__()
        self.need_update = False
        self._is_in_opacity = False
        self._opacity = 255
        self.init_conf()

    def on_init_complete(self):
        self.check_control_target()

    def check_control_target(self):
        control_target = self.ev_g_control_target()
        if control_target and control_target.logic == self.unit_obj:
            self.need_update = True
        else:
            self.need_update = False
            self.leave_opacity_mode()

    def on_switch_control_target(self, target_id, pos, *args):
        self.check_control_target()

    def init_conf(self):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        self._start_opacity = 127.5
        self._opacity_distance = 0.8 * NEOX_UNIT_SCALE
        self._must_opacity_distance = 0.4 * NEOX_UNIT_SCALE
        self._angle_threshold = math.radians(30)

    def destroy(self):
        self.need_update = False
        if self._is_in_opacity:
            self.leave_opacity_mode()
        super(ComHumanTransparentCam, self).destroy()

    def tick(self, delta):
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            dist = partcam.get_camera_to_focus_hoz_length()
            if not dist:
                return
            need_opacity = dist < self._must_opacity_distance or dist < self._opacity_distance and partcam.get_pitch() < self._angle_threshold
            if not need_opacity:
                self.leave_opacity_mode()
            else:
                percent = dist / self._opacity_distance
                opacity = self._start_opacity * percent
                self.enter_opacity_mode(opacity)

    def enter_opacity_mode(self, opacity):
        self.send_event('E_SET_MODEL_OPACITY', opacity)

    def leave_opacity_mode(self):
        self.send_event('E_LEAVE_MODEL_OPACITY')

    def on_finish_change_dress(self):
        if self.ev_g_is_model_opacity():
            self.leave_opacity_mode()
            self.enter_opacity_mode(self._opacity)