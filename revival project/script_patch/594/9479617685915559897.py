# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleBroadcastUI.py
from __future__ import absolute_import
from logic.comsys.lottery.LotteryBroadcastUI import LotteryBroadcastUI

class BattleBroadcastUI(LotteryBroadcastUI):

    def set_nd_tips(self):
        self.panel.nd_tips.SetPosition('50%-54', '100%-84')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'battle_broadcast_event': self.on_receive_broadcast_notice
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_next_notice(self):
        self.show()
        super(BattleBroadcastUI, self).show_next_notice()