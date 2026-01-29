# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/ExpireData.py
from __future__ import absolute_import
from logic.gcommon.time_utility import get_server_time

class ExpireData(object):
    BACKUP_TIME = 10800

    def __init__(self, expire_ts=0, bdict=None, need_backup=False):
        self.data = {}
        self.backup_data = {}
        self.expire_ts = expire_ts
        self.last_backup_ts = 0
        self.need_backup = need_backup
        if bdict:
            self.init_from_dict(bdict)

    def init_from_dict(self, bdict):
        self.data = bdict.get('data', {})
        self.last_backup_ts = bdict.get('last_backup_ts', 0)
        self.backup_data = bdict.get('backup_data', 0)
        last_expire_ts = bdict.get('expire_ts', 0) or self.expire_ts
        self._check_expire(last_expire_ts)
        self._check_backup_data()

    def _check_expire(self, expire_ts):
        now = get_server_time()
        if expire_ts and expire_ts < now:
            if self.need_backup and self.data:
                self.backup_data = self.data
                self.last_backup_ts = now
            self.data = {}

    def _check_backup_data(self):
        now = get_server_time()
        if self.need_backup and self.last_backup_ts + self.BACKUP_TIME < now:
            self.last_backup_ts = now
            self.backup_data = {}

    def get_persistent_dict(self):
        pdict = {'data': self.data,
           'expire_ts': self.expire_ts
           }
        if self.need_backup:
            pdict['last_backup_ts'] = self.last_backup_ts
            if self.backup_data:
                pdict['backup_data'] = self.backup_data
        return pdict

    def get_client_dict(self):
        return {'data': self.data
           }

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, item):
        return self.data.get(item, None)