# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeeklyCollect.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_readable_time, ONE_DAY_SECONDS
from logic.gcommon.time_utility import get_server_time, get_weekday, get_utc8_today_pass_time
from logic.gutils import sync_time
from common.cfg import confmgr

class ActivityWeeklyCollect(ActivityCollect):

    def refresh_time(self, parent_task):
        conf = confmgr.get('c_activity_config', self._activity_type)
        time_range = conf.get('cOpenTimeControl')
        if not time_range or not self.panel.lab_time:
            return
        cur_weekday = get_weekday(get_server_time())
        left_seconds = ONE_DAY_SECONDS - get_utc8_today_pass_time()
        start_weekday = time_range.get('start_weekday', 1)
        end_weekday = time_range.get('end_weekday', 1)
        if end_weekday < start_weekday:
            if end_weekday < cur_weekday:
                left_day = 7 - cur_weekday + end_weekday - 1
            else:
                left_day = end_weekday - cur_weekday - 1
            all_day = 7 - start_weekday + end_weekday - 1
            if left_day > all_day:
                day = 0
            else:
                day = left_day
        else:
            day = end_weekday - max(start_weekday, cur_weekday) - 1
        if day < 0:
            left_time = 0
        else:
            left_time = day * ONE_DAY_SECONDS + left_seconds
        self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))