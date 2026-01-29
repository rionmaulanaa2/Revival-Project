# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/SnatchEggData.py
from __future__ import absolute_import
from collections import defaultdict
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
from common.cfg import confmgr
from logic.gcommon.common_const import battle_const

class SnatchEggData(DeathBattleData):

    def init_parameters(self):
        super(SnatchEggData, self).init_parameters()
        self.egg_picker_dict = {}
        self.egg_throw_dict = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'snatchegg_egg_drop': self.on_egg_drop,
           'snatchegg_egg_throw_event': self.on_egg_throw,
           'snatchegg_egg_pick_up': self.on_egg_pick_up
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_egg_picker_dict(self, dict):
        self.egg_picker_dict = dict
        self.egg_throw_dict = {}

    def on_egg_pick_up(self, picker_id, faction, npc_id):
        self.egg_picker_dict[picker_id] = npc_id
        if picker_id in self.egg_throw_dict and self.egg_throw_dict[picker_id] == npc_id:
            self.egg_throw_dict.pop(picker_id)

    def on_egg_throw(self, holder_id, npc_id):
        if holder_id in self.egg_picker_dict and self.egg_picker_dict[holder_id] == npc_id:
            self.egg_throw_dict[holder_id] = npc_id

    def on_egg_drop(self, holder_id, faction, reason, npc_id):
        if holder_id in self.egg_picker_dict and self.egg_picker_dict[holder_id] == npc_id:
            self.egg_picker_dict.pop(holder_id)
        if holder_id in self.egg_throw_dict and self.egg_throw_dict[holder_id] == npc_id:
            self.egg_throw_dict.pop(holder_id)

    def on_finalize(self):
        super(SnatchEggData, self).on_finalize()
        self.egg_picker_dict = {}

    def get_is_in_base_part(self):
        return global_data.battle._round_status != battle_const.ROUND_STATUS_PLAYING