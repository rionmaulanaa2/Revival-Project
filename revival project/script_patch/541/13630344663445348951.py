# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHealthFishHeadTargetClient.py
from ..share.ComHealth import ComHealth
FISH_HEAD_DAMAGED_HP_RATE = 0.3

class ComHealthFishHeadTargetClient(ComHealth):

    def set_hp(self, hp):
        super(ComHealthFishHeadTargetClient, self).set_hp(hp)
        if self.get_hp_percent() < FISH_HEAD_DAMAGED_HP_RATE:
            self.send_event('E_FISH_HEAD_TARGET_LOW_HP')