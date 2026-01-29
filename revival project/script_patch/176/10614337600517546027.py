# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ListWidgetBase.py
from __future__ import absolute_import
import six_ex
import six
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gutils import items_book_utils
from logic.gutils import lobby_model_display_utils
from logic.gcommon.item import item_const
from logic.comsys.effect import ui_effect
from logic.client.const import mall_const
from logic.client.const import lobby_model_display_const
import time
ROTATE_FACTOR = 850
PER_FRAME_LOAD_TAG = 60001

class ListWidgetBase(object):
    MIN_SKIN_NUM = 6

    def __init__(self, dlg):
        self.panel = dlg
        self.init_parameters()
        self.init_event()
        self.init_widget()

    def on_finalize_panel(self):
        self.process_event(False)

    def set_show(self, show):
        self.panel.setVisible(show)

    def init_parameters(self):
        self.is_bind = False
        self.skin_items = []
        self._cur_page_index = None
        self._seleted_widget = None
        self.select_goods_id = None
        self.select_item_no = None
        self._select_index = 0
        self._filter_index = 0
        self.cur_filter_widget = None
        self.cur_filter_item_no = None
        self._bStartLoad = False
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        if is_bind == self.is_bind:
            return
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.player_item_update,
           'refresh_item_red_point': self.refresh_filter_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self.is_bind = is_bind

    def init_widget(self):
        self.panel.lab_name.SetString('')
        self.panel.lab_describe.SetString('')
        global_data.emgr.change_model_display_scene_item.emit(None)
        self.init_buy_confirm()
        self.init_display()
        self.init_use_skin()
        return

    def do_show_panel(self):
        self.process_event(True)
        self.reset_items_list()

    def do_hide_panel(self):
        self.process_event(False)

    def player_item_update(self):
        self.reset_items_list()

        def _cd():
            if len(self.skin_items) > self._select_index:
                item_no = self.skin_items[self._select_index]
                global_data.player.req_del_item_redpoint(item_no)

        global_data.game_mgr.next_exec(_cd)

    def cb_create_item(self, index, item_widget):
        item_widget.setVisible(True)
        items_conf = items_book_utils.get_items_conf(self._cur_page_index)
        filter_items = six_ex.keys(items_conf)
        item_no = filter_items[index]
        item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        item_widget.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
        item_widget.choose.setVisible(False)
        show_new = global_data.lobby_red_point_data.get_rp_by_belong_no(item_no)
        item_widget.nd_new.setVisible(show_new)
        if not show_new:
            left_time_str = items_book_utils.get_filter_item_left_time_str(self._cur_page_index, item_no)
            if left_time_str:
                item_widget.nd_new.setVisible(True)
                item_widget.nd_new.lab_new.SetString(get_text_by_id(606085))

        @item_widget.bar.unique_callback()
        def OnClick(btn, touch, item_widget=item_widget, filter_index=index, filter_item_no=item_no):
            if self.cur_filter_widget is not None:
                self.cur_filter_widget.choose.setVisible(False)
            self._seleted_widget = None
            item_widget.choose.setVisible(True)
            self.cur_filter_widget = item_widget
            self.cur_filter_item_no = filter_item_no
            is_init = self._filter_index != filter_index
            self._filter_index = filter_index
            self.reset_skins_list(is_init=is_init)
            self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name(self._cur_page_index, filter_item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(filter_item_no))
            return

        if index == self._filter_index:
            item_widget.bar.OnClick(None)
        return

    def refresh_filter_list(self):
        if self._cur_page_index is None:
            return
        else:
            list_item = self.panel.list_item
            all_items = list_item.GetAllItem()
            items_conf = items_book_utils.get_items_conf(self._cur_page_index)
            filter_items = six_ex.keys(items_conf)
            for index, item_widget in enumerate(all_items):
                if type(item_widget) in [dict, six.text_type, str]:
                    continue
                if len(filter_items) <= index:
                    break
                item_no = filter_items[index]
                show_new = global_data.lobby_red_point_data.get_rp_by_belong_no(item_no)
                item_widget.nd_new.setVisible(show_new)
                if not show_new:
                    left_time_str = items_book_utils.get_filter_item_left_time_str(self._cur_page_index, item_no)
                    if left_time_str:
                        item_widget.nd_new.setVisible(True)
                        item_widget.nd_new.lab_new.SetString(get_text_by_id(606085))

            list_skin = self.panel.list_skin
            all_items = list_skin.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                if len(self.skin_items) <= index:
                    break
                item_no = self.skin_items[index]
                show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
                widget.nd_new.setVisible(show_new)

            return

    def show_item_detail(self, item_no):
        pass

    def init_buy_confirm(self):

        @self.panel.btn_buy_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if self.select_goods_id is None or mall_utils.item_has_owned_by_goods_id(self.select_goods_id):
                return
            else:
                from logic.comsys.mall_ui.BuyConfirmUIInterface import item_skin_buy_confirmUI
                item_skin_buy_confirmUI(self.select_goods_id)
                return

    def init_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def init_items_list(self, page_index):
        self._cur_page_index = page_index
        if self.cur_filter_widget is not None:
            self.cur_filter_widget.choose.setVisible(False)
        self.cur_filter_widget = None
        self.reset_items_list(is_init=True)
        return

    def reset_items_list(self, is_init=False):
        if not self._cur_page_index:
            return
        else:
            list_item = self.panel.list_item
            items_conf = items_book_utils.get_items_conf(self._cur_page_index)
            filter_items = six_ex.keys(items_conf)

            @list_item.unique_callback()
            def OnCreateItem(lv, index, item_widget):
                self.cb_create_item(index, item_widget)

            off_set = list_item.GetContentOffset()
            list_item.SetInitCount(len(filter_items))
            all_items = list_item.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                self.cb_create_item(index, widget)

            if len(filter_items):
                if is_init:
                    self.init_select_item(0)
                else:
                    self.init_select_item(self._filter_index, off_set)
            else:
                global_data.emgr.change_model_display_scene_item.emit(None)
            list_item.scroll_Load()
            return

    def reset_skins_list(self, is_init=False):
        if not self.cur_filter_item_no:
            return
        else:
            list_skin = self.panel.list_skin
            self.skin_items = items_book_utils.get_items_skins_by_item_no(self._cur_page_index, self.cur_filter_item_no)
            show_count = max(self.MIN_SKIN_NUM, len(self.skin_items))

            @list_skin.unique_callback()
            def OnCreateItem(lv, index, item_widget):
                self.cb_create_skin_item(index, item_widget)

            off_set = list_skin.GetContentOffset()
            list_skin.SetInitCount(show_count)
            all_items = list_skin.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                self.cb_create_skin_item(index, widget)

            if len(self.skin_items):
                if is_init:
                    self.init_select_skin_item(0)
                else:
                    self.init_select_skin_item(self._select_index, off_set)
            else:
                global_data.emgr.change_model_display_scene_item.emit(None)
            list_skin.scroll_Load()
            return

    def init_select_item(self, index, off_set=None):
        list_item = self.panel.list_item
        items_conf = items_book_utils.get_items_conf(self._cur_page_index)
        filter_items = six_ex.keys(items_conf)
        index = min(index, len(filter_items) - 1)
        if not off_set:
            list_item.LocatePosByItem(index)
        else:
            list_item.SetContentOffset(off_set)
        select_widget = list_item.GetItem(index)
        if select_widget is None:
            select_widget = list_item.DoLoadItem(index)
        if select_widget is None:
            select_widget = list_item.DoLoadItem(index)
        select_widget and select_widget.bar.OnClick(None)
        return

    def init_select_skin_item(self, index, off_set=None):
        list_skin = self.panel.list_skin
        index = min(index, len(self.skin_items) - 1)
        if not off_set:
            list_skin.LocatePosByItem(index)
        else:
            list_skin.SetContentOffset(off_set)
        select_widget = list_skin.GetItem(index)
        if select_widget is None:
            select_widget = list_skin.DoLoadItem(index)
        select_widget and select_widget.bar.OnClick(None)
        return

    def cb_create_skin_item(self, index, item_widget):
        if index < len(self.skin_items):
            item_widget.nd_content.setVisible(True)
            item_no = self.skin_items[index]
            item_widget.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            item_widget.choose.setVisible(False)
            item_fashion_no = self.get_item_fashion_no()
            item_widget.img_using.setVisible(item_fashion_no == int(item_no))
            goods_id = items_book_utils.get_items_skin_conf(self._cur_page_index).get(item_no, {}).get('goods_id')
            item_can_use, limit_left_timestamp = mall_utils.item_can_use_by_item_no(item_no)
            item_widget.img_lock.setVisible(not item_can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, item_no)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            item_widget.nd_new.setVisible(show_new)
            template_utils.show_remain_time(item_widget.lab_limited, item_widget.lab_limited, item_no)

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, index=index, goods_id=goods_id, item_no=item_no, item_widget=item_widget, show_new=show_new):
                self._select_index = index
                from logic.gcommon.common_const import scene_const
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
                self.selete_skin(item_widget, goods_id, item_no)
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
                global_data.emgr.change_model_display_scene_item.emit(model_data)
                if show_new:
                    global_data.player.req_del_item_redpoint(item_no)
                    item_widget.nd_new.setVisible(False)

        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)

    def get_item_fashion_no(self):
        item_fashion = None
        if global_data.player:
            item_fashion = global_data.player.get_battle_item_fashion()
        item_fashion_no = -1
        if item_fashion:
            item_fashion_no = item_fashion.get(str(self.cur_filter_item_no), {}).get(item_const.WEAPON_FASHION_PART_SUIT)
        return item_fashion_no

    def selete_skin(self, item_widget, goods_id, item_no):
        global_data.emgr.select_item_goods.emit(goods_id)
        if self._seleted_widget and self._seleted_widget.isValid():
            self._seleted_widget.setLocalZOrder(0)
            self._seleted_widget.choose.setVisible(False)
            self._seleted_widget = None
        self.select_goods_id = goods_id
        self.select_item_no = item_no
        item_widget.setLocalZOrder(2)
        self._seleted_widget = item_widget
        self._seleted_widget.choose.setVisible(True)
        self.refresh_btn(goods_id, item_no)
        return

    def refresh_btn(self, goods_id, item_no):
        if goods_id:
            template_utils.init_price_view(self.panel.temp_price, goods_id)
        item_can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
        can_buy = bool(goods_id) and not item_can_use
        self.panel.btn_buy_1.setVisible(can_buy)
        item_fashion_no = self.get_item_fashion_no()
        can_use = item_can_use and item_fashion_no != int(item_no)
        self.panel.btn_use.setVisible(can_use)
        self.panel.btn_use.btn_common_big.SetEnable(item_can_use and item_fashion_no != int(item_no))
        can_jump = item_utils.can_jump_to_ui(item_no)
        jump_txt = item_utils.get_item_access(item_no)
        self.panel.lab_get_method.SetString(jump_txt or '')
        self.panel.btn_go.setVisible(can_jump and not can_buy and not can_use and item_fashion_no != int(item_no))
        is_valid = items_book_utils.is_valid_item(item_no)
        self.panel.btn_go.btn_common_big.SetEnable(is_valid)
        self.panel.btn_go.btn_common_big.SetText(get_text_by_id(2222) if is_valid else get_text_by_id(81137))
        return can_use

    def init_use_skin(self):

        @self.panel.btn_use.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if self.select_item_no is None or self.cur_filter_item_no is None:
                return
            else:
                if not self.refresh_btn(self.select_goods_id, self.select_item_no):
                    return
                fashion_dict = {item_const.WEAPON_FASHION_PART_SUIT: self.select_item_no}
                global_data.player and global_data.player.try_dress_battle_item_fashion(str(self.cur_filter_item_no), fashion_dict)
                return

        @self.panel.btn_go.btn_common_big.callback()
        def OnClick(btn, touch):
            item_utils.jump_to_ui(self.select_item_no)

    def jump_to_item_no(self, item_no):
        if not item_no:
            return
        belong_no = item_utils.get_lobby_item_belong_no(item_no)
        if belong_no:
            items_conf = items_book_utils.get_items_conf(self._cur_page_index)
            filter_items = six_ex.keys(items_conf)
            if not filter_items:
                return
            try:
                index = filter_items.index(str(belong_no))
            except:
                index = 0

            list_item = self.panel.list_item
            self.init_select_item(index)
            list_item.scroll_Load()
            if not self.skin_items:
                return
            try:
                index = self.skin_items.index(str(item_no))
            except:
                index = 0

            list_skin = self.panel.list_skin
            self.init_select_skin_item(index)
            list_skin.scroll_Load()