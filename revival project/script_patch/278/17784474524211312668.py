# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComParabolaMove.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const
from logic.gcommon.time_utility import time
import math3d
import math

class ComParabolaMove(UnitCom):
    BIND_EVENT = {'E_MOVE_PATH': '_set_move',
       'G_POSITION': '_get_position',
       'G_STOP_POSITION': '_get_stop_position',
       'G_REACH_DURATION': '_get_reach_duration'
       }

    def __init__(self):
        super(ComParabolaMove, self).__init__()
        self._start_point = None
        self._end_point = None
        self._start_timestamp = None
        self._fall_delay = 0
        self._h_speed = 0
        self._v_speed = 0
        self._v_acc = 0
        self._start_pos = None
        self._cur_pos = None
        self._reach_dt = None
        self._h_direction = None
        self._v_direction = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComParabolaMove, self).init_from_dict(unit_obj, bdict)
        self._start_timestamp = bdict.get('start_timestamp', None)
        self._start_point = bdict.get('start_point', None)
        self._end_point = bdict.get('end_point', None)
        self._fall_delay = bdict.get('fall_delay', 0)
        self._h_speed = bdict.get('h_speed', 0)
        self._v_speed = bdict.get('v_speed', 0)
        self._v_acc = bdict.get('v_acc', 0)
        return

    def on_init_complete(self):
        if self._start_timestamp is not None:
            self._set_move(self._start_timestamp, self._h_speed, self._v_speed, self._v_acc, self._start_point, self._end_point)
        return

    def get_client_dict(self):
        return {'start_timestamp': self._start_timestamp,
           'start_point': self._start_point,
           'end_point': self._end_point,
           'fall_delay': self._fall_delay,
           'h_speed': self._h_speed,
           'v_speed': self._v_speed,
           'v_acc': self._v_acc
           }

    def destroy(self):
        if self.is_valid() and self.unit_obj.is_valid():
            self.send_event('E_PATH_DESTROY')
        super(ComParabolaMove, self).destroy()

    def _get_position(self):
        return self._cur_pos

    def _get_stop_position(self):
        return self._end_point

    def _get_reach_duration(self):
        return self._reach_dt

    def _set_move(self, start_timestamp, h_speed, v_speed, v_acc, start_point, end_point):
        self._start_timestamp = start_timestamp
        self._start_point = start_point
        self._end_point = end_point
        self._h_speed = h_speed
        self._v_speed = v_speed
        self._v_acc = v_acc
        now = time()
        pass_time = now - start_timestamp
        fall_time = max(0, pass_time - self._fall_delay)
        end_pos = math3d.vector(*end_point)
        self._start_pos = math3d.vector(*start_point)
        direction = end_pos - self._start_pos
        if end_pos == self._start_pos:
            self._h_direction = math3d.vector(0, 0, 0)
            self._v_direction = math3d.vector(0, 0, 0)
            self._reach_dt = 0
        else:
            self._h_direction = math3d.vector(end_pos.x - self._start_pos.x, 0, end_pos.z - self._start_pos.z)
            self._v_direction = math3d.vector(0, end_pos.y - self._start_pos.y, 0)
            duration = self._h_direction.length / h_speed
            self._reach_dt = start_timestamp + duration - now
            self._h_direction.normalize()
            self._v_direction.normalize()
        if self._reach_dt <= 0:
            self._cur_pos = end_pos
            self.need_update = False
        else:
            h_vec = self._h_direction * self._h_speed * pass_time
            v_vec = self._v_direction * (self._v_speed * fall_time + self._v_acc * 0.5 * fall_time ** 2)
            self._cur_pos = self._start_pos + h_vec + v_vec
            self.need_update = True
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(self._cur_pos)
        else:
            self.send_event('E_POSITION', self._cur_pos)

    def tick(self, dt):
        if not self.is_valid():
            return
        self._reach_dt -= dt
        if self._reach_dt <= 0:
            self._cur_speed = 0
            self._cur_pos = math3d.vector(*self._end_point)
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(self._cur_pos)
            else:
                self.send_event('E_POSITION', self._cur_pos)
            ret = self.ev_g_reach_destination(self._cur_pos)
            if ret is True:
                self.destroy_from_unit()
            elif ret is False:
                self.need_update = False
            return
        pass_time = time() - self._start_timestamp
        fall_time = max(0, pass_time - self._fall_delay)
        h_vec = self._h_direction * self._h_speed * pass_time
        v_vec = self._v_direction * (self._v_speed * fall_time + self._v_acc * 0.5 * fall_time ** 2)
        self._cur_pos = self._start_pos + h_vec + v_vec
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(self._cur_pos)
        else:
            self.send_event('E_POSITION', self._cur_pos)