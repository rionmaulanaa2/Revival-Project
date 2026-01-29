# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayItemListWidget.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from logic.client.const import mall_const
import logic.gcommon.const as gconst
from logic.gutils import lobby_model_display_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_PET_SKIN
ROTATE_FACTOR = 850
MIN_LIST_NUM = 6

class MallDisplayItemListWidget(WidgetExtModelPic):

    def __init__(self, dlg):
        super(MallDisplayItemListWidget, self).__init__(dlg)
        self.panel = dlg
        self.init_parameters()
        self.init_event()
        self.init_widget()

    def on_finalize_panel(self):
        super(MallDisplayItemListWidget, self).destroy()
        self.process_event(False)

    def set_show(self, show):
        self.panel.setVisible(show)
        self.do_show_panel()

    def do_show_panel(self):
        pass

    def init_parameters(self):
        self.goods_items = []
        self.goods_price_infos = {}
        self._cur_page_index = None
        self._cur_sub_page_index = None
        self._seleted_mall_widget = None
        self._select_index = 0
        self.select_goods_id = None
        self.cur_filter_widegt = None
        self.cur_filter_item_no = None
        self._filter = lambda x: True
        return

    def init_event(self):
        self.process_event(True)

    def get_event_conf(self):
        return {'player_money_info_update_event': self._on_player_info_update}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = self.get_event_conf()
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self.init_sort_option()
        self.init_own_filter()
        self.init_buy_confirm()
        self.init_display()
        self.init_switch_detail()

    def get_sort_option(self):
        sort_option = [{'name': get_text_local_content(12012)}, {'name': get_text_local_content(12011)}]
        sort_cmp = [
         lambda a, b: self.mall_price_cmp(b, a), lambda a, b: self.mall_price_cmp(a, b)]
        return (
         sort_option, sort_cmp)

    def init_sort_option(self):
        sort_option, sort_cmp = self.get_sort_option()

        def call_back(index):
            self._sort_cmp = sort_cmp[index]
            option = sort_option[index]
            self.panel.btn_sort.SetText(option['name'])
            self.panel.sort_list.setVisible(False)
            self.panel.sort_icon.setRotation(180)
            self.reset_mall_list(is_init=True)

        def close_cb():
            self.panel.sort_icon.setRotation(180)

        template_utils.init_common_choose_list(self.panel.sort_list, sort_option, call_back, close_cb=close_cb)
        self.panel.btn_sort.SetForceHandleTouch(True)

        @self.panel.btn_sort.unique_callback()
        def OnBegin(btn, touch):
            wpos = touch.getLocation()
            if btn.IsPointIn(wpos):
                if self.panel.sort_list.isVisible():
                    self.panel.sort_list.setVisible(False)
                    self.panel.sort_icon.setRotation(180)
                    return False
                return True
            self.panel.sort_list.setVisible(False)
            self.panel.sort_icon.setRotation(180)
            btn.SetSelect(False)
            return False

        @self.panel.btn_sort.unique_callback()
        def OnClick(btn, touch):
            vis = not self.panel.sort_list.isVisible()
            self.panel.sort_list.setVisible(vis)
            if vis:
                self.panel.sort_icon.setRotation(0)
            else:
                self.panel.sort_icon.setRotation(180)

        self._sort_cmp = sort_cmp[0]
        self.panel.btn_sort.SetText(sort_option[0]['name'])

    def init_own_filter(self):
        self.btn_filter_select = False
        self.panel.btn_show_own.SetShowEnable(not self.btn_filter_select)

        @self.panel.btn_show_own.unique_callback()
        def OnClick(btn, touch):
            self.btn_filter_select = not self.btn_filter_select
            btn.SetShowEnable(not self.btn_filter_select)
            self.reset_mall_list(is_init=True)

    def init_item_filter(self):
        self.cur_filter_widegt = None
        filter_lst = mall_utils.get_page_filter_lst(self._cur_page_index, self._cur_sub_page_index)
        if not filter_lst:
            return
        else:
            filter_items = [
             None]
            filter_items.extend(filter_lst)
            list_filter = self.panel.list_filter
            list_filter.SetInitCount(len(filter_items))
            self.panel.img_bar.ResizeAndPosition()
            all_items = list_filter.GetAllItem()
            for index, item_widget in enumerate(all_items):
                item_no = filter_items[index]
                normal_path, select_path = mall_utils.get_filter_btn_frame_path(item_no)
                item_widget.btn_icon_filter.SetFrames('', [normal_path, select_path], False, None)
                item_widget.btn_filter.SetSelect(False)
                item_widget.btn_icon_filter.SetSelect(False)

                @item_widget.btn_icon_filter.unique_callback()
                def OnClick(btn, touch, item_widget=item_widget, filter_item_no=item_no):
                    if self.cur_filter_widegt is not None:
                        self.cur_filter_widegt.btn_filter.SetSelect(False)
                        self.cur_filter_widegt.btn_icon_filter.SetSelect(False)
                    item_widget.btn_filter.SetSelect(True)
                    item_widget.btn_icon_filter.SetSelect(True)
                    self.cur_filter_widegt = item_widget
                    self.cur_filter_item_no = filter_item_no
                    self.reset_mall_list(is_init=True)
                    return

            if all_items:
                item_widget = all_items[0]
                item_widget.btn_filter.SetSelect(True)
                item_widget.btn_icon_filter.SetSelect(True)
                self.cur_filter_widegt = item_widget
                self.cur_filter_item_no = filter_items[0]
            return

    def init_buy_confirm(self):

        @self.panel.btn_buy_all.unique_callback()
        def OnClick(btn, touch):
            if self.select_goods_id is None or mall_utils.item_has_owned_by_goods_id(self.select_goods_id):
                return
            else:
                specail_goods_logic = mall_utils.get_special_goods_logic(self.select_goods_id)
                if specail_goods_logic and specail_goods_logic['buy_callback']:
                    specail_goods_logic['buy_callback']()
                    return
                self.buy_goods()
                return

    def buy_goods(self):
        from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI, item_skin_buy_confirmUI, groceries_buy_confirmUI
        is_item = mall_utils.is_weapon(self.select_goods_id) or mall_utils.is_vehicle(self.select_goods_id)
        is_role_or_skin = mall_utils.is_driver(self.select_goods_id) or mall_utils.is_mecha(self.select_goods_id)
        if is_item:
            ui = item_skin_buy_confirmUI(self.select_goods_id)
        elif is_role_or_skin:
            ui = role_or_skin_buy_confirmUI(self.select_goods_id)
        else:
            ui = groceries_buy_confirmUI(self.select_goods_id)
        mall_ui = global_data.ui_mgr.get_ui('MallMainUI')
        if mall_ui:
            set_buttom_ui_price_nd = getattr(ui, 'set_buttom_ui_price_nd', None)
            if set_buttom_ui_price_nd:
                set_buttom_ui_price_nd(mall_ui.panel.top)
        return

    def init_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def init_switch_detail(self):

        @self.panel.btn_check.unique_callback()
        def OnClick(btn, touch):
            mall_utils.mall_switch_detail(self.select_goods_id)

    def init_mall_list(self, page_index, sub_page_index=None):
        self._cur_page_index = page_index
        self._cur_sub_page_index = sub_page_index
        goods_items = []
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        if self._cur_sub_page_index is not None:
            goods_items = item_page_conf.get(self._cur_sub_page_index, [])
        else:
            for sub_page_conf in six.itervalues(item_page_conf):
                goods_items.extend(sub_page_conf)

        self.goods_price_infos = {}
        for goods_id in goods_items:
            if not mall_utils.is_good_opened(goods_id):
                continue
            self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

        self.panel.mall_list.set_asyncLoad_tick_time(0)
        self.panel.mall_list.set_asyncLoad_interval_time(0.05)
        self.init_item_filter()
        self.reset_mall_list(is_init=True)
        return

    def jump_to_goods_id(self, goods_id):
        if not goods_id:
            return
        self.goods_items = self.get_mall_items()
        if not self.goods_item:
            return
        try:
            index = self.goods_item.index(goods_id)
        except:
            index = 0

        mall_list = self.panel.mall_list
        self.init_select_mall_item(index)
        mall_list.scroll_Load()

    def reset_mall_list(self, is_init=False):
        self._seleted_mall_widget = None
        mall_list = self.panel.mall_list
        self.goods_item = self.get_mall_items()
        show_count = max(len(self.goods_item), MIN_LIST_NUM)

        @mall_list.unique_callback()
        def OnCreateItem(lv, index, item_widget):
            self.cb_create_item(index, item_widget)

        off_set = mall_list.GetContentOffset()
        mall_list.SetInitCount(show_count)
        all_items = mall_list.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.cb_create_item(index, widget)

        if len(self.goods_item):
            if is_init:
                self.init_select_mall_item(0)
            else:
                self.init_select_mall_item(self._select_index, off_set)
        else:
            global_data.emgr.change_model_display_scene_item.emit(None)
        mall_list.scroll_Load()
        return

    def init_select_mall_item(self, index, off_set=None):
        mall_list = self.panel.mall_list
        index = min(index, len(self.goods_item) - 1)
        if not off_set:
            mall_list.LocatePosByItem(index)
        else:
            mall_list.SetContentOffset(off_set)
        select_widget = mall_list.GetItem(index)
        if select_widget is None:
            select_widget = mall_list.DoLoadItem(index)
        select_widget and select_widget.bar.OnClick(None)
        return

    def _check_show_video_btn(self, goods_id):
        if self.panel.nd_show_video is None:
            return
        else:
            from common.platform.dctool import interface
            flag = not interface.is_mainland_package() and (goods_id.startswith('2018010') or goods_id == '101008010')
            self.panel.nd_show_video.setVisible(flag)
            if flag:

                @self.panel.nd_show_video.btn_show_video.unique_callback()
                def OnClick(*args):
                    from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_JA
                    language = get_cur_text_lang()
                    if language == LANG_CN or language == LANG_ZHTW:
                        url = 'https://www.youtube.com/watch?v=NAN5YkTHkT8'
                    elif language == LANG_JA:
                        url = 'https://www.youtube.com/watch?v=1nZODb_Waq8'
                    else:
                        url = 'https://www.youtube.com/watch?v=HYD6J4_TRkQ'
                    import game3d
                    game3d.open_url(url)

            return

    def cb_create_item(self, index, item_widget):
        if index < len(self.goods_item):
            goods_id = self.goods_item[index]
        else:
            goods_id = None
        template_utils.init_mall_item(item_widget, goods_id)
        if goods_id is None:
            item_widget.bar.SetEnable(False)
        else:
            item_widget.bar.SetEnable(True)
            if item_widget.nd_new:
                is_new_arrival = confmgr.get('c_mall_new_arrival_conf', goods_id, 'cShowNewHint', default=False)
                item_widget.nd_new.setVisible(bool(is_new_arrival))

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, index=index, goods_id=goods_id, item_widget=item_widget):
                if goods_id is None:
                    return
                else:
                    self._check_show_video_btn(goods_id)
                    self._select_index = index
                    mall_utils.show_model_display_scene(goods_id)
                    item_no = mall_utils.get_goods_item_no(goods_id)
                    model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
                    item_type = item_utils.get_lobby_item_type(item_no)
                    if item_type == L_ITEM_TYPE_PET_SKIN:
                        for mdata in model_data:
                            mdata['off_position'] = [
                             0, 10, 0]

                    is_show_model = bool(model_data)
                    self.selete_product(item_widget, goods_id, is_show_model)
                    if is_show_model:
                        self.ext_show_item_model(model_data, goods_id, item_no)
                    return

        return

    def selete_product(self, mall_widget, goods_id, is_show_model=True):
        if not is_show_model:
            self.ext_not_show_no_model()
        global_data.emgr.select_mall_goods.emit(goods_id)
        if self._seleted_mall_widget and not self._seleted_mall_widget.IsDestroyed():
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        specail_goods_logic = mall_utils.get_special_goods_logic(goods_id)
        show_price = specail_goods_logic or True if 1 else specail_goods_logic['show_price']
        btn_buy_txt = specail_goods_logic or '' if 1 else specail_goods_logic['btn_buy_txt']
        is_valid = mall_utils.is_valid_goods(goods_id)
        btn_buy_txt = btn_buy_txt if is_valid else 81137
        is_open, _ = mall_utils.get_goods_is_open(goods_id)
        btn_buy_txt = btn_buy_txt if is_open else 81154
        self.select_goods_id = goods_id
        mall_widget.setLocalZOrder(2)
        self._seleted_mall_widget = mall_widget
        self._seleted_mall_widget.choose.setVisible(True)
        if show_price:
            template_utils.init_price_view(self.panel.temp_price, goods_id, mall_const.DARK_PRICE_COLOR)
            self.panel.temp_price.setVisible(True)
            self.panel.btn_buy_all.SetTextOffset({'x': '50%90','y': '50%'})
        else:
            self.panel.temp_price.setVisible(False)
            self.panel.btn_buy_all.SetTextOffset({'x': '50%','y': '50%'})
        owned = mall_utils.item_has_owned_by_goods_id(goods_id)
        self.panel.btn_buy_all.setVisible(not owned)
        self.panel.btn_buy_all.SetEnable(is_valid and is_open)
        if btn_buy_txt:
            self.panel.btn_buy_all.SetText(btn_buy_txt)
        else:
            self.panel.btn_buy_all.SetText(80166)
        self.panel.nd_item_describe.setVisible(is_show_model)
        self.panel.nd_item_check.setVisible(is_show_model)
        self.panel.nd_common_reward and self.panel.nd_common_reward.setVisible(not is_show_model)
        if is_show_model:
            belong_item_name = mall_utils.get_goods_belong_item_name(goods_id) or ''
            item_name = mall_utils.get_goods_name(goods_id) or ''
            if belong_item_name:
                self.panel.nd_item_describe.lab_name.SetString(''.join([belong_item_name, '\xc2\xb7', item_name]))
            else:
                self.panel.nd_item_describe.lab_name.SetString(item_name)
            item_utils.check_skin_tag(self.panel.nd_item_describe.nd_kind, None, goods_id)
            self.refresh_detail_btn()
        elif self.panel.nd_common_reward:
            self.panel.img_item.SetDisplayFrameByPath('', mall_utils.get_goods_pic_path(goods_id))
            self.panel.nd_common_reward.lab_name.SetString(mall_utils.get_goods_name(goods_id))
            self.panel.nd_common_reward.lab_describe.SetString(mall_utils.get_goods_decs(goods_id))
        self.show_installment_info(owned)
        return

    def refresh_detail_btn(self):
        btn_check = self.panel.btn_check
        if not btn_check:
            return
        btn_check.setVisible(mall_utils.has_detail_info(self.select_goods_id))

    def show_installment_info(self, owned):
        if not self.panel.temp_mech_try:
            return
        if not mall_utils.is_ticket_permanent_discount(self.select_goods_id):
            self.panel.temp_mech_try.setVisible(False)
            return
        num_7day_goods = mall_utils.get_7day_goods_num(self.select_goods_id)
        txt_id = 12106 if mall_utils.is_max_7day_goods_num(self.select_goods_id) else 12104
        template_utils.show_installment_info(bool(num_7day_goods) and not owned, self.panel.temp_mech_try, self.select_goods_id, txt_id)

    def _on_player_info_update(self, *args):
        template_utils.init_price_view(self.panel.temp_price, self.select_goods_id, mall_const.DARK_PRICE_COLOR)

    def mall_price_cmp(self, goods_id1, goods_id2):
        price1_infos = self.goods_price_infos.get(goods_id1)
        price2_infos = self.goods_price_infos.get(goods_id2)
        price1_info = {}
        if price1_infos:
            price1_info = price1_infos[0]
        price2_info = {}
        if price2_infos:
            price2_info = price2_infos[0]
        goods1_payment = price1_info.get('goods_payment', gconst.SHOP_PAYMENT_GOLD)
        goods2_payment = price2_info.get('goods_payment', gconst.SHOP_PAYMENT_GOLD)
        goods1_payment_type = mall_utils.get_payment_type(goods1_payment)
        goods2_payment_type = mall_utils.get_payment_type(goods2_payment)
        real_price1 = price1_info.get('real_price', 0)
        real_price2 = price2_info.get('real_price', 0)
        goods1_rare_degree = item_utils.get_item_rare_degree(mall_utils.get_goods_item_no(goods_id1)) or 0
        goods2_rare_degree = item_utils.get_item_rare_degree(mall_utils.get_goods_item_no(goods_id2)) or 0
        if goods1_rare_degree != goods2_rare_degree:
            return goods1_rare_degree - goods2_rare_degree
        item_utils.get_item_rare_degree(mall_utils.get_goods_item_no(goods_id2)) or 0
        if goods1_payment_type == goods2_payment_type:
            return real_price1 - real_price2
        return goods2_payment_type - goods1_payment_type

    def get_mall_items(self):
        items = six_ex.keys(self.goods_price_infos)
        items.sort(key=cmp_to_key(self._sort_cmp))

        def _new_sort--- This code section failed: ---

 452       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_mall_new_arrival_conf'
           9  LOAD_CONST            2  'cShowNewHint'
          12  LOAD_CONST            3  'default'
          15  LOAD_GLOBAL           2  'False'
          18  CALL_FUNCTION_259   259 
          21  UNARY_NOT        
          22  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18

        items.sort(key=_new_sort)

        def _owned_sort(goods_id):
            return mall_utils.item_has_owned_by_goods_id(goods_id)

        items.sort(key=_owned_sort)
        if self.btn_filter_select:
            final_items = []
            for goods_id in items:
                if not _owned_sort(goods_id):
                    final_items.append(goods_id)

            items = final_items
        if self.cur_filter_item_no:
            final_items = []
            for goods_id in items:
                belong_id = item_utils.get_lobby_item_belong_no(goods_id)
                if belong_id == self.cur_filter_item_no:
                    final_items.append(goods_id)

            items = final_items
        return items