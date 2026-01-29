# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ArmRace/ArmRaceFinishCountDownWidget.py
from __future__ import absolute_import
import math

class ArmRaceFinishCountDownWidget(object):

    def __init__(self, root_node, count_down_end_cb=None):
        self.panel = root_node
        self._count_down_end_cb = count_down_end_cb

    def on_init_panel(self):
        pass

    def on_finalize_panel(self):
        self.panel = None
        self._count_down_end_cb = None
        return

    def on_delay_close(self, revive_time):
        self.last_time = -1

        def refresh_time(pass_time):
            left_time = int(math.ceil((revive_time - pass_time) * 10 / 10.0))
            self.panel.lab_time.SetString(str(left_time))
            if self.last_time != left_time:
                self.panel.PlayAnimation('appear')
                self.last_time = left_time

        def refresh_time_finsh():
            if self.last_time != 0:
                self.panel.PlayAnimation('appear')
            self.panel.lab_time.SetString(str(0))
            self.panel.SetTimeOut(1, lambda : self._count_down_end())

        self.panel.StopTimerAction()
        if revive_time <= 0:
            self._count_down_end()
            return
        refresh_time(0)
        self.panel.PlayAnimation('appear')
        self.panel.prog_time.SetPercentageWithAni(0, revive_time)
        global_data.emgr.death_count_down_start.emit()
        self.panel.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=0.1)

    def _count_down_end(self):
        if callable(self._count_down_end_cb):
            self._count_down_end_cb()