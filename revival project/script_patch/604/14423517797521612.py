# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/SlideStatistics.py
from __future__ import absolute_import
import six_ex
import time
import world

class SlideStatistics(object):
    MAX_SLIDE_INTERVAL = 5
    ROCKER_CNT = 600
    ENABLE = False

    def __init__(self, rocker_func):
        self._rocker_func = rocker_func
        self._tmp_rocker_cnt = 0
        self._tmp_rocker_total_cnt = 0
        self._rocker_cnt = 0
        self._rocker_total_cnt = 0
        self._slide_outside_cnt = 0
        self._slide_total_cnt = 0
        self._slide_distribution = {}
        self._slide_time_distribution = {}
        self._slide_x_min = 0
        self._slide_x_max = 0
        self._slide_start_time = 0
        self._record_interval_cnt = 0

    def destroy(self):
        pass

    def get_info(self):
        info = [
         [
          self._tmp_rocker_cnt, self._tmp_rocker_total_cnt, self._rocker_cnt, self._rocker_total_cnt],
         [
          self._slide_outside_cnt, self._slide_total_cnt],
         six_ex.items(self._slide_distribution),
         six_ex.items(self._slide_time_distribution)]
        return info

    def record_rocker_dir(self):
        ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if not ui or ui.get_is_run_lock():
            return False
        rocker_dir = ui.get_move_dir()
        if not rocker_dir or rocker_dir.is_zero:
            return False
        angle = int(rocker_dir.yaw / 3.1415926 * 180)
        if self._rocker_func(angle):
            self._tmp_rocker_cnt += 1
            self._rocker_cnt += 1
        self._tmp_rocker_total_cnt += 1
        self._rocker_total_cnt += 1
        if self._tmp_rocker_total_cnt == self.ROCKER_CNT:
            data = self.get_info()
            self._tmp_rocker_cnt = 0
            self._tmp_rocker_total_cnt = 0
            return data
        return False

    def on_touch_slide(self, *args):
        self._record_interval_cnt += 1
        if self._record_interval_cnt < 3:
            return
        self._record_interval_cnt = 0
        scene = world.get_active_scene()
        if not scene or not scene._touch_move_pos:
            return
        x = scene._touch_move_pos.x
        w = global_data.ui_mgr.design_screen_size.width
        if not -0.01 * w < x < 1.01 * w:
            self._slide_outside_cnt += 1
        self._slide_total_cnt += 1
        if not self._slide_start_time:
            self._slide_start_time = time.time()
            self._slide_x_min = x
            self._slide_x_max = x
        self._slide_x_min = min(self._slide_x_min, x)
        self._slide_x_max = max(self._slide_x_max, x)
        if time.time() - self._slide_start_time >= self.MAX_SLIDE_INTERVAL:
            self.reset_slide_data()

    def reset_slide_data(self):
        if self._slide_start_time:
            dt = int(min(max(time.time() - self._slide_start_time, 0), self.MAX_SLIDE_INTERVAL))
            self._slide_time_distribution[dt] = self._slide_time_distribution.get(dt, 0) + 1
            diff = self._slide_x_max - self._slide_x_min
            level = min(int(10 * diff / global_data.ui_mgr.design_screen_size.width), 10)
            self._slide_distribution[level] = self._slide_distribution.get(level, 0) + 1
        self._slide_start_time = 0