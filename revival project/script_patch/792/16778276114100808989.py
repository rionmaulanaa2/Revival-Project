# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryRateUpWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils.template_utils import init_common_item_head, init_tempate_mall_i_item
from logic.gcommon import time_utility
from logic.comsys.common_ui.ButtonGroupHelper import SingleButtonGroupHepler
from logic.gutils.mall_utils import get_lottery_id_list, get_lottery_table_id_list
from logic.gutils.reward_item_ui_utils import process_lottery_probability_up_data

class LotteryRateUpWidget(object):

    def __init__(self, panel, on_click_callback):
        self.panel = panel
        self.single_button_group = None
        self.on_click_callback = on_click_callback
        self._cur_time_span_probability_data = None
        self._rate_up_item_list = []
        self.is_on_show = False
        self.cur_table_id = None
        return

    def get_rate_up_item_list(self):
        return self._rate_up_item_list

    def destroy(self):
        self.panel = None
        if self.single_button_group:
            self.single_button_group.destroy()
            self.single_button_group = None
        self.on_click_callback = None
        return

    def init(self):
        if not self._cur_time_span_probability_data:
            self.panel.nd_rate_up.setVisible(False)
            self.is_on_show = False
            self._rate_up_item_list = []
            return
        self.panel.nd_rate_up.setVisible(True)
        self.is_on_show = True
        start_time, end_time, probability_data = self._cur_time_span_probability_data
        sorted_item_no_list, probability_dict = process_lottery_probability_up_data(self.cur_table_id, probability_data)
        self._rate_up_item_list = sorted_item_no_list
        self.init_reward_list_widget(sorted_item_no_list)
        self.init_count_down_time(end_time)

    def refresh_rate_up_widget(self, table_id):
        cur_tab_id = table_id
        self.cur_table_id = cur_tab_id
        self._cur_time_span_probability_data = global_data.player.get_reward_probability_up_data(cur_tab_id)
        if not self._cur_time_span_probability_data:
            self.panel.nd_rate_up.setVisible(False)
            return
        self.init()

    def init_reward_list_widget(self, sorted_item_no_list):
        reward_count = len(sorted_item_no_list)
        self.panel.list_reward.SetInitCount(reward_count)
        sorted_keys = sorted_item_no_list
        for idx in range(reward_count):
            ui_item = self.panel.list_reward.GetItem(idx)
            if ui_item:
                item_id = sorted_keys[idx]
                self.init_reward_item(ui_item, item_id)

        if not self.single_button_group:
            self.single_button_group = SingleButtonGroupHepler()
        self.single_button_group.selectButton(None)
        btn_list = [ self.panel.list_reward.GetItem(idx).btn_choose for idx in range(reward_count) ]
        self.single_button_group.setButtonList(btn_list, self.on_select_reward_button)
        return

    def on_select_reward_button(self, btn, btn_index, is_choose):
        if btn and btn.isValid():
            btn.SetSelect(is_choose)

    def init_count_down_time(self, end_time):

        def show_count_down():
            now = time_utility.get_server_time()
            seconds = end_time - now
            if seconds < 0:
                if global_data.player:
                    global_data.player.request_reward_display_data(get_lottery_table_id_list())
                return
            text = time_utility.get_readable_time_day_hour_minitue(seconds)
            self.panel.lab_time.SetString(text)
            self.panel.lab_time.DelayCall(5, lambda : show_count_down())

        show_count_down()

    def init_reward_item(self, ui_item, item_id):

        def OnClick():
            if self.single_button_group:
                self.single_button_group.selectButton(ui_item.btn_choose)
            if callable(self.on_click_callback):
                self.on_click_callback(item_id)

        init_tempate_mall_i_item(ui_item, item_id, callback=OnClick)

    def switch_show_item_id(self, show_item_id):
        if not self.single_button_group:
            return
        else:
            if show_item_id in self._rate_up_item_list:
                index = self._rate_up_item_list.index(show_item_id)
                self.single_button_group.selectButtonByIndex(index)
            else:
                self.single_button_group.selectButton(None)
            return