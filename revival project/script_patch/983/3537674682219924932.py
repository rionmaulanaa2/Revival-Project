# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ListSelectWidget.py
from __future__ import absolute_import
from common.framework import Functor
from logic.client.const import items_book_const
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_UNKONW_ITEM
from logic.gutils.interaction_utils import set_emoji_icon

class ListSelectWidget(object):

    def __init__(self, parent, list_temp):
        super(ListSelectWidget, self).__init__()
        self.parent = parent
        self.list_temp = list_temp
        self.selected_role_id = None
        self.parent_selected_item_no = None
        self.role_data = {}
        return

    def destroy(self):
        pass

    def update_parent_selected_item_no(self, item_no):
        self.parent_selected_item_no = item_no
        self.update_list_temp_state()

    def udpate_selected_role_id(self, role_id):
        if not global_data.player:
            return
        self.selected_role_id = role_id
        self.update_widget()

    def update_widget(self):
        self.role_data = global_data.player.get_role_interaction_data(self.selected_role_id, is_auto_mode=True)
        self.update_list_temp()

    def update_list_temp_state(self):
        selected_state = bool(self.parent_selected_item_no)
        for temp_item in self.list_temp.GetAllItem():
            temp_item.temp_expression_item.btn.SetSelect(selected_state)

    def update_list_temp(self):
        auto_emoji = confmgr.get('auto_emoji', default={})
        moment_ids = auto_emoji.get('moment_list', [])
        if len(moment_ids) != len(self.list_temp.GetAllItem()):
            log_error('Auto emoji error\xef\xbc\x9a not match moment count!')
            return
        for idx, temp_item in enumerate(self.list_temp.GetAllItem()):
            moment_id = moment_ids[idx]
            self.update_temp_item(temp_item, moment_id)

    def update_temp_item(self, temp_item, idx):
        item_no = self.role_data.get(idx, None)
        item_type = item_utils.get_lobby_item_type(item_no)
        is_emoji = item_type == L_ITEM_TYPE_EMOTICON
        if not is_emoji and bool(item_no):
            self.on_click_btn_delete(idx)
        item_valid = bool(item_no) and is_emoji
        temp_item.temp_expression_item.btn.SetSwallowTouch(False)
        temp_item.temp_expression_item.btn.SetNoEventAfterMove(False, '5w')
        temp_item.temp_expression_item.temp_icon.setVisible(item_valid)
        temp_item.temp_expression_item.btn_delete.setVisible(item_valid)
        temp_item.lab_info.setVisible(item_valid)
        self.bind_btn_callback(temp_item.temp_expression_item.btn, idx)
        self.bind_btn_delete_cb(temp_item.temp_expression_item.btn_delete, idx)
        if item_valid:
            set_emoji_icon(temp_item.temp_expression_item.temp_icon, item_no)
            temp_item.lab_info.SetString(item_utils.get_lobby_item_name(item_no))
        temp_item.temp_expression_item.btn.SetSelect(False)
        return

    def check_drag_pos(self, wpos):
        auto_emoji = confmgr.get('auto_emoji', default={})
        moment_ids = auto_emoji.get('moment_list', [])
        for idx, temp_item in enumerate(self.list_temp.GetAllItem()):
            if temp_item.IsPointIn(wpos):
                moment_id = moment_ids[idx]
                temp_item.temp_expression_item.btn.SetSelect(True)
                return moment_id

    def bind_btn_delete_cb(self, btn_delete, index):
        btn_delete.BindMethod('OnClick', Functor(self.on_click_btn_delete, index))

    def on_click_btn_delete(self, index, *args):
        item_no = self.role_data.get(index, None)
        if bool(item_no):
            self.parent.on_delete_interaction(index)
        return

    def bind_btn_callback(self, btn, index):
        item_no = self.role_data.get(index, 0)
        btn.BindMethod('OnClick', Functor(self.on_btn_click_callback, index))
        btn.BindMethod('OnBegin', Functor(self.on_btn_begin, item_no))
        btn.BindMethod('OnDrag', Functor(self.on_btn_drag, item_no))
        btn.BindMethod('OnEnd', Functor(self.on_btn_end, index, item_no))
        btn.BindMethod('OnCancel', Functor(self.on_btn_end, index, item_no))

    def on_btn_begin(self, *args):
        if not self.parent:
            return False
        else:
            if self.parent_selected_item_no is None:
                self.parent.unselect_item()
                self.update_parent_selected_item_no(None)
                self.parent.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM
            return True

    def on_btn_drag(self, item_no, btn, touch, *args):
        if not self.parent:
            return
        else:
            if self.parent_selected_item_no is None:
                if item_no == 0:
                    return False
                wpos = touch.getLocation()
                if not self.parent.panel.drag_item.isVisible():
                    self.parent.show_drag_item(item_no)
                btn.SetSwallowTouch(True)
                self.parent.on_drag_item(item_no, wpos)
            return

    def on_btn_end(self, index, item_no, btn, touch, *args):
        if not self.parent:
            return
        else:
            if self.parent_selected_item_no is None:
                btn.SetSwallowTouch(False)
                self.parent.on_end_select_item(index, item_no, btn, touch)
            return

    def on_btn_click_callback(self, index, *args):
        if self.parent_selected_item_no:
            self.parent.on_click_set_interaction(index)
            return
        item_no = self.role_data.get(index, 0)
        if item_no:
            self.parent.show_item_detail(item_no)