# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComInterpolater.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom

class InterData(object):

    def __init__(self):
        self.delta = 0
        self.leave_time = 0
        self.callback = None
        self.time_out = False
        return

    def do_tick(self, dt):
        val = dt / self.leave_time * self.delta
        if abs(self.delta) > abs(val):
            self.delta -= val
        else:
            val = self.delta
            self.delta = 0
        self.leave_time -= dt
        if self.callback:
            self.time_out = self.callback(val)
        if self.leave_time <= 0.001 or abs(self.delta) <= 0.0001:
            self.time_out = True
            self.callback(self.delta)

    def put(self, delta, leave_time, callback):
        if leave_time <= 0:
            return
        self.delta = delta
        self.leave_time = leave_time
        self.callback = callback
        self.time_out = False


class ComInterpolater(UnitCom):
    INTER_LINEAR = 1
    BIND_EVENT = {'E_CLIENT_INTER_PUT': '_put_inter',
       'E_CLIENT_INTER_DEL': '_remove_inter'
       }

    def __init__(self):
        super(ComInterpolater, self).__init__()
        self._mp_inters = {}
        self.del_arr = []
        self._start_update_time = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComInterpolater, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        self.need_update = False
        self._mp_inters = {}
        super(ComInterpolater, self).destroy()

    def _put_inter(self, key, delta, leave_time, callback=None):
        if not callback or leave_time <= 0:
            return
        if key not in self._mp_inters:
            it_data = InterData()
        else:
            it_data = self._mp_inters[key]
        it_data.put(delta, max(leave_time, 0.1), callback)
        self._mp_inters[key] = it_data
        if not self._need_update:
            self.need_update = True
        self._start_update_time = global_data.game_time

    def _remove_inter(self, key):
        if key in self._mp_inters:
            self._mp_inters.pop(key)

    def tick(self, dt):
        for key, it_data in six.iteritems(self._mp_inters):
            it_data.do_tick(dt)
            if it_data.time_out:
                self.del_arr.append(key)

        if self.del_arr:
            for key in self.del_arr:
                if key in self._mp_inters:
                    self._mp_inters.pop(key)

            self.del_arr = []
        if global_data.game_time - self._start_update_time > 5:
            self.need_update = False