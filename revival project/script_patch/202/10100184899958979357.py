# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryMultiExclusiveGiftUI.py
from __future__ import absolute_import
from .LotteryExclusiveGiftUI import LotteryExclusiveGiftUI
from logic.gutils.task_utils import try_do_jump, get_jump_conf
from logic.gutils.mall_utils import is_pc_global_pay

class LotteryMultiExclusiveGiftUI(LotteryExclusiveGiftUI):

    def on_init_panel(self, gift_dict=None, *args, **kwargs):
        self.bind_event(True)
        self.hide_main_ui()
        if not gift_dict:
            log_error('LotteryMultiExclusiveGiftUI has not gift_dict')
            return
        else:
            self._wait_for_charge_result = None
            self.task_list = gift_dict.get('task_list', None)
            self.goods_id = gift_dict.get('goods_id', [])
            self.goods_func_str = gift_dict.get('goods_func_str')
            self.goods_tag = gift_dict.get('goods_tag', [])
            lottery_name = gift_dict.get('lotteryname', '')
            if lottery_name:
                self.panel.lab_title.SetString(lottery_name)
            name = gift_dict.get('name', '')
            if name:
                self.panel.lab_name.SetString(name[0])
                self.panel.lab_name_r.SetString(name[1])
            if self.goods_tag:
                self.panel.lab_price.SetString(str(self.goods_tag[0]) + '%')
                self.panel.lab_price_r.SetString(str(self.goods_tag[1]) + '%')
            self.task_btns = [self.panel.temp_btn_2]
            self.goods_btn = [self.panel.temp_btn_3, self.panel.temp_btn_1]
            self.panel.btn_share.BindMethod('OnClick', self.on_click_btn_share)
            self.is_pc_global_pay = is_pc_global_pay()
            self.refresh_btns()
            return

    def on_click_btn_share(self, *args):
        if self.task_list:
            task_id = self.task_list[-1]
            jump_conf = get_jump_conf(task_id)
            if jump_conf:
                try_do_jump(task_id)

    def refresh_goods_reward(self):
        self._wait_for_charge_result = None
        for idx, widget in enumerate(self.goods_btn):
            self.update_one_item_widget(widget, str(self.goods_id[idx]), self.goods_func_str[idx])

        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def buy_good_fail(self):
        if self._wait_for_charge_result is None:
            return
        else:
            goods_id = self._wait_for_charge_result['goodsid']
            idx = 0
            for i, goods_list in enumerate(self.goods_func_str):
                if goods_id in goods_list:
                    idx = i

            fail_ui = global_data.ui_mgr.show_ui('ChargeGiftBoxFailUI', 'logic.comsys.common_ui')
            fail_ui.show_panel(str(self.goods_id[idx]), self.goods_func_str[idx], self.goods_tag[idx], global_data.lobby_mall_data.get_activity_sale_info(self.goods_func_str[idx]))
            self._wait_for_charge_result = None
            global_data.emgr.refresh_activity_redpoint.emit()
            return