# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/ListContainer.py
from __future__ import absolute_import
from six.moves import range
from .. import utility as util
from . import item_utility as iutil
from . import item_const as iconst
from .SortedDict import SortedDict
from .SlotIndexRecord import SlotIndexRecord

class ListContainer(object):
    CONT_NONE_OBJ = -1
    CONT_DUP_OBJ = -2
    CONT_REACH_LIMIT = -3
    CONT_INVALID_OBJ = -4
    CONT_WRONG_NUM = -5
    MAX_CAPACITY = 8192
    DEFAULT_CAPACITY = 32

    def __init__(self, logger):
        super(ListContainer, self).__init__()
        self._slots = []
        self._empty_slot_index_list = []
        self._id_to_slot_index = {}
        self._no_to_slot_index = SlotIndexRecord()
        self._size = 0
        self._capacity = 0
        self._build_new_slots(self.DEFAULT_CAPACITY)
        self._logger = logger

    def clear(self):
        self._slots = []
        self._empty_slot_index_list = []
        self._id_to_slot_index = {}
        self._no_to_slot_index = SlotIndexRecord()
        self._size = 0
        self._capacity = 0

    def _get_obj(self, obj_id):
        idx = self._id_to_slot_index.get(obj_id)
        if idx is None:
            return
        else:
            return self._slots[idx]
            return

    def _build_new_slots(self, capacity):
        self._slots = [
         None] * capacity
        for i in range(capacity - 1, -1, -1):
            self._empty_slot_index_list.append(i)

        self._size = 0
        self._capacity = capacity
        return

    def _build_slots_from_list(self, item_list):
        self.clear()
        knapsack_size = 0
        idx = 0
        for item_dict in item_list:
            info_dict = util.unicode_to_str(item_dict)
            obj = iutil.create_item_from_dict(info_dict)
            if obj is None:
                util.log_error('create item failed when _build_slots_from_list, info_dict:%s', info_dict)
                continue
            self._slots.append(obj)
            if obj.is_knapsack_item():
                knapsack_size += 1
            self._id_to_slot_index[obj.id] = idx
            self._no_to_slot_index.add_idx(obj.item_no, obj.unlock_time, idx)
            idx += 1

        self._size = len(self._slots)
        self._capacity = self._size
        if self._capacity == 0:
            self._build_new_slots(self.DEFAULT_CAPACITY)
        elif self._capacity < self.MAX_CAPACITY:
            cap = util.get_next_pow_of_two(self._capacity)
            res = self._expand_slots(cap)
        return knapsack_size

    def _expand_slots(self, new_cap):
        if new_cap <= self._capacity:
            self._logger.error('new_cap=%s is smaller than capacity=%s' % (new_cap, self._capacity))
            return False
        else:
            if new_cap > self.MAX_CAPACITY:
                self._logger.error('new_cap=%s is large than MAX_CAPACITY=%s' % (new_cap, self.MAX_CAPACITY))
                return False
            old_cap = self._capacity
            delta_cap = new_cap - self._capacity
            self._slots.extend([None] * delta_cap)
            for i in range(new_cap - 1, old_cap - 1, -1):
                self._empty_slot_index_list.append(i)

            self._capacity = new_cap
            return True

    def _pop_empty_slot_idx(self):
        try:
            return self._empty_slot_index_list.pop()
        except:
            return None

        return None

    def _push_empty_slot_idx(self, idx):
        self._empty_slot_index_list.append(idx)

    def _put_obj_to_slot(self, obj, idx):
        self._slots[idx] = obj
        self._id_to_slot_index[obj.id] = idx
        self._no_to_slot_index.add_idx(obj.item_no, obj.unlock_time, idx)
        self._size += 1

    def _remove_obj_from_slot(self, obj_id, idx):
        obj = self._slots[idx]
        self._no_to_slot_index.del_idx(obj.item_no, obj.unlock_time, idx)
        self._slots[idx] = None
        del self._id_to_slot_index[obj_id]
        self._size -= 1
        return

    def get_size(self):
        return self._size

    def get_capacity(self):
        return self._capacity

    def _get_persistent_item_list(self):
        ret_list = []
        for obj in self._slots:
            if not obj or not obj.item_no:
                continue
            ret_list.append(obj.get_persistent_dict())

        return ret_list

    def _get_client_item_list(self):
        ret_list = []
        for obj in self._slots:
            if obj is not None:
                ret_list.append(obj.get_client_dict())

        return ret_list

    def get_persistent_dict(self):
        return {'items': self._get_persistent_item_list()}

    def get_client_dict(self):
        pdict = {'items': self._get_client_item_list()}
        return pdict

    def init_from_dict(self, pdict):
        if not pdict:
            return 0
        return self._build_slots_from_list(pdict.get('items', []))

    def _add_obj(self, obj):
        if not obj.is_valid():
            self._logger.error('Found invalid obj %s' % obj.get_persistent_dict())
            return (
             False, ListContainer.CONT_INVALID_OBJ)
        else:
            if obj.id in self._id_to_slot_index:
                return (False, ListContainer.CONT_DUP_OBJ)
            empty_idx = self._pop_empty_slot_idx()
            if empty_idx is None:
                new_cap = util.get_next_pow_of_two(self.get_capacity())
                if not self._expand_slots(new_cap):
                    return (
                     False, ListContainer.CONT_REACH_LIMIT)
                empty_idx = self._pop_empty_slot_idx()
            self._put_obj_to_slot(obj, empty_idx)
            return (
             True, None)

    def add_item(self, item):
        if item is None:
            return (False, ListContainer.CONT_NONE_OBJ)
        else:
            if item.can_stack():
                return (False, ListContainer.CONT_INVALID_OBJ)
            return self._add_obj(item)

    def add_stack_item(self, item, num):
        if item is None:
            return (False, ListContainer.CONT_NONE_OBJ, None)
        else:
            if not item.can_stack():
                return (False, ListContainer.CONT_INVALID_OBJ, None)
            if num <= 0:
                return (False, ListContainer.CONT_WRONG_NUM, None)
            existed_item = self.get_item_by_item_id(item.id)
            if existed_item:
                existed_item.increase_stack_num(num)
                return (
                 True, None, existed_item)
            item.set_stack_num(num)
            res, error = self._add_obj(item)
            return (
             res, error, item)
            return

    def remove_item(self, item_id):
        return self._remove_obj(item_id)

    def _remove_obj(self, obj_id):
        idx = self._id_to_slot_index.get(obj_id)
        if idx is None:
            return False
        else:
            self._remove_obj_from_slot(obj_id, idx)
            self._push_empty_slot_idx(idx)
            return True
            return

    def reduce_item_num(self, item_no, num, check_lock=False):
        if num <= 0:
            return (False, 0, None, None)
        else:
            item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
            if item_sorted_dict is None:
                return (False, 0, None, None)
            counter = 0
            remove_id_list = []
            remove_num = 0
            last_item = None
            remove_item = None
            reduce_item_dict = {}
            for _, idx_list in item_sorted_dict.reiteritems():
                for idx in idx_list:
                    item = self._slots[idx]
                    if check_lock and item.is_lock():
                        continue
                    stack_num = item.get_current_stack_num()
                    counter += stack_num
                    last_item = item
                    if counter > num:
                        remove_item = item
                        break
                    else:
                        remove_id_list.append(item.id)
                        reduce_item_dict[item] = stack_num
                        remove_num = counter
                        if counter == num:
                            break
                else:
                    continue

                break

            if counter < num:
                return (False, 0, None, None)
            if remove_item is not None:
                remove_num = num - remove_num
                reduce_item_dict[remove_item] = remove_num
                if remove_item.can_stack():
                    remove_item.reduce_stack_num(remove_num)
                else:
                    remove_id_list.append(remove_item.id)
            for item_id in remove_id_list:
                self._remove_obj(item_id)

            return (
             True, len(remove_id_list), last_item, reduce_item_dict)

    def reduce_circulation_item_num(self, item_no, num, circulation_type=iconst.ITEM_CIRCULATION_UNLIMIT):
        if num <= 0:
            return (False, 0, None, None)
        else:
            item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
            if item_sorted_dict is None:
                return (False, 0, None, None)
            counter = 0
            remove_id_list = []
            remove_num = 0
            last_item = None
            remove_item = None
            reduce_item_dict = {}
            for _, idx_list in item_sorted_dict.reiteritems():
                for idx in idx_list:
                    item = self._slots[idx]
                    if not item.check_circulation(circulation_type):
                        continue
                    stack_num = item.get_current_stack_num()
                    counter += stack_num
                    last_item = item
                    if counter > num:
                        remove_item = item
                        break
                    else:
                        remove_id_list.append(item.id)
                        reduce_item_dict[item] = stack_num
                        remove_num = counter
                        if counter == num:
                            break
                else:
                    continue

                break

            if counter < num:
                return (False, 0, None, None)
            if remove_item is not None:
                remove_num = num - remove_num
                reduce_item_dict[remove_item] = remove_num
                if remove_item.can_stack():
                    remove_item.reduce_stack_num(remove_num)
                else:
                    remove_id_list.append(remove_item.id)
            for item_id in remove_id_list:
                self._remove_obj(item_id)

            return (
             True, len(remove_id_list), last_item, reduce_item_dict)

    def reduce_item_num_by_item_id(self, item_id, num):
        if num <= 0:
            return (False, False, None)
        else:
            item = self.get_item_by_item_id(item_id)
            if not item:
                return (False, False, None)
            item_num = item.get_current_stack_num()
            if item_num < num:
                return (False, False, None)
            if item_num == num:
                self._remove_obj(item_id)
                return (
                 True, True, item)
            item.reduce_stack_num(num)
            return (
             True, False, item)
            return (
             False, False, None)

    def combine_item(self, item_no, item_id=None):
        item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
        if item_sorted_dict is None:
            return (False, ListContainer.CONT_NONE_OBJ, None, None, 0)
        if item_id is not None:
            combine_item = self.get_item_by_item_id(item_id)
            if combine_item is None:
                return (False, ListContainer.CONT_NONE_OBJ, None, None, 0)
        else:
            combine_item = None
            max_unlock_time_item_list = item_sorted_dict.last()
            if max_unlock_time_item_list:
                combine_item = self._slots[max_unlock_time_item_list[0]]
            if combine_item is not None and not combine_item.is_lock():
                min_unlock_time_item_list = item_sorted_dict.first()
                if min_unlock_time_item_list:
                    combine_item = self._slots[min_unlock_time_item_list[0]]
        combine_num = 0
        remove_id_list = []
        for _, idx_list in item_sorted_dict.reiteritems():
            for idx in idx_list:
                item = self._slots[idx]
                if combine_item is None:
                    combine_item = item
                    continue
                if combine_item == item:
                    continue
                remove_id_list.append(item.id)
                combine_num += item.get_current_stack_num()

        if combine_item is None:
            return (False, ListContainer.CONT_NONE_OBJ, None, None, 0)
        else:
            if not combine_item.can_stack():
                return (False, ListContainer.CONT_INVALID_OBJ, None, None, 0)
            for item_id in remove_id_list:
                self._remove_obj(item_id)

            combine_item.increase_stack_num(combine_num)
            return (
             True, None, remove_id_list, combine_item, combine_num)

    def has_enough_item(self, item_no, num, unlock_time=None, check_lock=False):
        if num <= 0:
            return False
        else:
            item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
            if item_sorted_dict is None:
                return False
            counter = 0
            if unlock_time is None:
                for _, idx_list in item_sorted_dict.sorted_dict_iteritems():
                    for idx in idx_list:
                        item = self._slots[idx]
                        if check_lock and item.is_lock():
                            continue
                        counter += item.get_current_stack_num()
                        if counter >= num:
                            return True

            else:
                idx_list = item_sorted_dict.get(unlock_time, [])
                for idx in idx_list:
                    item = self._slots[idx]
                    if check_lock and item.is_lock():
                        continue
                    counter += item.get_current_stack_num()
                    if counter >= num:
                        return True

            return False

    def has_enough_circulation_items(self, item_no, num, circulation_type):
        if num <= 0:
            return False
        else:
            item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
            if item_sorted_dict is None:
                return False
            counter = 0
            for _, idx_list in item_sorted_dict.sorted_dict_iteritems():
                for idx in idx_list:
                    item = self._slots[idx]
                    if not item.check_circulation(circulation_type):
                        continue
                    counter += item.get_current_stack_num()
                    if counter >= num:
                        return True

            return False

    def has_enough_item_by_item_id(self, item_id, num):
        if num <= 0:
            return False
        item = self.get_item_by_item_id(item_id)
        if not item:
            return False
        return item.get_current_stack_num() >= num

    def get_item_by_item_no(self, item_no):
        item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
        if item_sorted_dict is None:
            return
        else:
            idx_list = item_sorted_dict.last()
            if not idx_list:
                return
            item = self._slots[idx_list[0]]
            return item

    def get_item_by_item_obj(self, item_obj):
        item_no = item_obj.item_no
        unlock_time = item_obj.unlock_time
        item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
        if item_sorted_dict is None:
            return
        else:
            idx_list = item_sorted_dict.get(unlock_time, None)
            if not idx_list:
                return
            try:
                item = self._slots[idx_list[0]]
                if not (item is not None and item.item_no == item_no and item.unlock_time == unlock_time):
                    util.log_error('[item %s] unlock_time: %s, slots: %s, item_sorted_dict: %s', item_no, unlock_time, self._slots, item_sorted_dict)
                    return
            except Exception as e:
                util.log_error('[item %s] unlock_time: %s, error: %s', item_no, unlock_time, str(e))
                return

            return item

    def get_item_num_by_no(self, item_no, check_lock=False):
        item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
        if not item_sorted_dict:
            return 0
        counter = 0
        for _, idx_list in item_sorted_dict.sorted_dict_iteritems():
            for idx in idx_list:
                item = self._slots[idx]
                if check_lock and item.is_lock():
                    continue
                counter += item.get_current_stack_num()

        return counter

    def get_circulation_item_num_by_no(self, item_no):
        item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
        if not item_sorted_dict:
            return (0, 0)
        counter, lock_counter = (0, 0)
        for _, idx_list in item_sorted_dict.sorted_dict_iteritems():
            for idx in idx_list:
                item = self._slots[idx]
                stack_num = item.get_current_stack_num()
                if item.is_lock():
                    lock_counter += stack_num
                else:
                    counter += stack_num

        return (
         counter, lock_counter)

    def get_items_by_item_no(self, item_no, check_lock=False):
        item_list = []
        item_sorted_dict = self._no_to_slot_index.get_idx_list(item_no)
        if item_sorted_dict is None:
            return item_list
        else:
            for _, idx_list in item_sorted_dict.reiteritems():
                for idx in idx_list:
                    item = self._slots[idx]
                    if check_lock and item.is_lock():
                        continue
                    item_list.append(item)

            return item_list

    def get_item_by_item_id(self, item_id):
        idx = self._id_to_slot_index.get(item_id)
        if idx is None:
            return
        else:
            return self._slots[idx]
            return

    def get_item_by_type_stype(self, type, stype):
        for item in self._slots:
            if item is not None and item.type == type and item.stype == stype:
                return item

        return

    def get_item_by_type(self, type):
        for item in self._slots:
            if item is not None and item.type == type:
                return item

        return

    def get_items_by_type(self, type):
        return [ item for item in self._slots if item is not None and item.type == type ]

    def get_item_list(self):
        return [ item for item in self._slots if item is not None ]

    def get_items_by_type_list(self, type_list):
        return [ item for item in self._slots if item is not None and item.type in type_list ]

    def check_capacity(self, need_cap):
        return self.MAX_CAPACITY - self._size >= need_cap

    def get_items_by_type_sort_by_create_time(self, type):
        item_list = [ item for item in self._slots if item is not None and item.type == type ]
        item_list.sort(key=lambda x: x.get_create_time())
        return item_list