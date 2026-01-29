# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryHalloweenWidget.py
from __future__ import absolute_import
from .LotteryCommonTurntableWidget import LotteryCommonTurntableWidget
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_const.activity_const import ACTIVITY_TEMP_GO_20935
from logic.gcommon.item import item_const
from logic.gutils.mall_utils import limite_pay
from logic.gutils.jump_to_ui_utils import jump_to_activity
from logic.gutils.activity_utils import check_out_of_date
PIC_MAP = {201001146: 'gui/ui_res_2/activity/activity_202111/halloween/icon_halloween_lotter_role1.png',
   201001244: 'gui/ui_res_2/activity/activity_202111/halloween/icon_halloween_lotter_role3.png',
   201001346: 'gui/ui_res_2/activity/activity_202111/halloween/icon_halloween_lotter_role2.png'
   }
ACTIVITY_ITEM = '700800001'

class LotteryHalloweenWidget(LotteryCommonTurntableWidget):

    def init_panel(self):
        super(LotteryHalloweenWidget, self).init_panel()
        self.init_btn_exchange()
        self.init_btn_get()
        self.update_exchange_coin()
        self.update_lucky_info()
        self.update_activity_btn_visible()
        self.init_shop_role_img()

    def show(self):
        super(LotteryHalloweenWidget, self).show()
        if self.panel.isVisible() and self.exchange_reward_widget and self.exchange_reward_widget.visible:
            global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', False)

    def on_lottery_ended(self):
        super(LotteryHalloweenWidget, self).on_lottery_ended()
        self.update_exchange_coin()
        self.update_activity_btn_visible()

    def update_remind_exchange_item_id(self):
        super(LotteryHalloweenWidget, self).update_remind_exchange_item_id()
        self.update_exchange_coin()

    def switch_show_model(self, offset, is_auto=False):
        super(LotteryHalloweenWidget, self).switch_show_model(offset, is_auto)
        self.init_shop_role_img()

    def refresh_show_model(self, show_model_id=None):
        super(LotteryHalloweenWidget, self).refresh_show_model(show_model_id)
        self.init_shop_role_img()

    def update_exchange_coin(self):
        self.panel.temp_exchange.list_item_coin.GetItem(0).lab_num.SetString(str(global_data.player.get_item_money(70400087)))
        self.panel.temp_exchange.list_item_coin.GetItem(1).lab_num.SetString(str(global_data.player.get_item_money(70400086)))

    def init_shop_role_img(self):
        if self.show_model_id in PIC_MAP:
            self.panel.img_role.SetDisplayFrameByPath('', PIC_MAP[self.show_model_id])

    def init_btn_exchange(self):
        if self.panel.btn_exchange:
            self.panel.btn_exchange.lab_num.setVisible(False)
            self.panel.btn_exchange.lab_name.setVisible(True)
            self.panel.btn_exchange.lab_name.SetString(400460)

            @global_unique_click(self.panel.btn_exchange)
            def OnClick(*args):
                self.on_click_btn_exchange()

    def on_click_btn_exchange(self, *args):
        from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
        global_data.ui_mgr.close_ui('GroceriesBuyConfirmUI')
        GroceriesBuyConfirmUI(goods_id='700400587', need_show=item_const.ITEM_SHOW_TYPE_ITEM)

    def init_btn_get(self):

        @global_unique_click(self.panel.btn_get)
        def OnClick(*args):
            if limite_pay(ACTIVITY_ITEM) or check_out_of_date(ACTIVITY_TEMP_GO_20935):
                self.panel.btn_get.setVisible(False)
                return
            jump_to_activity(ACTIVITY_TEMP_GO_20935)

    def update_activity_btn_visible(self):
        self.panel.btn_get.setVisible(not (limite_pay(ACTIVITY_ITEM) or check_out_of_date(ACTIVITY_TEMP_GO_20935)))

    def on_click_btn_shop(self, *args):
        super(LotteryHalloweenWidget, self).on_click_btn_shop()
        exchange_goods_list = []
        if not self.exchange_reward_widget or not self.exchange_reward_widget.big_display_item_list:
            return
        for _, item_id in self.exchange_reward_widget.big_display_item_list:
            exchange_goods_list.append(item_id)

        if self.show_model_id in exchange_goods_list:
            idx = exchange_goods_list.index(self.show_model_id)
            self.exchange_reward_widget.perform_click_big_display_item(idx)

    def jump_to_exchange_shop_widget(self, goods_id, check=True):
        if not self.exchange_reward_widget:
            return
        self.exchange_reward_widget.visible = True
        self.remind_exchange_archive_data[self.lottery_id] = self.cur_remind_exchange_item_id
        self.update_remind_exchange_item_id()
        if goods_id in self.exchange_reward_widget.big_display_goods_ids:
            idx = self.exchange_reward_widget.big_display_goods_ids.index(goods_id)
            self.exchange_reward_widget.perform_click_big_display_item(idx)
            self.exchange_reward_widget.scroll_exchange_item_list(True)
        elif goods_id in self.exchange_reward_widget.small_display_goods_ids:
            idx = self.exchange_reward_widget.small_display_goods_ids.index(goods_id)
            self.exchange_reward_widget.perform_click_small_display_item(idx)
            self.exchange_reward_widget.scroll_exchange_item_list(False)