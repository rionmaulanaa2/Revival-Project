# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PetItemListWidget.py
from __future__ import absolute_import
import six

class PetItemListWidget(object):

    def __init__(self, parent, panel, on_create_item_callback, min_skin_count, on_select_equip_item=None, need_set_opacity_zero=False, need_init_select_item=True):
        self.parent = parent
        self.panel = panel
        self.on_click_item_callback = None
        self._on_select_equip_item = on_select_equip_item
        self.min_skin_count = min_skin_count
        self.set_create_item_callback(on_create_item_callback)
        self.need_set_opacity_zero = need_set_opacity_zero
        self.need_init_select_item = need_init_select_item
        return

    def set_create_item_callback(self, cb):
        self.on_create_item_callback = cb

    def update_skin_data(self, skins_list, is_init=True, init_index=0, need_init_select_item=True):
        self.skins_list = skins_list
        self.need_init_select_item = need_init_select_item
        self.init_list(is_init, init_index)

    def destroy(self):
        self.parent = None
        self.on_create_item_callback = None
        self.skins_list = None
        return

    def on_create_item(self, lst, index, item_widget):
        if self.need_set_opacity_zero:
            if item_widget.IsPlayingAnimation('in'):
                item_widget.StopAnimation('in')
            item_widget.setOpacity(0)
        if self.on_create_item_callback:
            self.on_create_item_callback(lst, index, item_widget)

    def click_item(self, index):
        if callable(self._on_select_equip_item):
            item_widget = self.panel.GetItem(index)
            self._on_select_equip_item(self.panel, index, item_widget)

    def init_select_item(self, index, off_set=None):
        if not self.skins_list:
            return
        else:
            list_item = self.panel
            index = max(min(index, len(self.skins_list) - 1), 0)
            select_widget = list_item.GetItem(index)
            if select_widget is None:
                if hasattr(list_item, 'DoLoadItem') and callable(list_item.DoLoadItem):
                    select_widget = list_item.DoLoadItem(index)
            if not (off_set and len(self.skins_list) > 0):
                list_item.LocatePosByItem(index)
            else:
                list_item.SetContentOffsetInDuration(off_set)
            if list_item.IsAsync():
                list_item.scroll_Load()
            select_widget and select_widget.btn_choose.OnClick()
            return

    def init_list(self, is_init=True, select_idx=0):
        list_item = self.panel
        list_item.BindMethod('OnCreateItem', self.on_create_item)
        skin_count = len(self.skins_list)
        off_set_before = list_item.GetContentOffset()
        list_item.SetInitCount(max(skin_count, self.min_skin_count))
        off_set_after = list_item.GetContentOffset()
        if is_init:
            off_set = off_set_after if 1 else off_set_before
            all_items = list_item.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                self.on_create_item(list_item, index, widget)

            if self.need_init_select_item:
                if is_init:
                    self.init_select_item(select_idx)
                else:
                    self.init_select_item(select_idx, off_set)
            if hasattr(list_item, 'scroll_Load') and skin_count > 0 and callable(list_item.scroll_Load):
                list_item.scroll_Load()