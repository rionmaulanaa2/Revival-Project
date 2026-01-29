# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/MonsterStateBase.py
from __future__ import absolute_import
from .StateBase import StateBase

class MonsterStateBase(StateBase):

    def exit(self, enter_states):
        super(MonsterStateBase, self).exit(enter_states)
        self.send_event('E_ON_STATE_EXIT', self.sid)