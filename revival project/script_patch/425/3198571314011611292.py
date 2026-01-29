# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/LeftTimeCountDownWidget.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
import common.utils.timer as timer

class LeftTimeCountDownWidget(object):

    def __init__(self, parent_panel, time_lab_node, format_time_func):
        self.panel = parent_panel
        self._format_time_func = format_time_func
        self._time_lab_node = time_lab_node
        self._finish_func = None
        self._tick_timer = None
        self._tick_interval = 1
        self.init_parameters()
        self.init_event()
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel = None
        self._time_lab_node = None
        self._format_time_func = None
        self._finish_func = None
        self._tick_timer = None
        return

    def destroy(self):
        self._stop_timer()
        self.on_finalize_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'net_login_reconnect_event': self._on_login_reconnected
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        self._left_time_count_down_timer = None
        self._expire_time = None
        return

    def init_event(self):
        self.process_event(True)

    def begin_count_down_time(self, expire_time, count_down_finish_callback=None, use_big_interval=True):
        if not self._time_lab_node:
            return
        if not expire_time:
            return
        self._expire_time = expire_time
        self._finish_func = count_down_finish_callback
        self._stop_timer()
        left_time = self._expire_time - tutil.get_server_time()
        if left_time <= 0:
            return
        self._time_lab_node.setVisible(True)
        self._tick_interval = 1
        if use_big_interval:
            if left_time > tutil.ONE_DAY_SECONDS:
                self._tick_interval = tutil.ONE_HOUR_SECONS
            elif left_time > tutil.ONE_HOUR_SECONS:
                self._tick_interval = tutil.ONE_MINUTE_SECONDS
        self._time_lab_node.SetString(self._format_time_func(self._expire_time - tutil.get_server_time()))
        self._start_timer()

    def _time_update_cb(self, *args):
        if self.panel and self.panel.isValid():
            left_time = self._expire_time - tutil.get_server_time()
            if left_time > 1.0:
                self._time_lab_node.SetString(self._format_time_func(left_time))
            else:
                self._stop_timer()
                if self._finish_func:
                    self._finish_func()

    def _stop_timer(self):
        if self._tick_timer:
            global_data.game_mgr.unregister_logic_timer(self._tick_timer)
            self._tick_timer = None
        return

    def _start_timer(self):
        left_time = self._expire_time - tutil.get_server_time()
        if left_time <= 0:
            return
        self._tick_timer = global_data.game_mgr.register_logic_timer(self._time_update_cb, interval=self._tick_interval, times=-1, mode=timer.CLOCK)

    def _on_login_reconnected(self, *args):
        self._stop_timer()
        self._start_timer()