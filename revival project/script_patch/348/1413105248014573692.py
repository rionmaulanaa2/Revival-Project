# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Building.py
from __future__ import absolute_import
from .NPC import CacheableNPC
from mobile.common.EntityManager import Dynamic
from logic.gcommon.common_const import building_const as b_const
from logic.gcommon.common_const.guide_const import GUIDE_BOUNCER

@Dynamic
class Building(CacheableNPC):

    def __init__(self, entity_id=None):
        super(Building, self).__init__(entity_id)
        self._is_bouncer = False

    def cache(self):
        super(Building, self).cache()
        self._is_bouncer = False

    def init_from_dict(self, bdict):
        super(Building, self).init_from_dict(bdict)
        if bdict.get('building_no') in b_const.B_BOUNCER_LIST:
            self._is_bouncer = True
            logic = global_data.player.logic if global_data.player else None
            if logic:
                logic.send_event('E_GUIDE_ADD_ENTITY', GUIDE_BOUNCER, self)
        return

    def on_remove_from_battle(self):
        super(Building, self).on_remove_from_battle()
        if self._is_bouncer:
            logic = global_data.player.logic if global_data.player else None
            if logic:
                logic.send_event('E_GUIDE_DEL_ENTITY', GUIDE_BOUNCER, self)
        return