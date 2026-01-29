# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Airship.py
from __future__ import absolute_import
from .NPC import NPC
from mobile.common.EntityManager import Dynamic

@Dynamic
class Airship(NPC):

    def on_add_to_battle(self, battle_id):
        from mobile.common.EntityManager import EntityManager
        vehicle_data = self._data
        super(Airship, self).on_add_to_battle(battle_id)
        driver_id = self.logic.sd.ref_driver_id
        passenger_ids = self.logic.ev_g_passenger()
        driver = None
        if driver_id:
            driver = EntityManager.getentity(driver_id)
        target = self
        if driver:
            driver.logic.send_event('E_SET_CONTROL_TARGET', target)
        myid = global_data.player.id
        if myid == driver_id:
            target.logic.send_event('E_START_CONTROL_VEHICLE')
        if passenger_ids:
            for pid in passenger_ids:
                if driver_id == pid:
                    continue
                p = EntityManager.getentity(pid)
                if p:
                    p.logic.send_event('E_SET_CONTROL_TARGET', target)

        return