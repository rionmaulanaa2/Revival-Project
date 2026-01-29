# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/KeepAliveProxy.py
from __future__ import absolute_import
from . import Timer
ST_INIT = 0
ST_INTERVAL = 1
ST_WAITING = 2

class KeepAliveProxy(object):

    def __init__(self, connection, interval, timeoutnum):
        super(KeepAliveProxy, self).__init__()
        self.connection = connection
        self.keep_interval = interval
        self.keep_interval_timer = None
        self.time_out_counter = 0
        self.time_out_max = timeoutnum
        self.keep_state = ST_INIT
        return

    def set_keep_alive(self, flag):
        if flag:
            if self.keep_state == ST_INIT:
                self.keep_state = ST_INTERVAL
                self.keep_interval_timer = Timer.addRepeatTimer(self.keep_interval, lambda : self._send_keep_alive())
        elif self.keep_state != ST_INIT:
            self.keep_interval_timer.cancel()
            self.keep_interval_timer = None
        return

    def keep_alive_ack(self):
        self.keep_state = ST_INTERVAL
        self.time_out_counter = 0

    def _keep_alive(self):
        self.connection.keep_alive()

    def _send_keep_alive(self):
        if self.keep_state == ST_WAITING:
            self._keep_alive_timeout()
        self._keep_alive()
        self.keep_state = ST_WAITING

    def _keep_alive_timeout(self):
        self.time_out_counter += 1
        if self.time_out_counter < self.time_out_max:
            self.connection.keep_alive_timeout(self.time_out_counter)
        else:
            self.connection.keep_alive_failed()