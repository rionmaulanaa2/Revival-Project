# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityQingMingExchange.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityExchangeNew import ActivityExchangeNew
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.comsys.activity.widget import widget

@widget('DescribeWidget')
class ActivityQingMingExchange(ActivityExchangeNew):

    def __init__(self, dlg, activity_type):
        super(ActivityQingMingExchange, self).__init__(dlg, activity_type)

    def get_exchange_tasks(self):
        tasks = []
        tasks += task_utils.get_children_task(self.parent_task_id) or []
        return tasks

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

    def on_init_panel(self):
        super(ActivityQingMingExchange, self).on_init_panel()
        start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
        self._exchange_tasks = self.get_exchange_tasks()
        self.show_exchange_reward()
        self.panel.list_item.setVisible(False)
        self.panel.act_list.setVisible(True)
        self.panel.pnl_get_all.setVisible(False)
        self.panel.temp_get_all.setVisible(False)

    def init_describe(self):
        btn_describe = self.panel.btn_question
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        act_name_id = conf.get('iCatalogID', '')

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))

    def buy_good_success(self):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()
        self.show_exchange_reward()