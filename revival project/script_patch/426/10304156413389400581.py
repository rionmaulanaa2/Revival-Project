# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/FunctionWidgetBase.py
from __future__ import absolute_import
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.KillSfxGetUseBuyWidget import KillSfxGetUseBuyWidget
from logic.comsys.items_book_ui.ItemFilterWidget import ItemFilterWidget
from logic.gutils import items_book_utils
from logic.client.const import items_book_const
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from common.framework import Functor
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
import world
from logic.gcommon import time_utility
from logic.gcommon.item.item_const import BATTLE_EFFECT_KILL
from logic.gutils import red_point_utils
from common.cfg import confmgr
ROTATE_FACTOR = 850

class FunctionWidgetBase(object):

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.sel_callback = None
        self.sel_before_cb = None
        return

    def get_parent_selected_item_index(self):
        return self.parent.selected_item_index

    def set_parent_selected_item_index(self, val):
        self.parent.selected_item_index = val

    def set_data(self, data_list, data_dict):
        pass

    def set_select_callback(self, before_cb, cb):
        self.sel_before_cb = before_cb
        self.sel_callback = cb

    def on_clear_effect(self):
        pass

    def on_update_scene(self):
        pass

    def is_panel_visible(self):
        ui_parent = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        return ui_parent and ui_parent.panel.isVisible()

    def on_create_skin_item(self, lst, index, item_widget):
        pass

    def on_remove_skin_item(self, lst, index, item_widget):
        pass

    def on_create_empty_skin_item(self, lst, index, item_widget):
        pass

    def destroy(self):
        self.inited = False
        self.sel_callback = None
        self.sel_before_cb = None
        self.panel.StopTimerAction()
        self.panel = None
        self.parent = None
        return

    def get_default_select_item_no(self):
        return None