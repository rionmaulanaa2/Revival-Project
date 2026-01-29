# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/BattleFlagBgChooseWidget.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.cfg import confmgr
from logic.gutils.template_utils import init_price_view
from logic.gutils import item_utils
from logic.gutils import mall_utils
from logic.client.const import mall_const
from logic.comsys.effect import ui_effect
from logic.gutils import battle_flag_utils
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI

class BattleFlagBgChooseWidget(object):

    def __init__(self, panel, auto_init=True):
        self.panel = panel
        self.auto_init_list = auto_init
        self.on_init_panel()

    def on_init_panel(self):
        self.init_parameters()
        self.init_panel()
        self.process_event(True)

    def process_event(self, is_bind):
        if is_bind == self.is_bind:
            return
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.reset_mall_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self.is_bind = is_bind

    def destroy(self):
        self.process_event(False)
        global_data.emgr.set_battle_flag_frame_event.emit()

    def init_parameters(self):
        self.is_bind = False
        self.battle_flag_bg_config = confmgr.get('battle_flag_bg_config', default={})
        self.flag_bg_data = self.get_bg_items()
        self.select_flag_bg = str(global_data.player.get_battle_flag_frame() if global_data.player else DEFAULT_FLAG_FRAME())
        self.cur_select_index = None
        return

    def init_panel(self):
        self.panel.btn_sure.btn_common.SetEnable(False)
        self.panel.btn_sure.btn_common.SetText(80305)
        self.panel.lab_get_method.setVisible(False)
        self.panel.temp_price.setVisible(False)
        self.panel.img_empty.setVisible(False)
        if self.auto_init_list:
            self.init_item_list()

    def init_item_list(self, list_data=None):
        if list_data:
            self.flag_bg_data = list_data
        flag_lst_nd = self.panel.list_change
        flag_lst_nd.SetInitCount(0)
        flag_lst_nd.SetTemplate('battle_flag/i_frame_item')
        item_count = len(self.flag_bg_data)
        flag_lst_nd.SetInitCount(item_count)
        self.refresh_select_view(True)
        self.panel.lab_item_describe.setVisible(False)

    def reset_mall_list(self):
        self.flag_bg_data = self.get_bg_items()
        self.refresh_select_view()

    def get_bg_items(self):
        items = []
        for item_id, _ in six.iteritems(self.battle_flag_bg_config):
            if item_utils.can_open_show(item_id):
                items.append(item_id)

        def my_cmp(x, y):
            sort_key_x = item_utils.get_item_rare_degree(x)
            sort_key_y = item_utils.get_item_rare_degree(y)
            if sort_key_x == sort_key_y:
                return six_ex.compare(int(x), int(y))
            return six_ex.compare(sort_key_y, sort_key_x)

        items.sort(key=cmp_to_key(my_cmp))

        def _owned_sort(item_id):
            if global_data.player.get_item_by_no(int(item_id)):
                return True
            return False

        items.sort(key=_owned_sort, reverse=True)
        return items

    def set_select_flag(self, index):
        cur_index = None
        if self.select_flag_bg:
            cur_index = self.flag_bg_data.index(self.select_flag_bg)
        self.panel.btn_sure.btn_common.SetEnable(cur_index != index)
        flag_lst_nd = self.panel.list_change
        item_widget = flag_lst_nd.GetItem(index)
        if not item_widget:
            return
        else:
            if self.cur_select_index is not None:
                cur_item_widget = flag_lst_nd.GetItem(self.cur_select_index)
                if cur_item_widget:
                    cur_item_widget.btn.SetSelect(False)
            item_widget.btn.SetSelect(True)
            self.cur_select_index = index
            self.panel.lab_item_describe.setVisible(True)
            cur_select_flag_bg = self.flag_bg_data[self.cur_select_index]
            global_data.emgr.set_battle_flag_frame_event.emit(battle_frame=cur_select_flag_bg)
            self.panel.temp_price.setVisible(False)
            self.panel.lab_get_method.setVisible(False)
            self.panel.lab_item_describe.SetString(item_utils.get_lobby_item_desc(cur_select_flag_bg))
            item_data = global_data.player.get_item_by_no(int(cur_select_flag_bg))
            if item_data:
                self.panel.btn_sure.btn_common.SetText(80305)

                @self.panel.btn_sure.btn_common.callback()
                def OnClick(btn, touch):
                    self.on_click_sure()

            else:
                bg_cnf = self.battle_flag_bg_config.get(cur_select_flag_bg, {})
                goods_id = bg_cnf.get('goods_id')
                if item_utils.can_jump_to_ui(cur_select_flag_bg):
                    jump_txt = item_utils.get_item_access(cur_select_flag_bg)
                    self.panel.lab_get_method.SetString(jump_txt)
                    self.panel.lab_get_method.setVisible(True)
                    self.panel.btn_sure.btn_common.SetText(get_text_by_id(2222))

                    @self.panel.btn_sure.btn_common.callback()
                    def OnClick(btn, touch):
                        self.on_click_goto()

                else:
                    price = None
                    if goods_id:
                        price = mall_utils.get_mall_item_price(goods_id)
                    if price:
                        init_price_view(self.panel.temp_price, goods_id, mall_const.DEF_PRICE_COLOR)
                        self.panel.temp_price.setVisible(True)
                        self.panel.btn_sure.btn_common.SetText(get_text_by_id(12017))

                        @self.panel.btn_sure.btn_common.callback()
                        def OnClick(btn, touch):
                            self.on_click_buy()

                    else:
                        self.panel.btn_sure.btn_common.SetText(get_text_by_id(80828))
                        self.panel.btn_sure.btn_common.SetEnable(False)
                        access_txt = item_utils.get_item_access(cur_select_flag_bg)
                        if access_txt:
                            self.panel.lab_get_method.SetString(access_txt)
                            self.panel.lab_get_method.setVisible(True)
            return

    def on_click_sure(self):
        item_no = self.flag_bg_data[self.cur_select_index]
        self.select_flag_bg = item_no
        self.refresh_select_view()
        global_data.game_mgr.show_tip(81703)
        if global_data.player:
            global_data.player.set_battle_flag_frame(int(self.select_flag_bg))

    def on_click_goto(self):
        item_utils.jump_to_ui(self.flag_bg_data[self.cur_select_index])

    def on_click_buy(self):
        bg_cnf = self.battle_flag_bg_config.get(self.flag_bg_data[self.cur_select_index], {})
        goods_id = bg_cnf.get('goods_id')
        goods_id and groceries_buy_confirmUI(goods_id)

    def refresh_select_view(self, is_click_register=False):
        flag_lst_nd = self.panel.list_change
        all_items = flag_lst_nd.GetAllItem()
        for index, item_widget in enumerate(all_items):
            item_id = self.flag_bg_data[index]
            is_choose = item_id == self.select_flag_bg
            item_widget.img_choose.setVisible(is_choose)
            battle_flag_utils.refresh_battle_frame(item_id, item_widget.img_bottom_frame)
            battle_flag_utils.refresh_battle_front_frame(item_id, item_widget.img_front_frame)
            item_widget.btn.SetText(item_utils.get_lobby_item_name(item_id))
            is_owned = bool(global_data.player.get_item_by_no(int(item_id)))
            item_widget.icon_lock.setVisible(not is_owned)
            ui_effect.set_dark(item_widget.img_bottom_frame, is_choose or not is_owned)
            ui_effect.set_dark(item_widget.img_front_frame, is_choose or not is_owned)
            if is_click_register:

                @item_widget.btn.unique_callback()
                def OnClick(btn, touch, index=index):
                    self.set_select_flag(index)

        if self.cur_select_index is not None:
            self.set_select_flag(self.cur_select_index)
        return

    def set_item_selected(self, item_no):
        if item_no is None:
            return
        else:
            item_no = str(item_no)
            if item_no not in self.flag_bg_data:
                log_error('invalid battle flag !!!', item_no, self.flag_bg_data)
                return
            cur_select_index = self.flag_bg_data.index(item_no)
            if cur_select_index != self.cur_select_index:
                self.set_select_flag(cur_select_index)
            if self.panel.list_change.GetItem(cur_select_index):
                self.panel.list_change.CenterWithNode(self.panel.list_change.GetItem(cur_select_index))
            return