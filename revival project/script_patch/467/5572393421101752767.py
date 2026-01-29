# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/CameraSystem.py
from __future__ import absolute_import
from .SystemBase import SystemBase
from ..client.ComDataCamTarget import ComDataCamTarget
from ..client.ComDataRenderRotate import ComDataRenderRotate
from ..client.ComDataNotAffectCamSystem import ComDataNotAffectCamSystem
import math3d
import math
from common.const.common_const import FORCE_DELTA_TIME
TO_DEGREES_FACTOR = 180 / math.pi

class CameraSystem(SystemBase):

    def __init__(self):
        super(CameraSystem, self).__init__(0)

    def interested_type(self):
        return (
         ComDataCamTarget, ComDataRenderRotate)

    def ignored_type(self):
        return (
         ComDataNotAffectCamSystem,)

    def handler_types(self):
        return []

    def add_handler(self, handler_type, handler):
        raise NotImplementedError()

    def remove_handler(self, handler_type, handler):
        raise NotImplementedError()

    def tick(self, dt):
        for unit_obj in self._element_list:
            data = unit_obj.sd.ref_cam_target
            rotdata = unit_obj.sd.ref_rotatedata
            if rotdata.yaw_head != data.cam_target_yaw:
                data.cam_target_yaw = rotdata.yaw_head
                global_data.emgr.sync_cam_yaw_with_role.emit(rotdata.yaw_head)