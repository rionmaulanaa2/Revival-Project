# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComOrientationSyncSender.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import math3d
import world
from logic.gutils.sync.TriggerBox import TriggerBox
from logic.gutils.sync.TriggerBoxCam import TriggerBoxCam

class ComOrientationSyncSender(UnitCom):
    BIND_EVENT = {'E_SYNC_YAW': 'on_yaw_changed',
       'E_SYNC_PITCH': 'on_pitch_changed'
       }

    def __init__(self):
        super(ComOrientationSyncSender, self).__init__(need_update=True)
        self._box_yaw = TriggerBoxCam(min_itvl=0.1, min_delta=0.1, max_stay=0.5)
        self._box_yaw.set_callback(self.on_trigger_yaw)
        self._box_pitch = TriggerBox(min_itvl=0.2, min_delta=0.2, max_stay=0.5)
        self._box_pitch.set_callback(self.on_trigger_pitch)

    def destroy(self):
        self._box_yaw.destroy()
        self._box_pitch.destroy()
        super(ComOrientationSyncSender, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComOrientationSyncSender, self).init_from_dict(unit_obj, bdict)

    def on_yaw_changed(self, f_yaw):
        f_yaw = self.ev_g_yaw()
        self._box_yaw.input(t_util.time(), f_yaw)

    def on_trigger_yaw(self, f_dt, f_yaw):
        self.send_event('E_CALL_SYNC_METHOD', 'sync_yaw', (f_yaw, f_dt))

    def on_pitch_changed(self, f_head_pitch):
        f_head_pitch = self.ev_g_cam_pitch() or 0
        self._box_pitch.input(t_util.time(), f_head_pitch)

    def on_trigger_pitch(self, f_dt, f_head_pitch):
        self.send_event('E_CALL_SYNC_METHOD', 'sync_pitch', (f_head_pitch, f_dt))

    def tick(self, dt):
        now = t_util.time()
        self._box_yaw.check_trigger(now)
        self._box_pitch.check_trigger(now)