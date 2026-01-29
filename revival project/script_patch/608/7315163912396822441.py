# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/RatRobot.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from .NPC import CacheableNPC

@Dynamic
class RatRobot(CacheableNPC):

    def on_add_to_battle(self, battle_id):
        super(RatRobot, self).on_add_to_battle(battle_id)
        global_data.war_lrobots[self.id] = self.logic

    def on_remove_from_battle(self):
        global_data.war_lrobots.pop(self.id, None)
        super(RatRobot, self).on_remove_from_battle()
        return