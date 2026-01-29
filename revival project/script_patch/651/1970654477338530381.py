# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComBallDriver.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const.animation_const import BONE_BIPED_ROOT, BONE_BIPED_NAME
from logic.gutils.character_ctrl_utils import get_character_logic_height
import math3d
import collision
import time
import math
import world
import logic.gcommon.const as const
import logic.gcommon.common_utils.bcast_utils as bcast
MAX_REVERSE_SPEED = 5 * NEOX_UNIT_SCALE
MAX_REVERSE_SPEED_SQR = MAX_REVERSE_SPEED * MAX_REVERSE_SPEED
MAX_LERP = math.cos(math.radians(70))
RAIDUS_TO_ANGLE = 180 / math.pi
UP_VECTOR = math3d.vector(0, 1, 0)
DOWN_VECTOR = math3d.vector(0, -1, 0)
SPEED_QUEUE_LENGTH = 30
RUN_SPEED_BOUNDARY_VALUE = 8.0 * NEOX_UNIT_SCALE
BALL_RADIUS = 1.7 * NEOX_UNIT_SCALE
GRAVITY = 20 * NEOX_UNIT_SCALE
FRICTION_RATIO = 0.32

class ComBallDriver(UnitCom):
    BIND_EVENT = {'E_ACTIVE_BALL_DRIVER': 'active_ball_driver',
       'E_DISABLE_BALL_DRIVER': 'disable_ball_driver',
       'E_SET_BALL_MOVE_SPEED': 'set_ball_move_speed',
       'E_MOVE_BALL': 'on_move_ball',
       'E_BALL_JUMP': 'on_ball_jump',
       'E_FALL': 'on_ball_fall',
       'E_BALL_SYNC_TRANSFORM': 'sync_ball_transform',
       'E_BALL_CHECK_DAMAGE': 'check_can_damage',
       'E_BALL_IS_DASH': 'on_ball_dash',
       'E_IMMOBILIZED': 'on_ball_immobilized',
       'E_ON_FROZEN': 'on_ball_immobilized',
       'G_BALL_CAN_DAMAGE': 'on_get_ball_can_damage',
       'G_BALL_ACTIVE': 'on_get_ball_state_active',
       'G_BALL_AVG_SPEED': 'on_ball_avg_speed',
       'G_BALL_FALL_GRAVITY': 'on_get_ball_gravity',
       'G_AGL_SPD': '_get_agl_spd',
       'G_ROT_MATRIX': '_get_rot_mat',
       'E_ENABLE_MULTIJUMP': 'enable_multiple_jump'
       }
    BALL_FORCE_OFFSET = None
    CHARACTER_HEIGHT = 78.0

    def __init__(self):
        super(ComBallDriver, self).__init__()
        self.last_jump_time = 0
        self.on_ground = True
        self.ground_normal = UP_VECTOR
        self.ground_pos = math3d.vector(0, 0, 0)
        self.ground_dist = 0
        self.sd.ref_is_ball_mode = False
        self.speed_queue = [ 0.0 for i in range(SPEED_QUEUE_LENGTH) ]
        self.speed_sum = 0.0
        self.speed_queue_head = 0
        self.acc_speed = 40 * NEOX_UNIT_SCALE
        self.air_acc_coe = 0.2
        self.move_speed = 20 * NEOX_UNIT_SCALE
        self.dash_speed = 25 * NEOX_UNIT_SCALE
        self.damage_speed = 15 * NEOX_UNIT_SCALE
        self.max_speed = self.move_speed
        self.fall_gravity = 80 * NEOX_UNIT_SCALE
        self.max_fall_speed = -100 * NEOX_UNIT_SCALE
        self.agl_spd = None
        self.ball_is_dash = False
        self.last_ball_dash_hit_time = 0
        self.immobilized = False
        self.sd.ref_cur_rotation_matrix = math3d.matrix.make_orient(math3d.vector(0, 0, 1), UP_VECTOR)
        self.can_damage = False
        self.last_ground_sfx_time = 0
        self.last_ground_sfx_pos = math3d.vector(0, 0, 0)
        self.cur_jump_count = 0
        self.max_continual_jump_count = 1
        self.is_running = False
        if self.BALL_FORCE_OFFSET is None:
            from common.cfg import confmgr
            physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content', str(8012))
            self.CHARACTER_HEIGHT = physic_conf['character_size'][1] * NEOX_UNIT_SCALE
            self.BALL_FORCE_OFFSET = -self.CHARACTER_HEIGHT / 2
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBallDriver, self).init_from_dict(unit_obj, bdict)
        self.detect_col = collision.col_object(collision.SPHERE, math3d.vector(BALL_RADIUS - 1, BALL_RADIUS - 1, BALL_RADIUS - 1), 0, 0)

    def destroy(self):
        self.sd.ref_is_ball_mode = False
        self.detect_col = None
        super(ComBallDriver, self).destroy()
        return

    def on_get_ball_can_damage(self):
        return self.can_damage

    def on_get_ball_state_active(self):
        return self.sd.ref_is_ball_mode

    def _get_agl_spd(self):
        return self.agl_spd

    def _get_rot_mat(self):
        return self.sd.ref_cur_rotation_matrix

    def active_ball_driver(self, fall_gravity, move_speed, acc_speed, air_acc_coe, damage_speed):
        self.fall_gravity = fall_gravity
        self.move_speed = move_speed
        self.acc_speed = acc_speed
        self.air_acc_coe = air_acc_coe
        self.damage_speed = damage_speed
        self.can_damage = False
        self.sd.ref_is_ball_mode = True
        self.cur_jump_count = self.sd.ref_cur_jump_count
        self.send_event('E_REBIND_SHOOT_COL', BONE_BIPED_ROOT)
        self.send_event('E_FORBID_ROTATION', True)
        self.sd.ref_cur_rotation_matrix = math3d.matrix.make_orient(self.ev_g_forward(), UP_VECTOR)
        rot = math3d.matrix_to_rotation(self.sd.ref_cur_rotation_matrix)
        self.send_event('E_ROTATION', rot)
        self.detect_ground()
        self.check_can_damage()
        self.send_event('E_ACTION_SYNC_CLEAR')
        self.send_event('E_ACTION_SYNC_CLEAR_EULER')
        euler = math3d.rotation_to_euler(math3d.matrix_to_rotation(self.sd.ref_cur_rotation_matrix))
        self.send_event('E_ACTION_SYNC_EULER', euler.x, euler.y, euler.z)
        self.send_event('E_TRANS_TO_BALL_FINISH', True)
        self.send_event('E_SHOW_LIGHT', False)
        self.send_event('E_CLEAR_ACC_INFO')
        cur_foot_position = self.ev_g_foot_position()
        self.send_event('E_HEIGHT', 0.1)
        self.send_event('E_REFRESH_CHARACTER_Y_OFFSET', self.BALL_FORCE_OFFSET)
        self.send_event('E_FOOT_POSITION', cur_foot_position)

    def disable_ball_driver(self):
        self.sd.ref_is_ball_mode = False
        self.sd.ref_cur_jump_count = self.cur_jump_count
        self.speed_queue = [ 0.0 for i in range(SPEED_QUEUE_LENGTH) ]
        self.speed_queue_head = 0
        self.speed_sum = 0.0
        self.send_event('E_REBIND_SHOOT_COL', BONE_BIPED_NAME)
        self.send_event('E_FORBID_ROTATION', False)
        self.send_event('E_CLEAR_BALL_SFX')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 2, ('m_8012_sprint_loop', 'nf'), 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (0, ('m_8012_sprint_loop', 'nf'), 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 2, ('m_8012_sprint_loop_high',
                                                            'nf'), 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (0, ('m_8012_sprint_loop_high', 'nf'), 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
        self.send_event('E_ACTION_SYNC_CLEAR')
        self.send_event('E_ACTION_SYNC_CLEAR_EULER')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_ACTION_SYNC_RC_RESUME_ROLL, ()))
        self.send_event('E_CLEAR_ACC_INFO')
        self.send_event('E_HEIGHT', get_character_logic_height(self.sd.ref_character, self.CHARACTER_HEIGHT))
        self.send_event('E_REFRESH_CHARACTER_Y_OFFSET')

    def detect_ground(self):
        on_ground = self.ev_g_on_ground()
        if not self.on_ground and on_ground:
            self.cur_jump_count = 0
        self.on_ground = on_ground
        ball_center_pos = self.ev_g_position()
        ground_pos = ball_center_pos - math3d.vector(0, BALL_RADIUS, 0)
        ret = self.scene.scene_col.sweep_test(self.detect_col, ball_center_pos, ground_pos, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, 0, collision.INCLUDE_FILTER)
        if ret[0]:
            is_unit_obj = global_data.emgr.scene_find_unit_event.emit(ret[5].cid)[0]
            if ret[3] > 0.0 or is_unit_obj:
                self.ground_normal = ret[2]
        if self.on_ground and time.time() - self.last_ground_sfx_time > 0.15 and self.sd.ref_cur_speed > 1:
            delta = ground_pos - self.last_ground_sfx_pos
            delta.y = 0
            if delta.length < 1:
                return
            normal = self.ground_normal
            self.send_event('E_SHOW_BALL_GROUND_SFX', (ground_pos.x, ground_pos.y, ground_pos.z), (normal.x, normal.y, normal.z))
            self.last_ground_sfx_time = time.time()
            self.last_ground_sfx_pos = ground_pos

    def on_move_ball(self, move_dir, dt):
        self.max_speed = self.move_speed
        cur_v = self.ev_g_char_walk_direction()
        if not cur_v:
            return
        else:
            self.detect_ground()
            cur_v = math3d.vector(cur_v.x, 0, cur_v.z)
            cur_dir = math3d.vector(cur_v)
            if not cur_dir.is_zero:
                cur_dir.normalize()
            if self.on_ground:
                acc_speed = self.acc_speed
            else:
                acc_speed = self.acc_speed * self.air_acc_coe
            if not move_dir or move_dir.is_zero or self.immobilized:
                if self.on_ground:
                    opposite_normal = -self.ground_normal
                    pressure_value = DOWN_VECTOR.dot(opposite_normal)
                    pressure_dir = opposite_normal * pressure_value
                    gravity_move_dir = DOWN_VECTOR - pressure_dir
                    hor_gravity_move_dir = math3d.vector(gravity_move_dir.x, 0, gravity_move_dir.z)
                    hor_gravity_v = hor_gravity_move_dir * GRAVITY * dt
                    friction_v = pressure_value * FRICTION_RATIO * GRAVITY * dt
                    cur_v.is_zero or cur_v += hor_gravity_v
                    if cur_v.length > friction_v:
                        new_move_dir = math3d.vector(cur_v)
                        new_move_dir.normalize()
                        cur_v -= new_move_dir * friction_v
                    else:
                        cur_v = math3d.vector(0, 0, 0)
                elif pressure_value * FRICTION_RATIO < hor_gravity_move_dir.length:
                    cur_v = hor_gravity_v - hor_gravity_move_dir * friction_v
            else:
                if self.immobilized:
                    acc_speed = self.acc_speed
                if not cur_v.is_zero:
                    if cur_v.length < acc_speed * dt:
                        cur_v = math3d.vector(0, 0, 0)
                    else:
                        cur_v -= cur_dir * acc_speed * dt
                        if abs(cur_v.length) < 0.1:
                            cur_v = math3d.vector(0, 0, 0)
            if self.immobilized or cur_v.is_zero:
                speed_vec = math3d.vector(0, 0, 0) if 1 else cur_v
                final_v = speed_vec
            else:
                yaw = self.ev_g_yaw() or 0
                forward = math3d.matrix.make_rotation_y(yaw).forward
                right = UP_VECTOR.cross(forward)
                if not move_dir or move_dir.is_zero:
                    move_dir = math3d.vector(0, 0, 1)
                move_dir = forward * move_dir.z + right * move_dir.x
                cur_v += move_dir * acc_speed * dt
                if cur_v.length > self.max_speed:
                    cur_v.normalize()
                    cur_v *= self.max_speed
                final_v = cur_v
            cur_speed = final_v.length
            self.speed_sum -= self.speed_queue[self.speed_queue_head]
            self.speed_queue[self.speed_queue_head] = cur_speed
            self.speed_queue_head += 1
            if self.speed_queue_head >= SPEED_QUEUE_LENGTH:
                self.speed_queue_head = 0
            self.speed_sum += cur_speed
            self.sd.ref_cur_speed = cur_speed
            self.send_event('E_CHARACTER_WALK', final_v)
            if cur_speed > 0:
                cur_dir = math3d.vector(final_v)
                cur_dir.normalize()
                right = UP_VECTOR.cross(cur_dir)
                rot = math3d.rotation(0, 0, 0, 1)
                rot.set_axis_angle(right, dt * cur_speed / BALL_RADIUS)
                cur_rot = math3d.matrix_to_rotation(self.sd.ref_cur_rotation_matrix)
                cur_rot = rot * cur_rot
                if dt > 0:
                    self.agl_spd = math3d.rotation_to_euler(rot) * (1 / dt)
                self.sd.ref_cur_rotation_matrix = math3d.rotation_to_matrix(cur_rot)
            else:
                self.agl_spd = math3d.vector(0, 0, 0)
            self.sync_ball_transform()
            self.check_can_damage()
            if self.is_running and cur_speed < RUN_SPEED_BOUNDARY_VALUE:
                self.is_running = False
                sound_name = ('m_8012_sprint_loop', 'nf')
                self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 1, 2, const.SOUND_TYPE_MECHA_FOOTSTEP)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 1, 2, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
                sound_name = ('m_8012_sprint_loop_high', 'nf')
                self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, sound_name, 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (0, sound_name, 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
            elif not self.is_running and cur_speed > RUN_SPEED_BOUNDARY_VALUE:
                self.is_running = True
                sound_name = ('m_8012_sprint_loop', 'nf')
                self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, sound_name, 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (0, sound_name, 0, 1, 0, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
                sound_name = ('m_8012_sprint_loop_high', 'nf')
                self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 1, 2, const.SOUND_TYPE_MECHA_FOOTSTEP)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 1, 2, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
                sound_name = ('m_8012_sprint_roll_start', 'nf')
                self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, None, const.SOUND_TYPE_MECHA_FOOTSTEP)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, None, const.SOUND_TYPE_MECHA_FOOTSTEP)], True)
            return

    def sync_ball_transform(self):
        rot = math3d.matrix_to_rotation(self.sd.ref_cur_rotation_matrix)
        self.send_event('E_ROTATION', rot)
        euler = math3d.rotation_to_euler(rot)
        self.send_event('E_ACTION_SYNC_EULER', euler.x, euler.y, euler.z)

    def check_can_damage(self, force_damage=False):
        can_damage = self.speed_sum / len(self.speed_queue) >= self.damage_speed or force_damage
        if self.can_damage != can_damage:
            self.send_event('E_BALL_CAN_DAMAGE', can_damage)
        self.can_damage = can_damage

    def on_ball_jump(self, jump_speed, jump_gravity, cam_fllow_speed, cam_recover_delay, cam_recover_time, skill_id=None):
        if self.ball_is_dash:
            return
        cur_jump_time = time.time()
        if cur_jump_time - self.last_jump_time > 0.4:
            new_jump_count = self.cur_jump_count
            if not self.on_ground:
                if self.cur_jump_count == 0:
                    new_jump_count = 1
                if new_jump_count >= self.max_continual_jump_count:
                    return
            self.on_ground = False
            self.cur_jump_count = new_jump_count + 1
            self.send_event('E_GRAVITY', jump_gravity)
            self.send_event('E_JUMP', jump_speed)
            self.last_jump_time = cur_jump_time
            self.send_event('E_SET_CAMERA_FOLLOW_SPEED', True, cam_fllow_speed, cam_recover_delay, cam_recover_time)
            if skill_id:
                self.send_event('E_DO_SKILL', skill_id)

    def on_ball_fall(self, *args):
        if self.sd.ref_is_ball_mode:
            self.send_event('E_GRAVITY', self.fall_gravity)

    def on_ball_avg_speed(self):
        return self.speed_sum / len(self.speed_queue)

    def on_get_ball_gravity(self):
        return self.fall_gravity

    def on_ball_dash(self, is_dash, *args):
        if is_dash:
            self.on_ground = False
        else:
            self.detect_ground()
            self.is_running = False
        self.ball_is_dash = is_dash

    def on_ball_immobilized(self, immobilized, *args):
        self.immobilized = immobilized

    def set_ball_move_speed(self, move_speed):
        self.move_speed = move_speed

    def enable_multiple_jump(self, enabled):
        self.max_continual_jump_count += 1 if enabled else -1
        if self.max_continual_jump_count < 1:
            self.extra_continual_jump_count = 1