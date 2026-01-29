# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/RoleSelectWidget.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.cfg import confmgr
from logic.client.const import items_book_const
from logic.gutils import items_book_utils
from common.framework import Functor
from logic.gutils import item_utils

class RoleSelectWidget(object):

    def __init__(self, parent, select_btn, select_list_container, role_select_list, on_select_role_cb, item_type, img_red_dot):
        super(RoleSelectWidget, self).__init__()
        self.valid = True
        self.selected_role = None
        self.enable_select = True
        self.item_type = item_type
        self.init_role_data()
        self.parent = parent
        self.select_btn = select_btn
        self.select_list_container = select_list_container
        self.role_select_list = role_select_list
        self.on_select_role_cb = on_select_role_cb
        self.img_red_dot = img_red_dot
        self.init_widget()
        return

    def init_widget(self):
        init_role = global_data.player.get_role()
        self.init_select_btn()
        self.init_role_list()
        self.on_select_role(init_role)

    def init_select_btn(self):
        self.select_btn.BindMethod('OnClick', self.on_click_select_btn)

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
        self.img_red_dot.setVisible(bool(self.role_rp_dict))
        for role_info in self.role_list:
            role_id = role_info[0]
            item_widget = self.role_select_list.GetItem(self.role_id_to_idx_dict[role_id])
            item_widget.img_reddot.setVisible(role_id in self.role_rp_dict)

    def init_role_data(self):
        self.role_config = confmgr.get('role_info', 'RoleInfo', 'Content')
        self.role_profile = confmgr.get('role_info', 'RoleProfile', 'Content')
        role_list = []
        for k, v in six.iteritems(self.role_config):
            goods_id = v.get('goods_id', None)
            if not goods_id:
                continue
            role_list.append((k, v))

        sorted(role_list, key=cmp_to_key(--- This code section failed: ---

  76       0  LOAD_GLOBAL           0  'six_ex'
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

        return

    def set_select_enable(self, enable_select):
        self.enable_select = enable_select

    def on_select_role(self, role_id, *args):
        if not self.valid:
            return
        index = self.role_id_to_idx_dict[str(role_id)]
        role_info = self.role_list[index][1]
        self.select_list_container.setVisible(False)
        self.parent.panel.img_role.SetDisplayFrameByPath('', role_info['icon'])
        self.parent.panel.lab_role_name.SetString(self.role_profile[str(role_id)]['role_name'])
        item_widget = self.role_select_list.GetItem(index)
        if self.selected_role:
            prev_index = self.role_id_to_idx_dict[self.selected_role]
            prev_item_widget = self.role_select_list.GetItem(prev_index)
            if prev_item_widget:
                prev_item_widget.btn_sort.SetSelect(False)
        if item_widget:
            item_widget.btn_sort.SetSelect(True)
        self.selected_role = str(role_id)
        if self.on_select_role_cb:
            if self.parent.get_interaction_state() == items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
                self.parent.set_interaction_state(items_book_const.INTERACTION_STATE_MANAGE_DISPLAY)
            self.on_select_role_cb(self.selected_role)

    def on_click_select_btn(self, *args):
        list_visible = self.select_list_container.isVisible()
        self.select_list_container.setVisible(not list_visible)

    def create_role_list_cb(self, lst, index, item_widget):
        pass

    def on_click_role_list_item(self, index, btn, *args):
        role_id = self.role_list[index][0]
        self.on_select_role(role_id)

    def init_role_list(self):
        self.role_select_list.SetInitCount(len(self.role_list))
        items = self.role_select_list.GetAllItem()
        for idx, item_widget in enumerate(items):
            role_info = self.role_list[idx]
            item_widget.img_role.SetDisplayFrameByPath('', role_info[1]['icon'])
            item_widget.lab_name.SetString(self.role_profile[role_info[0]]['role_name'])
            item_widget.btn_sort.BindMethod('OnClick', Functor(self.on_click_role_list_item, idx))
            item_widget.btn_sort.EnableCustomState(True)
            item_widget.btn_sort.SetSelect(False)

        self.update_red_point_widget()

    def destroy(self):
        self.parent = None
        self.select_btn = None
        self.select_list_container = None
        self.role_select_list = None
        self.on_select_role_cb = None
        self.valid = False
        return