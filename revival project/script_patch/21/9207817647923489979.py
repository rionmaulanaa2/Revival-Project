# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/AimColorWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.item import item_const
from logic.gcommon.common_const.buff_const import COMMON_BUFF
from logic.gcommon.item import item_utility as iutil
from common.uisys.BaseUIWidget import BaseUIWidget

class AimColorWidget(BaseUIWidget):
    NEED_PAGE_LIFE_RECORD = False

    def __init__(self, parent_ui, panel):
        self.global_events = {'change_aim_color_event': self.on_update_aim_color
           }
        self._aim_normal_color = '#SW'
        self._color_node_list = None
        self._color_exclude_node_set = set()
        self._color_replace_node_set = set()
        self._top_exclude_node_list = []
        self._node_old_sprite_map = {}
        super(AimColorWidget, self).__init__(parent_ui, panel)
        return

    def destroy(self):
        self.panel = None
        self._color_exclude_node_set = set()
        self._color_replace_node_set = set()
        self._top_exclude_node_list = []
        self._color_node_list = None
        self._node_old_sprite_map = {}
        super(AimColorWidget, self).destroy()
        return

    def on_update_aim_color(self):
        if global_data.player:
            from logic.gcommon.common_const import ui_operation_const as uoc
            cur_color_val = global_data.player.get_setting(uoc.AIM_COLOR_VAL)
            self._aim_normal_color = cur_color_val
            nd_list = self.get_aim_color_nodes()
            from common.uisys.uielment.CCSprite import CCSprite
            from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
            from common.uisys.uielment.CCUIImageView import CCUIImageView

            def set_node_color_recursive(node):
                if type(node) in [CCSprite, CCScale9Sprite, CCUIImageView]:
                    if node in self._color_replace_node_set:
                        node.AddReordedNodeInfo('color')
                        if uoc.AIM_COLOR_DEFAULT - self._aim_normal_color <= 1:
                            if node in self._node_old_sprite_map:
                                node.SetDisplayFrameByPath('', self._node_old_sprite_map[node])
                            node.ReConfColor()
                        else:
                            aim_color_sp = node.GetConfUserData().get('aim_color_sp')
                            if node not in self._node_old_sprite_map:
                                self._node_old_sprite_map[node] = node.GetDisplayFramePath()
                            node.SetDisplayFrameByPath('', aim_color_sp)
                            node.SetColor(self._aim_normal_color)
                    elif node not in self._color_exclude_node_set:
                        node.SetColor(self._aim_normal_color)
                for c in node.GetChildren():
                    set_node_color_recursive(c)

            for nd in nd_list:
                if nd:
                    set_node_color_recursive(nd)

    def get_aim_normal_color(self):
        return self._aim_normal_color

    def get_color_exclude_replace_node_set(self):
        nd_list = self.get_aim_color_nodes()
        exclude_node_set = set()
        replace_node_set = set()

        def check_node_recursive(nd):
            if nd.GetConfUserData().get('aim_color_sp'):
                replace_node_set.add(nd)
            elif nd.GetConfUserData().get('color_exclude'):
                exclude_node_set.add(nd)
            for c in nd.GetChildren():
                check_node_recursive(c)

        for nd in nd_list:
            check_node_recursive(nd)

        return (exclude_node_set, replace_node_set)

    def get_aim_color_nodes(self):
        if self._color_node_list is not None:
            return self._color_node_list
        else:
            nd_list = [ c for c in self.panel.GetChildren() if c not in self._top_exclude_node_list ]
            return nd_list

    def set_color_node_list(self, nd_list):
        self._color_node_list = nd_list

    def set_top_color_exclude_list(self, nd_list):
        self._top_exclude_node_list = nd_list

    def calculate_aim_node(self):
        self._color_exclude_node_set, self._color_replace_node_set = self.get_color_exclude_replace_node_set()

    def setup_color(self):
        self.on_update_aim_color()