# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/RotateSystem.py
from __future__ import absolute_import
import cython_flag
from logic.gcommon.component.system.SystemBase import SystemBase, FPS_30
from logic.gcommon.component.client.ComDataRenderRotate import ComDataRenderRotate, YAW_MODE_LINK_HEAD, YAW_MODE_LERP_HEAD, PITCH_MODE_LERP_ZERO, PITCH_MODE_LINK_HEAD
from logic.gcommon.component.client.ComDataAppearance import ComDataAppearance
from logic.gcommon.component.client.ComDataCamTarget import ComDataCamTarget
from logic.gcommon.behavior.MoveLogic import Turn
import math3d
import math
import exception_hook
PI = math.pi
PI2 = PI + PI
PITCH_MAX = 0.8
PITCH_MIN = -0.6
C_YAW_MODE_LINK_HEAD = YAW_MODE_LINK_HEAD
C_YAW_MODE_LERP_HEAD = YAW_MODE_LERP_HEAD
C_PITCH_MODE_LERP_ZERO = PITCH_MODE_LERP_ZERO
C_PITCH_MODE_LINK_HEAD = PITCH_MODE_LINK_HEAD

class RotateSystem(SystemBase):

    def __init__(self, tick_step=FPS_30):
        super(RotateSystem, self).__init__(tick_step)
        self._sub_sys_list = []
        self._data_to_handler = {}

    def interested_type(self):
        return (
         ComDataRenderRotate, ComDataAppearance)

    def ignored_type(self):
        return (
         ComDataCamTarget,)

    def handler_types(self):
        return [
         Turn.HANDLER_TYPE]

    def lerp_data(self, current_val, target_val, cur_time, total_time):
        u = cur_time / total_time
        delta_val = target_val - current_val
        if delta_val > PI:
            current_val += PI2
            delta_val -= PI2
        elif delta_val < -PI:
            current_val -= PI2
            delta_val += PI2
        return current_val + delta_val * u * u

    def tick(self, dt):
        for unit in self._element_list:
            try:
                data = unit.sd.ref_rotatedata
                if data.use_quaternion or data.dirty:
                    handler = self._data_to_handler.get(unit)
                    if handler:
                        handler.on_action_yaw(data, data.force_turn_body)
                if data.yaw_body != data.yaw_head:
                    if data.yaw_body_mode == C_YAW_MODE_LINK_HEAD:
                        data.yaw_body = data.yaw_head
                        data.dirty = True
                    elif data.yaw_body_mode == C_YAW_MODE_LERP_HEAD:
                        data.yaw_lerp_factor += dt
                        if data.yaw_lerp_factor < data.yaw_duration:
                            data.yaw_body = self.lerp_data(data.yaw_body, data.yaw_head, data.yaw_lerp_factor, data.yaw_duration)
                            data.dirty = True
                        else:
                            data.yaw_body_mode = C_YAW_MODE_LINK_HEAD
                            data.yaw_body = data.yaw_head
                            data.dirty = True
                if data.pitch_body_mode:
                    if data.pitch_body_mode == C_PITCH_MODE_LINK_HEAD:
                        data.dirty = data.dirty or data.pitch_body != data.pitch_head
                        data.pitch_body = data.pitch_head
                    else:
                        data.dirty = True
                        data.pitch_lerp_factor += dt
                        if data.pitch_body_mode == C_PITCH_MODE_LERP_ZERO:
                            pitch_target = 0 if 1 else data.pitch_head
                            if data.pitch_lerp_factor < data.pitch_duration:
                                data.pitch_body = self.lerp_data(data.pitch_body, pitch_target, data.pitch_lerp_factor, data.pitch_duration)
                            else:
                                data.pitch_body_mode -= 1
                                data.pitch_body = pitch_target
                        if data.dirty:
                            data.rotation_mat = math3d.matrix.make_rotation_y(data.yaw_body + data.yaw_offset)
                            if data.pitch_body_mode:
                                if data.use_pitch_limit:
                                    data.pitch_body = max(min(data.pitch_body, PITCH_MAX), PITCH_MIN)
                                data.rotation_mat = math3d.matrix.make_rotation_x(data.pitch_body) * data.rotation_mat
                            data.rotation = math3d.matrix_to_rotation(data.rotation_mat)
                            unit.sd.ref_appearance.model.rotation_matrix = data.rotation_mat
                elif data.dirty:
                    data.rotation_mat = math3d.rotation_to_matrix(data.rotation)
                    data.yaw_body = data.yaw_head
                    unit.sd.ref_appearance.model.rotation_matrix = data.rotation_mat
            except RuntimeError:
                unit.sd.ref_appearance.deactivate_ecs()
                exception_hook.traceback_uploader()

    def add_handler(self, handler_type, handler):
        self._data_to_handler[handler.unit_obj] = handler

    def remove_handler(self, handler_type, handler):
        del self._data_to_handler[handler.unit_obj]


class RotateSystemFullFps(RotateSystem):

    def __init__(self):
        super(RotateSystemFullFps, self).__init__(0)

    def ignored_type(self):
        return ()

    def interested_type(self):
        return (
         ComDataRenderRotate, ComDataAppearance, ComDataCamTarget)