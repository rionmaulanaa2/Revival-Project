# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic4108.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.cdata.mecha_status_config import *
from .BoostLogic import OxRushNew
from .MoveLogic import Walk, Run, Stand
from .StateBase import StateBase, clamp
from logic.gutils import character_ctrl_utils
from common.utils import timer
from copy import deepcopy
import math3d
import world
import math
import collision
from .ShootLogic import Reload, WeaponFire
from .MoveLogic import Turn
from .JumpLogic import OnGround, Fall
from logic.gcommon.common_const import ui_operation_const
import logic.gcommon.common_utils.bcast_utils as bcast_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import editor
from math import pi
from .StateLogic import Die
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.common_const import collision_const
import logic.gcommon.common_const.animation_const as animation_const
import time
from mobile.common.EntityManager import EntityManager
import logic.gcommon.common_utils.bcast_utils as bcast
pi2 = pi * 2

def common_try_enter(self, player):
    if not player:
        return
    seat_name = self.ev_g_passenger_seat(player.id)
    seat_logic = self.ev_g_seat_logic(seat_name)
    if not seat_logic:
        return
    return seat_logic.ev_g_try_enter(self.sid)


def common_try_exit(self, player):
    if not player:
        return
    seat_name = self.ev_g_passenger_seat(player.id)
    seat_logic = self.ev_g_seat_logic(seat_name)
    if not seat_logic:
        return
    return seat_logic.ev_g_try_exit(self.sid)


class WeaponFire4108(StateBase):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire4108, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()

    def read_data_from_custom_param(self):
        self.slow_down_on_shoot = self.custom_param.get('slow_down_on_shoot', True)
        self.slow_down_speed = self.custom_param.get('slow_down_speed', None)
        return

    def action_btn_down(self, ignore_reload=False):
        return common_try_enter(self, global_data.player)

    def action_btn_up(self):
        return common_try_exit(self, global_data.player)

    def enter(self, leave_states):
        super(WeaponFire4108, self).enter(leave_states)
        self.send_event('E_SLOW_DOWN', self.slow_down_on_shoot, self.slow_down_speed, 'WeaponFire4108')

    def exit(self, enter_states):
        super(WeaponFire4108, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire4108')


class WeaponFire4108Seat(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CHANGE_SEAT_OWNER': 'change_passenger'
       })

    def change_passenger(self, passenger_id):
        if not passenger_id:
            if self.is_active and self.want_to_fire:
                self.action_btn_up()

    def enter(self, leave_states):
        self.fired = True
        super(WeaponFire4108Seat, self).enter(leave_states)
        if self.ev_g_seat_index() == 0:
            if self.sd.ref_vehicle_logic:
                self.sd.ref_vehicle_logic.send_event('E_ACTIVE_STATE', self.sid)
                obj_wp = self.ev_g_wpbar_cur_weapon()
                speed_scale = 1
                if obj_wp:
                    fSpdDebuff = obj_wp.get_effective_value('fSpdDebuff')
                    speed_scale = 1 - fSpdDebuff
                self.sd.ref_vehicle_logic.send_event('E_SET_SPEED_SCALE', speed_scale)

    def exit(self, enter_states):
        super(WeaponFire4108Seat, self).exit(enter_states)
        if self.ev_g_seat_index() == 0:
            if self.sd.ref_vehicle_logic:
                self.sd.ref_vehicle_logic.send_event('E_DISABLE_STATE', self.sid)
                self.sd.ref_vehicle_logic.send_event('E_SET_SPEED_SCALE', 1)

    def check_transitions(self):
        if self.sd.ref_vehicle_logic.sd.ref_avatar_seat_idx != self.ev_g_seat_index():
            self.disable_self()
        return super(WeaponFire4108Seat, self).check_transitions()

    def play_fire_anim(self, fired_socket_index):
        super(WeaponFire4108Seat, self).play_fire_anim(fired_socket_index)
        owner = self.sd.ref_vehicle_logic
        if owner:
            seat_name = self.ev_g_name()
            owner.send_event('E_PLAY_SEAT_FIRE_SFX', seat_name)


class Reload4108(StateBase):
    BIND_EVENT = {'E_START_SEAT_RELOAD': 'start_seat_reload',
       'E_CLICK_RELOAD_UI': 'action_btn_down'
       }

    def action_btn_down(self, ignore_reload=False):
        return common_try_enter(self, global_data.player)

    def start_seat_reload(self, reload_time):
        if global_data.player and self.bind_action_id:
            seat_name = self.ev_g_passenger_seat(global_data.player.id)
            seat_logic = self.ev_g_seat_logic(seat_name)
            self.send_event('E_START_ACTION_CD', self.bind_action_id, reload_time)


class Reload4108Seat(Reload):

    def enter(self, leave_states):
        super(Reload4108Seat, self).enter(leave_states)
        owner = self.sd.ref_vehicle_logic
        if owner:
            owner.send_event('E_START_SEAT_RELOAD', self.reload_time)


class RightAim4108(StateBase):

    def action_btn_down(self, ignore_reload=False):
        return common_try_enter(self, global_data.player)

    def action_btn_up(self):
        return common_try_exit(self, global_data.player)


class RightAim4108Seat(StateBase):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(RightAim4108Seat, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.is_on_aim_when_begin_touch = False
        self.init_parameters()

    def init_parameters(self):
        self.is_on_aim_when_begin_touch = False
        self.init_aim_btn_trigger_way()

    def init_aim_btn_trigger_way(self):
        self._aim_btn_press_trigger = global_data.player.get_setting_2(ui_operation_const.WEAPON_AIM_PRESS_TRIGGER_KEY)

    def action_btn_down(self, ignore_reload=False):
        self.is_on_aim_when_begin_touch = self.ev_g_get_state(self.sid)
        if self.check_can_active():
            if not self.is_on_aim_when_begin_touch:
                self.active_self()
        return True

    def action_btn_up(self):
        super(RightAim4108Seat, self).action_btn_up()
        if not self.is_active or not self.is_on_aim_when_begin_touch:
            return
        self.disable_self()
        return True

    def enter(self, leave_states):
        super(RightAim4108Seat, self).enter(leave_states)


@editor.state_exporter({('rotate_speed', 'param'): {'zh_name': '\xe8\xbd\xac\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6(\xe5\xba\xa6/\xe7\xa7\x92)','min_val': 1,'max_val': 50,'getter': lambda self: math.degrees(self.rotate_speed),
                               'setter': --- This code section failed: ---

 241       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'math'
           6  LOAD_GLOBAL           1  'math'
           9  LOAD_ATTR             2  'radians'
          12  LOAD_FAST             1  'v'
          15  CALL_FUNCTION_1       1 
          18  CALL_FUNCTION_3       3 
          21  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 18
}
   })
class Turn4108(Turn):
    BIND_EVENT = Turn.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MECHA_CAMERA': 'change_camera',
       'E_ON_DRIVER_CHANGE': 'on_driver_change'
       })

    def read_data_from_custom_param1(self):
        self.rotate_speed = self.custom_param.get('rotate_speed', 7)
        self.rotate_speed = math.radians(self.rotate_speed)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Turn4108, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param1()
        self.intrp_forward_timer = None
        self._is_stand = True
        return

    def destroy(self):
        if self.intrp_forward_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.intrp_forward_timer)
            self.intrp_forward_timer = None
        super(Turn4108, self).destroy()
        return

    def change_character_attr(self, name, *args):
        super(Turn4108, self).change_character_attr(name, *args)
        seat_logic = self.ev_g_seat_logic_by_id(global_data.player.id)
        if seat_logic:
            if name == 'animator_info':
                print(('test--Turn4108Seat.animator_info--seat_logic.camera_yaw =', seat_logic.ev_g_yaw(), '--seat_logic.ev_g_trans_yaw =', seat_logic.ev_g_trans_yaw(), '--seat_logic =', seat_logic))

    def on_driver_change(self, *args):
        if not self.sd.ref_driver_id:
            if self.intrp_forward_timer:
                global_data.game_mgr.get_post_logic_timer().unregister(self.intrp_forward_timer)
                self.intrp_forward_timer = None
        return

    def on_set_camera_yaw(self, yaw):
        self.camera_yaw = (yaw + pi) % pi2 - pi
        if not self.intrp_forward_timer:
            self.intrp_forward_timer = global_data.game_mgr.get_post_logic_timer().register(func=self.interpolate_yaw, timedelta=True)

    def change_camera(self, *args):
        self.camera_yaw = (global_data.cam_data.yaw + pi) % pi2 - pi

    def get_model_yaw_mat(self):
        return self.sd.ref_rotatedata.rotation_mat

    def interpolate_yaw(self, dt):
        cur_yaw = (self.sd.ref_logic_trans.yaw_target + pi) % pi2 - pi
        delta_yaw = cur_yaw - self.camera_yaw
        speed = self.rotate_speed * dt
        release = False
        if abs(delta_yaw) <= speed:
            trans_yaw = self.camera_yaw
            release = True
        elif delta_yaw > math.pi or -math.pi < delta_yaw < 0:
            trans_yaw = cur_yaw + speed
        else:
            trans_yaw = cur_yaw - speed
        self.sd.ref_logic_trans.yaw_target = trans_yaw
        self.send_event('E_TRANS_SEAT_YAW', speed)
        if release:
            self.intrp_forward_timer = None
            return timer.RELEASE
        else:
            return


class Turn4108Seat(Turn):
    BIND_EVENT = Turn.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MECHA_CAMERA': 'change_camera',
       'E_SET_SEAT_CONTROLLER': 'on_set_player',
       'E_TRANS_SEAT_YAW': ('on_vehicle_tran_yaw', 99),
       'E_ANIMATOR_LOADED': 'recover_orientation',
       'E_DUMP_DEBUG_INFO': 'dump_debug_info',
       'E_ACTION_YAW': 'on_action_yaw'
       })

    def read_data_from_custom_param1(self):
        self.forward_driver = self.custom_param.get('forward_driver', False)
        self.trans_self = self.custom_param.get('trans_self', False)
        self.forward_vehicle = self.custom_param.get('forward_vehicle', False)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Turn4108Seat, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param1()
        self.camera_yaw = bdict.get('yaw', 0)
        self.camera_pitch = bdict.get('pitch', 0)

    def dump_debug_info(self):
        print(('test--Turn4108Seat.dump_debug_info--camera_yaw =', self.camera_yaw, '--name =', self.ev_g_name(), '--unit_obj =', self.unit_obj))

    def recover_orientation(self, *args):
        if not self.ev_g_animator():
            return
        if self.forward_vehicle and self.sd.ref_vehicle_logic:
            self.sd.ref_vehicle_logic.send_event('E_TRANS_YAW', self.camera_yaw)
        self.on_set_camera_yaw(self.camera_yaw)
        self.on_set_camera_pitch(self.camera_pitch)

    def on_get_camera_yaw(self):
        return self.camera_yaw

    def on_set_camera_yaw(self, yaw):
        dt_yaw = yaw - self.camera_yaw
        self.camera_yaw = yaw
        self.camera_yaw = math.fmod(self.camera_yaw, pi2)
        if not self.sd.ref_driver_id:
            return
        if self.trans_self:
            self.on_turn_barbette()
        elif self.forward_driver:
            self.turn_human(dt_yaw)
        elif self.forward_vehicle:
            self.turn_vehicle()

    def on_action_yaw(self, yaw, *args):
        self.camera_yaw += yaw
        self.camera_yaw = math.fmod(self.camera_yaw, pi2)
        if not self.sd.ref_driver_id:
            return
        if self.forward_driver:
            self.turn_human(yaw)
        elif self.trans_self:
            self.on_turn_barbette()
        elif self.forward_vehicle:
            self.turn_vehicle()

    def cal_twist_angle(self, yaw):
        offset_rad = yaw - self.sd.ref_vehicle_logic.sd.ref_rotatedata.yaw_body or 0
        offset_rad = (offset_rad + pi) % pi2 - pi
        twist_angle = offset_rad * 180 / math.pi
        return twist_angle

    def on_turn_barbette(self):
        offset_angle = self.cal_twist_angle(self.camera_yaw)
        twist_yaw_angle = offset_angle + self.twist_yaw_offset
        self.send_event('E_TWIST_YAW', twist_yaw_angle)

    def turn_human(self, dt_yaw):
        driver = EntityManager.getentity(self.sd.ref_driver_id)
        if driver and driver.logic:
            driver.logic.send_event('E_TURN_ON_SEAT', self.camera_yaw, self.sd.ref_vehicle_logic.sd.ref_rotatedata.yaw_body, dt_yaw)

    def turn_human_pitch(self):
        driver = EntityManager.getentity(self.sd.ref_driver_id)
        if driver and driver.logic:
            driver.logic.send_event('E_CAM_PITCH', self.camera_pitch)

    def turn_vehicle(self):
        vehicle = self.sd.ref_vehicle_logic
        if vehicle:
            vehicle.send_event('E_CAM_YAW', self.camera_yaw)

    def on_action_pitch(self, pitch):
        self.camera_pitch += pitch
        if not self.sd.ref_driver_id:
            return
        if self.forward_driver:
            self.turn_human_pitch()

    def on_set_camera_pitch(self, pitch):
        self.camera_pitch = pitch
        if self.forward_driver:
            self.turn_human_pitch()

    def change_camera(self, *args):
        dt_yaw = global_data.cam_data.yaw - self.camera_yaw
        self.camera_yaw = global_data.cam_data.yaw
        self.camera_yaw = math.fmod(self.camera_yaw, pi2)
        self.camera_pitch = global_data.cam_data.pitch
        if not global_data.player or global_data.player.id == self.sd.ref_driver_id:
            return
        if self.trans_self:
            self.on_turn_barbette()
        elif self.forward_driver:
            self.turn_human(dt_yaw)
        elif self.forward_vehicle:
            self.turn_vehicle()

    def on_set_player(self, player):
        if player:
            return
        self.camera_yaw = self.sd.ref_vehicle_logic.sd.ref_rotatedata.yaw_body or 0
        self.camera_yaw = math.fmod(self.camera_yaw, pi2)
        if self.trans_self:
            self.on_turn_barbette()

    def on_vehicle_tran_yaw(self, dt_yaw, *args):
        if not self.sd.ref_driver_id:
            return
        if self.trans_self:
            self.on_turn_barbette()
        elif self.forward_driver:
            self.turn_human(dt_yaw)


class Stand4108(Stand):

    def enter(self, leave_states):
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
            global_data.player.logic.send_event('E_VEHICLE_STOP')
        super(Stand4108, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')

    def on_exit(self):
        pass


class SeatStand(StateBase):
    pass


def __editor_crash_col_setter(self, value):
    self.hit_range = value
    self.create_hit_collision()


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('dash_duration', 'param'): {'zh_name': '\xe4\xbf\x9d\xe6\x8c\x81\xe5\x96\xb7\xe5\xb0\x84\xe7\x8a\xb6\xe6\x80\x81\xe6\x97\xb6\xe9\x95\xbf','min_val': 0,'max_val': 100},('forward_walk_speed', 'meter'): {'zh_name': '\xe5\x89\x8d\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100},('back_walk_speed', 'meter'): {'zh_name': '\xe5\xb7\xa6\xe5\x8f\xb3\xe5\x90\x8e\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100},('move_acc', 'meter'): {'zh_name': '\xe5\x90\xaf\xe5\x8a\xa8\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100},('brake_acc', 'meter'): {'zh_name': '\xe5\x89\x8d\xe5\x90\x8e\xe9\x80\x9f\xe5\xba\xa6\xe5\x8f\x98\xe5\x8c\x96\xe7\x9a\x84\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','min_val': 1,'max_val': 100},('rotate_speed', 'param'): {'zh_name': '\xe8\xbd\xac\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6(\xe5\xba\xa6/\xe7\xa7\x92)','min_val': 1,'max_val': 50,'getter': lambda self: math.degrees(self.rotate_speed),
                               'setter': --- This code section failed: ---

 486       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'math'
           6  LOAD_GLOBAL           1  'math'
           9  LOAD_ATTR             2  'radians'
          12  LOAD_FAST             1  'v'
          15  CALL_FUNCTION_1       1 
          18  CALL_FUNCTION_3       3 
          21  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 18
},
   ('min_hit_speed', 'meter'): {'zh_name': '\xe5\xa4\x9a\xe4\xba\xba\xe8\xbd\xbd\xe5\x85\xb7\xe9\x80\xa0\xe6\x88\x90\xe6\x92\x9e\xe5\x87\xbb\xe4\xbc\xa4\xe5\xae\xb3\xe7\x9a\x84\xe6\x9c\x80\xe5\xb0\x8f\xe9\x80\x9f\xe5\xba\xa6','min_val': 1,'max_val': 200},('hit_interval', 'param'): {'zh_name': '\xe8\x87\xb3\xe5\xb0\x91\xe9\x97\xb4\xe9\x9a\x94\xe5\x87\xa0\xe7\xa7\x92\xe5\x86\x8d\xe6\xac\xa1\xe9\x80\xa0\xe6\x88\x90\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbc\xa4\xe5\xae\xb3','min_val': 0,'max_val': 100},('hit_range', 'param'): {'zh_name': '\xe6\x92\x9e\xe5\x87\xbb\xe7\xa2\xb0\xe6\x92\x9e\xe7\x9b\x92\xe5\xb0\xba\xe5\xaf\xb8','param_type': 'list','structure': [{'zh_name': '\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe9\x95\xbf\xe5\xba\xa6','type': 'float'}],'setter': lambda self, value: __editor_crash_col_setter(self, value)
                            }
   })
class DashMotorcycle(StateBase):
    BIND_EVENT = {'E_TRY_VEHICLE_DASH': 'try_vehicle_dash',
       'E_BEGIN_OR_END_VEHICLE_DASH': 'begin_or_end_dash',
       'E_ON_DRIVER_CHANGE': 'change_driver',
       'G_DASH_BRAKE_ACC': 'get_dash_brake_acc',
       'G_DASH_HIT_COL': 'get_dash_hit_col',
       'E_CHARACTER_ATTR': 'change_character_attr',
       'E_MECHA_LOD_LOADED': 'on_mecha_lod_loaded',
       'E_REMOVE_DASH_COL': 'remove_hit_collision'
       }

    def read_data_from_custom_param(self):
        self.tick_interval = self.custom_param.get('tick_interval', 0.1)
        self.skill_id = self.custom_param.get('skill_id', 410851)
        self.dash_duration = self.custom_param.get('dash_duration', 5)
        self.forward_walk_speed = self.custom_param.get('forward_walk_speed', 60) * NEOX_UNIT_SCALE
        self.back_walk_speed = self.custom_param.get('back_walk_speed', 60) * NEOX_UNIT_SCALE
        self.move_acc = self.custom_param.get('move_acc', 8) * NEOX_UNIT_SCALE
        self.brake_acc = self.custom_param.get('brake_acc', 6) * NEOX_UNIT_SCALE
        self.rotate_speed = self.custom_param.get('rotate_speed', 7)
        self.rotate_speed = math.radians(self.rotate_speed)
        self.min_hit_speed = self.custom_param.get('min_hit_speed', 20) * NEOX_UNIT_SCALE
        self.hit_interval = self.custom_param.get('hit_interval', 3)
        size = 2
        self.hit_range = self.custom_param.get('hit_range', [size, size, size])

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DashMotorcycle, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.walk_speed = 0
        self.is_front = True
        self.cur_move_acc = 0
        self.hit_col = None
        self.alreay_hit_objs = {}
        return

    def change_character_attr(self, name, *arg):
        if name == 'dump_character':
            group = 0
            mask = 0
            if self.hit_col:
                group = self.hit_col.group
                mask = self.hit_col.mask
            print(('test--DashMotorcycle.dump_character--step1--hit_col =', self.hit_col, '--group =', group, '--mask =', mask, '--unit_obj =', self.unit_obj))
        if name == 'test_dash_col':
            shape = self.hit_col.get_shape(0)
            ret = global_data.game_mgr.scene.scene_col.static_test(self.hit_col, 65535, collision_const.GROUP_SHOOTUNIT, collision.INCLUDE_FILTER) or []
            print(('test--change_character_attr.test_dash_col--step1--ret =', ret, '--hit_col.position =', self.hit_col.position, '--tick_interval =', self.tick_interval, '--shape.size =', shape.size, '--GROUP_SHOOTUNIT =', collision_const.GROUP_SHOOTUNIT, '--hit_col.group =', self.hit_col.group, '--hit_col.mask =', self.hit_col.mask, '--skill_id =', self.skill_id, '--unit_obj =', self.unit_obj))

    def on_mecha_lod_loaded(self, owner_model, lod_res_path):
        if not self.hit_col:
            self.create_hit_collision()

    def destroy(self):
        super(DashMotorcycle, self).destroy()
        self.remove_hit_collision()

    def get_dash_hit_col(self):
        if not self.hit_col:
            return 0
        return self.hit_col.cid

    def get_dash_brake_acc(self):
        return self.brake_acc

    def change_driver(self, driver_id):
        if not global_data.player:
            return
        else:
            if driver_id != None:
                return
            model = self.ev_g_model()
            if self.hit_col:
                self.hit_col.mask = 0
                self.hit_col.group = 0
            if self.is_active:
                self.disable_self()
                self.send_event('E_ACTIVE_STATE', MC_RUN)
            return

    def remove_hit_collision(self):
        if self.hit_col:
            global_data.emgr.scene_remove_shoot_vehicle_event.emit(self.hit_col.cid)
            model = self.ev_g_model()
            if model:
                model.unbind_col_obj(self.hit_col)
            self.hit_col = None
        return

    def create_hit_collision(self):
        model = self.ev_g_model()
        if not model:
            return
        self.remove_hit_collision()
        hit_width = self.hit_range[0] * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * NEOX_UNIT_SCALE
        size = math3d.vector(hit_width, hit_height, hit_depth)
        self.hit_col = collision.col_object(collision.BOX, size, 0, 0, 0)
        global_data.emgr.scene_add_shoot_vehicle_event.emit(self.hit_col.cid, self.unit_obj)
        model.bind_col_obj(self.hit_col, animation_const.BONE_CHESHEN_BONE01_NAME)

    def begin_or_end_dash(self, *args):
        if self.ev_g_get_state(MC_DASH):
            self.disable_self()
            self.send_event('E_ACTIVE_STATE', MC_RUN)
            return
        from logic.gutils.move_utils import can_move
        if not can_move():
            return
        self.try_vehicle_dash()

    def enter(self, leave_states):
        super(DashMotorcycle, self).enter(leave_states)
        self.alreay_hit_objs = {}
        rocker_dir = self.sd.ref_rocker_dir
        if not rocker_dir or rocker_dir.is_zero:
            rocker_dir = math3d.vector(0, 0, 1)
        self.is_front = rocker_dir.z > 0 or rocker_dir.is_zero
        if self.is_front:
            self.walk_speed = self.forward_walk_speed
        else:
            self.walk_speed = self.back_walk_speed
        self.cur_move_acc = self.move_acc
        self.send_event('E_DO_SKILL', self.skill_id)
        if self.hit_col:
            self.hit_col.mask = collision_const.GROUP_SHOOTUNIT
            self.hit_col.group = collision_const.GROUP_SHOOTUNIT
        self.send_event('E_TRIGGER_DASH_EFFECT', True)

    def exit(self, enter_states):
        super(DashMotorcycle, self).exit(enter_states)
        if self.hit_col:
            self.hit_col.mask = 0
            self.hit_col.group = 0
        self.send_event('E_TRIGGER_DASH_EFFECT', False)

    def check_transitions(self):
        if self.elapsed_time >= self.dash_duration:
            self.disable_self()
            return MC_MOVE

    def update(self, dt):
        super(DashMotorcycle, self).update(dt)
        rocker_dir = self.sd.ref_rocker_dir
        if not rocker_dir or rocker_dir.is_zero:
            rocker_dir = math3d.vector(0, 0, 1)
        cur_is_front = rocker_dir.z > 0 or rocker_dir.is_zero
        if self.is_front != cur_is_front:
            self.is_front = cur_is_front
            if self.is_front:
                self.walk_speed = self.forward_walk_speed
            else:
                self.walk_speed = self.back_walk_speed
            self.cur_move_acc = self.brake_acc
        cur_speed = self.sd.ref_cur_speed
        speed_scale = self.ev_g_get_speed_scale() or 1
        max_speed = speed_scale * self.walk_speed
        acc = cur_speed < max_speed
        cur_move_acc = self.cur_move_acc * 1 if acc else -1
        cur_speed += dt * cur_move_acc
        cur_speed = clamp(cur_speed, 0, max_speed)
        self.sd.ref_cur_speed = cur_speed
        char_ctrl = self.sd.ref_character
        walk_direction = char_ctrl.getWalkDirection()
        self.send_event('E_MOVE', rocker_dir)
        self.check_hit_enemy_tick(dt)

    def play_hit_effect(self, eid):
        model = self.ev_g_model()
        if not model:
            return
        else:
            start = model.get_bone_matrix(animation_const.BONE_CHESHEN_BONE01_NAME, world.SPACE_TYPE_WORLD).translation
            pos, rot = None, math3d.matrix()
            entity = EntityManager.getentity(eid)
            if entity and entity.logic:
                target_model = entity.logic.ev_g_model()
                if target_model:
                    end = target_model.position + math3d.vector(0, target_model.bounding_box.y, 0)
                    direct = end - start
                    direct.normalize()
                    direct *= NEOX_UNIT_SCALE * 50
                    if entity.logic.sd.ref_model_hit_by_ray_func:
                        res = entity.logic.sd.ref_model_hit_by_ray_func(start, direct)
                    else:
                        res = target_model.hit_by_ray2(start, direct)
                    if res and res[0]:
                        pos = start + direct * res[1]
            if not pos:
                return rot
            return rot

    def check_hit_enemy_tick(self, dt):
        if not global_data.player or not global_data.player.logic or not self.hit_col:
            return
        if self.sd.ref_cur_speed < self.min_hit_speed:
            return
        main_player = global_data.player.logic
        ret = global_data.game_mgr.scene.scene_col.static_test(self.hit_col, 65535, collision_const.GROUP_SHOOTUNIT, collision.INCLUDE_FILTER) or []
        hit_obj = []
        hit_static = []
        hit_effect_rot = []
        hit_cid = self.ev_g_human_base_col_id()
        relative_ids = self.sd.ref_mecha_relative_cols
        self_cids = [self.hit_col.cid, hit_cid]
        if relative_ids:
            self_cids.extend(relative_ids)
        cur_time = time.time()
        for col in ret:
            if col.cid not in self_cids:
                model_col_name = getattr(col, 'model_col_name', '')
                if global_data.emgr.scene_is_shoot_obj.emit(col.cid):
                    res = global_data.emgr.scene_find_unit_event.emit(col.cid)
                    if res and res[0] and res[0].__class__.__name__ == 'LHouse':
                        return
                    if res and res[0] and res[0].__class__.__name__ == 'LField':
                        eid = res[0].id
                        field = EntityManager.getentity(eid)
                        if field and field.logic and self.ev_g_is_campmate(field.logic.ev_g_camp_id()):
                            continue
                        if cur_time - self.alreay_hit_objs.get(eid, 0) >= self.hit_interval:
                            hit_obj.append(eid)
                            rot = self.play_hit_effect(eid)
                            hit_effect_rot.append(rot)
                            self.alreay_hit_objs[eid] = cur_time
                            break
                    if res and res[0] and res[0].ev_g_is_campmate(self.ev_g_camp_id()):
                        continue
                    if res and res[0] and res[0] != global_data.player.logic:
                        eid = res[0].id
                        ent = EntityManager.getentity(eid)
                        if not ent:
                            continue
                        if cur_time - self.alreay_hit_objs.get(eid, 0) >= self.hit_interval:
                            if res[0].__class__.__name__ == 'LHPBreakable':
                                if not res[0].share_data.ref_hp or res[0].share_data.ref_hp <= 0:
                                    continue
                            if res[0].__class__.__name__ == 'LMecha':
                                mecha_creator = res[0].ev_g_creator()
                                if not mecha_creator:
                                    continue
                                is_teammate = main_player.ev_g_is_groupmate(mecha_creator.id, False)
                                if is_teammate:
                                    continue
                            hit_obj.append(eid)
                            rot = self.play_hit_effect(eid)
                            hit_effect_rot.append(rot)
                            self.alreay_hit_objs[eid] = cur_time
                else:
                    hit_static.append(col)

        start = self.hit_col.position
        if len(hit_obj) > 0:
            pos = self.ev_g_position()
            self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, hit_obj), False, True)

    def try_vehicle_dash(self):
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()


class Walk4108(Walk):

    def enter(self, leave_states):
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
            global_data.player.logic.send_event('E_VEHICLE_BEGIN_MOVE')
        if leave_states and MC_STAND in leave_states:
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_start')), 0, False, None, 6)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
             bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_start')), 0, False, None, 6)], True)
        super(Walk4108, self).enter(leave_states)
        return

    def check_transitions(self):
        return super(Walk4108, self).check_transitions()

    def exit(self, enter_states):
        if self.sd.ref_cur_speed == 0:
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_end')), 0, False, None, 6)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
             bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, ('Play_duorenzaiju', ('duorenzaiju', 'duorenzaiju_end')), 0, False, None, 6)], True)
        super(Walk4108, self).exit(enter_states)
        return


class Run4108(Run):
    BIND_EVENT = Run.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTION_YAW': 'on_action_yaw'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Run4108, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.cur_brake_acc = self.brake_acc

    def enter(self, leave_states):
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_driver():
            global_data.player.logic.send_event('E_VEHICLE_BEGIN_MOVE')
        if leave_states and MC_DASH in leave_states:
            self.cur_brake_acc = -self.ev_g_dash_brake_acc()
        else:
            self.cur_brake_acc = self.brake_acc
        super(Run4108, self).enter(leave_states)

    def exit(self, enter_states):
        super(Run4108, self).exit(enter_states)

    def update(self, dt):
        super(Run, self).update(dt)
        rocker_dir = self.sd.ref_rocker_dir
        can_run = self.sd.ref_can_run
        if self.show_stop_anim and not can_run and self.sub_state != self.STATE_STOP:
            self.sub_state = self.STATE_STOP
        if self.sub_state == self.STATE_STOP:
            rocker_dir = None
        if self.last_rocker_dir != rocker_dir:
            self.last_rocker_dir = rocker_dir
            self.send_event('E_ACTION_MOVE')
        cur_speed = self.sd.ref_cur_speed
        speed_scale = self.ev_g_get_speed_scale() or 1
        max_speed = speed_scale * self.run_speed
        acc = rocker_dir and not rocker_dir.is_zero
        if cur_speed > max_speed:
            acc = False
        cur_speed += dt * (self.move_acc if acc and can_run else self.cur_brake_acc)
        if acc:
            cur_speed = clamp(cur_speed, 0, max_speed)
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_MOVE', rocker_dir)
        if self.enable_dynamic_speed_rate:
            self.send_event('E_ANIM_RATE', LOW_BODY, cur_speed / self.run_speed * self.dynamic_speed_rate)
        return

    def check_transitions(self):
        return super(Run4108, self).check_transitions()


class Die4108(Die):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Die4108, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.anim_duration = self.custom_param.get('anim_duration', 2)
        self._die_action = self.custom_param.get('die_action', None)
        self._die_timer_id = None
        self._model = None
        return

    def enter(self, leave_states):
        self.send_event('E_ROCK_STOP')
        self.send_event('E_CLEAR_SPEED')
        super(Die4108, self).enter(leave_states)

    def exit(self, enter_states):
        super(Die4108, self).exit(enter_states)

    def on_exit(self, *args):
        self._die_timer_id = None
        self.manual_destroy()
        if not self.ev_g_get_state(self.sid):
            return
        else:
            self.disable_self()
            return

    def manual_destroy(self):
        if self._model and self._model.valid:
            scene = world.get_active_scene()
            scene.remove_object(self._model)
            self._model.destroy()
            self._model = None
        return

    def on_die(self, *args):
        self.active_self()
        if self._die_action:
            clip_name, part, blend_dir, kwargs = self._die_action
            self.send_event('E_POST_ACTION', clip_name, (LOW_BODY if part == 'lower' else UP_BODY), blend_dir, **kwargs)
        if self._die_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._die_timer_id)
            self._die_timer_id = None
        self._die_timer_id = global_data.game_mgr.register_logic_timer(self.on_exit, self.anim_duration, times=1, mode=timer.CLOCK)
        self._model = self.ev_g_model()
        self.send_event('E_DELAY_DESTROY')
        return


class Fall4108(Fall):

    def check_transitions(self):
        is_in_water_area = self.ev_g_is_in_water_area()
        if is_in_water_area:
            self.disable_self()
            return self.status_config.MC_STAND

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Fall4108, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = 1.0 / 30.0

    def update(self, dt):
        super(Fall4108, self).update(dt)
        self.send_event('E_CHECK_WATER_AREA')


class OnGround4108(OnGround):

    def check_transitions(self):
        rocker_dir = self.sd.ref_rocker_dir
        if self.elapsed_time > self.recover_time:
            if rocker_dir and not rocker_dir.is_zero:
                return self.status_config.MC_MOVE
        if self.elapsed_time > self.anim_time:
            self.send_event('E_CLEAR_SPEED')
            return self.status_config.MC_STAND

    def exit(self, enter_states):
        super(OnGround4108, self).exit(enter_states)
        self.send_event('E_LEAVE_JUMP_GROUND')

    def update(self, dt):
        super(OnGround, self).update(dt)
        move_dir = self.ev_g_move_dir()
        if self.elapsed_time < 0.1 or move_dir is None or not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
            return
        else:
            speed = (self.sd.ref_cur_speed or 0) - dt * self.brake_acc
            speed = 0 if speed < 0 else speed
            self.sd.ref_cur_speed = speed
            if self.last_speed > 0 and speed == 0:
                self.send_event('E_ACTION_SYNC_STOP')
            self.last_speed = speed
            self.send_event('E_SET_WALK_DIRECTION', move_dir * speed)
            return