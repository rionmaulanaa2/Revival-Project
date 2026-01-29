# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataCommonMotor.py
from __future__ import absolute_import
import cython_flag
from ..share.ComDataBase import ComDataBase
import math
PI = math.pi
PI2 = PI + PI

class ComDataCommonMotor(ComDataBase):

    def __init__(self):
        super(ComDataCommonMotor, self).__init__()
        self.yaw_duration = 0
        self.yaw_delta = 0

    def get_share_data_name(self):
        return 'ref_common_motor'

    def set_yaw_time(self, dt):
        if self.yaw_duration != -1:
            self.yaw_duration = dt
        if self.yaw_duration == -1 or self.yaw_duration == 0:
            self.yaw_delta = 0
        else:
            logic_trans = self.sd.ref_logic_trans
            rotate_data = self.sd.ref_rotatedata
            dt_yaw = (logic_trans.yaw_target - rotate_data.yaw_head) % PI2
            self.yaw_delta = dt_yaw if dt_yaw < PI else dt_yaw - PI2