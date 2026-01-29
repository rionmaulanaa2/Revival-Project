# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8034.py
from __future__ import absolute_import
import math3d
from math import sin, cos, radians, degrees, pi
from logic.gcommon.editor import state_exporter
from .StateBase import StateBase
from .JumpLogic import JumpUp, OnGround
from .Logic8011 import StandWithGuard
from .ShootLogic import AccumulateShootPure
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.const import PART_WEAPON_POS_MAIN3
from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
from logic.gcommon.cdata.mecha_status_config import MC_STAND, MC_RUN, MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_JUMP_1, MC_DASH, MC_RELOAD
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
from logic.gcommon.common_const.mecha_const import MECHA_JUMP_TYPE_POISON_JUMP, MECHA_JUMP_TYPE_8034_JUMP
import random
from logic.gcommon.common_const.ui_operation_const import DASH_TRIGGER_TYPE_8034

class JumpUp8034(JumpUp):

    def enter(self, leave_states):
        super(JumpUp8034, self).enter(leave_states)
        self.send_event('E_JUMP_UP')


class OnGround8034(OnGround):
    BIND_EVENT = OnGround.BIND_EVENT.copy()
    BIND_EVENT.update({'E_JUMP_UP': 'on_jump_up'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(OnGround8034, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.has_jumped = False

    def on_jump_up(self):
        self.has_jumped = True

    def on_ground(self, *args):
        super(OnGround8034, self).on_ground(*args)
        if self.has_jumped:
            self.has_jumped = False
            self.send_event('E_ACTION_SYNC_GROUND', -30 * NEOX_UNIT_SCALE, MECHA_JUMP_TYPE_8034_JUMP)


def __editor_pitch_postsetter(self):
    self.swp_sin_cos = (
     sin(self.sub_weapon_pitch), cos(self.sub_weapon_pitch))


@state_exporter({('sub_weapon_pitch', 'param'): {'zh_name': '\xe5\xad\x90\xe6\xa6\xb4\xe5\xbc\xb9\xe5\x8f\x91\xe5\xb0\x84\xe4\xbb\xb0\xe8\xa7\x92(-90~90\xe5\xba\xa6)',
                                   'min_val': -90.0,
                                   'max_val': 90.0,'getter': lambda self: degrees(self.sub_weapon_pitch),
                                   'setter': --- This code section failed: ---

  56       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'radians'
           6  LOAD_GLOBAL           1  'radians'
           9  LOAD_FAST             1  'v'
          12  CALL_FUNCTION_1       1 
          15  CALL_FUNCTION_3       3 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15
,'post_setter': lambda self: __editor_pitch_postsetter(self)
                                   },
   ('post_anim_blend_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe8\x9e\x8d\xe5\x90\x88\xe6\x97\xb6\xe9\x97\xb4'}})
class ClusterShoot8034(AccumulateShootPure):
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD}

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ClusterShoot8034, self).init_from_dict(unit_obj, bdict, sid, info)
        self.explode_position = None
        self.pos_dir_getter_setted = False
        self.is_sp = False
        self.enable_param_changed_by_buff()
        return

    def read_data_from_custom_param(self):
        super(ClusterShoot8034, self).read_data_from_custom_param()
        self.main_weapon_id = self.custom_param.get('main_weapon_id', 803402)
        self.sub_weapon_pos = self.custom_param.get('sub_weapon_pos', PART_WEAPON_POS_MAIN3)
        self.sub_weapon_pitch = radians(self.custom_param.get('sub_weapon_pitch', 0))
        self.swp_sin_cos = (sin(self.sub_weapon_pitch), cos(self.sub_weapon_pitch))
        self.post_anim_blend_time = self.custom_param.get('post_anim_blend_time', 0.0)
        self.loop_stand_anim = self.custom_param.get('loop_stand_anim', 'boom_loop')
        self.loop_walk_anim = self.custom_param.get('loop_walk_anim', 'dash_move')

    def enter(self, leave_states):
        super(ClusterShoot8034, self).enter(leave_states)
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_SHOW_SEC_AIM', True)

    def exit(self, enter_states):
        super(ClusterShoot8034, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_SHOW_SEC_AIM', False)
        self.send_event('E_SHOW_SEC_WP_ACC', False)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        self.sound_drive.end_custom_sound('pre_state')
        self.sound_drive.end_custom_sound('loop_state')
        self.sound_drive.end_custom_sound('fire_state')
        return

    def _fire(self):
        if self.is_sp:
            self.ev_g_try_weapon_attack_begin(self.sub_weapon_pos)
            self.ev_g_try_weapon_attack_end(self.sub_weapon_pos)
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def on_begin_pre(self):
        part = UP_BODY
        if MC_STAND in self.ev_g_cur_state():
            part = LOW_BODY
        self.send_event('E_POST_ACTION', self.pre_anim_name, part, 1)
        self.send_event('E_SHOW_SEC_WP_ACC', True)
        self.sound_drive.start_custom_sound('pre_state')

    def on_end_pre(self):
        super(ClusterShoot8034, self).on_end_pre()
        self.sound_drive.end_custom_sound('pre_state')

    def on_begin_loop(self):
        self.sound_drive.start_custom_sound('loop_state')
        self.send_event('E_POST_ACTION', self.loop_anim_name, UP_BODY, 1)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.loop_stand_anim, loop=True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.loop_walk_anim, loop=True)

    def on_begin_post(self):
        self.sound_drive.end_custom_sound('loop_state')
        self.sound_drive.start_custom_sound('fire_state')
        self.send_event('E_SHOW_SEC_WP_ACC', False)
        self.skill_id and self.send_event('E_DO_SKILL', self.skill_id)
        self.acc_skill_ended = True
        self._fire()
        if MC_STAND in self.ev_g_cur_state():
            self.send_event('E_POST_ACTION', self.post_anim_name, LOW_BODY, 1, blend_time=self.post_anim_blend_time)
        self.send_event('E_ANIM_RATE', UP_BODY, self.post_anim_rate)
        self.send_event('E_POST_ACTION', self.post_anim_name, UP_BODY, 1, blend_time=self.post_anim_blend_time)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')

    def show_track(self, show):
        if show:
            self.send_event('E_SHOW_ACC_WP_TRACK')
        else:
            self.send_event('E_STOP_ACC_WP_TRACK')


class StandWithGuard8034(StandWithGuard):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(StandWithGuard8034, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._enable_guard_anim = True

    def replace_action_trigger_anim(self, anim, only_data=False, part=None, blend_dir=None, **kwargs):
        super(StandWithGuard8034, self).replace_action_trigger_anim(anim, only_data, part, blend_dir, **kwargs)
        if anim:
            self.default_anim = anim
            self._enable_guard_anim = False
        else:
            self.default_anim = self.custom_param.get('default_anim', None)
            self._enable_guard_anim = True
        if self.is_active and self.sub_state == self.STATE_DEFAULT:
            if self.sd.ref_low_body_anim != self.default_anim:
                self.switch_to_default()
                self.reset_sub_state_timer()
        return

    def switch_to_guard(self):
        if not self._enable_guard_anim or self.sd.ref_up_body_anim:
            self.reset_sub_state_timer()
            return
        guard_anim_index = random.randint(0, self.max_guard_anim_index) if self.max_guard_anim_index > 0 else 0
        self.sub_state = guard_anim_index
        self.send_event('E_POST_ACTION', self.guard_anim[guard_anim_index], LOW_BODY, 1, loop=True)
        self.sound_drive.custom_start()

    def switch_to_default(self):
        self.sub_state = self.STATE_DEFAULT
        self.send_event('E_POST_ACTION', self.default_anim, LOW_BODY, 1, loop=True)
        self.sound_drive.custom_end()

    def exit(self, enter_states):
        super(StandWithGuard8034, self).exit(enter_states)
        self.sound_drive.custom_end()


@state_exporter({('land_break_time', 'param'): {'zh_name': '\xe8\x90\xbd\xe5\x9c\xb0\xe7\xa1\xac\xe7\x9b\xb4\xe6\x97\xb6\xe9\x95\xbf'},('jump_dist', 'meter'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe7\xa7\xbb\xe5\x8a\xa8\xe8\xb7\x9d\xe7\xa6\xbb(\xe7\xb1\xb3)'},('jump_speed', 'meter'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6(\xe7\xb1\xb3/\xe7\xa7\x92)',
                             'post_setter': --- This code section failed: ---

 204       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'jump_dist'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'jump_dist'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             2  'jump_speed'
          18  BINARY_DIVIDE    
          19  CALL_FUNCTION_3       3 
          22  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 19
},
   ('jump_hori_acc', 'meter'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe6\xb0\xb4\xe5\xb9\xb3\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6(\xe7\xb1\xb3)'},('fall_gravity', 'meter'): {'zh_name': '\xe4\xb8\x8b\xe8\x90\xbd\xe9\x87\x8d\xe5\x8a\x9b'},('fall_hori_acc', 'meter'): {'zh_name': '\xe4\xb8\x8b\xe8\x90\xbd\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6(\xe7\xb1\xb3)'},('hori_move_acc', 'meter'): {'zh_name': '\xe4\xb8\x8b\xe8\x90\xbd\xe6\xb0\xb4\xe5\xb9\xb3\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6(\xe7\xb1\xb3)'},('jump_min_angle', 'param'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe6\x9c\x80\xe5\xb0\x8f\xe4\xbb\xb0\xe8\xa7\x92',
                                 'getter': lambda self: degrees(self.jump_min_angle),
                                 'setter': --- This code section failed: ---

 213       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'radians'
           6  LOAD_GLOBAL           1  'radians'
           9  LOAD_FAST             1  'v'
          12  CALL_FUNCTION_1       1 
          15  CALL_FUNCTION_3       3 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15
},
   ('real_max_jump_angle', 'param'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbb\xb0\xe8\xa7\x92',
                                      'getter': lambda self: degrees(self.real_max_jump_angle),
                                      'setter': --- This code section failed: ---

 218       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'radians'
           6  LOAD_GLOBAL           1  'radians'
           9  LOAD_FAST             1  'v'
          12  CALL_FUNCTION_1       1 
          15  CALL_FUNCTION_3       3 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15
},
   ('best_jump_angle', 'param'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe6\x9c\x80\xe4\xbd\xb3\xe4\xbb\xb0\xe8\xa7\x92',
                                  'getter': lambda self: degrees(self.best_jump_angle),
                                  'setter': --- This code section failed: ---

 223       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'radians'
           6  LOAD_GLOBAL           1  'radians'
           9  LOAD_FAST             1  'v'
          12  CALL_FUNCTION_1       1 
          15  CALL_FUNCTION_3       3 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15
},
   ('max_jump_angle', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xb7\x9d\xe7\xa6\xbb\xe8\xa1\xb0\xe5\x87\x8f\xe4\xbb\xb0\xe8\xa7\x92',
                                 'getter': lambda self: degrees(self.max_jump_angle),
                                 'setter': --- This code section failed: ---

 228       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'radians'
           6  LOAD_GLOBAL           1  'radians'
           9  LOAD_FAST             1  'v'
          12  CALL_FUNCTION_1       1 
          15  CALL_FUNCTION_3       3 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15
},
   ('jump_dist_param', 'param'): {'zh_name': '\xe5\x96\xb7\xe6\xb0\x94\xe8\xb7\x9d\xe7\xa6\xbb\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0'},('add_jump_angle', 'param'): {'zh_name': '\xe5\x9b\xba\xe5\xae\x9a\xe4\xbb\xb0\xe8\xa7\x92\xe5\x8a\xa0\xe6\x95\xb0',
                                 'getter': lambda self: degrees(self.add_jump_angle),
                                 'setter': --- This code section failed: ---

 234       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'radians'
           6  LOAD_GLOBAL           1  'radians'
           9  LOAD_FAST             1  'v'
          12  CALL_FUNCTION_1       1 
          15  CALL_FUNCTION_3       3 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 15
}
   })
class PoisonJump8034(StateBase):
    HOLDIND = -1
    JUMP_UP = 0
    JUMP_FALL = 1
    JUMP_GROUND = 2
    TRIGGER_TYPE_DOWN = 0
    TRIGGER_TYPE_UP = 1
    BIND_EVENT = {}

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(PoisonJump8034, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.trigger_type = self.TRIGGER_TYPE_DOWN
        if global_data.player and global_data.player.get_setting_2(DASH_TRIGGER_TYPE_8034):
            self.trigger_type = self.TRIGGER_TYPE_UP
        self.enable_rocker = self.ev_g_set_action_rocker(self.bind_action_id, self.trigger_type == self.TRIGGER_TYPE_UP)
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.bind_action_id = bdict.get('bind_action_id', 0)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.skill_obj = None
        self.hold_stand_anim = 'dash_stasr_loop'
        self.hold_move_anim = 'dash_move'
        self.jump_anim = 'dash_jump_01'
        self.fall_anim = 'dash_jump_02'
        self.land_anim = 'dash_jump_03'
        self.land_time = self.custom_param.get('land_time', 1.4)
        self.land_break_time = self.custom_param.get('land_break_time', 0.3)
        self.jump_dist = self.custom_param.get('jump_dist', 30.0) * NEOX_UNIT_SCALE
        self.jump_speed = self.custom_param.get('jump_speed', 25.0) * NEOX_UNIT_SCALE
        self.jump_hori_acc = self.custom_param.get('jump_hori_acc', 5.0) * NEOX_UNIT_SCALE
        self.fall_gravity = self.custom_param.get('fall_gravity', 100.0) * NEOX_UNIT_SCALE
        self.fall_hori_acc = self.custom_param.get('fall_hori_acc', 5.0) * NEOX_UNIT_SCALE
        self.hori_move_acc = self.custom_param.get('hori_move_acc', 5.0) * NEOX_UNIT_SCALE
        self.jump_min_angle = radians(self.custom_param.get('jump_min_angle', 15))
        self.best_jump_angle = radians(self.custom_param.get('best_jump_angle', 45.0))
        self.max_jump_angle = radians(self.custom_param.get('max_jump_angle', 50.0))
        self.real_max_jump_angle = radians(self.custom_param.get('real_max_jump_angle', 85.0))
        self.add_jump_angle = radians(self.custom_param.get('add_jump_angle', 20.0))
        self.jump_dist_param = self.custom_param.get('jump_dist_param', 1.0)
        self.max_jump_time = self.jump_dist / self.jump_speed
        self.hori_move_speed = 0
        self.ver_move_speed = 0
        self.jump_gravity = 0
        self.jump_hori_dir = None
        self.btn_down = False
        self._can_break = False
        self.track_timer_id = None
        self.last_position = math3d.vector(0, 0, 0)
        self.leave_ground_tried = False
        self.force_on_ground = False
        self._register_sub_state_callbacks()
        global_data.emgr.update_dash_trigger_type_8034 += self.on_trigger_type_changed
        return

    def _register_sub_state_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.JUMP_UP, 0.0, self.jump_start)
        self.register_substate_callback(self.JUMP_GROUND, self.land_break_time, self.on_can_break)
        self.register_substate_callback(self.JUMP_GROUND, self.land_time, self.disable_self)

    def on_trigger_type_changed(self, enable):
        self.trigger_type = enable and self.TRIGGER_TYPE_UP if 1 else self.TRIGGER_TYPE_DOWN
        self.enable_rocker = self.ev_g_set_action_rocker(self.bind_action_id, enable)

    def get_jump_dist(self, jump_angle):
        jump_dist = self.jump_dist
        if not self.skill_obj:
            self.skill_obj = self.ev_g_skill(self.skill_id)
        if self.skill_obj:
            data = self.skill_obj._data
            jump_distance_rate = data.get('ext_info', {}).get('jump_distance_rate', 0)
            if jump_distance_rate > 1.0:
                jump_dist *= jump_distance_rate
        rate = max(0.0, 1.0 - self.jump_dist_param * sin(abs(min(jump_angle, self.max_jump_angle) - self.best_jump_angle)))
        jump_dist *= rate
        return jump_dist

    def action_btn_down(self):
        if self.btn_down:
            return False
        else:
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
            if self.trigger_type == self.TRIGGER_TYPE_DOWN:
                self.active_self()
            else:
                self.btn_down = True
                if not self.enable_rocker:
                    self.enable_rocker = self.ev_g_set_action_rocker(self.bind_action_id, True)
                if self.ev_g_is_avatar():
                    from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                    MechaCancelUI(None, self.end_btn_down, True)
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.hold_stand_anim, loop=True)
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.hold_move_anim, loop=True)
                self.send_event('E_SLOW_DOWN', True)
                self.sound_drive.start_custom_sound('loop_state')
            super(PoisonJump8034, self).action_btn_down()
            return True

    def action_btn_up(self):
        super(PoisonJump8034, self).action_btn_up()
        if not self.btn_down:
            return
        if self.trigger_type == self.TRIGGER_TYPE_UP:
            self.active_self()
            self.end_btn_down()

    def update_jump_track(self):
        cam_mat = global_data.game_mgr.scene.active_camera.rotation_matrix
        move_dir = cam_mat.forward
        move_dir.y = 0
        move_dir.normalize()
        jump_angle = self.get_jump_angle(-cam_mat.pitch)
        jump_dist = self.get_jump_dist(jump_angle)
        start_pos = self.ev_g_position()
        hori_move = cos(jump_angle) * jump_dist
        ver_move = jump_dist * sin(jump_angle)
        ver_move_speed = ver_move * 2.0 / self.max_jump_time
        jump_gravity = ver_move_speed / self.max_jump_time
        target_pos = start_pos + move_dir * hori_move * 2.0
        move_dir *= hori_move / self.max_jump_time
        self.send_event('E_SHOW_JUMP_TRACK', 'effect/fx/niudan/tishitexiao_jiantou.sfx', start_pos, math3d.vector(move_dir.x, ver_move_speed, move_dir.z), -jump_gravity, target_pos)

    def get_jump_angle(self, jump_angle):
        return min(max(jump_angle + self.add_jump_angle, self.jump_min_angle), self.real_max_jump_angle)

    def enter(self, leave_states):
        super(PoisonJump8034, self).enter(leave_states)
        self._can_break = False
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.JUMP_UP
        global_data.emgr.disable_free_sight_btn.emit(True)

    def exit(self, enter_states):
        super(PoisonJump8034, self).exit(enter_states)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_SHOW_POISON_JUMP_SFX', False)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        cam_mtx = global_data.game_mgr.scene.active_camera.rotation_matrix
        self.sd.ref_logic_trans.yaw_target = cam_mtx.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        self.sound_drive.end_custom_sound('loop_state')
        self.sound_drive.end_custom_sound('jump_state')
        self.sound_drive.end_custom_sound('land_state')
        global_data.emgr.disable_free_sight_btn.emit(False)

    def jump_start(self):
        self.sound_drive.end_custom_sound('loop_state')
        self.sound_drive.start_custom_sound('jump_state')
        self.send_event('E_SHOW_POISON_JUMP_SFX', True)
        self.send_event('E_JET_CAMERA_SHAKE')
        self.send_event('E_POST_ACTION', self.jump_anim, LOW_BODY, 1, blend_time=0)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        cam_mat = global_data.game_mgr.scene.active_camera.rotation_matrix
        jump_hori_dir = cam_mat.forward
        jump_hori_dir.y = 0
        jump_hori_dir.normalize()
        jump_angle = self.get_jump_angle(-cam_mat.pitch)
        jump_dist = self.get_jump_dist(jump_angle)
        self.max_jump_time = jump_dist / self.jump_speed
        self.max_hori_speed = jump_dist * cos(jump_angle) / self.max_jump_time
        self.ver_move_speed = jump_dist * sin(jump_angle) * 2.0 / self.max_jump_time
        self.jump_gravity = self.ver_move_speed / self.max_jump_time
        self.jump_hori_vec = jump_hori_dir * self.max_hori_speed
        speed = self.jump_hori_vec
        speed.y = self.ver_move_speed
        self.air_walk_direction_setter.reset()
        self.air_walk_direction_setter.execute(speed)

    def jump_end(self, *args):
        self.ver_move_speed = 0
        self.regist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.send_event('E_POST_ACTION', self.fall_anim, LOW_BODY, 1, blend_time=0.2)
        self.sub_state = self.JUMP_FALL

    def on_ground(self, *args):
        if not self.is_active:
            return
        self.sound_drive.end_custom_sound('jump_state')
        self.sound_drive.start_custom_sound('land_state')
        self.sub_state = self.JUMP_GROUND
        self.send_event('E_SHOW_POISON_JUMP_SFX', False)
        self.send_event('E_POST_ACTION', self.land_anim, LOW_BODY, 1, blend_time=0)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_MECHA_ON_GROUND', args[0])
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.send_event('E_ACTION_SYNC_GROUND', -30 * NEOX_UNIT_SCALE, MECHA_JUMP_TYPE_POISON_JUMP)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        cam_mtx = global_data.game_mgr.scene.active_camera.rotation_matrix
        self.sd.ref_logic_trans.yaw_target = cam_mtx.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)

    def on_can_break(self):
        break_states = {
         MC_RUN, MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_JUMP_1, MC_DASH}
        self.send_event('E_ADD_WHITE_STATE', break_states, self.sid)
        self._can_break = True

    def update(self, dt):
        super(PoisonJump8034, self).update(dt)
        if self.sub_state not in (self.JUMP_UP, self.JUMP_FALL):
            return
        if self.sub_state == self.JUMP_FALL and self.ev_g_on_ground():
            self.on_ground(-self.fall_gravity * self.sub_sid_timer)
            return
        if self.sub_state == self.JUMP_UP and self.sub_sid_timer >= self.max_jump_time:
            self.jump_end()
            return
        cam_mtx = global_data.game_mgr.scene.active_camera.rotation_matrix
        self.sd.ref_logic_trans.yaw_target = cam_mtx.yaw
        self.sd.ref_common_motor.set_yaw_time(0)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir:
            rocker_dir *= math3d.matrix.make_rotation_y(cam_mtx.yaw)
            self.jump_hori_vec += rocker_dir * (self.hori_move_acc if self.sub_state == self.JUMP_FALL else self.jump_hori_acc)
        if self.sub_state == self.JUMP_FALL:
            self.max_hori_speed = max(0.0, self.max_hori_speed - self.fall_hori_acc * dt)
        cur_speed = self.jump_hori_vec.length
        if cur_speed > self.max_hori_speed:
            self.jump_hori_vec.normalize()
            self.jump_hori_vec *= self.max_hori_speed
        speed = self.jump_hori_vec
        if self.sub_state == self.JUMP_UP:
            speed.y = self.ver_move_speed - self.jump_gravity * self.sub_sid_timer
        elif self.sub_state == self.JUMP_FALL:
            speed.y = -self.fall_gravity * self.sub_sid_timer
        self.air_walk_direction_setter.execute(speed)

    def check_transitions(self):
        if self._can_break and self.sd.ref_rocker_dir:
            return MC_MOVE

    def end_btn_down(self):
        if not self.btn_down:
            return
        else:
            self.btn_down = False
            if self.ev_g_is_avatar():
                global_data.ui_mgr.close_ui('MechaCancelUI')
                self.send_event('E_ACTION_UP', self.bind_action_id)
            self.sound_drive.end_custom_sound('loop_state')
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND, MC_MOVE), None)
            self.send_event('E_SLOW_DOWN', False)
            self.send_event('E_HIDE_JUMP_TRACK')
            if self.track_timer_id:
                global_data.game_mgr.unregister_logic_timer(self.track_timer_id)
                self.track_timer_id = None
            return

    def destroy(self):
        super(PoisonJump8034, self).destroy()
        global_data.emgr.update_dash_trigger_type_8034 -= self.on_trigger_type_changed
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        return