# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaaiPlanTask.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils import task_utils
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
import cc
KIZUNAAI_ITEM_NO = 50600025
ITEM_ID_LST = [205102401, 30100050, 50101140, 50102006, 50101002]

class ActivityKizunaaiPlanTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaaiPlanTask, self).__init__(dlg, activity_type)
        self.fixed_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.random_task_id = act_data.get('daily_random', None)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        self.sub_widget = None
        return

    def on_finalize_panel(self):
        super(ActivityKizunaaiPlanTask, self).on_finalize_panel()
        self.sub_widget = None
        return

    def init_items(self):
        from logic.gutils.item_utils import get_lobby_item_name
        for idx in range(len(ITEM_ID_LST)):
            name_node = getattr(self.panel, 'lab_name_%s' % (idx + 1))
            name_node.SetString(get_lobby_item_name(ITEM_ID_LST[idx], need_part_name=False))
            name_btn = getattr(self.panel, 'btn_click_%s' % (idx + 1))

            @name_btn.unique_callback()
            def OnClick(btn, touch, item_id=ITEM_ID_LST[idx]):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, w_pos, extra_info=extra_info)
                return

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.init_items()
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.show_list()
        self.refresh_item_num()

        @self.panel.btn_have.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_KIZUNA_AI_GIFT
            jump_to_ui_utils.jump_to_charge(ACTIVITY_KIZUNA_AI_GIFT)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

    def init_parameters(self):
        super(ActivityKizunaaiPlanTask, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

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

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget

    def set_show(self, show, is_init=False):
        super(ActivityKizunaaiPlanTask, self).set_show(show, is_init)
        if self.cur_tab_name_id == self.last_tab_name_id:
            show and self.panel.PlayAnimation('loop')
            return
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        if show:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
             cc.DelayTime.create(1.0),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))
            if self.sub_widget and self.sub_widget.panel:
                self.sub_widget.panel.PlayAnimation('show')

    def refresh_item_num(self):
        item_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(KIZUNAAI_ITEM_NO)
        self.panel.lab_num.SetString(str(item_num))

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not global_data.player:
            return
        player = global_data.player
        fixed_children_tasks = task_utils.get_children_task(self.fixed_task_id)
        random_refresh_type = task_utils.get_task_fresh_type(self.random_task_id)
        random_children_tasks = player.get_random_children_tasks(random_refresh_type, self.random_task_id)
        children_tasks = fixed_children_tasks + random_children_tasks
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        self._timer_cb[0] = lambda : self.refresh_time(self.fixed_task_id)
        self.refresh_time(self.fixed_task_id)
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
        self.refresh_item_num()

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            total_times_a = task_utils.get_total_prog(task_id_a)
            cur_times_a = global_data.player.get_task_prog(task_id_a)
            total_times_b = task_utils.get_total_prog(task_id_b)
            cur_times_b = global_data.player.get_task_prog(task_id_b)
            not_finished_a = cur_times_a < total_times_a
            not_finished_b = cur_times_b < total_times_b
            if not_finished_a != not_finished_b:
                if not_finished_a:
                    return 1
                if not_finished_b:
                    return -1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list