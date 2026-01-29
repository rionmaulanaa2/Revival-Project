# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/QualityListWidget.py
from __future__ import absolute_import
from logic.gutils import item_utils
from common.framework import Functor
from common.cfg import confmgr
from logic.gutils import template_utils

class QualityListWidget(object):

    def __init__(self, parent):
        self.parent = parent
        self.init_event()
        self.item_data = None
        self.select_index = None
        return

    def init_event(self):
        self.parent.panel.list_class.BindMethod('OnCreateItem', self.on_create_quality_item)

    def set_item_data(self, item_data):
        self.item_data = item_data
        self.select_index = None
        self.update_widget()
        return

    def on_create_quality_item(self, lst, index, item_widget):
        pass

    def on_click_list_item(self, index, *args):
        prev_item = self.parent.panel.list_class.GetItem(self.select_index)
        if prev_item:
            prev_item.img_choose.setVisible(False)
        item_widget = self.parent.panel.list_class.GetItem(index)
        self.select_index = index
        item_widget.img_choose.setVisible(True)
        lv_items = self.item_data[1].get('lv_lobby_item_no', {})
        battle_items = self.item_data[1].get('battle_item_no')
        self.show_item_info(lv_items[index], battle_items[index])

    def update_widget(self):
        lv_items = self.item_data[1].get('lv_lobby_item_no', {})
        battle_items = self.item_data[1].get('battle_item_no')
        lv_empty = len(lv_items) == 0
        self.parent.panel.list_class.SetInitCount(len(lv_items))
        self.parent.panel.lab_class_sel.setVisible(not lv_empty)
        all_items = self.parent.panel.list_class.GetAllItem()
        for index, item_widget in enumerate(all_items):
            item_conf = confmgr.get('item', str(battle_items[index]))
            item_level = item_conf['iQuality']
            pic = template_utils.get_equipment_quality_pic(item_level)
            item_widget.btn_class.SetFrames('', [pic, pic, pic], True, None)
            item_widget.img_choose.setVisible(False)
            item_widget.btn_class.BindMethod('OnClick', Functor(self.on_click_list_item, index))

        if not lv_empty:
            all_items[0].btn_class.OnClick(None)
        else:
            self.show_item_info(self.item_data[0], battle_items[0])
        return

    def show_item_info(self, item_no, battle_item_no):
        self.parent.panel.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        self.parent.panel.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
        self.parent.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))

    def destroy(self):
        self.parent = None
        return