# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/CrystalBuff.py
from __future__ import absolute_import
from .NPC import NPC

class CrystalBuff(NPC):

    def init_from_dict(self, bdict):
        super(CrystalBuff, self).init_from_dict(bdict)
        self.player_cnt = bdict.get('player_cnt', 0)
        self.faction_id = bdict.get('faction_id', 0)
        self.crystal_stage = bdict.get('crystal_stage')
        if self.crystal_stage is None:
            ui = global_data.ui_mgr.show_ui('CrystalMarkUI', 'logic.comsys.battle.Crystal')
            ui and ui.update_crystal_buff_cnt(self.faction_id, self.player_cnt)
        return