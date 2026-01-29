# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComControlLeaveAOI.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom

class ComControlLeaveAOI(UnitCom):
    BIND_EVENT = {'E_ON_LOGIC_DESTROY': '_on_logic_destroy'
       }

    def __init__(self):
        super(ComControlLeaveAOI, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComControlLeaveAOI, self).init_from_dict(unit_obj, bdict)

    def _on_logic_destroy(self):
        if not self.is_valid():
            return
        else:
            passenger_info = self.ev_g_passenger_info()
            if not passenger_info:
                return
            if not global_data.player:
                return
            l_player = global_data.player.logic
            if not l_player:
                return
            from mobile.common.EntityManager import EntityManager
            for eid, seat_name in six.iteritems(passenger_info):
                if not l_player.ev_g_is_groupmate(eid):
                    continue
                entity = EntityManager.getentity(eid)
                if not entity or not entity.logic:
                    continue
                entity.logic.send_event('E_SET_CONTROL_TARGET', None, {})

            return