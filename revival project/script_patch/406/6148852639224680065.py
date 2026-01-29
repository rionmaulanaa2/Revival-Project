# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPathPeriodicMove.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.time_utility import time
import math3d
import math

class ComPathPeriodicMove(UnitCom):
    BIND_EVENT = {'E_MACHINE_MOVING': ('_machine_moving', 10)
       }

    def __init__(self):
        super(ComPathPeriodicMove, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPathPeriodicMove, self).init_from_dict(unit_obj, bdict)
        is_dynamic = bdict.get('is_dynamic', False)
        if not is_dynamic:
            return
        else:
            self.cur_position = math3d.vector(*bdict.get('cur_pos'))
            self.target_position = None
            cur_start = math3d.vector(*bdict.get('cur_start'))
            cur_dest = math3d.vector(*bdict.get('cur_dest'))
            cur_period = bdict.get('cur_period')
            cur_start_time = bdict.get('cur_start_time')
            len_this = (cur_dest - cur_start).length
            len_to = (cur_dest - self.cur_position).length
            t_to = len_this and len_to / len_this * cur_period
            self.send_event('E_MACHINE_MOVING', cur_dest, cur_start_time, t_to, 0)
            return

    def _machine_moving(self, v3d_pos_dest, t_start, t_moving, move_index):
        pass