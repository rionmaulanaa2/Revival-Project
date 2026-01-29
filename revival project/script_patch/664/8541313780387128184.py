# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyBatchBagRecycleUI.py
from __future__ import absolute_import
from six.moves import filter
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item, get_recycle_item_price_tips
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from .LobbyBagRecycleUI import RecyclePriceWidget
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gcommon.time_utility import get_server_time

class BatchRecycleItem(object):

    def __init__(self, panel):
        self.panel = panel
        self.item_data = {}
        self.index = None
        self.is_choose = False
        self.num_callback = None
        self._recycle_btn_widget = ItemNumBtnWidget(self.panel.temp_input_quantity)
        return

    def init_item(self, item_data, is_choose, index, item_num, num_callback, choose_callback):
        self.item_data = item_data
        self.index = index
        self.set_choose(is_choose)
        self.num_callback = num_callback
        self._recycle_btn_widget.init_item(self.item_data, self.on_num_changed, item_num)
        quantity = self.item_data.get('quantity', 1)
        self.panel.temp_input_quantity.lab_num.SetString(str(item_num) + '/' + str(quantity))
        ui_item = self.panel
        init_lobby_bag_item(self.panel.temp_head, item_data)
        item_no = item_data.get('item_no', None)
        self.panel.lab_name.SetString(get_lobby_item_name(item_no))

        @ui_item.temp_choose.btn.callback()
        def OnClick(btn, touch):
            if callable(choose_callback):
                self.set_choose(not self.is_choose)
                choose_callback(index, self.is_choose)

        return

    def set_selected_num(self, num):
        if self._recycle_btn_widget:
            self._recycle_btn_widget.set_num(num)

    def set_choose(self, is_choose):
        self.is_choose = is_choose
        self.panel.temp_choose.choose.setVisible(is_choose)

    def on_num_changed(self, item_data, num):
        if callable(self.num_callback):
            self.num_callback(self.index, num)
        quantity = self.item_data.get('quantity', 1)
        self.panel.temp_input_quantity.lab_num.SetString(str(num) + '/' + str(quantity))

    def destroy(self):
        self._recycle_btn_widget.destroy()
        self._recycle_btn_widget = None
        self.num_callback = None
        self.panel = None
        self.item_data = {}
        self.index = None
        return


class LobbyBatchBagRecycleUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'bag/bag_batch_recycle'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bar'
    UI_ACTION_EVENT = {'btn_recycle.btn_common.OnClick': 'on_click_recycle_btn',
       'temp_choose_all.btn.OnClick': 'on_click_select_all_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        super(LobbyBatchBagRecycleUI, self).on_init_panel()
        self.item_data_list = []
        self.item_data_choose_list = []
        self.item_data_num_list = []
        self.item_data_widget_list = []
        self.init_scroll_view()
        self.recyclePriceWidget = RecyclePriceWidget(self.panel)

    def init_scroll_view(self):

        @self.panel.list_item.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.init_bag_item_helper(ui_item, idx)

    def init_bag_item_helper(self, ui_item, idx):
        ui_item.img_bg.setVisible(idx % 2 == 0)
        if idx < len(self.item_data_list):
            item_data = self.item_data_list[idx]
            is_choose = self.item_data_choose_list[idx]
            widget = self.item_data_widget_list[idx]
            item_num = self.item_data_num_list[idx]
            if not widget:
                widget = BatchRecycleItem(ui_item)
                self.item_data_widget_list[idx] = widget
                widget.init_item(item_data, is_choose, idx, item_num, self.on_num_changed, self.on_choose_changed)
        else:
            log_error('idx out of range!!!', idx, len(self._bag_items))

    def on_num_changed(self, index, num):
        if index < len(self.item_data_num_list):
            if self.item_data_num_list[index] != num:
                self.item_data_num_list[index] = num
                self.update_all_choose_show()
                self.update_price_show()

    def on_choose_changed(self, index, is_choose):
        if index < len(self.item_data_choose_list):
            self.item_data_choose_list[index] = is_choose
        self.update_all_choose_show()
        self.update_price_show()

    def on_finalize_panel(self):
        self.destroy_widget('recyclePriceWidget')

    def on_click_close_ui(self, *args):
        self.close()

    def on_click_recycle_btn(self, btn, touch):
        if not self.item_data_list:
            global_data.game_mgr.show_tip(get_text_local_content(80824))
            return

        def confirm_callback():
            if global_data.player:
                _, _item_ids, _item_nums = self.get_sel_items()
                item_dict = {}
                for idx, iid in enumerate(_item_ids):
                    item_dict[iid] = _item_nums[idx]

                global_data.player.recycle_items(item_dict)
                self.close()

        _, _item_ids, _item_nums = self.get_sel_items()
        if sum(_item_nums) <= 0:
            global_data.game_mgr.show_tip(get_text_local_content(80779))
            return
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        coin_list_str = get_recycle_item_price_tips(self._price_dict)
        SecondConfirmDlg2().confirm(content=get_text_local_content(80777).format(coin_list=coin_list_str), confirm_callback=confirm_callback)

    def init_recycle_list_item(self, item_data_list):
        item_data_list = self.get_recyclable_item_list(item_data_list)
        if item_data_list:
            self.item_data_list = item_data_list
            self.item_data_choose_list = [ False for i in item_data_list ]
            self.item_data_num_list = [ 1 for i in item_data_list ]
            self.item_data_widget_list = [ None for i in item_data_list ]
            self.item_data_max_num_list = [ item_data.get('quantity', 1) for item_data in item_data_list ]
            self.set_all_choose(False)
            self.update_price_show()
            self.panel.list_item.SetInitCount(0)
            self.panel.list_item.SetInitCount(len(item_data_list))
            self.panel.img_empty.setVisible(False)
            self.panel.btn_recycle.btn_common.SetShowEnable(True)
        else:
            self.panel.list_item.SetInitCount(0)
            self.panel.img_empty.setVisible(True)
            self.recyclePriceWidget.show_empty_price()
            self.panel.btn_recycle.btn_common.SetShowEnable(False)
        return

    def get_recyclable_item_list(self, item_data_list):

        def filter_recycle(item_data):
            item_no = item_data.get('item_no', None)
            item_conf = confmgr.get('lobby_item', str(item_no), default={})
            recyle_gain_item = item_conf.get('recyle_gain_item', [])
            recyclable = True if recyle_gain_item and get_server_time() >= item_conf.get('recycle_begin_time', 0) else False
            return recyclable

        item_list = list(filter(filter_recycle, item_data_list))
        return item_list

    def update_button_show(self):
        pass

    def on_click_select_all_btn(self, btn, touch):
        if not self.item_data_list:
            return
        is_all_choose = all(self.item_data_choose_list) and self.item_data_max_num_list == self.item_data_num_list
        self.set_all_choose(not is_all_choose)
        self.update_price_show()

    def update_all_choose_show(self):
        is_all_choose = all(self.item_data_choose_list) and self.item_data_max_num_list == self.item_data_num_list
        self.panel.temp_choose_all.choose.setVisible(is_all_choose)

    def update_price_show(self):
        _item_nos, _, _item_nums = self.get_sel_items()
        self._price_dict = self.recyclePriceWidget.set_price(_item_nos, _item_nums)

    def set_all_choose(self, is_choose):
        self.item_data_choose_list = [ is_choose for i in self.item_data_list ]
        self.item_data_num_list = [ num for num in self.item_data_max_num_list ]
        for idx, widget in enumerate(self.item_data_widget_list):
            if widget:
                widget.set_choose(is_choose)
                if idx < len(self.item_data_max_num_list):
                    max_num = self.item_data_max_num_list[idx]
                    widget.set_selected_num(max_num)

        self.panel.temp_choose_all.choose.setVisible(is_choose)

    def get_sel_items(self):
        _item_nos = []
        _item_ids = []
        _item_nums = []
        for idx, is_choose in enumerate(self.item_data_choose_list):
            if is_choose:
                item_conf = self.item_data_list[idx]
                item_no = item_conf.get('item_no', None)
                if item_no:
                    item_id = item_conf.get('id', None)
                    _item_nos.append(item_no)
                    _item_ids.append(item_id)
                    num = self.item_data_num_list[idx]
                    _item_nums.append(num)

        return (
         _item_nos, _item_ids, _item_nums)