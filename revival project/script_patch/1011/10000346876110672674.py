# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/TrainCarriage.py
from __future__ import absolute_import
from .NPC import CacheableNPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class TrainCarriage(CacheableNPC):

    def init_from_dict(self, bdict):
        super(TrainCarriage, self).init_from_dict(bdict)
        as_base = bdict.get('as_base')
        if as_base:
            global_data.carry_mgr.register_base_ent(self.id)

    def on_remove_from_battle(self):
        global_data.carry_mgr.unregister_base_ent(self.id)
        super(TrainCarriage, self).on_remove_from_battle()