# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemFilterWidget.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common.framework import Functor
from logic.gutils import item_utils
from logic.gcommon.item import item_const
from logic.gutils import mall_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
KEY_TOTAL = 'ALL'
MAX_LEVEL = 100000

class ItemFilterWidget(object):

    def __init__(self, parent, choose_list_widget, choose_btn, default_str_id, pattern_str_id, on_select_item_cb, arrow_img):
        super(ItemFilterWidget, self).__init__()
        self.valid = True
        self.parent = parent
        self.selected_degree = KEY_TOTAL
        self.selected_index = None
        self.choose_list_widget = choose_list_widget
        self.choose_btn = choose_btn
        self.arrow_img = arrow_img
        self.index_to_degree_map = {}
        self.degree_to_index_map = {}
        self.default_str_id = default_str_id
        self.pattern_str_id = pattern_str_id
        self.on_select_item_cb = on_select_item_cb
        self.valid_degree_list = [item_const.RARE_DEGREE_1, item_const.RARE_DEGREE_2, item_const.RARE_DEGREE_3, item_const.RARE_DEGREE_4, item_const.RARE_DEGREE_5]
        self.valid_degree_list.reverse()
        self.valid_degree_set = set(self.valid_degree_list)
        self.degree_to_items_map = {}
        self.degree_owned_count_map = {}
        self.init_widget()
        return

    def destroy(self):
        self.valid = False
        self.parent = None
        self.choose_list_widget = None
        self.choose_btn = None
        self.on_select_item_cb = None
        self.arrow_img = None
        return

    def get_selected_degree_items(self, filter_can_use=False, sort_by_can_use=False):
        from logic.gutils import dress_utils
        index = self.selected_index or 0
        degree = self.index_to_degree_map[index]
        ret_list = []
        can_use_list = []
        can_use = True
        for k in self.degree_to_items_map[degree]:
            if not sort_by_can_use:
                if filter_can_use:
                    can_use, _ = mall_utils.item_can_use_by_item_no(k)
                if can_use:
                    ret_list.append(k)
            else:
                can_use, _ = mall_utils.item_can_use_by_item_no(k)
                can_skim = item_utils.can_open_show(k)
                if can_use:
                    can_use_list.append(k)
                elif can_skim:
                    ret_list.append(k)

        if can_use_list:
            return can_use_list + ret_list
        return ret_list

    def get_selected_item_str(self):
        index = self.selected_index or 0
        item_widget = self.choose_list_widget.option_list.GetItem(index)
        return (
         item_widget.text1.getString(), item_widget.text2.getString())

    def init_widget(self):
        self.choose_list_widget.setVisible(False)
        if self.arrow_img:
            self.arrow_img.setRotation(0)
        self.choose_btn.BindMethod('OnClick', self.on_click_choose_btn)
        self.choose_list_widget.option_list.BindMethod('OnClick', self.on_create_item)
        self.choose_list_widget.nd_close.BindMethod('OnClick', self.toggle_choose_list_visible)

    def on_click_choose_btn(self, *args):
        self.toggle_choose_list_visible()

    def toggle_choose_list_visible(self, *args):
        if not self.valid:
            return
        new_visible = not self.choose_list_widget.isVisible()
        self.choose_list_widget.setVisible(new_visible)
        angle = 180 if new_visible else 0
        if self.arrow_img:
            self.arrow_img.setRotation(angle)

    def reverse_item_list_by_degree(self, item_list):

        def cmp_item(a, b):
            da = item_utils.get_item_rare_degree(a)
            db = item_utils.get_item_rare_degree(b)
            if not da:
                da = MAX_LEVEL
            if not db:
                db = MAX_LEVEL
            return six_ex.compare(db, da)

        return sorted(item_list, key=cmp_to_key(cmp_item))

    def set_itemlist(self, itemlist):
        self.index_to_degree_map = {}
        self.degree_to_index_map = {}
        self.degree_to_items_map = {}
        self.degree_owned_count_map = {}
        for degree in self.valid_degree_list:
            self.degree_to_items_map[degree] = []
            self.degree_owned_count_map[degree] = 0

        self.degree_owned_count_map[KEY_TOTAL] = 0
        self.degree_to_items_map[KEY_TOTAL] = []
        for item_no in itemlist:
            item_degree = item_utils.get_item_rare_degree(item_no)
            can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
            self.degree_to_items_map[KEY_TOTAL].append(item_no)
            if can_use:
                self.degree_owned_count_map[KEY_TOTAL] += 1
            if item_degree in self.valid_degree_set:
                self.degree_to_items_map[item_degree].append(item_no)
                if can_use:
                    self.degree_owned_count_map[item_degree] += 1

        self.degree_to_items_map[KEY_TOTAL] = self.reverse_item_list_by_degree(self.degree_to_items_map[KEY_TOTAL])
        list_index = 1
        self.total_option_count = 1
        for k in self.valid_degree_list:
            if len(self.degree_to_items_map[k]) > 0:
                self.degree_to_index_map[k] = list_index
                self.index_to_degree_map[list_index] = k
                list_index += 1
                self.total_option_count += 1

        self.degree_to_index_map[KEY_TOTAL] = 0
        self.index_to_degree_map[0] = KEY_TOTAL
        self.update_choose_list()

    def on_create_item(self, lst, index, item_widget):
        desc_str = ''
        count_str = '%d/%d'
        if index == 0:
            desc_str = get_text_by_id(self.default_str_id)
            count_str = count_str % (self.degree_owned_count_map[KEY_TOTAL], len(self.degree_to_items_map[KEY_TOTAL]))
        else:
            degree = self.index_to_degree_map[index]
            try:
                desc_str = get_text_by_id(self.pattern_str_id).format(item_utils.get_rare_degree_name(degree))
            except:
                desc_str = ''

            count_str = count_str % (self.degree_owned_count_map[degree], len(self.degree_to_items_map[degree]))
        item_widget.text1.SetString(desc_str)
        item_widget.text2.SetString(count_str)
        item_widget.text1.setVisible(True)
        item_widget.text2.setVisible(True)
        item_widget.button.SetText('')
        item_widget.button.BindMethod('OnClick', Functor(self.on_click_list_item, index))

    def on_click_list_item(self, index, *args):
        if not self.valid:
            return
        self.selected_index = index
        self.selected_degree = self.index_to_degree_map[index]
        self.toggle_choose_list_visible()
        if self.on_select_item_cb:
            self.on_select_item_cb()

    def update_choose_list(self):
        item_list = self.choose_list_widget.option_list
        item_list.SetInitCount(self.total_option_count)
        all_items = item_list.GetAllItem()
        for index, widget in enumerate(all_items):
            self.on_create_item(item_list, index, widget)

        if self.selected_degree is not None and len(self.degree_to_items_map[self.selected_degree]) == 0:
            self.selected_degree = KEY_TOTAL
            self.selected_index = 0
        else:
            self.selected_index = self.degree_to_index_map[self.selected_degree]
        return