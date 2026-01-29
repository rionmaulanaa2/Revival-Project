# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/delay_module.py
from __future__ import absolute_import
from six.moves import range
import time
DELTA_FIX = 60
MAX_AVERAGE = 5
BASE_DECADE = 4
ITVL_SHOW = 3

class DelayCnt(object):

    def __init__(self):
        super(DelayCnt, self).__init__()
        self._cnt = 0
        self._lst_delay = [ 0 for i in range(0, MAX_AVERAGE) ]
        self._lst_out = []

    def tick(self):
        t = time.time()
        self._lst_out.append(t)

    def is_show_tick(self):
        return self._cnt % ITVL_SHOW == 0

    def tock(self):
        t = time.time()
        if not self._lst_out:
            return
        t0 = self._lst_out.pop(0)
        n = (t - t0) * 1000
        if n > BASE_DECADE * 10:
            fix = (int(n) / 10 - BASE_DECADE) * 10
            delta = n - fix if fix <= DELTA_FIX else n - DELTA_FIX
        else:
            delta = n
        self.record(delta)

    def record(self, delta):
        self._lst_delay[self._cnt % MAX_AVERAGE] = delta
        self._cnt += 1

    def get_delay(self):
        if self._cnt < MAX_AVERAGE:
            return 0
        total = sum(self._lst_delay)
        return int(total / float(MAX_AVERAGE))

    def reset(self):
        self._lst_out = []
        self._lst_delay = [ 0 for i in range(0, MAX_AVERAGE) ]


g_cnt = DelayCnt()