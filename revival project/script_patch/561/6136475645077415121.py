# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPathMoveNotify.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const
from logic.gcommon.time_utility import time
import math3d
import math

class ComPathMoveNotify(UnitCom):
    BIND_EVENT = {'E_MOVE_PATH': ('_set_move', 10)
       }

    def __init__(self):
        super(ComPathMoveNotify, self).__init__()
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
        super(ComPathMoveNotify, self).init_from_dict(unit_obj, bdict)
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

    def _set_move(self, start_timestamp, speed, acc, start_point, end_point):
        from logic.gcommon.const import AIRLINE_AIRSHIP
        global_data.emgr.scene_add_airline_event.emit(self.unit_obj.id, AIRLINE_AIRSHIP, math3d.vector(*start_point), math3d.vector(*end_point))

    def destroy(self):
        global_data.emgr.scene_del_airline_event.emit(self.unit_obj.id)
        super(ComPathMoveNotify, self).destroy()