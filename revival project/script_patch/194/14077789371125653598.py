# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/DeathDoor.py
from __future__ import absolute_import
from .NPC import FullCacheableNPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class DeathDoor(FullCacheableNPC):

    def __init__(self, entityid=None):
        super(DeathDoor, self).__init__(entityid)
        self._group_limit = None
        return

    def init_from_dict(self, bdict):
        super(DeathDoor, self).init_from_dict(bdict)
        self._group_limit = bdict.get('group_limit', None)
        self.npc_id = bdict.get('npc_id')
        return

    def on_add_to_battle(self, battle_id):
        super(DeathDoor, self).on_add_to_battle(battle_id)
        global_data.death_battle_door_col.add_door_entity_id(self.npc_id, self.id)

    def cache(self):
        self._group_limit = None
        super(DeathDoor, self).cache()
        return

    def report_enter(self, entity):
        if not entity.logic:
            return
        self.call_soul_method('report_enter', (entity.id,))

    def report_leave(self, entity):
        if not entity.logic:
            return
        self.call_soul_method('report_leave', (entity.id,))