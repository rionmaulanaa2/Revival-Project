# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ConcertArena.py
from __future__ import absolute_import
from .NPC import NPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class ConcertArena(NPC):

    def __init__(self, entity_id=None):
        super(ConcertArena, self).__init__(entity_id)

    def init_from_dict(self, bdict):
        super(ConcertArena, self).init_from_dict(bdict)


def TT():
    from mobile.common.EntityFactory import EntityFactory
    from mobile.common.IdManager import IdManager
    entity_id = IdManager.genid()
    entity_obj = EntityFactory.instance().create_entity('ConcertArena', entity_id)
    position = global_data.cam_lplayer.ev_g_position()
    entity_obj.init_from_dict({'position': [position.x + 20, position.y, position.z]})
    entity_obj.on_add_to_battle(global_data.player.battle_id)