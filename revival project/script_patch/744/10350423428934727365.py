# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComOrientationSyncReceiver.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import math3d
from math import pi
pi2 = pi * 2

class ComOrientationSyncReceiver(UnitCom):
    BIND_EVENT = {'E_SYNC_YAW': 'on_sync_yaw',
       'E_SYNC_PITCH': 'on_sync_pitch'
       }

    def __init__(self):
        super(ComOrientationSyncReceiver, self).__init__()
        self.need_interpolate = True
        self._to_yaw = 0
        self._yaw = 0
        self._to_pitch = 0
        self._pitch = 0

    def destroy(self):
        super(ComOrientationSyncReceiver, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComOrientationSyncReceiver, self).init_from_dict(unit_obj, bdict)

    def on_sync_yaw(self, yaw, dt=0):
        self._to_yaw = yaw
        self._yaw = self.ev_g_yaw()
        d_yaw = (yaw - self._yaw + pi) % pi2 - pi
        self.send_event('E_CLIENT_INTER_PUT', 'it_yaw', d_yaw, 0.1, self.on_yaw_changed)

    def on_yaw_changed(self, d_yaw):
        self._yaw += d_yaw
        self.send_event('E_CAM_YAW', self._yaw)
        cam_logic = global_data.cam_lplayer
        if cam_logic and cam_logic.id == self.sd.ref_driver_id:
            global_data.emgr.sync_cam_yaw_with_role.emit(self._yaw)

    def on_sync_pitch(self, pitch, dt=0):
        self._to_pitch = pitch
        self._pitch = self.ev_g_cam_pitch()
        d_pitch = (pitch - self._pitch + pi) % pi2 - pi
        self.send_event('E_CLIENT_INTER_PUT', 'it_pitch', d_pitch, 0.1, self.on_pitch_changed)

    def on_pitch_changed(self, d_pitch):
        self._pitch += d_pitch
        self.send_event('E_CAM_PITCH', self._pitch)
        cam_logic = global_data.cam_lplayer
        if cam_logic and cam_logic.id == self.sd.ref_driver_id:
            global_data.emgr.sync_cam_pitch_with_role.emit(self._pitch)

    def tick(self, dt):
        pass