# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/AimIkSystem.py
from __future__ import absolute_import
from .SystemBase import SystemBase
from ..client.ComDataAimIK import ComDataAimIK
import world
import math3d
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
PI2 = math.pi * 2
TO_DEGREES_FACTOR = 180 / math.pi
FORWARD_SCALE = NEOX_UNIT_SCALE * 200

class AimIkSystem(SystemBase):

    def __init__(self):
        super(AimIkSystem, self).__init__(0)
        self._leaving_list = []
        self._support_blend_rate = hasattr(world.aimik, 'set_aim_blend_rate')

    def interested_type(self):
        return (
         ComDataAimIK,)

    def handler_types(self):
        return []

    def add_handler(self, handler_type, handler):
        raise NotImplementedError()

    def remove_handler(self, handler_type, handler):
        raise NotImplementedError()

    def _get_forward(self, data, camera):
        rot_mat = camera.rotation_matrix
        forward = rot_mat.forward
        if forward.pitch * TO_DEGREES_FACTOR > data.pitch_limit:
            y = -math.tan(math.radians(data.pitch_limit)) * math.sqrt(forward.x ** 2 + forward.z ** 2)
            forward = math3d.vector(forward.x, y, forward.z)
            forward.normalize()
        if data.need_modify_forward:
            forward = forward + rot_mat.right * -0.2 + rot_mat.up * -0.1
            forward.normalize()
        return forward

    def _update_blend_value(self, data, dt):
        if not data.exit_lerp:
            data.lerp_time += dt
            if data.lerp_time >= data.lerp_thresh or data.lerp_thresh <= 0:
                data.is_blending = False
                rate = 1
            else:
                rate = data.lerp_time / data.lerp_thresh
            data.cur_blend_rate = rate * data.max_blend_rate
        else:
            data.exit_lerp_time += dt
            if data.exit_lerp_time >= data.exit_lerp_thresh or data.exit_lerp_thresh <= 0:
                data.is_blending = False
                rate = 0
                self._leaving_list.append(data)
            else:
                rate = 1 - data.exit_lerp_time / data.exit_lerp_thresh
            data.cur_blend_rate = rate * data.exit_blend_rate

    def tick(self, dt):
        for unit in self._element_list:
            data = unit.sd.ref_aimik
            if unit.sd.ref_rotatedata.dirty or data.is_blending or data.force_update_this_frame:
                camera = world.get_active_scene().active_camera
                forward = self._get_forward(data, camera)
                end_pos = camera.position + forward * FORWARD_SCALE
                if data.is_blending:
                    self._update_blend_value(data, dt)
                if self._support_blend_rate:
                    data.aim_ik_solver.set_aim_target(end_pos)
                    data.aim_ik_solver.set_aim_blend_rate(data.cur_blend_rate)
                else:
                    data.aim_ik_solver.set_aim_target(end_pos)
                data.force_update_this_frame = False

        while self._leaving_list:
            data = self._leaving_list.pop()
            data.deactivate_ecs()