# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLuckySummerSign.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang
from logic.gcommon.common_const.lang_data import LANG_CN
import cc

class ActivityLuckySummerSign(ActivityCollect):

    def on_init_panel(self):
        self._refresh_reward_cb = {}
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_info.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.show_list()

    def init_parameters(self):
        super(ActivityLuckySummerSign, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.prog_2_reward_id = task_utils.get_prog_rewards_in_dict(self.task_id)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

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

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(None)
        self.refresh_time(None)
        self._prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        sub_act_list = self.panel.act_list
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        ui_data = conf.get('cUiData', {})
        sub_act_list.BindMethod('OnCreateItem', self.on_create_item(self.on_task_item, ui_data))
        sub_act_list.DeleteAllSubItem()
        self._refresh_reward_cb = {}
        sub_act_list.SetInitCount(len(self.prog_2_reward_id))
        sub_act_list.scroll_Load()
        self.panel.img_swimring_01.setVisible(get_cur_text_lang() in [LANG_CN])
        return

    def set_show(self, show, is_init=False):
        super(ActivityLuckySummerSign, self).set_show(show, is_init)
        self.show_animation()

    def show_animation(self):
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))

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

    def on_create_item(self, inst_cb, ui_data):

        def _on_create_item(list_reward, index, widget_item):
            inst_cb(widget_item, index, ui_data)

        return _on_create_item

    def on_task_item(self, widget_item, i, ui_data):
        if len(self._prog_list) < i + 1:
            return
        prog = self._prog_list[i]
        self._show_list_impl(widget_item, prog, ui_data)

        def refresh_cb(p_id=prog, w_item=widget_item, u_data=ui_data):
            self._refresh_list_imp(w_item, p_id)

        self._refresh_reward_cb[i] = refresh_cb
        refresh_cb()

    def _show_list_impl(self, widget_item, prog, ui_data):
        task_ui = widget_item.temp_common
        task_ui.lab_name.SetString(task_utils.get_task_name(self.task_id, {'prog': prog}))
        reward_id = self.prog_2_reward_id.get(prog)
        template_utils.init_common_reward_list(task_ui.list_reward, reward_id)

    def refresh_list(self):
        for key, cb in six.iteritems(self._refresh_reward_cb):
            cb()

    def _refresh_list_imp(self, widget_item, prog):
        player = global_data.player
        if not player:
            return
        task_ui = widget_item.temp_common
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