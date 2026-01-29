# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComRelevance.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager

class ComRelevance(UnitCom):
    BIND_EVENT = {'E_RELEVANCE_EVENT': '_send_relevance_event',
       'G_RELEVANCE_ID': '_get_relevance_id'
       }

    def __init__(self):
        super(ComRelevance, self).__init__(need_update=True)
        self._relevance_ids = []

    def init_from_dict(self, unit_obj, bdict):
        super(ComRelevance, self).init_from_dict(unit_obj, bdict)
        self._relevance_ids = bdict.get('relevance_ids', [])

    def get_client_dict(self):
        return {'relevance_ids': self._relevance_ids
           }

    def _get_relevance_id(self):
        if self._relevance_ids:
            return self._relevance_ids[0]

    def _send_relevance_event(self, event, *args, **kwargs):
        getentity = EntityManager.getentity
        for eid in self._relevance_ids:
            entity = getentity(eid)
            if not entity:
                continue
            logic = entity.logic
            if not logic or not logic.is_valid():
                continue
            logic.send_event(event, *args, **kwargs)