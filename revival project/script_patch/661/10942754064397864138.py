# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MechaItemSelectWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from functools import cmp_to_key
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from common.framework import Functor
from logic.gutils import red_point_utils

class MechaItemSelectWidget(object):

    def __init__(self, parent, panel, item_type, click_item_callback):
        self.valid = True
        self.select_index = None
        self.item_type = item_type
        self.parent = parent
        self.panel = panel
        self.on_click_item_callback = click_item_callback
        self.init_mecha_data()
        self.init_list()
        return

    def init_mecha_data(self):
        mecha_config = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self.ui_config = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        role_list = []
        for k, v in six.iteritems(mecha_config):
            role_list.append((k, v))

        sorted(role_list, key=cmp_to_key(--- This code section failed: ---

  32       0  LOAD_GLOBAL           0  'six_ex'
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
        self.role_list = role_list
        self.role_id_to_idx_dict = {}
        self.role_rp_dict = {}
        for idx, role_info in enumerate(self.role_list):
            self.role_id_to_idx_dict[role_info[0]] = idx
            if self.check_role_rp_dict(role_info[0]):
                self.role_rp_dict[role_info[0]] = True

    def check_role_rp_dict(self, role_id):
        item_dict = items_book_utils.get_interaction_item_info(role_id, self.item_type)
        for k in six_ex.keys(item_dict):
            item_info = global_data.player.get_item_by_no(int(k))
            if not item_info:
                continue
            if item_info.rp:
                return True

        return False

    def update_red_point(self, item_no):
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type != self.item_type:
            return
        self.role_rp_dict = {}
        for idx, role_info in enumerate(self.role_list):
            if self.check_role_rp_dict(role_info[0]):
                self.role_rp_dict[role_info[0]] = True

        self.update_red_point_widget()

    def update_red_point_widget(self):
        for role_info in self.role_list:
            role_id = role_info[0]
            item_widget = self.panel.GetItem(self.role_id_to_idx_dict[role_id])
            if not item_widget:
                continue
            red_point_utils.show_red_point_template(item_widget.nd_new, role_id in self.role_rp_dict)

    def destroy(self):
        self.unselect_cnt_item()
        self.valid = False
        self.parent = None
        self.on_create_item_callback = None
        self.role_list = None
        return

    def on_create_item(self, lst, index, item_widget):
        if not self.valid:
            return
        if index < len(self.role_list):
            role_info = self.role_list[index]
            item_widget.img_role.SetDisplayFrameByPath('', role_info[1]['icon'])
            item_widget.btn.SetText(get_text_by_id(self.ui_config[str(role_info[0])]['name_text_id'][0]))
            item_widget.btn.EnableCustomState(True)
            item_widget.btn.BindMethod('OnClick', Functor(self.on_click_item, index))
            red_point_utils.show_red_point_template(item_widget.nd_new, role_info[0] in self.role_rp_dict)

    def unselect_cnt_item(self):
        if self.select_index is not None:
            prev_index = self.select_index
            prev_item_widget = self.panel.GetItem(prev_index)
            if prev_item_widget:
                prev_item_widget.btn.SetSelect(False)
        return

    def on_click_item(self, index, *args):
        if not self.valid:
            return
        else:
            print('click index', index)
            role_id = self.role_list[index][0]
            item_widget = self.panel.GetItem(index)
            if self.select_index is not None:
                prev_index = self.select_index
                prev_item_widget = self.panel.GetItem(prev_index)
                if prev_item_widget:
                    prev_item_widget.btn.SetSelect(False)
            if item_widget:
                self.select_index = index
                item_widget.btn.SetSelect(True)
                item_widget.PlayAnimation('click')
                if self.on_click_item_callback:
                    self.on_click_item_callback(role_id)
            return

    def get_role_idx_in_list(self, role_id):
        if role_id is None:
            return 0
        else:
            role_id = str(role_id)
            if role_id in self.role_id_to_idx_dict:
                return self.role_id_to_idx_dict[role_id]
            return 0

    def init_select_item(self, index, off_set=None):
        list_item = self.panel
        index = max(min(index, len(self.role_list) - 1), 0)
        if not (off_set and len(self.role_list) > 0):
            list_item.LocatePosByItem(index)
        else:
            list_item.SetContentOffset(off_set)
        select_widget = list_item.GetItem(index)
        if select_widget is None:
            if hasattr(list_item, 'DoLoadItem') and callable(list_item.DoLoadItem):
                select_widget = list_item.DoLoadItem(index)
        select_widget and select_widget.btn.OnClick(None)
        return

    def init_list(self):
        list_item = self.panel
        list_item.BindMethod('OnCreateItem', self.on_create_item)
        skin_count = len(self.role_list)
        list_item.SetInitCount(skin_count)
        all_items = list_item.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.on_create_item(list_item, index, widget)

        if hasattr(list_item, 'scroll_Load') and skin_count > 0:
            if callable(list_item.scroll_Load):
                list_item.scroll_Load()