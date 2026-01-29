# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryShopWidget.py
from __future__ import absolute_import
from six.moves import range
import six
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import GOODS_CHECK_OWN_TYPE, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, ITEM_TYPE_DEC
from logic.gutils import dress_utils
from logic.gutils.lobby_click_interval_utils import global_unique_click
from common.cfg import confmgr

class LotteryShopWidget(object):

    def __init__(self, panel, parent, on_change_show_reward, lottery_id, show_callback=None, hide_callback=None):
        self.panel = panel
        self.parent = parent
        self.lottery_id = lottery_id
        self.show_callback = show_callback
        self.hide_callback = hide_callback
        self.on_change_show_reward = on_change_show_reward
        self.event_processed = False
        self.init_parameters()
        self.on_init_panel()

    def on_init_panel(self):

        @global_unique_click(self.panel.btn_buy_all)
        def OnClick(btn, touch):
            if self.select_goods_id is None or mall_utils.item_has_owned_by_goods_id(self.select_goods_id):
                return
            else:
                self._on_click_exchange_item(self.select_goods_id)
                return

        self._init_title_text()
        self._init_tab_list()
        self.process_event(False)

    def init_parameters(self):
        from logic.gutils.mall_utils import get_lottery_exchange_list
        self._exchange_lottery_list, _ = get_lottery_exchange_list()
        self.lottery_id2tab_index = {}
        self.select_index = 0
        self._tab_panels = {}
        self._cur_tab_index = None
        self._goods_no_2_mall_ui = {}
        self._price_widget = None
        self._seleted_mall_widget = None
        self.select_goods_id = None
        self._waiting_for_batch_buy_item_list = []
        return

    def process_event(self, flag):
        if self.event_processed == flag:
            return
        self.event_processed = flag
        emgr = global_data.emgr
        econf = {'player_item_update_event': self._on_item_update,
           'buy_good_success': self._on_buy_success
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def parent_show(self, goods_id=None):
        self.show(goods_id)

    def show(self, goods_id=None):
        self.process_event(True)
        self.show_callback and self.show_callback()
        self._init_exchange_mall_list(self._cur_tab_index, goods_id)

    def parent_hide(self):
        self.hide()

    def hide(self):
        self.process_event(False)
        self.hide_callback and self.hide_callback()

    def destroy(self):
        self.process_event(False)

    def _on_item_update(self, *args):
        player = global_data.player
        if not player.requested_buy_goods:
            self._init_exchange_mall_list(self._cur_tab_index)
        if self._waiting_for_batch_buy_item_list and global_data.player:
            lottery_ui = global_data.ui_mgr.get_ui('LotteryMainUI')
            if not lottery_ui:
                return
            skin_id = lottery_ui.cur_show_model_id
            role_id = item_utils.get_lobby_item_belong_no(skin_id)
            for item_no in self._waiting_for_batch_buy_item_list:
                if not global_data.player.has_item_by_no(item_no):
                    return
                self.try_on_item_no(item_no, role_id, skin_id)

            preview_decoration_list = []
            for item_no in self._waiting_for_batch_buy_item_list:
                item_type = item_utils.get_lobby_item_type(item_no)
                if item_type in ITEM_TYPE_DEC:
                    preview_decoration_list.append(item_no)

            current_preview_item = dict(self.get_skin_decoration_data(skin_id, role_id))
            decoration_dict = dress_utils.decoration_list_to_fashion_dict(preview_decoration_list)
            current_preview_item.update(decoration_dict)
            if preview_decoration_list:
                from logic.comsys.role_profile.RoleSkinBuyShowUI import RoleSkinBuyShowUI
                ui = RoleSkinBuyShowUI()
                if ui:
                    ui.set_role_top_skin(role_id, dress_utils.get_top_skin_id_by_skin_id(skin_id), skin_id, None, current_preview_item, decoration_dict)
                    ui.set_close_callback(self.clear_buy_reward_blocking)
            else:
                self.clear_buy_reward_blocking()
        return

    def get_skin_decoration_data(self, skin_id, role_id):
        decoration_data = dress_utils.get_role_fashion_decoration_dict(role_id, skin_id)
        has_set = global_data.player.check_has_set_skin_scheme(role_id, skin_id)
        if not has_set:
            default_show_dict = dress_utils.get_skin_default_show_decoration_dict(skin_id)
            return default_show_dict
        else:
            return decoration_data

    def _on_buy_success(self, *args, **kargs):
        player = global_data.player
        if player.requested_buy_goods:
            self._init_exchange_mall_list(self._cur_tab_index)

    def try_on_item_no(self, item_no, role_id, skin_id):
        has_item = global_data.player.has_item_by_no(item_no)
        if not has_item:
            return
        belong_no = item_utils.get_lobby_item_belong_no(item_no)
        if belong_no != role_id:
            return
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in ITEM_TYPE_DEC:
            fashion_pos = dress_utils.get_lobby_type_fashion_pos(item_type)
            global_data.player.install_role_skin_scheme(role_id, dress_utils.get_top_skin_id_by_skin_id(skin_id), skin_id, {fashion_pos: item_no})

    def clear_buy_reward_blocking(self):
        self._waiting_for_batch_buy_item_list = []
        global_data.emgr.set_reward_show_blocking_item_no_event.emit(self._waiting_for_batch_buy_item_list)

    def _init_tab_list(self):
        exchange_lottery_len = len(self._exchange_lottery_list)
        if not exchange_lottery_len or exchange_lottery_len <= 0:
            return
        self.panel.nd_tab.setVisible(False)
        list_tab = self.panel.nd_tab.list_tab
        list_tab.DeleteAllSubItem()
        self.lottery_id2tab_index = {}
        for tab_index in range(exchange_lottery_len):
            lottery_info = self._exchange_lottery_list[tab_index]
            self.lottery_id2tab_index[lottery_info.get('lottery_id')] = tab_index
            panel = list_tab.AddTemplateItem()
            panel.btn_tab.SetText(get_text_by_id(lottery_info['text_id']))
            self.add_touch_tab(panel, tab_index)

        self._cur_tab_index = self.lottery_id2tab_index.get(str(self.lottery_id), 0)
        self._touch_tab_by_index(self._cur_tab_index, is_force=True)

    def add_touch_tab(self, panel, tab_index):
        self._tab_panels[tab_index] = panel
        panel.btn_tab.EnableCustomState(True)

        @global_unique_click(panel.btn_tab)
        def OnClick(btn, touch, tab_index=tab_index):
            self._touch_tab_by_index(tab_index)
            self._init_exchange_mall_list(tab_index)

    def _touch_tab_by_index(self, tab_index, is_force=False):
        if tab_index == self._cur_tab_index and not is_force:
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

    def _init_exchange_mall_list(self, tab_index, goods_id=None):
        mall_list = self.panel.mall_list_one
        if self._seleted_mall_widget:
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        self.select_goods_id = None
        if goods_id is not None:
            self.select_index = self.get_goods_ui_item_index_by_goods_id(goods_id)
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

            mall_list.LocatePosByItem(self.select_index)
            select_widget = mall_list.GetItem(self.select_index)
            if select_widget is None:
                select_widget = mall_list.DoLoadItem(self.select_index)
            select_widget and select_widget.bar.OnClick(None)
            mall_list.scroll_Load()
            return

    def get_goods_ui_item_index_by_goods_id(self, goods_id):
        goods_item = self._get_goods_items(self._cur_tab_index)
        if not goods_item:
            return
        return goods_item.index(str(goods_id))

    def refresh_buy_btn(self, has_owned):
        self.panel.btn_buy_all.SetEnable(True)
        if item_utils.get_lobby_item_type(mall_utils.get_goods_item_no(self.select_goods_id)) in ITEM_TYPE_DEC:
            self.panel.btn_buy_all.SetText(get_text_by_id(81710))
        else:
            self.panel.btn_buy_all.SetText(get_text_by_id(12017))
        if has_owned:
            self.panel.btn_buy_all.SetEnable(False)
        if not mall_utils.is_good_opened(self.select_goods_id):
            global_data.game_mgr.show_tip(get_text_by_id(12130).format(mall_utils.get_goods_name(self.select_goods_id)))
            self.panel.btn_buy_all.SetEnable(False)

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
            has_owned = False
            if self._check_skin_already_got(goods_id, item_widget):
                has_owned = True
            else:
                limit_num_all = mall_utils.get_goods_limit_num_all(goods_id)
                if limit_num_all > 0:
                    bought_num = global_data.player.get_buy_num_all(goods_id)
                    self._set_goods_buy_limit_info(bought_num, limit_num_all, item_widget)
                    if bought_num >= limit_num_all:
                        has_owned = True
            if goods_id == self.select_goods_id:
                self.refresh_buy_btn(has_owned)
            item_widget.bar.SetEnable(True)

            @global_unique_click(item_widget.bar)
            def OnClick(*args, **kwargs):
                self._on_click_item_widget(index, goods_id, item_widget, tab_index, has_owned)

            return

    def _on_click_item_widget(self, index, goods_id, item_widget, tab_index, has_owned):
        self.select_index = index
        if self._seleted_mall_widget:
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        self.select_goods_id = goods_id
        item_widget.setLocalZOrder(2)
        self._seleted_mall_widget = item_widget
        self._seleted_mall_widget.choose.setVisible(True)
        item_no = mall_utils.get_goods_item_no(goods_id)
        self.on_change_show_reward(item_no)
        if item_utils.get_lobby_item_type(mall_utils.get_goods_item_no(goods_id)) in ITEM_TYPE_DEC:
            role_id = item_utils.get_lobby_item_belong_no(item_no)
            if global_data.player.check_need_request_role_top_skin_scheme(role_id):
                global_data.player.request_role_skin_scheme(role_id)
        self.refresh_buy_btn(has_owned)
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
            ui = role_or_skin_buy_confirmUI(goods_id, close_after_jump=True)
        elif mall_utils.is_weapon(goods_id) or mall_utils.is_vehicle(goods_id):
            ui = item_skin_buy_confirmUI(goods_id)
        else:
            if lobby_i_type in ITEM_TYPE_DEC:
                self._waiting_for_batch_buy_item_list.append(item_no)
            groceries_buy_confirmUI(goods_id)

    def _set_goods_buy_limit_info(self, bought_num, limit_num_all, item_widget):
        if limit_num_all > 0:
            item_widget.lab_exchange_limit.SetString(get_text_by_id(12126).format(bought_num, limit_num_all))
            item_widget.lab_exchange_limit.setVisible(True)
            if bought_num >= limit_num_all:
                item_widget.txt_have.SetString(get_text_by_id(12127))
                item_widget.have.setVisible(True)
                item_widget.nd_price.setVisible(False)
                return
        item_widget.have.setVisible(False)
        item_widget.nd_price.setVisible(True)

    def _check_skin_already_got(self, goods_id, item_widget):
        item_no = mall_utils.get_goods_item_no(goods_id)
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in GOODS_CHECK_OWN_TYPE:
            item_widget.lab_exchange_limit.setVisible(False)
            if mall_utils.item_has_owned_by_goods_id(goods_id):
                item_widget.txt_have.SetString(get_text_by_id(80451))
                item_widget.have.setVisible(True)
                return True
        return False

    def _init_title_text(self):
        lottery_page_conf = confmgr.get('lottery_page_config', self.lottery_id, default={})
        title_text_id = lottery_page_conf.get('extra_data', {}).get('shop_title_text_id')
        if title_text_id:
            self.panel.lab_title.SetString(title_text_id)

    def refresh_show_model(self):
        if self.select_goods_id is None:
            return
        else:
            item_no = mall_utils.get_goods_item_no(self.select_goods_id)
            self.on_change_show_reward(item_no)
            return