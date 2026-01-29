# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/ActivitySpringFestivalLogin.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollectNew import ActivityCollectNew
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS

class ActivitySpringFestivalLogin(ActivityCollectNew):

    def on_init_panel(self):
        self.act_list = self.panel.act_list
        self.show_list()
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_activity_describe and self.panel.lab_activity_describe.SetString(get_text_by_id(conf.get('cDescTextID', '')))

    def show_list(self):
        super(ActivitySpringFestivalLogin, self).show_list()
        self._timer_cb[0] = lambda : self.refresh_time(self.fixed_task_id)
        self.refresh_time(self.fixed_task_id)

    def refresh_time(self, parent_task):
        if not self.panel or not self.panel.lab_activity_time:
            return
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_activity_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_activity_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_activity_time.SetString(get_readable_time(close_left_time))

    def update_get_all_btn(self):
        receivable_task_num = len(self.get_all_receivable_tasks())
        if receivable_task_num >= 1:
            self.panel.nd_get_all.setVisible(True)
        else:
            self.panel.nd_get_all.setVisible(False)