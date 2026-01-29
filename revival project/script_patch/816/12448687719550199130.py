# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KothCampShopUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.setting_ui.SimpleLabelUIBase import SimpleLabelUIBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gcommon.common_const import shop_const as spc
from logic.gcommon import const
from logic.gutils import koth_shop_utils
from .KothCampShopPlayerWidget import PlayerWeaponInfoWidget, PlayerArmorInfoWidget, PlayerItemInfoWidget, PlayerModuleInfoWidget
TYPE_WEAPON = spc.KING_SHOP_GOODS_TYPE_WEAPON
TYPE_ARMOR = spc.KING_SHOP_GOODS_TYPE_ARMOR
TYPE_PROP = spc.KING_SHOP_GOODS_TYPE_PROP
TYPE_MODULE = spc.KING_SHOP_GOODS_TYPE_MODULE
TYPE_VIHICLE = spc.KING_SHOP_GOODS_TYPE_VIHICLE
LV_1 = '1'
LV_2 = '2'
LV_3 = '3'

class KothCampShopUI(SimpleLabelUIBase):
    PANEL_CONFIG_NAME = 'battle_koth/mall_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    OPEN_SOUND_NAME = 'click_on_the_mall'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'temp_btn_buy.btn_common.OnClick': 'on_click_buy_btn',
       'temp_btn_upgrade.btn_common.OnClick': 'on_click_upgrade_btn',
       'nd_sell.temp_btn_sell.btn_common.OnClick': 'on_click_sell_btn',
       'nd_sell_and_up.temp_btn_sell.btn_common.OnClick': 'on_click_sell_btn'
       }
    GLOBAL_EVENT = {'update_koth_money_info_event': 'update_koth_money_info',
       'on_clothes_data_changed_event': '_on_clothes_data_changed',
       'observer_module_changed_event': 'refresh_modules',
       'on_weapon_data_switched_event': '_on_weapon_data_switched',
       'on_wpbar_switch_cur_event': '_on_weapon_data_changed',
       'on_observer_pick_up_weapon': '_on_weapon_data_changed',
       'on_observer_weapon_deleted': '_on_weapon_data_changed'
       }

    def on_click_close_btn(self, *args):
        self.close()

    def on_init_panel(self):
        self.BUY_ITEM_LEVEL = 1
        self._cur_sel_item = None
        self._cur_sel_goods_num = 0
        self._cur_sel_goods_data = {}
        self._cur_sell_player_item_data = {}
        self._cur_sell_item_num = 0
        self._cur_upgrade_player_item_data = {}
        self._cur_player_widget = None
        self._cur_check_own_items = []
        self._goods_id_to_ui_widget = {}
        self.init_player_money_label()
        self.init_add_sub_widget()
        self._init_menu()
        self.hide_main_ui(exceptions=('BattleInfoUI', ))
        self.panel.temp_btn_buy.btn_common.set_click_sound_name('menu_shop')
        self.panel.temp_btn_sell.btn_common.set_click_sound_name('menu_back')
        self.panel.btn_close.set_click_sound_name('close_on_the_mall')
        return

    def on_finalize_panel(self):
        self.show_main_ui()
        self.destroy_tab_widgets()
        self._goods_id_to_ui_widget = {}
        global_data.ui_mgr.close_ui('KothCampShopReplaceWeaponUI')
        self.destroy_widget('add_sub_widget')

    def init_add_sub_widget(self):
        from logic.comsys.common_ui.PressBtnComponent import PressBtnComponent
        self.add_sub_widget = PressBtnComponent(self.panel.nd_num)

    def _init_menu(self):
        self.label_data = {TYPE_WEAPON: {'text': 18201,'show_func': self.on_switch_to_weapon},TYPE_ARMOR: {'text': 18202,'show_func': self.on_switch_to_armor},TYPE_PROP: {'text': 18203,'show_func': self.on_switch_to_item},TYPE_MODULE: {'text': 18204,'show_func': self.on_switch_to_mecha_module},TYPE_VIHICLE: {'text': 18205,'show_func': self.on_switch_to_vehicle}}
        self._tab_info = {TYPE_WEAPON: {},TYPE_ARMOR: {},TYPE_PROP: {'can_change_num': True,'select_related': False},TYPE_MODULE: {},TYPE_VIHICLE: {'can_change_num': True,'select_related': False}}
        self.tab_player_widget = {TYPE_WEAPON: {'widget': PlayerWeaponInfoWidget,'text': 18207},TYPE_ARMOR: {'widget': PlayerArmorInfoWidget,'text': 18208},TYPE_PROP: {'widget': PlayerItemInfoWidget,'text': 18209},TYPE_MODULE: {'widget': PlayerModuleInfoWidget,'text': 18210},TYPE_VIHICLE: {'widget': PlayerItemInfoWidget,'text': 18211}}
        self.label_type = TYPE_WEAPON
        super(KothCampShopUI, self)._init()

    def on_click_buy_btn(self, btn, touch):
        self.buy_goods(self.BUY_ITEM_LEVEL)

    def buy_goods(self, level):
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            shop_lent = koth_shop_utils.get_cur_shop_lent()
            if not shop_lent:
                return
            empty_pos = None
            goods_id = self._cur_sel_goods_data.get('goods_id', None)
            if not goods_id:
                return
            MAIN_WEAPON_LIST = (const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3)
            if self.label_type == TYPE_WEAPON:
                for pos in MAIN_WEAPON_LIST:
                    weapon_data = player.share_data.ref_wp_bar_mp_weapons.get(pos)
                    if not weapon_data:
                        empty_pos = pos
                        break

                if not empty_pos:
                    from logic.comsys.battle.King.KothCampShopReplaceWeaponUI import KothCampShopReplaceWeaponUI
                    ui_inst = KothCampShopReplaceWeaponUI()
                    if ui_inst:
                        ui_inst.set_sel_goods(self._cur_sel_goods_data)
                    return
                goods_list = [
                 (
                  goods_id, empty_pos, level, 1)]
                shop_lent.send_event('E_CALL_SYNC_METHOD', 'buy_goods', (player.id, goods_list), False, True)
            else:
                goods_list = [
                 (
                  goods_id, 0, level, self._cur_sel_goods_num)]
                shop_lent.send_event('E_CALL_SYNC_METHOD', 'buy_goods', (player.id, goods_list), False, True)
            return

    def upgrade_goods(self):
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            shop_lent = koth_shop_utils.get_cur_shop_lent()
            if not shop_lent:
                return
            item_no = self._cur_upgrade_player_item_data.get('item_no', None)
            goods_id = koth_shop_utils.get_goods_id_by_item_id(item_no)
            level = self._cur_upgrade_player_item_data.get('level')
            pos = self._cur_upgrade_player_item_data.get('position', 0)
            num = self._cur_upgrade_player_item_data.get('num', 1)
            if not goods_id:
                return
            goods_list = [
             (
              goods_id, pos, level, num)]
            shop_lent.send_event('E_CALL_SYNC_METHOD', 'buy_goods', (player.id, goods_list), False, True)
            return

    def sell_goods(self):
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            shop_lent = koth_shop_utils.get_cur_shop_lent()
            if not shop_lent:
                return
            position = self._cur_sell_player_item_data.get('position', 0)
            entity_id = self._cur_sell_player_item_data.get('entity_id', '')
            goods_list = [(self.label_type, entity_id, position, self._cur_sell_item_num)]
            shop_lent.send_event('E_CALL_SYNC_METHOD', 'sell_items', (player.id, goods_list), False, True)
            return

    def on_click_sell_btn(self, btn, touch):
        if self.label_type != TYPE_WEAPON:
            global_data.game_mgr.show_tip('\xe6\x9a\x82\xe4\xb8\x8d\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x87\xba\xe5\x94\xae')
            return
        if self._cur_sell_player_item_data:
            self.sell_goods()

    def on_click_upgrade_btn(self, btn, touch):
        if self._cur_upgrade_player_item_data:
            self.upgrade_goods()

    def on_switch_to_tab(self, tab_type):
        tab_info = self._tab_info.get(tab_type, {})
        self.set_sel_goods(None)
        self.set_cur_sel_item(None)
        self.refresh_tab_data(tab_type)
        self.switch_tab_widget(tab_type)
        return

    def refresh_tab_data(self, tab_type):
        tab_info = self._tab_info.get(tab_type, {})
        init_func = tab_info.get('init_func', self.init_item_ui_item)
        tab_goods = self.get_tab_shop_items(tab_type)
        if self.panel.list_item.GetItemCount() != len(tab_goods):
            self.panel.list_item.SetInitCount(len(tab_goods))
        sorted_items = sorted(six_ex.keys(tab_goods))
        self._goods_id_to_ui_widget = {}
        for idx in range(0, len(sorted_items)):
            ui_item = self.panel.list_item.GetItem(idx)
            goods_data = tab_goods.get(sorted_items[idx])
            init_func(ui_item, goods_data)
            goods_id = goods_data.get('goods_id')
            self._goods_id_to_ui_widget[goods_id] = ui_item

    def switch_tab_widget(self, tab_type):
        if self._cur_player_widget:
            self._cur_player_widget.hide()
        widget_class = self.tab_player_widget.get(tab_type, {}).get('widget', None)
        text = self.tab_player_widget.get(tab_type, {}).get('text')
        if not widget_class:
            return
        else:
            widget = None
            if hasattr(self, widget_class.__name__):
                widget = getattr(self, widget_class.__name__)
            if not widget:
                if widget_class:
                    nd_wrappr = widget_class(self.panel.nd_equip, None)
                    setattr(self, widget_class.__name__, nd_wrappr)
                    self._cur_player_widget = nd_wrappr
            else:
                self._cur_player_widget = widget
            if self._cur_player_widget:
                self._cur_player_widget.show()
                if text:
                    self._cur_player_widget.set_show_tips(text)
            return

    def destroy_tab_widgets(self):
        self._cur_player_widget = None
        for key, widget_class_info in six.iteritems(self.tab_player_widget):
            widget_class = widget_class_info.get('widget', '')
            if not widget_class:
                continue
            if hasattr(self, widget_class.__name__):
                widget = getattr(self, widget_class.__name__)
                if widget:
                    widget.destroy()

        return

    def on_switch_to_weapon(self):
        tab_type = TYPE_WEAPON
        self.set_installed_weapons_goods_id()
        self.on_switch_to_tab(tab_type)

    def on_switch_to_armor(self):
        tab_type = TYPE_ARMOR
        self.set_installed_clothed()
        self.on_switch_to_tab(tab_type)

    def on_switch_to_vehicle(self):
        tab_type = TYPE_VIHICLE
        self.on_switch_to_tab(tab_type)
        tab_goods = self.get_tab_shop_items(tab_type)
        item_ids = self.get_tab_goods_item_nos(tab_goods)
        if self._cur_player_widget:
            self._cur_player_widget.set_only_check_list(item_ids)

    def on_switch_to_mecha_module(self):
        tab_type = TYPE_MODULE
        self.set_installed_modules()
        self.on_switch_to_tab(tab_type)

    def get_tab_goods_item_nos(self, tab_goods, lv_list=(
 LV_1, LV_2, LV_3)):
        item_nos = []
        for goods_id, goods_data in six.iteritems(tab_goods):
            item_dict = goods_data.get('item_dict', {})
            for lv in lv_list:
                item_no = item_dict.get(lv, {}).get('item_no')
                item_nos.append(item_no)

        return item_nos

    def on_switch_to_item(self):
        tab_type = TYPE_PROP
        self.on_switch_to_tab(tab_type)
        tab_goods = self.get_tab_shop_items(tab_type)
        item_ids = self.get_tab_goods_item_nos(tab_goods)
        if self._cur_player_widget:
            self._cur_player_widget.set_only_check_list(item_ids)

    def get_tab_shop_items(self, tab_type):
        from common.cfg import confmgr
        tab_items = confmgr.get('king_shop_config', 'goods_data', str(tab_type), default={})
        return tab_items

    def init_money_label(self, ui_item, item_info, is_enough, colors=('#SW', '#SR')):
        from logic.gutils.koth_shop_utils import init_shop_money_label
        if item_info:
            ui_item.img_money.setVisible(True)
            init_shop_money_label(ui_item, item_info, is_enough, colors)
        else:
            ui_item.img_money.setVisible(False)

    def get_price_dict(self, goods_data):
        price_dict = {}
        price_keys = ['diamond_consumed', 'gold_consumed']
        for k, v in six.iteritems(goods_data):
            if k in price_keys:
                price_dict[k] = v

        return price_dict

    def init_item_ui_item(self, ui_item, goods_data):
        goods_id = goods_data.get('goods_id', None)
        item_no = goods_data.get('item_no', None)
        item_name = item_utils.get_item_name(item_no)
        ui_item.lab_name.setString(item_name)
        is_enough = koth_shop_utils.check_payment(self.get_price_dict(goods_data), self.money_dict)
        self.init_money_label(ui_item, goods_data, is_enough)
        self.init_item_button(ui_item, goods_data)
        if goods_id in self._cur_check_own_items:
            ui_item.img_tick.setVisible(True)
        else:
            ui_item.img_tick.setVisible(False)
        koth_shop_utils.init_mall_item_temp(ui_item.temp_item, {'item_no': item_no,'can_upgrade': False})
        return

    def init_item_button(self, ui_item, goods_data):

        @ui_item.btn_item.callback()
        def OnClick(btn, touch):
            goods_id = goods_data.get('goods_id', None)
            if goods_id not in self._cur_check_own_items:
                self.on_player_choose_own_item(None)
                self.set_sel_goods(goods_data)
                self.set_goods_id_widget_selected(goods_id)
            else:
                self.on_player_select_goods_id(goods_id)
            return

    def on_player_select_goods_id(self, goods_id):
        if self._cur_player_widget:
            item_info = self._cur_player_widget.get_goods_id_to_owned_item_no(goods_id)
            item_no = item_info.get('item_no')
            position = item_info.get('position', 0)
            if item_no:
                self.on_player_choose_own_item(item_no, position)

    def set_cur_sel_item(self, item):
        if self._cur_sel_item is not None and self._cur_sel_item.isValid():
            self._cur_sel_item.temp_item.img_select.setVisible(False)
            self._cur_sel_item.setLocalZOrder(0)
        self._cur_sel_item = item
        if self._cur_sel_item:
            self._cur_sel_item.temp_item.img_select.setVisible(True)
            self._cur_sel_item.setLocalZOrder(1)
        return

    def set_sel_goods(self, goods_data):
        if goods_data:
            self._cur_sel_goods_data = goods_data
            self.set_sel_good_num(1)
            num_show = self._tab_info.get(self.label_type, {}).get('can_change_num', False)
            self.panel.nd_num.setVisible(num_show)
            self.add_sub_widget.set_args({'min_num': 1,
               'max_num': 99,
               'per_num': 1,
               'begin_num': 1,
               'begin_ttf': 1
               })
            self.add_sub_widget.set_num_change_callback(self.on_buy_num_changed)
        else:
            self._cur_sel_goods_data = {}
            self._pay_money_data = {}
            self.panel.nd_num.setVisible(False)
        self.update_financial_btns()
        self.show_sel_goods_details(self._cur_sel_goods_data)

    def set_sel_good_num(self, num):
        self._cur_sel_goods_num = num
        self._pay_money_data = self.cal_price(self._cur_sel_goods_data, num)
        self.panel.lab_num.SetString(str(num))

    def cal_price(self, good_data, num):
        diamond_consumed = good_data.get('diamond_consumed', 0)
        gold_consumed = good_data.get('gold_consumed', 0)
        return {'diamond_consumed': int(diamond_consumed * num),'gold_consumed': int(gold_consumed * num)}

    def add_price(self, goods_data1, goods_data2):
        diamond_consumed1 = goods_data1.get('diamond_consumed', 0)
        gold_consumed1 = goods_data1.get('gold_consumed', 0)
        diamond_consumed2 = goods_data2.get('diamond_consumed', 0)
        gold_consumed2 = goods_data2.get('gold_consumed', 0)
        return {'diamond_consumed': int(diamond_consumed1 + diamond_consumed2),'gold_consumed': int(gold_consumed1 + gold_consumed2)
           }

    def get_sel_good_num(self):
        return self._cur_sel_goods_num

    def update_buy_button_show(self):
        if not global_data.player:
            return
        money_info = global_data.king_battle_data.get_money_info(global_data.player.id)
        is_enough = self._pay_money_data and koth_shop_utils.check_payment(self._pay_money_data, money_info, False)
        self.panel.temp_btn_buy.btn_common.SetEnable(is_enough)
        self.init_money_label(self.panel.nd_buy.temp_money_buy, self._pay_money_data, is_enough)

    def init_player_money_label(self):
        if not global_data.player:
            return
        money_info = global_data.king_battle_data.get_money_info(global_data.player.id)
        self.money_dict = money_info
        koth_shop_utils.init_koth_own_money2(self.panel.nd_title.temp_money, money_info)

    def update_koth_money_info(self, entity_id, money_dict):
        if not global_data.player:
            return
        if entity_id == global_data.player.id:
            self.money_dict = money_dict
            koth_shop_utils.init_koth_own_money2(self.panel.nd_title.temp_money, money_dict)
            self.refresh_tab_data(self.label_type)
            self.update_financial_btns()

    def refresh_modules(self):
        self.set_installed_modules()
        if self.label_type == TYPE_WEAPON:
            self.refresh_tab_data(self.label_type)
        self.panel.SetTimeOut(0.03, self.update_selected_item_show)

    def set_installed_modules(self):
        if self.label_type != TYPE_MODULE:
            return
        else:
            if global_data.player:
                player = global_data.player.logic if 1 else None
                return player or None
            self._cur_check_own_items = []
            cur_module_config = player.ev_g_mecha_all_installed_module() or {}
            for slot_conf in six_ex.values(cur_module_config):
                card_id, item_id = slot_conf
                self._cur_check_own_items.append(str(koth_shop_utils.get_goods_id_by_item_id(item_id)))

            return

    def get_goods_id_by_item_id(self, item_id):
        from common.cfg import confmgr
        item_infos = confmgr.get('king_shop_config', 'items_data', str(item_id), default={})
        goods_id = item_infos.get('goods_id')
        return goods_id

    def _on_clothes_data_changed(self, dress_pos):
        self.set_installed_clothed()
        if self.label_type == TYPE_ARMOR:
            self.refresh_tab_data(self.label_type)
        self.panel.SetTimeOut(0.03, self.update_selected_item_show)

    def set_installed_clothed(self):
        if self.label_type != TYPE_ARMOR:
            return
        else:
            if global_data.player:
                player = global_data.player.logic if 1 else None
                return player or None
            self._cur_check_own_items = []
            clothes = player.ev_g_clothing()
            for clothes_data in six_ex.values(clothes):
                item_id = clothes_data['item_id']
                self._cur_check_own_items.append(str(koth_shop_utils.get_goods_id_by_item_id(item_id)))

            return

    def show_sel_goods_details(self, goods_data):
        if goods_data:
            self.panel.nd_details.setVisible(True)
            item_no = goods_data.get('item_no', None)
            item_name = item_utils.get_item_name(item_no)
            self.panel.nd_details.lab_name.setString(item_name)
            self.panel.nd_details.lab_describe.SetString(item_utils.get_item_desc(item_no))
        else:
            self.panel.nd_details.setVisible(False)
        return

    def on_buy_num_changed(self, num):
        self.set_sel_good_num(num)
        self.update_buy_button_show()

    def on_sell_num_changed(self, num):
        self._cur_sell_item_num = num
        self.panel.lab_num.SetString(str(num))
        self.update_financial_btns()

    def get_item_no_sell_info(self, item_no):
        if not item_no:
            return {}
        import copy
        from common.cfg import confmgr
        item_infos = confmgr.get('king_shop_config', 'items_data', str(item_no), default={})
        goods_id = item_infos.get('goods_id')
        level = item_infos.get('level')
        tab_goods = self.get_tab_shop_items(self.label_type)
        price_dict = {'diamond_consumed': 0,'gold_consumed': 0}
        for lv in spc.KING_SHOP_ITEM_LEVEL_SEQUENCE:
            goods_data = tab_goods.get(str(goods_id), {}).get('item_dict', {}).get(str(lv))
            price_dict = self.add_price(price_dict, goods_data)
            if str(lv) == str(level):
                break

        goods_data = copy.deepcopy(tab_goods.get(str(goods_id), {}).get('item_dict', {}).get(str(level)))
        price_dict = self.cal_price(price_dict, spc.KING_SHOP_ITEM_SELL_PRICE_PERCENT)
        goods_data.update(price_dict)
        goods_data.update({'goods_id': goods_id})
        return goods_data

    def update_financial_btns(self):
        is_buy = False
        is_sell = False
        has_upgrade_func = False
        if self._cur_sel_goods_data:
            is_buy = True
        if self._cur_sell_player_item_data:
            is_sell = True
        if self._cur_sell_player_item_data and self._cur_upgrade_player_item_data:
            has_upgrade_func = True
        if is_sell and not has_upgrade_func:
            self.panel.nd_details.nd_buy.setVisible(False)
            self.panel.nd_details.nd_sell.setVisible(True)
            self.panel.nd_details.nd_sell_and_up.setVisible(False)
            self.update_sell_button_show()
        elif is_sell and has_upgrade_func:
            self.panel.nd_details.nd_buy.setVisible(False)
            self.panel.nd_details.nd_sell.setVisible(False)
            self.panel.nd_details.nd_sell_and_up.setVisible(True)
            self.update_sell_and_up_button_show()
        elif is_buy and not is_sell:
            self.panel.nd_details.nd_buy.setVisible(True)
            self.panel.nd_details.nd_sell.setVisible(False)
            self.panel.nd_details.nd_sell_and_up.setVisible(False)
            self.update_buy_button_show()
        else:
            self.panel.nd_details.nd_buy.setVisible(False)
            self.panel.nd_details.nd_sell.setVisible(False)
            self.panel.nd_details.nd_sell_and_up.setVisible(False)

    def update_sell_button_show(self):
        if not global_data.player:
            return
        if not self._cur_sell_player_item_data:
            return
        price_dict = self.cal_price(self._cur_sell_player_item_data, self._cur_sell_item_num)
        self.init_money_label(self.panel.nd_sell.temp_money_sell, price_dict, True, colors=['#SG', '#SG'])

    def update_sell_and_up_button_show(self):
        if not global_data.player:
            return
        if not self._cur_sell_player_item_data:
            return
        price_dict = self.cal_price(self._cur_sell_player_item_data, self._cur_sell_item_num)
        self.init_money_label(self.panel.nd_sell_and_up.temp_money_sell, price_dict, True, colors=['#SG', '#SG'])
        is_full_lv = False
        if self._cur_upgrade_player_item_data:
            is_full_lv = self._cur_upgrade_player_item_data.get('is_full_lv', False)
        if not is_full_lv:
            price_dict2 = self.cal_price(self._cur_upgrade_player_item_data, self._cur_sell_item_num)
            is_enough = koth_shop_utils.check_payment(price_dict2, self.money_dict)
            self.init_money_label(self.panel.nd_sell_and_up.temp_money_up, price_dict2, is_enough)
            self.panel.nd_sell_and_up.temp_btn_upgrade.btn_common.SetEnable(True)
        else:
            self.init_money_label(self.panel.nd_sell_and_up.temp_money_up, {}, True)
            self.panel.nd_sell_and_up.temp_btn_upgrade.btn_common.SetEnable(False)

    def set_installed_weapons_goods_id(self):
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            self._cur_check_own_items = []
            pos_list = [
             const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3]
            for pos in pos_list:
                weapon_obj = player.share_data.ref_wp_bar_mp_weapons.get(pos)
                if weapon_obj is None:
                    item_no = None if 1 else weapon_obj.get_id()
                    self._cur_check_own_items.append(str(koth_shop_utils.get_goods_id_by_item_id(item_no)))

            return

    def _on_weapon_data_changed(self, *args):
        self.set_installed_weapons_goods_id()
        if self.label_type == TYPE_WEAPON:
            self.refresh_tab_data(TYPE_WEAPON)
        self.panel.SetTimeOut(0.03, self.update_selected_item_show)

    def _on_weapon_data_switched(self, pos1, pos2):
        self.set_installed_weapons_goods_id()
        if self.label_type == TYPE_WEAPON:
            self.refresh_tab_data(TYPE_WEAPON)
        self.panel.SetTimeOut(0.03, self.update_selected_item_show)

    def update_selected_item_show(self):
        if not self.panel:
            return
        else:
            if self._cur_sel_goods_data:
                sel_goods_id = self._cur_sel_goods_data.get('goods_id', None)
                if sel_goods_id in self._cur_check_own_items:
                    self.on_player_select_goods_id(sel_goods_id)
                    return
            if self._cur_sell_player_item_data:
                sel_goods_id = self._cur_sell_player_item_data.get('goods_id', None)
                if sel_goods_id in self._cur_check_own_items:
                    self.on_player_select_goods_id(sel_goods_id)
                else:
                    self.on_player_choose_own_item(None)
                    return
            return

    def on_player_choose_own_item(self, item_no, wepaon_pos=0):
        if item_no:
            self._cur_sell_player_item_data = self.get_item_no_sell_info(item_no)
            self._cur_sell_player_item_data['position'] = wepaon_pos
            if wepaon_pos:
                if global_data.player and global_data.player.logic:
                    player = global_data.player.logic
                    weapon_obj = player.share_data.ref_wp_bar_mp_weapons.get(wepaon_pos)
                    if weapon_obj:
                        self._cur_sell_player_item_data['entity_id'] = weapon_obj.get_entity_id()
            self.set_sel_goods(None)
            goods_id = koth_shop_utils.get_goods_id_by_item_id(item_no)
            if self._tab_info.get(self.label_type, {}).get('select_related', False):
                self.set_goods_id_widget_selected(goods_id)
            else:
                self.set_goods_id_widget_selected(None)
            if self._cur_player_widget:
                self._cur_player_widget.on_player_choose_own_item(goods_id)
            upgrade_info = koth_shop_utils.calc_player_item_upgrade_info(item_no, self.label_type)
            if upgrade_info:
                self._cur_upgrade_player_item_data = upgrade_info
                self._cur_upgrade_player_item_data['position'] = wepaon_pos
            else:
                self._cur_upgrade_player_item_data = {}
            num_show = self._tab_info.get(self.label_type, {}).get('can_change_num', False)
            self.panel.nd_num.setVisible(num_show)
            self._cur_sell_item_num = 1
            if num_show:
                max_num = 1
                if global_data.player and global_data.player.logic:
                    item_count = global_data.player.logic.ev_g_item_count(item_no)
                    max_num = item_count
                self.add_sub_widget.set_args({'min_num': 1,
                   'max_num': max_num,
                   'per_num': 1,
                   'begin_num': self._cur_sell_item_num,
                   'begin_ttf': self._cur_sell_item_num
                   })
                self.add_sub_widget.set_num_change_callback(self.on_sell_num_changed)
        else:
            self._cur_upgrade_player_item_data = {}
            self._cur_sell_player_item_data = {}
            if self._cur_player_widget:
                self._cur_player_widget.on_player_choose_own_item(None)
        self.show_sel_goods_details(self._cur_sell_player_item_data)
        self.update_financial_btns()
        return

    def set_goods_id_widget_selected(self, goods_id):
        if goods_id in self._goods_id_to_ui_widget:
            ui_widget = self._goods_id_to_ui_widget[goods_id]
            if ui_widget:
                self.set_cur_sel_item(ui_widget)
        else:
            self.set_cur_sel_item(None)
        return