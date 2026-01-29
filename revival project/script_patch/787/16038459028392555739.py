# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryExchangeMallUI.py
from __future__ import absolute_import
from six.moves import range
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER, NORMAL_LAYER_ZORDER_3
from common.cfg import confmgr
from common.const import uiconst
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import RP_SKIN_TYPE, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
import logic.gcommon.const as gconst
from logic.gcommon.common_const import activity_const
import logic.gcommon.time_utility as tutil
from logic.gutils.activity_utils import get_left_time

class LotteryExchangeMallUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/exchange_mall'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, exchange_lottery_list, **kwargs):
        self.init_parameters(exchange_lottery_list)
        self._init_panel()
        self._init_title_text()
        self._init_price_widget()
        self._init_tab_list()
        self.panel.PlayAnimation('appear')
        self.process_event(True)

    def init_parameters(self, exchange_lottery_list):
        self._exchange_lottery_list = exchange_lottery_list
        self._tab_panels = {}
        self._cur_tab_index = None
        self._goods_no_2_mall_ui = {}
        self._price_widget = None
        self._seleted_mall_widget = None
        self.select_goods_id = None
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'buy_good_success_with_list': self._on_buy_good_success_with_list
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)

    def _init_panel(self):

        @self.panel.btn_buy_all.unique_callback()
        def OnClick(btn, touch):
            if self.select_goods_id is None or mall_utils.item_has_owned_by_goods_id(self.select_goods_id):
                return
            else:
                self._on_click_exchange_item(self.select_goods_id)
                return

    def _init_tab_list(self):
        exchange_lottery_len = len(self._exchange_lottery_list)
        if not exchange_lottery_len or exchange_lottery_len <= 0:
            return
        self.panel.nd_tab.setVisible(False)
        list_tab = self.panel.nd_tab.list_tab
        list_tab.DeleteAllSubItem()
        for tab_index in range(exchange_lottery_len):
            lottery_info = self._exchange_lottery_list[tab_index]
            panel = list_tab.AddTemplateItem()
            panel.btn_tab.SetText(get_text_by_id(lottery_info['text_id']))
            self.add_touch_tab(panel, tab_index)

        self._cur_tab_index = 1
        self._touch_tab_by_index(0)

    def add_touch_tab(self, panel, tab_index):
        self._tab_panels[tab_index] = panel
        panel.btn_tab.EnableCustomState(True)

        @panel.btn_tab.callback()
        def OnClick(btn, touch, tab_index=tab_index):
            self._touch_tab_by_index(tab_index)

    def _touch_tab_by_index(self, tab_index):
        if tab_index == self._cur_tab_index:
            return
        tab_panel = self._tab_panels.get(self._cur_tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(False)
            tab_panel.PlayAnimation('unclick')
            tab_panel.img_vx.setVisible(False)
        tab_panel = self._tab_panels.get(tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(True)
            tab_panel.img_vx.setVisible(True)
            tab_panel.PlayAnimation('click')
        self._cur_tab_index = tab_index
        self._init_exchange_mall_list(self.panel.mall_list_one, tab_index)

    def _init_exchange_mall_list(self, mall_list, tab_index):
        if self._seleted_mall_widget:
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        self.select_goods_id = None
        goods_item = self._get_goods_items(tab_index)
        if not goods_item:
            return
        else:

            @mall_list.unique_callback()
            def OnCreateItem(lv, index, item_widget):
                self._cb_create_item(tab_index, index, item_widget)

            mall_list.SetInitCount(len(goods_item))
            all_items = mall_list.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                self._cb_create_item(tab_index, index, widget)

            mall_list.ScrollToTop()
            mall_list.scroll_Load()
            select_widget = mall_list.GetItem(0)
            if select_widget is None:
                select_widget = mall_list.DoLoadItem(0)
            select_widget and select_widget.bar.OnClick(None)
            return

    def _cb_create_item(self, tab_index, index, item_widget):
        if not global_data.player:
            return
        else:
            goods_item = self._get_goods_items(tab_index)
            if index < len(goods_item):
                goods_id = goods_item[index]
            else:
                goods_id = None
            if goods_id is None:
                item_widget.bar.SetEnable(False)
                return
            self._goods_no_2_mall_ui[goods_id] = item_widget
            template_utils.init_mall_item(item_widget, goods_id)
            if self._check_skin_already_got(goods_id, item_widget):
                return
            limit_num_all = mall_utils.get_goods_limit_num_all(goods_id)
            if limit_num_all > 0:
                bought_num = global_data.player.get_buy_num_all(goods_id)
                self._set_goods_buy_limit_info(bought_num, limit_num_all, item_widget)
                if bought_num >= limit_num_all:
                    return
            item_widget.bar.SetEnable(True)

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, index=index, goods_id=goods_id, item_widget=item_widget, tab_index=tab_index):
                if not mall_utils.is_good_opened(goods_id):
                    global_data.game_mgr.show_tip(get_text_by_id(12130).format(mall_utils.get_goods_name(goods_id)))
                    return
                else:
                    if self._seleted_mall_widget:
                        self._seleted_mall_widget.setLocalZOrder(0)
                        self._seleted_mall_widget.choose.setVisible(False)
                        self._seleted_mall_widget = None
                    self.select_goods_id = goods_id
                    item_widget.setLocalZOrder(2)
                    self._seleted_mall_widget = item_widget
                    self._seleted_mall_widget.choose.setVisible(True)
                    return

            return

    def _get_goods_items(self, lottery_index):
        lottery_info = self._exchange_lottery_list[lottery_index]
        exchange_goods_list = lottery_info.get('exchange_goods_list', [])
        return exchange_goods_list

    def _on_click_exchange_item(self, goods_id):
        from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI, item_skin_buy_confirmUI, groceries_buy_confirmUI
        item_no = mall_utils.get_goods_item_no(goods_id)
        lobby_i_type = item_utils.get_lobby_item_type(item_no)
        if lobby_i_type in [L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN]:
            ui = role_or_skin_buy_confirmUI(goods_id)
        elif mall_utils.is_weapon(goods_id) or mall_utils.is_vehicle(goods_id):
            ui = item_skin_buy_confirmUI(goods_id)
        else:
            groceries_buy_confirmUI(goods_id)

    def _on_click_close(self, *args):
        self.close()

    def _on_buy_good_success_with_list(self, goods_list):
        if not goods_list:
            return
        if not global_data.player:
            return
        for goods_id, pay_num, goods_type, need_show, reward_list, reason, payment, lucky_list in goods_list:
            item_widget = self._goods_no_2_mall_ui.get(goods_id)
            if not item_widget:
                continue
            if self._check_skin_already_got(goods_id, item_widget):
                continue
            limit_num_all = mall_utils.get_goods_limit_num_all(goods_id)
            if limit_num_all > 0:
                self._set_goods_buy_limit_info(global_data.player.get_buy_num_all(goods_id), limit_num_all, item_widget)

    def _set_goods_buy_limit_info(self, bought_num, limit_num_all, item_widget):
        if limit_num_all > 0:
            item_widget.lab_exchange_limit.SetString(get_text_by_id(12126).format(bought_num, limit_num_all))
            item_widget.lab_exchange_limit.setVisible(True)
            if bought_num >= limit_num_all:
                item_widget.txt_have.SetString(get_text_by_id(12127))
                item_widget.have.setVisible(True)
                item_widget.nd_price.setVisible(False)
                item_widget.bar.SetEnable(False)
                return
        item_widget.have.setVisible(False)
        item_widget.nd_price.setVisible(True)

    def _init_price_widget(self):
        pass

    def _check_skin_already_got(self, goods_id, item_widget):
        item_no = mall_utils.get_goods_item_no(goods_id)
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in RP_SKIN_TYPE and mall_utils.item_has_owned_by_goods_id(goods_id):
            item_widget.txt_have.SetString(get_text_by_id(80451))
            item_widget.have.setVisible(True)
            item_widget.bar.SetEnable(False)
            return True
        return False

    def _init_title_text(self):
        pass