# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/FogField.py
from __future__ import absolute_import
from logic.entities.NPC import CacheableNPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class FogField(CacheableNPC):

    def __init__(self, entityid=None):
        super(FogField, self).__init__(entityid)
        self._creator_id = None
        self._tag = None
        self._group_limit = None
        return

    def init_from_dict(self, bdict):
        super(FogField, self).init_from_dict(bdict)
        self._creator_id = bdict.get('creator_id', None)
        self._tag = bdict.get('tag', None)
        self._group_limit = bdict.get('group_limit', None)
        return

    def cache(self):
        self._creator_id = None
        self._tag = None
        self._group_limit = None
        super(FogField, self).cache()
        return

    def report_leave(self, entity):
        if not entity.logic:
            return
        else:
            if self._group_limit is not None and entity.logic.ev_g_group_id() != self._group_limit:
                return
            self.call_soul_method('report_leave', (entity.id,))
            return