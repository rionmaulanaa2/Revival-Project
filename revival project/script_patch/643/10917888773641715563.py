# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIPaint.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect

class ActivityKizunaAIPaint(ActivityCollect):

    def on_init_panel(self):
        super(ActivityKizunaAIPaint, self).on_init_panel()
        global_data.player.call_server_method('attend_activity', (self._activity_type,))

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            can_receive_reward_a = global_data.player.is_task_reward_receivable(task_id_a)
            can_receive_reward_b = global_data.player.is_task_reward_receivable(task_id_b)
            if can_receive_reward_a or can_receive_reward_b:
                if can_receive_reward_a:
                    return -1
                if can_receive_reward_b:
                    return 1
                return 0
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list