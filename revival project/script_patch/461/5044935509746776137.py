# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLoopTeamup.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCommonTeamupNew import ActivityCommonTeamupNew
from logic.gcommon.cdata import loop_activity_data
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityLoopTeamup(ActivityCommonTeamupNew):

    def refresh_time(self):
        if not self.panel or not self.panel.lab_date:
            return
        if not loop_activity_data.is_loop_activity(self._activity_type):
            log_error('this should never happen! activity %s', self._activity_type)
            return
        lab_time = self.panel.lab_date
        begin_time, end_time = loop_activity_data.get_loop_activity_open_time(self._activity_type)
        if end_time:
            left_time = end_time - tutil.time()
        else:
            left_time = 0
        if left_time > 0:
            if left_time > tutil.ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(610105).format(tutil.get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(610105).format(tutil.get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(tutil.get_readable_time(close_left_time))