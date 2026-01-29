# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/CommonMotorSystem.py
from __future__ import absolute_import
import cython_flag
from .SystemBase import SystemBase, FPS_30
from ..client.ComDataCommonMotor import ComDataCommonMotor
from ..client.ComDataLogicTransform import ComDataLogicTransform
from ..client.ComDataRenderRotate import ComDataRenderRotate
from ..client.ComDataCamTarget import ComDataCamTarget
import math3d
import math
PI2 = math.pi * 2

class CommonMotorSystem(SystemBase):

    def __init__(self, tick_step=FPS_30):
        super(CommonMotorSystem, self).__init__(tick_step)

    def interested_type(self):
        return (
         ComDataCommonMotor, ComDataLogicTransform, ComDataRenderRotate)

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
        for unit in self._element_list:
            data = unit.sd.ref_common_motor
            rotdata = data.sd.ref_rotatedata
            logicdata = data.sd.ref_logic_trans
            logicdata.yaw_target %= PI2
            rotdata.dirty = False
            if logicdata.force_turn_body != rotdata.force_turn_body:
                rotdata.force_turn_body = logicdata.force_turn_body
                rotdata.dirty = True
            if logicdata.yaw_offset != rotdata.yaw_offset:
                rotdata.yaw_offset = logicdata.yaw_offset
                rotdata.dirty = True
            if not logicdata.use_quaternion:
                rotdata.dirty = rotdata.dirty or rotdata.use_quaternion
                rotdata.use_quaternion = False
                if logicdata.yaw_target != rotdata.yaw_head:
                    if data.yaw_delta:
                        if dt > data.yaw_duration:
                            dt = data.yaw_duration
                        yaw_add = dt / data.yaw_duration * data.yaw_delta
                        data.yaw_duration -= dt
                        data.yaw_delta -= yaw_add
                        rotdata.yaw_head = (rotdata.yaw_head + yaw_add) % PI2
                        rotdata.dirty = True
                    else:
                        rotdata.yaw_head = logicdata.yaw_target
                        rotdata.dirty = True
                        data.yaw_duration = 0
                if logicdata.pitch_target != rotdata.pitch_head:
                    rotdata.pitch_head = logicdata.pitch_target
                    rotdata.dirty = True
            elif logicdata.quaternion != rotdata.rotation and logicdata.quaternion is not None:
                q = logicdata.quaternion
                rotdata.rotation.set(q.x, q.y, q.z, q.w)
                rotdata.yaw_head = logicdata.yaw_target
                rotdata.dirty = True
                rotdata.use_quaternion = True

        return


class CommonMotorSystemFullFps(CommonMotorSystem):

    def __init__(self):
        super(CommonMotorSystemFullFps, self).__init__(0)

    def ignored_type(self):
        return ()

    def interested_type(self):
        return (
         ComDataCommonMotor, ComDataLogicTransform, ComDataRenderRotate, ComDataCamTarget)