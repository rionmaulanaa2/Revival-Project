# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/TriggerRot.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gutils.sync.SimBoxPosRot import SimBoxPosRot
import math3d
import time
V3D_ZERO = math3d.vector(0, 0, 0)

def default_callback(*args, **argv):
    print('[TriggerRot] --- default_callback', args, argv)


class TriggerRot(object):
    TIME_PREDICT = 1.0

    def __init__(self):
        super(TriggerRot, self).__init__()
        self._sim_real = SimBoxPosRot()
        self._sim_ghost = SimBoxPosRot()
        self._agl_t = 0
        self._agl_v3d = None
        self._agl_vel = V3D_ZERO
        self._agl_acc = V3D_ZERO
        self._agl_stop = True
        self._last_tri_agl = None
        self.handle = {'agl': default_callback
           }
        self.input_handle = {'agl': self.input_agl
           }
        self._tri_t_agl = 0
        return

    def set_callback(self, key, cb):
        self.handle[key] = cb

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
        self.check_trigger_agl(now)

    def check_trigger_agl(self, t):
        if not self._agl_v3d:
            return
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