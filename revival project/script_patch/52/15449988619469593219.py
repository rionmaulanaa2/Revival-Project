# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/BaseClientEntity.py
from __future__ import absolute_import
from mobile.client.ClientEntity import ClientEntity
from mobile.common.EntityManager import EntityManager

class BaseClientEntity(ClientEntity):

    def __init__(self, entityid=None):
        super(BaseClientEntity, self).__init__(entityid)
        self.battle_id = None
        self.logic = None
        return

    def init_from_dict(self, bdict):
        self.update_data_from_dict(bdict)

    def update_from_dict(self, bdict):
        pass

    def destroy(self):
        self.battle_id = None
        super(BaseClientEntity, self).destroy()
        return

    def get_battle(self):
        if self.battle_id is None:
            return
        else:
            battle = EntityManager.getentity(self.battle_id)
            if battle is None:
                return
            return battle

    def on_add_to_battle(self, battle_id):
        self.battle_id = battle_id

    def on_update_to_battle(self, battle_id):
        self.battle_id = battle_id

    def on_remove_from_battle(self):
        self.battle_id = None
        return

    def tick(self, delta):
        if self.logic:
            self.logic.tick(delta)