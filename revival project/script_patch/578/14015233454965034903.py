# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ScaleableVerContainer.py
from __future__ import absolute_import
import cc
from common.uisys.uielment.CCLayer import CCLayer
from common.utils.cocos_utils import ccp
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer

class ScaleableVerContainer(ScaleableHorzContainer):

    def __init__(self, container, cut_node, list_dot, move_select_change_callback=None, up_select_change_callback=None):
        super(ScaleableVerContainer, self).__init__(container, cut_node, list_dot, move_select_change_callback, up_select_change_callback)
        self.set_is_vertical(True)
        self.index_view_distance = 2

    def _create_drag_nd(self):
        nd = CCLayer.Create()
        nd.SetContentSize(*self._cut_node.GetContentSize())
        nd.SetPosition(0, 0)
        nd.setAnchorPoint(ccp(0, 0))
        bSwallow = False
        nd.HandleTouchMove(True, bSwallow, False)
        nd.set_sound_enable(False)
        return nd

    def update_list_layout(self, trigge_move_select=True):
        cur_x, cur_y = self._container.GetPosition()
        item_list = self._container.GetAllItem()
        dis_offset = (self.CLOTHEING_UNSELECTED_H + self.CLOTHEING_SELECTED_H) / 2 + self.ver_indent
        min_dis_y = None
        for index, item in enumerate(item_list):
            item = self._container.GetItem(index)
            dis_y = abs(cur_y + item.getPosition().y - item.getContentSize().height / 2 - self._center_pos)
            if dis_y < dis_offset:
                if min_dis_y == None or dis_y < min_dis_y:
                    min_dis_y = dis_y
                    self._drag_selected_index = index
                scale = 1 - self.fixed_scale * (dis_y / dis_offset)
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
            if callable(item.nd_card.EnableCustomState):
                item.nd_card.EnableCustomState(True)
                item.nd_card.SetSelect(self._selected_index == index)
            item.nd_card.InitConfPosition()
            item.nd_rot.InitConfPosition()
            if abs(index - self._drag_selected_index) <= self.index_view_distance:
                item.setVisible(True)
            else:
                item.setVisible(False)

        self._container._refreshItemPos()
        if trigge_move_select:
            item = self._container.GetItem(self._drag_selected_index)
            self.set_dot_selected(self._drag_selected_index)
            self._move_select_change_callback(self._drag_selected_index)
        else:
            item = self._container.GetItem(self._selected_index)
        return