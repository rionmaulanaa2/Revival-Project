# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityDaliyChargeExchange.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_CONFIRM, NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils.template_utils import init_tempate_mall_i_item, get_reward_list_by_reward_id
from logic.gutils.mall_utils import get_goods_item_reward_id, get_goods_limit_num_all, get_goods_item_no
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
REMIND_PREIX = 'DALIY_CHARGE_REMIND_{}'

class ActivityDaliyChargeExchange(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202211/activity_common_charge_daily/open_activity_common_charge_daily_exchange'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'
       }
    GLOBAL_EVENT = {'buy_good_success': 'update_panel'
       }

    def on_init_panel(self, activity_type):
        super(ActivityDaliyChargeExchange, self).on_init_panel()
        self.activity_type = activity_type
        self.init_parameters()
        self.init_panel()

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self.activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self.exchange_item = ui_data.get('exchange_item', '70400093')
        self.init_exchange_goods_list(ui_data)

    def init_panel(self):
        self.panel.list_item.SetInitCount(self.exchange_goods_len)
        for idx in range(self.exchange_goods_len):
            self.init_exchange_item(idx)

        self.update_item_num()

    def init_exchange_goods_list(self, ui_data):
        exchange_goods_list = ui_data.get('exchange_goods_list', [])
        default_show_redpoint = ui_data.get('default_show_redpoint', [])
        self.default_show_redpoint = set([ exchange_goods_list[idx] for idx in default_show_redpoint ])

        def cmp_func(goods_id_a, goods_id_b):
            player = global_data.player
            is_a_all = player.get_buy_num_all(goods_id_a) >= get_goods_limit_num_all(goods_id_a)
            is_b_all = player.get_buy_num_all(goods_id_b) >= get_goods_limit_num_all(goods_id_b)
            if is_a_all != is_b_all:
                if is_a_all:
                    return 1
                if is_b_all:
                    return -1
            return 0

        self.exchange_goods_list = sorted(exchange_goods_list, key=cmp_to_key(cmp_func))
        self.exchange_goods_len = len(self.exchange_goods_list)
        self.exchange_item_cost = [ 0 for i in range(self.exchange_goods_len) ]

    def init_exchange_item(self, idx):
        item = self.panel.list_item.GetItem(idx)
        exchange_goods = self.exchange_goods_list[idx]
        mall_conf = confmgr.get('mall_config', exchange_goods, default={})
        exchange_item = get_goods_item_no(exchange_goods)
        item_cost = mall_conf.get('item_consumed', [])
        cost_item = item_cost[0]
        cost_num = item_cost[1]
        init_tempate_mall_i_item(item.temp_fragment, cost_item, cost_num, show_tips=True)
        init_tempate_mall_i_item(item.temp_reward, exchange_item, show_tips=True)
        item.temp_btn_get.btn_common.BindMethod('OnClick', lambda btn, touch, exchange_goods=exchange_goods: self.on_click_btn_exchange(btn, exchange_goods))
        item.btn_tick.BindMethod('OnClick', lambda btn, touch, exchange_goods=exchange_goods: self.on_click_btn_remind(btn, exchange_goods))
        self.exchange_item_cost[idx] = cost_num
        self.update_exchange_item(idx)

    def on_click_btn_remind(self, btn, exchange_goods):
        remind_str = REMIND_PREIX.format(exchange_goods)
        state = global_data.achi_mgr.get_cur_user_archive_data(remind_str, None)
        if state is None:
            state = True
        else:
            state = not state
        btn.SetSelect(state)
        global_data.achi_mgr.set_cur_user_archive_data(remind_str, state)
        return

    def on_click_btn_exchange(self, btn, exchange_goods):
        groceries_buy_confirmUI(str(exchange_goods))

    def update_panel(self):
        self.update_item_num()
        for idx in range(self.exchange_goods_len):
            self.update_exchange_item(idx)

    def update_item_num(self):
        player = global_data.player
        if not player:
            return
        self.panel.lab_got.SetString(get_text_by_id(80860) + str(global_data.player.get_item_num_by_no(int(self.exchange_item))))

    def update_exchange_item(self, idx):
        player = global_data.player
        if not player:
            return
        else:
            item = self.panel.list_item.GetItem(idx)
            exchange_goods = self.exchange_goods_list[idx]
            buy_num = player.get_buy_num_all(exchange_goods)
            max_buy_num = get_goods_limit_num_all(exchange_goods)
            item.lab_num.SetString(get_text_by_id(607018).format(buy_num, max_buy_num))
            is_all_exchange = False
            is_enough_cost = False
            if self.exchange_item_cost[idx] > global_data.player.get_item_num_by_no(int(self.exchange_item)):
                item.temp_fragment.lab_quantity.SetColor('#SR')
                item.temp_fragment.lab_quantity.SetString(str(self.exchange_item_cost[idx]))
                is_enough_cost = False
            else:
                is_enough_cost = True
                item.temp_fragment.lab_quantity.SetColor('#DW')
                item.temp_fragment.lab_quantity.SetString(str(self.exchange_item_cost[idx]))
            if buy_num >= max_buy_num:
                item.temp_btn_get.btn_common.SetEnable(False)
                item.temp_btn_get.btn_common.SetText(81877)
                is_all_exchange = True
            else:
                item.temp_btn_get.btn_common.SetEnable(is_enough_cost)
            remind_str = REMIND_PREIX.format(exchange_goods)
            state = global_data.achi_mgr.get_cur_user_archive_data(remind_str, None)
            if state is None and exchange_goods in self.default_show_redpoint:
                global_data.achi_mgr.set_cur_user_archive_data(remind_str, not is_all_exchange)
                state = not is_all_exchange
            elif state is None:
                state = False
            elif state and is_all_exchange:
                state = False
                global_data.achi_mgr.set_cur_user_archive_data(remind_str, False)
            item.btn_tick.SetSelect(state)
            item.btn_tick.SetEnable(not is_all_exchange)
            color = '#SC' if is_all_exchange else 4013373
            item.lab_tips.SetColor(color)
            item.lab_num.SetColor(color)
            return

    def on_click_btn_close(self, btn, touch):
        global_data.emgr.refresh_activity_redpoint.emit()
        self.close()