# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Motorcycle.py
from __future__ import absolute_import
import six_ex
from mobile.common.EntityManager import Dynamic
from .NPC import NPC
from mobile.common.EntityManager import EntityManager

@Dynamic
class Motorcycle(NPC):

    def init_from_dict(self, bdict):
        super(Motorcycle, self).init_from_dict(bdict)

    def is_share(self):
        return False

    def on_add_to_battle(self, battle_id):
        bdata = self._data
        super(Motorcycle, self).on_add_to_battle(battle_id)
        if bdata:
            driver_id = bdata.get('driver_id')
            passenger_info = bdata.get('passenger_dict')
            target = self
            for passenger_id, seat_name in six_ex.items(passenger_info):
                passenger_entity = EntityManager.getentity(passenger_id)
                if passenger_entity:
                    ctrl_conf = {'seat_name': seat_name}
                    passenger_entity.logic.send_event('E_SET_CONTROL_TARGET', target, ctrl_conf, False, True)

            myid = global_data.player.id
            if myid == driver_id or myid in six_ex.keys(passenger_info):
                global_data.mecha = target
                target.logic.send_event('E_ENABLE_SYNC', True)
                target.logic.send_event('E_CONTROL_MECHA_TWO', True, True, is_reconnect=True)
            elif global_data.player and global_data.player.logic and driver_id and driver_id == global_data.player.logic.ev_g_spectate_target_id():
                target.logic.send_event('E_OBSERVE_CONTROL_MECHA_TWO')