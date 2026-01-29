# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCtrlVehicle.py
from __future__ import absolute_import
import weakref
import math3d
from logic.gcommon.common_const import vehicle_const
from logic.gcommon.common_const import water_const
from mobile.common.EntityManager import EntityManager
from ..UnitCom import UnitCom
from ...cdata import status_config

class ComCtrlVehicle(UnitCom):
    BIND_EVENT = {'E_VEHICLE_LAUNCH': '_launch_vehicle',
       'E_TRY_JOIN_VEHICLE': '_try_join_vehicle',
       'E_TRY_LEAVE_VEHICLE': '_try_leave_vehicle',
       'E_TRY_CHANGE_VEHICLE_DATA': '_try_change_vehicle_data',
       'E_TRY_CHANGE_SEAT': '_try_change_seat',
       'E_ON_JOIN_VEHICLE': '_on_join_vehicle',
       'E_ON_LEAVE_VEHICLE': '_on_leave_vehicle',
       'E_ON_CHANGE_SEAT': '_on_change_seat',
       'E_ON_CHANGE_VEHICLE_DATA': '_on_change_vehicle_data',
       'E_UPDATE_VEHICLE_CAMERA': '_update_vehicle_camera',
       'G_IS_DRIVER': 'get_is_driver',
       'G_IS_IN_VEHICLE': 'get_is_in_vehicle',
       'G_GET_CUR_VEHICLE': 'get_cur_vehicle',
       'E_CHANGE_LAST_DRIVER': '_on_change_last_driver',
       'G_LAST_VEHICLE_ID': 'get_last_vehicle_id'
       }

    def __init__(self):
        super(ComCtrlVehicle, self).__init__()
        self._is_boat = False
        self.vehicle = None
        self.last_vehicle_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComCtrlVehicle, self).init_from_dict(unit_obj, bdict)
        global_data.emgr.drive_ui_ope_change_event += self.on_switch_car_ope

    def get_last_vehicle_id(self):
        return self.last_vehicle_id

    def destroy(self):
        super(ComCtrlVehicle, self).destroy()
        global_data.emgr.drive_ui_ope_change_event -= self.on_switch_car_ope
        if self.last_vehicle_id:
            entity = EntityManager.getentity(self.last_vehicle_id)
            if entity and entity.logic:
                entity.logic.send_event('E_CHANGE_LAST_VEHICLE')
                self.last_vehicle_id = None
        return

    def _try_change_seat(self, target_seat_index):
        control_target = self.ev_g_control_target()
        vconf = control_target.logic.ev_g_vehicle_conf()
        seats = vconf['seatpoints']
        seat_name = seats[target_seat_index]
        pid = self.unit_obj.id
        if seat_name:
            self._try_change_vehicle_data(control_target.id, vehicle_const.CH_SEAT_INFO, {pid: seat_name})

    def _on_change_seat(self, vehicle_id, seat_name):
        pass

    def _on_leave_vehicle(self, vehicle_info):
        leave_id = vehicle_info['leave_id']
        vid = vehicle_info.get('vid', None)
        if not vid:
            return
        else:
            if leave_id != self.unit_obj.id:
                return
            self.send_event('E_ON_ACTION_LEAVE_VEHICLE')
            self.ev_g_cancel_state(status_config.ST_MECHA_DRIVER)
            self.ev_g_cancel_state(status_config.ST_MECHA_PASSENGER)
            self.send_event('E_ON_STATUS_CHANGED')
            vehicle = EntityManager.getentity(vehicle_info['vid'])
            if not (vehicle and vehicle.logic):
                return
            off_position = vehicle_info.get('off_position', None)
            if off_position:
                _pos = math3d.vector(*off_position)
            else:
                has_block, off_pos = vehicle.logic.ev_g_check_off_pos(self.unit_obj.id)
                _pos = off_pos
            old_driver = vehicle.logic.sd.ref_driver_id
            if self.unit_obj.id == old_driver:
                vehicle.logic.send_event('E_MOVE_NO_FORCE')
                vehicle.logic.send_event('E_STOP_CONTROL_VEHICLE')
            target = EntityManager.getentity(vid)
            ownid = vehicle_info['driver']
            passenger = vehicle_info['passenger']
            target.logic.send_event('E_SET_PASSENGER', passenger)
            passenger['driver_info'] = {'new_driver': ownid}
            data = {'data': passenger,
               'change_type': vehicle_const.CH_SEAT_INFO
               }
            target.logic.send_event('E_VEHICLE_DATA_CHANGE', data)
            self.send_event('E_SET_CONTROL_TARGET', None, {})
            target.logic.send_event('E_LEAVE_VEHICLE', self.unit_obj)
            self.send_event('E_TO_THIRD_PERSON_CAMERA')
            com_camera = self.scene.get_com('PartCamera')
            self.send_event('E_ACTION_SET_YAW', com_camera.get_yaw())
            if not self.ev_g_get_state(status_config.ST_SWIM):
                self.send_event('E_FOOT_POSITION', _pos, True)
            if not target.logic.ev_g_simulate_physics():
                target.logic.send_event('E_VEHICLE_COLLISION_SET', False)
            self._is_boat = False
            self.vehicle = None
            return

    def _on_change_last_driver(self):
        self.last_vehicle_id = None
        return

    def _on_join_vehicle(self, vehicle_id, driver, passenger):
        target = EntityManager.getentity(vehicle_id)
        eid = self.unit_obj.id
        if global_data.player and global_data.player.id == self.unit_obj.id:
            if self.last_vehicle_id:
                entity = EntityManager.getentity(self.last_vehicle_id)
                if entity and entity.logic:
                    entity.logic.send_event('E_CHANGE_LAST_VEHICLE')
            self.last_vehicle_id = vehicle_id
        if eid == driver:
            self.ev_g_status_try_trans(status_config.ST_MECHA_DRIVER)
            is_driver = True
        else:
            self.ev_g_status_try_trans(status_config.ST_MECHA_PASSENGER)
            is_driver = False
        self.send_event('E_ON_ACTION_ON_VEHICLE')
        self.send_event('E_ON_STATUS_CHANGED')
        if not target:
            return
        target.logic.send_event('E_SET_PASSENGER', passenger)
        self._is_boat = target.logic.ev_g_is_water_vehicle()
        self.vehicle = weakref.ref(target.logic)
        if driver:
            passenger['driver_info'] = {'new_driver': driver}
        data = {'data': passenger,'change_type': vehicle_const.CH_SEAT_INFO
           }
        target.logic.send_event('E_VEHICLE_DATA_CHANGE', data)
        myid = global_data.player.id
        seat_name = passenger.get(eid)
        if True or eid == driver:
            self.send_event('E_SET_EMPTY_HAND')
        self.send_event('E_SET_CONTROL_TARGET', target, {'seat_name': seat_name,'driver': driver})
        target.logic.send_event('E_ENTER_VEHICLE', self.unit_obj)
        if target and eid == myid:
            target.logic.send_event('E_VEHICLE_COLLISION_SET', True)
        if eid == myid:
            if is_driver:
                target.logic.send_event('E_START_CONTROL_VEHICLE')

    def _update_vehicle_camera(self, lvehicle):
        from logic.units.LAirship import LAirship
        if isinstance(lvehicle, LAirship):
            pass
        else:
            is_driver = self.get_is_driver()
            if is_driver:
                self.send_event('E_TO_VEHICLE_CAMERA', lvehicle=lvehicle)
            else:
                self.send_event('E_TO_PASSENGER_VEHICLE_CAMERA', lvehicle=lvehicle)

    def _launch_vehicle(self, vehicle_id, leave_point=None):
        entity = EntityManager.getentity(vehicle_id)
        if entity and entity.logic:
            entity.logic.send_event('E_CALL_SYNC_METHOD', 'vehicle_launch', (leave_point,), True)

    def _try_join_vehicle(self, status, vehicle_id, seat_type):
        if self.ev_g_status_check_pass(status):
            entity = EntityManager.getentity(vehicle_id)
            if entity and entity.logic:
                self.send_event('E_LEAVE_ATTACHABLE_ENTITY')
                self.send_event('E_CALL_SYNC_METHOD', 'try_join_vehicle', (vehicle_id, seat_type), True)

    def _try_leave_vehicle(self):
        ctrl_target = self.ev_g_control_target()
        has_block, off_pos = ctrl_target.logic.ev_g_check_off_pos(self.unit_obj.id)
        if not has_block:
            off_point = (
             off_pos.x, off_pos.y, off_pos.z)
            self.send_event('E_CALL_SYNC_METHOD', 'try_leave_vehicle', (off_point,), True)
        else:
            self.send_event('E_SHOW_MESSAGE', get_text_local_content(18016))

    def _try_change_vehicle_data(self, vid, dtype, data):
        info = {'vid': vid,
           'change_type': dtype,
           'data': data
           }
        self.send_event('E_CALL_SYNC_METHOD', 'change_vehicle_data', (info,), True)

    def _on_change_vehicle_data(self, vehicle_info):
        vid = vehicle_info['vid']
        vnpc = EntityManager.getentity(vid)
        if vnpc:
            vnpc.logic.send_event('E_VEHICLE_DATA_CHANGE', vehicle_info)

    def on_switch_car_ope(self, new_ope):
        vehicle_npc = self.ev_g_control_target()
        if vehicle_npc and vehicle_npc.__class__.__name__ == 'MechaTrans':
            self._update_vehicle_camera(vehicle_npc.logic)

    def get_is_driver(self):
        vehicle_npc = self.ev_g_control_target()
        if not vehicle_npc or not vehicle_npc.logic:
            return
        if vehicle_npc.__class__.__name__ == 'MechaTrans' or vehicle_npc.__class__.__name__ == 'Motorcycle':
            return self.unit_obj.id == vehicle_npc.logic.sd.ref_driver_id

    def get_is_in_vehicle(self):
        vehicle_npc = self.ev_g_control_target()
        if not vehicle_npc or not vehicle_npc.logic:
            return False
        if vehicle_npc.__class__.__name__ == 'MechaTrans' or vehicle_npc.__class__.__name__ == 'Motorcycle':
            return True

    def get_cur_vehicle(self):
        vehicle_npc = self.ev_g_control_target()
        if vehicle_npc and vehicle_npc.__class__.__name__ == 'MechaTrans':
            return vehicle_npc.id

    def _on_handle_water_event(self, change_status, water_height):
        if self.get_is_driver() and not self._is_boat:
            vehicle = self.vehicle()
            if vehicle:
                if change_status in [water_const.WATER_NONE]:
                    vehicle.send_event('E_VEHICLE_IN_LAND', water_height)
                elif change_status in [water_const.WATER_MID_LEVEL, water_const.WATER_SHALLOW_LEVEL, water_const.WATER_SHWLLOW_LEVEL2]:
                    vehicle.send_event('E_VEHICLE_IN_MID_WATER', water_height)
                elif change_status == water_const.WATER_DEEP_LEVEL:
                    vehicle.send_event('E_VEHICLE_IN_DEEP_WATER', water_height)