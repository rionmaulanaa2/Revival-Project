# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/MiaomiaoWidget.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.comsys.items_book_ui.MiaomiaoItemGoUseDismountWidget import MiaomiaoItemGoUseDismountWidget
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

class MiaomiaoWidget(object):
    BALLON_BIND_POINT = 'ballon'
    BALLON_RES_PATH = confmgr.get('script_gim_ref')['ballon_res']

    def __init__(self, parent, panel):
        self.inited = False
        self.parent = parent
        self.panel = panel
        self.selected_item_no = None
        self.selected_skin_list = None
        self.cur_show_model_item_no = None
        self.page_index = items_book_const.MIAOMIAO_ID
        self.selected_skin_idx = None
        self.init_data()
        self.init_scene()
        self.init_widget()
        global_data.emgr.miaomiao_lobby_skin_change += self.on_lobby_skin_change
        return

    def is_panel_visible(self):
        ui_parent = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        return ui_parent and ui_parent.panel.isVisible()

    def init_scene(self):
        if not self.is_panel_visible():
            return
        else:
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY, scene_content_type=scene_const.SCENE_ITEM_BOOK)
            global_data.emgr.change_model_display_scene_item.emit(None)
            return

    def init_data(self):
        self.data_dict = {}
        config = items_book_utils.get_items_conf(self.page_index)
        self.data_dict['miaomiao_items'] = config
        _data_list = sorted(six.iteritems(self.data_dict['miaomiao_items']), key=cmp_to_key(--- This code section failed: ---

  63       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_GLOBAL           2  'int'
           9  LOAD_GLOBAL           1  'compare'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_1       1 
          16  LOAD_GLOBAL           2  'int'
          19  LOAD_FAST             1  'y'
          22  LOAD_CONST            1  ''
          25  BINARY_SUBSCR    
          26  CALL_FUNCTION_1       1 
          29  CALL_FUNCTION_2       2 
          32  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 29
))
        self.data_list = []
        for i, info in enumerate(_data_list):
            if item_utils.can_open_show(info[0], owned_should_show=True):
                self.data_list.append(info)

    def init_widget(self):
        self._item_filter_widget = ItemFilterWidget(self, self.panel.choose_list, self.panel.btn_change, 82291, 81364, self.on_select_filter_item, self.panel.img_arrow)
        self._miaomiao_go_use_dismount_widget = MiaomiaoItemGoUseDismountWidget(self, self.panel.btn_go, self.panel.btn_use, self.panel.btn_dismount, self.panel.btn_preview, self.panel.temp_price)
        self._skin_list_widget = SkinItemListWidget(self, self.panel.list_item, self.on_create_skin_item, 4)
        self.on_default_select(self.data_list)

    def on_lobby_skin_change(self, *args):
        if self._skin_list_widget:
            self._skin_list_widget.update_skin_data(self.selected_skin_list, False, self.selected_skin_idx)

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        else:
            prev_index = self.selected_skin_idx
            self.selected_skin_idx = index
            item_widget = self.panel.list_item.GetItem(index)
            item_no = self.selected_skin_list[index]
            self.selected_item_no = item_no
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            if show_new:
                global_data.player.req_del_item_redpoint(item_no)
                red_point_utils.show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(item_no)
            prev_item = self.panel.list_item.GetItem(prev_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            item_widget.setLocalZOrder(2)
            miaomiao_config = items_book_utils.get_items_conf(self.page_index)
            miaomiao_data = miaomiao_config.get(item_no, {})
            goods_id = miaomiao_data.get('goods_id', None)
            item_widget.choose.setVisible(True)
            self._miaomiao_go_use_dismount_widget.update_target_item_no(self.selected_item_no, goods_id)
            show_pic_path = miaomiao_data.get('show_pic_path', None)
            self.panel.img_item.SetDisplayFrameByPath('', show_pic_path)
            return

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.selected_skin_list) and self.selected_item_no
        if valid:
            item_widget.nd_content.setVisible(True)
            skin_no = self.selected_skin_list[index]
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
            item_widget.choose.setVisible(False)
            cur_use_miaomiao_no = None
            if global_data.player:
                cur_use_miaomiao_no = global_data.player.get_lobby_skin()
            item_widget.img_using.setVisible(str(cur_use_miaomiao_no) == str(skin_no))
            item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(skin_no)
            item_widget.img_lock.setVisible(not item_can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, skin_no)
            item_utils.check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        if item_widget.nd_empty:
            item_widget.nd_empty.setVisible(not valid)
        return

    def init_count_down_time(self, ui_item, end_time):

        def show_count_down():
            now = time_utility.get_server_time()
            seconds = end_time - now
            if seconds < -1:
                self.refresh_widget()
                return
            text = time_utility.get_readable_time_day_hour_minitue(seconds)
            ui_item.lab_limited.SetString(text)
            ui_item.lab_limited.DelayCall(5, lambda : show_count_down())

        show_count_down()

    def refresh_widget(self):
        if self.selected_item_no is None:
            return
        else:
            old_data_list = self.data_list
            self.init_scene()
            self.init_data()
            if old_data_list == self.data_list:
                self._skin_list_widget.update_skin_data(self.selected_skin_list, False, self.selected_skin_idx)
                self.update_select_item_collect_count()
            else:
                self.selected_item_no = None
                self.on_default_select(self.data_list)
            return

    def update_select_item_collect_count(self):
        if not self.selected_item_no:
            return
        desc_str, skin_str = self._item_filter_widget.get_selected_item_str()
        self.panel.lab_collect_skin.SetString(skin_str)
        self.panel.lab_collect_desc.SetString(desc_str)

    def on_default_select(self, data):
        is_same_item = self.selected_item_no == data[0]
        self.selected_item_no = data[0]
        select_idx = is_same_item or 0 if 1 else self.selected_skin_idx
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(self.selected_item_no))
        self._item_filter_widget.set_itemlist([ sort_item_data[0] for sort_item_data in self.data_list ])
        self.selected_skin_list = self._item_filter_widget.get_selected_degree_items()
        item_index = select_idx
        self._skin_list_widget.update_skin_data(self.selected_skin_list, not is_same_item, item_index)
        self.update_select_item_collect_count()

    def on_select_filter_item(self):
        self.selected_skin_list = self._item_filter_widget.get_selected_degree_items()
        item_index = 0
        if global_data.player:
            cur_kill_effect_no = global_data.player.get_lobby_skin()
            try:
                item_index = self.selected_skin_list.index(str(cur_kill_effect_no))
            except:
                pass

        self._skin_list_widget.update_skin_data(self.selected_skin_list, False, item_index)
        self.update_select_item_collect_count()

    def do_hide_panel(self):
        self.panel.StopTimerAction()
        global_data.emgr.change_model_display_scene_tag_effect.emit('')

    def destroy(self):
        global_data.emgr.change_model_display_scene_tag_effect.emit('')
        self.inited = False
        self.panel.StopTimerAction()
        self._skin_list_widget.destroy()
        self._skin_list_widget = None
        self._miaomiao_go_use_dismount_widget.destroy()
        self._miaomiao_go_use_dismount_widget = None
        self.panel = None
        self.parent = None
        self.data_dict = None
        return

    def jump_to_item_no(self, item_no):
        if not item_no:
            return
        try:
            skin_index = self._skin_list_widget.skins_list.index(str(item_no))
            self._skin_list_widget.init_select_item(skin_index)
        except:
            return