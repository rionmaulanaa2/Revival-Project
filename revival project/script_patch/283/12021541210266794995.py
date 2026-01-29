# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComVehicleDriver2.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import math
import time
import game
import math3d
import world
import collision
from logic.client.const.camera_const import VEHICLE_MODE
from logic.gcommon.common_const import vehicle_const
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import paragliding_const
from ..UnitCom import UnitCom
from logic.gcommon.cdata.mecha_status_config import MC_TRANSFORM
import logic.gcommon.common_const.collision_const as collision_const
from logic.gutils import character_ctrl_utils
MIN_SLOPE_DEGREE = 45

class ComVehicleDriver2(UnitCom):
    BIND_EVENT = {'E_VECHICLE_LOADED': 'on_vehicle_load',
       'E_START_CONTROL_VEHICLE': '_start_control_vehicle',
       'E_STOP_CONTROL_VEHICLE': '_stop_control_vehicle',
       'E_FOOT_POSITION': 'set_foot_position',
       'E_SET_POSITION': '_set_pos',
       'G_POSITION': '_get_pos',
       'G_FOOT_POSITION': 'get_foot_position',
       'G_IS_VERTICAL_IN_WALL': 'is_vertical_in_wall',
       'G_YAW': '_get_yaw',
       'G_CHAR_WALK_DIRECTION': '_get_walk_direction',
       'E_VEHICLE_ENABLE_PHYSICS': '_enable_physics',
       'G_WHEEL_ROTATION_RADIAN': '_get_wheel_rotation_radian',
       'G_WHEEL_ROTATION_SPEED': '_get_wheel_rotation_speed',
       'E_ON_VEHICLE_COLLISION': '_on_vehicle_collision',
       'G_VEHICLE_COLLISION_ID': '_get_collision_id',
       'G_MOVE_DIRECTION': '_get_move_direction',
       'E_SIMULATE_PHYSICS': '_simulate_physics',
       'G_SIMULATE_PHYSICS': '_get_simulate_physics',
       'G_SIMULATE_PHYSICS_ID': '_get_simulate_player',
       'E_VEHICLE_GAS_CHANGED': '_on_gas_changed',
       'E_VEHICLE_ENABLE_PHYSX': '_set_physx_enable',
       'E_VEHICLE_HEALTH_CHANGED': '_on_vehicle_health_change',
       'E_ON_POS_CHECK_INVALID': '_on_pos_check_invalid',
       'E_MOVE_STATUS_CHANGED': '_on_move_status_changed',
       'E_DELTA_YAW': ('_set_forward_yaw', 1),
       'G_VEHICLE_TARGET_YAW': '_on_get_target_yaw',
       'E_VEHICLE_ENGINE_BREAK': '_on_set_engine_break',
       'E_SET_TARGET_YAW_OFFSET': '_set_target_yaw_offset',
       'E_ENABLE_TARGET_YAW_OFFSET': 'on_enable_target_yaw_offset',
       'E_ENABLE_VEHICLE_CAMERA_FOLLOW': 'on_enable_camera_follow',
       'E_SWITCH_VEHICLE_OPE_TYPE': 'on_switch_vehicle_ope_type',
       'E_TRANSFORMING_TO_VEHICLE_IN_WATER': 'on_transforming_to_vehicle_in_water',
       'E_RESET_VEHICLE_MAT_BY_MODEL': '_reset_vehicle_mat_by_model',
       'E_CHONGCI': ('_on_chongci', 1),
       'E_SET_VEHICLE_SPEED': 'set_vehicle_speed',
       'E_SUPER_JUMP': 'on_super_jump',
       'E_ON_FROZEN': '_on_frozen',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_CLEAR_SPEED': '_move_stop'
       }
    CONTROL_EVENT = {'E_MOVE_ACC': '_move_acc',
       'E_MOVE_FORWARD': '_move_forward',
       'E_MOVE_NO_FORCE': '_move_no_force',
       'E_MOVE_BACK': '_move_back',
       'E_MOVE_BRAKE_START': '_brake_begin',
       'E_MOVE_BRAKE_END': '_brake_end',
       'E_VEHICLE_HORN': 'on_vehicle_horn',
       'E_SET_MAX_OMEGA': '_set_max_omega'
       }
    MIN_DELTA_DIST = 3
    SENSITIVE_SPEED = 20
    COLLISTION_FACTOR = 1000
    CHECK_STATIC_TIME = 0.1
    CHECK_MOVE_DIR = 0.3
    ITVL_NOTI_ENGINE_ARGS = 0.2

    def __init__(self):
        super(ComVehicleDriver2, self).__init__()
        if self.sd.ref_cur_speed is None:
            self.sd.ref_cur_speed = 0
        self.vehicle = None
        self.move_status = vehicle_const.MOVE_STOP
        now = time.time()
        self.last_op_info = None
        self.pos_for_check_static = math3d.vector(0, 0, 0)
        self.time_for_check_static = now
        self.pos_for_check_move_dir = math3d.vector(0, 0, 0)
        self.time_for_check_move_dir = now
        self.pos_for_check_move_status = math3d.vector(0, 0, 0)
        self.time_for_check_move_status = now
        self.time_for_check_update_force = now
        self._yaw = 0
        self._target_yaw = 0
        self.static_col = None
        self._enable_physics_flag = None
        self._phys_player = None
        self.move_dir_factor = 1
        self._t_args_noti = 0
        self.is_strong_handbrake = False
        self.is_engine_broken = False
        self._enable_target_yaw_offset = False
        self._target_yaw_offset = 0
        self._enable_camera_follow = False
        self._delay_camera_follow_frame = 5
        self.cur_camera_speed = 0
        self._last_vehicle_yaw = None
        self._target_pitch = 0
        self._vehical_yaw_list = []
        self.additive_speed_frame = 0
        self.additive_speed = 0
        self._diff_pitch = 0
        self._is_auto_chongci = False
        self._is_on_chongci = False
        self._is_transforming_to_vehicle_in_water = False
        self._last_transforming_status = None
        self._last_transforming_force = None
        self._is_in_frozen = False
        self._has_bind_control_event = False
        self._ini_speed = None
        self._update_timer_id = None
        self._last_train_speed = None
        return

    def start_update_timer(self):
        from common.utils import timer
        tm = global_data.game_mgr.get_post_logic_timer()
        if self._update_timer_id:
            return
        self._update_timer_id = tm.register(func=self._on_update, interval=1, timedelta=True)
        part_camera = world.get_active_scene().get_com('PartCamera')
        if part_camera:
            part_camera.cam_manager.on_net_reconnect()

    def stop_update_timer(self):
        from common.utils import timer
        tm = global_data.game_mgr.get_post_logic_timer()
        if self._update_timer_id:
            tm.unregister(self._update_timer_id)
        self._update_timer_id = None
        return

    def on_init_complete(self):
        pass

    def _get_move_direction(self):
        return self.move_dir_factor

    def _on_move_status_changed(self, data):
        if data == vehicle_const.MOVE_ENGINE_BREAK:
            self.is_engine_broken = True

    def _simulate_physics(self, vehicle_info):
        simulate_id = vehicle_info['simulate_id']
        myid = global_data.player.id
        if myid == simulate_id:
            self._brake()
            impulse = math3d.vector(*vehicle_info['impulse'])
            m = self.ev_g_model()
            self.scene.scene_col.apply_impulse(m.position, math3d.vector(1, 1, 1), impulse)

    def _get_walk_direction(self):
        if not self.vehicle:
            return
        return self.vehicle.speed

    def get_wheel_rotation_info(self):
        if not self.vehicle:
            return {}
        wheels_agl = {}
        for idx in range(vehicle_const.VEHICLE_WHEEL_COUNT):
            wheels_agl[idx] = round(self._get_wheel_rotation_radian(idx), 2)

        return wheels_agl

    def _get_wheel_rotation_radian(self, index):
        if not self.vehicle:
            return
        return self.vehicle.get_wheel_rotation_angle(index)

    def _get_wheel_rotation_speed(self, index):
        if not self.vehicle:
            return
        return self.vehicle.get_wheel_rotation_speed(index)

    def _get_yaw(self):
        if global_data.player and self.sd.ref_driver_id != global_data.player.id:
            m = self.ev_g_model()
            if m:
                return m.world_transformation.yaw
            return 0
        else:
            if not self.vehicle:
                return None
            yaw = self.vehicle.forward.yaw
            self._yaw = yaw
            return self._yaw

    def _on_vehicle_health_change(self, health):
        if health[0] <= 0:
            self.unit_obj.del_com('ComVehicleMoveSyncSender')

    def _start_control_vehicle(self):
        if self.vehicle:
            self._target_yaw = self._get_yaw()
            self._target_yaw_offset = 0
            from logic.gutils.CameraHelper import get_camera_state_default_pitch
            self._target_pitch = get_camera_state_default_pitch(VEHICLE_MODE)
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(self._target_yaw, None, True, 0.5)
        if self._has_bind_control_event:
            return
        else:
            self._has_bind_control_event = True
            self._bind_event(self.CONTROL_EVENT)
            return

    def _stop_control_vehicle(self):
        self._has_bind_control_event = False
        self._unbind_event(self.CONTROL_EVENT)

    def _on_set_engine_break(self):
        self.is_engine_broken = True
        self.move_status = vehicle_const.MOVE_ENGINE_BREAK
        self.send_event('E_MOVE_STATUS_CHANGED', self.move_status)
        controler = self.ev_g_simulate_physics_id()
        if controler == global_data.player.id:
            global_data.player.logic.send_event('E_TRY_CHANGE_VEHICLE_DATA', self.unit_obj.id, vehicle_const.CH_MOVE_STATUS, self.move_status)

    def phys_owner_is_me(self):
        return global_data.player and self._phys_player == global_data.player.id

    def init_from_dict(self, unit_obj, bdict):
        super(ComVehicleDriver2, self).init_from_dict(unit_obj, bdict)
        self.vtype = self.ev_g_transform_id()
        self._phys_player = bdict.get('phys_owner', None)
        if not self.phys_owner_is_me():
            self._enable_physics(False)
        self._load_vehicle_ctrl_config()
        vehicle = self.ev_g_vehicle()
        self._ini_speed = bdict['init_speed']
        if vehicle:
            self.on_vehicle_load(vehicle)
            if self.sd.ref_driver_id == global_data.player.id:
                self._start_control_vehicle()
            else:
                print('no control vehicle')
        return

    def _load_vehicle_ctrl_config(self):
        from common.cfg import confmgr
        import math
        self.acc_force = 1
        self.back_force = -1
        self.brake_force = 0
        self.max_steer_angle = math.degrees(confmgr.get('vehicle_data2', str(self.vtype), 'max_steer'))
        self.brake_factor = confmgr.get('vehicle_data2', str(self.vtype), 'brake_factor')
        self.diss_speed_turn = confmgr.get('vehicle_data2', str(self.vtype), 'diss_speed_turn')
        self.diss_turn_rate = confmgr.get('vehicle_data2', str(self.vtype), 'diss_turn_angle')
        self.max_omega = confmgr.get('vehicle_data2', str(self.vtype), 'max_omega')
        self.acc_max_omega = confmgr.get('vehicle_data2', str(self.vtype), 'acc_max_omega')
        self.max_omega_factor = 1.0

    def _get_pos(self):
        m = self.ev_g_model()
        if m:
            return m.position

    def get_ground_height(self, chect_begin, check_end):
        hit_point_list = []
        group = collision_const.GROUP_CAN_SHOOT
        mask = collision_const.GROUP_CAN_SHOOT
        filter_col_ids = self.ev_g_all_exclude_col_id()
        col_model_obj_list = []
        is_hit = character_ctrl_utils.hit_by_scene_collision(chect_begin, check_end, group, mask, filter_type=collision.INCLUDE_FILTER, filter_col_ids=filter_col_ids, col_model_obj_list=col_model_obj_list, is_multi_select=True, hit_point_list=hit_point_list)
        if is_hit and hit_point_list:
            hit_position = hit_point_list[0]
            return hit_position.y

    def is_vertical_in_wall(self):
        vehicle = self.ev_g_vehicle()
        if not vehicle:
            return True
        wheel_count = 4
        up_dir = math3d.vector(0, 1, 0)
        in_wall_count = 0
        for index in range(wheel_count):
            one_is_wheel_in_air = vehicle.get_wheel_in_air(index)
            one_wheel_contact_normal = vehicle.get_wheel_contact_normal(index)
            dot_ret = up_dir.dot(one_wheel_contact_normal)
            dot_ret = -1.0 if dot_ret < -1.0 else dot_ret
            dot_ret = 1.0 if dot_ret > 1.0 else dot_ret
            one_radian = math.acos(dot_ret)
            degree = math.degrees(one_radian)
            if not one_is_wheel_in_air and degree >= MIN_SLOPE_DEGREE:
                in_wall_count += 1

        return in_wall_count > 1

    def get_foot_position(self):
        model = self.ev_g_model()
        if not model:
            return math3d.vector(0, 0, 0)
        vehicle = self.ev_g_vehicle()
        if not vehicle:
            return math3d.vector(0, 0, 0)
        position = vehicle.position
        up_dir = math3d.vector(0, 1, 0)
        wheel_count = 4
        last_degree = MIN_SLOPE_DEGREE
        for index in range(wheel_count):
            one_is_wheel_in_air = vehicle.get_wheel_in_air(index)
            one_wheel_contact_normal = vehicle.get_wheel_contact_normal(index)
            dot_ret = up_dir.dot(one_wheel_contact_normal)
            dot_ret = -1.0 if dot_ret < -1.0 else dot_ret
            dot_ret = 1.0 if dot_ret > 1.0 else dot_ret
            one_radian = math.acos(dot_ret)
            degree = math.degrees(one_radian)
            if not one_is_wheel_in_air and degree < last_degree:
                wheel_pos = vehicle.get_wheel_contact_point(index)
                position = wheel_pos
                last_degree = degree

        return position

    def _set_pos(self, pos):
        vehicle = self.ev_g_vehicle()
        if vehicle:
            vehicle.position = pos
        model = self.ev_g_model()
        if model:
            model.position = pos

    def set_foot_position(self, pos):
        vehicle = self.ev_g_vehicle()
        if not vehicle:
            return
        wheel_contact_normal = vehicle.get_wheel_contact_normal(0)
        is_wheel_in_air = vehicle.get_wheel_in_air(0)
        if is_wheel_in_air or wheel_contact_normal.y <= 0.01:
            if pos.y <= vehicle.position.y:
                return
        self._set_pos(pos)

    def _on_pos_check_invalid(self):
        global_data.game_mgr.next_exec(self.delay_on_pos_check_invalid)

    def delay_on_pos_check_invalid(self):
        self._move_no_force()
        vehicle = self.ev_g_vehicle()
        if vehicle:
            vehicle.speed = math3d.vector(0, 0, 0)
            vehicle.angular_speed = math3d.vector(0, 0, 0)

    def _on_vehicle_collision(self, other_vehicle):
        pass

    def _on_gas_changed(self, cur_gas):
        pass

    def on_vehicle_load(self, vehicle):
        self.vehicle = vehicle
        if self._ini_speed:
            vehicle.speed = self._ini_speed
        self._last_vehicle_yaw = self.vehicle.forward.yaw
        vehicle.set_position_changed_callback(self._position_changed)
        self.last_op_info = None
        self.start_update_timer()
        self._target_yaw = self.vehicle.forward.yaw
        return

    def _position_changed(self, pos, world_mat):
        if self.unit_obj:
            send_event = self.send_event
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(pos)
            else:
                send_event('E_POSITION', pos)
            send_event('E_VEHICLE_SYNC_TRANSFORM', world_mat)
            yaw = self.vehicle.forward.yaw
            diff_yaw = yaw - self._yaw
            self._yaw = diff_yaw

    def _get_rotation(self):
        m = self.ev_g_model()
        if m:
            return m.world_transformation.forward

    def _on_chongci--- This code section failed: ---

 583       0  LOAD_FAST             1  'flag'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            0  '_is_on_chongci'

 584       9  LOAD_FAST             1  'flag'
          12  POP_JUMP_IF_FALSE    86  'to 86'

 585      15  LOAD_GLOBAL           1  'getattr'
          18  LOAD_GLOBAL           1  'getattr'
          21  LOAD_CONST            2  ''
          24  CALL_FUNCTION_3       3 
          27  STORE_FAST            2  'force'

 586      30  LOAD_FAST             2  'force'
          33  LOAD_CONST            2  ''
          36  COMPARE_OP            2  '=='
          39  POP_JUMP_IF_FALSE   123  'to 123'

 587      42  LOAD_FAST             0  'self'
          45  LOAD_ATTR             2  '_move_forward'
          48  CALL_FUNCTION_0       0 
          51  POP_TOP          

 588      52  LOAD_GLOBAL           3  'True'
          55  LOAD_FAST             0  'self'
          58  STORE_ATTR            4  '_is_auto_chongci'

 589      61  LOAD_GLOBAL           5  'global_data'
          64  LOAD_ATTR             6  'emgr'
          67  LOAD_ATTR             7  'show_chongci_ui'
          70  LOAD_ATTR             8  'emit'
          73  LOAD_GLOBAL           3  'True'
          76  CALL_FUNCTION_1       1 
          79  POP_TOP          
          80  JUMP_ABSOLUTE       123  'to 123'
          83  JUMP_FORWARD         37  'to 123'

 591      86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             9  'vehicle'
          92  STORE_FAST            3  'vehicle'

 592      95  LOAD_FAST             3  'vehicle'
          98  POP_JUMP_IF_FALSE   123  'to 123'

 593     101  LOAD_FAST             0  'self'
         104  LOAD_ATTR            10  'max_omega'
         107  LOAD_FAST             0  'self'
         110  LOAD_ATTR            11  'max_omega_factor'
         113  BINARY_MULTIPLY  
         114  LOAD_FAST             3  'vehicle'
         117  STORE_ATTR           10  'max_omega'
         120  JUMP_FORWARD          0  'to 123'
       123_0  COME_FROM                '120'
       123_1  COME_FROM                '83'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 24

    def apply_force(self, force):
        if not global_data.debug_vehicle:
            vehicle = self.vehicle
            if vehicle:
                self.force = force

    def apply_sterring(self, angle):
        vehicle = global_data.debug_vehicle or self.vehicle
        if vehicle:
            angle = angle / 25.0
            if self._is_on_chongci:
                max_omega = self.acc_max_omega * self.max_omega_factor if 1 else self.max_omega * self.max_omega_factor
                if angle > self.diss_turn_rate:
                    vehicle.max_omega = max_omega * self.diss_speed_turn
                else:
                    vehicle.max_omega = max_omega
                vehicle.set_analog_steer(angle)

    def _get_collision_id(self):
        if self.static_col:
            return self.static_col.cid
        else:
            if self.vehicle:
                return self.vehicle.cid
            return None

    def _nomalize_angle(self, angle):
        pi = math.pi
        pi2 = pi * 2
        while angle > pi:
            angle -= pi2

        while angle < -pi:
            angle += pi2

        return angle

    def _check_move_direction(self):
        m = self.ev_g_model()
        npos = m.position
        now = time.time()
        if now - self.time_for_check_move_dir > self.CHECK_MOVE_DIR:
            pos_diff = npos - self.pos_for_check_move_dir
            if pos_diff.length > self.MIN_DELTA_DIST:
                self.pos_for_check_move_dir = npos
                v = self.vehicle
                pos_diff.y = 0
                speed_dir = v.forward
                speed_dir.y = 0
                if speed_dir.is_zero:
                    return
                if pos_diff.is_zero:
                    return
                pos_diff.normalize()
                speed_dir.normalize()
                cosx = pos_diff.dot(speed_dir)
                if cosx < 0:
                    self.move_dir_factor = 1
                elif cosx > 0:
                    self.move_dir_factor = -1

    def _tick_for_steer_action(self):
        m = self.ev_g_model()
        w_trans = m.world_transformation
        m_yaw = self._nomalize_angle(w_trans.yaw)
        self._check_move_direction()
        if self._enable_target_yaw_offset:
            self._target_yaw = m_yaw + self._target_yaw_offset * -self.move_dir_factor
        pi = math.pi
        hpi = pi / 2
        scn = self.scene
        com_camera = scn.get_com('PartCamera')
        target_yaw = self._nomalize_angle(self._on_get_target_yaw())
        diff_yaw = m_yaw - target_yaw
        if m_yaw != target_yaw:
            diff_yaw = self._nomalize_angle(m_yaw - target_yaw)
            if diff_yaw >= hpi:
                angle = self.max_steer_angle
            elif diff_yaw <= -hpi:
                angle = -self.max_steer_angle
            else:
                angle = diff_yaw / hpi * self.max_steer_angle
            angle *= self.move_dir_factor
            self.apply_sterring(angle)
        else:
            self.apply_sterring(0)
        self._vehical_yaw_list.append(m_yaw)
        if len(self._vehical_yaw_list) > 60:
            self._vehical_yaw_list.pop(0)
        if self._enable_camera_follow:
            if len(self._vehical_yaw_list) > 8:
                if self.additive_speed_frame > 0.1:
                    self.additive_speed_frame -= 1
                    self.addtive_yaw += self.additive_speed
                    yyy = self._diff_yaw - self.addtive_yaw
                    com_camera.set_yaw(self._vehical_yaw_list[-8] - yyy)
                    self.update_camera_pitch_follow_status()
                else:
                    com_camera.set_yaw(self._vehical_yaw_list[-8])
        driver_id = self.sd.ref_driver_id
        driver = EntityManager.getentity(driver_id)
        if driver and driver.logic:
            driver.logic.send_event('E_VEHICLE_TURN', diff_yaw)

    def _check_engine_args(self):
        t = time.time()
        if self._t_args_noti + ComVehicleDriver2.ITVL_NOTI_ENGINE_ARGS > t:
            return
        if not self.vehicle or not self._enable_physics_flag:
            return
        sp_info = {'eg_spd': self.vehicle.engine_speed,
           'wheels_agl': self.get_wheel_rotation_info()
           }
        self.send_event('E_VEHICLE_ENGINE_SPEED_CHANGE', sp_info)

    def _tick_user_action(self):
        if not self._enable_physics_flag:
            return
        else:
            if self.vehicle is None:
                self.need_update = False
                self.stop_update_timer()
                return
            if self.static_col:
                self.need_update = False
                self.stop_update_timer()
                return
            self._check_engine_args()
            id_driver = self.sd.ref_driver_id
            if id_driver == global_data.player.id:
                self._tick_for_steer_action()
            now = time.time()
            m = self.ev_g_model()
            npos = m.position
            if self._is_in_frozen:
                self.move_status = vehicle_const.MOVE_STOP
                self.vehicle.speed = math3d.vector(0, 0, 0)
            if self.move_status not in [vehicle_const.MOVE_STOP, vehicle_const.MOVE_BRAKE, vehicle_const.MOVE_NO_FORCE]:
                self.time_for_check_static = now
                self.pos_for_check_static = npos
                return
            if now - self.time_for_check_static > self.CHECK_STATIC_TIME:
                pos_diff = npos - self.pos_for_check_static
                md = max(abs(pos_diff.x), abs(pos_diff.y), abs(pos_diff.z))
                if md < self.MIN_DELTA_DIST and not self.ev_g_get_state(MC_TRANSFORM) and not self.vehicle.in_air:
                    self._enable_physics(False)
                    self.move_status = vehicle_const.MOVE_STOP
                    global_data.player.logic.send_event('E_TRY_CHANGE_VEHICLE_DATA', self.unit_obj.id, vehicle_const.CH_MOVE_STATUS, self.move_status)
                    self.need_update = False
                    self.stop_update_timer()
                else:
                    self.time_for_check_static = now
                    self.pos_for_check_static = npos
            return

    def is_in_air(self):
        if not self.vehicle:
            return False
        for i in range(4):
            if self.vehicle.get_wheel_in_air(i):
                return True

        return False

    def _move_control(self, status, force):
        if self.vehicle is None:
            return
        else:
            if self._is_transforming_to_vehicle_in_water:
                self._last_transforming_status = status
                self._last_transforming_force = force
                return
            if self.move_status == status:
                return
            self.move_status = status
            self._enable_physics(True)
            self.apply_force(force)
            m = self.ev_g_model()
            now = time.time()
            self.time_for_check_move_status = now
            self.time_for_check_move_dir = now
            npos = m.position
            self.pos_for_check_move_status = npos
            self.pos_for_check_move_dir = npos
            self.start_update_timer()
            controler = self.ev_g_simulate_physics_id()
            if controler == global_data.player.id:
                global_data.player.logic.send_event('E_TRY_CHANGE_VEHICLE_DATA', self.unit_obj.id, vehicle_const.CH_MOVE_STATUS, self.move_status)
            else:
                print('????????????not control but start physical???????????????', controler)
            return

    def check_gas_pass(self):
        return True

    def _move_acc(self):
        if not self.check_gas_pass():
            return
        self._move_control(vehicle_const.MOVE_FORWARD_ACC, self.acc_force)

    def _move_forward(self):
        if not self.check_gas_pass():
            return
        self._move_control(vehicle_const.MOVE_FORWARD, self.acc_force)
        self._is_auto_chongci = False

    def _move_back(self):
        if not self.check_gas_pass():
            return
        self._move_control(vehicle_const.MOVE_BACKWARD, self.back_force)
        self._is_auto_chongci = False

    def _move_no_force(self):
        self._move_control(vehicle_const.MOVE_NO_FORCE, 0)

    def _brake(self):
        self._move_control(vehicle_const.MOVE_BRAKE, 0)
        self._is_auto_chongci = False

    def _set_physx_enable(self, enable, new_player_id, lin_spd, agl_spd):
        if enable and new_player_id != global_data.player.id:
            log_error('E_VEHICLE_ENABLE_PHYSX error : v - {}, new - {}, pp - {}'.format(self.unit_obj.id, new_player_id, global_data.player.id))
            return
        self._phys_player = new_player_id
        self._enable_physics(enable, lin_spd, agl_spd)
        if enable:
            self._reset_vehicle_mat_by_model()

    def _get_simulate_physics(self):
        return self._enable_physics_flag

    def _get_simulate_player(self):
        return self._phys_player

    def _enable_physics(self, flag, lin_spd=None, agl_spd=None, force=False):
        if flag == self._enable_physics_flag:
            return
        if flag and self.is_engine_broken:
            self.send_event('E_VEHICLE_COLLISION_SET', False)
            return
        if flag and not force and self._phys_player != global_data.player.id:
            log_error('E_VEHICLE_ENABLE_PHYSX error : v - {}, old - {}, pp - {}'.format(self.unit_obj.id, self._phys_player, global_data.player.id))
            return
        self._enable_physics_flag = flag
        is_control_driver = self._phys_player == global_data.player.id
        uobj = self.unit_obj
        vehicle = uobj.ev_g_vehicle()
        scene_col = self.scene.scene_col
        if flag:
            self.send_event('E_VEHICLE_COLLISION_SET', flag)
            if vehicle:
                scene_col.add_object(vehicle)
                self.send_event('E_PLAY_EFFECT_BY_STATUS', vehicle_const.MOVE_FORWARD_ACC)
            com = uobj.get_com('ComVehicleMoveSyncSender')
            if not com:
                com = uobj.add_com('ComVehicleMoveSyncSender', 'client')
                com.init_from_dict(uobj, {})
            uobj.send_event('E_VEHICLE_SYNC_TRIGGER_ENABLE', True)
            uobj.del_com('ComVehicleMoveSyncReceiver')
            if vehicle and lin_spd and agl_spd:
                vehicle.speed = lin_spd
                vehicle.angular_speed = agl_spd
        else:
            if vehicle:
                vehicle.linear_velocity = math3d.vector(0, 0, 0)
                scene_col.remove_object(vehicle)
                self.send_event('E_PLAY_EFFECT_BY_STATUS', vehicle_const.MOVE_STOP)
            self.send_event('E_VEHICLE_COLLISION_SET', flag)
            com = uobj.get_com('ComVehicleMoveSyncReceiver')
            if not com and uobj.is_valid():
                com = uobj.add_com('ComVehicleMoveSyncReceiver', 'client')
                com.init_from_dict(uobj, {})
            if vehicle:
                vehicle.speed = math3d.vector(0, 0, 0)
                vehicle.angular_speed = math3d.vector(0, 0, 0)
        if flag:
            self.send_event('E_SET_CONTROLLER', global_data.player.id)

    def _on_update--- This code section failed: ---

 971       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'debug_vehicle'
           6  POP_JUMP_IF_FALSE   282  'to 282'

 973       9  LOAD_GLOBAL           0  'global_data'
          12  LOAD_ATTR             2  'v'
          15  POP_JUMP_IF_FALSE   562  'to 562'

 974      18  LOAD_GLOBAL           0  'global_data'
          21  LOAD_ATTR             2  'v'
          24  STORE_FAST            2  'vehicle'

 976      27  LOAD_GLOBAL           0  'global_data'
          30  LOAD_ATTR             3  'is_key_down'
          33  LOAD_GLOBAL           4  'game'
          36  LOAD_ATTR             5  'VK_W'
          39  CALL_FUNCTION_1       1 
          42  POP_JUMP_IF_FALSE    64  'to 64'

 977      45  LOAD_FAST             2  'vehicle'
          48  LOAD_ATTR             6  'set_gear'
          51  LOAD_GLOBAL           7  'vehicle_const'
          54  LOAD_ATTR             8  'GEAR_FORWARD'
          57  CALL_FUNCTION_1       1 
          60  POP_TOP          
          61  JUMP_FORWARD         37  'to 101'

 978      64  LOAD_GLOBAL           0  'global_data'
          67  LOAD_ATTR             3  'is_key_down'
          70  LOAD_GLOBAL           4  'game'
          73  LOAD_ATTR             9  'VK_S'
          76  CALL_FUNCTION_1       1 
          79  POP_JUMP_IF_FALSE   101  'to 101'

 979      82  LOAD_FAST             2  'vehicle'
          85  LOAD_ATTR             6  'set_gear'
          88  LOAD_GLOBAL           7  'vehicle_const'
          91  LOAD_ATTR            10  'GEAR_REVERSE'
          94  CALL_FUNCTION_1       1 
          97  POP_TOP          
          98  JUMP_FORWARD          0  'to 101'
       101_0  COME_FROM                '98'
       101_1  COME_FROM                '61'

 981     101  LOAD_GLOBAL           0  'global_data'
         104  LOAD_ATTR             3  'is_key_down'
         107  LOAD_GLOBAL           4  'game'
         110  LOAD_ATTR             5  'VK_W'
         113  CALL_FUNCTION_1       1 
         116  POP_JUMP_IF_FALSE   135  'to 135'

 982     119  LOAD_FAST             2  'vehicle'
         122  LOAD_ATTR            11  'set_analog_accel'
         125  LOAD_CONST            1  1
         128  CALL_FUNCTION_1       1 
         131  POP_TOP          
         132  JUMP_FORWARD         13  'to 148'

 984     135  LOAD_FAST             2  'vehicle'
         138  LOAD_ATTR            11  'set_analog_accel'
         141  LOAD_CONST            2  ''
         144  CALL_FUNCTION_1       1 
         147  POP_TOP          
       148_0  COME_FROM                '132'

 986     148  LOAD_GLOBAL           0  'global_data'
         151  LOAD_ATTR             3  'is_key_down'
         154  LOAD_GLOBAL           4  'game'
         157  LOAD_ATTR             9  'VK_S'
         160  CALL_FUNCTION_1       1 
         163  POP_JUMP_IF_FALSE   182  'to 182'

 987     166  LOAD_FAST             2  'vehicle'
         169  LOAD_ATTR            12  'set_analog_brake'
         172  LOAD_CONST            1  1
         175  CALL_FUNCTION_1       1 
         178  POP_TOP          
         179  JUMP_FORWARD         13  'to 195'

 989     182  LOAD_FAST             2  'vehicle'
         185  LOAD_ATTR            12  'set_analog_brake'
         188  LOAD_CONST            2  ''
         191  CALL_FUNCTION_1       1 
         194  POP_TOP          
       195_0  COME_FROM                '179'

 991     195  LOAD_GLOBAL           0  'global_data'
         198  LOAD_ATTR             3  'is_key_down'
         201  LOAD_GLOBAL           4  'game'
         204  LOAD_ATTR            13  'VK_A'
         207  CALL_FUNCTION_1       1 
         210  POP_JUMP_IF_FALSE   229  'to 229'

 992     213  LOAD_FAST             2  'vehicle'
         216  LOAD_ATTR            14  'set_analog_steer'
         219  LOAD_CONST            3  -1
         222  CALL_FUNCTION_1       1 
         225  POP_TOP          
         226  JUMP_ABSOLUTE       279  'to 279'

 993     229  LOAD_GLOBAL           0  'global_data'
         232  LOAD_ATTR             3  'is_key_down'
         235  LOAD_GLOBAL           4  'game'
         238  LOAD_ATTR            15  'VK_D'
         241  CALL_FUNCTION_1       1 
         244  POP_JUMP_IF_FALSE   263  'to 263'

 994     247  LOAD_FAST             2  'vehicle'
         250  LOAD_ATTR            14  'set_analog_steer'
         253  LOAD_CONST            1  1
         256  CALL_FUNCTION_1       1 
         259  POP_TOP          
         260  JUMP_ABSOLUTE       279  'to 279'

 996     263  LOAD_FAST             2  'vehicle'
         266  LOAD_ATTR            14  'set_analog_steer'
         269  LOAD_CONST            2  ''
         272  CALL_FUNCTION_1       1 
         275  POP_TOP          
         276  JUMP_ABSOLUTE       562  'to 562'
         279  JUMP_FORWARD        280  'to 562'

 998     282  LOAD_FAST             0  'self'
         285  LOAD_ATTR            16  'vehicle'
         288  POP_JUMP_IF_FALSE   562  'to 562'

 999     291  LOAD_FAST             0  'self'
         294  LOAD_ATTR            16  'vehicle'
         297  STORE_FAST            2  'vehicle'

1000     300  LOAD_GLOBAL          17  'getattr'
         303  LOAD_GLOBAL           4  'game'
         306  LOAD_CONST            2  ''
         309  CALL_FUNCTION_3       3 
         312  STORE_FAST            3  'force'

1001     315  LOAD_FAST             3  'force'
         318  LOAD_CONST            2  ''
         321  COMPARE_OP            4  '>'
         324  POP_JUMP_IF_FALSE   385  'to 385'

1002     327  LOAD_FAST             2  'vehicle'
         330  LOAD_ATTR            18  'set_analog_handbrake'
         333  LOAD_CONST            2  ''
         336  CALL_FUNCTION_1       1 
         339  POP_TOP          

1003     340  LOAD_FAST             2  'vehicle'
         343  LOAD_ATTR             6  'set_gear'
         346  LOAD_GLOBAL           7  'vehicle_const'
         349  LOAD_ATTR             8  'GEAR_FORWARD'
         352  CALL_FUNCTION_1       1 
         355  POP_TOP          

1004     356  LOAD_FAST             2  'vehicle'
         359  LOAD_ATTR            11  'set_analog_accel'
         362  LOAD_CONST            1  1
         365  CALL_FUNCTION_1       1 
         368  POP_TOP          

1005     369  LOAD_FAST             2  'vehicle'
         372  LOAD_ATTR            12  'set_analog_brake'
         375  LOAD_CONST            2  ''
         378  CALL_FUNCTION_1       1 
         381  POP_TOP          
         382  JUMP_ABSOLUTE       562  'to 562'

1006     385  LOAD_FAST             3  'force'
         388  LOAD_CONST            2  ''
         391  COMPARE_OP            0  '<'
         394  POP_JUMP_IF_FALSE   455  'to 455'

1007     397  LOAD_FAST             2  'vehicle'
         400  LOAD_ATTR            18  'set_analog_handbrake'
         403  LOAD_CONST            2  ''
         406  CALL_FUNCTION_1       1 
         409  POP_TOP          

1008     410  LOAD_FAST             2  'vehicle'
         413  LOAD_ATTR             6  'set_gear'
         416  LOAD_GLOBAL           7  'vehicle_const'
         419  LOAD_ATTR            10  'GEAR_REVERSE'
         422  CALL_FUNCTION_1       1 
         425  POP_TOP          

1009     426  LOAD_FAST             2  'vehicle'
         429  LOAD_ATTR            12  'set_analog_brake'
         432  LOAD_CONST            1  1
         435  CALL_FUNCTION_1       1 
         438  POP_TOP          

1010     439  LOAD_FAST             2  'vehicle'
         442  LOAD_ATTR            11  'set_analog_accel'
         445  LOAD_CONST            2  ''
         448  CALL_FUNCTION_1       1 
         451  POP_TOP          
         452  JUMP_ABSOLUTE       562  'to 562'

1012     455  LOAD_FAST             2  'vehicle'
         458  LOAD_ATTR            11  'set_analog_accel'
         461  LOAD_CONST            2  ''
         464  CALL_FUNCTION_1       1 
         467  POP_TOP          

1013     468  LOAD_FAST             2  'vehicle'
         471  LOAD_ATTR            12  'set_analog_brake'
         474  LOAD_CONST            2  ''
         477  CALL_FUNCTION_1       1 
         480  POP_TOP          

1014     481  LOAD_FAST             0  'self'
         484  LOAD_ATTR            19  'is_strong_handbrake'
         487  POP_JUMP_IF_TRUE    527  'to 527'

1015     490  LOAD_FAST             2  'vehicle'
         493  LOAD_ATTR            18  'set_analog_handbrake'
         496  LOAD_GLOBAL           0  'global_data'
         499  LOAD_ATTR            20  'brake_factor'
         502  POP_JUMP_IF_TRUE    514  'to 514'
         505  LOAD_FAST             0  'self'
         508  LOAD_ATTR            20  'brake_factor'
         511  JUMP_FORWARD          6  'to 520'
         514  LOAD_GLOBAL           0  'global_data'
         517  LOAD_ATTR            20  'brake_factor'
       520_0  COME_FROM                '511'
         520  CALL_FUNCTION_1       1 
         523  POP_TOP          
         524  JUMP_ABSOLUTE       562  'to 562'

1017     527  LOAD_FAST             2  'vehicle'
         530  LOAD_ATTR             6  'set_gear'
         533  LOAD_GLOBAL           7  'vehicle_const'
         536  LOAD_ATTR            10  'GEAR_REVERSE'
         539  CALL_FUNCTION_1       1 
         542  POP_TOP          

1018     543  LOAD_FAST             0  'self'
         546  LOAD_ATTR            16  'vehicle'
         549  LOAD_ATTR            18  'set_analog_handbrake'
         552  LOAD_CONST            1  1
         555  CALL_FUNCTION_1       1 
         558  POP_TOP          
         559  JUMP_FORWARD          0  'to 562'
       562_0  COME_FROM                '559'
       562_1  COME_FROM                '279'

1020     562  LOAD_FAST             0  'self'
         565  LOAD_ATTR            21  '_tick_user_action'
         568  CALL_FUNCTION_0       0 
         571  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 309

    def _move_stop(self):
        self.move_status = vehicle_const.MOVE_STOP
        self.last_op_info = None
        self.apply_force(0)
        self.apply_sterring(0)
        if self.vehicle:
            self.vehicle.speed = math3d.vector(0, 0, 0)
        return

    def destroy(self):
        self._enable_physics(False)
        self.unit_obj.del_com('ComVehicleMoveSyncReceiver')
        if self.vehicle:
            m = self.ev_g_model()
            if m and m.valid and self.sd.ref_logic_trans:
                w_trans = m.world_transformation
                self.sd.ref_logic_trans.yaw_target = self._nomalize_angle(w_trans.yaw)
            self.vehicle.set_position_changed_callback(None)
            self.scene.scene_col.del_interest_id(self.vehicle.cid)
        self._stop_control_vehicle()
        self.vehicle = None
        super(ComVehicleDriver2, self).destroy()
        return

    def _set_forward_yaw(self, delta):
        if self._enable_target_yaw_offset:
            return
        if self.vehicle:
            scn = self.scene
            com_camera = scn.get_com('PartCamera')
            self._target_yaw = com_camera.get_yaw()

    def _on_get_target_yaw(self):
        return self._target_yaw

    def _brake_begin(self):
        if not self.vehicle:
            return
        self.is_strong_handbrake = True
        self.vehicle.set_analog_handbrake(1)
        self._move_control(vehicle_const.MOVE_BRAKE, 0)

    def _brake_end(self):
        if not self.vehicle:
            return
        self.is_strong_handbrake = False
        self.vehicle.set_analog_handbrake(0)
        self._move_control(vehicle_const.MOVE_NO_FORCE, 0)

    def _set_target_yaw_offset(self, offset):
        if self.vehicle:
            if not self.vehicle.speed.is_zero:
                old_offset = self._target_yaw_offset
                self._target_yaw_offset = offset

    def on_enable_target_yaw_offset(self, is_enable):
        self._enable_target_yaw_offset = is_enable

    def update_camera_pitch_follow_status(self):
        scn = self.scene
        com_camera = scn.get_com('PartCamera')
        com_camera.pitch(self._diff_pitch / 30.0)

    def on_enable_camera_follow(self, is_enable):
        old_enable = self._enable_camera_follow
        self._enable_camera_follow = is_enable
        if old_enable != is_enable:
            if is_enable:
                m = self.ev_g_model()
                if not m or not m.valid:
                    return
                w_trans = m.world_transformation
                m_yaw = self._nomalize_angle(w_trans.yaw)
                scn = self.scene
                com_camera = scn.get_com('PartCamera')
                cam_model_yaw_diff = self._nomalize_angle(m_yaw - com_camera.get_yaw())
                self.additive_speed_frame = 30.0
                self.additive_speed = cam_model_yaw_diff / self.additive_speed_frame
                self.addtive_yaw = 0
                self._diff_yaw = cam_model_yaw_diff
                self._diff_pitch = self._target_pitch - com_camera.get_pitch()

    def on_switch_vehicle_ope_type(self, new_ope):
        from logic.gcommon.common_const import ui_operation_const as uoc
        scn = self.scene
        com_camera = scn.get_com('PartCamera')
        if new_ope == uoc.DRIVE_OPE_FORWARD:
            self._target_yaw = self._nomalize_angle(com_camera.get_yaw())
            self.on_enable_camera_follow(False)
            self.on_enable_target_yaw_offset(False)
        else:
            self.on_enable_camera_follow(True)
            self.on_enable_target_yaw_offset(True)

    def on_transforming_to_vehicle_in_water(self, flag):
        self._is_transforming_to_vehicle_in_water = flag
        if not flag:
            if self._last_transforming_status and self._last_transforming_force:
                self._move_control(self._last_transforming_status, self._last_transforming_force)
        self._last_transforming_status = None
        self._last_transforming_force = None
        return

    def on_vehicle_horn(self, *args):
        self.send_event('E_VEHICLE_HORN_SOUND')

    def _reset_vehicle_mat_by_model(self):
        model = self.ev_g_model()
        if not model:
            return
        mat_rot = model.rotation_matrix
        position = model.position
        if not self.vehicle:
            return
        self.vehicle.reset_position(position, mat_rot)

    def on_super_jump(self, *args):
        vehicle = self.ev_g_vehicle()
        if vehicle:
            print('super jump')
            jump_info = paragliding_const.bouncer_config['vehicle']
            cur_speed = vehicle.speed
            vehicle.speed = math3d.vector(cur_speed.x, jump_info['V_SPEED'], cur_speed.z)

    def set_vehicle_speed(self, speed):
        self._enable_physics(True, speed, math3d.vector(0, 0, 0))

    def _set_max_omega(self, factor):
        self.max_omega_factor = factor
        if not self._is_on_chongci and self.vehicle:
            self.vehicle.max_omega = self.max_omega * factor

    def _on_frozen(self, frozen, *args):
        self._is_in_frozen = frozen
        rock_info = frozen or global_data.emgr.get_is_lock.emit()
        if rock_info:
            is_run_lock = rock_info[0] if 1 else False
            if is_run_lock:
                global_data.emgr.lock_drive_ui.emit()

    def _change_character_attr(self, name, *arg):
        if name == 'dump_character':
            if self.vehicle:
                foot_position = self.get_foot_position()
                print(('test--ComVehicleDriver2.dump_character--foot_position =', foot_position, '--speed =', self.vehicle.speed, '--angular_speed =', self.vehicle.angular_speed, '--engine_speed =', self.vehicle.engine_speed))