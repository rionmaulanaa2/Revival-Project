# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSeatController.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from ..share.ComSeats import ComSeats
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const
from mobile.common.EntityManager import EntityManager
from functools import partial

class ComSeatController(UnitCom):
    BIND_EVENT = {'G_ON_SEAT_LOAD': 'on_seat_load',
       'G_ON_SEAT_DESTROY': 'on_seat_destroy',
       'G_SEAT_LOGIC': 'get_seat_logic',
       'G_SEAT_LOGIC_BY_ID': 'get_seat_logic_by_id',
       'G_SEAT_OBJ_BY_ID': 'get_seat_obj_by_id',
       'E_DUMP_STATE': 'dump_state',
       'E_ADD_PASSENGER': ('_add_passenger', 99),
       'E_REMOVE_PASSENGER': ('remove_passenger', 99),
       'E_CHANGE_PASSENGER': ('change_passenger', 99),
       'E_SET_MOVE_CONTROLLER': 'set_move_controller',
       'E_ON_BEING_OBSERVE': 'on_being_observed'
       }
    FORWARD_EVENT = ('E_ANIMATOR_LOADED', 'E_MODEL_LOADED', 'E_TRANS_SEAT_YAW')

    def __init__(self):
        super(ComSeatController, self).__init__()
        self._seat_map = {}
        self._seat_logic = {}
        self._move_controller = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSeatController, self).init_from_dict(unit_obj, bdict)
        self._seat_map = bdict.get('seat_map', {})
        self._move_controller = bdict.get('move_controller', None)
        self.register_forward_event()
        return

    def on_init_complete(self):
        for seat_name in self._seat_map:
            self.on_seat_load(seat_name)

        self.set_move_controller(self._move_controller)

    def destroy(self):
        self.sd.ref_avatar_seat_logic = None
        for seat_logic in six.itervalues(self._seat_logic):
            seat_logic.ev_g_on_vehicle_destroy()

        self._seat_logic = {}
        super(ComSeatController, self).destroy()
        return

    def register_forward_event(self):
        register = self.regist_event
        for event in self.FORWARD_EVENT:
            func = partial(self.forward_event, event)
            register(event, func)

    def forward_event(self, event_name, *args, **kwargs):
        for seat_logic in six.itervalues(self._seat_logic):
            seat_logic.send_event(event_name, *args, **kwargs)

    def on_seat_load(self, seat_name, seat_logic=None):
        if not seat_logic:
            seat = EntityManager.getentity(self._seat_map.get(seat_name, 0))
            if not seat or not seat.logic:
                return
            seat_logic = seat.logic
            seat_logic.ev_g_on_vehicle_load(self.unit_obj)
        self._seat_logic[seat_name] = seat_logic
        self.check_avatar_seat()
        if self.ev_g_animator():
            seat_logic.send_event('E_ANIMATOR_LOADED')
        is_empty = self.ev_g_is_empty_seat(seat_name)
        if is_empty:
            seat_logic.send_event('E_DISABLE_BEHAVIOR')
        else:
            seat_logic.send_event('E_ENABLE_BEHAVIOR', True)

    def on_seat_destroy(self, seat_name):
        self._seat_logic.pop(seat_name, None)
        self.check_avatar_seat()
        return

    def _add_passenger(self, eid, seat_name):
        seat_logic = self._seat_logic.get(seat_name, None)
        if not seat_logic:
            return
        else:
            seat_logic.send_event('E_ENABLE_BEHAVIOR', True)
            self.check_avatar_seat()
            return

    def remove_passenger(self, passenger_id):
        self.change_passenger(passenger_id)

    def change_passenger(self, passenger_id, *args):
        for seat_name, seat_logic in six_ex.items(self._seat_logic):
            is_empty = self.ev_g_is_empty_seat(seat_name)
            if is_empty:
                if seat_logic.ev_g_is_enable_behavior():
                    seat_logic.send_event('E_DISABLE_BEHAVIOR')
            elif not seat_logic.ev_g_is_enable_behavior():
                seat_logic.send_event('E_ENABLE_BEHAVIOR', True)

        self.check_avatar_seat()
        if global_data.player and passenger_id == global_data.player.id:
            global_data.emgr.player_change_seat_event.emit()

    def set_move_controller(self, owner_id):
        self._move_controller = owner_id
        if owner_id:
            if owner_id == global_data.player.id:
                add_coms = ('ComMoveSyncSender2', )
                del_coms = ('ComMoveSyncReceiver2', )
            else:
                add_coms = ('ComMoveSyncReceiver2', )
                del_coms = ('ComMoveSyncSender2', )
        else:
            add_coms = ()
            del_coms = ('ComMoveSyncSender2', 'ComMoveSyncReceiver2')
        for del_com in del_coms:
            self.unit_obj.del_com(del_com)

        for add_com in add_coms:
            if not self.unit_obj.get_com(add_com):
                com = self.unit_obj.add_com(add_com, 'client')
                com.init_from_dict(self.unit_obj, {})
                com.on_init_complete()
                com.on_post_init_complete({})

    def check_avatar_seat(self):
        avatar_seat_logic = self.get_seat_logic_by_id(global_data.player.id)
        if avatar_seat_logic:
            self.sd.ref_avatar_seat_logic = avatar_seat_logic
            self.sd.ref_avatar_seat_idx = self.ev_g_passenger_seat_index(global_data.player.id)
        else:
            self.sd.ref_avatar_seat_logic = None
            self.sd.ref_avatar_seat_idx = None
        return

    def get_seat_logic(self, seat_name):
        return self._seat_logic.get(seat_name, None)

    def get_seat_logic_by_id(self, player_id):
        seat_name = self.ev_g_passenger_seat(player_id) or 0
        return self._seat_logic.get(seat_name, None)

    def get_seat_obj_by_id(self, player_id):
        seat_name = self.ev_g_passenger_seat(player_id) or 0
        seat_eid = self._seat_map.get(seat_name)
        if not seat_eid:
            return None
        else:
            seat_obj = EntityManager.getentity(seat_eid)
            return seat_obj

    def dump_state(self):
        for seat_name, seat_logic in six_ex.items(self._seat_logic):
            if not seat_logic.ev_g_is_enable_behavior():
                continue
            print(('test--ComSeatController.dump_state--seat_name =', seat_name, '--ev_g_is_enable_behavior =', self.ev_g_is_enable_behavior(), '--seat_logic =', seat_logic))
            seat_logic.send_event('E_DUMP_STATE')
            seat_logic.send_event('E_DUMP_DEBUG_INFO')

    def on_being_observed(self, is_observed):
        if global_data.cam_lplayer:
            seat_logic = self.get_seat_logic_by_id(global_data.cam_lplayer.id)
            if seat_logic:
                seat_logic.send_event('E_ON_BEING_OBSERVE', is_observed)