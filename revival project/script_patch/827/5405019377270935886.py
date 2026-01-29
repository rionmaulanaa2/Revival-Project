# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Drone.py
from __future__ import absolute_import
from .NPC import NPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class Drone(NPC):

    def on_remove_from_battle(self):
        control_id = self.logic.ev_g_controler()
        self.logic.send_event('E_YIELD_CONTROL', control_id, False)
        super(Drone, self).on_remove_from_battle()