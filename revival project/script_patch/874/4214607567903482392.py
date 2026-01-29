# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Shop.py
from __future__ import absolute_import
from .NPC import NPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class Shop(NPC):

    def __init__(self, entity_id=None):
        super(Shop, self).__init__(entity_id)

    def init_from_dict(self, bdict):
        self._faction_id = bdict.get('faction_id')
        super(Shop, self).init_from_dict(bdict)

    def get_faction_id(self):
        return self._faction_id