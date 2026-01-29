# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryScratchItemWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_const.activity_const import CARD_WIDTH, CARD_HEIGHT, MAX_SELECT_NUM
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gutils.template_utils import splice_price
from logic.client.const.mall_const import DEF_PRICE_COLOR
from .LotteryBuyWidget import LotteryBuyWidget
PRICE_COLOR = [
 '#SK', '#SR', '#DC']
STATE_CLOSE_PIC = 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/icon_jojo_scrawl_confirm_0.png'
STATE_SCRATCH_PIC = 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/icon_jojo_scrawl_confirm_2.png'
STATE_OPEN_PIC = 'gui/ui_res_2/activity/activity_202211/jojo_scrawl/icon_jojo_scrawl_confirm_3.png'

class LotteryScratchItemWidget(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202211/jojo_scrawl/open_jojo_scrawl_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, main_widget, lottery_id, scratch_select_list, scratch_open_list, half_single_get_price, get_price, half_single_buy_logic, buy_logic, close_cb=None, confirm_cb=None):
        self.main_widget = main_widget
        self.lottery_id = lottery_id
        self.card_sum = CARD_HEIGHT * CARD_WIDTH
        self.scratch_select_list = scratch_select_list
        self.scratch_open_list = scratch_open_list
        self.half_single_get_price = half_single_get_price
        self.get_price = get_price
        self.half_single_buy_logic = half_single_buy_logic
        self.buy_logic = buy_logic
        self.close_cb = close_cb
        self.confirm_cb = confirm_cb
        self.init_panel()

    def init_panel(self):
        self.panel.list_icon.BindMethod('OnCreateItem', self.create_scratch_item)
        self.panel.list_icon.DeleteAllSubItem()
        self.panel.list_icon.SetInitCount(self.card_sum)
        self.panel.list_icon.scroll_Load()
        self.panel.btn_cancel.BindMethod('OnClick', self.on_click_btn_close)
        self.panel.btn_confirm.BindMethod('OnClick', self.on_click_btn_confirm)
        self.panel.btn_close.BindMethod('OnClick', self.on_click_btn_close)
        self.panel.lab_num.SetString(get_text_by_id(633841).format(len(self.scratch_select_list)))
        self.panel.lab_cost.SetString(get_text_by_id(633842))
        self.lottery_buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={CONTINUAL_LOTTERY_COUNT: self.panel.btn_confirm
           }, buy_price_info={CONTINUAL_LOTTERY_COUNT: self.panel.temp_prcie
           }, price_color=PRICE_COLOR, special_buy_logic_func=self.special_buy_logic, get_special_price_info=self.get_special_buy_price)

    def special_buy_logic(self, price_info, lottery_count):
        if self.half_single_buy_logic and self.buy_logic and self.main_widget and self.main_widget.get_is_visible():
            if len(self.scratch_select_list) == 1 and self.half_single_buy_logic(self.scratch_select_list):
                pass
            else:
                self.buy_logic(len(self.scratch_select_list), select_list=self.scratch_select_list)
        self.on_click_btn_confirm()
        return True

    def get_special_buy_price(self, price_info, lottery_count):
        if len(self.scratch_select_list) == 1:
            return self.half_single_get_price
        return self.get_price(len(self.scratch_select_list))

    def create_scratch_item(self, lv, idx, item):
        if str(idx) in self.scratch_select_list:
            item.icon.SetDisplayFrameByPath('', STATE_SCRATCH_PIC)
        elif str(idx) in self.scratch_open_list:
            item.icon.SetDisplayFrameByPath('', STATE_OPEN_PIC)
            item.icon_tick.setVisible(True)
        else:
            item.icon.SetDisplayFrameByPath('', STATE_CLOSE_PIC)

    def on_finalize_panel(self):
        if self.lottery_buy_widget:
            self.lottery_buy_widget.destroy()
        super(LotteryScratchItemWidget, self).on_finalize_panel()

    def on_click_btn_close(self, *args):
        self.close()

    def on_click_btn_confirm(self, *args):
        if self.confirm_cb:
            self.confirm_cb()
        self.close()

    def close(self, *args):
        if self.close_cb:
            self.close_cb()
        super(LotteryScratchItemWidget, self).close(*args)