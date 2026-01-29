# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ScaleableHorzContainer.py
from __future__ import absolute_import
import cc
from common.uisys.uielment.CCLayer import CCLayer
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK

class ScaleableHorzContainer(object):

    def __init__(self, container, cut_node, list_dot, move_select_change_callback=None, up_select_change_callback=None, begin_callback=None):
        self._is_init = False
        self._container = container
        self._cut_node = cut_node
        self._list_dot = list_dot
        self._selected_index = 0
        self._drag_selected_index = 0
        self._drag_selected_change = False
        self._move_select_change_callback = move_select_change_callback
        self._up_select_change_callback = up_select_change_callback
        self._begin_callback = begin_callback
        self.nd_cut_width = None
        self.nd_cut_height = None
        self.CLOTHEING_UNSELECTED_SCALE = 0.8
        self.CLOTHEING_SELECTED_W = None
        self.CLOTHEING_SELECTED_H = None
        self.CLOTHEING_UNSELECTED_W = None
        self.CLOTHEING_UNSELECTED_H = None
        self.fixed_scale = None
        self.list_skin_min_x = None
        self.list_skin_max_x = None
        self.list_skin_min_y = None
        self.list_skin_max_y = None
        self.horz_indent = self._container.GetHorzIndent()
        self.ver_indent = self._container.GetVertIndent()
        self._is_vertical = False
        nd = self._create_drag_nd()
        self._cut_node.AddChild('clothing_drag_layer', nd)
        self._drag_node = nd
        self.index_view_distance = 1
        self.hover_timer_id = None

        @nd.callback()
        def OnBegin(layer, touch):
            pass

        @nd.callback()
        def OnDrag(layer, touch):
            if not self._container:
                return
            self.move_drag(layer, touch)

        @nd.callback()
        def OnEnd(layer, touch):
            if not self._container:
                return
            self.check_up_selected()

        @nd.callback()
        def OnCancel(layer, touch):
            if not self._container:
                return
            self.check_up_selected()

        return

    def set_is_vertical(self, is_vertical):
        self._is_vertical = is_vertical

    def _create_drag_nd(self):
        nd = CCLayer.Create()
        nd.SetContentSize(420, 400)
        nd.SetPosition(0, 0)
        nd.setAnchorPoint(ccp(0, 0))
        bSwallow = False
        nd.HandleTouchMove(True, bSwallow, False)
        nd.set_sound_enable(False)
        return nd

    def get_item(self, idx):
        if self._container and len(self._container) > idx:
            return self._container.GetItem(idx)
        else:
            return None
            return None

    def release(self):
        self._container = None
        self._cut_node = None
        self._list_dot = None
        self._move_select_change_callback = None
        self._up_select_change_callback = None
        if self.hover_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.hover_timer_id)
        self.hover_timer_id = None
        return

    def check_up_selected(self):
        if not self._container:
            return
        self._drag_selected_change = False
        if self._drag_selected_index != self._selected_index:
            if self._drag_selected_index >= self._container.GetItemCount():
                return
            self._drag_selected_change = True
            self._selected_index = self._drag_selected_index
            self._up_select_change_callback(self._selected_index)
        self.scroll_to_selected_item()

    def get_selected_index(self):
        return self._selected_index

    def clear(self):
        self._is_init = False
        self._cut_node.stopAllActions()
        self._container.stopAllActions()

    def is_init(self):
        return self._is_init

    def init_list(self):
        self._is_init = True
        if self._is_vertical:
            pass
        self._selected_index = 0
        self._drag_selected_index = 0
        self.nd_cut_width, self.nd_cut_height = self._cut_node.GetContentSize()
        skin_item = self._container.GetItem(0)
        if self.CLOTHEING_SELECTED_W == None or self.CLOTHEING_SELECTED_H == None:
            self.CLOTHEING_SELECTED_W, self.CLOTHEING_SELECTED_H = skin_item.GetContentSize()
            self.CLOTHEING_UNSELECTED_W = self.CLOTHEING_SELECTED_W * self.CLOTHEING_UNSELECTED_SCALE
            self.CLOTHEING_UNSELECTED_H = self.CLOTHEING_SELECTED_H * self.CLOTHEING_UNSELECTED_SCALE
            self.fixed_scale = 1 - self.CLOTHEING_UNSELECTED_SCALE
            if not self._is_vertical:
                self._container.SetForceH(self.CLOTHEING_SELECTED_H)
            else:
                self._container.SetForceW(self.CLOTHEING_SELECTED_W)
        if not self._is_vertical:
            self._center_pos = self.nd_cut_width / 2.0
        else:
            self._center_pos = self.nd_cut_height / 2.0
        self.list_skin_min_x, self.list_skin_min_y = self.force_select_clothing(self._container.GetItemCount() - 1)
        self.list_skin_max_x, self.list_skin_max_y = self.force_select_clothing(0)
        if self.list_skin_max_y < self.list_skin_min_y:
            temp = self.list_skin_max_y
            self.list_skin_max_y = self.list_skin_min_y
            self.list_skin_min_y = temp
        item_list = self._container.GetAllItem()
        for index, item in enumerate(item_list):
            item = self._container.GetItem(index)
            self.allow_item_click(item, index)

        return

    def allow_item_click(self, item, index):

        @item.nd_card.callback()
        def OnClick(*args):
            if not self._drag_selected_change:
                self._selected_index = index
                self.set_dot_selected(index)
                self._up_select_change_callback and self._up_select_change_callback(self._selected_index)
                self.scroll_to_selected_item()

        if self._begin_callback and callable(self._begin_callback):

            @item.nd_card.callback()
            def OnBegin(*args):
                self._begin_callback()

    def set_dot_selected(self, selected_index):
        if not self._list_dot:
            return
        item_list = self._list_dot.GetAllItem()
        for index, dot_item in enumerate(item_list):
            dot_item = self._list_dot.GetItem(index)
            if index == selected_index:
                dot_item.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/img_skin_list_dot_1.png')
            else:
                dot_item.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/img_skin_list_dot_2.png')

    def force_select_clothing(self, selected_index):
        self._selected_index = selected_index
        self._drag_selected_index = selected_index
        self.set_dot_selected(selected_index)
        item_list = self._container.GetAllItem()
        for index, item in enumerate(item_list):
            item = self._container.GetItem(index)
            if self._list_dot:
                self._list_dot.GetItem(selected_index)
            if callable(item.nd_card.EnableCustomState):
                item.nd_card.EnableCustomState(True)
                item.nd_card.SetSelect(index == selected_index)
            if index == selected_index:
                item.SetContentSize(self.CLOTHEING_SELECTED_W, self.CLOTHEING_SELECTED_H)
                item.nd_card.setScaleX(1)
                item.nd_card.setScaleY(1)
                item.setLocalZOrder(1000)
            else:
                item.SetContentSize(self.CLOTHEING_UNSELECTED_W, self.CLOTHEING_UNSELECTED_H)
                item.nd_card.setScaleX(self.CLOTHEING_UNSELECTED_SCALE)
                item.nd_card.setScaleY(self.CLOTHEING_UNSELECTED_SCALE)
                item.setLocalZOrder(int(self.CLOTHEING_UNSELECTED_SCALE * 1000) - abs(index - self._selected_index))
            item.nd_card.InitConfPosition()
            item.nd_rot.InitConfPosition()
            if abs(index - self._selected_index) <= self.index_view_distance:
                item.setVisible(True)
            else:
                item.setVisible(False)

        self._container._refreshItemPos()
        cur_x, cur_y = self.get_list_skin_pos_by_item(selected_index)
        self._container.SetPosition(cur_x, cur_y)
        return (
         cur_x, cur_y)

    def get_list_skin_pos_by_item(self, index):
        width, height = self._container.GetContentSize()
        x, y = self._container.GetPosition()
        if not self._is_vertical:
            selected_item_center_x = index * self.CLOTHEING_UNSELECTED_W + index * self.horz_indent + self.CLOTHEING_SELECTED_W / 2
            fixed_x = 0.5 * self.nd_cut_width - selected_item_center_x
            return (
             fixed_x, y)
        else:
            selected_item_center_y = index * self.CLOTHEING_UNSELECTED_H + index * self.ver_indent + self.CLOTHEING_SELECTED_H / 2
            selected_item_center_y = selected_item_center_y * self._container.getScaleY()
            fixed_y = self._center_pos + selected_item_center_y
            return (
             x, fixed_y)

    def move_drag(self, layer, touch):
        if not self._cut_node.IsVisible():
            return
        else:
            if self._container.GetItemCount() <= 0:
                return
            if not self._is_init:
                return
            delta = touch.getDelta()
            cur_x, cur_y = self._container.GetPosition()
            if not self._is_vertical:
                new_x = cur_x + delta.x
                if self.list_skin_min_x is not None and new_x < self.list_skin_min_x:
                    new_x = self.list_skin_min_x
                elif self.list_skin_max_x is not None and new_x > self.list_skin_max_x:
                    new_x = self.list_skin_max_x
                self._container.SetPosition(new_x, cur_y)
            else:
                new_y = cur_y + delta.y
                if self.list_skin_min_y is not None and new_y < self.list_skin_min_y:
                    new_y = self.list_skin_min_y
                elif self.list_skin_max_y is not None and new_y > self.list_skin_max_y:
                    new_y = self.list_skin_max_y
                self._container.SetPosition(cur_x, new_y)
            self.update_list_layout(True)
            return

    def update_list_layout(self, trigge_move_select=True):
        cur_x, cur_y = self._container.GetPosition()
        item_list = self._container.GetAllItem()
        dis_offset = (self.CLOTHEING_UNSELECTED_W + self.CLOTHEING_SELECTED_W) / 2 + self.horz_indent
        min_dis_x = None
        for index, item in enumerate(item_list):
            item = self._container.GetItem(index)
            dis_x = abs(cur_x + item.getPosition().x - item.getContentSize().width * item.getAnchorPoint().x + item.getContentSize().width / 2 - self.nd_cut_width / 2)
            if dis_x < dis_offset:
                if min_dis_x == None or dis_x < min_dis_x:
                    min_dis_x = dis_x
                    self._drag_selected_index = index
                scale = 1 - self.fixed_scale * (dis_x / dis_offset)
                width = self.CLOTHEING_SELECTED_W * scale
                height = self.CLOTHEING_SELECTED_H * scale
                item.SetContentSize(width, height)
                item.nd_card.setScaleX(scale)
                item.nd_card.setScaleY(scale)
                item.setLocalZOrder(int(scale * 1000))
            else:
                item.SetContentSize(self.CLOTHEING_UNSELECTED_W, self.CLOTHEING_UNSELECTED_H)
                item.nd_card.setScaleX(self.CLOTHEING_UNSELECTED_SCALE)
                item.nd_card.setScaleY(self.CLOTHEING_UNSELECTED_SCALE)
                item.setLocalZOrder(int(self.CLOTHEING_UNSELECTED_SCALE * 1000) - abs(index - self._drag_selected_index))
            item.nd_card.InitConfPosition()
            item.nd_rot.InitConfPosition()
            if abs(index - self._drag_selected_index) <= self.index_view_distance:
                item.setVisible(True)
            else:
                item.setVisible(False)

        self._container._refreshItemPos()
        if trigge_move_select:
            self.check_timer()
        else:
            item = self._container.GetItem(self._selected_index)
        return

    def check_timer(self):
        if self._drag_selected_index == self._selected_index:
            pass
        else:
            if self.hover_timer_id:
                global_data.game_mgr.unregister_logic_timer(self.hover_timer_id)
            self.hover_timer_id = global_data.game_mgr.register_logic_timer(self.check_timer_pass, interval=0.2, times=1, mode=CLOCK)

    def check_timer_pass(self):
        if not self._container:
            return
        if self._drag_selected_index >= self._container.GetItemCount():
            return
        self.set_dot_selected(self._drag_selected_index)
        self._move_select_change_callback(self._drag_selected_index)

    def scroll_to_selected_item(self):
        if not self._is_vertical:
            if not self._is_init or self.CLOTHEING_UNSELECTED_W is None:
                return
            fixed_x, fixed_y = self._container.GetPosition()
            selected_item_center_x = self._selected_index * self.CLOTHEING_UNSELECTED_W + self._selected_index * self.horz_indent + self.CLOTHEING_SELECTED_W / 2
            fixed_x = 0.5 * self.nd_cut_width - selected_item_center_x
        else:
            if not self._is_init or self.CLOTHEING_UNSELECTED_H is None:
                return
            fixed_x, fixed_y = self._container.GetPosition()
            selected_item_center_y = self._selected_index * self.CLOTHEING_UNSELECTED_H + self._selected_index * self.ver_indent + self.CLOTHEING_SELECTED_H / 2
            selected_item_center_y = selected_item_center_y * self._container.getScaleY()
            fixed_y = self._center_pos + selected_item_center_y
        self._cut_node.stopAllActions()
        self._container.stopAllActions()

        def scroll_end():
            self._cut_node.stopAllActions()
            self.update_list_layout(False)

        self._container.runAction(cc.Sequence.create([
         cc.MoveTo.create(0.5, ccp(fixed_x, fixed_y)),
         cc.CallFunc.create(scroll_end)]))

        def tick():
            self.update_list_layout(False)

        seq_action = cc.Sequence.create([cc.DelayTime.create(0.03), cc.CallFunc.create(tick)])
        repeat_action = cc.RepeatForever.create(seq_action)
        self._cut_node.runAction(repeat_action)
        return