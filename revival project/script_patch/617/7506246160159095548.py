# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/SimplePortal.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from .NPC import CacheableNPC

@Dynamic
class SimplePortal(CacheableNPC):

    def init_from_dict(self, bdict):
        super(SimplePortal, self).init_from_dict(bdict)
        self.faction_id = bdict.get('faction_id', 0)

    def get_faction(self):
        return self.faction_id

    def on_add_to_battle(self, battle_id):
        super(SimplePortal, self).on_add_to_battle(battle_id)

    def on_remove_from_battle(self):
        super(SimplePortal, self).on_remove_from_battle()