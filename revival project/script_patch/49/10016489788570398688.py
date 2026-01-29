# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/ManagerAgentBase.py
from __future__ import absolute_import
from __future__ import print_function
from common.framework import SingletonBase

class ManagerAgentBase(SingletonBase):

    def init(self, need_update=False, *args):
        self.need_update = need_update
        print('init manager agent', self.ALIAS_NAME)

    def on_update(self, dt):
        pass

    def on_replaced(self):
        pass

    def on_stop_game(self):
        pass