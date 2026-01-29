# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityExchangeNew.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.item.item_const import BTN_ST_EXCHANGED, BTN_ST_EXCHANGE, BTN_ST_UNEXCHANGE
from logic.gutils.new_template_utils import update_task_list_btn
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityExchangeNew(ActivityExchange):

    def __init__(self, dlg, activity_type):
        super(ActivityExchangeNew, self).__init__(dlg, activity_type)
        self.act_list = None
        self._children_tasks = []
        self.parent_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        return

    def on_init_panel(self):
        self.act_list = self.panel.act_list
        self.show_list()

    def on_finalize_panel(self):
        super(ActivityExchangeNew, self).on_finalize_panel()
        self._children_tasks = []

    def show_list(self):
        children_tasks = task_utils.get_children_task(self.parent_task_id)
        self._children_tasks = self.reorder_task_list(children_tasks)
        self.act_list.SetInitCount(len(self._children_tasks))
        for idx, task_id in enumerate(self._children_tasks):
            item_widget = self.act_list.GetItem(idx).temp_common
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                return
            prices_list = mall_utils.get_mall_item_price_list(goods_id)
            if not prices_list:
                return
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            target_item_num = mall_utils.get_goods_num(goods_id)
            if len(prices_list) == 4:
                item_widget.nd_1.setVisible(False)
                item_widget.nd_2.setVisible(True)
                cur_nd = item_widget.nd_2
                cost_item_no_a = prices_list[0]
                cost_item_no_b = prices_list[2]
                template_utils.init_tempate_mall_i_item(cur_nd.temp_fragment, cost_item_no_a, show_tips=True)
                template_utils.init_tempate_mall_i_item(cur_nd.temp_reward_2, cost_item_no_b, show_tips=True)
                template_utils.init_tempate_mall_i_item(cur_nd.temp_reward, target_item_no, target_item_num, show_tips=True)
            elif len(prices_list) == 2:
                item_widget.nd_1.setVisible(True)
                item_widget.nd_2.setVisible(False)
                cur_nd = item_widget.nd_1
                cost_item_no = prices_list[0]
                template_utils.init_tempate_mall_i_item(cur_nd.temp_fragment, cost_item_no, show_tips=True)
                template_utils.init_tempate_mall_i_item(cur_nd.temp_reward, target_item_no, target_item_num, show_tips=True)
            else:
                log_error('ActivityExchangeNew unsupported price_list!')
                return
            do_remind = [
             global_data.player.has_exchange_reminder(goods_id)]

            @item_widget.btn_tick.unique_callback()
            def OnClick(btn, touch, _do_remind=do_remind, goods_id=goods_id):
                _do_remind[0] = not _do_remind[0]
                btn.SetSelect(_do_remind[0])
                global_data.player.add_exchange_reminder(goods_id, _do_remind[0])

            item_widget.btn_tick.SetSelect(do_remind[0])

        self.refresh_list()

    def refresh_list(self):
        for idx, task_id in enumerate(self._children_tasks):
            item_widget = self.act_list.GetItem(idx).temp_common
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                return
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                return
            prices_list = mall_utils.get_mall_item_price_list(goods_id)
            if not prices_list:
                return
            limit_left_num = 1
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                limit_left_num = left_num
                item_widget.lab_num.SetString(get_text_by_id(607018).format(left_num, max_num))
            else:
                item_widget.lab_num.SetString('')
            if len(prices_list) == 4:
                cur_nd = item_widget.nd_2
                cost_item_no_a = prices_list[0]
                cost_item_no_b = prices_list[2]
                cost_item_amount_a = global_data.player.get_item_num_by_no(int(cost_item_no_a))
                cost_item_amount_b = global_data.player.get_item_num_by_no(int(cost_item_no_b))
                cost_item_num_a = prices_list[1]
                cost_item_num_b = prices_list[3]
                cost_str_a = self.get_cost_str(cost_item_amount_a, cost_item_num_a)
                cost_str_b = self.get_cost_str(cost_item_amount_b, cost_item_num_b)
                cur_nd.temp_fragment.lab_quantity.SetString(cost_str_a)
                cur_nd.temp_fragment_2.lab_quantity.SetString(cost_str_b)
            elif len(prices_list) == 2:
                cur_nd = item_widget.nd_1
                cost_item_no = prices_list[0]
                cost_item_amount = global_data.player.get_item_num_by_no(int(cost_item_no))
                cost_item_num = prices_list[1]
                cost_str = self.get_cost_str(cost_item_amount, cost_item_num)
                cur_nd.temp_fragment.lab_quantity.SetString(cost_str)
                cur_nd.temp_fragment.lab_quantity.setVisible(True)
            exchange_lv = extra_params.get('exchange_lv', None)

            @item_widget.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, _goods_id=goods_id, _prices_list=prices_list, _left_num=left_num, ex_lv=exchange_lv):
                self.on_click_exchange_btn(_goods_id, _prices_list, _left_num, ex_lv)

            self.update_exchange_btn(item_widget.temp_btn_get, left_num, prices_list)

        return

    def get_cost_str(self, have_cnt, need_cnt):
        if have_cnt >= need_cnt:
            return '#DB{0}#n/{1}'.format(have_cnt, need_cnt)
        else:
            return '#SR{0}#n/{1}'.format(have_cnt, need_cnt)

    def update_exchange_btn(self, nd_btn, left_num, price_list):
        if left_num <= 0:
            update_task_list_btn(nd_btn, BTN_ST_EXCHANGED)
        else:
            enable = mall_utils.check_item_money_list(price_list)
            if enable:
                update_task_list_btn(nd_btn, BTN_ST_EXCHANGE)
            else:
                update_task_list_btn(nd_btn, BTN_ST_UNEXCHANGE)

    def on_click_exchange_btn(self, goods_id, prices_list, left_num, exchange_lv):
        from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
        from logic.gcommon.item import item_const
        if not activity_utils.is_activity_in_limit_time(self._activity_type):
            return
        else:
            if exchange_lv is not None and global_data.player.get_lv() < exchange_lv:
                item_name = mall_utils.get_goods_name(goods_id)
                global_data.game_mgr.show_tip(get_text_by_id(608422).format(item=item_name))
                return
            if left_num >= 1:
                global_data.ui_mgr.close_ui('GroceriesBuyConfirmUI')
                GroceriesBuyConfirmUI(goods_id=goods_id, need_show=item_const.ITEM_SHOW_TYPE_ITEM)
            return