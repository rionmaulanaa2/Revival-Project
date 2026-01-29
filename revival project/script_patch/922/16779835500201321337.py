# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/OthersListWidget.py
from __future__ import absolute_import
import six
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.items_book_ui.ItemCategoryListWidget import ItemCategoryListWidget
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.QualityListWidget import QualityListWidget
from logic.client.const import items_book_const
from common.framework import Functor
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
OUTLINE_ICON_PATH = 'gui/ui_res_2/catalogue/outline/%s.png'

class OthersListWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.selected_equip_type = None
        self.selected_item_no = None
        self.selectd_item_index = None
        self.selected_equip_list = None
        self.init_data()
        self.init_widget()
        self.init_scene()
        return

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def init_data(self):
        self.data_dict = {}
        self.category_name_id_list = [
         ('equip', 80940),
         ('module', 80941),
         ('consumable', 80942)]
        self.category_icon_list = [
         'img_equipment', 'img_module', 'img_item']
        self.item_dict = items_book_utils.get_others_item_ids(items_book_const.OTHERS_ID)

    def on_create_category_item(self, lst, index, item_widget):
        if not self.panel:
            return
        item_widget.btn.EnableCustomState(True)
        item_widget.btn.SetText(get_text_by_id(self.category_name_id_list[index][1]))
        icon_path = OUTLINE_ICON_PATH % self.category_icon_list[index]
        item_widget.btn.icon.SetDisplayFrameByPath('', icon_path)
        item_widget.btn.icon_sel.SetDisplayFrameByPath('', icon_path)
        item_widget.btn.icon.setVisible(True)
        item_widget.btn.icon_sel.setVisible(False)
        item_widget.btn.SetSelect(False)
        item_widget.btn.BindMethod('OnClick', Functor(self._category_list_widget.on_click_category_item, index))

    def init_widget(self):
        self._equip_quality_list_widget = QualityListWidget(self)
        self._equip_list_widget = SkinItemListWidget(self, self.panel.list_item, self.on_create_equip_item, 12, self._on_select_equip_item)
        self._category_list_widget = ItemCategoryListWidget(self, self.panel.temp_right_tab, self.category_name_id_list, self.click_category_item_callback, items_book_const.OTHERS_ID, self.on_create_category_item, need_show_outline_pic=True)
        self._category_list_widget.init_widget()

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        item_widget = self.panel.list_item.GetItem(index)
        item_data = self.selected_equip_list[index]
        prev_item = self.panel.list_item.GetItem(self.selectd_item_index)
        if prev_item:
            prev_item.setLocalZOrder(0)
            prev_item.choose.setVisible(False)
        self.selectd_item_index = index
        item_widget.setLocalZOrder(2)
        item_widget.choose.setVisible(True)
        self._equip_quality_list_widget.set_item_data(item_data)

    def on_create_equip_item(self, lst, index, item_widget):
        if index < len(self.selected_equip_list):
            item_widget.nd_content.setVisible(True)
            select_item_info = self.selected_equip_list[index]
            skin_no = select_item_info[0]
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
            item_widget.choose.setVisible(False)
            item_widget.img_using.setVisible(False)
            item_widget.img_lock.setVisible(False)
            item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
            item_utils.check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            item_widget.nd_new.setVisible(False)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)

    def _on_select_equip_item(self, lst, index, item_widget):
        item_widget.bar.OnClick(item_widget.bar)

    def click_category_item_callback(self, index, data):
        is_same_item = self.selected_equip_type == data[0]
        self.selected_equip_type = data[0]
        select_idx = is_same_item or 0 if 1 else self.selectd_item_index
        self.selected_equip_list = self.item_dict[self.selected_equip_type]
        self._equip_list_widget.update_skin_data(self.selected_equip_list, not is_same_item, select_idx)

    def jump_to_item_no(self, item_no):
        if item_no is None:
            return
        else:
            cat_idx = self._get_category_idx_by_item_no(item_no)
            if cat_idx is None:
                return
            self._category_list_widget.click_item(cat_idx)
            idx_in_cat = self._get_idx_in_cat_by_item_no(item_no)
            if idx_in_cat is None:
                return
            self._equip_list_widget.click_item(idx_in_cat)
            return

    def _get_category_idx_by_item_no(self, item_no):
        cat_id = self._get_category_id_by_item_no(item_no)
        if cat_id is None:
            return
        else:
            for idx, cat_info in enumerate(self.category_name_id_list):
                if cat_info[0] == cat_id:
                    return idx

            return

    def _get_category_id_by_item_no(self, item_no):
        for cat_name, item_info_list in six.iteritems(self.item_dict):
            for item_info in item_info_list:
                item_no_str = item_info[0]
                if item_no == item_no_str:
                    return cat_name

        return None

    def _get_idx_in_cat_by_item_no(self, item_no):
        for cat_name, item_info_list in six.iteritems(self.item_dict):
            for idx, item_info in enumerate(item_info_list):
                item_no_str = item_info[0]
                if item_no == item_no_str:
                    return idx

        return None

    def destroy(self):
        self._equip_list_widget.destroy()
        self._category_list_widget.destroy()
        self._category_list_widget = None
        self._equip_list_widget.destroy()
        self._equip_list_widget = None
        self._equip_quality_list_widget.destroy()
        self._equip_quality_list_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        return