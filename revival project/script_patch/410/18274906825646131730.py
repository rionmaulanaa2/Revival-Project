# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHappySummerSign.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
import cc

class ActivityHappySummerSign(ActivityCollect):

    def init_parameters(self):
        super(ActivityHappySummerSign, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.prog_2_reward_id = task_utils.get_prog_rewards_in_dict(self.task_id)
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_info.SetString(get_text_by_id(conf.get('cDescTextID', '')))

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(None)
        self.refresh_time(None)
        task_ui_list = self.panel.act_list
        task_ui_list.SetInitCount(0)
        task_ui_list.SetInitCount(len(self.prog_2_reward_id))
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            task_ui = task_ui_list.GetItem(idx).temp_common
            if not task_ui:
                return
            task_ui.lab_name.SetString(task_utils.get_task_name(self.task_id, {'prog': prog}))
            reward_id = self.prog_2_reward_id.get(prog)
            template_utils.init_common_reward_list(task_ui.list_reward, reward_id)

        self.refresh_list()
        return

    def refresh_list(self):
        player = global_data.player
        if not player:
            return
        task_ui_list = self.panel.act_list
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            task_ui = task_ui_list.GetItem(idx).temp_common
            if not task_ui:
                return
            btn_receive = task_ui.temp_btn_get.btn_common
            task_ui.nd_get.setVisible(False)

            def check_btn(btn=btn_receive):
                can_receive = player.is_prog_reward_receivable(self.task_id, prog) and not player.has_receive_prog_reward(self.task_id, prog)
                is_received = player.has_receive_prog_reward(self.task_id, prog)
                btn.setVisible(not is_received)
                btn.SetEnable(can_receive)
                task_ui.nd_get.setVisible(is_received)

            @btn_receive.unique_callback()
            def OnClick(btn, touch, progress=prog):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                player.receive_task_prog_reward(self.task_id, progress)
                btn.SetText(80866)
                btn.SetEnable(False)

            check_btn()

    def reorder_prog_list(self, progs):

        def cmp_func(prog_a, prog_b):
            is_received_a = global_data.player.has_receive_prog_reward(self.task_id, prog_a)
            is_received_b = global_data.player.has_receive_prog_reward(self.task_id, prog_b)
            if is_received_a != is_received_b:
                if is_received_a:
                    return 1
                if is_received_b:
                    return -1
            return six_ex.compare(prog_a, prog_b)

        ret_list = sorted(progs, key=cmp_to_key(cmp_func))
        return ret_list

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))