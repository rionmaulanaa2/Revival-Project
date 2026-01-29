# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/PriceUIWidget.py
from __future__ import absolute_import
import logic.gcommon.const as gconst
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gcommon.item import item_const
PAYMENT_MEOW_COIN = '{}_{}'.format(gconst.SHOP_PAYMENT_ITEM, item_const.LOBBY_ITEM_NO_MEOW_COIN)

class PriceUIWidget(object):

    def __init__(self, parent, call_back=None, list_money_node=None, pnl_title=True, hide_jump_payments=None):
        self.parent = parent
        self.panel = parent.panel
        if not list_money_node:
            self.list_money = self.panel.top.list_money
        else:
            self.list_money = list_money_node
        self.callback = call_back
        self.hide_jump_payments = set() if hide_jump_payments is None else hide_jump_payments
        self.init_parameters()
        self.init_event()
        if pnl_title:
            self.init_panel_title()
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.parent = None
        self.panel = None
        self.callback = None
        self.exchange_callback_dict = {}
        return

    def destroy(self):
        self.on_finalize_panel()

    def init_parameters(self):
        self.yuanbao_red_img = None
        self.last_money_types = []
        self.money_types = []
        self.lottery_id = None
        self.lottery_ticket_item_id = None
        self.lottery_ticket_goods_id = None
        self.exchange_dict = {}
        self.exchange_callback_dict = {}
        return

    def init_event(self):
        self.process_event(True)

    def init_panel_title(self):
        if self.callback:
            template_utils.init_common_pnl_title(self.panel.top, call_back=self.callback)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self._on_player_info_update,
           'buy_good_success': self.refresh_red_point,
           'update_weekly_card_info': self.refresh_red_point,
           'update_month_card_info': self.refresh_red_point,
           'receive_task_reward_succ_event': self.refresh_red_point,
           'refresh_activity_redpoint': self.refresh_red_point,
           'receive_task_prog_reward_succ_event': self.refresh_red_point,
           'task_prog_changed': self.refresh_red_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_close_btn_visible(self, visible):
        if self.callback and self.panel.top:
            self.panel.top.btn_back.setVisible(visible)

    def set_exchange_item_dict(self, exchange_dict):
        self.exchange_dict = exchange_dict

    def set_exchange_callback_dict(self, exchange_callback_dict):
        self.exchange_callback_dict = exchange_callback_dict

    def refresh_red_point(self, *args):
        if not self.yuanbao_red_img or self.yuanbao_red_img.IsDestroyed() or not global_data.player:
            return
        self.yuanbao_red_img.setVisible(mall_utils.refresh_charge_red_point())

    def refresh_lottery_ticket(self, lottery_id):
        self.lottery_id = lottery_id
        self.lottery_ticket_item_id, self.lottery_ticket_goods_id = mall_utils.get_lottery_ticket(lottery_id)

    def show_money_types(self, money_types):
        if money_types == self.last_money_types:
            return
        self.money_types = money_types
        self.list_money.DeleteAllSubItem()
        self._on_player_info_update()
        self.last_money_types = money_types

    def _on_player_info_update(self, *args):
        if global_data.ui_mgr.get_ui('ScreenLockerUI'):
            return
        else:
            if not self.money_types:
                return
            if not self.list_money or self.list_money.IsDestroyed() or not global_data.player:
                return
            self.yuanbao_red_img = None
            list_money = self.list_money
            list_money.SetInitCount(len(self.money_types))
            off_num = len(self.money_types) - len(self.last_money_types)
            for i, m_type in enumerate(self.money_types):
                money_node = list_money.GetItem(i)
                money_node.setLocalZOrder(len(self.money_types) - i)
                if i - off_num < 0:
                    money_node.PlayAnimation('change')
                elif m_type != self.last_money_types[i - off_num]:
                    money_node.PlayAnimation('change')
                money = mall_utils.get_my_money(m_type)
                show = False
                item_no = mall_utils.get_payment_item_no(m_type)
                if item_no == gconst.SHOP_ITEM_YUANBAO:
                    extra_info = {'show_yuanbao': True}
                else:
                    extra_info = {}
                extra_info['show_jump'] = m_type not in self.hide_jump_payments

                @money_node.unique_callback()
                def OnClick(btn, touch, item_no=item_no, extra_info=extra_info):
                    wpos = touch.getLocation()
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=wpos, extra_info=extra_info)
                    return

                if item_no == gconst.SHOP_ITEM_YUANBAO:
                    if self.parent and self.parent.__class__.__name__ == 'ChargeUINew':
                        pass
                    else:
                        self.yuanbao_red_img = money_node.img_red
                        show = True

                        @money_node.btn_add.unique_callback()
                        def OnClick(btn, touch):
                            from logic.comsys.charge_ui.ChargeUINew import ChargeUINew, ACTIVITY_CHARGE_TYPE
                            ui = global_data.ui_mgr.get_ui('ChargeUINew')
                            if not ui:
                                ui = ChargeUINew(None, ACTIVITY_CHARGE_TYPE)
                            ui.switch_to_activity_page(ACTIVITY_CHARGE_TYPE)
                            return

                elif item_no == gconst.SHOP_ITEM_DIAMON:
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
                        ExchangeUI()

                elif item_no == gconst.SHOP_PAYMENT_LOTTERT_POINTS:
                    from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
                    from logic.client.const import mall_const
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        ExchangeUI(from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=gconst.LOTTERY_POINTS, buy_goods_id=mall_const.MALL_LOTTERY_POINTS_GIFT)

                elif item_no == gconst.SHOP_ITEM_DEC_COIN:
                    show = True
                    from logic.client.const import mall_const

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
                        ExchangeUI(from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=gconst.DEC_COIN_TICKET, buy_goods_id=mall_const.DEC_COIN_GIFT, keyboard_for_from_payment=False)

                elif item_no == item_const.LOBBY_ITEM_NO_MEOW_COIN:
                    from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
                    from logic.client.const import mall_const
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        ExchangeUI(from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=PAYMENT_MEOW_COIN, buy_goods_id=mall_const.MEOW_COIN_GIFT)

                elif item_no == self.lottery_ticket_item_id:
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        from logic.comsys.mall_ui.LotteryTicketBuyConfirmUI import LotteryTicketBuyConfirmUI
                        LotteryTicketBuyConfirmUI(goods_id=self.lottery_ticket_goods_id, lottery_id=self.lottery_id)

                elif item_no in self.exchange_dict:
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch, item_no=item_no):
                        from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
                        GroceriesBuyConfirmUI(goods_id=self.exchange_dict[item_no], need_show=item_const.ITEM_SHOW_TYPE_ITEM)

                elif item_no == item_const.ITEM_NO_PVE_KEY:
                    show = False if self.parent.get_name() == 'PVEKeyBuyUI' else True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVEKeyBuyUI import PVEKeyBuyUI
                        PVEKeyBuyUI()

                elif item_no == gconst.SHOP_PAYMENT_PVE_COIN:
                    from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
                    from logic.client.const import mall_const
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        ExchangeUI(from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=gconst.SHOP_PAYMENT_ITEM_PVE_COIN, buy_goods_id=mall_const.PVE_ITEM_DIAMOND_GIFT)

                elif item_no == gconst.SHOP_PAYMENT_SEASON_PREMIUM_EXCHANGE:
                    from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
                    from logic.client.const import mall_const
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch):
                        ExchangeUI(from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=gconst.SHOP_PAYMENT_ITEM_SEASON_PREMIUM_EXCHANGE, buy_goods_id=mall_const.SEASON_PREMIUM_EXCHANGE_ITEM_DIAMOND_GIFT, keyboard_for_from_payment=False)

                elif item_no in self.exchange_callback_dict:
                    show = True

                    @money_node.btn_add.unique_callback()
                    def OnClick(btn, touch, item_no=item_no):
                        cb = self.exchange_callback_dict[item_no]
                        if callable(cb):
                            cb(item_no)
                        else:
                            log_error('invalid exchange callback: ', item_no)

                money_node.btn_add.setVisible(show)
                template_utils.init_common_price(money_node, money, m_type)

            list_money._refreshItemPos(is_cal_scale=True)
            self.refresh_red_point()
            return