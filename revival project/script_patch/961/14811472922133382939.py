# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComDrivable.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
import time

class ComDrivable(UnitCom):
    BIND_EVENT = {'E_MOUNTS_LOADED': '_on_loaded',
       'E_BUILDING_ENABLE': '_on_building_enable',
       'E_ASSIST_GET_ON': '_on_assist_get_on',
       'G_MOUNTS': '_on_get_mounts'
       }

    def __init__(self):
        super(ComDrivable, self).__init__()
        self._mounts_model = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComDrivable, self).init_from_dict(unit_obj, bdict)
        self._owner_id = bdict['owner_id']
        self._birth_time = bdict.get('birthtime', None)
        self._effective = bdict['effective']
        self.have_assist = False
        return

    def destroy(self):
        player = EntityManager.getentity(self._owner_id)
        if player and player.logic and self.have_assist:
            player.logic.send_event('E_ASSIST_GET_OFF')
        super(ComDrivable, self).destroy()

    def _on_loaded(self, m, action):
        self._mounts_model = m
        if self._birth_time and self._effective:
            build_time = time.time() - self._birth_time
            message = 'E_BEGIN_CONTROL' if build_time < 5 else 'E_SECOND_CONTROL'
            player = EntityManager.getentity(self._owner_id)
            if player and player.logic:
                player.logic.send_event(message, self.unit_obj.id, action)

    def _on_building_enable(self, enable):
        self._effective = enable
        if self._owner_id == global_data.player.id:
            return
        if not enable:
            player = EntityManager.getentity(self._owner_id)
            if player and player.logic:
                player.logic.send_event('E_ASSIST_GET_OFF', True)

    def _on_assist_get_on(self, get_on):
        self.have_assist = get_on

    def _on_get_mounts(self):
        return self._mounts_model