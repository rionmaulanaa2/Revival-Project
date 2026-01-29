# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySkateboard.py
from __future__ import absolute_import
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.ActivityTemplate import ActivityGlobalTemplate, ActivityGlTaskTemplate

class ActivitySkateboard(ActivityGlTaskTemplate):
    ACTIVITY_TYPE = activity_const.ACTIVITY_ALL_SERVER_SKATEBOARD
    TASK_SUFFIX = 'm'
    MY_DATA_SUFFIX = 'm'

    def __init__(self, dlg, activity_type):
        super(ActivitySkateboard, self).__init__(dlg, activity_type)

    def set_show(self, show, is_init=False):
        super(ActivitySkateboard, self).set_show(show)
        if show:
            self.second_callback()

    def _init_global_achieve_sp(self, final_goal_num):
        text = get_text_by_id(705056) + str(final_goal_num) + 'km'
        self.panel.lab_goal_num.SetString(text)

    def get_achieve_reward_nodes(self):
        return [
         [
          self.panel.temp_final_reward, None]]