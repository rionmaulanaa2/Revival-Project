# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCollect.py
from __future__ import absolute_import
import six
from functools import cmp_to_key
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.time_utility import get_readable_time, ONE_DAY_SECONDS
from cocosui import cc, ccui, ccs

class ActivityCollect(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCollect, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self.register_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.show_list()

    def _on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_describe
        if btn_describe:

            @btn_describe.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))
                x, y = btn_describe.GetPosition()
                wpos = btn_describe.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
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

    def refresh_time(self, parent_task):
        if not self.panel or not self.panel.lab_time:
            return
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = ONE_DAY_SECONDS + left_time
            self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(close_left_time)))

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        self._timer_cb[0] = lambda : self.refresh_time(parent_task)
        self.refresh_time(parent_task)
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list()

    def _set_item_widget_lab_num(self, item_widget, total_times, cur_times):
        if total_times > 1:
            item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
        else:
            item_widget.lab_num.SetString('')

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    text_id = jump_conf.get('unreach_text', '')
                    if text_id:
                        btn.SetText(text_id)
                        btn.SetEnable(True)
                    else:
                        btn.SetEnable(False)
                else:
                    btn.setVisible(True)
                    btn.SetEnable(True)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = task_utils.get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = task_utils.get_jump_conf(task_id)
                if _cur_times < _total_times and jump_conf.get('unreach_text', ''):
                    item_utils.exec_jump_to_ui_info(jump_conf)
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

            check_btn()