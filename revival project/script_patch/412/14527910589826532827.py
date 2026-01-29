# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/RpcCacheQueue.py
from __future__ import absolute_import
from six.moves import range

class RpcCacheQueue(object):
    __slots__ = ('cache_cap', 'cache_size', 'cache', 'cache_head', 'cache_tail', 'max_seq')

    def __init__(self, cap):
        super(RpcCacheQueue, self).__init__()
        self.cache_cap = cap
        self.cache_size = 0
        self.cache = [None] * self.cache_cap
        self.cache_head = 0
        self.cache_tail = 0
        self.max_seq = 0
        return

    def add(self, op_code, *args):
        elem = (
         op_code, args)
        self.cache[self.cache_tail] = elem
        self.cache_tail = (self.cache_tail + 1) % self.cache_cap
        if self.cache_size == self.cache_cap:
            self.cache_head = self.cache_tail
        else:
            self.cache_size += 1
        self.max_seq += 1

    def clear(self, reset_seq=True):
        self.max_seq = reset_seq and 0 if 1 else self.max_seq
        self.cache_size = 0
        self.cache = [None] * self.cache_cap
        self.cache_head = 0
        self.cache_tail = 0
        return

    def size(self):
        return self.cache_size

    def is_seq_in_cache(self, seq):
        if self.cache_size == 0:
            return False
        else:
            min_seq = self.max_seq - self.cache_size + 1
            return min_seq <= seq <= self.max_seq

    def seq_range(self):
        min_seq = self.max_seq - self.cache_size + 1
        return (
         min_seq, self.max_seq)

    def dispatch(self, from_seq, func):
        if self.cache_size == 0:
            return
        min_seq = self.max_seq - self.cache_size + 1
        if from_seq < min_seq or from_seq > self.max_seq:
            return
        send_idx = from_seq - min_seq
        n_send = self.max_seq - from_seq + 1
        for i in range(send_idx, send_idx + n_send):
            msg_idx = (self.cache_head + i) % self.cache_cap
            op_code, args = self.cache[msg_idx]
            func(op_code, *args)