# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGenericItemDiscount.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import mall_utils, jump_to_ui_utils, activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gutils.template_utils import init_price_view
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

class ActivityGenericItemDiscount(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGenericItemDiscount, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.activity_conf = conf
        ui_data = conf.get('cUiData', {})
        self.task_id = conf.get('cTask', '')
        self._timer = 0
        self._timer_cb = {}
        self.goods_id = ui_data.get('goods_id', '')
        self._mall_conf = confmgr.get('mall_config', self.goods_id, default={})
        self._price_top_widget = None
        return

    def on_init_panel(self):
        self.register_timer()
        self.init_money_widget()
        self.init_btn_buy()
        self.init_btn_goto()
        self.update_widget()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()
        self.activity_conf = None
        self.task_id = None
        self._timer = None
        self._timer_cb = None
        self.goods_id = None
        self._mall_conf = None
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.update_widget,
           'buy_good_success': self.update_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def refresh_time(self):
        if not self.panel or not self.panel.nd_content:
            return
        lab_time = self.panel.nd_content.bar_time.lab_countdown
        left_time = activity_utils.get_left_time(self._activity_type)
        if left_time > 0:
            if left_time > tutil.ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(tutil.get_readable_time(close_left_time))
        if left_time < tutil.ONE_DAY_SECONDS:
            lab_time.SetColor(16776557)
        else:
            lab_time.SetColor(16777215)

    def init_money_widget--- This code section failed: ---

 101       0  LOAD_GLOBAL           0  'PriceUIWidget'
           3  LOAD_GLOBAL           1  'panel'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'panel'
          12  LOAD_ATTR             2  'list_money'
          15  LOAD_CONST            2  'pnl_title'
          18  LOAD_GLOBAL           3  'False'
          21  CALL_FUNCTION_513   513 
          24  LOAD_FAST             0  'self'
          27  STORE_ATTR            4  '_price_top_widget'

 102      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             4  '_price_top_widget'
          36  LOAD_ATTR             5  'show_money_types'
          39  LOAD_GLOBAL           6  'SHOP_PAYMENT_YUANBAO'
          42  BUILD_LIST_1          1 
          45  CALL_FUNCTION_1       1 
          48  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 21

    def init_time_widget(self):
        player = global_data.player
        if not player:
            return
        self._timer_cb[0] = lambda : self.refresh_time()
        self.refresh_time()

    def init_btn_buy(self):
        btn_buy = self.panel.nd_content.btn_buy
        if not self._mall_conf:
            btn_buy.SetEnable(False)
            btn_buy.SetText('******')
            return

        @btn_buy.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_buy()

        self._update_btn_buy()

    def _update_btn_buy(self):
        btn_buy = self.panel.nd_content.btn_buy
        has_bought = mall_utils.limite_pay(self.goods_id)
        if has_bought:
            self.panel.temp_price.setVisible(False)
            btn_buy.SetEnable(False)
            self.panel.lab_got.setVisible(True)
        else:
            btn_buy.SetEnable(True)
            self.panel.lab_got.setVisible(False)
            init_price_view(self.panel.temp_price, self.goods_id, DARK_PRICE_COLOR)

    def init_btn_goto(self):
        self.panel.lab_name.SetString(mall_utils.get_goods_name(self.goods_id))

        @self.panel.nd_content.btn_search.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_goto()

    def on_click_btn_buy(self, *args):
        if self._mall_conf:
            prices = mall_utils.get_mall_item_price(self.goods_id)
            if not prices:
                return
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            real_price = price_info.get('real_price')

            def confirm_callback():
                global_data.player and global_data.player.buy_goods(self.goods_id, 1, goods_payment)

            if mall_utils.check_payment(goods_payment, price_info.get('real_price')):
                SecondConfirmDlg2().confirm(content=get_text_by_id(634879).format(real_price), confirm_callback=confirm_callback)

    def on_click_btn_goto(self, *args):
        jump_to_ui_utils.jump_to_display_detail_by_goods_id(self.goods_id, {'role_info_ui': True})

    def update_widget(self, *args):
        self.init_time_widget()
        self._update_btn_buy()
        global_data.emgr.refresh_activity_redpoint.emit()