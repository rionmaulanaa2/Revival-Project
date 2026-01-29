# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNormalWidget.py
from __future__ import absolute_import
from logic.gutils.mall_utils import limite_pay
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import ONE_DAY_SECONDS, ONE_MINUTE_SECONDS, ONE_HOUR_SECONS, get_now_struct_time, cal_hms_from_s
from common.utils.timer import CLOCK, RELEASE
from common.platform.dctool.interface import is_tw_package
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryPreviewWidget import LotteryPreviewWidget
from .LotteryBuyWidget import LotteryBuyWidget
from random import randint

class LotteryNormalWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryNormalWidget, self).init_parameters()
        self.has_used_free_lottery = False
        self.free_lottery_count_down = 0
        self.free_lottery_timer = None
        self.show_model_index = randint(0, self.data['core_reward_count'] - 1)
        self.show_model_id = self.data['core_item_id_list'][self.show_model_index]
        self.preview_widget = None
        return

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended
           }
        return econf

    def init_panel(self):
        super(LotteryNormalWidget, self).init_panel()

        @global_unique_click(self.panel.btn_view)
        def OnClick(*args):
            self.preview_widget.show()

        @global_unique_click(self.panel.temp_review.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        self._init_preview_widget()
        self._init_buy_widget()
        self.panel.nd_show.lab_tw.setVisible(is_tw_package())
        self.panel.nd_tips.setVisible(False)
        self.panel.lab_tips.SetString(12093)

    def _init_preview_widget(self):

        def show_callback():
            self.refresh_preview()
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def close_callback():
            self.refresh_show_model()
            global_data.emgr.refresh_switch_core_model_button_visible.emit(True)

        self.preview_widget = LotteryPreviewWidget(self.panel.temp_review, self.panel, self.lottery_id, self.on_change_show_reward, show_callback=show_callback, close_callback=close_callback)

    def _init_buy_widget(self):

        def buying_callback(lottery_count):
            self.preview_widget.hide()
            self.panel.PlayAnimation('begin')

        def lottery_data_ready_callback(bought_successfully):

            def callback():
                self.panel.StopAnimation('begin')
                self.panel.PlayAnimation('end')

            delay_time = 2.0 if bought_successfully else 0.0
            self.panel.DelayCall(delay_time, callback)

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buying_callback=buying_callback, lottery_data_ready_callback=lottery_data_ready_callback)
        self.has_used_free_lottery = limite_pay(self.data['free_single_goods_id'])

    def show(self):
        self.panel.setVisible(True)
        self.panel.PlayAnimation('change')
        self.panel.StopAnimation('begin')
        self.panel.PlayAnimation('end')
        self.preview_widget.parent_show()

    def hide(self):
        self.panel.setVisible(False)
        self.preview_widget.parent_hide()
        if self.free_lottery_timer:
            global_data.game_mgr.unregister_logic_timer(self.free_lottery_timer)
            self.free_lottery_timer = None
        return

    def on_finalize_panel(self):
        super(LotteryNormalWidget, self).on_finalize_panel()
        self.destroy_widget('preview_widget')
        self.destroy_widget('buy_widget')
        if self.free_lottery_timer:
            global_data.game_mgr.unregister_logic_timer(self.free_lottery_timer)
            self.free_lottery_timer = None
        return

    def refresh(self):
        self.buy_widget.refresh()
        self.refresh_free_lottery_chance()
        self.refresh_lottery_limit_count()

    def on_lottery_ended(self):
        self.refresh_free_lottery_chance()

    def refresh_free_lottery_chance(self):
        self.has_used_free_lottery = limite_pay(self.data['free_single_goods_id'])
        if self.has_used_free_lottery:
            cur_time = get_now_struct_time()
            h = cur_time.tm_hour
            m = cur_time.tm_min
            s = cur_time.tm_sec
            self.free_lottery_count_down = ONE_DAY_SECONDS - h * ONE_HOUR_SECONS - m * ONE_MINUTE_SECONDS - s
            h, m, s = cal_hms_from_s(self.free_lottery_count_down)
            self.panel.lab_free_time.setVisible(True)
            self.panel.lab_free_time.SetString('%02d:%02d:%02d' % (h, m, s))
            if self.free_lottery_timer:
                global_data.game_mgr.unregister_logic_timer(self.free_lottery_timer)
                self.free_lottery_timer = None
            self.free_lottery_timer = global_data.game_mgr.register_logic_timer(self._count_down, interval=1, times=-1, mode=CLOCK)
        else:
            if self.free_lottery_timer:
                global_data.game_mgr.unregister_logic_timer(self.free_lottery_timer)
                self.free_lottery_timer = None
            self.panel.lab_free_time.setVisible(False)
        return

    def refresh_preview(self):
        self.preview_widget.refresh_preview_list(self.lottery_id, self.data.get('limited_item_id_list', None), self.data.get('percent_up_item_id_dict', {}))
        return

    def _count_down(self):
        self.free_lottery_count_down -= 1
        if self.free_lottery_count_down <= 0:
            self.has_used_free_lottery = limite_pay(self.data['free_single_goods_id'])
            if not self.has_used_free_lottery:
                self.free_lottery_timer = None
                self.panel.lab_free_time.setVisible(False)
                self.buy_widget.refresh_lottery_price()
                return RELEASE
            self.free_lottery_count_down = 0
        _h, _m, _s = cal_hms_from_s(self.free_lottery_count_down)
        self.panel.lab_free_time.SetString('%02d:%02d:%02d' % (_h, _m, _s))
        return

    def refresh_show_model(self, show_model_id=None):
        if self.panel and self.panel.isValid():
            self._update_show_model_id_and_index(show_model_id)
            self.on_change_show_reward(self.show_model_id)

    def switch_show_model(self, offset):
        self.show_model_index = (self.show_model_index + self.data['core_reward_count'] + offset) % self.data['core_reward_count']
        self.show_model_id = self.data['core_item_id_list'][self.show_model_index]
        self.on_change_show_reward(self.show_model_id)

    def _update_show_model_id_and_index(self, force_show_model_id):
        if force_show_model_id is not None:
            if force_show_model_id in self.data['core_item_id_list']:
                self.show_model_id = force_show_model_id
        index = self.data['core_item_id_list'].index(self.show_model_id)
        self.show_model_index = index
        return

    def hide_preview_widget--- This code section failed: ---

 174       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  JUMP_IF_FALSE_OR_POP    27  'to 27'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'preview_widget'
          21  LOAD_ATTR             3  'hide'
          24  CALL_FUNCTION_0       0 
        27_0  COME_FROM                '12'
          27  POP_TOP          
          28  LOAD_CONST            0  ''
          31  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9