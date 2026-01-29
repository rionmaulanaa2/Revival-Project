# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyBagUI.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item, get_lobby_item_usage, try_use_lobby_item, get_lobby_item_use_type, get_lobby_item_type
from common.cfg import confmgr
from logic.gcommon.item import item_sorter
from logic.gutils import mall_utils
from logic.gutils import item_utils
from data.season_update_config import MONEY_DICT
from common.const import uiconst
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_PRODUCT

class LobbyBagUI(BasePanel):
    MIN_SHOW_NUM = 25
    PANEL_CONFIG_NAME = 'bag/bag_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn',
       'btn_batch_recycle.OnClick': 'on_click_batch_recycle_btn',
       'btn_preview.OnClick': 'on_click_btn_preview'
       }
    GLOBAL_EVENT = {'on_lobby_bag_item_changed_event': 'need_update_list_show'
       }

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        self._bag_items = []
        self._bag_show_items = []
        self._show_type_filter = None
        self.init_left_tab_list()
        self.cur_tab_index = 0
        self.left_tab_list.set_tab_selected(self.cur_tab_index)
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('common/bg_full_screen_bg', BG_ZORDER)
        self.get_bg_ui() and self.get_bg_ui().img_right.setVisible(False)
        self.init_widget()
        self.init_scroll_view()
        self.init_bag_item_detail_panel()
        self._selected_item = None
        self._selected_item_id = None
        self._selected_item_no = None
        self.init_data()
        return

    def get_bg_ui(self):
        if self.bg_ui and self.bg_ui.is_valid():
            return self.bg_ui

    def do_hide_panel(self):
        super(LobbyBagUI, self).do_hide_panel()
        self.get_bg_ui() and self.get_bg_ui().hide()

    def do_show_panel(self):
        super(LobbyBagUI, self).do_show_panel()
        self.get_bg_ui() and self.get_bg_ui().show()

    def on_finalize_panel(self):
        self.get_bg_ui() and self.get_bg_ui().close()
        self.show_main_ui()
        if self.price_top_widget:
            self.price_top_widget.on_finalize_panel()
            self.price_top_widget = None
        if self.left_tab_list:
            self.left_tab_list.destroy()
            self.left_tab_list = None
        return

    def init_widget(self):

        def close(*args):
            self.on_before_close(self.close)

        from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
        self.price_top_widget = PriceUIWidget(self, pnl_title=False, call_back=close)
        self.price_top_widget.show_money_types(mall_utils.get_mall_default_money_types())

    def init_test_data(self):
        item_conf = confmgr.get('lobby_item', default={})
        item_nos = [
         502001001,
         502001011,
         502001012,
         502001013,
         502001021,
         502001022,
         502001023,
         502001031,
         502001032,
         502001033]
        import random
        sel_item_nos = item_nos
        test_data = []
        for i_no in sel_item_nos:
            test_data.append({'item_no': i_no,'quantity': random.randint(1, 999)})

        self.on_set_bag_items(test_data)

    def init_data(self):
        if not global_data.player:
            return []
        from logic.gcommon.item.lobby_item_type import ITEM_TYPE_KNAPSACK
        items = global_data.player.get_items_by_type_list(ITEM_TYPE_KNAPSACK)
        items.sort(key=cmp_to_key(item_sorter.cmp_sort_key))
        item_datas = []
        for it in items:
            if it.item_no != 50101008:
                item_datas.append({'id': it.id,
                   'item_no': it.item_no,
                   'quantity': it.get_current_stack_num()
                   })

        self.on_set_bag_items(item_datas)

    def on_set_bag_items(self, data_list):

        def my_cmp--- This code section failed: ---

 132       0  LOAD_GLOBAL           0  'get_lobby_item_type'
           3  LOAD_GLOBAL           1  'L_ITEM_TYPE_PRODUCT'
           6  BINARY_SUBSCR    
           7  CALL_FUNCTION_1       1 
          10  LOAD_GLOBAL           1  'L_ITEM_TYPE_PRODUCT'
          13  COMPARE_OP            2  '=='
          16  STORE_FAST            2  'use_type_x'

 133      19  LOAD_GLOBAL           0  'get_lobby_item_type'
          22  LOAD_FAST             1  'y'
          25  LOAD_CONST            1  'item_no'
          28  BINARY_SUBSCR    
          29  CALL_FUNCTION_1       1 
          32  LOAD_GLOBAL           1  'L_ITEM_TYPE_PRODUCT'
          35  COMPARE_OP            2  '=='
          38  STORE_FAST            3  'use_type_y'

 134      41  LOAD_FAST             2  'use_type_x'
          44  LOAD_FAST             3  'use_type_y'
          47  COMPARE_OP            2  '=='
          50  POP_JUMP_IF_FALSE   137  'to 137'

 135      53  LOAD_GLOBAL           2  'item_utils'
          56  LOAD_ATTR             3  'get_item_rare_degree'
          59  LOAD_ATTR             1  'L_ITEM_TYPE_PRODUCT'
          62  BINARY_SUBSCR    
          63  CALL_FUNCTION_1       1 
          66  STORE_FAST            4  'rare_degree_x'

 136      69  LOAD_GLOBAL           2  'item_utils'
          72  LOAD_ATTR             3  'get_item_rare_degree'
          75  LOAD_FAST             1  'y'
          78  LOAD_CONST            1  'item_no'
          81  BINARY_SUBSCR    
          82  CALL_FUNCTION_1       1 
          85  STORE_FAST            5  'rare_degree_y'

 137      88  LOAD_FAST             4  'rare_degree_x'
          91  LOAD_FAST             5  'rare_degree_y'
          94  COMPARE_OP            2  '=='
          97  POP_JUMP_IF_FALSE   121  'to 121'

 138     100  LOAD_GLOBAL           4  'six_ex'
         103  LOAD_ATTR             5  'compare'
         106  LOAD_ATTR             1  'L_ITEM_TYPE_PRODUCT'
         109  BINARY_SUBSCR    
         110  LOAD_FAST             1  'y'
         113  LOAD_CONST            1  'item_no'
         116  BINARY_SUBSCR    
         117  CALL_FUNCTION_2       2 
         120  RETURN_END_IF    
       121_0  COME_FROM                '97'

 139     121  LOAD_GLOBAL           4  'six_ex'
         124  LOAD_ATTR             5  'compare'
         127  LOAD_FAST             5  'rare_degree_y'
         130  LOAD_FAST             4  'rare_degree_x'
         133  CALL_FUNCTION_2       2 
         136  RETURN_END_IF    
       137_0  COME_FROM                '50'

 141     137  LOAD_GLOBAL           4  'six_ex'
         140  LOAD_ATTR             5  'compare'
         143  LOAD_FAST             3  'use_type_y'
         146  LOAD_FAST             2  'use_type_x'
         149  CALL_FUNCTION_2       2 
         152  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 7

        data_list.sort(key=cmp_to_key(my_cmp))
        if self._bag_items == data_list:
            if len(self._bag_items) == 0 and self.panel.list_item.GetItemCount() < self.MIN_SHOW_NUM:
                self.update_show()
            return
        self._bag_items = data_list
        self.update_show()

    def update_show(self):
        new_data_list = self.get_show_list(self._bag_items)
        self.on_update_item_list(new_data_list)

    def get_show_list(self, data_list):
        if self._show_type_filter is None:
            return data_list
        else:
            new_data_list = []
            for item_data in self._bag_items:
                item_no = item_data.get('item_no', None)
                iType = confmgr.get('lobby_item', str(item_no), default={}).get('type', None)
                if iType in self._show_type_filter:
                    new_data_list.append(item_data)

            return new_data_list
            return

    def on_update_item_list(self, data_list):
        self._bag_show_items = data_list
        selected_data = {}
        for data in data_list:
            it_id = data.get('id', None)
            if self._selected_item_id == it_id:
                selected_data = data

        if selected_data:
            self.show_item_desc_info(selected_data)
        else:
            self._selected_item_id = None
            self.show_item_desc_info({})
        self.set_ui_item_selected(None)
        cur_all_item = self.panel.list_item.GetAllItem()
        for idx, ui_item in enumerate(cur_all_item):
            if ui_item and type(ui_item) not in (dict, six.text_type, str):
                self.init_bag_item_helper(ui_item, idx)

        self.panel.list_item.SetInitCount(max(len(data_list), self.MIN_SHOW_NUM))
        self.panel.list_item.scroll_Load()
        self.panel.list_item._refreshItemPos()
        return

    def init_scroll_view(self):

        @self.panel.list_item.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.init_bag_item_helper(ui_item, idx)

    def init_tab_data(self):
        self.tab_list = [{'text': 12013,'sec_text': '','type': None}]
        lobby_item_type_conf = confmgr.get('lobby_item_type')
        name_to_tab_index_dict = {}
        types = sorted(six_ex.keys(lobby_item_type_conf), key=lambda x: int(x))
        for ty in types:
            conf = lobby_item_type_conf[ty]
            cShowInBag = conf.get('cShowInBag', False)
            cBagTabName = conf.get('cBagTabName', '')
            if cShowInBag:
                main, sub = cShowInBag, ''
                if cBagTabName not in name_to_tab_index_dict:
                    self.tab_list.append({'text': cBagTabName,'sec_text': sub,'type': [int(ty)]})
                    name_to_tab_index_dict[cBagTabName] = len(self.tab_list) - 1
                else:
                    tab_data = self.tab_list[name_to_tab_index_dict[cBagTabName]]
                    tab_data['type'].append(int(ty))

        return

    def init_left_tab_list(self):
        self.init_tab_data()

        def return_func():
            self.on_before_close(self.close)

        from logic.gutils.new_template_utils import CommonLeftTabList
        self.left_tab_list = CommonLeftTabList(self.panel.tab_bar, self.tab_list, return_func, self.click_left_tab_btn)

    def click_left_tab_btn(self, index):
        if index == self.cur_tab_index:
            return
        else:
            self.set_ui_item_selected(None)
            self.show_item_desc_info({})
            self.cur_tab_index = index
            if index < len(self.tab_list):
                tab_data = self.tab_list[index]
                ty = tab_data.get('type')
                if ty:
                    self._show_type_filter = ty
                else:
                    self._show_type_filter = None
                self.update_show()
            return True

    def on_before_close(self, callback):
        self.panel.tab_bar.PlayAnimation('out')
        self.get_bg_ui() and self.get_bg_ui().close()
        if callback:
            callback()

    def init_bag_item(self, ui_item, item_data):
        ui_item.btn_choose.SetSwallowTouch(False)
        ui_item.btn_choose.SetNoEventAfterMove(True, '10w')
        if item_data:
            ui_item.nd_item.setVisible(True)
            ui_item.item.setVisible(True)
            ui_item.icon_try.setVisible(True)
            ui_item.lab_available.setVisible(True)
            item_id = item_data.get('id', None)
            if item_id == self._selected_item_id:
                self.set_ui_item_selected(ui_item)
            init_lobby_bag_item(ui_item, item_data, True)
            item_no = item_data.get('item_no', None)
            item_type = get_lobby_item_type(item_no)
            if item_type == L_ITEM_TYPE_PRODUCT:
                ui_item.PlayAnimation('get_tips')
            elif ui_item.IsPlayingAnimation('get_tips'):
                ui_item.StopAnimation('get_tips')
                ui_item.nd_get_tips.setVisible(False)
        else:
            ui_item.nd_item.setVisible(False)
            ui_item.item.setVisible(False)
            item_id = None
            ui_item.lab_quantity.SetString('')
            ui_item.icon_try.setVisible(False)
            ui_item.lab_available.setVisible(False)
            ui_item.nd_discount.setVisible(False)
            ui_item.img_frame.SetDisplayFrameByPath('', 'gui/ui_res_2/common/panel/frame_reward_white.png')
            ui_item.temp_role_tag.setVisible(False)
            if ui_item.IsPlayingAnimation('get_tips'):
                ui_item.StopAnimation('get_tips')
                ui_item.nd_get_tips.setVisible(False)

        @ui_item.btn_choose.callback()
        def OnClick(btn, touch):
            if not item_data:
                return
            else:
                self.set_ui_item_selected(ui_item)
                self._selected_item_id = item_id
                self.show_item_desc_info(item_data)
                item_no = item_data.get('item_no', None)
                self._selected_item_no = item_no
                use_params = confmgr.get('lobby_item', str(item_no), default={}).get('use_params', {})
                self.panel.btn_preview.setVisible(bool(use_params.get('need_preview', 0) or use_params.get('need_probability', 0)))
                return

        return

    def init_bag_item_helper(self, ui_item, idx):
        if idx < len(self._bag_show_items):
            item_data = self._bag_show_items[idx]
            self.init_bag_item(ui_item, item_data)
        else:
            self.init_bag_item(ui_item, None)
        return

    def init_bag_item_detail_panel(self):
        self.show_item_desc_info({})

    def show_item_desc_info(self, item_data):
        from common import utilities
        from logic.gutils import jump_to_ui_utils
        from logic.gcommon.cdata import bond_config
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_BOND
        content_nd = self.panel.nd_content
        if not item_data:
            self.panel.nd_content.setVisible(False)
            self.panel.img_empty.setVisible(True)
            return
        else:
            self.panel.nd_content.setVisible(True)
            self.panel.img_empty.setVisible(False)
            item_no = item_data.get('item_no', None)
            quantity = item_data.get('quantity', 1)
            init_lobby_bag_item(self.panel.temp_item, {'item_no': item_no})
            content_nd.lab_name.SetString(get_lobby_item_name(item_no))
            content_nd.lab_quantity.SetString(str(quantity))
            content_nd.lab_details.SetString(get_lobby_item_desc(item_no))
            item_conf = confmgr.get('lobby_item', str(item_no), default={})
            recyle_gain_item = item_conf.get('recyle_gain_item', [])
            recyclable = False
            if recyle_gain_item:
                from logic.gcommon.time_utility import get_server_time
                if get_server_time() >= item_conf.get('recycle_begin_time', 0):
                    recyclable = True
            if recyclable and int(item_no) in six_ex.values(MONEY_DICT):
                for season, coin in six.iteritems(MONEY_DICT):
                    if coin == int(item_no):
                        cur_season = global_data.player.get_battle_season()
                        if cur_season == season:
                            recyclable = False
                        break

            content_nd.btn_recycle.setVisible(recyclable)
            if not recyclable:
                content_nd.btn_use.SetPosition('50%', 28)
            else:
                content_nd.btn_use.ReConfPosition()
            usage = get_lobby_item_usage(item_no)
            use_type = get_lobby_item_use_type(item_no)
            if usage and use_type not in ('1024', '1025', '1058'):
                useable = True
            else:
                useable = False
            content_nd.btn_use.setVisible(useable)
            can_jump = item_utils.can_jump_to_ui(item_no)
            jump_txt = item_utils.get_item_access(item_no)
            content_nd.btn_go.lab_go.SetString(jump_txt or '')
            content_nd.btn_go.setVisible(False)

            @content_nd.btn_go.callback()
            def OnClick(btn, touch, item_no=item_no):
                item_utils.jump_to_ui(item_no)

            @content_nd.btn_use.btn_major.callback()
            def OnClick(btn, touch):
                try_use_lobby_item(item_data, usage)

            @content_nd.btn_recycle.btn_major.callback()
            def OnClick(btn, touch):
                from .LobbyBagRecycleUI import LobbyBagRecycleUI
                dlg = LobbyBagRecycleUI()
                dlg.init_recycle_item(item_data)

            content_nd.btn_check.setVisible(False)
            content_nd.btn_unlock.setVisible(False)
            content_nd.btn_send_gift.setVisible(False)
            content_nd.lab_gifts_num.setVisible(False)
            if item_conf.get('type', -1) == L_ITEM_TYPE_BOND:
                unlock_role_id = bond_config.get_unlock_role_id_of_bond_item(item_no)
                if unlock_role_id and not global_data.player.get_item_by_no(unlock_role_id):
                    need_count = 0
                    prices_info = mall_utils.get_mall_item_price(str(unlock_role_id), pick_list=['item'])
                    if prices_info:
                        need_count = prices_info[0]['real_price']
                    if quantity >= need_count:
                        content_nd.btn_unlock.setVisible(True)
                    else:
                        content_nd.btn_check.setVisible(True)
                    content_nd.lab_gifts_num.setVisible(True)
                    content_nd.lab_gifts_num.SetString(get_text_by_id(870065, [quantity, need_count]))
                    content_nd.lab_gifts_num.progress_bar.SetPercent(utilities.safe_percent(quantity, need_count))
                else:
                    content_nd.btn_send_gift.setVisible(True)

                @content_nd.btn_check.btn_major.callback()
                def OnClick(btn, touch):
                    jump_to_ui_utils.jump_to_display_detail_by_item_no(unlock_role_id)

                @content_nd.btn_send_gift.btn_major.callback()
                def OnClick(btn, touch):
                    select_role_id = unlock_role_id if unlock_role_id else global_data.player.get_role()
                    jump_to_ui_utils.try_jump_to_bond(select_role_id, select_item_id=item_no)

                @content_nd.btn_unlock.btn_major.callback()
                def OnClick(btn, touch):
                    jump_to_ui_utils.jump_to_display_detail_by_item_no(unlock_role_id)

            return

    def on_click_back_btn(self, *args):
        self.on_before_close(self.close)

    def on_click_btn_preview(self, btn, touch, *args):
        wpos = touch.getLocation()
        global_data.emgr.show_item_desc_ui_event.emit(self._selected_item_no, wpos)

    def on_click_batch_recycle_btn(self, btn, touch):
        from .LobbyBatchBagRecycleUI import LobbyBatchBagRecycleUI
        dlg = LobbyBatchBagRecycleUI()
        dlg.init_recycle_list_item(self._bag_show_items)

    def set_ui_item_selected(self, ui_item):
        if self._selected_item:
            self._selected_item.btn_choose.SetSelect(False)
        self._selected_item = ui_item
        if self._selected_item:
            self._selected_item.btn_choose.SetSelect(True)

    def need_update_list_show(self, *args):
        self.init_data()