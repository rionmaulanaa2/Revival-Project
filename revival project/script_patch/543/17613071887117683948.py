# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/TriggerBoxCam.py
from __future__ import absolute_import
import cython_flag
import time
from logic.gcommon.utility import dummy_cb
from .ITriggerBoxCam import ITriggerBoxCam

class TriggerBoxCam(ITriggerBoxCam):

    def __init__(self, min_itvl, min_delta, max_stay):
        super(TriggerBoxCam, self).__init__()
        self.min_itvl = min_itvl
        self.min_delta = min_delta
        self.max_stay = max_stay
        self._t = 0
        self._f_data = 0
        self._f_tmp = 0
        self._next_enable = 0
        self._t_tri = 0
        self._trigger_func = dummy_cb
        self._trigger_stop = True
        self._begin_input = 0
        self._input_dirty = False

    def set_callback(self, func):
        self._trigger_func = func

    def input(self, t, f_data, check_trigger=True):
        if f_data is None:
            return
        else:
            self._input_dirty = True
            if self._trigger_stop:
                self._begin_input = t
                self._trigger_stop = False
            if self._f_data is None:
                self._f_data = f_data
                self._f_tmp = f_data
                self._t = t
                self.do_tri(t)
                return
            self._t = t
            self._f_tmp = f_data
            if check_trigger:
                self.check_trigger(t)
            return

    def get_cur(self):
        pass

    def check_trigger(self, t_now):
        if not self._input_dirty:
            return
        delta = abs(self._f_tmp - self._f_data)
        if delta == 0:
            if not self._trigger_stop and t_now - self._begin_input > 0.033:
                self._trigger_stop = True
            return
        if t_now < self._next_enable:
            return
        if delta > self.min_delta:
            self.do_tri(t_now)
        elif delta and t_now - self._t_tri > self.max_stay:
            self.do_tri(t_now)

    def do_tri(self, t_now):
        dt = t_now - self._begin_input
        self._f_data = self._f_tmp
        self._t_tri = t_now
        self._next_enable = self._t + self.min_itvl
        dt = 0.03 if dt == 0 else dt
        self._trigger_func(dt, self._f_data)
        self._begin_input = t_now

    def destroy(self):
        self._trigger_func = dummy_cb