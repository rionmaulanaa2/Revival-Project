# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/RewardRecord.py
from __future__ import absolute_import
import six
from .Record import Record

class RewardRecord(dict):

    def __init__(self):
        self.reward_records = {}

    def init_from_dict(self, bdict):
        self.reward_records = {reward_type:Record(record_dict) for reward_type, record_dict in six.iteritems(bdict)}

    def get_persistent_dict(self):
        return {reward_type:record.get_persistent_dict() for reward_type, record in six.iteritems(self.reward_records)}

    def get_client_dict(self):
        return {reward_type:record.get_persistent_dict() for reward_type, record in six.iteritems(self.reward_records)}

    def compact(self, record_id):
        for record in six.itervalues(self):
            record.compact(record_id)

    def clear(self):
        self.reward_records.clear()

    def iteritems(self):
        return six.iteritems(self.reward_records)

    def itervalues(self):
        return six.itervalues(self.reward_records)

    def iterkeys(self):
        return six.iterkeys(self.reward_records)

    def setdefault(self, reward_type, record):
        return self.reward_records.setdefault(reward_type, record)

    def get(self, reward_type, default=None):
        return self.reward_records.get(reward_type, default)

    def __contains__(self, reward_type):
        return reward_type in self.reward_records

    def __getitem__(self, reward_type):
        return self.reward_records[reward_type]

    def __setitem__(self, reward_type, record):
        self.reward_records[reward_type] = record

    def __delitem__(self, reward_type):
        del self.reward_records[reward_type]