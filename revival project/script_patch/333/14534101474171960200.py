# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/idle_workqueue.py
from __future__ import absolute_import
from common.framework import Singleton

class IdleWorkQueue(Singleton):

    def init(self):
        self._workqueue = []

    def add_idle_workqueue(self, key, callfunc):
        old_queue = self.find_idle_workqueue(key)
        if old_queue:
            self._workqueue.remove(old_queue)
        self._workqueue.append([key, callfunc])

    def find_idle_workqueue(self, key):
        for i, info in enumerate(self._workqueue):
            if info[0] == key:
                return info

        return None

    def update(self, dt):
        if len(self._workqueue) <= 0:
            return
        else:
            pick_queue = self._workqueue[0]
            func = pick_queue[1]
            try:
                ret = func()
                if ret == None or ret == True:
                    self._workqueue.remove(pick_queue)
            except Exception as e:
                self._workqueue.remove(pick_queue)

            return