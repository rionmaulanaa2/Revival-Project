# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/LotteryTicketBuyConfirmUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from common.const import uiconst
from logic.gcommon.item import item_const
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.client.const import mall_const
from common.cfg import confmgr
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.common_ui.ItemNumInputWidget import ItemNumInputWidget
from logic.gutils.mall_buy_confirm_func import goods_buy_need_confirm
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class LotteryTicketBuyConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mall/buy_confirm_lottery'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}

    def on_init_panel(self, goods_id, pick_list=[], lottery_id=None):
        super(LotteryTicketBuyConfirmUI, self).on_init_panel()
        self.lottery_id = lottery_id
        self.goods_id = goods_id
        self.pick_list = pick_list
        self.init_desc_widget()
        self.init_num_adjust_widget()
        self.process_event(True)

    def on_finalize_panel(self):
        self.destroy_widget('num_adjust_widget')
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_desc_widget(self):
        self.panel.img_item.SetDisplayFrameByPath('', mall_utils.get_goods_pic_path(self.goods_id))
        self.panel.lab_name.SetString(mall_utils.get_goods_name(self.goods_id))
        self.panel.lab_describe.SetString(mall_utils.get_goods_decs(self.goods_id))
        limit_buy, num_info, limit_txt_id = mall_utils.get_limit_info(self.goods_id)
        if limit_buy:
            left_num, max_num = num_info
            color = '#SS' if left_num else '#SR'
            self.panel.lab_num.SetString(''.join([color, str(left_num), '#n', '/', str(max_num)]))
            self.panel.temp_btn_buy1.btn_common.SetEnable(left_num > 0)
        else:
            self.panel.lab_limit.setVisible(False)

    def init_num_adjust_widget(self):
        mall_conf = confmgr.get('mall_config', self.goods_id, default={})
        num_times = mall_conf.get('num_times', 1)
        limit_buy, num_info, limit_txt_id = mall_utils.get_limit_info(self.goods_id)
        if limit_buy:
            left_num, max_num = num_info
            max_adjust_num = min(left_num, num_times) if num_times else left_num
        else:
            max_adjust_num = num_times
        self.num_adjust_widget = ItemNumInputWidget(self.panel.temp_quantity)
        self.num_adjust_widget.init_input_widget(self.on_item_num_changed, init_quantity=1, max_quantity=max_adjust_num)

    def on_item_num_changed(self, item_num):
        buy_btn = self.panel.temp_btn_buy1
        prices = mall_utils.get_mall_item_price(self.goods_id, item_num, pick_list=self.pick_list)
        if not prices:
            return
        price_info = prices[0]
        goods_payment = price_info.get('goods_payment')
        real_price = price_info.get('real_price')
        template_utils.init_price_template(price_info, buy_btn.temp_price, color=mall_const.DARK_PRICE_COLOR)
        buy_btn.btn_common.SetEnable(item_num > 0)

        @buy_btn.btn_common.unique_callback()
        def OnClick(btn, touch, _goods_payment=goods_payment, _real_price=real_price):
            if mall_utils.limite_pay(self.goods_id):
                return

            def _pay():
                extra_info = {'ticket_lottery_id': self.lottery_id} if self.lottery_id else {}
                global_data.player.buy_goods(self.goods_id, item_num, _goods_payment, need_show=item_const.ITEM_SHOW_TYPE_ITEM, extra_info=extra_info)

            def _after_yueka():
                if not mall_utils.check_payment(_goods_payment, _real_price, cb=_pay):
                    return
                if goods_buy_need_confirm(self.goods_id, call_back=_pay):
                    return
                _pay()

            mall_utils.check_yueka_discount_notice(self.goods_id, lambda : _after_yueka())