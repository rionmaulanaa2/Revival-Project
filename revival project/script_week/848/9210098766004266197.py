# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8016.py
from __future__ import absolute_import
import math3d
import world
import math
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.cdata import jump_physic_config
from .StateBase import StateBase
from .MoveLogic import Walk
from .JumpLogic import JumpUpPure, FallPure, OnGroundPure, SuperJumpUpPure
from .Logic8009 import Run8009
from common.utils import timer
from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.skill.client.SkillSecWeapon8016 import get_hit_target, get_fire_end
import logic.gcommon.const as g_const
from logic.gcommon.common_const import attr_const
from logic.gcommon.common_const import skill_const
from logic.gcommon.behavior.StateBase import clamp
from logic.vscene.parts import PartCtrl
from logic.gcommon import editor
import time
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_7
from logic.gutils.mecha_utils import do_hit_phantom
TURN_FORWARD = 0
TURN_LEFT = 1
TURN_RIGHT = 2
DEFAULT_CAM_STATE = '79'
CAM_STATE_DASH_START = '88'
CAM_STATE_DASH = '81'
CAM_STATE_DASH_STOP = '89'
CAM_STATE_DASH_SHOOT = '84'
CAM_STATE_DASH_SHOOT_TURN = '90'
CAM_STATE_BLAST_END = '87'
CAM_STATE_AIM_SHOOT = '86'
CAM_STATE_AIM_SHOOT_POST = '97'

def get_cur_turn_dir(move_dir):
    rot = global_data.game_mgr.scene.active_camera.rotation_matrix
    forward = rot.forward
    forward.normalize()
    right = math3d.vector(0, 1, 0).cross(forward)
    w_dot_f = move_dir.dot(forward)
    w_dot_r = move_dir.dot(right)
    if w_dot_f > 0:
        return TURN_FORWARD
    else:
        if w_dot_r < 0:
            return TURN_RIGHT
        return TURN_LEFT


def recoil_force(self, direction, max_force=5.0, recoil_time=0.3):
    self.applied_time = 0
    recoil_force_dir = math3d.vector(direction.x, 0, direction.z)
    recoil_force_dir.normalize()

    def apply_force(dt):
        if self and self.is_valid() and not self.ev_g_death():
            self.applied_time += dt
            if self.applied_time >= recoil_time:
                self.applied_time = recoil_time
            u = self.applied_time / recoil_time
            force = (math.cos(u * math.pi) + 1) * max_force * NEOX_UNIT_SCALE
            walk_direction = self.ev_g_char_walk_direction() or math3d.vector(0, 0, 0)
            delta_force = recoil_force_dir * math3d.vector(force, 0, force)
            walk_direction += delta_force
            self.sd.ref_character.setWalkDirection(walk_direction)
            if u == 1:
                return timer.RELEASE

    global_data.game_mgr.get_post_logic_timer().register(func=apply_force, interval=1, timedelta=True)


def process_move_tilt(self, tilt_coe):
    delta_yaw = abs(self.sd.ref_yaw / 5.0)
    if self.sd.ref_yaw < 0:
        self.sd.ref_yaw += delta_yaw * 4
    elif self.sd.ref_yaw > 0:
        self.sd.ref_yaw -= delta_yaw * 3
    if abs(self.sd.ref_yaw) < 0.001:
        self.sd.ref_yaw = 0
    dir_x = self.sd.ref_yaw * tilt_coe
    self.send_event('E_CHANGE_ANIM_MOVE_DIR', dir_x, 0.3)


def change_state(self):
    if not self or not self.is_valid():
        return
    WEAPON_STATES = [
     MC_SHOOT, MC_AIM_SHOOT]
    state_idx = 1 if self.sd.ref_cur_shoot_state == MC_SHOOT else 0
    self.send_event('E_SWITCH_ACTION', 'action1', WEAPON_STATES[state_idx], state_idx == 0)
    self.send_event('E_SWITCH_ACTION', 'action2', WEAPON_STATES[state_idx], state_idx == 0)
    self.send_event('E_SWITCH_ACTION', 'action3', WEAPON_STATES[state_idx], state_idx == 0)
    self.sd.ref_cur_shoot_state = WEAPON_STATES[state_idx]
    self.send_event('E_SWITCH_BIND_WEAPON_CUR_POS', 0, state_idx + 1)
    self.send_event('E_SHOW_MAIN_ACC_IDLE_EFFECT', state_idx == 1, True)
    icon = 'gui/ui_res_2/battle/mech_main/mech_charge_shoot_8016.png' if state_idx == 1 else 'gui/ui_res_2/battle/mech_main/icon_mech8016_1.png'
    self.send_event('E_SET_ACTION_ICON', 'action1', icon, 'show')
    self.send_event('E_SET_ACTION_ICON', 'action2', icon, 'show')
    self.send_event('E_SET_ACTION_ICON', 'action3', icon, 'show')


class Move8016(Walk):
    BIND_EVENT = Walk.BIND_EVENT.copy()
    BIND_EVENT.update({})

    def read_data_from_custom_param(self):
        super(Move8016, self).read_data_from_custom_param()
        self.tick_interval = 0.01

    def update(self, dt):
        super(Move8016, self).update(dt)


@editor.state_exporter({('tilt_coe', 'param'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe8\xbd\xac\xe8\xba\xab\xe7\x9a\x84\xe4\xbe\xa7\xe8\xba\xab\xe7\xb3\xbb\xe6\x95\xb0','min_val': 0,'max_val': 10}})
class Run8016(Run8009):

    def read_data_from_custom_param(self):
        super(Run8016, self).read_data_from_custom_param()
        self.tilt_coe = self.custom_param.get('tilt_coe', 5) * 1.0

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Run8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.sd.ref_yaw = 0

    def update(self, dt):
        super(Run8016, self).update(dt)
        if self.sd.ref_mecha_free_sight_mode_enabled:
            process_move_tilt(self, self.tilt_coe)

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_state_running_time_stamp < self.stop_anim_cost_time:
            return
        super(Run8009, self).begin_run_stop_anim()

    def check_transitions(self):
        if self.brakeing:
            self.send_event('E_CLEAR_SPEED')
            return self.STAND_STATE
        if self.slow_down:
            return self.MOVE_STATE
        cur_speed = self.sd.ref_cur_speed
        walk_speed = self.ev_g_get_speed_scale() * self.walk_speed
        if cur_speed < walk_speed:
            if not self.show_stop_anim or self.sd.ref_rocker_dir:
                return self.MOVE_STATE
        if cur_speed <= 0.0 and self.sd.ref_low_body_anim != self.run_stop_anim:
            return self.STAND_STATE
        if self.stop_break_time and self.sub_state == self.STATE_STOP and self.sd.ref_rocker_dir and self.sub_sid_timer > self.stop_break_time:
            return self.MOVE_STATE


class ChangeWeaponState(StateBase):
    WEAPON_STATES = [
     MC_SHOOT, MC_AIM_SHOOT]
    STATE_NONE = 0
    STATE_CHANING = 1
    STATE_COMPLETE = 2
    BIND_EVENT = {'G_IS_MAIN_ACC_MODE': 'on_main_acc_mode'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ChangeWeaponState, self).init_from_dict(unit_obj, bdict, sid, info)
        self.refresh_sub_state_callback()
        self.change_time = self.custom_param.get('change_time', 1.0)
        self.state_idx = 0
        self.sd.ref_cur_shoot_state = self.WEAPON_STATES[self.state_idx]
        self.anim_name = 'change_mode'

    def on_main_acc_mode(self):
        return self.state_idx == 1

    def on_post_init_complete(self, bdict):
        super(ChangeWeaponState, self).on_post_init_complete(bdict)

    def refresh_sub_state_callback(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_COMPLETE, 0, self.change_state)

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        return self.active_self()

    def enter(self, leave_states):
        super(ChangeWeaponState, self).enter(leave_states)
        self.sub_state = self.STATE_CHANING
        self.send_event('E_POST_ACTION', self.anim_name, UP_BODY, 1, timeScale=1.0)
        sound_clip = 'm_8016_weapon2_to_single' if self.on_main_acc_mode() else 'm_8016_weapon2_to_hold'
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, (sound_clip, 'nf'), 0, 0, 1, 6)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (0, (sound_clip, 'nf'), 0, 0, 1, 6)], True)

    def update(self, dt):
        super(ChangeWeaponState, self).update(dt)
        if self.elapsed_time > self.change_time:
            self.sub_state = self.STATE_COMPLETE

    def exit(self, enter_states):
        super(ChangeWeaponState, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')

    def change_state(self):
        self.state_idx += 1
        if self.state_idx >= len(self.WEAPON_STATES):
            self.state_idx = 0
        self.send_event('E_SWITCH_ACTION', 'action1', self.WEAPON_STATES[self.state_idx], False)
        self.send_event('E_SWITCH_ACTION', 'action2', self.WEAPON_STATES[self.state_idx], False)
        self.send_event('E_SWITCH_ACTION', 'action3', self.WEAPON_STATES[self.state_idx], False)
        self.sub_state = self.STATE_NONE
        self.disable_self()
        self.sd.ref_cur_shoot_state = self.WEAPON_STATES[self.state_idx]
        self.send_event('E_SWITCH_BIND_WEAPON_CUR_POS', 0, self.state_idx + 1)
        self.send_event('E_SHOW_MAIN_ACC_IDLE_EFFECT', self.on_main_acc_mode(), True)
        icon = 'gui/ui_res_2/battle/mech_main/mech_charge_shoot_8016.png' if self.on_main_acc_mode() else 'gui/ui_res_2/battle/mech_main/icon_mech8016_1.png'
        self.send_event('E_SET_ACTION_ICON', 'action1', icon, 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', icon, 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', icon, 'show')


class AimIKBase(StateBase):
    NONE_STATE = -1
    PRE_STATE = 0
    HOLD_STATE = 1
    POST_STATE = 2
    BIND_EVENT = {'E_SWITCH_TO_AIR_SHOOT': 'on_switch_to_air_shoot'
       }

    def refresh_sub_state_callback(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.PRE_STATE, self.pre_time, self.pre_end)
        self.register_substate_callback(self.POST_STATE, 0, self.post_start)
        self.register_substate_callback(self.POST_STATE, self.post_time, self.shoot_end)

    def on_post_init_complete(self, *args):
        super(AimIKBase, self).on_post_init_complete(*args)

    def read_data_from_custom_param(self):
        self.sub_state = self.NONE_STATE
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.pre_time = self.custom_param.get('pre_time', 0.3)
        self.post_time = self.custom_param.get('post_time', 0.2)
        self.is_air_shoot = False
        return

    def enter(self, leave_states):
        super(AimIKBase, self).enter(leave_states)
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False, max_lerp_duration=0.2)
        self.pre_start()

    def update(self, dt):
        super(AimIKBase, self).update(dt)
        rot = self.sd.ref_effective_camera_rot or math3d.matrix_to_rotation(global_data.game_mgr.scene.active_camera.rotation_matrix)
        cur_pitch = rot.get_forward().pitch
        enable_aim_ik = cur_pitch > 0 and self.ev_g_on_ground()
        if not self.last_enable_aim_ik and enable_aim_ik:
            self.send_event('E_ENABLE_TWIST_PITCH', True)
            self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.1)
        elif self.last_enable_aim_ik and not enable_aim_ik:
            self.send_event('E_ENABLE_TWIST_PITCH', False)
            self.send_event('E_SOFT_ENTER_PITCH_MODEL', 0.1)
        self.last_enable_aim_ik = enable_aim_ik

    def exit(self, enter_states):
        super(AimIKBase, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_ENABLE_TWIST_PITCH', False)
        self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.2)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.sub_state = self.NONE_STATE
        return

    def pre_start(self):
        if self.shoot_aim_ik:
            self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, True)
            self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.post_time)
        rot = self.sd.ref_effective_camera_rot or math3d.matrix_to_rotation(global_data.game_mgr.scene.active_camera.rotation_matrix)
        self.last_enable_aim_ik = rot.get_forward().pitch > 0 and self.ev_g_on_ground()
        if self.last_enable_aim_ik:
            self.send_event('E_ENABLE_TWIST_PITCH', True)
            self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.1)
        else:
            self.send_event('E_ENABLE_TWIST_PITCH', False)
            self.send_event('E_SOFT_ENTER_PITCH_MODEL', 0.1)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.normal_aim_anim[0], loop=True, blend_dir=8)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.normal_aim_anim[0], loop=True)

    def pre_end(self):
        pass

    def post_start(self):
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)

    def shoot_end(self):
        self.disable_self()

    def on_switch_to_air_shoot(self, is_air_shoot):
        self.is_air_shoot = is_air_shoot
        self.cur_aim_anim = self.air_aim_anim if is_air_shoot else self.normal_aim_anim
        self.cur_shoot_anim = self.air_shoot_anim if is_air_shoot else self.normal_shoot_anim
        if self.is_active:
            self.play_aim_anim()

    def play_aim_anim(self):
        if self.is_air_shoot:
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        clip_name, part, blend_dir, kwargs = self.cur_aim_anim
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, blend_dir, **kwargs)
        if part == LOW_BODY:
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, blend_dir, **kwargs)

    def play_shoot_anim(self):
        clip_name, part, blend_dir, kwargs = self.cur_shoot_anim
        self.send_event('E_SET_SMOOTH_SPEED', LOW_BODY, 0)
        self.send_event('E_SET_SMOOTH_SPEED', UP_BODY, 0)
        kwargs['force_trigger_effect'] = True
        self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)
        if part == UP_BODY and self.ev_g_on_ground() and not self.ev_g_get_state(MC_JUMP_3):
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        if part == LOW_BODY:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if not self.sd.ref_rocker_dir:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)


@editor.state_exporter({('pre_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x89\x8d\xe6\x91\x87','min_val': 0.2,'max_val': 1,'setter': lambda self, v: self.setter(v)
                           },
   ('hold_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe6\x9e\xaa\xe5\x90\x8e\xe7\x9a\x84\xe6\x8c\x81\xe6\x9e\xaa\xe6\x97\xb6\xe9\x97\xb4','min_val': 1,'max_val': 5}})
class WeaponFire8016(AimIKBase):
    BIND_EVENT = AimIKBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_FIRE': 'on_fire',
       'TRY_STOP_WEAPON_ATTACK': 'on_end_shoot'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.refresh_sub_state_callback()
        self.idle_time = 0
        self.btn_hold = False

    def check_can_active(self, only_avatar=True):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not weapon:
            return False
        return self.ev_g_status_check_pass(self.sid, only_avatar=only_avatar)

    def action_btn_down(self):
        super(WeaponFire8016, self).action_btn_down()
        self.btn_hold = True
        if self.sub_state >= self.HOLD_STATE:
            self.ev_g_try_weapon_attack_begin(self.weapon_pos)
            return
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            return False
        if self.sub_state != self.NONE_STATE:
            return
        if self.ev_g_combo_shoot():
            self.send_event('E_COMBO_SHOOT')
            return
        if self.check_can_active():
            self.active_self()

    def action_btn_up(self):
        self.btn_hold = False
        super(WeaponFire8016, self).action_btn_up()
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def pre_end(self):
        self.sub_state = self.HOLD_STATE
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)

    def post_start(self):
        super(WeaponFire8016, self).post_start()

    def enter(self, leave_states):
        super(WeaponFire8016, self).enter(leave_states)
        self.sub_state = self.PRE_STATE
        self.idle_time = 0
        self.play_aim_anim()

    def exit(self, enter_states):
        super(WeaponFire8016, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def update(self, dt):
        super(WeaponFire8016, self).update(dt)
        if self.sub_state == self.HOLD_STATE:
            self.idle_time += dt
            if not self.btn_hold:
                self.ev_g_try_weapon_attack_end(self.weapon_pos)
                if self.idle_time >= self.hold_time:
                    self.sub_state = self.POST_STATE

    def destroy(self):
        super(WeaponFire8016, self).destroy()

    def read_data_from_custom_param(self):
        self.tick_interval = 0.03
        super(WeaponFire8016, self).read_data_from_custom_param()
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.hold_time = self.custom_param.get('hold_time', 2.0) * 1.0
        self.fire_interval = self.custom_param.get('fire_interval', 0.5) * 1.0
        self.normal_aim_anim = (
         'aim', UP_BODY, 9, {'blend_time': 0.2,'loop': True,'timeScale': 1.0})
        self.normal_shoot_anim = ('shoot', UP_BODY, 9, {'blend_time': 0,'timeScale': 1.5})
        self.air_aim_anim = (
         'jump_aim', UP_BODY, 1, {'blend_time': 0.2,'loop': True,'timeScale': 1.0})
        self.air_shoot_anim = ('jump_shoot', UP_BODY, 1, {'blend_time': 0,'timeScale': 1.0})
        self.cur_aim_anim = self.normal_aim_anim
        self.cur_shoot_anim = self.normal_shoot_anim

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        if weapon_pos != self.weapon_pos:
            return
        if self.ev_g_get_state(MC_FLIGHT_BOOST):
            return
        if not self.is_active and not self.check_can_active():
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.play_shoot_anim()
        self.idle_time = 0

    def on_end_shoot(self, *args):
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        self.disable_self()

    def setter(self, v):
        self.pre_time = v
        self.refresh_sub_state_callback()


@editor.state_exporter({('pre_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x89\x8d\xe6\x91\x87','min_val': 0.2,'max_val': 1,'setter': lambda self, v: self.setter(v)
                           },
   ('acc_time', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe9\x97\xb4'},('reinforce_speed', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x90\x8e\xe5\x9d\x90\xe5\x8a\x9b','min_val': 1,'max_val': 15},('acc_spread_speed', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x95\xa3\xe5\xb8\x83\xe8\xa1\xb0\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6','min_val': 0.5,'max_val': 8}})
class AccumulateFire8016(AimIKBase):
    BIND_EVENT = AimIKBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_FIRE': 'on_fire',
       'E_SET_ACC_SHOOT': 'on_acc_shoot'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateFire8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.refresh_sub_state_callback()
        self.btn_hold = False
        self.post_before_exit = False
        self.start_acc_time = 0
        self.acc_shoot_id = 0
        self.acc_shoot_activated = False

    def setter(self, v):
        self.pre_time = v
        self.refresh_sub_state_callback()

    def action_btn_down(self):
        super(AccumulateFire8016, self).action_btn_down()
        if self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos).get_bullet_num() <= 1:
            self.send_event('E_TRY_RELOAD', self.weapon_pos)
            return
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            return False
        if self.sub_state != self.NONE_STATE:
            return
        if self.check_can_active():
            self.active_self()

    def action_btn_up(self):
        super(AccumulateFire8016, self).action_btn_up()
        self.btn_hold = False
        if self.sub_state == self.HOLD_STATE:
            self.sub_state = self.POST_STATE

    def enter(self, leave_states):
        super(AccumulateFire8016, self).enter(leave_states)
        if MC_FLIGHT_BOOST in leave_states:
            self.pre_end()
        else:
            self.sub_state = self.PRE_STATE
        self.post_before_exit = False
        self.start_acc_time = get_server_time()
        self.play_aim_anim()
        self.start_spread_base, _, _ = self.ev_g_spread_values()
        self.send_event('E_ACC_FIRE_BEGIN')
        self.enter_high_priority_camera(CAM_STATE_AIM_SHOOT)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)

    def exit(self, enter_states):
        super(AccumulateFire8016, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_CLEAR_SPREAD_OVERRIDE')
        self.exit_high_priority_camera()
        self.enter_camera(DEFAULT_CAM_STATE)
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.clear_acc_shoot()

    def update(self, dt):
        super(AccumulateFire8016, self).update(dt)
        if self.btn_hold and self.sub_state == self.HOLD_STATE:
            self.start_spread_base -= dt * self.acc_spread_speed
            if self.start_spread_base < 0:
                self.start_spread_base = 0 if 1 else self.start_spread_base
                self.send_event('E_OVERRIDE_SPREAD_BASE', self.sid, self.start_spread_base)
                self.send_event('E_REFRESH_SPREAD_AIM_UI')
            if not self.btn_hold and self.sub_state == self.HOLD_STATE:
                self.sub_state = self.POST_STATE
            if self.sub_state == self.POST_STATE and self.post_before_exit and self.btn_hold:
                self.sub_state = self.PRE_STATE
                self.pre_start()
                self.play_aim_anim()
                self.post_before_exit = False
                self.send_event('E_ACC_FIRE_BEGIN')
                self.enter_high_priority_camera(CAM_STATE_AIM_SHOOT)
                self.start_acc_time = get_server_time()

    def destroy(self):
        super(AccumulateFire8016, self).destroy()

    def read_data_from_custom_param(self):
        super(AccumulateFire8016, self).read_data_from_custom_param()
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN2)
        self.normal_aim_anim = (
         'aim_charge', UP_BODY, 7, {'blend_time': 0.2,'loop': True,'timeScale': 1.0})
        self.normal_shoot_anim = ('shoot_charge', UP_BODY, 7, {'blend_time': 0,'timeScale': 1.0})
        self.air_aim_anim = (
         'jump_change', UP_BODY, 1, {'blend_time': 0.2,'loop': True,'timeScale': 1.0})
        self.air_shoot_anim = ('shoot_charge_fl', UP_BODY, 1, {'blend_time': 0,'timeScale': 1.0})
        self.cur_aim_anim = self.normal_aim_anim
        self.cur_shoot_anim = self.normal_shoot_anim
        self.reinforce_speed = self.custom_param.get('reinforce_speed', 10) * 1.0
        self.acc_time = self.custom_param.get('acc_time', 3) * 1.0
        self.sd.ref_8016_acc_fire_time = self.acc_time
        self.acc_spread_speed = self.custom_param.get('acc_spread_speed', 2) * 1.0
        self.max_camera_rotate_val = self.custom_param.get('max_camera_rotate_val', 1.0) * 1.0

    def pre_end(self):
        self.sub_state = self.HOLD_STATE
        self.ev_g_try_weapon_attack_begin(self.weapon_pos, True)

    def post_start(self):
        super(AccumulateFire8016, self).post_start()
        self.play_shoot_anim()
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        self.send_event('E_ACC_FIRE_END')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.exit_high_priority_camera()
        self.enter_camera(CAM_STATE_AIM_SHOOT_POST)
        self.sound_custom_start()
        self.sound_custom_end()
        self.clear_acc_shoot()
        return

    def check_pre_break(self):
        self.post_before_exit = True
        if not self.btn_hold:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.2)
            self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT}, self.sid)

    def play_shoot_anim(self):
        super(AccumulateFire8016, self).play_shoot_anim()
        self.delay_call(0.5, self.check_pre_break)
        acc_percent = get_server_time() - self.start_acc_time
        acc_percent = 0.1 if acc_percent < 0.1 else acc_percent
        acc_percent = 1 if acc_percent > 1 else acc_percent
        recoil_force(self, -global_data.game_mgr.scene.active_camera.rotation_matrix.forward, max_force=self.reinforce_speed * acc_percent, recoil_time=0.6)
        self.send_event('E_CLEAR_SPREAD_OVERRIDE')
        self.send_event('E_REFRESH_SPREAD_AIM_UI')
        self.start_spread_base, _, _ = self.ev_g_spread_values()

    def on_acc_shoot(self):
        if self.acc_shoot_activated:
            return
        change_state(self)
        self.acc_shoot_activated = True
        self.acc_shoot_id += 1
        tmp_id = self.acc_shoot_id
        global_data.game_mgr.delay_exec(3, self.clear_acc_shoot, tmp_id)

    def clear_acc_shoot(self, tmp_id=0):
        if tmp_id != 0 and tmp_id != self.acc_shoot_id:
            return
        if self.acc_shoot_activated:
            change_state(self)
            self.acc_shoot_activated = False


@editor.state_exporter({('pre_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x89\x8d\xe6\x91\x87','min_val': 0.2,'max_val': 1.5,'setter': lambda self, v: self.setter(v)
                           },
   ('fire_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4','min_val': 2,'max_val': 5,'setter': lambda self, v: self.setter2(v)
                            },
   ('post_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe6\x97\xb6\xe9\x95\xbf','min_val': 0.2,'max_val': 2,'setter': lambda self, v: self.setter3(v)
                            },
   ('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe6\x8f\x90\xe5\x89\x8d\xe5\x8f\xaf\xe5\x8f\x96\xe6\xb6\x88\xe6\x97\xb6\xe9\x97\xb4','setter': lambda self, v: self.setter4(v)
                                  },
   ('damage_interval', 'param'): {'zh_name': '\xe6\x8c\x81\xe7\xbb\xad\xe8\xb7\xb3\xe5\xad\x97\xe9\xa2\x91\xe7\x8e\x87'},('cancel_cd', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8f\x96\xe6\xb6\x88\xe7\x9a\x84\xe6\x83\xa9\xe7\xbd\x9aCD'},('camera_sense', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x95\x9c\xe5\xa4\xb4\xe7\x81\xb5\xe6\x95\x8f\xe5\xba\xa6','min_val': 0.2,'max_val': 5},('vice_fire_scale_speed', 'param'): {'zh_name': '\xe8\xbe\x90\xe7\x85\xa7\xe7\x82\xae\xe5\xbc\xb9\xe9\x81\x93\xe9\x80\x9f\xe5\xba\xa6','setter': lambda self, v: self.setter4(v),
                                        'getter': lambda self: self.vice_fire_scale_speed / NEOX_UNIT_SCALE},
   ('rising_speed', 'meter'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8d\x87\xe7\xa9\xba\xe9\x80\x9f\xe5\xba\xa6','min_val': 1,'max_val': 10},('sputtering_coe', 'param'): {'zh_name': '\xe6\xba\x85\xe5\xb0\x84\xe8\x8c\x83\xe5\x9b\xb4\xe7\xb3\xbb\xe6\x95\xb0\xef\xbc\x88\xe5\x9f\xba\xe7\xa1\x80\xe5\x80\xbc\xe4\xb8\xba4\xe7\xb1\xb3\xe5\x8d\x8a\xe5\xbe\x84\xef\xbc\x89'}})
class AccumulateSkill8016(StateBase):
    STATE_NONE = -1
    STATE_PRE = 0
    STATE_HOLD = 1
    STATE_FIRE = 2
    STATE_POST = 3
    BIND_EVENT = StateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'TRY_STOP_WEAPON_ATTACK': 'on_end_shoot'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateSkill8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.refresh_sub_state_callback()

    def destroy(self):
        super(AccumulateSkill8016, self).destroy()
        PartCtrl.enable_clamp_cam_rotation(False)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')

    def refresh_sub_state_callback(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_FIRE, self.fire_time, self.post_fire)
        self.register_substate_callback(self.STATE_POST, self.post_break_time, self.post_break)
        self.register_substate_callback(self.STATE_POST, self.post_time, self.fire_end)

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.hover_skill_id = self.custom_param.get('hover_skill_id', 801655)
        self.pre_anim = self.custom_param.get('pre_anim', 'blast_dash')
        self.pre_time = self.custom_param.get('pre_time', 0.767) * 1.0
        self.fire_anim = self.custom_param.get('fire_anim', 'blast_shoot')
        self.fire_time = self.custom_param.get('fire_time', 2.5) * 1.0
        self.sd.ref_8016_acc_skill_time = self.fire_time
        self.damage_interval = self.custom_param.get('damage_interval', 0.2) * 1.0
        self.damage_cnt = 0
        self.post_anim = self.custom_param.get('post_anim', 'blast_end')
        self.post_time = self.custom_param.get('post_time', 1.2) * 1.0
        self.post_break_time = self.custom_param.get('post_break_time', 0.6) * 1.0
        self.cancel_cd = self.custom_param.get('cancel_cd', 2.0) * 1.0
        self.cancel_time = self.custom_param.get('cancel_time', 0.2) * 1.0
        self.rising_speed = self.custom_param.get('rising_speed', 3) * NEOX_UNIT_SCALE
        self.camera_sense = self.custom_param.get('camera_sense', 1.0) * 1.0
        self.sputtering_coe = self.custom_param.get('sputtering_coe', 1.0) * 1.0
        self.last_cancel_time = 0
        self.turn_anim = [
         'blast_dash', 'blast_dash_turn_r', 'blast_dash_turn_l']
        self.can_break = False
        self.btn_hold = False
        self.vice_fire_scale_speed = self.custom_param.get('vice_fire_scale_speed', 450) * NEOX_UNIT_SCALE
        self.sd.ref_vice_fire_scale_speed = self.vice_fire_scale_speed
        self.sd.ref_vice_sync_interval = self.custom_param.get('vice_sync_interval', 0.1) * 1.0
        self.sync_cnt = self.sd.ref_vice_sync_interval
        self.atk_radius = 1.0
        self.last_rocker_dir = None
        self.walk_speed = self.custom_param.get('walk_speed', 8) * NEOX_UNIT_SCALE
        self.move_acc = self.custom_param.get('move_acc', 30) * NEOX_UNIT_SCALE
        self.brake_acc = self.custom_param.get('brake_acc', -30) * NEOX_UNIT_SCALE
        self.auto_fire_mode = False
        self.cnt = 0
        self.cast_time = 0
        self.hovering = False
        self.start_pos = self.end_pos = None
        self.hit_phantom = []
        return

    def _do_hover(self, flag):
        if flag == self.hovering:
            return
        self.hovering = flag
        if flag:
            self.send_event('E_DO_SKILL', self.hover_skill_id)
        else:
            self.send_event('E_END_SKILL', self.hover_skill_id)

    def enter(self, leave_states):
        super(AccumulateSkill8016, self).enter(leave_states)
        self.start_pos = self.end_pos = None
        self.send_event('E_SWITCH_ACTION', 'action5', MC_OTHER_JUMP_1)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False, max_lerp_duration=0.5)
        self.send_event('E_CLEAR_SPEED_INTRP', self.pre_time)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_SOFT_ENTER_PITCH_MODEL', 0.2)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.pre_fire(MC_FLIGHT_BOOST in leave_states)
        self.camp_id = self.ev_g_camp_id()
        self.cnt = 0
        self.request_cnt = self.fire_time / self.damage_interval
        if not self.auto_fire_mode and self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.cancel_attack)
        self.last_on_ground = self.ev_g_on_ground()
        if not self.last_on_ground:
            self.send_event('E_GRAVITY', 0)
            self._do_hover(True)
        else:
            self.send_event('E_GRAVITY', 0.1)
        self.hit_phantom = []
        return

    def exit(self, enter_states):
        super(AccumulateSkill8016, self).exit(enter_states)
        if {MC_SHOOT, MC_RELOAD, MC_AIM_SHOOT} & enter_states:
            if not self.ev_g_on_ground() and MC_JUMP_2 not in self.ev_g_cur_state():
                self.send_event('E_FALL')
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_CLEAR_VICE_EFFECT')
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.1)
        self.send_event('E_END_SKILL', self.skill_id)
        self._do_hover(False)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_ACC_SKILL_END')
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.enter_camera(DEFAULT_CAM_STATE)
        PartCtrl.enable_clamp_cam_rotation(False)
        if self.sub_state == self.STATE_FIRE:
            self.send_event('E_CREATE_VICE_END_EFFECT', sync=True, force=True)
        self.sub_state = self.STATE_NONE
        self.play_charge_sound(False)
        self.play_cast_fire_sound(False)
        if self.ev_g_on_ground():
            self.send_event('E_BEGIN_RECOVER_MP', skill_const.SKILL_DASH_8016)

    def action_btn_down(self):
        self.btn_hold = True
        if get_server_time() - self.last_cancel_time <= self.cancel_cd + 0.1:
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        super(AccumulateSkill8016, self).action_btn_down()
        self.active_self()
        return True

    def action_btn_up(self):
        super(AccumulateSkill8016, self).action_btn_up()
        self.btn_hold = False
        if not self.is_active:
            return
        if self.auto_fire_mode:
            if self.sub_state == self.STATE_FIRE:
                self.post_fire()
        elif self.sub_state == self.STATE_HOLD:
            self.cast_fire()
        elif self.sub_state == self.STATE_FIRE:
            self.post_fire()

    def update(self, dt):
        super(AccumulateSkill8016, self).update(dt)
        self.check_need_float()
        if self.sub_state == self.STATE_FIRE:
            mat = self.ev_g_model().get_socket_matrix('aim', world.SPACE_TYPE_WORLD)
            camera = global_data.game_mgr.scene.active_camera
            forward = camera.rotation_matrix.forward
            start_pos = mat.translation
            fire_forward = mat.rotation.forward
            end_pos = get_fire_end(self.camp_id, camera.position, camera.position + forward * 300 * NEOX_UNIT_SCALE, self.ev_g_position(), start_pos - fire_forward * 4 * NEOX_UNIT_SCALE, forward)
            sync = False
            self.sync_cnt += dt
            if self.sync_cnt >= self.sd.ref_vice_sync_interval:
                self.sync_cnt = 0
                sync = True
            self.end_pos = self.ev_g_update_vice_effect(dt, start_pos, end_pos, sync=sync)
            self.start_pos = start_pos
            self.damage_cnt += dt
            if self.damage_cnt > self.damage_interval:
                self.request_damage()
        if self.sub_state in (self.STATE_HOLD,):
            if not self.btn_hold:
                self.cast_fire()
            self.normal_move_logic(dt)

    def check_transitions(self):
        if self.sub_state == self.STATE_POST and self.can_break:
            if self.sd.ref_rocker_dir is not None:
                if self.ev_g_on_ground():
                    self.send_event('E_ADD_WHITE_STATE', {MC_MOVE}, self.sid)
                    return MC_MOVE
                self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2}, self.sid)
                return MC_JUMP_2
        if self.sub_state == self.STATE_NONE:
            self.disable_self()
            if self.ev_g_on_ground():
                return MC_STAND
            else:
                return MC_JUMP_2

        if self.sub_state in (self.STATE_HOLD, self.STATE_PRE):
            if self.ev_g_fuel() <= 0:
                self.send_event('E_RESET_GRAVITY')
        return

    def check_need_float(self):
        cur_on_ground = self.ev_g_on_ground()
        if not cur_on_ground and self.last_on_ground:
            if self.ev_g_fuel() > 0:
                self.send_event('E_GRAVITY', 0)
            self._do_hover(True)
        elif cur_on_ground and not self.last_on_ground:
            self.send_event('E_GRAVITY', 0.1)
            if self.ev_g_fuel() > 0:
                self._do_hover(False)
        self.last_on_ground = cur_on_ground

    def request_damage(self):
        self.damage_cnt = 0
        if self.cnt > self.request_cnt:
            return
        else:
            if self.start_pos is None or self.end_pos is None:
                return
            hit_target_list, hit_phantom, atk_range, pos, t_forward, up = get_hit_target(self.unit_obj.id, self.camp_id, self.start_pos, self.end_pos, self.atk_radius, self.sputtering_coe)
            self.check_hit_phantom(hit_phantom)
            self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, [hit_target_list, atk_range, pos, t_forward, up]), False, True)
            self.send_event('E_SYNC_UPDATE_VICE_HIT', hit_target_list, sync=True)
            self.cast_time = self.elapsed_time
            self.cnt += 1
            return

    def pre_fire(self, combo_flight_boost):
        self.damage_cnt = 0
        self.can_break = False
        self.sub_state = self.STATE_PRE
        turn_shoot = False
        if combo_flight_boost:
            turn_dir = get_cur_turn_dir(self.ev_g_get_walk_direction())
            turn_shoot = turn_dir != TURN_FORWARD
            pre_anim = self.turn_anim[turn_dir]
        else:
            pre_anim = self.pre_anim
        self.send_event('E_POST_ACTION', pre_anim, LOW_BODY, 1, timeScale=0.7 / self.pre_time)
        self.send_event('E_ACC_SKILL_PRE_BEGIN')
        pre_time = self.pre_time
        self.delay_call(pre_time + 0.15 if turn_shoot else pre_time, self.hold_fire)

    def hold_fire(self):
        if self.auto_fire_mode:
            if not self.btn_hold:
                self.cancel_attack()
            else:
                self.send_event('E_ACC_SKILL_HOLD')
                self.cast_fire()
        else:
            self.send_event('E_ACC_SKILL_HOLD')
            self.sub_state = self.STATE_HOLD
            self.send_event('E_POST_ACTION', 'blast_idle', LOW_BODY, 1, loop=True, timeScale=1.0)
            self.play_charge_sound(True)
        self.send_event('E_VERTICAL_SPEED', 0)

    def cast_fire(self):
        self.sub_state = self.STATE_FIRE
        self.send_event('E_POST_ACTION', self.fire_anim, LOW_BODY, 1, loop=True, timeScale=1.0)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.atk_radius = self.ev_g_add_attr(attr_const.WEAPON_RADIUS_ADD_FACTOR_8016) + 1.0
        self.send_event('E_CREATE_VICE_EFFECT', self.atk_radius, sync=True)
        self.send_event('E_ACC_SKILL_BEGIN')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_CLEAR_SPEED')
        PartCtrl.enable_clamp_cam_rotation(True, 0.01 * self.camera_sense * (1.0 + self.ev_g_add_attr(attr_const.MECHA_MAX_BODY_TURN_SPEED_FACTOR)))
        if not self.ev_g_on_ground():
            self.send_event('E_GRAVITY', 0)
        self.send_event('E_END_SKILL', self.hover_skill_id)
        self.play_charge_sound(False)
        self.play_cast_fire_sound(True)

    def cancel_attack(self):
        if self.sub_state != self.STATE_FIRE:
            self.last_cancel_time = get_server_time()
            self.send_event('E_START_ACTION_CD', self.bind_action_id, self.cancel_cd)
            self.fire_end()
        else:
            self.post_fire()
        self.send_event('E_ACC_SKILL_END')

    def post_fire(self):

        def last_damage():
            self.request_damage()
            self.send_event('E_END_SKILL', self.skill_id)

        self.delay_call(self.elapsed_time - self.cast_time, last_damage)
        self.sub_state = self.STATE_POST
        self.send_event('E_POST_ACTION', self.post_anim, LOW_BODY, 1, loop=True, timeScale=1.0)
        self.send_event('E_CREATE_VICE_END_EFFECT', sync=True)
        self.send_event('E_SOFT_EXIT_PITCH_MODEL', self.post_time)
        self.send_event('E_ACC_SKILL_END')
        self.enter_camera(CAM_STATE_BLAST_END)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        PartCtrl.enable_clamp_cam_rotation(False)
        self.send_event('E_RESET_GRAVITY')
        self.sound_custom_start()
        self.sound_custom_end()

    def post_break(self):
        self.can_break = True
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2, MC_SHOOT, MC_FLIGHT_BOOST, MC_RELOAD, MC_SHOOT_MODE, MC_AIM_SHOOT}, self.sid)
        self.send_event('E_ACC_SKILL_END')

    def fire_end(self):
        self.sub_state = self.STATE_NONE
        self.send_event('E_ACC_SKILL_END')

    def normal_move_logic(self, dt):
        rocker_dir = self.sd.ref_rocker_dir
        if self.last_rocker_dir != rocker_dir:
            self.last_rocker_dir = rocker_dir
        cur_speed = self.sd.ref_cur_speed
        max_speed = self.walk_speed
        if cur_speed is None or max_speed is None:
            return
        else:
            acc = rocker_dir and not rocker_dir.is_zero
            cur_speed += dt * (self.move_acc if acc else self.brake_acc)
            cur_speed = clamp(cur_speed, 0, max_speed + 1)
            self.sd.ref_cur_speed = cur_speed
            self.send_event('E_MOVE', rocker_dir)
            return

    def on_end_shoot(self):
        if self.sub_state != self.STATE_FIRE:
            self.fire_end()
        else:
            self.post_fire()
        self.send_event('E_ACC_SKILL_END')

    def play_charge_sound(self, play):
        play = 1 if play else 0
        visible = 2 if play else 0
        sound_clip = 'm_8016_weapon1_charge'
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', play, (sound_clip, 'nf'), 0, 1, visible, 6)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (play, (sound_clip, 'nf'), 0, 1, visible, 6)], True)

    def play_cast_fire_sound(self, play):
        play = 1 if play else 0
        if play:
            sound_clip = 'm_8016_weapon1_charge_fire'
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', play, (sound_clip, 'nf'), 0, 0, None, None)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (play, (sound_clip, 'nf'), 0, 0, None, None)], True)
        visible = 2 if play else 0
        sound_clip = 'm_8016_weapon1_fire_loop'
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', play, (sound_clip, 'nf'), 0, 1, visible, 6)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (play, (sound_clip, 'nf'), 0, 1, visible, 6)], True)
        return

    def check_hit_phantom(self, phantom_list):
        for phantom in phantom_list:
            if phantom not in self.hit_phantom:
                do_hit_phantom(self, phantom)
                self.hit_phantom.append(phantom)

    def setter(self, v):
        self.pre_time = v
        self.refresh_sub_state_callback()

    def setter2(self, v):
        self.fire_time = v
        self.refresh_sub_state_callback()

    def setter3(self, v):
        self.post_time = v
        self.refresh_sub_state_callback()

    def setter4(self, v):
        self.post_break_time = v
        self.refresh_sub_state_callback()

    def setter5(self, v):
        self.vice_fire_scale_speed = v * NEOX_UNIT_SCALE
        self.sd.ref_vice_fire_scale_speed = self.vice_fire_scale_speed

    def getter5(self):
        return self.vice_fire_scale_speed / NEOX_UNIT_SCALE


@editor.state_exporter({('boost_pre_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x95\xbf','min_val': 0.2,'max_val': 1.5,'setter': lambda self, v: self.setter(v)
                                     },
   ('boost_post_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe6\x97\xb6\xe9\x95\xbf','min_val': 0.5,'max_val': 1.5,'setter': lambda self, v: self.setter2(v)
                                      },
   ('boost_post_brake', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8f\xaf\xe5\x8f\x96\xe6\xb6\x88\xe7\x82\xb9','setter': lambda self, v: self.setter3(v)
                                   },
   ('boost_acc_duration', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa0\xe9\x80\x9f\xe6\x97\xb6\xe9\x95\xbf','setter': lambda self, v: self.setter4(v)
                                     },
   ('boost_brake_duration', 'param'): {'zh_name': '\xe5\x88\xb9\xe8\xbd\xa6\xe6\x97\xb6\xe9\x97\xb4'},('boost_start_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('boost_speed', 'meter'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x95\x9c\xe5\xa4\xb4\xe7\x81\xb5\xe6\x95\x8f\xe5\xba\xa6','min_val': 0.2,'max_val': 5},('boost_combo_shoot_duration', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x8e\xa5\xe5\xbc\x80\xe7\x81\xab\xe7\x9a\x84\xe5\x88\x87\xe6\x8d\xa2\xe6\x97\xb6\xe9\x97\xb4'},('turn_shoot_time', 'param'): {'zh_name': '\xe8\xbd\xac\xe8\xba\xab\xe5\xb0\x84\xe5\x87\xbb\xe5\xbc\x80\xe6\x9e\xaa\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3'},('action_cd', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x97\xb4CD'},('reinforce_speed', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x8e\xa5\xe6\xad\xa3\xe5\x90\x91\xe5\xb0\x84\xe5\x87\xbb\xe5\x90\x8e\xe5\x9d\x90\xe5\x8a\x9b','min_val': 1,'max_val': 30},('min_elevation_speed_ratio', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbb\xb0\xe8\xa7\x92\xe6\x97\xb6\xe7\x9a\x84\xe9\x80\x9f\xe5\xba\xa6\xe8\xa1\xb0\xe5\x87\x8f'}})
class FlightBoost8016(StateBase):
    BIND_EVENT = {'G_COMBO_SHOOT': 'check_combo_shoot',
       'E_COMBO_SHOOT': 'start_combo_shoot',
       'G_TRY_INTERRUPT_FLIGHT_BOOST_BY_JUMP': 'try_interrupt_flight_boost_by_jump'
       }
    STATE_NONE = -1
    STATE_PRE = 0
    STATE_START = 1
    STATE_DASH = 2
    STATE_STOP = 3
    STATE_BRAKE_SHOOT = 4
    STATE_TURN_SHOOT = 5

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        from logic.gcommon.common_const.ui_operation_const import DASH_CAM_DIR_8016
        super(FlightBoost8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.need_trigger_btn_up_when_action_forbidden = False
        self.refresh_sub_state_callback()
        self.is_waiting_to_interrupt = False
        self.need_reset_forward = False
        if self.ev_g_is_avatar():
            global_data.emgr.dash_dir_type_8016 += self.on_setting_changed
            if global_data.player:
                self._dash_cam_dir = global_data.player.get_setting_2(DASH_CAM_DIR_8016)

    def destroy(self):
        super(FlightBoost8016, self).destroy()
        self.unregist_event('E_ROTATE', self.on_rotate)
        global_data.emgr.dash_dir_type_8016 -= self.on_setting_changed

    def on_setting_changed(self, enable):
        self._dash_cam_dir = enable

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param['skill_id']
        self.boost_pre_anim = 'dash_start'
        self.boost_anim = 'dash_f'
        self.boost_post_anim = self.custom_param['boost_post_anim']
        self.boost_pre_duration = self.custom_param.get('boost_pre_duration', 1.0)
        self.boost_acc_duration = self.custom_param.get('boost_acc_duration', 0.5)
        self.boost_post_brake = self.custom_param.get('boost_post_brake', 0.6)
        self.boost_post_duration = self.custom_param.get('boost_post_duration', 1.0)
        self.boost_brake_duration = self.custom_param.get('boost_brake_duration', 0.8)
        self.boost_combo_shoot_duration = self.custom_param.get('boost_combo_shoot_duration', 0.6)
        self.boost_start_speed = self.custom_param.get('boost_start_speed', 1) * NEOX_UNIT_SCALE
        self.boost_speed = self.custom_param.get('boost_speed', 50) * NEOX_UNIT_SCALE
        self.max_pitch_rad = self.custom_param.get('max_pitch_rad', 0.8)
        self.vertical_turn_speed = self.custom_param.get('vertical_turn_speed', 0.3) * math.pi
        self.horizon_turn_speed = self.custom_param.get('horizon_turn_speed', 0.3) * math.pi
        self.action_cd = self.custom_param.get('action_cd', 1.5) * 1.0
        self.reinforce_speed = self.custom_param.get('reinforce_speed', 20) * 1.0
        self.turn_anim = [
         'dash_shoot', 'dash_shoot_turn_r', 'dash_shoot_turn_l']
        self.turn_shoot_time = self.custom_param.get('turn_shoot_time', 0.4) * 1.0
        self.shoot_brake_duration = 0.65
        self.min_elevation_speed_ratio = self.custom_param.get('min_elevation_speed_ratio', 0.65)
        self.can_brake = False
        self.can_exit = False
        self.boost_acc = 0
        self.brake_acc = 0
        self.brake_acc_land = 0
        self.brake_acc_air = 0
        self.brake_speed_air = 20 * NEOX_UNIT_SCALE
        self.free_mode = False
        self.last_exit_time = 0
        self.boost_direction = None
        self.speed_ratio = 1.0
        self.acc_shooted = False
        self._old_pos = None
        return

    def refresh_sub_state_callback(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, self.boost_pre_duration, self.flight_acc)
        self.register_substate_callback(self.STATE_START, self.boost_acc_duration, self.flight_boost)
        self.register_substate_callback(self.STATE_STOP, self.boost_post_brake, self.flight_end_brake)
        self.register_substate_callback(self.STATE_STOP, self.boost_post_duration, self.flight_end)
        self.register_substate_callback(self.STATE_BRAKE_SHOOT, self.shoot_brake_duration, self.flight_end)

    def action_btn_down(self):
        if get_server_time() - self.last_exit_time <= self.action_cd + 0.03:
            self.send_event('E_SOUND_TIP_CD')
            return False
        if not self.check_can_active():
            return False
        super(FlightBoost8016, self).action_btn_down()
        if self.sub_state == self.STATE_DASH:
            self.flight_post()

    def action_btn_up(self):
        if get_server_time() - self.last_exit_time <= self.action_cd + 0.03:
            return False
        if not self.check_can_active():
            return False
        super(FlightBoost8016, self).action_btn_up()
        if self.sub_state != self.STATE_DASH:
            if self.check_can_cast_skill():
                self.active_self()

    def enter(self, leave_states):
        super(FlightBoost8016, self).enter(leave_states)
        self.is_waiting_to_interrupt = False
        self.need_reset_forward = False
        self.send_event('E_SWITCH_ACTION', 'action5', MC_OTHER_JUMP_1)
        self.flight_pre()
        self.send_event('E_STOP_POLLER', 'action1')
        self.send_event('E_STOP_POLLER', 'action2')
        self.send_event('E_STOP_POLLER', 'action3')
        self.send_event('E_STOP_POLLER', 'action5')
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def exit(self, enter_states):
        super(FlightBoost8016, self).exit(enter_states)
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_RESET_GRAVITY')
        if self.sub_state != self.STATE_STOP:
            self.reset_forward()
        self.sub_state = self.STATE_NONE
        self.unregist_event('E_ROTATE', self.on_rotate)
        self.send_event('E_DELTA_YAW', 0)
        self.send_event('E_DELTA_PITCH', 0)
        self.send_event('E_END_SKILL', self.skill_id)
        self._check_dash_dist()
        if self.ev_g_on_ground():
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True
        if not self.ev_g_is_action_down('action1') or not self.ev_g_is_action_down('action2') or not self.ev_g_is_action_down('action3'):
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_START_ACTION_CD', self.bind_action_id, self.action_cd)
        self.last_exit_time = get_server_time()
        self.enter_camera(DEFAULT_CAM_STATE)
        if self.ev_g_attr_get(attr_const.ENABLE_WEAPON_MAX_ACCUMULATE_8016) and not self.acc_shooted:
            self.send_event('E_SET_ACC_SHOOT')
        self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.1)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)

    def update(self, dt):
        super(FlightBoost8016, self).update(dt)
        if self.sub_state == self.STATE_PRE:
            return
        forward = math3d.vector(self.boost_direction)
        speed = self.sd.ref_cur_speed
        if self.sub_state in (self.STATE_START, self.STATE_DASH):
            max_speed = self.boost_speed * self.speed_ratio
            if self.boost_acc < 0.0:
                speed = max_speed
            else:
                speed += dt * self.boost_acc
                speed = max_speed if speed > max_speed else speed
            if self.ev_g_on_ground() and forward.pitch > 0:
                forward.y = 0
                forward.normalize()
            if self.sub_state == self.STATE_DASH:
                if self.ev_g_energy(skill_const.SKILL_DASH_8016) <= 0:
                    self.flight_post()
            self.sd.ref_effective_camera_rot = math3d.matrix_to_rotation(global_data.game_mgr.scene.active_camera.rotation_matrix)
        elif self.sub_state == self.STATE_STOP:
            speed -= dt * self.brake_acc
            speed = 0 if speed < 0 else speed
        elif self.sub_state == self.STATE_TURN_SHOOT:
            self.combo_walk_time += dt
            percent = (self.boost_combo_shoot_duration - self.combo_walk_time) / self.boost_combo_shoot_duration
            cur_walk_dir = self.combo_walk_direction * (percent if percent > 0 else 0)
            self.send_event('E_SET_WALK_DIRECTION', cur_walk_dir)
            self.sd.ref_cur_speed = cur_walk_dir.length
            return
        on_ground = self.ev_g_on_ground()
        if on_ground:
            if forward.y > 0:
                self.send_event('E_JUMP', 0)
            elif not self.last_on_ground:
                self.send_event('E_GRAVITY', 1)
        elif self.last_on_ground:
            self.send_event('E_GRAVITY', 0)
        self.last_on_ground = on_ground
        self.send_event('E_VERTICAL_SPEED', forward.y * speed)
        self.boost_direction = math3d.vector(forward)
        forward.y = 0
        self.send_event('E_SET_WALK_DIRECTION', forward * speed)
        self.sd.ref_cur_speed = speed

    def check_transitions(self):
        if self.is_waiting_to_interrupt:
            if self.sub_state == self.STATE_DASH or self.sub_state == self.STATE_STOP and self.can_brake:
                if self.ev_g_try_jump_directly():
                    return
        in_air = not self.ev_g_on_ground()
        rocker_dir = self.sd.ref_rocker_dir
        if self.can_brake:
            if rocker_dir and not in_air:
                next_state = MC_RUN if self.sd.ref_cur_speed > self.ev_g_max_walk_speed() else MC_MOVE
                self.disable_self()
                return next_state
            if in_air:
                self.disable_self()
                return MC_JUMP_2
        if self.can_exit:
            self.disable_self()
            if in_air:
                return MC_JUMP_2
            return MC_STAND
        if self.sub_state == self.STATE_TURN_SHOOT:
            speed = abs(self.sd.ref_cur_speed)
            if speed < 1:
                self.disable_self()
                if in_air:
                    return MC_JUMP_2
                return MC_STAND
            if speed < 8 * NEOX_UNIT_SCALE and not in_air:
                if rocker_dir:
                    self.disable_self()
                    return MC_MOVE

    def check_combo_shoot(self):
        return self.sub_state == self.STATE_DASH

    def start_combo_shoot(self):
        self.combo_walk_direction = self.ev_g_get_walk_direction()
        self.combo_walk_time = 0
        turn_dir = get_cur_turn_dir(self.combo_walk_direction)
        if turn_dir == 0:
            self.sub_state = self.STATE_BRAKE_SHOOT if 1 else self.STATE_TURN_SHOOT
            self.reset_forward()
            anim_name = self.turn_anim[turn_dir]
            self.send_event('E_POST_ACTION', anim_name, UP_BODY, 7, blend_time=0, ignore_sufix=True, timeScale=1.0)
            self.send_event('E_POST_ACTION', anim_name, LOW_BODY, 1, blend_time=0, timeScale=1.0)
            self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
            self.ev_g_on_ground() or self.send_event('E_SOFT_ENTER_PITCH_MODEL', 0.1)
        if turn_dir == 0:
            self.send_event('E_CLEAR_SPEED')
            recoil_force(self, -global_data.game_mgr.scene.active_camera.rotation_matrix.forward, max_force=self.reinforce_speed, recoil_time=0.6)
            self.enter_camera(CAM_STATE_DASH_SHOOT)
            shoot_time = 0.09
        else:
            self.enter_camera(CAM_STATE_DASH_SHOOT_TURN)
            shoot_time = self.turn_shoot_time

        def shoot():
            acc_shoot = self.ev_g_attr_get(attr_const.ENABLE_WEAPON_MAX_ACCUMULATE_8016)
            weapon_pos = 2 if acc_shoot else 1
            self.ev_g_try_weapon_attack_begin(weapon_pos, acc_shoot)
            self.ev_g_try_weapon_attack_end(weapon_pos)

        self.delay_call(shoot_time, shoot)
        if self.ev_g_on_ground():
            self.send_event('E_CREATE_SMOG_EFFECT', 1, True)
        self.sound_custom_start()
        self.sound_custom_end()
        self.acc_shooted = True

    def on_rotate(self, *args):
        self.free_mode = True

    def get_boost_direction(self):
        rd = self.sd.ref_logic_trans
        camera_dir = global_data.game_mgr.scene.active_camera.rotation_matrix.forward
        if rd and not self._dash_cam_dir:
            yaw_val = rd.yaw_target
            cam_y = max(0, camera_dir.y)
            forward = math3d.vector(0, cam_y, math.sqrt(1.0 - cam_y * cam_y))
            m = math3d.matrix.make_rotation_y(yaw_val)
            forward = forward * m
            return forward
        return camera_dir

    def flight_pre(self):
        self.sub_state = self.STATE_PRE
        self.free_mode = False
        self.can_brake = False
        self.can_exit = False
        self.acc_shooted = False
        self.last_on_ground = self.ev_g_on_ground()
        boost_direction = self.get_boost_direction()
        self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', boost_direction, max_lerp_duration=0.2)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.enter_camera(CAM_STATE_DASH_START)
        if self.ev_g_on_ground():
            self.send_event('E_CREATE_SMOG_EFFECT', 0, True)

    def flight_acc(self):
        self.sub_state = self.STATE_START
        boost_direction = self.get_boost_direction()
        self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', boost_direction, max_lerp_duration=0, force=True)
        self.boost_direction = boost_direction
        pitch = boost_direction.pitch
        if pitch < 0.0:
            if pitch < -1.3:
                speed_ratio = self.min_elevation_speed_ratio
            else:
                speed_ratio = 1.0 - pitch / -1.3 * (1.0 - self.min_elevation_speed_ratio)
        else:
            speed_ratio = 1.0
        self.speed_ratio = speed_ratio
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_POST_ACTION', self.boost_pre_anim, LOW_BODY, 1, blend_time=0, timeScale=1.0)
        self.send_event('E_GRAVITY', 1)
        self.send_event('E_STEP_HEIGHT', 3 * NEOX_UNIT_SCALE)
        self.regist_event('E_ROTATE', self.on_rotate)
        self.send_event('E_DO_SKILL', self.skill_id)
        self._old_pos = self.ev_g_position()
        speed = self.sd.ref_cur_speed
        forward = self.ev_g_forward() * speed
        self.send_event('E_SET_WALK_DIRECTION', forward)
        self.sd.ref_cur_speed = speed
        max_speed = self.boost_speed * self.speed_ratio
        self.boost_acc = (max_speed - speed) / self.boost_acc_duration
        self.brake_acc_land = max_speed / self.boost_brake_duration
        self.brake_acc_air = (max_speed - self.brake_speed_air) / self.boost_brake_duration

    def flight_boost(self):
        self.sub_state = self.STATE_DASH
        self.send_event('E_POST_ACTION', self.boost_anim, LOW_BODY, 1, timeScale=1.0)
        self.send_event('E_ADD_WHITE_STATE', {MC_SECOND_WEAPON_ATTACK}, self.sid)
        self.enter_camera(CAM_STATE_DASH)
        self.send_event('E_FORBID_ROTATION', True)
        self.send_event('E_FORWARD', self.boost_direction)
        self.need_reset_forward = True

    def flight_post(self):
        if self.sub_state == self.STATE_STOP:
            return
        self.free_mode = True
        self.reset_forward()
        self.sub_state = self.STATE_STOP
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_POST_ACTION', self.boost_post_anim, LOW_BODY, 1, timeScale=1.0)
        self.unregist_event('E_ROTATE', self.on_rotate)
        self.brake_acc = self.brake_acc_land if self.ev_g_on_ground() else self.brake_speed_air
        self.send_event('E_END_SKILL', self.skill_id)
        self._check_dash_dist()
        self.enter_camera(CAM_STATE_DASH_STOP)
        if self.ev_g_on_ground():
            self.send_event('E_CREATE_SMOG_EFFECT', 1, True)
        self.sound_custom_start()
        self.sound_custom_end()
        if self.ev_g_attr_get(attr_const.ENABLE_WEAPON_MAX_ACCUMULATE_8016) and not self.acc_shooted:
            self.send_event('E_SET_ACC_SHOOT')

    def _check_dash_dist(self):
        if self._old_pos:
            dist = int((self.ev_g_position() - self._old_pos).length)
            if dist > 0:
                self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8016', MECHA_MEMORY_LEVEL_7, dist / NEOX_UNIT_SCALE), False, True)
        self._old_pos = None
        return

    def flight_end_brake(self):
        self.can_brake = True
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_AIM_SHOOT, MC_SUPER_JUMP}, self.sid)

    def flight_end(self):
        self.can_exit = True

    def reset_forward(self):
        if self.need_reset_forward:
            forward = self.ev_g_forward()
            forward.y = 0
            forward.normalize()
            self.send_event('E_FORWARD', forward)
            self.send_event('E_FORBID_ROTATION', False)

    def try_interrupt_flight_boost_by_jump(self):
        if self.is_active:
            if not self.is_waiting_to_interrupt:
                self.send_event('E_ADD_WHITE_STATE', {MC_OTHER_JUMP_1}, self.sid)
                self.is_waiting_to_interrupt = True
            if self.sub_state == self.STATE_DASH or self.sub_state == self.STATE_STOP and self.can_brake:
                if not self.ev_g_try_jump_directly():
                    if self.sub_state == self.STATE_DASH:
                        self.flight_post()
            return True
        return False

    def setter(self, v):
        self.boost_pre_duration = v
        self.refresh_sub_state_callback()

    def setter2(self, v):
        self.boost_post_duration = v
        self.refresh_sub_state_callback()

    def setter3(self, v):
        self.boost_post_brake = v
        self.refresh_sub_state_callback()

    def setter4(self, v):
        self.boost_acc_duration = v
        self.refresh_sub_state_callback()


class JumpUp8016(JumpUpPure):

    def enter(self, leave_states):
        super(JumpUp8016, self).enter(leave_states)
        self.send_event('E_FLIGHT_BOOST_FALL', False)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.sd.ref_tmp_forbid_anim_dir = True

    def exit(self, enter_states):
        super(JumpUp8016, self).exit(enter_states)
        self.sd.ref_tmp_forbid_anim_dir = False


@editor.state_exporter({('jump_speed_scale', 'param'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe5\x8f\x96\xe6\xb6\x88\xe5\x89\xaf\xe6\xad\xa6\xe5\x99\xa8\xe6\x97\xb6\xe7\x9a\x84\xe8\xb7\xb3\xe8\xb7\x83\xe9\x80\x9f\xe5\xba\xa6\xe7\xbc\xa9\xe6\x94\xbe'}})
class InterruptionJumpUp8016(JumpUpPure):
    BIND_EVENT = {'E_BUFF_JUMP_SPD_ADD': 'on_add_jump_speed_scale',
       'G_TRY_JUMP_DIRECTLY': 'jump_up_without_jump_count'
       }

    def read_data_from_custom_param(self):
        super(InterruptionJumpUp8016, self).read_data_from_custom_param()
        self.jump_anim = self.custom_param.get('jump_anim', 'jump_01')
        self.dash_jump_anim = self.custom_param.get('dash_jump_anim', 'dash_jump')
        self.jump_speed_scale = self.custom_param.get('jump_speed_scale', 0.6)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(InterruptionJumpUp8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.cur_jump_speed_scale = 1.0

    def jump_up_without_jump_count(self):
        if not self.check_can_cast_skill():
            return False
        if not self.check_can_active():
            return False
        self.active_self()
        return True

    def action_btn_down(self):
        if self.ev_g_try_interrupt_flight_boost_by_jump():
            return True
        return self.jump_up_without_jump_count()

    def get_jump_speed(self):
        self.speed_scale_anticheat = self.extra_jump_speed_scale
        jump_speed = self.jump_speed * self.extra_jump_speed_scale * self.cur_jump_speed_scale
        self.cur_jump_speed_scale = 1.0
        return jump_speed

    def _do_jump(self):
        jump_speed = self.get_jump_speed()
        self.air_horizontal_offset_speed_setter.reset()
        self.send_event('E_GRAVITY', self.jump_gravity)
        self.send_event('E_JUMP', jump_speed)
        self.end_custom_sound('jump')
        self.start_custom_sound('jump')
        jump_up_duration = (jump_speed - jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE) / self.jump_gravity
        anim_rate = self.anim_duration / jump_up_duration
        self.send_event('E_ANIM_RATE', LOW_BODY, anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, self.anim_dir, blend_time=self.anim_blend_time, force_trigger_effect=True)
        self.send_event('E_PLAY_CAMERA_STATE_TRK', self.jump_camera_trk_name)
        self.send_event('E_DO_SKILL', self.skill_id)

    def enter(self, leave_states):
        super(JumpUpPure, self).enter(leave_states)
        flight_boost_jump = MC_FLIGHT_BOOST in leave_states
        self.anim_name = self.dash_jump_anim if flight_boost_jump else self.jump_anim
        self.cur_jump_speed_scale = self.jump_speed_scale if MC_SECOND_WEAPON_ATTACK in leave_states else 1.0
        self._do_jump()
        self.send_event('E_FLIGHT_BOOST_FALL', flight_boost_jump)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.sd.ref_tmp_forbid_anim_dir = True
        self.send_event('E_STOP_POLLER', 'action4')

    def exit(self, enter_states):
        super(InterruptionJumpUp8016, self).exit(enter_states)
        self.sd.ref_tmp_forbid_anim_dir = False


@editor.state_exporter({('flight_boost_fall_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe8\xb7\xb3\xe9\x87\x8d\xe5\x8a\x9b\xe5\x87\x8f\xe7\xbc\x93\xe6\x97\xb6\xe9\x97\xb4'},('flight_boost_fall_gravity', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe8\xb7\xb3\xe9\x87\x8d\xe5\x8a\x9b\xe5\x80\xbc'}})
class Fall8016(FallPure):
    BIND_EVENT = FallPure.BIND_EVENT.copy()
    BIND_EVENT.update({'E_FLIGHT_BOOST_FALL': 'on_flight_boost_fall'
       })

    def read_data_from_custom_param(self):
        super(Fall8016, self).read_data_from_custom_param()
        self.flight_boost_fall_time = self.custom_param.get('flight_boost_fall_time', 1) * 1.0
        self.flight_boost_fall_gravity = self.custom_param.get('flight_boost_fall_gravity', 10) * NEOX_UNIT_SCALE

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Fall8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.flight_boost_fall = False

    def enter(self, leave_states):
        super(FallPure, self).enter(leave_states)
        self.air_horizontal_offset_speed_setter.reset()
        self.check_on_ground_flag = 0
        if leave_states and self.coyote_duration > 0 and leave_states & self.ALLOW_JUMP_UP_STATES:
            self.send_event('E_ADD_WHITE_STATE', self.JUMP_UP_STATES, self.sid)
            self.sd.ref_in_coyote_time = True
            self.delay_call(self.coyote_duration, self.reset_jump_up_allowance)
        self.sd.ref_tmp_forbid_anim_dir = True
        if self.flight_boost_fall:
            self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_GRAVITY', self.flight_boost_fall_gravity if self.flight_boost_fall else self.fall_gravity)
        self.delay_call(self.flight_boost_fall_time, lambda : self.send_event('E_GRAVITY', self.fall_gravity))
        self.flight_boost_fall = False

    def exit(self, enter_states):
        super(Fall8016, self).exit(enter_states)
        self.sd.ref_tmp_forbid_anim_dir = False

    def on_flight_boost_fall(self, flight_boost_fall):
        self.flight_boost_fall = flight_boost_fall


class OnGround8016(OnGroundPure):

    def read_data_from_custom_param(self):
        super(OnGround8016, self).read_data_from_custom_param()
        self.normal_onground_anim = self.custom_param.get('normal_onground_anim', 'jump_05')
        self.jet_onground_anim = self.custom_param.get('jet_onground_anim', 'jump_04')
        self.jet_thread_speed = self.custom_param.get('jet_threa_speed', 65) * NEOX_UNIT_SCALE

    def enter(self, leave_states):
        super(OnGround8016, self).enter(leave_states)
        onground_anim = self.normal_onground_anim if self.hit_ground_vertical_speed < self.jet_thread_speed else self.jet_onground_anim
        self.send_event('E_POST_ACTION', onground_anim, LOW_BODY, 1, timeScale=1.0)
        self.sd.ref_tmp_forbid_anim_dir = True

    def exit(self, enter_states):
        super(OnGround8016, self).exit(enter_states)
        self.sd.ref_tmp_forbid_anim_dir = False

    def on_ground(self, *args):
        if super(OnGround8016, self).on_ground(*args):
            self.send_event('E_SOFT_EXIT_PITCH_MODEL', 0.1, reset_yaw=False)
            self.send_event('E_SWITCH_TO_AIR_SHOOT', False)
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
            self.send_event('E_BEGIN_RECOVER_MP', skill_const.SKILL_DASH_8016)


class SuperJump8016(SuperJumpUpPure):

    def enter(self, leave_states):
        super(SuperJump8016, self).enter(leave_states)
        self.sd.ref_tmp_forbid_anim_dir = True
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)

    def exit(self, enter_states):
        super(SuperJump8016, self).exit(enter_states)
        self.sd.ref_tmp_forbid_anim_dir = False


@editor.state_exporter({('slow_down_speed', 'meter'): {'zh_name': '\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'}})
class Reload8016(StateBase):
    BIND_EVENT = {'E_RELOADING': 'on_reloading_bullet',
       'E_WEAPON_BULLET_CHG': 'on_reloaded',
       'E_WEAPON_CHANGED': 'on_weapon_change',
       'G_RELOADING': 'on_reloading',
       'E_IGNORE_RELOAD_ANIM': 'on_ignore_reload_anim'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8016, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.continue_fire = False
        self.reloaded = True
        self.ignore_anim = False

    def read_data_from_custom_param(self):
        self.idle_reload_anim = self.custom_param.get('reload_anim', 'reload_idle')
        self.move_reload_anim = self.custom_param.get('reload_anim', 'reload_f')
        self.anim_time = self.custom_param.get('anim_duration', 1.3)
        self.reload_time = self.custom_param.get('reload_time', 2)
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.slow_down_speed = self.custom_param.get('slow_down_speed', 10) * NEOX_UNIT_SCALE

    def on_ignore_reload_anim(self, ignore):
        self.ignore_anim = ignore

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.reloaded:
            return False
        self.send_event('E_TRY_RELOAD', self.weapon_pos)
        super(Reload8016, self).action_btn_down()
        return True

    def on_reloading_bullet(self, time, times, weapon_pos):
        self.reload_time = time
        if not self.ignore_anim:
            self.active_self()

    def refresh_action_param(self, action_param, custom_param):
        super(Reload8016, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()
            self.reloaded = True

    def enter(self, leave_states):
        super(Reload8016, self).enter(leave_states)
        self.continue_fire = False
        self.reloaded = False
        self.send_event('E_SLOW_DOWN', True, self.slow_down_speed)
        self.timer_rate = self.anim_time / self.reload_time
        if self.bind_action_id:
            self.send_event('E_START_ACTION_CD', self.bind_action_id, self.reload_time)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_POST_ACTION', self.idle_reload_anim, UP_BODY, 1, timeScale=self.timer_rate)

    def update(self, dt):
        super(Reload8016, self).update(dt)

    def check_transitions(self):
        if self.reloaded:
            self.disable_self()

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        self.reloaded = True

    def on_weapon_change(self, weapon_pos):
        self.reloaded = True

    def on_reset_reload_state(self):
        self.reloaded = True

    def on_reloading(self):
        return not self.reloaded

    def exit(self, enter_states):
        super(Reload8016, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_CLEAR_UP_BODY_ANIM')