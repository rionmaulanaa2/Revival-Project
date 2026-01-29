# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Puppet.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from logic.entities.BaseClientEntity import BaseClientEntity
from ext_package.ext_decorator import ext_role_use_org_skin

@Dynamic
class Puppet(BaseClientEntity):

    @ext_role_use_org_skin
    def init_from_dict(self, bdict):
        super(Puppet, self).init_from_dict(bdict)
        self._data = bdict
        self.uid = bdict.get('uid', None)
        self.lv = bdict.get('lv', 1)
        self.lobby_mecha_id = bdict.get('lobby_mecha_id', None)
        self.lobby_mecha_fashion = bdict.get('lobby_mecha_fashion', {})
        self._is_robot = bdict.get('is_robot', False)
        return

    def is_cacheable(self):
        return True

    def cache(self):
        self._data = None
        self.uid = None
        self.lv = None
        self._is_robot = None
        super(Puppet, self).cache()
        return

    def on_add_to_battle(self, battle_id):
        super(Puppet, self).on_add_to_battle(battle_id)
        battle = self.get_battle()
        kill = self._data.get('kill', 0)
        kill_mecha = self._data.get('kill_mecha', 0)
        assist_mecha = self._data.get('assist_mecha', 0)
        battle.update_battle_statistics(self.id, kill, kill_mecha, assist_mecha)
        battle.add_actor_id(self.id)
        if self._is_robot and not global_data.player.is_in_global_spectate():
            from logic.units.LPuppetRobot import LPuppetRobot
            self.logic = LPuppetRobot(self, self.get_battle())
            global_data.war_lrobots[self.id] = self.logic
        else:
            from logic.units.LPuppet import LPuppet
            self.logic = LPuppet(self, self.get_battle())
        self.logic.init_from_dict(self._data)
        global_data.war_puppets[self.id] = self.logic
        if not global_data.player.logic.ev_g_is_groupmate(self.id):
            global_data.war_noteam_puppets[self.id] = self.logic
        else:
            global_data.ccmini_mgr.set_entityid_map(self._data['uid'], self.id)
        self._data = None
        return

    def on_remove_from_battle(self):
        battle = self.get_battle()
        battle.del_actor_id(self.id)
        global_data.war_puppets.pop(self.id, None)
        if self._is_robot:
            global_data.war_lrobots.pop(self.id, None)
        if self.id in global_data.war_noteam_puppets:
            del global_data.war_noteam_puppets[self.id]
        else:
            global_data.ccmini_mgr.del_uid_by_entityid(self.id)
        if self.logic:
            self.logic.destroy()
            self.logic = None
        super(Puppet, self).on_remove_from_battle()
        return

    def get_lobby_mecha_info(self):
        return (
         self.lobby_mecha_id, self.lobby_mecha_fashion)