# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComVehicleData.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from copy import deepcopy
from logic.gcommon.common_const import vehicle_const

class ComVehicleData(UnitCom):
    BIND_EVENT = {'G_VEHICLE_ALL_INFO': '_get_all_vehicle_info',
       'G_PASSENGER_INFO': '_get_passenger_info',
       'G_DRIVER': '_get_driver',
       'G_EMPTY_SEAT': '_get_empty_seat',
       'G_VEHICLE_SEATS': '_get_vehicle_seats',
       'G_VEHICLE_SPEED': '_get_speed',
       'G_VEHICEL_HEALTH': '_get_vehicle_health',
       'E_ADD_PASSENGER': '_add_passenger',
       'E_REMOVE_PASSENGER': '_remove_passenger',
       'E_VEHICLE_DATA_CHANGE': '_on_vehicle_data_change',
       'E_ON_CHANGE_VEHICLE_DATA': '_on_vehicle_data_change',
       'G_VEHICEL_STATUS': '_get_status',
       'G_DRIVER_SEAT': '_get_driver_seat',
       'G_VEHICLE_TYPE': '_get_vehicle_type',
       'G_ITEM_ID': '_get_vehicle_type',
       'G_IS_MEMBER_IN_VEHICLE': 'is_passanger_or_driver'
       }

    def __init__(self):
        super(ComVehicleData, self).__init__(need_update=False)
        self.vtype = None
        self.vehicle_conf = None
        self.vehicle_data = {'driver': None,
           'passenger': {},'health': [
                    1000, 1000],
           'speed': [
                   0, 100],
           'status': vehicle_const.MOVE_STOP,
           'simulate_physics': None
           }
        self.last_avatar_drive = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComVehicleData, self).init_from_dict(unit_obj, bdict)
        self.vtype = bdict.get('vtype', None)
        if not self.vtype:
            from common.cfg import confmgr
            mecha_id = bdict.get('mecha_id', '8001')
            mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
            self.vtype = mecha_conf[str(mecha_id)].get('transform_id', None)
        self.get_vehicle_conf()
        for key in self.vehicle_data:
            if key in bdict:
                self.vehicle_data[key] = bdict[key]

        return

    def get_vehicle_conf(self):
        from data import vehicle_data
        if self.vehicle_conf:
            return self.vehicle_conf
        self.vehicle_conf = vehicle_data.data.get(str(self.vtype))
        return self.vehicle_conf

    def _get_vehicle_type(self):
        return self.vtype

    def _get_driver_seat(self):
        return self.vehicle_conf['seats'][0]

    def _on_vehicle_data_change(self, vehicle_info):
        change_type = vehicle_info['change_type']
        data = vehicle_info['data']
        vehicle_info['errcode'] = vehicle_const.CH_SUCCESS
        if change_type == vehicle_const.CH_VEHICLE_HEALTH:
            self.vehicle_data['health'][0] = data
            self.send_event('E_VEHICLE_HEALTH_CHANGED', self.vehicle_data['health'])
        elif change_type == vehicle_const.CH_MOVE_STATUS:
            if self.vehicle_data['status'] == vehicle_const.MOVE_ENGINE_BREAK:
                return
            old_val = self.vehicle_data['status']
            self.vehicle_data['status'] = data
            if data == vehicle_const.MOVE_STOP:
                self.vehicle_data['speed'][0] = 0
                self.send_event('E_SPEED_CHANGED', self.vehicle_data['speed'])
            if old_val != data:
                self.send_event('E_MOVE_STATUS_CHANGED', data)
        elif change_type == vehicle_const.CH_VEHICLE_SPEED:
            old_val = self.vehicle_data['speed'][0]
            self.vehicle_data['speed'][0] = data
            if old_val != data:
                self.send_event('E_SPEED_CHANGED', self.vehicle_data['speed'])
        elif change_type == vehicle_const.CH_SEAT_INFO:
            passenger = data.copy()
            old_passengers = self.vehicle_data['passenger']
            old_driver = self.vehicle_data['driver']
            if 'driver_info' in passenger:
                driver_info = passenger.pop('driver_info')
                new_driver = driver_info['new_driver']
                driver_info['old_driver'] = old_driver
            else:
                driver_info = {'old_driver': old_driver,
                   'new_driver': old_driver
                   }
                new_driver = old_driver
            self.send_event('E_CHANGE_LAST_DRIVER_STATUS', old_driver, new_driver, passenger)
            self.vehicle_data['driver'] = new_driver
            self.vehicle_data['passenger'] = passenger
            self.send_event('E_SWITCH_VEHICLE_SEAT', passenger, old_passengers, driver_info)
            if len(passenger) == 1 and len(old_passengers) == 0:
                self.send_event('E_VEHICLE_START_SOUND', None)
            elif len(passenger) == 0:
                self.send_event('E_VEHICLE_NO_PASSENGER', None)
        return True

    def is_passanger_or_driver(self, uid):
        if self.vehicle_data:
            driver = self.vehicle_data.get('driver', None)
            if driver == uid:
                return True
            passenger = self.vehicle_data.get('passenger', None)
            if passenger:
                if uid in passenger:
                    return True
        return False

    def _get_speed(self):
        return self.vehicle_data['speed']

    def _get_status(self):
        return self.vehicle_data['status']

    def _add_passenger(self, eid, seat_name):
        self.vehicle_data['passenger'][eid] = seat_name
        if self._get_driver_seat() == seat_name:
            self.vehicle_data['driver'] = eid
            self.vehicle_data['simulate_physics'] = eid
            self.send_event('E_VEHICLE_TRY_TRANS_PHYS', eid)

    def _remove_passenger(self, eid):
        passengers = self.vehicle_data['passenger']
        if eid in passengers:
            del passengers[eid]
        if self.vehicle_data['driver'] == eid:
            self.vehicle_data['driver'] = None
        return

    def _get_all_vehicle_info(self):
        return self.vehicle_data

    def _get_passenger_info(self):
        return self.vehicle_data['passenger']

    def _get_driver(self):
        return self.vehicle_data['driver']

    def _get_vehicle_health(self):
        return self.vehicle_data['health']

    def _get_vehicle_seats(self):
        vconf = self.vehicle_conf
        seats = vconf['seats'][:]
        return seats

    def _get_empty_seat(self, seat_type):
        vconf = self.vehicle_conf
        seats = vconf['seats'][:]
        driver_seat = seats[0]
        if seat_type == vehicle_const.SEAT_TYPE_DRIVER:
            if self.vehicle_data['driver']:
                return (None, False)
        elif seat_type == vehicle_const.SEAT_TYPE_PASSENGER:
            seats.remove(driver_seat)
        passengers = self.vehicle_data['passenger']
        for seat_name in six.itervalues(passengers):
            if seat_name in seats:
                seats.remove(seat_name)

        if seats:
            sname = seats[0]
            return (
             sname, sname == driver_seat)
        else:
            return (
             None, False)

    def get_client_dict(self):
        return deepcopy(self.vehicle_data)