# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChangeTicket.py
from __future__ import absolute_import
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.comsys.activity.ActivityTemplate import ActivityBase
import logic.gcommon.const as gconst
from logic.gutils import mall_utils
from logic.gcommon.item import item_const
from logic.gutils import jump_to_ui_utils

class ActivityChangeTicket(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityChangeTicket, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self.refresh_panel
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.panel.PlayAnimation('show')
        self.refresh_panel()

        @self.panel.temp_btn.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if player:
                player.exchange_ticket()

        @self.panel.btn_mall.unique_callback()
        def OnClick(btn, touch):
            jump_to_ui_utils.jump_to_mall(i_types=(mall_const.SKIN_ID, mall_const.SKIN_DRIVER_ID))

        @self.panel.btn_lucky.unique_callback()
        def OnClick(btn, touch):
            jump_to_ui_utils.jump_to_mall('50302025')

        @self.panel.btn_change.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(608100), get_text_by_id(608101))

    def refresh_panel(self):
        PIECES = [
         gconst.SHOP_PAYMENT_PIECE1, gconst.SHOP_PAYMENT_PIECE2, gconst.SHOP_PAYMENT_PIECE3, gconst.SHOP_PAYMENT_PIECE4]
        PIECES_ND = [self.panel.lab_num_blue, self.panel.lab_num_puple, self.panel.lab_num_orange, self.panel.lab_num_gold]
        all_num = 0
        for index, piece in enumerate(PIECES):
            p_type = '%d_%d' % (gconst.SHOP_PAYMENT_ITEM, piece)
            piece_nd = PIECES_ND[index]
            money = mall_utils.get_my_money(p_type)
            piece_nd.SetString(' '.join([get_text_by_id(81187), str(money)]))
            num = item_const.EXCHANGE_TICKETS.get(piece, 0)
            all_num += money * num

        self.panel.lab_ticket_num.SetString(str(all_num))
        self.panel.lab_gift.SetString(str(int(round(item_const.EXTRA_EXCHANGE_RATE * all_num))))
        self.panel.temp_btn.SetEnable(bool(all_num))