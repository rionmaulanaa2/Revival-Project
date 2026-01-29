# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataLogicMovementRel.py
from __future__ import absolute_import
import cython_flag
from logic.gcommon.component.share.ComDataBase import ComDataBase
from math3d import vector
from logic.gcommon.common_const import sync_const
from logic.gcommon import time_utility as tutil

class ComDataLogicMovementRel(ComDataBase):
    BIND_EVENT = {'E_SYNC_RTT': 'refresh_rtt'
       }

    def __init__(self):
        super(ComDataLogicMovementRel, self).__init__()
        self.rtt = 0.1
        self.sim_t = 0
        self.buffer = []
        self.buffer_max_t = 0
        self.max_predict_t = 0
        self.src_t = tutil.time()
        self.src_pos = None
        self.last_pos = None
        self.cur_pos = None
        self.sim_pos = None
        self.src_eid = None
        self.last_eid = None
        self.cur_eid = None
        self.cur_vel = vector(0, 0, 0)
        self.max_overdue_frames = 20
        self.overdue_frames = self.max_overdue_frames
        self.sim_eid = None
        self.dirty = False
        self.itpl_stop = True
        self.real_pos_cache = None
        self.disable = True
        return

    def is_buffer_clear(self):
        if self.buffer:
            return True
        return False

    def get_share_data_name(self):
        return 'ref_rel_logic_movement'

    def init_from_dict(self, unit_obj, bdict):
        super(ComDataLogicMovementRel, self).init_from_dict(unit_obj, bdict)
        rel_info = bdict.get('rel_info', {})
        pos = rel_info.get('rel_pos', vector(0, 0, 0))
        self.src_pos = vector(pos)
        self.last_pos = vector(pos)
        self.cur_pos = vector(pos)
        self.sim_pos = vector(pos)
        rel_eid = rel_info.get('rel_eid', None)
        self.src_eid = rel_eid
        self.last_eid = rel_eid
        self.cur_eid = rel_eid
        if rel_eid:
            self.disable = False
        self.rtt = bdict.get('rtt') or 0.1
        return

    def refresh_rtt(self, rtt):
        pass

    def add_state(self, t, ent_id, pos, vel):
        if pos:
            pre_disable = self.disable
            self.disable = False
            self.buffer.append((t, ent_id, pos, vel))
            if len(self.buffer) > 50 or pre_disable:
                vel = vector(0, 0, 0)
                self.clear_buffer(t, ent_id, pos, vel)
                return
            self.buffer_max_t = t
            self.max_predict_t = t
        else:
            self.disable = True

    def clear_buffer(self, t, ent_id, pos, vel):
        self.buffer = []
        self.src_t = t
        self.src_pos = vector(pos)
        self.last_pos = vector(pos)
        self.cur_pos = vector(pos)
        self.sim_pos = vector(pos)
        self.src_eid = ent_id
        self.last_eid = ent_id
        self.cur_eid = ent_id
        self.sim_eid = ent_id
        self.cur_vel = vel
        self.buffer_max_t = t
        self.max_predict_t = t
        self.itpl_stop = True

    def get_real_pos(self):
        if not global_data.battle:
            return None
        else:
            rel_ent = global_data.battle.get_entity(self.cur_eid)
            if not rel_ent or not rel_ent.logic:
                return None
            par_trans = rel_ent.logic.ev_g_trans()
            return global_data.carry_mgr.relative_to_world(self.cur_pos, par_trans)