# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/SimBoxPosRot.py
from __future__ import absolute_import
import math3d

class SimBoxPosRot(object):

    def __init__(self):
        super(SimBoxPosRot, self).__init__()
        self.lin_t = 0
        self.lin_pos = math3d.vector(0, 0, 0)
        self.lin_acc = math3d.vector(0, 0, 0)
        self.lin_vel = math3d.vector(0, 0, 0)
        self.agl_t = 0
        self.agl_v3d = math3d.vector(0, 0, 0)
        self.agl_acc = math3d.vector(0, 0, 0)
        self.agl_vel = math3d.vector(0, 0, 0)
        self.sim_pos = math3d.vector(0, 0, 0)
        self.sim_agl = math3d.vector(0, 0, 0)

    def set_lin_t(self, t):
        self.lin_t = t

    def set_pos(self, t, lin_pos):
        self.lin_t = t
        self.lin_pos = lin_pos

    def set_lin_vel(self, t, lin_vel):
        self.lin_t = t
        self.lin_vel = lin_vel

    def set_lin_all(self, t, lin_pos, lin_vel, lin_acc):
        self.lin_t = t
        self.lin_pos = lin_pos
        self.lin_acc = lin_acc
        self.lin_vel = lin_vel
        self.sim_pos = lin_pos

    def set_agl_t(self, t):
        self.agl_t = t

    def set_agl(self, t, agl_v3d):
        self.agl_t = t
        self.agl_v3d = agl_v3d

    def set_agl_vel(self, t, agl_vel):
        self.agl_t = t
        self.agl_vel = agl_vel

    def set_agl_all(self, t, agl_v3d, agl_vel, agl_acc):
        self.agl_t = t
        self.agl_v3d = agl_v3d
        self.agl_acc = agl_acc
        self.agl_vel = agl_vel
        self.sim_agl = agl_v3d

    def get_sim_pos(self, t):
        dt = t - self.lin_t
        _sim_pos = self.lin_pos + self.lin_vel * dt + self.lin_acc * 0.5 * dt ** 2
        return _sim_pos

    def get_sim_agl(self, t):
        dt = t - self.agl_t
        _sim_agl = self.agl_v3d + self.agl_vel * dt + self.agl_acc * 0.5 * dt ** 2
        return _sim_agl