# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/AnimatorSystem.py
from __future__ import absolute_import
from .SystemBase import SystemBase, FPS_30
from ..client.ComDataAnimator import ComDataAnimator
from ..client.ComDataRenderRotate import ComDataRenderRotate
from ..client.ComDataCamTarget import ComDataCamTarget
import math3d
import math
from common.const.common_const import FORCE_DELTA_TIME
import exception_hook
TO_DEGREES_FACTOR = 180 / math.pi

class AnimatorSystem(SystemBase):

    def __init__(self, tick_step=FPS_30):
        super(AnimatorSystem, self).__init__(tick_step)

    def interested_type(self):
        return (
         ComDataAnimator, ComDataRenderRotate)

    def ignored_type(self):
        return (
         ComDataCamTarget,)

    def handler_types(self):
        return []

    def add_handler(self, handler_type, handler):
        raise NotImplementedError()

    def remove_handler(self, handler_type, handler):
        raise NotImplementedError()

    def tick(self, dt):
        for unit_obj in self._element_list:
            try:
                data = unit_obj.sd.ref_animator_data
                rotdata = data.sd.ref_rotatedata
                if rotdata.yaw_head - rotdata.yaw_body != data.yaw_head_local:
                    data.yaw_head_local = rotdata.yaw_head - rotdata.yaw_body
                    yaw_val = data.yaw_head_local * TO_DEGREES_FACTOR
                    _y_twist_node = data.y_twist_node
                    if yaw_val > 180:
                        yaw_val -= 360
                    elif yaw_val < -180:
                        yaw_val += 360
                    if data.left_max_yaw_angle < yaw_val < data.right_max_yaw_angle:
                        twist_angle = yaw_val + data.yaw_head_offset
                        if data.yaw_mirrored:
                            twist_angle = -twist_angle
                        _y_twist_node.twistAngle = twist_angle
            except RuntimeError:
                unit_obj.sd.ref_animator_data.deactivate_ecs()
                exception_hook.traceback_uploader()


class AnimatorSystemFullFps(AnimatorSystem):

    def __init__(self):
        super(AnimatorSystemFullFps, self).__init__(0)

    def ignored_type(self):
        return ()

    def interested_type(self):
        return super(AnimatorSystemFullFps, self).interested_type() + (ComDataCamTarget,)