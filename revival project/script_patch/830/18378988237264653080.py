# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/MonitorManager.py
from __future__ import absolute_import
from .MonitorWatch import access_type_rw, access_type_rb, Watch

class MonitorManager(object):

    def __init__(self):
        super(MonitorManager, self).__init__()
        self._Watch = Watch('_root', access_type_rw)

    def get(self, key):
        return self._Watch.getnode(key)

    def monitor_info(self):
        return self._Watch.watch_to_dict()

    def monitor_set(self, value, key):
        watch = self._Watch
        index = 0
        while index < len(key) - 1:
            ret, watch = watch.getnode(key[index])
            index += 1
            if not ret:
                return False

        return watch.setvalue(key[index], value)

    def monitor_get(self, key):
        watch = self._Watch
        index = 0
        while index < len(key) - 1:
            ret, watch = watch.getnode(key[index])
            index += 1
            if not ret:
                return (False, None)

        if index < len(key):
            ret, value = watch.getnode(key[index])
            if not ret:
                ret, watch = watch.getvalue(key[index])
            else:
                watch = value.watch_to_dict()
        return (
         ret, watch)

    def monitor_create_watch(self, key, telnet_access=access_type_rw):
        return self._Watch.createwatch(key, telnet_access)