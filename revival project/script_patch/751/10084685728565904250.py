# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crown/CrownBattleData.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData, CBornData
import logic.gcommon.time_utility as tutil
from logic.gcommon.common_const.battle_const import CROWN_OTHER_FACTION, CROWN_SELF_FACTION, CROWN_TEAM_FACTION

class CrownBattleData(DeathBattleData):

    def init_parameters(self):
        super(CrownBattleData, self).init_parameters()
        self.crown_dict = {CROWN_OTHER_FACTION: None,
           CROWN_SELF_FACTION: None,
           CROWN_TEAM_FACTION: None
           }
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_crown_born': self.on_crown_born,
           'on_crown_death': self.on_crown_death
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_born_point(self, group_born_dict, born_point_list):
        for key in self.temp_born_point_key:
            del self.born_data[key]

        self.temp_born_point_key = []
        for index, data in enumerate(born_point_list):
            self.born_data[str(index)] = CBornData(str(index))
            self.born_data[str(index)].set_data(data)
            self.temp_born_point_key.append(str(index))

        for group_id, data in six.iteritems(group_born_dict):
            if group_id not in self.born_data:
                self.born_data[group_id] = CBornData(group_id)
            self.born_data[group_id].set_data(data)

        global_data.emgr.update_death_born_point.emit()
        self.check_pos()

    def on_crown_born(self, king_id, king_faction):
        self.crown_dict[king_faction] = king_id

    def on_crown_death(self, king_id, king_faction):
        self.crown_dict[king_faction] = None
        return

    def get_team_crown_id(self):
        return self.crown_dict.get(CROWN_TEAM_FACTION, None)