# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/KeyExpireData.py
from __future__ import absolute_import
from logic.gcommon.time_utility import get_server_time
from .ExpireData import ExpireData

class KeyExpireData(ExpireData):
    BACKUP_TIME = 10800

    def __init__(self, key, bdict=None, need_backup=False):
        self.data_key = key
        self.last_data_key = None
        super(KeyExpireData, self).__init__(0, bdict, need_backup)
        if bdict:
            self.init_from_dict(bdict)
        return

    def init_from_dict(self, bdict):
        self.data = bdict.get('data', {})
        self.last_backup_ts = bdict.get('last_backup_ts', 0)
        self.backup_data = bdict.get('backup_data', 0)
        data_key = bdict.get('data_key', None)
        self.last_data_key = data_key
        self._check_expire(data_key)
        self._check_backup_data()
        return

    def _check_expire(self, data_key):
        if data_key and data_key != self.data_key:
            if self.need_backup and self.data:
                self.backup_data = self.data
                self.last_backup_ts = get_server_time()
            self.data = {}

    def get_persistent_dict(self):
        pdict = {'data': self.data,'data_key': self.data_key
           }
        if self.need_backup:
            pdict['last_backup_ts'] = self.last_backup_ts
            if self.backup_data:
                pdict['backup_data'] = self.backup_data
        return pdict

    def __getitem__(self, item):
        return self.data[item]

    def get(self, item, default=None):
        return self.data.get(item, default)

    def __setitem__(self, key, value):
        self.data[key] = value

    def setdefault(self, key, value):
        self.data.setdefault(key, value)
        return self.data[key]