# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityValentineDay.py
from __future__ import absolute_import
from functools import cmp_to_key
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityValentineDay(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityValentineDay, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type)
        self._parent_task_id = conf.get('cTask')
        open_data_text = '2021.2.11 - 2021.3.18' if G_IS_NA_PROJECT else '2021.2.11 - 2021.2.24'
        self.panel.lab_time_num.SetString(open_data_text)
        self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        self._font_size = 19

    def on_init_panel(self):
        self._init_collect_list()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        e_mgr = global_data.emgr
        e_conf = {'receive_task_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            e_mgr.bind_events(e_conf)
        else:
            e_mgr.unbind_events(e_conf)

    def set_show(self, show, is_init=False):
        super(ActivityValentineDay, self).set_show(show, is_init)
        self.panel.PlayAnimation('into')

    def _on_update_reward(self, task_id):
        global_data.player.read_activity_list(self._activity_type)
        self._init_collect_list()

    def _reorder_collect_task_list(self, tasks):

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

    def _init_collect_list(self):
        children_tasks = task_utils.get_children_task(self._parent_task_id)
        self._children_tasks = self._reorder_collect_task_list(children_tasks)
        lang = get_cur_lang_name()
        if lang == 'jp':
            self._font_size = 13
        elif lang == 'th':
            self._font_size = 15
        elif lang == 'ko':
            self._font_size = 17
        else:
            self._font_size = 19
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(len(self._children_tasks))
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            self.set_item_content(item_widget, task_id)

    def set_item_content(self, item_widget, task_id):
        item_widget.lab_name.SetFontSize(self._font_size)
        item_widget.lab_num.SetFontSize(self._font_size)
        reward_id = task_utils.get_task_reward(task_id)
        item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
        template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
        total_times = task_utils.get_total_prog(task_id)
        cur_times = global_data.player.get_task_prog(task_id)
        if total_times > 1:
            item_widget.lab_num.SetString('({0}/{1})'.format(cur_times, total_times))
        else:
            item_widget.lab_num.SetString('')
        btn_widget = item_widget.temp_btn_get.btn_common
        has_rewarded = global_data.player.has_receive_reward(task_id)
        if has_rewarded:
            btn_widget.SetEnable(False)
            btn_widget.SetText(80866)
        elif cur_times < total_times:
            btn_widget.SetEnable(False)
            btn_widget.SetText(80930)
        else:
            btn_widget.SetEnable(True)
            btn_widget.SetText(80930)

        @btn_widget.unique_callback()
        def OnClick(btn, touch, task_id=task_id):
            if activity_utils.is_activity_finished(self._activity_type) or not task_utils.is_task_open(task_id):
                global_data.game_mgr.show_tip(607911)
                return
            if not global_data.player.is_task_reward_receivable(task_id):
                return
            global_data.player.receive_task_reward(task_id)
            btn.SetText(80866)
            btn.SetEnable(False)