# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/SimulateBox.py
from __future__ import absolute_import
import math3d

class SimulateBox(object):

    def __init__(self):
        super(SimulateBox, self).__init__()
        self.t = 0
        self.pos = math3d.vector(0, 0, 0)
        self.acc = math3d.vector(0, 0, 0)
        self.vel = math3d.vector(0, 0, 0)

    def set_t(self, t):
        self.t = t

    def set_pos(self, t, pos):
        self.t = t
        self.pos = pos

    def set_vel(self, t, vel):
        self.t = t
        self.vel = vel

    def set_all(self, t, pos, vel, acc):
        self.t = t
        self.pos = pos
        self.acc = acc
        self.vel = vel
        self.sim_pos = pos

    def get_sim_pos(self, t):
        dt = t - self.t
        _sim_pos = self.pos + self.vel * dt + self.acc * 0.5 * dt ** 2
        return _sim_pos