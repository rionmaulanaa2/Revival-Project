# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/TriggerPosRot.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gutils.sync.SimBoxPosRot import SimBoxPosRot
import math3d
import time
V3D_ZERO = math3d.vector(0, 0, 0)

def default_callback(*args, **argv):
    print('[TriggerPosRot] --- default_callback', args, argv)


class TriggerPosRot(object):
    TIME_PREDICT = 1.0
    POS_LENGTH_TRI = 20.0

    def __init__(self):
        super(TriggerPosRot, self).__init__()
        self._sim_real = SimBoxPosRot()
        self._sim_ghost = SimBoxPosRot()
        self._lin_cmp_dis = 20.0
        self._lin_t = 0
        self._lin_pos = None
        self._lin_vel = V3D_ZERO
        self._lin_acc = V3D_ZERO
        self._lin_stop = True
        self._last_tri_lin = None
        self._agl_t = 0
        self._agl_v3d = V3D_ZERO
        self._agl_vel = V3D_ZERO
        self._agl_acc = V3D_ZERO
        self._agl_stop = True
        self._last_tri_agl = None
        self.handle = {'lin': default_callback,
           'agl': default_callback
           }
        self.input_handle = {'lin': self.input_lin,
           'agl': self.input_agl
           }
        self._tri_t_lin = 0
        self._tri_t_agl = 0
        return

    def set_callback(self, key, cb):
        self.handle[key] = cb

    def input_lin(self, t, lin_pos, lin_vel, lin_acc):
        self._lin_t = t
        self._lin_pos = lin_pos
        self._lin_vel = lin_vel
        self._lin_acc = lin_acc
        self._sim_real.set_lin_all(t, lin_pos, lin_vel, lin_acc)
        if self._lin_vel.is_zero and self._lin_acc.is_zero:
            if not self._lin_stop:
                self.do_tri_lin(t)
            self._lin_stop = True
        else:
            self._lin_stop = False

    def input_agl(self, t, agl_v3d, agl_vel, agl_acc):
        self._agl_t = t
        self._agl_v3d = agl_v3d
        self._agl_vel = agl_vel
        self._agl_acc = agl_acc
        self._sim_real.set_agl_all(t, agl_v3d, agl_vel, agl_acc)
        if self._agl_vel.is_zero and self._agl_acc.is_zero:
            if not self._agl_stop:
                self.do_tri_agl(t)
            self._agl_stop = True
        else:
            self._agl_stop = False

    def tick(self, dt):
        now = time.time()
        self.check_trigger_lin(now)
        self.check_trigger_agl(now)
        self.do_sum()

    def check_trigger_lin(self, t):
        if not self._lin_pos:
            return
        _pred_real = self._sim_real.get_sim_pos(t + self.TIME_PREDICT)
        _pred_sim = self._sim_ghost.get_sim_pos(t + self.TIME_PREDICT)
        if not self._cmp_lin(t, _pred_real, _pred_sim) or t - self._tri_t_lin > self.TIME_PREDICT:
            self.do_tri_lin(t)

    def do_tri_lin(self, t):
        if self._last_tri_lin:
            _last = self._last_tri_lin
            if _last[1] == self._lin_pos and _last[2] == self._lin_vel and _last[3] == self._lin_acc:
                return
        self.handle['lin'](self._lin_t, self._lin_pos, self._lin_vel, self._lin_acc)
        self.refresh_lin()
        self._tri_t_lin = t
        self._last_tri_lin = (
         self._lin_t, self._lin_pos, self._lin_vel, self._lin_acc)

    def _cmp_lin(self, t, a, b):
        if not b:
            return False
        if (a - b).length > self._lin_cmp_dis and (t - self._tri_t_lin > 0.1 or (a - b).length > 100.0):
            return False
        return True

    def refresh_lin(self):
        self._sim_ghost.set_lin_all(self._lin_t, self._lin_pos, self._lin_vel, self._lin_acc)

    def check_trigger_agl(self, t):
        _pred_agl_real = self._sim_real.get_sim_agl(t + self.TIME_PREDICT)
        _pred_agl_sim = self._sim_ghost.get_sim_agl(t + self.TIME_PREDICT)
        if not self._cmp_agl(t, _pred_agl_real, _pred_agl_sim) or t - self._tri_t_agl > self.TIME_PREDICT:
            self.do_tri_agl(t)

    def do_tri_agl(self, t):
        if self._last_tri_agl:
            _last = self._last_tri_agl
            if _last[1] == self._agl_v3d and _last[2] == self._agl_vel and _last[3] == self._agl_acc:
                return
        self.handle['agl'](self._agl_t, self._agl_v3d, self._agl_vel, self._agl_acc)
        self.refresh_agl()
        self._tri_t_agl = t
        self._last_tri_agl = (
         self._agl_t, self._agl_v3d, self._agl_vel, self._agl_acc)

    def _cmp_agl(self, t, a, b):
        delta_t = t - self._tri_t_agl
        if not b:
            return False
        if delta_t > self.TIME_PREDICT:
            return True
        if delta_t > 0.2 or (a - b).length > 2.0:
            return False
        return True

    def refresh_agl(self):
        self._sim_ghost.set_agl_all(self._agl_t, self._agl_v3d, self._agl_vel, self._agl_acc)

    def do_sum(self):
        pass

    def set_lin_cmp_dis(self, dis):
        dis = min(100.0, max(8.0, dis))
        self._lin_cmp_dis = dis