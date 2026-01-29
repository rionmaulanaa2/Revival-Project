# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataLogicMovement.py
from __future__ import absolute_import
import cython_flag
from logic.gcommon.component.share.ComDataBase import ComDataBase
from math3d import vector
from logic.gcommon.common_const import sync_const
from logic.gcommon import time_utility as tutil

class ComDataLogicMovement(ComDataBase):
    BIND_EVENT = {'E_SYNC_RTT': 'refresh_rtt'
       }

    def __init__(self):
        super(ComDataLogicMovement, self).__init__()
        self.rtt = 0.1
        self.sim_t = 0
        self.buffer = []
        self.buffer_max_t = 0
        self.max_predict_t = 0
        self.src_t = tutil.time()
        self.src_pos = None
        self.last_pos = None
        self.cur_pos = None
        self.cur_vel = vector(0, 0, 0)
        self.cur_acc = vector(0, 0, 0)
        self.sim_pos = None
        self.dirty = False
        self.itpl_stop = True
        return

    def get_share_data_name(self):
        return 'ref_logic_movement'

    def init_from_dict(self, unit_obj, bdict):
        super(ComDataLogicMovement, self).init_from_dict(unit_obj, bdict)
        pos = bdict.get('position') or vector(0, 0, 0)
        self.src_pos = vector(pos)
        self.last_pos = vector(pos)
        self.cur_pos = vector(pos)
        self.sim_pos = vector(pos)
        self.rtt = bdict.get('rtt') or 0.1

    def refresh_rtt(self, rtt):
        pass

    def add_state(self, t, pos, vel, acc):
        t = max(t, self.buffer_max_t)
        self.buffer.append((t, pos, vel, acc))
        if len(self.buffer) > 50:
            self.clear_buffer(t, pos, vel, acc)
            return
        self.buffer_max_t = t
        self.max_predict_t = t + sync_const.MAX_ITVL_SILENT

    def clear_buffer(self, t, pos, vel, acc):
        self.buffer = []
        self.src_t = t
        self.src_pos = vector(pos)
        self.last_pos = vector(pos)
        self.cur_pos = vector(pos)
        self.cur_vel = vector(vel)
        self.cur_acc = vector(acc)
        self.sim_pos = vector(pos)
        self.buffer_max_t = t
        self.max_predict_t = t + sync_const.MAX_ITVL_SILENT
        self.itpl_stop = True