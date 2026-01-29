# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityQingMingTask.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollectNew import ActivityCollectNew
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_INACTIVE, BTN_ST_OVERDUE
from logic.gutils import mall_utils
from logic.comsys.activity.widget import widget

@widget('DescribeWidget')
class ActivityQingMingTask(ActivityCollectNew):

    def __init__(self, dlg, activity_type):
        super(ActivityQingMingTask, self).__init__(dlg, activity_type)
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.fixed_task_id = act_data.get('daily_fixed', None)
        self.exchange_task_id = act_data.get('exchange', None)
        self.week_1_task_id = act_data.get('weekend_1', None)
        self.week_2_task_id = act_data.get('weekend_2', None)
        return

    def on_init_panel(self):
        self.act_list_daily = self.panel.list_item.GetItem(0).act_list_common
        self.act_list_weekend = self.panel.list_item.GetItem(0).act_list_common_2
        self._daily_tasks = self.reorder_task_list(self.get_daily_tasks())
        self._weekend_tasks = self.reorder_task_list(self.get_weekend_tasks())
        self._exchange_tasks = self.get_exchange_tasks()
        self._children_tasks = self.reorder_task_list(self._daily_tasks + self._weekend_tasks)
        self.valid_tasks = self.filter_valid(self._children_tasks)
        self.show_list()
        self.show_exchange_reward()
        self.show_weekend_state()
        start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
        self.panel.list_item.setVisible(True)
        self.panel.act_list.setVisible(False)

    def filter_valid(self, tasks):
        valid_tasks = []
        for task in tasks:
            if task_utils.is_task_open_ex(task):
                valid_tasks.append(task)

        return valid_tasks

    def _on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()
        self.show_exchange_reward()

    def show_weekend_state(self):
        lab_weekend = self.panel.list_item.GetItem(0).lab_weekend
        if task_utils.get_raw_left_open_time(self.week_1_task_id) > 0:
            if task_utils.is_task_open_ex(self.week_1_task_id):
                lab_weekend.SetString(get_text_by_id(610815))
            else:
                lab_weekend.SetString(get_text_by_id(610814))
        elif task_utils.get_raw_left_open_time(self.week_2_task_id) > 0:
            if task_utils.is_task_open_ex(self.week_2_task_id):
                lab_weekend.SetString(get_text_by_id(610816))
            else:
                lab_weekend.SetString(get_text_by_id(610814))
        else:
            lab_weekend.SetString(get_text_by_id(610817))
        return None

    def show_exchange_reward(self):
        return
        for idx, task_id in enumerate(self._exchange_tasks):
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                return
            prices_list = mall_utils.get_mall_item_price_list(goods_id)
            if not prices_list:
                return
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            target_item_num = mall_utils.get_goods_num(goods_id)
            tmp_stock_state = getattr(self.panel, 'lab_stock_' + str(idx + 1), False)
            tmp_stock_num = getattr(self.panel, 'lab_stock_number_' + str(idx + 1), False)
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                if left_num > 0:
                    tmp_stock_state.SetString(get_text_by_id(610809))
                    tmp_stock_num.SetString(str(left_num))
                else:
                    tmp_stock_state.SetString(get_text_by_id(601221))
                    tmp_stock_num.SetString(' ')
            else:
                tmp_stock_state.SetString(get_text_by_id(601221))
                tmp_stock_num.SetString(' ')
            tmp_name = getattr(self.panel, 'lab_name_' + str(idx + 1), False)
            tmp_name.SetString(mall_utils.get_lobby_item_name(target_item_no))
            tmp_thing = getattr(self.panel, 'btn_thing_' + str(idx + 1), False)
            template_utils.init_tempate_mall_i_item(tmp_thing.temp_items, target_item_no, target_item_num, show_tips=True)

    def show_list(self):
        self.show_list_by_node(self.act_list_daily, self._daily_tasks)
        self.show_list_by_node(self.act_list_weekend, self._weekend_tasks)
        self.init_get_all_btn()
        self.update_get_all_btn()

    def get_exchange_tasks(self):
        tasks = []
        tasks += task_utils.get_children_task(self.exchange_task_id) or []
        return tasks

    def get_daily_tasks(self):
        tasks = []
        tasks += task_utils.get_children_task(self.fixed_task_id) or []
        return tasks

    def get_weekend_tasks(self):
        tasks = []
        if task_utils.get_raw_left_open_time(self.week_1_task_id) > 0:
            tasks += task_utils.get_children_task(self.week_1_task_id) or []
        else:
            tasks += task_utils.get_children_task(self.week_2_task_id) or []
        return tasks

    def gen_login_string(self):
        total_prog = task_utils.get_total_prog(self.login_task_id)
        login_prog = global_data.player.get_task_prog(self.login_task_id)
        return get_text_by_id(610823).format(prog=str(login_prog))

    def show_list_by_node(self, tmp_list, tasks):
        player = global_data.player
        if not player:
            return
        if not tmp_list:
            log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
            return
        tmp_list.SetInitCount(0)
        tmp_list.SetInitCount(len(tasks))
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        ui_data = conf.get('cUiData', {})
        for idx, task_id in enumerate(tasks):
            item_widget = tmp_list.GetItem(idx).temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)

        self.refresh_list_by_node(tmp_list, tasks)

    def refresh_list(self):
        self.refresh_list_by_node(self.act_list_daily, self._daily_tasks)
        self.refresh_list_by_node(self.act_list_weekend, self._weekend_tasks)

    def refresh_list_by_node(self, tmp_list, tasks):
        player = global_data.player
        if not player:
            return
        if not tmp_list:
            log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
            return
        for idx, task_id in enumerate(tasks):
            item_widget = tmp_list.GetItem(idx).temp_common
            total_times = task_utils.get_total_prog(task_id)
            cur_times = player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            update_task_list_btn(item_widget.nd_task.temp_btn_get, self.get_receive_btn_status(task_id))

            @item_widget.nd_task.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id):
                self.on_click_receive_btn(_task_id)

    def get_receive_btn_status(self, task_id):
        if not task_utils.is_task_open_ex(task_id):
            if task_utils.get_raw_left_open_time_ex(task_id) > 0:
                return BTN_ST_INACTIVE
            else:
                return BTN_ST_OVERDUE

        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_RECEIVED:
            return BTN_ST_RECEIVED
        if status == ITEM_UNGAIN:
            return BTN_ST_ONGOING
        if status == ITEM_UNRECEIVED:
            return BTN_ST_CAN_RECEIVE

    def on_click_get_all_btn(self, *args):
        global_data.player.receive_tasks_reward(self.valid_tasks)

    def on_click_receive_btn(self, task_id):
        super(ActivityQingMingTask, self).on_click_receive_btn(task_id)

    def init_describe(self):
        btn_describe = self.panel.btn_question
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        act_name_id = conf.get('iCatalogID', '')

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))

    def get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self.valid_tasks:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task