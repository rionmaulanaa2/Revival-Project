# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncRotItpler.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import time as org_time
import logic.gcommon.time_utility as time
import math3d
import math
from logic.gcommon.common_utils.math3d_utils import normal_tp_to_v3d as tp_to_v3d
V3D_ZERO = math3d.vector(0, 0, 0)
MAX_SEC_ITPL = 5

class ComMoveSyncRotItpler(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_RC_AGL': '_on_sync_agl',
       'E_ACTION_SYNC_RC_STOP_EULER_ITPL': 'stop_itpl'
       }

    def __init__(self):
        super(ComMoveSyncRotItpler, self).__init__(need_update=False)
        now = time.time()
        self.start_time = now
        self.end_time = now
        self._agl_t = 0
        self._agl_v3d = None
        self._agl_vel = V3D_ZERO
        self._agl_acc = V3D_ZERO
        self._itpl_agl = V3D_ZERO
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncRotItpler, self).init_from_dict(unit_obj, bdict)

    def _on_sync_agl(self, t, agl_v3d, agl_vel, agl_acc):
        self._agl_t = t
        self._agl_v3d = tp_to_v3d(agl_v3d)
        self._agl_vel = tp_to_v3d(agl_vel)
        self._agl_acc = tp_to_v3d(agl_acc)
        m = self.ev_g_model()
        if m:
            self.need_update = True
        self.end_time = t + 1.0

    def fix_2_pi(self, new_euler, old_euler):
        diff = new_euler - old_euler
        x_df = diff.x / abs(diff.x) * math.pi if abs(diff.x) > math.pi else 0
        y_df = diff.y / abs(diff.y) * math.pi if abs(diff.y) > math.pi else 0
        z_df = diff.z / abs(diff.z) * math.pi if abs(diff.z) > math.pi else 0
        v3d_diff = math3d.vector(x_df, y_df, z_df) * 2
        old_euler += v3d_diff
        return (
         new_euler, old_euler)

    def noti_change(self, euler3):
        self.send_event('E_ACTION_SYNC_IT_EULER', euler3)
        self.send_event('E_ROTATION', math3d.euler_to_rotation(euler3))

    def start_itpl(self):
        self.need_update = True

    def stop_itpl(self):
        self.need_update = False

    def tick(self, dt):
        now = time.time()
        if now - self.end_time > MAX_SEC_ITPL:
            self.need_update = False
            return
        self.itpl_lin_agl(dt)

    def itpl_lin_agl(self, dt):
        now = time.time() + 0.1
        m = self.ev_g_model()
        if self._agl_t != 0 and now - self._agl_t < MAX_SEC_ITPL:
            dt = now - self._agl_t
            _sim_agl = self._agl_v3d + self._agl_vel * dt
            mat_rot = m.rotation_matrix
            elr = math3d.rotation_to_euler(math3d.matrix_to_rotation(mat_rot))
            elr, _sim_agl = self.fix_2_pi(elr, _sim_agl)
            v3d = math3d.vector(0, 0, 0)
            v3d.intrp(elr, _sim_agl, 0.25)
            mat_rot = math3d.rotation_to_matrix(math3d.euler_to_rotation(v3d))
            m.rotation_matrix = mat_rot