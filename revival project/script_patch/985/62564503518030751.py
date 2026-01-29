# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallCommonItemListWidget.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from logic.gutils import template_utils
from common.const.uiconst import BG_ZORDER
from logic.gutils import mall_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.client.const import mall_const

class MallCommonItemListWidget(object):
    TYPE_TXT_IDS = []
    TYPES = []

    def __init__(self, dlg):
        self.panel = dlg
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('common/bg_full_screen_bg', BG_ZORDER)
        self.change_bg_ui_img_bg()
        self.init_parameters()
        self.init_event()
        self.init_widget()

    def get_bg_ui(self):
        if self.bg_ui and self.bg_ui.is_valid():
            return self.bg_ui

    def change_bg_ui_img_bg(self):
        if self.panel.GetTemplatePath() != 'mall/i_mall_content_item':
            return
        img_bg = getattr(self.bg_ui, 'img_bg')
        if img_bg:
            img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/bg_monthlypass.png')

    def on_finalize_panel(self):
        self.get_bg_ui() and self.get_bg_ui().close()
        self.process_event(False)

    def set_show(self, show):
        self.panel.setVisible(show)
        self.get_bg_ui() and self.get_bg_ui().setVisible(show)

    def do_show_panel(self):
        self.get_bg_ui() and self.get_bg_ui().setVisible(True)

    def do_hide_panel(self):
        self.get_bg_ui() and self.get_bg_ui().setVisible(False)

    def init_parameters(self):
        self.goods_items = []
        self.goods_price_infos = {}
        self._cur_page_index = None
        self._cur_sub_page_index = None
        self.cur_tab_index = None
        return

    def init_event(self):
        self.process_event(True)

    def init_widget(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_meow_capacity_lv': self.reset_mall_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def is_meow_shop(self):
        return self._cur_page_index == mall_const.MEOW_ID

    def init_mall_list(self, page_index, sub_page_index=None):
        self._cur_page_index = page_index
        self._cur_sub_page_index = sub_page_index
        self.panel.nd_title.setVisible(self.is_meow_shop())

        @self.panel.btn_help.unique_callback()
        def OnClick(btn, touch):
            if self.is_meow_shop():
                from logic.gcommon.common_const.battle_const import PLAY_TYPE_MEOW_PLAY_TIPS_ID, PLAY_TYPE_MEOW_PLAY_TIPS_ID_STEAM
                from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
                if global_data.channel.is_steam_channel():
                    PlayIntroduceUI(None, PLAY_TYPE_MEOW_PLAY_TIPS_ID_STEAM)
                else:
                    PlayIntroduceUI(None, PLAY_TYPE_MEOW_PLAY_TIPS_ID)
            return

        goods_items = []
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        if self._cur_sub_page_index is not None:
            goods_items = item_page_conf.get(self._cur_sub_page_index, [])
        else:
            for sub_page_conf in six.itervalues(item_page_conf):
                goods_items.extend(sub_page_conf)

        self.goods_price_infos = {}
        cur_host_num = global_data.channel.get_host_num()
        self.alter_goods_info = {}
        for goods_id in goods_items:
            goods_conf = confmgr.get('mall_config', str(goods_id), default={})
            open_hosts = goods_conf.get('open_hosts', [])
            alter_cond = goods_conf.get('alter_cond')
            if open_hosts and cur_host_num not in open_hosts:
                continue
            if alter_cond:
                self.alter_goods_info[goods_id] = alter_cond
                continue
            self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

        self.init_type_list()
        return

    def init_type_list(self):
        top_tab = self.panel.pnl_list_top_tab
        top_tab.SetInitCount(len(self.TYPE_TXT_IDS))
        if self.TYPE_TXT_IDS:
            for index, txt in enumerate(self.TYPE_TXT_IDS):
                node = top_tab.GetItem(index)
                node.nd_multilang_btn.btn_tab.SetText(txt)
                node.btn_tab.BindMethod('OnClick', lambda b, t, index=index: self.select_tab(index))

            self.select_tab(0)
        self.reset_mall_list(is_init=True)

    def select_tab(self, index):
        top_tab = self.panel.pnl_list_top_tab
        num = top_tab.GetItemCount()
        if index >= num:
            index = 0
        if self.cur_tab_index == index:
            return
        else:
            if self.cur_tab_index is not None:
                tab = top_tab.GetItem(self.cur_tab_index)
                tab and tab.btn_tab.SetSelect(False)
            tab = top_tab.GetItem(index)
            tab and tab.btn_tab.SetSelect(True)
            self.cur_tab_index = index
            self.reset_mall_list(is_init=True)
            return

    def alter_goods_price_info(self):
        for goods_id, conf in six.iteritems(self.alter_goods_info):
            cond_func = conf.get('func')
            param = conf.get('param')
            alter_goods_id = conf.get('alter_goods')
            if alter_goods_id not in self.goods_price_infos:
                continue
            cond_func = getattr(mall_utils, cond_func)
            if cond_func(**param):
                self.goods_price_infos.pop(alter_goods_id)
                self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

    def reset_mall_list(self, is_init=False):
        mall_list = self.panel.mall_list
        self.alter_goods_price_info()
        self.goods_items = self.get_mall_items()
        show_count = len(self.goods_items)

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

        if is_init:
            mall_list.ScrollToTop()
        else:
            mall_list.SetContentOffset(off_set)
        mall_list.scroll_Load()

    def cb_create_item(self, index, item_widget):
        goods_id = self.goods_items[index]
        extra_info = None
        if self.panel.GetTemplatePath() == 'mall/i_mall_content_item':
            if extra_info is None:
                extra_info = {}
            extra_info['money_icon_scale'] = 1
        conf = confmgr.get('mall_config', goods_id, default={})
        init_item_func_name = conf.get('cGoodsInfo', {}).get('init_item_func')
        if init_item_func_name:
            init_item_func = getattr(template_utils, init_item_func_name)
            init_item_func and init_item_func(item_widget, goods_id, is_show_kind=False, extra_info=extra_info)
        else:
            template_utils.init_mall_groceries_item(item_widget, goods_id, is_show_kind=False, extra_info=extra_info)
        limite_by_day, _, _ = mall_utils.buy_num_limite_by_day(goods_id)
        limite_by_week, _, _ = mall_utils.buy_num_limite_by_week(goods_id)
        item_widget.nd_sold_out.setVisible(limite_by_day or limite_by_week)
        if goods_id is None:
            item_widget.bar.SetEnable(False)
        else:
            item_widget.bar.SetEnable(True)

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id):
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    return
                conf = confmgr.get('mall_config', goods_id, default={})
                confirmUI_name = conf.get('cGoodsInfo', {}).get('confirmUI')
                if confirmUI_name:
                    from logic.comsys.mall_ui import BuyConfirmUIInterface
                    confirmUI = getattr(BuyConfirmUIInterface, confirmUI_name)
                    confirmUI and confirmUI(goods_id)
                else:
                    from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                    groceries_buy_confirmUI(goods_id)

        return

    def get_mall_items(self):
        items = six_ex.keys(self.goods_price_infos)
        new_items = []
        if self.cur_tab_index is not None:
            tab_type = self.TYPES[self.cur_tab_index]
            if tab_type == 'all':
                new_items = items
            else:
                for goods_id in items:
                    item_no = mall_utils.get_goods_item_no(goods_id)
                    i_type = item_utils.get_lobby_item_type(item_no)
                    if tab_type == i_type or tab_type == 'other' and i_type is None:
                        new_items.append(goods_id)

        else:
            new_items = items

        def my_cmp(x, y):
            item_no_x = mall_utils.get_goods_item_no(x)
            item_no_y = mall_utils.get_goods_item_no(y)
            if item_no_x is None or item_no_y is None:
                return six_ex.compare(int(x), int(y))
            else:
                sort_key_x = item_utils.get_lobby_item_sort_key(item_no_x)
                sort_key_y = item_utils.get_lobby_item_sort_key(item_no_y)
                if sort_key_x == sort_key_y:
                    return six_ex.compare(item_no_x, item_no_y)
                return six_ex.compare(sort_key_y, sort_key_x)

        new_items.sort(key=cmp_to_key(my_cmp))
        return new_items

    def jump_to_goods_id(self, goods_id):
        if not goods_id:
            return
        self.goods_items = self.get_mall_items()
        if not self.goods_items:
            return
        try:
            index = self.goods_items.index(goods_id)
        except:
            index = 0

        mall_list = self.panel.mall_list
        self.init_select_mall_item(index)
        mall_list.scroll_Load()

    def init_select_mall_item(self, index):
        mall_list = self.panel.mall_list
        index = min(index, len(self.goods_items) - 1)
        mall_list.LocatePosByItem(index)
        select_widget = mall_list.GetItem(index)
        if select_widget is None:
            select_widget = mall_list.DoLoadItem(index)
        select_widget and select_widget.bar.OnClick(None)
        return