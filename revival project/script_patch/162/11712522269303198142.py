# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemCategoryListWidget.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import red_point_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import game3d
OUTLINE_PIC_PATH = 'gui/ui_res_2/catalogue/outline/208%s.png'

class ItemCategoryListWidget(object):

    def __init__(self, parent, panel, data_dict, click_item_callback, tab_id, custom_create_item_callback=None, need_show_outline_pic=False):
        self.tab_id = tab_id
        self.select_index = None
        self.parent = parent
        self.panel = panel
        self.on_click_item_callback = None
        self.custom_create_item_callback = None
        self.need_show_outline_pic = need_show_outline_pic
        self.data_dict = data_dict
        self.init_data(data_dict)
        self.widget_dict = {}
        self.set_click_callback(click_item_callback)
        self.set_custom_create_item_callback(custom_create_item_callback)
        self.valid = True
        if not custom_create_item_callback:
            self.init_widget()
        return

    def init_data(self, data_dict):
        if isinstance(data_dict, list):
            self.data_list = data_dict
        else:
            self.data_list = sorted(six_ex.items(data_dict), key=cmp_to_key(--- This code section failed: ---

  42       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_GLOBAL           2  'int'
           9  LOAD_GLOBAL           1  'compare'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_1       1 
          16  LOAD_GLOBAL           2  'int'
          19  LOAD_FAST             1  'y'
          22  LOAD_CONST            1  ''
          25  BINARY_SUBSCR    
          26  CALL_FUNCTION_1       1 
          29  CALL_FUNCTION_2       2 
          32  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 29
))

    def set_click_callback(self, cb):
        self.on_click_item_callback = cb

    def set_custom_create_item_callback(self, cb):
        self.custom_create_item_callback = cb

    def init_widget(self):
        if not self.valid:
            return
        self.init_list()

    def refresh_widget(self, data_dict):
        self.init_data(data_dict)
        self.init_list(False)

    def on_create_item(self, lv, index, item_widget):
        if self.custom_create_item_callback:
            self.custom_create_item_callback(lv, index, item_widget)
            return
        item_no = self.data_list[index][0]
        item_widget.btn.EnableCustomState(True)
        item_widget.btn.SetText(item_utils.get_lobby_item_name(item_no))
        if self.need_show_outline_pic:
            icon_path = OUTLINE_PIC_PATH % str(item_no)[3:]
            item_widget.btn.icon.SetDisplayFrameByPath('', icon_path)
            item_widget.btn.icon_sel.SetDisplayFrameByPath('', icon_path)
            item_widget.btn.icon.setVisible(True)
            item_widget.btn.icon_sel.setVisible(False)
        else:
            item_widget.btn.icon.setVisible(False)
            item_widget.btn.icon_sel.setVisible(False)
        item_widget.btn.SetSelect(False)
        show_new = global_data.lobby_red_point_data.get_rp_by_belong_no(item_no)
        red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
        if not show_new:
            left_time_str = items_book_utils.get_filter_item_left_time_str(self.tab_id, item_no)
            item_widget.icon_limited.setVisible(bool(left_time_str))
        item_widget.btn.BindMethod('OnClick', Functor(self.on_click_category_item, index))

    def click_item(self, index):
        if not self.valid:
            return
        if not self.panel.list_right.IsAsync():
            click_item = self.panel.list_right.GetItem(index)
            click_item.btn.OnClick(click_item.btn)
        elif index < self.panel.list_right.GetItemCount():
            click_item = self.panel.list_right.GetItem(index)
            if not click_item:
                click_item = self.panel.list_right.DoLoadItem(index)
            click_item.btn.OnClick(click_item.btn)

    def on_click_category_item(self, index, *args):
        if not self.valid:
            return
        else:
            list_item = self.panel.list_right
            if self.select_index is not None:
                prev_item = list_item.GetItem(self.select_index)
                if prev_item:
                    prev_item.btn.SetSelect(False)
                    if self.need_show_outline_pic:
                        prev_item.btn.icon.setVisible(True)
                        prev_item.btn.icon_sel.setVisible(False)
            self.select_index = index
            if index is None:
                return
            click_item = list_item.GetItem(index)
            click_item.btn.SetSelect(True)
            if self.need_show_outline_pic:
                click_item.btn.icon.setVisible(False)
                click_item.btn.icon_sel.setVisible(True)
            click_item.PlayAnimation('click')
            if self.on_click_item_callback:
                self.on_click_item_callback(index, self.data_list[index])
            return

    def init_select_item(self, index, off_set=None):
        list_item = self.panel.list_right
        index = min(index, len(self.data_list) - 1)
        select_widget = list_item.GetItem(index)
        if select_widget is None:
            select_widget = list_item.DoLoadItem(index)
        if select_widget is None:
            select_widget = list_item.DoLoadItem(index)
        if not off_set:
            if index != 0:
                self.panel.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/catalogue/pnl_catalogue_list_right.png', force_sync=True)
            list_item.LocatePosByItem(index)
        else:
            list_item.SetContentOffset(off_set)
        select_widget is not None and self.on_click_category_item(index)
        if list_item.IsAsync():
            list_item.scroll_Load()
        return

    def init_list(self, is_init=True):
        list_item = self.panel.list_right
        list_item.BindMethod('OnCreateItem', self.on_create_item)
        list_item.SetInitCount(len(self.data_list))
        off_set = list_item.GetContentOffset()
        all_items = list_item.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.on_create_item(list_item, index, widget)

        if len(self.data_list):
            if is_init:
                self.init_select_item(0)
            else:
                self.init_select_item(self.select_index, off_set)
        else:
            global_data.emgr.change_model_display_scene_item.emit(None)
        if list_item.IsAsync():
            list_item.scroll_Load()
        return

    def destroy(self):
        self.panel = None
        self.parent = None
        self.on_click_item_callback = None
        self.valid = False
        return