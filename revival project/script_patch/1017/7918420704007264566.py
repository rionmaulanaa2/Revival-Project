# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSeatClient.py
from __future__ import absolute_import
import six_ex
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager

class ComSeatClient(UnitCom):
    BIND_EVENT = {'G_ON_VEHICLE_LOAD': 'on_vehicle_load',
       'G_ON_VEHICLE_DESTROY': 'on_vehicle_destroy',
       'E_SET_SEAT_CONTROLLER': 'set_controller',
       'G_OWNER': 'get_owner',
       'G_CAMERA_PROXY': 'get_owner',
       'G_IS_MECHA': 'is_mecha',
       'G_NAME': 'get_name',
       'G_SEAT_INDEX': 'get_seat_index',
       'E_ON_BEING_OBSERVE': 'on_being_observed',
       'E_ON_PASSENGER_BINDED_SEAT': 'on_passenger_binded_seat'
       }

    def __init__(self):
        super(ComSeatClient, self).__init__()
        self.seat_name = ''
        self.vehicle_id = None
        self.sd.ref_vehicle_logic = None
        self.sd.ref_driver_id = None
        self._is_sender = None
        self.sd.ref_is_mecha = True
        self._has_registered_event = False
        self.last_cam_target_pos = None
        self.move_timer = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSeatClient, self).init_from_dict(unit_obj, bdict)
        self.seat_name = bdict.get('seat_name', '')
        self.seat_index = 0
        if 'renwu_01' == self.seat_name:
            self.seat_index = 0
        elif 'renwu_02' == self.seat_name:
            self.seat_index = 1
        else:
            self.seat_index = 2
        self.vehicle_id = bdict.get('vehicle_eid', None)
        self.sd.ref_driver_id = bdict.get('player_id', None)
        self.sd.ref_mecha_id = bdict.get('mecha_id', '0')
        return

    def on_init_complete(self):
        self.forward_event()
        self.on_vehicle_load()
        self.set_controller(self.sd.ref_driver_id)

    def destroy(self):
        if self.sd.ref_vehicle_logic:
            self.sd.ref_vehicle_logic.ev_g_on_seat_destroy(self.seat_name)
            self.on_vehicle_destroy()
        if self.ev_g_is_cam_target():
            global_data.emgr.enable_special_target_pos_logic.emit(False)
        self.stop_camera_pos_tick()
        self.last_cam_target_pos = None
        super(ComSeatClient, self).destroy()
        return

    def get_name(self):
        return self.seat_name

    def get_seat_index(self):
        return self.seat_index

    def on_vehicle_load(self, vehicle_logic=None):
        if not vehicle_logic:
            vehicle = EntityManager.getentity(self.vehicle_id)
            if not vehicle or not vehicle.logic:
                return
            vehicle_logic = vehicle.logic
            vehicle_logic.ev_g_on_seat_load(self.seat_name, self.unit_obj)
        self.sd.ref_vehicle_logic = vehicle_logic
        self.ev_g_set_forward_entity(self.vehicle_id)
        self.check_camera_setup(self.sd.ref_driver_id)

    def on_vehicle_destroy(self):
        self.sd.ref_vehicle_logic = None
        self.ev_g_set_forward_entity(None)
        return

    def is_mecha(self):
        return True

    def get_owner(self):
        return self.sd.ref_vehicle_logic

    def forward_event(self):
        from logic.gcommon.component.client.ComMotorcycleAppearance import ComMotorcycleAppearance
        events = six_ex.keys(ComMotorcycleAppearance.BIND_EVENT)
        events.append('G_POSITION')
        events.append('G_TRANS_YAW')
        events.append('G_CAMP_ID')
        self.ev_g_register_forward_events(events)

    def set_controller(self, player_id):
        if global_data.cam_lplayer:
            if self.sd.ref_driver_id == global_data.cam_lplayer.id:
                self.check_camera_setup(player_id)
        self.sd.ref_driver_id = player_id
        is_sender = player_id == global_data.player.id
        if is_sender == self._is_sender:
            return
        self._is_sender = is_sender
        self.unit_obj.del_com('ComOrientationSyncSender')
        self.unit_obj.del_com('ComOrientationSyncReceiver')
        data = {'seat_name': self.seat_name
           }
        com_name = 'ComOrientationSyncSender' if is_sender else 'ComOrientationSyncReceiver'
        com = self.unit_obj.add_com(com_name, 'client')
        com.init_from_dict(self.unit_obj, data)
        self.send_event('E_CHANGE_SEAT_OWNER', player_id)

    def on_passenger_binded_seat(self, player_id):
        self.check_camera_setup(player_id)
        global_data.game_mgr.delay_exec(0.1, self.update_check, player_id)

    def update_check(self, player_id):
        if self and self.is_valid():
            if self.sd.ref_driver_id == player_id and self._has_registered_event:
                self.camera_pos_tick()

    def start_camera_pos_tick(self):
        if self._has_registered_event:
            return
        self.stop_camera_pos_tick()
        import world
        if self.sd.ref_vehicle_logic:
            if G_POS_CHANGE_MGR:
                self.sd.ref_vehicle_logic.regist_pos_change(self._on_position)
            else:
                self.sd.ref_vehicle_logic.regist_event('E_POSITION', self._on_position)
            self._has_registered_event = True

    def stop_camera_pos_tick(self):
        if self.sd.ref_vehicle_logic:
            if self._has_registered_event:
                if G_POS_CHANGE_MGR:
                    self.sd.ref_vehicle_logic.unregist_pos_change(self._on_position)
                else:
                    self.sd.ref_vehicle_logic.unregist_event('E_POSITION', self._on_position)
                self._has_registered_event = False

    def _on_position(self, pos):
        self.camera_pos_tick()

    def camera_pos_tick(self):
        if not global_data.cam_lplayer:
            return
        model = global_data.cam_lplayer.ev_g_model()
        if model:
            pos = model.world_position
            if self.last_cam_target_pos != pos:
                global_data.emgr.set_target_pos_for_special_logic.emit(pos)
                self.last_cam_target_pos = pos

    def check_camera_setup(self, player_id):
        if global_data.cam_lplayer:
            if player_id == global_data.cam_lplayer.id:
                global_data.emgr.enable_special_target_pos_logic.emit(True)
                self.start_camera_pos_tick()
                self.camera_pos_tick()
            elif self.sd.ref_driver_id == global_data.cam_lplayer.id:
                global_data.emgr.enable_special_target_pos_logic.emit(False)
                self.stop_camera_pos_tick()

    def on_being_observed(self, is_on_observe):
        if is_on_observe:
            self.check_camera_setup(self.sd.ref_driver_id)
        else:
            self.last_cam_target_pos = None
            global_data.emgr.enable_special_target_pos_logic.emit(False)
            self.stop_camera_pos_tick()
        return