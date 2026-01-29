# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/simple_lru_utils.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
import time

def default_time():
    return time.time()


def default_cmp(a, b):
    return a == b


class LRUSimpleList(object):

    def __init__(self, capacity=10):
        super(LRUSimpleList, self).__init__()
        self.capacity = capacity
        self.cur_idx = -1
        self.arr = [ None for x in range(0, self.capacity) ]
        self.mapping = {}
        return

    def push(self, element):
        self.cur_idx += 1
        if self.cur_idx == self.capacity:
            self.cur_idx = 0
        self.arr[self.cur_idx] = element

    def get_cur(self):
        return self.arr[self.cur_idx]

    def get_recent_list(self):
        res = []
        x = self.cur_idx
        for i in range(0, self.capacity):
            if self.arr[x] is None:
                break
            res.append(self.arr[x])
            x -= 1
            if x < 0:
                x = self.capacity - 1

        return res


class LRUSimpleMap(object):

    def __init__(self, capacity=20, time=default_time):
        super(LRUSimpleMap, self).__init__()
        self.capacity = capacity
        self.mp = {}
        self.time = time

    def get_left_recent(self, time_to_left):
        lst_del = []
        now = self.time()
        check_time = now - time_to_left
        for k, t in six.iteritems(self.mp):
            if t < check_time:
                lst_del.append(k)

        for k in lst_del:
            self.mp.pop(k)

        return six_ex.keys(self.mp)

    def push(self, element):
        self.mp[element] = self.time()

    def destory(self):
        self.time = None
        return


class LRUSimpleRecord(object):

    def __init__(self, capacity=100, time=default_time):
        super(LRUSimpleRecord, self).__init__()
        self.capacity = capacity
        self.record = []
        self.time = time

    def get_left_recent(self, time_to_left):
        now = self.time()
        check_time = now - time_to_left
        recent_records = []
        rm_idx = 0
        for idx, record in enumerate(self.record):
            t, k = record
            if t < check_time:
                rm_idx = idx + 1
            else:
                recent_records.append(k)

        self.record = self.record[rm_idx:]
        return recent_records

    def push(self, element):
        if len(self.record) >= self.capacity:
            self.record = self.record[1:]
        now = self.time()
        self.record.append([now, element])

    def destory(self):
        self.time = None
        return