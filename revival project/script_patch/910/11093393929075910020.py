# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/CareerRecord.py
from __future__ import absolute_import
from six.moves import range

class CareerRecord(object):

    def __init__(self, bdict=None):
        self.career_data = {}
        self._is_career_reset = False
        if bdict:
            self.init_from_dict(bdict)

    def init_from_dict(self, bdict):
        self.career_data = bdict.get('career_data', {})
        self._is_career_reset = bdict.get('is_career_reset', False)
        if not self._is_career_reset:
            self._is_career_reset = True
            for task_id in self.career_data:
                self.career_data[task_id][0] = 0

    def get_persistent_dict(self):
        return {'career_data': self.career_data,
           'is_career_reset': self._is_career_reset
           }

    def get_client_dict(self):
        return {'career_data': self.career_data,
           'is_career_reset': True
           }

    def __get_task_record(self, task_id):
        if task_id not in self.career_data:
            self.career_data[task_id] = [
             0, [0, 0, 0]]
        return self.career_data[task_id]

    def get_point_idx(self, task_id):
        task_record = self.__get_task_record(task_id)
        return task_record[0]

    def set_point_idx(self, task_id, point_idx):
        task_record = self.__get_task_record(task_id)
        task_record[0] = point_idx
        return task_record[0]

    def update_point_idx(self, task_id):
        task_record = self.__get_task_record(task_id)
        task_record[0] = task_record[0] + 1
        return task_record[0]

    def get_badge_level(self, task_id):
        task_record = self.__get_task_record(task_id)
        badge_records = task_record[1]
        for lv in range(len(badge_records), 0, -1):
            ts = badge_records[lv - 1]
            if ts > 0:
                return lv

        return 0

    def has_got_badge(self, task_id, lv):
        lv = int(lv)
        task_record = self.__get_task_record(task_id)
        badge_records = task_record[1]
        idx = lv - 1
        if idx >= 0 and idx < len(badge_records) and badge_records[idx] > 0:
            return (True, badge_records[idx])
        else:
            return (
             False, 0.0)

    def get_badge_record(self, task_id):
        task_record = self.__get_task_record(task_id)
        return task_record[1]

    def set_badge_timestamp(self, task_id, badge_idx, timestamp):
        task_record = self.__get_task_record(task_id)
        if 0 <= badge_idx < len(task_record[1]):
            task_record[1][badge_idx] = timestamp
            return task_record[1][badge_idx]
        return 0

    def update_badge_timestamp(self, task_id, badge_idx, timestamp):
        task_record = self.__get_task_record(task_id)
        if 0 <= badge_idx < len(task_record[1]):
            if task_record[1][badge_idx] <= 0:
                task_record[1][badge_idx] = int(timestamp)
            return task_record[1][badge_idx]
        return 0