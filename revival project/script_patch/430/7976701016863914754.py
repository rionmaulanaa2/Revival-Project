# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComSeats.py
from __future__ import absolute_import
import six
import six_ex
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const

class ComSeats(UnitCom):
    BIND_EVENT = {'G_PASSENGER': '_get_passenger_ids',
       'G_PASSENGER_INFO': '_get_passenger_dict',
       'G_PASSENGER_SEAT': '_get_passenger_seat',
       'G_DRIVER': '_get_driver',
       'G_EMPTY_SEAT': '_get_empty_seat',
       'G_DRIVER_SEAT': '_get_driver_seat',
       'G_IS_MEMBER_IN_VEHICLE': '_is_passanger',
       'G_IS_EMPTY_SEAT': '_is_empty_seat',
       'G_IS_FULL_SEAT': '_is_full_seat',
       'E_CHANGE_PASSENGER_SEAT': 'change_passenger',
       'E_ADD_PASSENGER': '_add_passenger',
       'E_REMOVE_PASSENGER': '_remove_passenger',
       'E_SET_PASSENGER': '_set_passenger',
       'G_PASSENGER_SEAT_INDEX': '_get_passenger_seat_index',
       'G_ALL_EMPTY_SEAT': 'get_all_empty_seat',
       'G_SEAT_NAME_BY_INDEX': 'get_seat_name_by_index',
       'G_SEAT_INDEX_BY_SEAT_NAME': 'get_seat_index_by_seat_name'
       }

    def __init__(self):
        super(ComSeats, self).__init__()
        self._seats = ()
        self.sd.ref_driver_id = 0
        self._passenger_dict = {}
        self._seat_dict = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComSeats, self).init_from_dict(unit_obj, bdict)
        self._seats = bdict.get('seats', [])
        self.sd.ref_seats = self._seats
        self.sd.ref_driver_id = bdict.get('driver_id', None)
        self._set_passenger(bdict.get('passenger_dict', {}))
        return

    def get_client_dict(self):
        passenger_dict = {}
        passenger_dict.update(self._passenger_dict)
        return {'seats': self._seats,
           'driver_id': self.sd.ref_driver_id,
           'passenger_dict': passenger_dict
           }

    def _get_driver_seat(self):
        if self._seats:
            return self._seats[0]
        else:
            return None

    def _is_passanger(self, eid):
        return eid in self._passenger_dict

    def _is_empty_seat(self, seat_name):
        return seat_name in self._seats and seat_name not in self._seat_dict

    def _is_full_seat(self):
        return len(self._seat_dict) >= len(self._seats)

    def _get_empty_seat(self, seat_type):
        seats = [ seat_name for seat_name in self._seats if seat_name not in self._seat_dict ]
        driver_seat = self._get_driver_seat()
        if seat_type == vehicle_const.SEAT_TYPE_DRIVER:
            if self.sd.ref_driver_id:
                return (None, False)
        elif seat_type == vehicle_const.SEAT_TYPE_PASSENGER:
            if driver_seat in seats:
                seats.remove(driver_seat)
        if seats:
            sname = seats[0]
            return (
             sname, seat_type == vehicle_const.SEAT_TYPE_DRIVER and sname == driver_seat or True)
        else:
            return (
             None, False)

    def _get_passenger_ids(self):
        return six_ex.keys(self._passenger_dict)

    def _get_passenger_dict(self):
        return self._passenger_dict

    def _get_driver(self):
        return self.sd.ref_driver_id

    def _get_passenger_seat_index(self, eid):
        seat_name = self._get_passenger_seat(eid)
        for index, one_seat_name in enumerate(self._seats):
            if one_seat_name == seat_name:
                return index

        return -1

    def get_all_empty_seat(self):
        all_empty_seat = []
        for index, one_seat_name in enumerate(self._seats):
            if one_seat_name not in self._seat_dict:
                all_empty_seat.append(index)

        return all_empty_seat

    def get_seat_name_by_index(self, index):
        if index < 0 or index >= len(self._seats):
            log_error('test--get_seat_name_by_index--index =%s--len(_seats) =%s' % (index, len(self._seats)))
            import traceback
            traceback.print_stack()
            return
        return self._seats[index]

    def get_seat_index_by_seat_name(self, seat_name):
        for index, one_seat_name in enumerate(self._seats):
            if one_seat_name == seat_name:
                return index

        return -1

    def _get_passenger_seat(self, eid):
        return self._passenger_dict.get(eid)

    def change_passenger(self, eid, seat_name):
        if eid in self._passenger_dict:
            self._remove_passenger(eid)
        self._add_passenger(eid, seat_name)

    def _add_passenger(self, eid, seat_name):
        if seat_name in self._seat_dict:
            return
        self._seat_dict[seat_name] = eid
        self._passenger_dict[eid] = seat_name
        if seat_name == self._get_driver_seat():
            self.sd.ref_driver_id = eid
            self.send_event('E_ON_DRIVER_CHANGE', eid)

    def _remove_passenger(self, eid):
        seat_name = self._passenger_dict.get(eid, None)
        if not seat_name:
            return
        else:
            del self._passenger_dict[eid]
            del self._seat_dict[seat_name]
            if self.sd.ref_driver_id == eid:
                self.sd.ref_driver_id = None
                self.send_event('E_ON_DRIVER_CHANGE', None)
            return

    def _set_passenger(self, passenger_dict):
        self.sd.ref_driver_id = None
        self._passenger_dict = {}
        self._seat_dict = {}
        for eid, seat_name in six.iteritems(passenger_dict):
            self._add_passenger(eid, seat_name)

        return