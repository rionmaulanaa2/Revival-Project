# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryShopWidgetNew.py
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

class LotteryShopWidgetNew(object):

    def __init__(self, panel, parent, on_change_show_reward, lottery_id, init_goods_id=None):
        self.panel = panel
        self.parent = parent
        self.lottery_id = lottery_id
        self.init_goods_id = init_goods_id
        self.on_change_show_reward = on_change_show_reward
        self.init_parameters()
        self.on_init_panel()
        self.process_event(True)

    def init_parameters(self):
        self._exchange_lottery_list = None
        self._get_exchange_lottery_list()
        self.select_index = 0
        self._goods_no_2_mall_ui = {}
        self._seleted_mall_widget = None
        self.select_goods_id = None
        self._waiting_for_batch_buy_item_list = []
        return

    def on_init_panel(self):
        self.btn_exchange = self.panel.btn_exchange

        @global_unique_click(self.btn_exchange)
        def OnClick(btn, touch):
            if self.select_goods_id is None or mall_utils.item_has_owned_by_goods_id(self.select_goods_id):
                return
            else:
                self._on_click_exchange_item(self.select_goods_id)
                return

        self._init_exchange_mall_list(self.init_goods_id)
        self.init_goods_id = None
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self._on_item_update,
           'buy_good_success': self._on_buy_success
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)

    def _on_item_update(self, *args):
        if not self.parent.IsVisible():
            return
        else:
            player = global_data.player
            if not player.requested_buy_goods:
                self._init_exchange_mall_list()
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
        if not self.parent.IsVisible():
            return
        player = global_data.player
        if player.requested_buy_goods:
            self._init_exchange_mall_list()

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

    def _init_exchange_mall_list(self, goods_id=None):
        list_exchange = self.panel.list_exchange
        if self._seleted_mall_widget:
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        self.select_goods_id = None
        if goods_id is not None:
            self.select_index = self.get_goods_ui_item_index_by_goods_id(goods_id)
        goods_item = self._get_goods_items()
        if not goods_item:
            return
        else:

            @list_exchange.unique_callback()
            def OnCreateItem(lv, index, item_widget):
                self._cb_create_item(index, item_widget)

            list_exchange.SetInitCount(len(goods_item))
            all_items = list_exchange.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                self._cb_create_item(index, widget)

            list_exchange.LocatePosByItem(self.select_index)
            select_widget = list_exchange.GetItem(self.select_index)
            if select_widget is None:
                select_widget = list_exchange.DoLoadItem(self.select_index)
            select_widget and select_widget.bar.OnClick(None)
            return

    def get_goods_ui_item_index_by_goods_id(self, goods_id):
        goods_item = self._get_goods_items()
        if not goods_item:
            return
        return goods_item.index(str(goods_id))

    def refresh_buy_btn(self, has_owned):
        self.btn_exchange.SetEnable(True)
        if item_utils.get_lobby_item_type(mall_utils.get_goods_item_no(self.select_goods_id)) in ITEM_TYPE_DEC:
            self.btn_exchange.SetText(get_text_by_id(81710))
        else:
            self.btn_exchange.SetText(get_text_by_id(12017))
        if has_owned:
            self.btn_exchange.SetEnable(False)
        if not mall_utils.is_good_opened(self.select_goods_id):
            global_data.game_mgr.show_tip(get_text_by_id(12130).format(mall_utils.get_goods_name(self.select_goods_id)))
            self.btn_exchange.SetEnable(False)

    def _cb_create_item(self, index, item_widget):
        if not global_data.player:
            return
        else:
            goods_item = self._get_goods_items()
            if index < len(goods_item):
                goods_id = goods_item[index]
            else:
                goods_id = None
            if goods_id is None:
                item_widget.bar.SetEnable(False)
                return
            self._goods_no_2_mall_ui[goods_id] = item_widget
            template_utils.init_mall_item(item_widget, goods_id, adjust_pos=False, ignore_improve=True)
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
            item_no = mall_utils.get_goods_item_no(goods_id)
            rare_degree = item_utils.get_item_rare_degree(item_no, ignore_imporve=True)
            color = item_utils.REWARD_RARE_COLOR.get(rare_degree, 'orange')
            pic = 'gui/ui_res_2/lottery/img_exchange_{}.png'.format(color)
            item_widget.bar.SetFrames('', [pic, pic, pic])
            item_widget.bar.SetEnable(True)
            item_type = item_utils.get_lobby_item_type(item_no)
            item = item_widget.nd_content.nd_cut.item
            if item_type == L_ITEM_TYPE_MECHA_SKIN or item_type == L_ITEM_TYPE_ROLE_SKIN:
                item.SetPosition('50%0', '50%104')
                item.setScale(0.86)
            else:
                item.SetPosition('50%0', '50%68')
                item.setScale(0.54)

            @global_unique_click(item_widget.bar)
            def OnClick(*args, **kwargs):
                self._on_click_item_widget(index, goods_id, item_widget, has_owned)

            return

    def _on_click_item_widget(self, index, goods_id, item_widget, has_owned):
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

    def _get_exchange_lottery_list(self):
        from logic.gutils.mall_utils import get_lottery_exchange_list
        exchange_lottery_list, _ = get_lottery_exchange_list()
        for lottery_info in exchange_lottery_list:
            if lottery_info['lottery_id'] == self.lottery_id:
                self._exchange_lottery_list = lottery_info

    def _get_goods_items(self):
        if not self._exchange_lottery_list:
            self._get_exchange_lottery_list()
        exchange_goods_list = self._exchange_lottery_list.get('exchange_goods_list', [])
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
                item_widget.have.setVisible(True)
                return True
        return False

    def refresh_show_model(self):
        if self.select_goods_id is None:
            return
        else:
            item_no = mall_utils.get_goods_item_no(self.select_goods_id)
            self.on_change_show_reward(item_no)
            return