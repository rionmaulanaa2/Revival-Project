# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/Inventory.py
from __future__ import absolute_import
import six
from . import InventoryView
from . import InventoryStatistics
from . import item_utility as iutil
from . import item_const as iconst
from .ListContainer import ListContainer
import math

class Inventory(object):
    KNAPSACK_CAPACITY = 800

    def __init__(self, owner, update_view, update_statistics=False):
        super(Inventory, self).__init__()
        self._logger = owner.logger
        self._container = ListContainer(owner.logger)
        self._knapsack_size = 0
        self._update_statistics = update_statistics
        self._statistics_dict = {}
        self._update_view = update_view
        self._views_dict = {}
        self._owner = owner

    def destroy(self):
        self._owner = None
        return

    def init_from_dict(self, pdict):
        self._knapsack_size = self._container.init_from_dict(pdict.get('container', {}))
        item_list = self._container.get_item_list()
        if self._update_view:
            self._init_view(item_list)
        if self._update_statistics:
            self._init_statistics(item_list)

    def _init_view(self, item_list):
        self._views_dict = {iconst.INV_VIEW_ALL_ITEM: InventoryView.InvViewAllItem(),
           iconst.INV_VIEW_KNAPSACK: InventoryView.InvViewKnapsack(),
           iconst.INV_VIEW_HEAD: InventoryView.InvViewHead(),
           iconst.INV_VIEW_BODICE: InventoryView.InvViewBodice(),
           iconst.INV_VIEW_BOTTOMS: InventoryView.InvViewBottoms(),
           iconst.INV_VIEW_HEAD_FRAME: InventoryView.InvViewHeadFrame(),
           iconst.INV_VIEW_HEAD_PHOTO: InventoryView.InvViewHeadPhoto(),
           iconst.INV_VIEW_HOUSE_WALL_PICTURE: InventoryView.InvViewHouseWallPicture(),
           iconst.INV_VIEW_RED_POINT_ITEM: InventoryView.InvViewRedPointItem(),
           iconst.INV_VIEW_CHAT_ITEM: InventoryView.InvViewChatItem()
           }
        for view in six.itervalues(self._views_dict):
            view.update(item_list)

    def _init_statistics(self, item_list):
        self._statistics_dict = {iconst.INV_STAT_PERMANENT_SKIN: InventoryStatistics.InvStatPermanentSkin(),
           iconst.INV_STAT_MECHA_SKIN: InventoryStatistics.InvStatMechaSkin(),
           iconst.INV_STAT_ROLE_SKIN: InventoryStatistics.InvStatRoleSkin(),
           iconst.INV_STAT_OTHER_SKIN: InventoryStatistics.InvStatOtherSkin(),
           iconst.INV_STAT_MECHA_SLEVEL_SKIN: InventoryStatistics.InvStatMechaSLevelSkin(),
           iconst.INV_STAT_ROLE_SLEVEL_SKIN: InventoryStatistics.InvStatRoleSLevelSkin(),
           iconst.INV_STAT_OTHER_SLEVEL_SKIN: InventoryStatistics.InvStatOtherSLevelSkin(),
           iconst.INV_STAT_EMOTICON: InventoryStatistics.InvStatEmoticon(),
           iconst.INV_STAT_SPRAY: InventoryStatistics.InvStatSpray(),
           iconst.INV_STAT_GESTURE: InventoryStatistics.InvStatGesture(),
           iconst.INV_STAT_TALKING: InventoryStatistics.InvStatTalking(),
           iconst.INV_STAT_HEAD_PHOTO: InventoryStatistics.InvStatHeadPhoto(),
           iconst.INV_STAT_HEAD_FRAME: InventoryStatistics.InvStatHeadFrame()
           }
        for stat in six.itervalues(self._statistics_dict):
            stat.update(item_list)

    def get_stat_dict(self):
        item_stat_dict = {}
        for key, stat in six.iteritems(self._statistics_dict):
            item_stat_dict[str(key)] = stat.get_count()

        return item_stat_dict

    def get_persistent_dict(self):
        return {'container': self._container.get_persistent_dict()
           }

    def get_client_dict(self):
        return {'container': self._container.get_client_dict()
           }

    def clear(self):
        self._container.clear()
        self._knapsack_size = 0

    def add_item(self, item, reason='', update_view=True):
        if not item:
            return (False, ListContainer.CONT_NONE_OBJ)
        else:
            if item.is_knapsack_item() and self.check_knapsack_full():
                return (
                 False, ListContainer.CONT_REACH_LIMIT)
            res, err_code = self._container.add_item(item)
            if not res:
                return (False, err_code)
            self._notify_item_add(item, update_view)
            self._on_add_knapsack_item(item)
            return (
             True, None)

    def add_stack_item(self, item, num, reason='', update_view=True):
        need_new_slot = False
        if item.is_knapsack_item() and not self.get_item_by_item_obj(item):
            if self.check_knapsack_full():
                return (False, ListContainer.CONT_REACH_LIMIT, None)
            need_new_slot = True
        res, err_code, item = self._container.add_stack_item(item, num)
        if not res:
            return (False, err_code, None)
        else:
            self._notify_item_add(item, update_view)
            if need_new_slot:
                self._on_add_knapsack_item(item)
            return (
             True, None, item)

    def add_one_item(self, item, reason='', update_view=True):
        if item is None:
            return (False, ListContainer.CONT_NONE_OBJ)
        else:
            if item.can_stack():
                return self.add_stack_item(item, 1, reason, update_view)
            return self.add_item(item, reason, update_view)
            return

    def _on_add_knapsack_item(self, item):
        if item.is_knapsack_item():
            self._knapsack_size += 1

    def reduce_item_num_by_id(self, item_id, num):
        ret, is_remove, item = self._container.reduce_item_num_by_item_id(item_id, num)
        if ret:
            self._notify_item_remove(item)
        if is_remove:
            self._on_remove_knapsack_item(item, 1)
        return (
         ret, item)

    def remove_item(self, item_id):
        item = self._container.get_item_by_item_id(item_id)
        if item is None:
            return False
        else:
            ret = self._container.remove_item(item_id)
            if ret:
                self._notify_item_remove(item)
                self._on_remove_knapsack_item(item, 1)
            return ret

    def reduce_item_num(self, item_no, num, check_lock=False):
        res, slot_num, item, reduce_item_dict = self._container.reduce_item_num(item_no, num, check_lock)
        if res:
            self._notify_item_remove(item)
            self._on_remove_knapsack_item(item, slot_num)
        return (
         res, reduce_item_dict)

    def reduce_circulation_item_num(self, item_no, num, circulation_type=iconst.ITEM_CIRCULATION_UNLIMIT):
        res, slot_num, item, reduce_item_dict = self._container.reduce_circulation_item_num(item_no, num, circulation_type)
        if res:
            self._notify_item_remove(item)
            self._on_remove_knapsack_item(item, slot_num)
        return (
         res, reduce_item_dict)

    def _on_remove_knapsack_item(self, item, slot_num):
        if slot_num > 0 and item.is_knapsack_item():
            self._knapsack_size -= slot_num

    def get_knapsack_size(self):
        return self._knapsack_size

    def get_max_knapsack_size(self):
        return Inventory.KNAPSACK_CAPACITY

    def get_empty_knapsack_size(self):
        return Inventory.KNAPSACK_CAPACITY - self._knapsack_size

    def get_current_slot_num(self):
        return self._container.get_size()

    def get_max_slot_num(self):
        return self._container.MAX_CAPACITY

    def get_empty_slot_num(self):
        return self._container.MAX_CAPACITY - self._container.get_size()

    def has_enough_item(self, item_no, num, unlock_time=None, check_lock=False):
        return self._container.has_enough_item(item_no, num, unlock_time, check_lock)

    def has_enough_circulation_items(self, item_no, num, circulation_type):
        return self._container.has_enough_circulation_items(item_no, num, circulation_type)

    def has_enough_item_by_id(self, item_id, num):
        return self._container.has_enough_item_by_item_id(item_id, num)

    def get_item_by_id(self, item_id):
        return self._container.get_item_by_item_id(item_id)

    def get_item_by_no(self, item_no):
        return self._container.get_item_by_item_no(item_no)

    def get_item_by_item_obj(self, item_obj):
        return self._container.get_item_by_item_obj(item_obj)

    def get_items_by_type_list(self, item_list):
        return self._container.get_items_by_type_list(item_list)

    def get_item_num_by_no(self, item_no, check_lock=False):
        return self._container.get_item_num_by_no(item_no, check_lock)

    def get_circulation_item_num_by_no(self, item_no):
        return self._container.get_circulation_item_num_by_no(item_no)

    def get_items_by_no(self, item_no, check_lock=False):
        items = self._container.get_items_by_item_no(item_no, check_lock)
        return items

    def get_items_by_type(self, item_type):
        items = self._container.get_items_by_type(item_type)
        return items

    def get_items_by_type_sort_by_create_time(self, item_type):
        items = self._container.get_items_by_type_sort_by_create_time(item_type)
        return items

    def get_item_by_view_and_index(self, view_id, index):
        if index >= len(self.get_view_item_list(view_id)):
            return None
        else:
            return self.get_view_item_list(view_id)[index]

    def get_all_items(self):
        return self._container.get_item_list()

    def get_item_idx_in_view_by_id(self, item_id, view):
        item_list = self.get_view_item_list(view)
        idx = 0
        for item in item_list:
            if item.id == item_id:
                return idx
            idx += 1

        return -1

    def get_item_count_info(self):
        item_list = self.get_all_items()
        item_count_info = {}
        for item in item_list:
            item_no = str(item.item_no)
            item_num = item.get_current_stack_num()
            item_count_info.setdefault(item_no, [])
            item_count_info[item_no].append((item.id, item_num))

        return item_count_info

    def set_view_order(self, view_id, order_type):
        if view_id not in self._views_dict:
            return
        self._views_dict[view_id].set_order_type(order_type)

    def get_view_order(self, view_id):
        if view_id not in self._views_dict:
            return None
        else:
            return self._views_dict[view_id].get_order_type()

    def get_view(self, view_id):
        return self._views_dict.get(view_id, None)

    def get_stat(self, stat_id):
        return self._statistics_dict.get(stat_id, None)

    def get_view_item_list(self, view_id, refresh=False, filter=None):
        if view_id not in self._views_dict:
            return None
        else:
            return self._views_dict[view_id].get_view_item_list(refresh, filter)

    def update_item_view(self, item):
        self._refresh_item_related_view(item)

    def _refresh_item_related_view(self, item):
        item_list = self._container.get_item_list()
        for v in six.itervalues(self._views_dict):
            if v.is_view_item(item):
                v.update(item_list)

        global_data.emgr.player_item_update_event.emit()
        global_data.emgr.player_item_update_event_with_id.emit(item.item_no)

    def _notify_item_add(self, item, update_view=True):
        if self._update_view and update_view:
            self._refresh_item_related_view(item)
        if self._update_statistics:
            for stat in six.itervalues(self._statistics_dict):
                stat.add(item)

    def _notify_item_remove(self, item):
        if self._update_view:
            self._refresh_item_related_view(item)
        if self._update_statistics:
            for stat in six.itervalues(self._statistics_dict):
                stat.remove(item)

    def check_knapsack_full(self):
        return self._knapsack_size >= Inventory.KNAPSACK_CAPACITY

    def check_knapsack_capacity(self, need_cap):
        return Inventory.KNAPSACK_CAPACITY - self.get_knapsack_size() >= need_cap

    def check_inventory_capacity(self, need_cap):
        return self._container.check_capacity(need_cap)

    def check_can_add_items(self, item_dict, check_lock=False, auto_use_list=None):
        auto_use_list = [] if auto_use_list is None else auto_use_list
        knapsack_num = 0
        inventory_num = 0
        for item_key, item_num in six.iteritems(item_dict):
            if check_lock:
                item_no, unlock_time = item_key if 1 else (item_key, 0)
                item_data = iutil.get_lobby_item_data(item_no)
                if not item_data:
                    inventory_num += item_num
                else:
                    if item_no in auto_use_list:
                        continue
                    need_knapsack = iutil.is_knapsack_item(item_no)
                    max_stack_num = item_data.get('max_stack_num', 1)
                    timeliness = item_data.get('timeliness', 0)
                    if not timeliness:
                        if max_stack_num > 1:
                            cur_item_list = self.get_items_by_no(item_no, True)
                            can_stack_num = 0
                            for cur_item in cur_item_list:
                                can_stack_num += cur_item.max_stack_num - cur_item.current_stack_num

                            left_num = item_num - can_stack_num
                            if left_num > 0:
                                inventory_num += int(math.ceil(1.0 * left_num / max_stack_num))
                                knapsack_num += inventory_num if need_knapsack else 0
                        else:
                            inventory_num += item_num
                            knapsack_num += item_num if need_knapsack else 0
                    else:
                        cur_item = self.get_item_by_no(item_no)
                        if not cur_item:
                            if iutil.is_role_item(item_no) or iutil.is_mecha_item(item_no):
                                inventory_num += 2
                            else:
                                inventory_num += 1
                                knapsack_num += 1 if need_knapsack else 0
                        if not self.check_knapsack_capacity(knapsack_num):
                            return (False, None)
                    if not self.check_inventory_capacity(inventory_num):
                        return (False, None)

        return (
         True, None)

    def check_can_add_item(self, item_no, item_num, unlock_time=0, auto_use=False):
        return self.check_can_add_items({(item_no, unlock_time): item_num}, True, [item_no] if auto_use else [])