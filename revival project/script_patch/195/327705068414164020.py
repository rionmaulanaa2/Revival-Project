# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/scale_timer.py
from __future__ import absolute_import
from __future__ import print_function
import six
import time
import common.utils.timer as timer

class ScaleTimer(object):

    def __init__(self, interval):
        self.state_groups = {}
        self.timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self.on_update, interval=interval, mode=timer.CLOCK, timedelta=True)

    def destroy(self):
        global_data.game_mgr.get_post_logic_timer().unregister(self.timer_id)
        self.state_groups.clear()

    def on_update(self, dt):
        remove_groups = {}
        state_groups = dict(self.state_groups)
        for key, group in six.iteritems(state_groups):
            dt_pass = dt * group[4]
            group[1] += dt_pass
            group[2] += dt_pass
            if group[1] >= group[3]:
                group[1] -= group[3]
                group[5] += 1
                if group[5] >= group[6]:
                    remove_groups[key] = True
                try:
                    group[7]()
                except Exception as e:
                    print('[ERROR] ScaleTimer on_update key={}'.format(key))
                    import traceback
                    traceback.print_exc()

        for key, _ in six.iteritems(remove_groups):
            if key in self.state_groups:
                del self.state_groups[key]

    def register(self, key, interval, callback, max_times=1):
        self.unregister(key)
        if key not in self.state_groups:
            start_time = time.time()
            acc_time = 0.0
            time_scale = 1.0
            pass_time = 0.0
            exec_times = 0
            max_times = max_times
            self.state_groups[key] = [start_time, pass_time, acc_time, interval, time_scale, exec_times, max_times, callback]

    def unregister(self, key):
        if key in self.state_groups:
            del self.state_groups[key]

    def is_active(self, key):
        return key in self.state_groups

    def set_time_scale(self, key, scale):
        if key in self.state_groups:
            self.state_groups[key][4] = scale

    def get_time_scale(self, key):
        if key not in self.state_groups:
            return 1.0
        return self.state_groups[key][4]

    def set_interval(self, key, interval):
        if key in self.state_groups:
            self.state_groups[key][3] = interval

    def get_pass_time(self, key):
        if key not in self.state_groups:
            return -1
        return self.state_groups[key][2]

    def get_state_groups(self):
        return self.state_groups