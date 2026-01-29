# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/cache_lru.py
from __future__ import absolute_import
from __future__ import print_function
from functools import reduce
import six
from six.moves import range
from time import time

class Node(object):
    __slots__ = [
     'prev', 'next', 'key', 'data']

    def __init__(self, key, max_size, need_destroy=True):
        self.prev = None
        self.next = None
        self.key = key
        self.data = CacheDataItem(max_size, need_destroy)
        return

    def clearNode(self):
        self.prev = None
        self.next = None
        self.key = None
        self.data.clear()
        return


class CacheDataItem(object):

    def __init__(self, max_size, need_destroy=True):
        self.max_size = max_size
        self.unused_queue = []
        self._need_destroy = need_destroy
        self.recent_used_timestamp = 0.0
        super(CacheDataItem, self).__init__()

    def add_item(self, item):
        self.recent_used_timestamp = global_data.game_time
        if len(self.unused_queue) < self.max_size:
            self.unused_queue.append(item)
            return True
        return False

    def is_full(self):
        return len(self.unused_queue) >= self.max_size

    def is_empty(self):
        return len(self.unused_queue) == 0

    def pop_item(self):
        self.recent_used_timestamp = global_data.game_time
        if not self.unused_queue:
            return None
        else:
            item = self.unused_queue.pop(-1)
            return item

    def del_item(self):
        item = self.pop_item()
        if item and self._need_destroy:
            self.destroy_item(item)
        return bool(self.unused_queue)

    def destroy_item(self, item):
        release_handler = getattr(item, 'destroy', None)
        valid = getattr(item, 'valid', True)
        if valid and release_handler:
            release_handler()
        return

    def clear(self):
        count = len(self.unused_queue)
        if self._need_destroy:
            for item in self.unused_queue:
                self.destroy_item(item)

        self.unused_queue = []
        return count

    def get_queue_mem_size_tot(self):
        tot = 0
        for item in self.unused_queue:
            tot += item.get_mem_size()

        return tot

    def get_queue_size(self):
        return len(self.unused_queue)


class FixedSizeCacheLRU(object):

    def __init__(self, max_size, node_size, item_size=0, need_destroy=True):
        self._init_data(max_size, node_size, item_size, need_destroy)
        self._init_map()

    def _init_data(self, max_size, node_size, item_size=0, need_destroy=True):
        self.__max_size = max_size
        self.__item_size = item_size if item_size else max_size
        self.__node_size = node_size
        self.__total_count = 0
        self.__node_count = 0
        self._get_count = 0.0
        self._hit_count = 0.0
        self._need_destroy = need_destroy

    def log_info(self):
        print('max_size', self.__max_size, 'item_size', self.__item_size, 'node_size', self.__node_size, 'total_count', self.__total_count, 'node_count', self.__node_count)
        node = self.__old
        print('-------- node info ----------')
        while node:
            print('node is', node)
            print('node key is', node.key)
            print('node next', node.next)
            node = node.next

        print('--------- node end ---------')
        for k, v in six.iteritems(self.__map):
            print(k, v)

        print('--------- map end ---------')

    def get_map(self):
        return self.__map

    def _init_map(self):
        self.__map = {}
        nodes = [ Node(None, self.__item_size, self._need_destroy) for i in range(self.__node_size) ]
        for i, node in enumerate(nodes):
            node.prev = nodes[i - 1] if i != 0 else None
            if i != self.__node_size - 1:
                node.next = nodes[i + 1] if 1 else None
                self.__map[i] = node

        self.__old = nodes[0]
        self.__new = nodes[self.__node_size - 1]
        self.__used_old = None
        return

    def check_key(self, key):
        if isinstance(key, int) and (0 <= key < self.__node_size or key is None):
            pass
        return

    def is_total_count_full(self):
        return self.__total_count >= self.__max_size

    def is_node_count_full(self):
        return self.__node_count >= self.__node_size

    def add_item(self, key, item):
        self.check_key(key)
        if key in self.__map:
            cache_item = self.__map[key]
            self._move_to_new(cache_item)
            cache_data = cache_item.data
            if cache_data.is_full():
                return False
            if self.is_total_count_full():
                self._del_last_used_item()
            self.__total_count += 1
            return cache_data.add_item(item)
        else:
            if self.is_node_count_full():
                self._del_last_used_item(True)
            if self.is_total_count_full():
                self._del_last_used_item()
            old_node = self.__old
            old_node.key = key
            old_node.data.add_item(item)
            self.__map[key] = old_node
            self.__total_count += 1
            self.__node_count += 1
            self._move_to_new(old_node)
            if not self.__used_old:
                self.__used_old = old_node
            return True

        return False

    def del_last_cache(self, key):
        cache_item = self.__map.pop(key)
        cache_item.data.clear()
        self.__node_count -= 1
        cache_item.key = None
        self.__used_old = self.__used_old.next
        return

    def _del_last_used_item(self, is_all=False):
        key = self.__used_old.key
        cache_item = self.__map[key]
        if is_all:
            count = cache_item.data.clear()
            self.__total_count -= count
            self.del_last_cache(key)
        else:
            self.__total_count -= 1
            if not cache_item.data.del_item():
                self.del_last_cache(key)

    def get_item(self, key):
        self.check_key(key)
        cache_item = self.__map.get(key, None)
        self._get_count += 1
        ret_item = None
        if cache_item is not None:
            cache_data = cache_item.data
            ret_item = cache_data.pop_item()
            self.__total_count -= 1
            if cache_data.is_empty():
                self._move_to_old(cache_item)
            else:
                self._move_to_new(cache_item)
            self._hit_count += 1
        return ret_item

    def _move_to_old(self, node_i):
        self.__map.pop(node_i.key)
        node_i.key = None
        self.__node_count -= 1
        node_prev = node_i.prev
        node_next = node_i.next
        if node_i is self.__used_old:
            self.__used_old = node_next
        if node_prev is None:
            return
        else:
            node_i.prev = None
            node_i.next = self.__old
            self.__old.prev = node_i
            self.__old = node_i
            node_prev.next = node_next
            if node_next is not None:
                node_next.prev = node_prev
            else:
                self.__new = node_prev
            return

    def _move_to_new(self, node_i):
        node_prev = node_i.prev
        node_next = node_i.next
        if node_next is None:
            return
        else:
            if node_i is self.__used_old and node_next:
                self.__used_old = node_next
            node_i.prev = self.__new
            node_i.next = None
            self.__new.next = node_i
            self.__new = node_i
            node_next.prev = node_prev
            if node_prev:
                node_prev.next = node_next
            else:
                self.__old = node_next
            return

    def check_auto_del_item(self, interval):
        cur_timestamp = global_data.game_time
        if self.__used_old:
            last_used_timestamp = self.__map[self.__used_old.key].data.recent_used_timestamp
            if last_used_timestamp != 0.0 and cur_timestamp - last_used_timestamp >= interval:
                self._del_last_used_item()
        return self.__total_count <= 0

    def destroy(self):
        for i in six.itervalues(self.__map):
            i.clearNode()

        self.__map = {}


class CacheLRU(object):

    def __init__(self, size, release_handler):
        self._init_map(size)
        self.__max = size
        self.release_handler = release_handler

    def _init_map(self, size):
        self.__map = {}
        nodes = [ Node(i) for i in range(size) ]
        for i in range(size):
            if i == 0:
                nodes[i].prev = None
                nodes[i].next = nodes[i + 1]
            elif i != size - 1:
                nodes[i].prev = nodes[i - 1]
                nodes[i].next = nodes[i + 1]
            else:
                nodes[i].prev = nodes[i - 1]
                nodes[i].next = None
            self.__map[i] = [None, nodes[i]]

        self.__old = nodes[0]
        self.__new = nodes[size - 1]
        return

    def _move_to_new(self, node_i):
        node_prev = node_i.prev
        node_next = node_i.next
        if node_next is None:
            pass
        elif node_prev is not None:
            node_prev.next = node_next
            node_next.prev = node_prev
            node_i.prev = self.__new
            node_i.next = None
            self.__new.next = node_i
            self.__new = node_i
        else:
            node_next.prev = None
            self.__old = node_next
            node_i.prev = self.__new
            node_i.next = None
            self.__new.next = node_i
            self.__new = node_i
        return

    def get(self, key):
        vnn = self.__map.get(key, None)
        if vnn:
            self._move_to_new(vnn[1])
            return vnn[0]
        else:
            return

    def add(self, key, value):
        vt = self.__map.get(key, None)
        if vt:
            self.release_obj(vt[0])
            vt[0] = value
            self._move_to_new(vt[1])
        else:
            if self.__old.key:
                vt = self.__map.pop(self.__old.key)
                self.release_obj(vt[0])
            self.__old.key = key
            self.__map[key] = [value, self.__old]
            self._move_to_new(self.__old)
        return

    def size(self):
        return reduce(--- This code section failed: ---

 369       0  LOAD_FAST             1  'y'
           3  LOAD_CONST            1  ''
           6  BINARY_SUBSCR    
           7  POP_JUMP_IF_FALSE    17  'to 17'
          10  POP_JUMP_IF_FALSE     2  'to 2'
          13  BINARY_ADD       
        14_0  COME_FROM                '10'
        14_1  COME_FROM                '7'
          14  JUMP_IF_TRUE_OR_POP    20  'to 20'
          17  LOAD_FAST             0  'x'
        20_0  COME_FROM                '14'
          20  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 10
, six.itervalues(self.__map), 0)

    def clear(self):
        for i in six.itervalues(self.__map):
            self.release_obj(i[0])
            i[1].clearNode()

        self._init_map(self.__max)

    def destroy(self):
        for i in six.itervalues(self.__map):
            self.release_obj(i[0])
            i[0] = None
            i[1].clearNode()

        self.__map = {}
        return

    def __str__(self):
        result = ''
        node = self.__old
        while node is not None:
            result += str(node.key) + ', '
            node = node.next

        return result

    def release_obj(self, v):
        if v and self.release_handler:
            self.release_handler(v)

    def get_all_item_mem_info(self):
        info = {}
        for k, v in six.iteritems(self.__map):
            if v[0]:
                info[k] = {'mem_size_tot': v[0].get_queue_mem_size_tot() / 1024.0 / 1024.0,'length': v[0].get_queue_size()}

        return info