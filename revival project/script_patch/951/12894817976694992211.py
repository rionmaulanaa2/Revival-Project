# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncEulerItpler.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import math3d
import math
ITPL_FRAME = 10
SL_TLRC = 0.01

class ComMoveSyncEulerItpler(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_RC_EULER': '_on_sync_euler',
       'E_ACTION_SYNC_RC_STOP_EULER_ITPL': 'stop_itpl'
       }

    def __init__(self):
        super(ComMoveSyncEulerItpler, self).__init__(need_update=False)
        self._cur_rot = None
        self._to_rot = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncEulerItpler, self).init_from_dict(unit_obj, bdict)

    def _on_sync_euler(self, yaw, pitch, roll):
        euler3 = math3d.vector(yaw, pitch, roll)
        rot = math3d.euler_to_rotation(euler3)
        if not self._cur_rot:
            self._cur_rot = rot
            self._to_rot = rot
            self.noti_rot(rot)
            return
        self._to_rot = rot
        self.start_itpl()

    def noti_rot(self, rot):
        self.send_event('E_ROTATION', rot)

    def start_itpl(self):
        self.need_update = True

    def stop_itpl(self):
        self.need_update = False
        if not self._cur_rot:
            return
        else:
            self.noti_rot(self._to_rot)
            self._to_rot = None
            self._cur_rot = None
            return

    def tick(self, dt):
        self.update_rot(dt)

    def update_rot(self, dt):
        self._cur_rot.slerp(self._cur_rot, self._to_rot, 0.2, True)
        self.noti_rot(self._cur_rot)
        delta = self._to_rot - self._cur_rot
        if abs(delta.x) < SL_TLRC and abs(delta.y) < SL_TLRC and abs(delta.z) < SL_TLRC and abs(delta.w) < SL_TLRC:
            self.stop_itpl()