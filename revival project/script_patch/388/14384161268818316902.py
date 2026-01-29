# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impItem.py
from __future__ import absolute_import
import six
import common.platform.appsflyer_const as af_const
from mobile.common.RpcMethodArgs import Str, Int, Dict, Uuid, List, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.item.Inventory import Inventory
from logic.gcommon.item.ListContainer import ListContainer
from logic.gcommon.item import item_utility as iutil
from logic.gcommon.item import item_const as iconst
from logic.gcommon.item.item_const import FASHION_POS_SUIT, DEFAULT_LOBBY_SKIN, DEFAULT_LOBBY_SKYBOX
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_MECHA, REDPOINT_ITEM_TYPE, L_ITEM_TYPE_TALKING, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_LOTTERY_TICKET, ITEM_TYPE_DEC
from common.cfg import confmgr
from common.platform.appsflyer import Appsflyer
from logic.gcommon.const import SHOP_ITEM_YUANBAO, SHOP_ITEM_DIAMON, SHOP_ITEM_GOLD
from logic.gutils import item_utils
from logic.gutils.item_utils import get_lobby_item_type
from logic.gutils.mecha_skin_utils import get_mecha_base_skin_id
from logic.gutils.mecha_module_utils import is_default_module
from logic.comsys.item_use.ItemUseConfirmUI import ItemUseConfirmUI
AttrEvent = {'fashion': 'role_fashion_chagne',
   'sfx': 'role_sfx_chagne',
   'wsfx': 'weapon_sfx_change'
   }

class impItem(object):

    def _init_item_from_dict(self, bdict):
        self.inventory = Inventory(self, True, True)
        self.inventory.init_from_dict(bdict.get('inventory', {}))
        self.check_items()

    def _destroy_item(self):
        if self.inventory:
            self.inventory.destroy()
            self.inventory = None
        return

    def get_item_stat(self):
        pass

    def check_items(self):
        items = self.inventory.get_all_items()
        for item in items:
            if item.get_current_stack_num() <= 0:
                self.inventory.remove_item(item.id)

        self.inventory.add_item(iutil.create_item(DEFAULT_LOBBY_SKIN, redpoint=False), 'CLIENT_ITEM', False)
        self.inventory.add_item(iutil.create_item(DEFAULT_LOBBY_SKYBOX, redpoint=False), 'CLIENT_ITEM', False)

    def is_item_no_valid(self, item_no):
        if not iutil.get_backpack_item_data(item_no):
            return False
        else:
            return True

    def is_item_money(self, item_no):
        payment_item_type = confmgr.get('payment_item_type', default={})
        if str(item_no) in payment_item_type:
            return item_no
        return False

    def can_use_item_by_no(self, item_no):
        item = self.get_item_by_no(item_no)
        if item is None:
            return False
        else:
            return item.can_use(self.sex, self.get_lv())

    def can_use_item_by_id(self, item_id):
        item = self.get_item_by_id(item_id)
        if item is None:
            return False
        else:
            return

    def has_enough_item(self, item_no, num, unlock_time=None, check_lock=False):
        if not self.inventory:
            return False
        return self.inventory.has_enough_item(item_no, num, unlock_time, check_lock)

    def has_enough_circulation_items(self, item_no, num, circulation_type):
        return self.inventory.has_enough_circulation_items(item_no, num, circulation_type)

    def has_enough_item_by_id(self, item_id, num):
        return self.inventory.has_enough_item_by_id(item_id, num)

    def has_limit_time_item_by_no(self, item_no, limit_ts):
        item = self.get_item_by_no(item_no)
        if item and item.get_create_time() < limit_ts:
            return True
        else:
            return False

    def has_item_by_no(self, item_no):
        return self.has_enough_item(item_no, 1)

    def has_item_by_id(self, item_id):
        return self.has_enough_item_by_id(item_id, 1)

    def has_permanent_item_by_no(self, item_no):
        item = self.get_item_by_no(item_no)
        return item and item.is_permanent_item()

    def check_can_add_item(self, item_no, item_num, unlock_time=0):
        return self.inventory.check_can_add_item(item_no, item_num, unlock_time)

    def check_can_add_items(self, item_dict, check_lock=False):
        return self.inventory.check_can_add_items(item_dict, check_lock)

    def check_knapsack_capacity(self, cnt):
        return self.inventory.check_knapsack_capacity(cnt)

    def get_item_by_no(self, item_no):
        if not self.inventory:
            return None
        else:
            return self.inventory.get_item_by_no(item_no)

    def get_item_by_id(self, item_id):
        if not self.inventory:
            return None
        else:
            return self.inventory.get_item_by_id(item_id)

    def get_item_num_by_no(self, item_no, check_lock=False):
        if not self.inventory:
            return 0
        if item_no == SHOP_ITEM_YUANBAO:
            return self.get_yuanbao()
        if item_no == SHOP_ITEM_DIAMON:
            return self.get_diamond()
        if item_no == SHOP_ITEM_GOLD:
            return self.get_gold()
        return self.inventory.get_item_num_by_no(item_no, check_lock)

    def get_circulation_item_num_by_no(self, item_no):
        if not self.inventory:
            return 0
        return self.inventory.get_circulation_item_num_by_no(item_no)

    def get_item_num_by_nos(self, item_no_list, check_lock=False):
        num = 0
        for item_no in item_no_list:
            num += self.inventory.get_item_num_by_no(item_no, check_lock)

        return num

    def get_items_by_no(self, item_no, check_lock=False):
        if not self.inventory:
            return []
        return self.inventory.get_items_by_no(item_no, check_lock)

    def get_items_by_type(self, item_type):
        if not self.inventory:
            return []
        return self.inventory.get_items_by_type(item_type)

    def get_items_by_type_list(self, type_list):
        if not self.inventory:
            return []
        return self.inventory.get_items_by_type_list(type_list)

    def get_view_item_list(self, view_id, refresh=False, filter=None):
        if not self.inventory:
            return []
        return self.inventory.get_view_item_list(view_id, refresh, filter)

    @rpc_method(CLIENT_STUB, (Dict('inventory_dict'),))
    def refresh_inventory(self, inventory_dict):
        self.inventory = Inventory(self, True)
        self.inventory.init_from_dict(inventory_dict)

    @rpc_method(CLIENT_STUB, (Str('item_id'),))
    def remove_all_item(self, item_id):
        item_no = 0
        item = self.get_item_by_id(item_id)
        if item:
            item_no = item.item_no
            global_data.emgr.del_item_red_point.emit(item_no)
        if not self.inventory.remove_item(item_id):
            pass
        self.on_remove_all_item(item_id, item_no)

    @rpc_method(CLIENT_STUB, (Dict('item_ids'),))
    def remove_items(self, item_ids):
        item_nos = []
        for item_id in item_ids:
            item = self.get_item_by_id(item_id)
            if item:
                item_nos.append(item.item_no)
                global_data.emgr.del_item_red_point.emit(item.item_no)
            if not self.inventory.reduce_item_num_by_id(item_id, item_ids[item_id]):
                continue

        self.on_remove_items(item_ids, item_nos)

    @rpc_method(CLIENT_STUB, (Dict('item_dict'), Int('item_num'), List('item_id_list')))
    def add_item(self, item_dict, item_num, item_id_list):
        item = iutil.create_item_from_dict(item_dict)
        if item is None:
            return
        else:
            item_no = item.item_no
            if not self.inventory:
                return
            if item.can_stack():
                ret, _, real_item = self.inventory.add_stack_item(item, item_num, 'add_item')
            elif item_num != len(item_id_list):
                pass
            else:
                add_num = 0
                last_add_item = None
                while item_num > 0:
                    item.id = item_id_list[add_num]
                    res, err_code = self.inventory.add_one_item(item, 'add_item', item_num <= 1)
                    if not res:
                        last_add_item and self.inventory.update_item_view(last_add_item)
                        break
                    last_add_item = item
                    add_num += 1
                    item_num -= 1
                    if item.get_type() == L_ITEM_TYPE_MECHA:
                        self._appsflyer_mecha()
                    if item_num <= 0:
                        break
                    item = iutil.create_item_from_dict(item_dict)

            self.on_add_item(item_no)
            if item_num <= 1:
                if iutil.is_mecha_module_only_lobby(item_no) and is_default_module(item_no):
                    pass
                elif item.get_rp_state():
                    global_data.emgr.add_item_red_point.emit(item_no)
            l_type = item.get_type()
            if l_type == L_ITEM_TYPE_TALKING:
                global_data.emgr.message_on_add_chat_item.emit(item_no)
            if l_type == L_ITEM_TYPE_ROLE_SKIN:
                self.check_default_decoration_action_for_skin(item_no)
            if l_type in ITEM_TYPE_DEC:
                self.check_default_decortion_action_for_dec(item_no)
            if iutil.is_item_confirm_use(item_no):
                global_data.ui_mgr.close_ui('ItemUseConfirmUI')
                ItemUseConfirmUI(item_no=item_no, item_num=item_num)
            global_data.emgr.on_lobby_bag_item_add_event.emit(item_dict, item_num, item_id_list)
            return

    def _appsflyer_mecha(self):
        mechas = self.get_items_by_type(L_ITEM_TYPE_MECHA)
        mecha_num = len(mechas)
        for check_num in af_const.af_mecha_collect_nums:
            if mecha_num >= check_num:
                Appsflyer().advert_track_event(event_name=af_const.AF_COLLECT, suffix=str(check_num))
                return

    def on_add_item(self, item_no):
        global_data.emgr.on_lobby_bag_item_changed_event.emit()
        if self.is_item_money(item_no):
            global_data.emgr.player_money_info_update_event.emit()

    def on_remove_items(self, item_ids, item_nos):
        global_data.emgr.on_lobby_bag_item_changed_event.emit()
        for item_no in item_nos:
            if self.is_item_money(item_no):
                global_data.emgr.player_money_info_update_event.emit()
                break

    def on_remove_all_item(self, item_id, item_no):
        global_data.emgr.on_lobby_bag_item_changed_event.emit()
        if self.is_item_money(item_no):
            global_data.emgr.player_money_info_update_event.emit()

    @rpc_method(CLIENT_STUB, (Str('item_id'), Int('expire_time')))
    def set_item_expire_time(self, item_id, expire_time):
        item = self.get_item_by_id(item_id)
        if item:
            item.set_expire_time(expire_time)
            global_data.emgr.player_item_update_event.emit()
            global_data.emgr.player_item_update_event_with_id.emit(item_id)

    @rpc_method(CLIENT_STUB, (Str('item_id'), Dict('info_dict')))
    def set_item_attr(self, item_id, info_dict):
        item = self.get_item_by_id(item_id)
        if not item:
            return
        for key, value in six.iteritems(info_dict):
            if not hasattr(item, key):
                continue
            setattr(item, key, value)
            if key in AttrEvent:
                self.handle_attr_msg(key, value)
                global_data.emgr[AttrEvent[key]].emit(item.item_no, value)

        if self.is_item_money(item.item_no):
            global_data.emgr.player_money_info_update_event.emit()

    def handle_attr_msg(self, key, value):
        if key == 'fashion':
            fashion_id = value.get(FASHION_POS_SUIT, None)
            if get_lobby_item_type(fashion_id) != L_ITEM_TYPE_MECHA_SKIN:
                return
            base_skin_id = get_mecha_base_skin_id(fashion_id)
            if base_skin_id:
                global_data.player.set_sss_base_fashion_info(base_skin_id, fashion_id)
        return

    def use_item(self, item_id, cnt, params=None):
        if params is None:
            params = {}
        self.call_server_method('use_item', (item_id, cnt, params))
        return

    @rpc_method(CLIENT_STUB, (Int('item_no'), Bool('use_success')))
    def use_item_result(self, item_no, use_success):
        if use_success:
            item_utils.show_item_use_success_tips(item_no)

    def recycle_item(self, item_id, cnt):
        self.call_server_method('recycle_items', ({item_id: cnt},))

    def recycle_items(self, item_dict):
        self.call_server_method('recycle_items', (item_dict,))

    @rpc_method(CLIENT_STUB, (Int('reason_id'),))
    def forbiden_item_msg(self, reason_id):
        content = get_text_by_id(180, {'reason': get_text_by_id(reason_id)})
        global_data.game_mgr.show_tip(content, True)

    def req_del_item_redpoint(self, item_no):
        item_id = self.get_del_redpoint_item_id(item_no)
        if item_id is None:
            return
        else:
            global_data.emgr.del_item_red_point.emit(int(item_no))
            self.call_server_method('del_item_redpoint', (item_id,))
            return

    def req_del_item_redpoint_list(self, item_no_list):
        item_id_list = []
        for item_no in item_no_list:
            item_id = self.get_del_redpoint_item_id(item_no)
            if item_id:
                item_id_list.append(item_id)

        global_data.emgr.del_item_red_point_list.emit(item_no_list)
        self.call_server_method('del_item_redpoint_list', (item_id_list,))

    def get_del_redpoint_item_id(self, item_no):
        item_no = int(item_no)
        item = self.get_item_by_no(item_no)
        if not item:
            return None
        else:
            if item.get_type() not in REDPOINT_ITEM_TYPE:
                return None
            if not item.get_rp_state():
                return None
            item.set_rp_state(False)
            return item.id

    def exchange_ticket(self):
        self.call_server_method('exchange_ticket', ())