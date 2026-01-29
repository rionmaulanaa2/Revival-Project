# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySpringFestival2022ShopWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.item.lobby_item_type import MODEL_DISPLAY_TYPE, RP_SKIN_TYPE, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gcommon.item.lobby_item_type import GOODS_CHECK_OWN_TYPE, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.item_utils import get_lobby_item_type, get_item_rare_degree, get_skin_rare_path_by_rare, check_skin_tag
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import splice_price, init_price_view
from logic.gutils.mall_utils import get_mall_item_price, check_payment, get_goods_pic_path, is_good_opened, get_lottery_exchange_list, get_goods_item_no, get_goods_name, item_has_owned_by_goods_id, get_goods_limit_num_all, is_weapon, is_vehicle, buy_num_limit_by_all
import math
import cc

class LotterySpringFestival2022ShopWidget(object):

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

        @self.panel.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if self.select_goods_id is None or item_has_owned_by_goods_id(self.select_goods_id):
                return
            else:
                self._on_click_exchange_item(self.select_goods_id)
                return

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

    def _on_buy_success(self, *args, **kargs):
        player = global_data.player
        if player.requested_buy_goods:
            self._init_exchange_mall_list(self._cur_tab_index)

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

        @panel.btn_tab.callback()
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
        up_mall_list = self.panel.list_item.GetItem(0).list_0_item
        down_mall_list = up_mall_list.nd_auto_fit.list_1_item
        self.select_goods_id = None
        if goods_id is not None:
            self.select_index = self.get_goods_ui_item_index_by_goods_id(goods_id)
        goods_item = self._get_goods_items(tab_index)
        if not goods_item:
            return
        else:
            up_len = 3
            down_len = len(goods_item) - up_len
            up_mall_list.SetInitCount(up_len)
            down_mall_list.SetInitCount(down_len)
            self.adjust_list_view_size(up_len, down_len)
            for index, widget in enumerate(up_mall_list.GetAllItem()):
                if isinstance(widget, dict):
                    continue
                self._cb_create_item(tab_index, index, widget, True)

            for index, widget in enumerate(down_mall_list.GetAllItem()):
                if isinstance(widget, dict):
                    continue
                self._cb_create_item(tab_index, index + up_len, widget, False)

            mall_list = up_mall_list
            select_idx = self.select_index
            if self.select_index >= 3:
                mall_list = down_mall_list
                select_idx -= 3
            select_widget = mall_list.GetItem(select_idx)
            if select_widget is None:
                select_widget = mall_list.DoLoadItem(select_idx)
            select_widget and select_widget.OnClick(None)
            return

    def adjust_list_view_size(self, up_len, down_len):
        first_node = self.panel.list_item.GetItem(0)
        list_0_item = first_node.list_0_item
        list_1_item = first_node.list_1_item
        one_big_bar = list_0_item.GetItem(0)
        one_small_bar = list_1_item.GetItem(0)
        size1 = one_big_bar.GetConfSize()
        size2 = one_small_bar.GetConfSize()
        if down_len % 3 == 0:
            small_row = down_len / 3
        else:
            small_row = math.ceil(down_len / 3) + 1
        indents = list_0_item.GetVertIndent() * (up_len - 1) + list_1_item.GetVertIndent() * small_row
        size = cc.Size(size1.width, size1.height * up_len + size2.height * small_row + indents)
        first_node.setContentSize(size)
        first_node.ChildRecursionRePosition()
        self.panel.list_item.RefreshItemPos()

    def get_goods_ui_item_index_by_goods_id(self, goods_id):
        goods_item = self._get_goods_items(self._cur_tab_index)
        if not goods_item:
            return
        return goods_item.index(str(goods_id))

    def refresh_buy_btn(self):
        item_price = get_mall_item_price(self.select_goods_id)
        splice_price(self.panel.temp_price, item_price, color=['#SK', '#SR', '#DC'])
        has_owned = item_has_owned_by_goods_id(self.select_goods_id)
        sold_out, _, _ = buy_num_limit_by_all(self.select_goods_id)
        self._enable_buy_btn(True)
        if has_owned or not check_payment(item_price[0]['goods_payment'], item_price[0]['real_price'], pay_tip=False) or sold_out:
            self._enable_buy_btn(False)
        if not is_good_opened(self.select_goods_id):
            self._enable_buy_btn(False)
            global_data.game_mgr.show_tip(get_text_by_id(12130).format(get_goods_name(self.select_goods_id)))
        self.panel.lab_buy.SetString(self._get_item_state_text_id(self.select_goods_id))
        self.panel.btn_buy.SetEnable(True)
        if has_owned:
            self.panel.btn_buy.SetEnable(False)
        if not is_good_opened(self.select_goods_id):
            global_data.game_mgr.show_tip(get_text_by_id(12130).format(get_goods_name(self.select_goods_id)))
            self.panel.btn_buy.SetEnable(False)

    def _enable_buy_btn(self, flag):
        self.panel.btn_buy.SetEnable(flag)
        if self.panel.HasAnimation('button_loop'):
            if flag:
                self.panel.PlayAnimation('button_loop')
            else:
                self.panel.StopAnimation('button_loop')
                self.panel.RecoverAnimationNodeState('button_loop')
        if self.panel.HasAnimation('disappear'):
            if not flag:
                self.panel.PlayAnimation('disappear')

    def _get_item_state_text_id(self, goods_id, item_no=None):
        if item_no is None:
            item_no = get_goods_item_no(goods_id)
        limit_num_all = get_goods_limit_num_all(goods_id)
        bought_num = global_data.player.get_buy_num_all(goods_id)
        item_type = get_lobby_item_type(item_no)
        is_have = item_has_owned_by_goods_id(goods_id)
        if bought_num >= limit_num_all > 0:
            if item_type in RP_SKIN_TYPE:
                return 80451
            else:
                return 12127

        else:
            if is_have:
                return 80451
            return 12074
        return

    def _cb_create_item(self, tab_index, index, item_widget, up):
        if not global_data.player:
            return
        else:
            goods_item = self._get_goods_items(tab_index)
            if index < len(goods_item):
                goods_id = goods_item[index]
            else:
                goods_id = None
            if goods_id is None:
                item_widget.SetEnable(False)
                return
            self._goods_no_2_mall_ui[goods_id] = item_widget
            if not up:
                pic_path = get_goods_pic_path(goods_id)
                item_widget.img_pic.SetDisplayFrameByPath('', pic_path)
            item_widget.lab_name.SetString(get_goods_name(goods_id))
            init_price_view(item_widget.temp_price, goods_id)
            item_no = get_goods_item_no(goods_id)
            rare_degree = get_item_rare_degree(item_no)
            tag_img = get_skin_rare_path_by_rare(rare_degree)
            if tag_img:
                item_widget.img_class.SetDisplayFrameByPath('', tag_img)
            has_owned = False
            if self._check_skin_already_got(goods_id, item_widget):
                has_owned = True
            else:
                limit_num_all = get_goods_limit_num_all(goods_id)
                if limit_num_all > 0:
                    bought_num = global_data.player.get_buy_num_all(goods_id)
                    self._set_goods_buy_limit_info(bought_num, limit_num_all, item_widget)
                    if bought_num >= limit_num_all:
                        has_owned = True
            if goods_id == self.select_goods_id:
                self.refresh_buy_btn()
            item_widget.SetEnable(True)

            @item_widget.unique_callback()
            def OnClick(btn, touch, index=index, goods_id=goods_id, item_widget=item_widget, tab_index=tab_index, has_owned=has_owned):
                self.select_index = index
                if self._seleted_mall_widget:
                    self._seleted_mall_widget.PlayAnimation('empty')
                    self._seleted_mall_widget = None
                self.select_goods_id = goods_id
                self._seleted_mall_widget = item_widget
                self._seleted_mall_widget.PlayAnimation('click')
                self._seleted_mall_widget.vx_choose.setVisible(True)
                item_no = get_goods_item_no(goods_id)
                self.on_change_show_reward(item_no)
                self.refresh_buy_btn()
                return

            return

    def _get_goods_items(self, lottery_index):
        lottery_info = self._exchange_lottery_list[lottery_index]
        exchange_goods_list = lottery_info.get('exchange_goods_list', [])
        return exchange_goods_list

    def _on_click_exchange_item(self, goods_id):
        from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI, item_skin_buy_confirmUI, groceries_buy_confirmUI
        item_no = get_goods_item_no(goods_id)
        lobby_i_type = get_lobby_item_type(item_no)
        if lobby_i_type in [L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN]:
            ui = role_or_skin_buy_confirmUI(goods_id, close_after_jump=True)
        elif is_weapon(goods_id) or is_vehicle(goods_id):
            ui = item_skin_buy_confirmUI(goods_id)
        else:
            groceries_buy_confirmUI(goods_id)

    def _set_goods_buy_limit_info(self, bought_num, limit_num_all, item_widget):
        if limit_num_all > 0 and bought_num >= limit_num_all:
            item_widget.pnl_get.setVisible(True)
            item_widget.lab_get.SetString(12127)
        else:
            item_widget.pnl_get.setVisible(False)

    def _check_skin_already_got(self, goods_id, item_widget):
        item_no = get_goods_item_no(goods_id)
        item_type = get_lobby_item_type(item_no)
        if item_type in GOODS_CHECK_OWN_TYPE:
            if item_has_owned_by_goods_id(goods_id):
                item_widget.pnl_get.setVisible(True)
                return True
        return False

    def refresh_show_model(self):
        if self.select_goods_id is None:
            return
        else:
            item_no = get_goods_item_no(self.select_goods_id)
            self.on_change_show_reward(item_no)
            return