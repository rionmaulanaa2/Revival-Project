# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/pos_change_mgr.py
from __future__ import absolute_import
import time
_G_LOG_TIMES = 0

class PosChangeMgr(object):
    __slots__ = ('listeners', )

    def __init__(self):
        self.listeners = []

    def add_pos_listener(self, listener, interval=0):
        self.listeners.append([listener, interval, -1])

    def del_pos_listener(self, listener):
        for info in self.listeners:
            if listener == info[0]:
                self.listeners.remove(info)
                break

    def notify_pos_change(self, pos, instantly=False):
        global _G_LOG_TIMES
        if pos is None and G_IS_CLIENT:
            if _G_LOG_TIMES:
                return
            _G_LOG_TIMES = 1
            from exception_hook import post_stack
            post_stack('[TRACE INFO] notify_pos_change error, pos is None')
        cur_time = global_data.game_time if G_IS_CLIENT else time.time()
        for info in self.listeners:
            if cur_time - info[2] >= info[1] or instantly:
                info[0](pos)
                info[2] = cur_time

        return

    def destroy(self):
        self.listeners = None
        return