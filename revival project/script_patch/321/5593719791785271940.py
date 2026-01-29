# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/Record.py
from __future__ import absolute_import
from six.moves import range

class Record(object):

    def __init__(self, bdict=None):
        self.last_record_id = 0
        self.record_set = set()
        if bdict:
            self.init_from_dict(bdict)

    def init_from_dict(self, bdict):
        self.last_record_id = bdict.get('last_record_id', 0)
        self.record_set = set(bdict.get('record_set', []))

    def get_persistent_dict(self):
        return {'last_record_id': self.last_record_id,
           'record_set': list(self.record_set)
           }

    def get_client_dict(self):
        return {'last_record_id': self.last_record_id,
           'record_set': list(self.record_set)
           }

    def is_record(self, record_id):
        return record_id <= self.last_record_id or record_id in self.record_set

    def clear(self):
        self.last_record_id = 0
        self.record_set = set()

    def update(self, last_record_id, record_set):
        self.last_record_id = last_record_id
        self.record_set |= record_set

    def compact(self, max_record_id):
        for record_id in range(self.last_record_id + 1, max_record_id + 1):
            if record_id in self.record_set:
                self.last_record_id = record_id
                self.record_set.remove(record_id)
            else:
                break

    def record(self, record_id):
        if record_id == self.last_record_id + 1:
            self.last_record_id = record_id
        else:
            self.record_set.add(record_id)

    def get_reward_set(self):
        set_continue = set((lv + 1 for lv in range(self.last_record_id)))
        return set_continue | self.record_set

    def remove(self, record_id):
        if record_id <= 0 or not self.is_record(record_id):
            return
        if record_id in self.record_set:
            self.record_set.remove(record_id)
        elif record_id == self.last_record_id:
            self.last_record_id = self.last_record_id - 1
        elif record_id < self.last_record_id:
            for i in range(record_id + 1, self.last_record_id + 1):
                self.record_set.add(i)

            self.last_record_id = record_id - 1