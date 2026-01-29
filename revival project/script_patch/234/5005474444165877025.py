# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Charger.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from logic.entities.NPC import NPC
from logic.gcommon.common_const.guide_const import GUIDE_CHARGER

@Dynamic
class Charger(NPC):

    def on_add_to_battle(self, battle_id):
        super(Charger, self).on_add_to_battle(battle_id)
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_GUIDE_ADD_ENTITY', GUIDE_CHARGER, self)
        return

    def on_remove_from_battle(self):
        super(Charger, self).on_remove_from_battle()
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_GUIDE_DEL_ENTITY', GUIDE_CHARGER, self)
        return