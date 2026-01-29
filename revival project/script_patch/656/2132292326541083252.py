# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/RoundSelectWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.client.const import items_book_const
from common.framework import Functor
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gutils.interaction_utils import set_emoji_icon
import math
import cc

class RoundSelectWidget(object):

    def __init__(self, parent, round_temp):
        super(RoundSelectWidget, self).__init__()
        self.parent = parent
        self.round_temp = round_temp
        self.select_role_id = None
        self.role_data = {}
        self.parent_selected_item_no = None
        self.init_angle_to_select_idx()
        return

    def destroy(self):
        self.parent = None
        self.round_temp = None
        self.select_role_id = None
        self.role_data = {}
        self.parent_selected_item_no = None
        return

    def init_angle_to_select_idx(self):
        self.angle_list = []
        self.list_idx_to_action_idx_map = {}
        delta_angle = math.pi / 8
        per_item_angle = math.pi / 4
        start_angle = -delta_angle
        angle_idx = 0
        for temp_idx in range(0, 8):
            end_angle = start_angle + per_item_angle
            if end_angle > math.pi:
                end_angle -= math.pi * 2
                self.list_idx_to_action_idx_map[angle_idx] = temp_idx
                angle_idx += 1
                self.angle_list.append([start_angle, math.pi])
                self.list_idx_to_action_idx_map[angle_idx] = temp_idx
                angle_idx += 1
                self.angle_list.append([-math.pi, end_angle])
            else:
                self.list_idx_to_action_idx_map[angle_idx] = temp_idx
                angle_idx += 1
                self.angle_list.append([start_angle, end_angle])
            start_angle = end_angle

    def update_parent_selected_item_no(self, item_no):
        self.parent_selected_item_no = item_no
        self.update_round_temp_state()

    def udpate_selected_role_id(self, role_id):
        if not global_data.player:
            return
        self.selected_role_id = role_id
        self.update_widget()

    def update_widget(self):
        self.role_data = global_data.player.get_role_interaction_data(self.selected_role_id)
        self.update_round_temp()

    def update_round_temp_state(self):
        selected_state = bool(self.parent_selected_item_no)
        for i in range(0, 8):
            temp_item = getattr(self.round_temp, 'temp__action_spray_%d' % (i + 1))
            ('i set select', selected_state)
            temp_item.btn.SetSelect(selected_state)

    def update_round_temp(self):
        for i in range(0, 8):
            temp_item = getattr(self.round_temp, 'temp__action_spray_%d' % (i + 1))
            self.update_temp_item(temp_item, i)

    def update_temp_item(self, temp_item, idx):
        item_no = self.role_data.get(idx, None)
        item_valid = bool(item_no)
        temp_item.temp_icon.setVisible(item_valid)
        temp_item.bar_driver_head.setVisible(False)
        temp_item.btn.EnableCustomState(True)
        temp_item.btn_delete.setVisible(item_valid)
        self.bind_btn_callback(temp_item.btn, idx)
        self.bind_btn_delete_cb(temp_item.btn_delete, idx)
        if item_valid:
            set_emoji_icon(temp_item.temp_icon, item_no)
            if hasattr(temp_item, 'bar_driver_head') and temp_item.bar_driver_head:
                from logic.gutils.item_utils import get_interact_role_tag_by_role_id
                role_id = items_book_utils.get_interaction_belong_to_role(item_no, only_one_role=True)
                if role_id:
                    temp_item.bar_driver_head.setVisible(True)
                    temp_item.bar_driver_head.icon_role.SetDisplayFrameByPath('', get_interact_role_tag_by_role_id(role_id))
                else:
                    temp_item.bar_driver_head.setVisible(False)
        temp_item.btn.SetSelect(False)
        return

    def check_drag_pos(self, wpos):
        radius = self.round_temp.GetContentSize()[0] / 2
        position = self.round_temp.getPosition()
        lpos = self.round_temp.getParent().convertToNodeSpace(wpos)
        position.x -= radius
        wpos = cc.Vec2(lpos)
        wpos.subtract(position)
        length = wpos.length()
        if length > radius:
            return None
        else:
            angle = wpos.getAngle(cc.Vec2(0, 1))
            selected_idx = -1
            for idx, angle_range in enumerate(self.angle_list):
                selected_idx = idx
                if angle_range[0] <= angle < angle_range[1]:
                    break

            temp_idx = self.list_idx_to_action_idx_map[selected_idx]
            for i in range(0, 8):
                temp_item = getattr(self.round_temp, 'temp__action_spray_%d' % (i + 1))
                ('i set select', i == temp_idx)
                temp_item.btn.SetSelect(i == temp_idx)

            return temp_idx

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

    def on_btn_begin(self, item_no, btn, touch, *args):
        if not self.parent:
            return False
        else:
            if self.parent_selected_item_no is None:
                self.parent.unselect_item()
                self.update_parent_selected_item_no(None)
                self.parent.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM
            return True

    def on_btn_drag(self, item_no, btn, touch, *args):
        if not self.parent or not self.parent.panel:
            return
        else:
            if self.parent_selected_item_no is None:
                if item_no == 0:
                    return False
                wpos = touch.getLocation()
                if not self.parent.panel.drag_item.isVisible():
                    self.parent.show_drag_item(item_no)
                self.parent.on_drag_item(item_no, wpos)
            return

    def on_btn_end(self, index, item_no, btn, touch, *args):
        if not self.parent:
            return
        else:
            if self.parent_selected_item_no is None:
                self.parent.on_end_select_item(index, item_no, btn, touch)
            return

    def on_btn_click_callback(self, index, *args):
        if self.parent_selected_item_no:
            self.parent.on_click_set_interaction(index)
            return
        item_no = self.role_data.get(index, 0)
        if item_no:
            self.parent.show_item_detail(item_no)