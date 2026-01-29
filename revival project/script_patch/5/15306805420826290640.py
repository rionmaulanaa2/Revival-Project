# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Monster.py
from __future__ import absolute_import
from logic.entities.NPC import CacheableNPC
from mobile.common.EntityManager import Dynamic
from logic.gcommon.common_const.guide_const import GUIDE_MONSTER

@Dynamic
class Monster(CacheableNPC):

    def __init__(self, entityid=None):
        if global_data.use_sunshine:
            from sunshine.Editor.Meta.MonsterMeta import InitMonsterMetaLink
            InitMonsterMetaLink(self)
        super(Monster, self).__init__(entityid)

    def init_from_dict(self, bdict):
        super(Monster, self).init_from_dict(bdict)
        self._monster_id = self._data.get('npc_id', None)
        self._pve_monster_level = self._data.get('pve_monster_level', 1)
        return

    def on_add_to_battle(self, battle_id):
        super(Monster, self).on_add_to_battle(battle_id)
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_GUIDE_ADD_ENTITY', GUIDE_MONSTER, self)
        battle = self.get_battle()
        battle.add_actor_id(self.id)
        return

    def on_remove_from_battle(self):
        battle = self.get_battle()
        battle.del_actor_id(self.id)
        super(Monster, self).on_remove_from_battle()
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_GUIDE_DEL_ENTITY', GUIDE_MONSTER, self)
        return

    def get_pve_monster_level(self):
        return self._pve_monster_level

    def get_monster_id(self):
        return self._monster_id

    def destroy(self):
        super(Monster, self).destroy()