# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComPathMove.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const
from logic.gcommon.time_utility import time
import math3d
import math

class ComPathMove(UnitCom):
    BIND_EVENT = {'E_MOVE_PATH': '_set_move',
       'G_MOVE_PATH': '_get_move_path',
       'G_POSITION': '_get_position',
       'G_SPEED': '_get_speed',
       'G_DIRECTION': '_get_direction',
       'G_STOP_POSITION': '_get_stop_position',
       'G_REACH_DURATION': '_get_reach_duration'
       }

    def __init__(self):
        super(ComPathMove, self).__init__()
        self._start_point = None
        self._start_pos = None
        self._end_point = None
        self._cur_pos = None
        self._start_timestamp = None
        self._speed = 0
        self._acc = 0
        self._cur_speed = 0
        self._speed_vec = 0
        self._reach_dt = None
        self._direction = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPathMove, self).init_from_dict(unit_obj, bdict)
        self._start_timestamp = bdict.get('start_timestamp', None)
        self._start_point = bdict.get('start_point', None)
        self._end_point = bdict.get('end_point', None)
        self._speed = bdict.get('speed', 0)
        self._acc = bdict.get('acc', 0)
        return

    def on_init_complete(self):
        if self._start_timestamp is not None:
            self._set_move(self._start_timestamp, self._speed, self._acc, self._start_point, self._end_point)
        return

    def get_client_dict(self):
        return {'start_point': self._start_point,
           'end_point': self._end_point,
           'start_timestamp': self._start_timestamp,
           'speed': self._speed,
           'acc': self._acc
           }

    def destroy(self):
        if self.is_valid() and self.unit_obj.is_valid():
            self.send_event('E_PATH_DESTROY')
        super(ComPathMove, self).destroy()

    def _get_position(self):
        return self._cur_pos

    def _get_stop_position(self):
        return self._end_point

    def _get_speed(self):
        return self._cur_speed

    def _get_reach_duration(self):
        return self._reach_dt

    def _get_direction(self):
        return self._direction

    def _set_move(self, start_timestamp, speed, acc, start_point, end_point):
        self._start_timestamp = start_timestamp
        self._start_point = start_point
        self._end_point = end_point
        self._speed = speed
        self._acc = acc
        now = time()
        pass_time = now - start_timestamp
        end_pos = math3d.vector(*end_point)
        self._start_pos = math3d.vector(*start_point)
        direction = end_pos - self._start_pos
        if direction.is_zero:
            self._reach_dt = 0
        else:
            if acc == 0:
                flight_timestamp = direction.length / speed
            else:
                flight_timestamp = (math.sqrt(max(0, speed ** 2 + 2 * acc * direction.length)) - speed) / acc
            self._reach_dt = start_timestamp + flight_timestamp - now
            direction.normalize()
        if self._reach_dt <= 0:
            self._cur_speed = 0
        else:
            self._cur_speed = self._speed + acc * pass_time
        self.send_event('E_SPEED', self._cur_speed)
        self._direction = direction
        self.send_event('S_DIRECTION', direction)
        if self._reach_dt <= 0:
            self._speed_vec = math3d.vector(0, 0, 0)
            self._cur_pos = end_pos
            self.need_update = False
        else:
            self._speed_vec = direction * self._speed
            self._cur_pos = self._start_pos + self._speed_vec * pass_time + direction * acc * 0.5 * pass_time ** 2
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
            self._speed_vec = math3d.vector(0, 0, 0)
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
        if self._acc == 0:
            self._cur_pos = self._cur_pos + self._speed_vec * dt
        else:
            pass_time = time() - self._start_timestamp
            self._cur_speed = self._speed + self._acc * pass_time
            self.send_event('E_SPEED', self._cur_speed)
            pos = self._direction * (self._speed * pass_time + 0.5 * self._acc * pass_time ** 2)
            self._cur_pos = self._start_pos + pos
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(self._cur_pos)
        else:
            self.send_event('E_POSITION', self._cur_pos)

    def _get_move_path(self):
        return (
         self._start_point, self._end_point)