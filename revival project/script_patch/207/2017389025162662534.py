# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/ReceiveBoxCam.py
from __future__ import absolute_import
import queue
import time
from logic.gcommon.utility import dummy_cb

class ReceiveBoxCam(object):

    def __init__(self, func=None):
        super(ReceiveBoxCam, self).__init__()
        self.func = func
        self._cache = queue.Queue()
        self._next_update_time = 0
        self.need_update = False

    def destroy(self):
        self.need_update = False
        self.func = dummy_cb

    def input(self, val, dt):
        if type(dt) not in (int, float):
            return
        self._cache.put([val, dt])
        if self._cache.qsize() >= 2 and self.need_update == False:
            self.need_update = True

    def tick(self, dt):
        if not self.need_update:
            return
        t_now = time.time()
        if self._cache.qsize() == 0:
            self.need_update = False
            self._next_update_time = 0
            return
        if self._next_update_time >= t_now + dt:
            return
        if self._next_update_time == 0:
            self._next_update_time = t_now
        reach_time = 0
        reach_val = 0
        while self._cache.qsize() != 0:
            info = self._cache.get()
            reach_val = info[0]
            reach_time += info[1]
            self._next_update_time += info[1]
            if self._next_update_time >= t_now + dt:
                break

        if self.func:
            self.func(reach_time, reach_val)