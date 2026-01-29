# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Plane.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from .NPC import NPC

@Dynamic
class Plane(NPC):

    def __init__(self, entity_id=None):
        super(Plane, self).__init__(entity_id)

    def init_from_dict(self, bdict):
        super(Plane, self).init_from_dict(bdict)
        self.init_event()

    def init_event(self):
        global_data.emgr.plane_destroy_event += self.remove_from_battle

    def remove_from_battle(self):
        if self.get_battle():
            self.get_battle().destroy_entity(self.id)