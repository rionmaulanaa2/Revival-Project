# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayGiftItemsWidget.py
from __future__ import absolute_import
from logic.client.const import mall_const
import logic.gcommon.const as gconst
from logic.gutils import lobby_model_display_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN
ROTATE_FACTOR = 850

class MallDisplayGiftItemsWidget(object):

    def __init__(self, dlg):
        self.panel = dlg
        self.init_parameters()
        self.init_event()
        self.init_widget()

    def on_finalize_panel(self):
        self.process_event(False)
        if self._left_time_widget:
            self._left_time_widget.destroy()
            self._left_time_widget = None
        self._select_item_no = None
        self._item_no_2_widget = None
        return

    def set_show(self, show):
        self.panel.setVisible(show)
        self.do_show_panel()

    def do_show_panel(self):
        pass

    def init_parameters(self):
        self._gift_goods_id = None
        self._cur_page_index = None
        self._cur_sub_page_index = None
        self._select_item_no = None
        self._item_no_2_widget = {}
        self._left_time_widget = None
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self._on_player_info_update,
           'buy_good_success_with_list': self._on_buy_good_success_with_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self.init_buy_confirm()
        self.init_display()
        self.init_switch_detail()

    def init_buy_confirm(self):

        @self.panel.btn_buy_all.unique_callback()
        def OnClick(btn, touch):
            if self._gift_goods_id is None or mall_utils.item_has_owned_by_goods_id(self._gift_goods_id):
                return
            else:
                specail_goods_logic = mall_utils.get_special_goods_logic(self._gift_goods_id)
                if specail_goods_logic and specail_goods_logic['buy_callback']:
                    specail_goods_logic['buy_callback']()
                    return
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(self._gift_goods_id)
                return

    def update_buy_confirm(self, is_time_up=False, is_own_items=False):
        if not global_data.player:
            return
        text_id = 12014
        if is_time_up:
            text_id = 81154
        elif is_own_items:
            text_id = 81137
        if is_time_up or is_own_items or global_data.player.get_buy_num_all(self._gift_goods_id) > 0:
            self.panel.temp_price.setVisible(False)
            self.panel.btn_buy_all.SetTextOffset({'x': '50%','y': '50%'})
            self.panel.btn_buy_all.SetText(get_text_by_id(text_id))
            self.panel.btn_buy_all.SetEnable(False)

    def init_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def init_switch_detail(self):

        @self.panel.btn_check.unique_callback()
        def OnClick(btn, touch):
            mall_utils.mall_switch_detail_by_item_no(self._select_item_no)

    def reset_mall_list(self, is_init=True):
        if is_init:
            return
        if self._select_item_no > 0:
            self.select_goods_item(self._select_item_no)
            return

    def init_mall_list(self, page_index, sub_page_index=None):
        self._cur_page_index = page_index
        self._cur_sub_page_index = sub_page_index
        self._gift_goods_id = self._get_gift_goods_id()
        if not self._gift_goods_id:
            return
        else:
            self._init_left_time_widget()
            template_utils.init_price_view(self.panel.temp_price, self._gift_goods_id, mall_const.DARK_PRICE_COLOR)
            reward_id = mall_utils.get_goods_item_reward_id(self._gift_goods_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            mall_list = self.panel.list_mall_vita
            mall_list.DeleteAllSubItem()
            mall_list.SetInitCount(len(reward_list))
            first_item_no = None
            has_own_role_or_skin = False
            for i, reward_conf in enumerate(reward_list):
                item_no, item_num = reward_conf
                if not first_item_no:
                    first_item_no = item_no
                item_type = item_utils.get_lobby_item_type(item_no)
                if item_type in [L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN] and mall_utils.item_has_owned_by_item_no(item_no):
                    has_own_role_or_skin = True
                temp_item_ui = mall_list.GetItem(i)
                template_utils.init_tempate_mall_vita_item(temp_item_ui, item_no, item_num)
                self._item_no_2_widget[item_no] = temp_item_ui

                @temp_item_ui.btn_box.unique_callback()
                def OnClick(btn, touch, item_no=item_no):
                    if not item_no:
                        return
                    self._on_click_item(item_no)

            if first_item_no:
                self._on_click_item(first_item_no)
            self.update_buy_confirm(is_own_items=has_own_role_or_skin)
            return

    def _on_click_item(self, item_no):
        if self._select_item_no and self._select_item_no != item_no:
            last_temp_item_ui = self._item_no_2_widget.get(self._select_item_no)
            if last_temp_item_ui:
                last_temp_item_ui.nd_choose.setVisible(False)
        temp_item_ui = self._item_no_2_widget.get(item_no)
        if not temp_item_ui:
            return
        else:
            temp_item_ui.nd_choose.setVisible(True)
            self._select_item_no = item_no
            mall_utils.show_model_display_scene(self._gift_goods_id)
            model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
            item_type = item_utils.get_lobby_item_type(item_no)
            if item_type in (L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA):
                self.panel.nd_item_describe.setVisible(True)
                self.panel.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
                item_utils.check_skin_tag(self.panel.nd_kind, item_no, None)
            else:
                self.panel.nd_item_describe.setVisible(False)
            self.panel.nd_item_check.setVisible(mall_utils.has_detail_info(None, item_no))
            if model_data:
                self.panel.nd_item.setVisible(False)
                self.panel.nd_detail.setVisible(False)
                global_data.emgr.change_model_display_scene_item.emit(model_data)
            else:
                global_data.emgr.change_model_display_scene_item.emit(None)
                self.panel.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
                self.panel.img_item.setScaleX(1.3)
                self.panel.img_item.setScaleY(1.3)
                self.panel.nd_item.setVisible(True)
                self.panel.nd_detail.setVisible(True)
                self.panel.nd_detail.lab_item_name.SetString(item_utils.get_lobby_item_name(item_no))
                self.panel.nd_detail.lab_item_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            return

    def select_goods_item(self, item_no):
        self._on_click_item(item_no)

    def _on_player_info_update(self, *args):
        template_utils.init_price_view(self.panel.temp_price, self._gift_goods_id, mall_const.DARK_PRICE_COLOR)

    def _get_gift_goods_id(self):
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        goods_items = item_page_conf.get(self._cur_sub_page_index, [])
        for goods_id in goods_items:
            if not mall_utils.is_good_opened(goods_id):
                continue
            mall_conf = confmgr.get('mall_config', goods_id, default={})
            item_type = mall_conf.get('item_type', 0)
            if item_type == mall_const.REWARD_TYPE:
                return goods_id

        return None

    def _init_left_time_widget(self):
        tab_conf = global_data.lobby_mall_data.get_mall_tag_conf().get(self._cur_page_index)
        if not tab_conf:
            return
        expire_time = tab_conf.get('end_time_val', {}).get(self._cur_sub_page_index, 0)
        if expire_time > tutil.get_server_time():
            format_func = lambda timestamp: get_text_by_id(81924).format(tutil.get_readable_time_2(timestamp))
            self._left_time_widget = LeftTimeCountDownWidget(self.panel, self.panel.lab_time, format_func)
            self._left_time_widget.begin_count_down_time(expire_time, lambda : self._on_time_up())

    def _on_time_up(self):
        self.panel.lab_time.SetString(get_text_by_id(81154))
        self.update_buy_confirm(is_time_up=True)

    def _on_buy_good_success_with_list(self, goods_list):
        if not goods_list:
            return
        if not global_data.player:
            return
        for goods_id, pay_num, goods_type, need_show, reward_list, reason, payment, lucky_list in goods_list:
            if self._gift_goods_id == goods_id:
                self.update_buy_confirm()
                break