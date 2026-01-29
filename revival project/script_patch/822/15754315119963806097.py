# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/YuanbaoStrikeDescribeWidget.py
from __future__ import absolute_import
from logic.comsys.activity.widget.DescribeWidget import DescribeWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.cdata import loop_activity_data
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr

class YuanbaoStrikeDescribeWidget(DescribeWidget):

    def get_rule_text(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        if loop_activity_data.is_loop_activity(self._activity_type):
            rule_text_id = conf.get('cRuleTextID')
            act_start, act_end = loop_activity_data.get_loop_activity_open_time(self._activity_type)
            task_start = act_start
            task_end = max(0, act_end - 259200)
            task_start_str = tutil.get_time_string('%Y.%m.%d', task_start)
            task_end_str = tutil.get_time_string('%Y.%m.%d', task_end)
            act_end_str = tutil.get_time_string('%Y.%m.%d', act_end)
            rule_text = get_text_by_id(rule_text_id).format('', task_start_str, task_end_str, act_end_str)
        else:
            rule_text = super(YuanbaoStrikeDescribeWidget, self).get_rule_text()
        return rule_text