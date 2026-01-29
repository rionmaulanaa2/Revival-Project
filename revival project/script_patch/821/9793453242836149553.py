# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySummerWidget.py
from __future__ import absolute_import
from .LotteryCommonTurntableWidget import LotteryCommonTurntableWidget
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.mall_utils import limite_pay
from logic.gutils.jump_to_ui_utils import jump_to_activity
from logic.gutils.activity_utils import check_out_of_date
from logic.gcommon.common_const.activity_const import ACTIVITY_SUMMER_BUY
PIC_MAP = {201001153: 'gui/ui_res_2/activity/activity_202107/summer_lottery/icon_lottery_ningning.png',
   201001550: 'gui/ui_res_2/activity/activity_202107/summer_lottery/icon_lottery_mila.png',
   201001445: 'gui/ui_res_2/activity/activity_202107/summer_lottery/icon_lottery_ivan.png'
   }
ACTIVITY_ITEM = '694000011'

class LotterySummerWidget(LotteryCommonTurntableWidget):

    def init_panel(self):
        super(LotterySummerWidget, self).init_panel()

        @global_unique_click(self.panel.btn_get)
        def OnClick(*args):
            if limite_pay(ACTIVITY_ITEM) or check_out_of_date(ACTIVITY_SUMMER_BUY):
                self.panel.btn_get.setVisible(False)
                return
            jump_to_activity(ACTIVITY_SUMMER_BUY)

        self.panel.img_role.SetDisplayFrameByPath('', PIC_MAP[self.show_model_id])
        self.update_activity_btn_visible()
        self.update_exchange_coin()
        self.update_lucky_info()

    def on_lottery_ended(self):
        super(LotterySummerWidget, self).on_lottery_ended()
        self.update_activity_btn_visible()
        self.update_exchange_coin()

    def switch_show_model(self, offset, is_auto=False):
        super(LotterySummerWidget, self).switch_show_model(offset, is_auto)
        self.panel.img_role.SetDisplayFrameByPath('', PIC_MAP[self.show_model_id])

    def update_exchange_coin(self):
        self.panel.list_item.GetItem(0).lab_num.SetString(str(global_data.player.get_item_money(50101215)))
        self.panel.list_item.GetItem(1).lab_num.SetString(str(global_data.player.get_item_money(50101214)))

    def update_activity_btn_visible(self):
        self.panel.btn_get.setVisible(not (limite_pay(ACTIVITY_ITEM) or check_out_of_date(ACTIVITY_SUMMER_BUY)))

    def update_remind_exchange_item_id(self):
        super(LotterySummerWidget, self).update_remind_exchange_item_id()
        self.update_exchange_coin()