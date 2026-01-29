# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSelectionMechaTrans.py
from __future__ import absolute_import
from .ComSelectionBase import ComSelectionBase
import math3d
import world
import logic.gcommon.common_const.animation_const as animation_const
from mobile.common.EntityManager import EntityManager
from logic.gcommon.cdata import status_config

class ComSelectionMechaTrans(ComSelectionBase):
    BIND_EVENT = ComSelectionBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CHANGE_PASSENGER': 'change_passenger'
       })

    def __init__(self):
        super(ComSelectionMechaTrans, self).__init__()

    def _on_being_selected(self, id_selector, control_info):
        super(ComSelectionMechaTrans, self)._on_being_selected(id_selector, control_info)

    def _on_losing_selected(self, control_info):
        super(ComSelectionMechaTrans, self)._on_losing_selected(control_info)

    def change_passenger(self, passenger_id, seat_name):
        if passenger_id not in self.mp_holder:
            return
        passenger_entity = self.try_get_selector_entity(passenger_id)
        if not passenger_entity or not passenger_entity.logic:
            log_error('[test--ComSelectionMechaTrans.change_passenger] Getting passenger_entity entity by id error.')
            return
        control_info = self.mp_holder[passenger_id]
        control_info['seat_name'] = seat_name
        passenger_model = passenger_entity.logic.ev_g_model()
        vehicle_model = self.ev_g_model()
        if not vehicle_model or not passenger_model:
            return
        vehicle_model.unbind(passenger_model)
        vehicle_model.bind(seat_name, passenger_model, world.BIND_TYPE_ALL)
        vehicle_entity = EntityManager.getentity(self.unit_obj.id)
        passenger_entity.logic.send_event('E_ON_ACTION_ON_VEHICLE', vehicle_entity)
        is_driver = self.sd.ref_driver_id == passenger_entity.logic.id
        vehicle_entity = EntityManager.getentity(self.unit_obj.id)
        driver_state = passenger_entity.logic.ev_g_vehicle_state(vehicle_entity) or status_config.ST_MECHA_DRIVER
        if passenger_entity.logic.ev_g_is_enable_behavior():
            passenger_entity.logic.send_event('E_ACTIVE_STATE', driver_state)
        else:
            passenger_entity.logic.ev_g_status_try_trans(driver_state)
            passenger_entity.logic.send_event('E_FORCE_MECHA_DRIVER')
        self.send_event('E_PASSENGER_BINDED_SEAT', passenger_id)

    def do_model_binding(self, passenger_id, passenger_model, vehicle_model):
        if passenger_id not in self.mp_holder:
            return
        else:
            control_info = self.mp_holder[passenger_id]
            from logic.gcommon.common_const import mecha_const
            is_vehicle = self.ev_g_is_vehicle()
            vconf = self.ev_g_vehicle_conf()
            seat_socks = vconf['seatpoints']
            seat_name = control_info.get('seat_name')
            if not seat_name:
                seat_name = self.ev_g_passenger_seat(passenger_id)
                if not seat_name:
                    seat_name = seat_socks[0]
            vehicle_model.visible = True
            bmodel = vehicle_model.get_socket_obj(seat_name, -1)
            if bmodel is None:
                passenger_model.remove_from_parent()
                passenger_model.visible = True
                vehicle_model.bind(seat_name, passenger_model, world.BIND_TYPE_ALL)
                passenger_model.position = math3d.vector(0, 0, 0)
                passenger_model.world_rotation_matrix = vehicle_model.world_rotation_matrix
            e_selector = EntityManager.getentity(passenger_id)
            vehicle_entity = EntityManager.getentity(self.unit_obj.id)
            if is_vehicle:
                self.send_event('E_ON_ACTION_ON_VEHICLE')
                if e_selector and e_selector.logic:
                    e_selector.logic.send_event('E_ON_ACTION_ON_VEHICLE', vehicle_entity)
            enable = self.ev_g_is_avatar()
            self.send_event('E_ENABLE_BEHAVIOR', enable)
            if e_selector and e_selector.logic:
                is_driver = self.sd.ref_driver_id == e_selector.logic.id
                driver_state = e_selector.logic.ev_g_vehicle_state(vehicle_entity) or status_config.ST_MECHA_DRIVER
                e_selector.logic.ev_g_cancel_state(status_config.ST_ROLL)
                if self.unit_obj.__class__.__name__ == 'LMechaTrans' and e_selector.logic.ev_g_is_human() and e_selector.logic.ev_g_is_avatar():
                    if not e_selector.logic.ev_g_is_enable_behavior():
                        e_selector.logic.send_event('E_ENABLE_BEHAVIOR')
                if e_selector.logic.ev_g_is_enable_behavior():
                    e_selector.logic.send_event('E_ACTIVE_STATE', driver_state)
                else:
                    e_selector.logic.ev_g_status_try_trans(driver_state)
                    e_selector.logic.send_event('E_FORCE_MECHA_DRIVER')
                e_selector.logic.send_event('E_SHOW_MODEL')
            if not self.sd.ref_driver_id:
                self.send_event('E_ON_JOIN_MECHA')
                pattern = self.ev_g_pattern()
                self.send_event('E_PATTERN_HANDLE', pattern, force_update=True)
                self.send_event('E_ENABLE_BEHAVIOR', True)
            self.send_event('E_PASSENGER_BINDED_SEAT', passenger_id)
            passenger_model.visible = True
            return