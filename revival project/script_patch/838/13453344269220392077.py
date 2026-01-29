# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8033.py
from __future__ import absolute_import
from .StateBase import StateBase
from .Logic8020 import check_space_enough_for_trans_to_human
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3, PART_WEAPON_POS_MAIN4, PART_WEAPON_POS_MAIN5
from .ShootLogic import AccumulateShootPure
from .Logic8009 import Run8009
from .JumpLogic import OnGround
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.common_const.mecha_const import MECHA_PATTERN_NORMAL, MECHA_PATTERN_VEHICLE
from logic.gutils.angle_utils import get_angle_difference, CIRCLE_ANGLE
from logic.vscene.parts.PartShootManager import CIRCLE_ANGLE, UP_VECTOR
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_9
from logic.client.const.camera_const import FREE_MODEL
from logic.gcommon.const import NEOX_UNIT_SCALE
from math import radians, sqrt, fabs, pi, cos, sin, pi
from logic.gcommon.common_const.idx_const import ExploderID
from common.utils.timer import CLOCK
from common.cfg import confmgr
from logic.gcommon import editor
import math3d
import random
import math
import collision
import world
import game3d
from mobile.common.IdManager import IdManager
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.comsys.battle.BattleUtils import can_fire
import logic.gcommon.common_const.weapon_const as w_const
from logic.gcommon.common_const.skill_const import SKILL_8033_TRANSFORM
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.behavior.ShootLogic import Reload
import time
from logic.client.const.camera_const import FREE_CAMERA_LIST
from .JumpLogic import JumpUpWithForceDec

def is_game_over():
    bat = global_data.battle
    if bat:
        return bat.is_settle
    return True


def get_cur_pitch_and_yaw(state):
    gun_models = state.sd.ref_socket_res_agent.model_res_map.get('gun')
    pedestal_models = state.sd.ref_socket_res_agent.model_res_map.get('pedestal')
    model = state.ev_g_model()
    scn = world.get_active_scene()
    if model and gun_models and pedestal_models and scn and scn.active_camera:
        start_pos = scn.active_camera.world_position
        dir = scn.active_camera.world_rotation_matrix.forward
        final_rotate = scn.active_camera.world_rotation_matrix
        end_pos = start_pos + dir * 400 * NEOX_UNIT_SCALE
        start_pos = gun_models[0].world_position
        if state.sd.car_gun_rotation_pitch is not None:
            final_pitch = state.sd.car_gun_rotation_pitch
        else:
            final_pitch = (end_pos - start_pos).pitch
        limit_pitch = max(min(final_pitch, 0), -0.25 * pi)
        if state.sd.car_gun_rotation_yaw is not None:
            final_yaw = state.sd.car_gun_rotation_yaw
        else:
            final_yaw = final_rotate.yaw
        return (limit_pitch, final_yaw)
    else:
        return (0, 0)


def update_gun(state, dt):
    if is_game_over():
        return
    if not global_data.cam_data:
        return
    cur_camera_state = global_data.cam_data.camera_state_type
    if cur_camera_state in FREE_CAMERA_LIST:
        return
    gun_models = state.sd.ref_socket_res_agent.model_res_map.get('gun')
    pedestal_models = state.sd.ref_socket_res_agent.model_res_map.get('pedestal')
    state.sd.gun_rotation_progress = min(state.sd.gun_rotation_progress + dt, 1.0)
    if gun_models and pedestal_models:
        limit_pitch, final_yaw = get_cur_pitch_and_yaw(state)
        last_pitch, last_yaw = state.sync_pitch_and_yaw
        if abs(limit_pitch - last_pitch) > 0.1 or abs(final_yaw - last_yaw) > 0.1:
            state.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_SET_GUN_PITCH_AND_YAW_8033, (limit_pitch, final_yaw)))
            state.sync_pitch_and_yaw = (limit_pitch, final_yaw)
        old_mat = gun_models[0].rotation_matrix
        off_mat = math3d.matrix.make_orient(math3d.vector(0, -1, 0), math3d.vector(-1, 0, 0))
        x_rotate = math3d.matrix.make_rotation_x(limit_pitch)
        y_rotate = math3d.matrix.make_rotation_y(final_yaw)
        new_mat = off_mat * x_rotate * y_rotate
        local_rot = math3d.matrix_to_rotation(old_mat)
        local_rot.slerp(local_rot, math3d.matrix_to_rotation(new_mat), state.sd.gun_rotation_progress)
        gun_models[0].rotation_matrix = math3d.rotation_to_matrix(local_rot)
        off_mat = math3d.matrix.make_orient(math3d.vector(0, 0, 1), math3d.vector(-1, 0, 0))
        pedestal_models[0].rotation_matrix = off_mat * y_rotate


@editor.state_exporter({('switch_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('switch_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('switch_back_time', 'param'): {'zh_name': '\xe8\xbf\x9e\xe7\xbb\xad\xe5\x8f\x98\xe5\xbd\xa2\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'}})
class CarSwitch(StateBase):
    BIND_EVENT = {'E_FORCE_SWITCH_MODE_8033': 'on_force_switch_mode'
       }
    STATE_SWITCH = 0

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.switch_anim_rate = self.custom_param.get('switch_anim_rate', 1.0)
        self.switch_anim_name = self.custom_param.get('switch_anim_name', None)
        self.switch_anim_move_name = self.custom_param.get('switch_anim_move_name', None)
        self.switch_gun_time = self.custom_param.get('switch_gun_time', 0.5) / self.switch_anim_rate
        self.switch_gun_move_time = self.custom_param.get('switch_gun_move_time', 0.764) / self.switch_anim_rate
        self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 1.0) / self.switch_anim_rate
        self.switch_anim_move_duration = self.custom_param.get('switch_anim_move_duration', 1.625) / self.switch_anim_rate
        self.switch_back_time = self.custom_param.get('switch_back_time', 0.8) / self.switch_anim_rate
        self.switch_break_time = self.custom_param.get('switch_break_time', 0.8) / self.switch_anim_rate
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_SWITCH, 0.0, self.on_begin_switch)
        switch_anim_duration = self.switch_anim_duration
        if self.sd.ref_cur_speed and self.sd.ref_cur_speed > 0:
            switch_anim_duration = self.switch_anim_move_duration
            if self.sd.ref_is_car_shape:
                self.register_substate_callback(self.STATE_SWITCH, self.switch_gun_move_time, self.on_hide_gun)
            else:
                self.register_substate_callback(self.STATE_SWITCH, self.switch_gun_move_time, self.on_show_gun)
        elif self.sd.ref_is_car_shape:
            self.register_substate_callback(self.STATE_SWITCH, self.switch_gun_time, self.on_hide_gun)
        else:
            self.register_substate_callback(self.STATE_SWITCH, self.switch_gun_time, self.on_show_gun)
        self.register_substate_callback(self.STATE_SWITCH, self.switch_break_time, self.on_break_switch)
        self.register_substate_callback(self.STATE_SWITCH, switch_anim_duration, self.on_end_switch)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(CarSwitch, self).init_from_dict(unit_obj, bdict, sid, info)
        self.sd.ref_is_switching_shape = False
        self.read_data_from_custom_param()
        self.new_custom_param = self.custom_param
        self.sound_param_delay_refresh = True
        self.sd.gun_rotation_progress = 1.0
        self.sync_pitch_and_yaw = get_cur_pitch_and_yaw(self)
        self.to_human_dec_speed = 0.0

    def on_skill_fuel_exhausted(self, skill_id):
        if skill_id == SKILL_8033_TRANSFORM:
            self.action_btn_down()

    def action_btn_down(self):
        super(CarSwitch, self).action_btn_down()
        if not self.check_can_active():
            return False
        if MC_OTHER_SECOND_WEAPON_ATTACK in self.ev_g_cur_state():
            return False
        if self.sd.ref_is_car_shape and not check_space_enough_for_trans_to_human(self):
            return False
        if self.is_active:
            if self.sub_sid_timer < self.switch_back_time:
                return False
            self.check_custom_param_refreshed()
            self.reset_sub_state_timer()
        else:
            self.active_self()
        return True

    def check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()
            self._check_sound_param_refresh()

    def enter(self, leave_states):
        super(CarSwitch, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.register_callbacks()
        self.sub_state = self.STATE_SWITCH
        self.send_event('E_DO_RELOAD_SFX_AND_VOICE_APPEARANCE', False)
        self.sd.ref_is_switching_shape = True

    def on_show_gun--- This code section failed: ---

 188       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'send_event'
           6  LOAD_CONST            1  'E_SHOW_GUN_8033'
           9  LOAD_GLOBAL           1  'True'
          12  CALL_FUNCTION_2       2 
          15  POP_TOP          

 189      16  LOAD_GLOBAL           2  'update_gun'
          19  LOAD_GLOBAL           2  'update_gun'
          22  CALL_FUNCTION_2       2 
          25  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 22

    def on_hide_gun--- This code section failed: ---

 192       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'send_event'
           6  LOAD_CONST            1  'E_SHOW_GUN_8033'
           9  LOAD_GLOBAL           1  'False'
          12  CALL_FUNCTION_2       2 
          15  POP_TOP          

 193      16  LOAD_GLOBAL           2  'update_gun'
          19  LOAD_GLOBAL           2  'update_gun'
          22  CALL_FUNCTION_2       2 
          25  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 22

    def on_begin_switch(self):
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.switch_anim_rate)
        if self.sd.ref_cur_speed > 0:
            anim_name = self.switch_anim_move_name
        else:
            anim_name = self.switch_anim_name
        self.send_event('E_POST_ACTION', anim_name, LOW_BODY, 1)
        if self.sd.ref_is_car_shape:
            self.to_human_dec_speed = self.sd.ref_cur_speed / self.switch_anim_move_duration
            self.send_event('E_END_SKILL', self.skill_id)
            self.send_event('E_DISABLE_STATE', MC_VEHICLE)
        else:
            self.send_event('E_DO_SKILL', self.skill_id, MECHA_PATTERN_VEHICLE)
            self.send_event('E_ACTIVE_STATE', MC_VEHICLE)

    def on_end_switch(self):
        self.disable_self()

    def on_break_switch(self):
        if self.sd.ref_is_car_shape:
            self.send_event('E_ADD_WHITE_STATE', {MC_OTHER_SHOOT, MC_OTHER_SECOND_WEAPON_ATTACK, MC_OTHER_DASH}, self.sid)
        else:
            self.disable_self()
        if not self.sd.ref_on_ground:
            self.send_event('E_ACTIVE_STATE', MC_JUMP_2)
        elif self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
            self.send_event('E_ACTIVE_STATE', MC_MOVE)

    def get_move_dir(self):
        move_dir = self.ev_g_get_walk_direction()
        if move_dir and not move_dir.is_zero:
            move_dir.normalize()
        else:
            move_dir = self.ev_g_forward()
        return move_dir

    def update(self, dt):
        super(CarSwitch, self).update(dt)
        update_gun(self, dt)
        if self.to_human_dec_speed:
            speed = self.sd.ref_cur_speed - self.to_human_dec_speed * dt
            if speed < 0:
                speed = 0
            self.sd.ref_cur_speed = speed
            self.send_event('E_SET_WALK_DIRECTION', self.get_move_dir() * speed)

    def exit(self, enter_states):
        super(CarSwitch, self).exit(enter_states)
        self.check_custom_param_refreshed()
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.reset_sub_state_timer()
        self.sd.ref_is_switching_shape = False

    def refresh_action_param(self, action_param, custom_param):
        if custom_param:
            self.new_custom_param = custom_param
            if not self.is_active:
                self.check_custom_param_refreshed()

    def on_force_switch_mode(self):
        self.action_btn_down()


@editor.state_exporter({('hit_interval', 'param'): {'zh_name': '\xe5\x90\x8c\xe4\xb8\x80\xe5\x8d\x95\xe4\xbd\x8d\xe6\x94\xbb\xe5\x87\xbb\xe9\x97\xb4\xe9\x9a\x94\xef\xbc\x88\xe7\xa7\x92\xef\xbc\x89'},('step_height', 'param'): {'zh_name': '\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6'},('acc_speed', 'meter'): {'zh_name': '\xe9\xbb\x98\xe8\xae\xa4\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('max_speed', 'meter'): {'zh_name': '\xe9\xbb\x98\xe8\xae\xa4\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('min_turning_angle_boundary', 'angle'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turning_speed_data()
                                             },
   ('max_turning_acc_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('max_turning_max_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('min_turning_dec_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('max_turning_angle_boundary', 'angle'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turning_speed_data()
                                             },
   ('min_turning_acc_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('min_turning_max_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('max_turning_dec_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('air_acc_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('air_max_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('air_dec_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'},('max_anim_move_dir_angle', 'angle'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbe\xe6\x96\x9c\xe5\xaf\xb9\xe5\xba\x94\xe8\xa7\x92\xe5\xba\xa6'},('min_angle_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                     },
   ('min_turn_speed', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                 },
   ('mid_angle_boundary', 'angle'): {'zh_name': '\xe4\xb8\xad\xe9\x97\xb4\xe8\xa7\x92 \xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                     },
   ('mid_turn_speed', 'angle'): {'zh_name': '\xe4\xb8\xad\xe9\x97\xb4\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                 },
   ('max_angle_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                     },
   ('max_turn_speed', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                 },
   ('min_offset_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                      },
   ('min_offset_angle', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                   },
   ('max_offset_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                      },
   ('max_offset_angle', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                   }
   })
class CarMode8033(StateBase):
    BIND_EVENT = {'E_IMMOBILIZED': 'on_immobilized',
       'E_ON_FROZEN': 'on_frozen',
       'E_ON_BEAT_BACK': 'on_beat_back',
       'E_ON_DASHING': 'on_dashing',
       'E_REFRESH_CAR_MODE_COVERED_FUNCTION': 'refresh_covered_function',
       'G_STATE_DEFAULT_CAMERA': 'get_state_default_camera',
       'E_STOP_MOVE_8033': 'on_stop_move',
       'E_EXECUTE_GUN_ROTATE_SOUND': 'on_execute_gun_rotate_sound',
       'E_ENABLE_BEHAVIOR': ('on_enable_behavior', 99)
       }
    IMMOBILIZE_MASK = 1
    FROZEN_MASK = 2
    BEAT_BACK_MASK = 4
    DASH_MASK = 8
    FULL_MASK = 15
    MAX_TWIST_ANGLE = 75
    HIT_TARGET_TAG_VALUE = register_unit_tag(('LPuppet', 'LPuppetRobot', 'LAttachable'))

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 802055)
        self.hit_interval = self.custom_param.get('hit_interval', 3)
        self.acc_speed = self.custom_param.get('acc_speed', 40) * NEOX_UNIT_SCALE
        self.max_speed = self.custom_param.get('max_speed', 20) * NEOX_UNIT_SCALE
        self.min_turning_angle_boundary = radians(self.custom_param.get('min_turning_angle_boundary', 10))
        self.max_turning_acc_speed = self.custom_param.get('max_turning_acc_speed', 80) * NEOX_UNIT_SCALE
        self.max_turning_max_speed = self.custom_param.get('max_turning_max_speed', 18) * NEOX_UNIT_SCALE
        self.min_turning_dec_speed = self.custom_param.get('dec_turning_dec_speed', 20) * NEOX_UNIT_SCALE
        self.max_turning_angle_boundary = radians(self.custom_param.get('max_turning_angle_boundary', 80))
        self.min_turning_acc_speed = self.custom_param.get('min_turning_acc_speed', 20) * NEOX_UNIT_SCALE
        self.min_turning_max_speed = self.custom_param.get('min_turning_max_speed', 10) * NEOX_UNIT_SCALE
        self.max_turning_dec_speed = self.custom_param.get('max_turning_dec_speed', 50) * NEOX_UNIT_SCALE
        self._update_turning_speed_data()
        self.air_acc_speed = self.custom_param.get('air_acc_speed', 25) * NEOX_UNIT_SCALE
        self.air_max_speed = self.custom_param.get('air_max_speed', 12) * NEOX_UNIT_SCALE
        self.air_dec_speed = self.custom_param.get('air_dec_speed', 30) * NEOX_UNIT_SCALE
        self.max_anim_move_dir_angle = radians(self.custom_param.get('max_anim_move_dir_angle', 120))
        self.min_angle_boundary = radians(self.custom_param.get('min_angle_boundary', 2))
        self.min_turn_speed = radians(self.custom_param.get('min_turn_speed', 5))
        self.mid_angle_boundary = radians(self.custom_param.get('mid_angle_boundary', 5))
        self.mid_turn_speed = radians(self.custom_param.get('mid_turn_speed', 15))
        self.max_angle_boundary = radians(self.custom_param.get('max_angle_boundary', 70))
        self.max_turn_speed = radians(self.custom_param.get('max_turn_speed', 60))
        self._update_turn_speed_data()
        self.min_offset_boundary = radians(self.custom_param.get('min_offset_boundary', 70))
        self.min_offset_angle = radians(self.custom_param.get('min_offset_angle', 1))
        self.max_offset_boundary = radians(self.custom_param.get('max_offset_boundary', 120))
        self.max_offset_angle = radians(self.custom_param.get('max_offset_angle', 3))
        self.step_height = self.custom_param.get('step_height', 1.0) * NEOX_UNIT_SCALE
        self._update_offset_angle_data()

    def _update_turning_speed_data(self):
        boundary_distance = self.max_turning_angle_boundary - self.min_turning_angle_boundary
        self.turning_acc_speed_rate = (self.max_turning_acc_speed - self.min_turning_acc_speed) / boundary_distance
        self.turning_max_speed_rate = (self.max_turning_max_speed - self.min_turning_max_speed) / boundary_distance
        self.turning_dec_speed_rate = (self.max_turning_dec_speed - self.min_turning_dec_speed) / boundary_distance

    def _update_turn_speed_data(self):
        self.angle_boundary_data = (
         self.min_angle_boundary, self.mid_angle_boundary, self.max_angle_boundary)
        self.turn_speed_data = (self.min_turn_speed, self.mid_turn_speed, self.max_turn_speed)
        self.angle_speed_rate_data = (
         0.0,
         (self.mid_turn_speed - self.min_turn_speed) / (self.mid_angle_boundary - self.min_angle_boundary),
         (self.max_turn_speed - self.mid_turn_speed) / (self.max_angle_boundary - self.mid_angle_boundary))

    def _update_offset_angle_data(self):
        self.mid_offset_angle_rate = (self.max_offset_angle - self.min_offset_angle) / (self.max_offset_boundary - self.min_offset_boundary)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(CarMode8033, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.stop_mask = 0
        self.stopped = False
        self.target_yaw = 0
        self.last_update_target_direction_time_stamp = 0
        self.last_turn_dir = -1
        self.cur_turn_speed = 0.0
        self.turning_with_offset = False
        self.offset_angle = 0.0
        self.offset_angle_symbol = 1
        self.clearing_offset = False
        self.speed_up_factor = 0.0
        self.cur_speed = 0.0
        self.playing_sound = False
        self.sound_rtpc_value = 0.0
        self._dash_dis = 0
        self._old_pos = None
        self.enable_param_changed_by_buff()
        self.slow_down_rate = 1.0
        self.joystick_stop = True
        self.lock_joystick_stop = set()
        self.sd.car_gun_rotation_pitch = None
        self.sd.car_gun_rotation_yaw = None
        self.sd.gun_rotation_progress = 1.0
        self.playing_gun_rotating_sound = False
        self.sync_pitch_and_yaw = get_cur_pitch_and_yaw(self)
        return

    def on_stop_move(self, key, is_stop):
        if is_stop:
            self.lock_joystick_stop.add(key)
        elif key in self.lock_joystick_stop:
            self.lock_joystick_stop.remove(key)

    def enable_car_drive(self, flag):
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', not flag)
        if MC_DASH not in self.ev_g_cur_state():
            self.refresh_covered_function(flag)
        if flag:
            self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8033_4.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8033_4.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8033_3.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8033_6.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action7', 'gui/ui_res_2/battle/mech_main/icon_mech8033_8.png', 'show')
            self.target_yaw = self.sd.ref_logic_trans.yaw_target
        else:
            self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8033_2.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8033_2.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8033_1.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8033_5.png', 'show')
            self.send_event('E_SET_ACTION_ICON', 'action7', 'gui/ui_res_2/battle/mech_main/icon_mech8033_7.png', 'show')

    def enter(self, leave_states):
        super(CarMode8033, self).enter(leave_states)
        self.stop_mask = 0
        self.sd.ref_cur_speed = self.max_speed * self.ev_g_get_speed_scale() * self.slow_down_rate
        self.cur_speed = self.sd.ref_cur_speed
        self.last_cam_yaw = None
        scn = world.get_active_scene()
        if self.sd.ref_rocker_dir:
            if scn and scn.active_camera:
                dir = scn.active_camera.world_rotation_matrix.forward
                self.last_cam_yaw = dir.yaw
        self.cur_turn_speed = 0.0
        self.turning_with_offset = False
        self.offset_angle = 0.0
        self.offset_angle_symbol = 1
        self.clearing_offset = False
        self.enable_car_drive(True)
        self.send_event('E_SET_MECAH_MODE', MECHA_PATTERN_VEHICLE)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        self.playing_sound = False
        self.send_event('E_ENABLE_MECHA_FOOT_IK', False)
        self.send_event('E_SHOW_ACTION_PROGRESSS', 'action1', True)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_OTHER_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_OTHER_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_OTHER_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action4', MC_OTHER_SECOND_WEAPON_ATTACK)
        self.send_event('E_SWITCH_ACTION', 'action6', MC_OTHER_DASH)
        self.send_event('E_SET_ACTION_NB_VISIBLE', 'action5', False)
        self.send_event('E_MECHA_VEHICLE_SPREAD')
        self.send_event('E_STEP_HEIGHT', self.step_height)
        return

    def _update_sound_state(self):
        need_play_sound = bool(self.stop_mask == 0 and self.sd.ref_on_ground and self.cur_speed > 0)
        if self.playing_sound ^ need_play_sound:
            self.playing_sound = need_play_sound
            if self.playing_sound:
                self.start_custom_sound('driving')
                self.end_custom_sound('stop')
            else:
                self.end_custom_sound('driving')
                self.start_custom_sound('stop')

    def _get_turn_speed(self, angle):
        for i, boundary_angle in enumerate(self.angle_boundary_data):
            if angle <= boundary_angle:
                if i > 0:
                    return self.turn_speed_data[i - 1] + self.angle_speed_rate_data[i] * (angle - self.angle_boundary_data[i - 1])
                return self.turn_speed_data[i]
        else:
            return self.turn_speed_data[-1]

    def _update_rotation(self):
        cur_yaw_target = self.target_yaw + self.offset_angle * self.offset_angle_symbol
        cur_yaw_target %= CIRCLE_ANGLE
        cur_yaw = self.sd.ref_rotatedata.yaw_head
        angle, symbol = get_angle_difference(cur_yaw, cur_yaw_target)
        if angle == 0:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        else:
            ratio = angle / self.max_anim_move_dir_angle
            if ratio > 1.0:
                ratio = 1.0
            x = ratio
            z = sqrt(1.0 - x * x)
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', x * symbol, z)
        if self.playing_sound:
            new_value = angle * 100.0 / pi
            if new_value != self.sound_rtpc_value:
                global_data.sound_mgr.set_rtpc_ex('car_drift', new_value)
                self.sound_rtpc_value = new_value
        if angle == 0:
            if self.turning_with_offset:
                self.turning_with_offset = False
                self.offset_angle = 0.0
                self.offset_angle_symbol = 0
                angle = fabs(cur_yaw - self.target_yaw)
                self.clearing_offset = True
            elif self.clearing_offset:
                self.clearing_offset = False
        turn_speed = self.min_turn_speed if self.clearing_offset else self._get_turn_speed(angle)
        cur_yaw_target = self.target_yaw + self.offset_angle * self.offset_angle_symbol
        if self.sd.ref_logic_trans.yaw_target != cur_yaw_target or turn_speed != self.cur_turn_speed:
            self.sd.ref_logic_trans.yaw_target = cur_yaw_target
            self.sd.ref_common_motor.set_yaw_time(angle / turn_speed)
            self.cur_turn_speed = turn_speed

    def _get_offset_angle(self, angle):
        if angle <= self.min_offset_boundary:
            return self.min_offset_angle
        if angle <= self.max_offset_boundary:
            return self.min_offset_angle + self.mid_offset_angle_rate * (angle - self.min_offset_boundary)
        return self.max_offset_angle

    def _update_offset_angle(self):
        if self.clearing_offset:
            self.clearing_offset = False
        cur_yaw = self.sd.ref_rotatedata.yaw_head
        angle, symbol = get_angle_difference(cur_yaw, self.target_yaw)
        if symbol:
            if angle >= self.min_offset_boundary:
                self.turning_with_offset = True
                self.offset_angle = self._get_offset_angle(angle)
                self.offset_angle_symbol = symbol
            else:
                self.turning_with_offset = False
                self.offset_angle = 0.0
                self.offset_angle_symbol = 0
        else:
            self.turning_with_offset = False
            self.offset_angle = 0.0
            self.offset_angle_symbol = 0

    def is_joystick_stop(self):
        return self.joystick_stop or bool(self.lock_joystick_stop)

    def _update_cur_speed(self, dt, angle_difference):
        cur_speed = self.cur_speed
        if self.sd.ref_on_ground:
            if angle_difference > 0:
                if angle_difference < self.min_turning_angle_boundary:
                    acc_speed, max_speed, dec_speed = self.max_turning_acc_speed, self.max_turning_max_speed, self.min_turning_dec_speed
                elif angle_difference < self.max_turning_angle_boundary:
                    acc_speed = self.max_turning_acc_speed - angle_difference * self.turning_acc_speed_rate
                    max_speed = self.max_turning_max_speed - angle_difference * self.turning_max_speed_rate
                    dec_speed = self.min_turning_dec_speed + angle_difference * self.turning_dec_speed_rate
                else:
                    acc_speed, max_speed, dec_speed = self.min_turning_acc_speed, self.min_turning_max_speed, self.max_turning_dec_speed
            else:
                acc_speed, max_speed, dec_speed = self.acc_speed, self.max_speed, self.air_dec_speed
        else:
            acc_speed, max_speed, dec_speed = self.air_acc_speed, self.air_max_speed, self.air_dec_speed
        dec_speed = max(cur_speed * 0.5, dec_speed)
        if self.is_joystick_stop():
            max_speed = 0
        else:
            max_speed *= 1.0 + self.speed_up_factor
        if cur_speed > max_speed:
            cur_speed -= dec_speed * dt
            if cur_speed < max_speed:
                cur_speed = max_speed
        elif cur_speed < max_speed:
            cur_speed += acc_speed * dt
            if cur_speed > max_speed:
                cur_speed = max_speed
        self.cur_speed = cur_speed

    def _update_cur_anim(self):
        is_move = self.sd.ref_is_switching_shape or self.cur_speed > 0
        if is_move:
            target_anim = 'tank_move_f' if 1 else 'tank_idle02'
            if self.sd.ref_low_body_anim != target_anim:
                self.send_event('E_POST_ACTION', target_anim, LOW_BODY, 1, loop=True)
                self.send_event('E_MECHA_VEHICLE_SPREAD')

    def update(self, dt):
        super(CarMode8033, self).update(dt)
        update_gun(self, dt)
        need_play_gun_rotate_sound = self.sd.gun_rotation_progress < 1.0
        if self.playing_gun_rotating_sound ^ need_play_gun_rotate_sound:
            self.playing_gun_rotating_sound = need_play_gun_rotate_sound
            if need_play_gun_rotate_sound:
                self.start_custom_sound('gun_rotate')
            else:
                self.end_custom_sound('gun_rotate')
        if self.sd.ref_rocker_dir:
            self.joystick_stop = False
        else:
            self.joystick_stop = True
        self._update_sound_state()
        cur_yaw = self.sd.ref_rotatedata.yaw_head
        if self.stop_mask:
            if not self.stopped:
                if self.stop_mask & self.DASH_MASK == 0 and self.stop_mask & self.BEAT_BACK_MASK == 0:
                    self.sd.ref_logic_trans.yaw_target = cur_yaw
                    self.sd.ref_cur_speed = self.cur_speed = 0
                    self.sd.ref_cur_speed = self.cur_speed = 0
                    cur_dir = math3d.vector(0, 0, 0)
                    if self.ev_g_get_walk_direction() != cur_dir:
                        self.send_event('E_SET_WALK_DIRECTION', cur_dir)
                self.stopped = True
            return
        if self.is_joystick_stop() and self.cur_speed <= 0:
            self.sd.ref_logic_trans.yaw_target = cur_yaw
            self.sd.ref_cur_speed = self.cur_speed = 0
            cur_dir = math3d.vector(0, 0, 0)
            if self.ev_g_get_walk_direction() != cur_dir:
                self.send_event('E_SET_WALK_DIRECTION', cur_dir)
            return
        if self.stopped:
            self.stopped = False
        scn = world.get_active_scene()
        if self.sd.ref_rocker_dir:
            if scn and scn.active_camera:
                if global_data.cam_state_type != FREE_MODEL:
                    dir = scn.active_camera.world_rotation_matrix.forward
                    self.last_cam_yaw = dir.yaw
                elif not self.last_cam_yaw:
                    dir = scn.active_camera.world_rotation_matrix.forward
                    self.last_cam_yaw = dir.yaw
                self.target_yaw = self.last_cam_yaw + self.sd.ref_rocker_dir.yaw
        self._update_rotation()
        self._update_cur_speed(dt, get_angle_difference(cur_yaw, self.target_yaw)[0])
        self._update_cur_anim()
        self.sd.ref_cur_speed = self.cur_speed * self.ev_g_get_speed_scale() * self.slow_down_rate
        rot = math3d.rotation(0, 0, 0, 1)
        rot.set_axis_angle(UP_VECTOR, cur_yaw)
        cur_dir = rot.get_forward() * self.sd.ref_cur_speed
        if self.ev_g_get_walk_direction() != cur_dir:
            self.send_event('E_SET_WALK_DIRECTION', cur_dir)
        self.send_event('E_ACTION_MOVE')

    def exit(self, enter_states):
        super(CarMode8033, self).exit(enter_states)
        self.enable_car_drive(False)
        self.send_event('E_SET_MECAH_MODE', MECHA_PATTERN_NORMAL)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
        scn = world.get_active_scene()
        if global_data.cam_data.cam_yaw_before_enter_free:
            self.sd.ref_logic_trans.yaw_target = global_data.cam_data.cam_yaw_before_enter_free
            self.sd.ref_common_motor.set_yaw_time(0.2)
        elif scn and scn.active_camera:
            dir = scn.active_camera.world_rotation_matrix.forward
            self.sd.ref_logic_trans.yaw_target = dir.yaw
            self.sd.ref_common_motor.set_yaw_time(0.2)
        self.send_event('E_ACTION_MOVE_STOP')
        self.playing_sound = False
        self.end_custom_sound('driving')
        self.end_custom_sound('stop')
        self.playing_gun_rotating_sound = False
        self.end_custom_sound('gun_rotate')
        self.send_event('E_ENABLE_MECHA_FOOT_IK', True)
        self.send_event('E_SHOW_ACTION_PROGRESSS', 'action1', False)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action4', MC_SECOND_WEAPON_ATTACK)
        self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH)
        self.send_event('E_SET_ACTION_NB_VISIBLE', 'action5', True)
        self.send_event('E_RESET_STEP_HEIGHT')

    def _update_stop_mask(self, flag, mask):
        if not self.ev_g_is_avatar() and not self.ev_g_is_agent():
            return
        if flag:
            self.stop_mask |= mask
        else:
            self.stop_mask &= self.FULL_MASK ^ mask

    def on_immobilized(self, immobilized, *args, **kwargs):
        self._update_stop_mask(immobilized, self.IMMOBILIZE_MASK)

    def on_frozen(self, frozen, *args, **kwargs):
        self._update_stop_mask(frozen, self.FROZEN_MASK)

    def on_beat_back(self, beat_back):
        self._update_stop_mask(beat_back, self.BEAT_BACK_MASK)

    def on_dashing(self, dashing):
        self._update_stop_mask(dashing, self.DASH_MASK)

    def refresh_covered_function(self, flag, change_align_on_ground=True):
        change_align_on_ground and self.send_event('E_ENABLE_ALIGN_ON_GROUND', flag, self.MAX_TWIST_ANGLE)

    def on_contact_targets(self, target_list):
        for index in range(len(target_list) - 1, -1, -1):
            if target_list[index].MASK & self.HIT_TARGET_TAG_VALUE == 0:
                target_list.pop(index)

        if target_list:
            target_id_tuple = [ target.id for target in target_list ]
            self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, target_id_tuple), False, True)

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8033', MECHA_MEMORY_LEVEL_9, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def get_state_default_camera(self):
        if self.is_active:
            return self.state_camera_conf.get('cam')
        else:
            return None

    def on_execute_gun_rotate_sound(self, flag):
        if flag:
            self.start_custom_sound('gun_rotate')
        else:
            self.end_custom_sound('gun_rotate')

    def on_enable_behavior(self, *args):
        if self.sd.ref_is_car_shape:
            self.active_self()


class CarDash8033(StateBase):
    BIND_EVENT = {}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(CarDash8033, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        super(CarDash8033, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(CarDash8033, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.disable_self()

    def exit(self, enter_states):
        super(CarDash8033, self).exit(enter_states)


@editor.state_exporter({('pre_aim_ik_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe7\x94\xa8IK\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4'},('aim_ik_lerp_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe7\x94\xa8IK\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('support_exit_aim_ik_lerp', 'param'): {'zh_name': '\xe6\x94\xaf\xe6\x8c\x81\xe9\x80\x80\xe5\x87\xbaIK\xe6\x8f\x92\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1'},('exit_aim_ik_lerp_time', 'param'): {'zh_name': '\xe9\x80\x80\xe5\x87\xbaIK\xe6\x8f\x92\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('aim_ik_pitch_limit', 'param'): {'zh_name': 'IK\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbf\xaf\xe4\xbb\xb0\xe8\xa7\x92\xe9\x99\x90\xe5\x88\xb6'}})
class ThrowGrenade8033(AccumulateShootPure):
    BIND_EVENT = AccumulateShootPure.BIND_EVENT.copy()
    BIND_EVENT.update({'E_GRENADE_EXPLODED': 'on_grenade_exploded'
       })
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD}

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ThrowGrenade8033, self).init_from_dict(unit_obj, bdict, sid, info)
        self.low_body_idle_anim_replaced = False

    def read_data_from_custom_param(self):
        super(ThrowGrenade8033, self).read_data_from_custom_param()
        self.main_weapon_pos = PART_WEAPON_POS_MAIN2
        self.sub_weapon_pos = PART_WEAPON_POS_MAIN3
        self.post_anim_blend_time = self.custom_param.get('post_anim_blend_time', 0.0)
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_pitch_limit = self.custom_param.get('aim_ik_pitch_limit', 80)
        self.support_exit_aim_ik_lerp = self.custom_param.get('support_exit_aim_ik_lerp', True)
        self.exit_aim_ik_lerp_time = self.custom_param.get('exit_aim_ik_lerp_time', 0.2)
        return

    def _reset_aim_ik_param(self):
        if self.shoot_aim_ik:
            self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, self.support_exit_aim_ik_lerp)
            self.send_event('E_ENABLE_AIM_IK', True, self.aim_ik_pitch_limit)
            self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.exit_aim_ik_lerp_time)

    def enter(self, leave_states):
        super(ThrowGrenade8033, self).enter(leave_states)
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')
        self.delay_call(self.pre_aim_ik_time, self._reset_aim_ik_param)

    def exit(self, enter_states):
        super(ThrowGrenade8033, self).exit(enter_states)
        if self.low_body_idle_anim_replaced:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
            self.low_body_idle_anim_replaced = False
        self.send_event('E_SLOW_DOWN', False)
        self.sound_drive.custom_end()
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        return

    def _fire(self):
        self.ev_g_try_weapon_attack_begin(self.sub_weapon_pos)
        self.ev_g_try_weapon_attack_end(self.sub_weapon_pos)
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def on_grenade_exploded(self, item_info):
        pass

    def on_begin_pre(self):
        super(ThrowGrenade8033, self).on_begin_pre()
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.pre_anim_name, loop=False)
        self.low_body_idle_anim_replaced = True

    def on_begin_loop(self):
        super(ThrowGrenade8033, self).on_begin_loop()
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.loop_anim_name, loop=True)
        self.low_body_idle_anim_replaced = True

    def on_begin_post(self):
        self.send_event('E_SHOW_SEC_AIM', False)
        self.sound_drive.custom_end()
        self.skill_id and self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ACC_SKILL_END', self.weapon_pos)
        self.acc_skill_ended = True
        self._fire()
        self.send_event('E_ANIM_RATE', self.PART, self.post_anim_rate)
        self.send_event('E_POST_ACTION', self.post_anim_name, self.PART, 1, blend_time=self.post_anim_blend_time)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        self.end_custom_sound('post')
        self.start_custom_sound('post')


@editor.state_exporter({('anim_name', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d'},('anim_duration', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('anim_rate', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('bomb_radius', 'param'): {'zh_name': '\xe7\x88\x86\xe7\x82\xb8\xe5\x8c\xba\xe8\x8c\x83\xe5\x9b\xb4'},('ammo_height', 'param'): {'zh_name': '\xe8\xb5\xb7\xe5\xa7\x8b\xe9\xab\x98\xe5\xba\xa6'},('speed', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6'},('shell_num', 'param'): {'zh_name': '\xe4\xb8\x80\xe6\x89\xb9\xe5\xaf\xbc\xe5\xbc\xb9\xe6\x95\xb0'},('shoot_times', 'param'): {'zh_name': '\xe5\xaf\xbc\xe5\xbc\xb9\xe6\x89\xb9\xe6\x95\xb0'},('shoot_interval', 'param'): {'zh_name': '\xe5\xaf\xbc\xe5\xbc\xb9\xe9\x97\xb4\xe9\x9a\x94'}})
class DownpourShell(StateBase):
    BIND_EVENT = {'E_MECHA_8033_RADAR_FIRE': 'on_radar_fire'
       }
    STATE_SCAN = 0
    STATE_FIRE = 1

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.anim_name = self.custom_param.get('anim_name', None)
        self.anim_duration = self.custom_param.get('anim_duration', 1.0)
        self.anim_rate = self.custom_param.get('anim_rate', 1.0)
        self.bomb_radius = self.custom_param.get('bomb_radius', 200.0)
        self.ammo_height = self.custom_param.get('ammo_height', 3000.0)
        self.wp_type = self.custom_param.get('wp_type', 0)
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_kind = self.wp_conf.get('iKind')
        skill_conf = confmgr.get('skill_conf', str(self.skill_id))
        ext_info = skill_conf.get('ext_info', {})
        self.shell_num = ext_info.get('shell_num', 9)
        self.shoot_times = ext_info.get('shoot_times', 3)
        self.shoot_interval = self.custom_param.get('shoot_interval', 0.2)
        self.radar_fire_id = 0
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_SCAN, 0.0, self.on_begin_scan)
        self.register_substate_callback(self.STATE_FIRE, 0.0, self.on_begin_fire)
        self.register_substate_callback(self.STATE_FIRE, self.anim_duration, self.on_end_fire)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DownpourShell, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.bomb_pos = []
        self.focus_pos = None
        self.sub_index = 0
        return

    def action_btn_down(self):
        super(DownpourShell, self).action_btn_down()
        return True

    def action_btn_up(self):
        if not self.sd.ref_on_ground:
            return False
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        super(DownpourShell, self).action_btn_up()
        return True

    def _cancle_scan(self):
        self.on_radar_fire()

    def on_begin_scan(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_SCAN_ENEMY_8033')
        self.send_event('E_STOP_MOVE_8033', 'DownpourShell', True)
        self.sd.car_gun_rotation_pitch = -pi
        self.sd.gun_rotation_progress = 0.0
        self.send_event('E_GUN_MODEL_ANI_8033', 'yubei')
        self.end_custom_sound('aim')
        self.start_custom_sound('aim')

    def on_radar_fire(self, pos=None):
        self.focus_pos = pos
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        if pos:
            self.send_event('E_UPDATE_RADAR_UI', False)
            self.send_event('E_END_SKILL', self.skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
            self.sub_state = self.STATE_FIRE
            cur_pos = self.ev_g_position()
            traget_dir = math3d.vector(pos.x - cur_pos.x, pos.y - cur_pos.y, pos.z - cur_pos.z)
            self.sd.car_gun_rotation_yaw = traget_dir.yaw
            self.sd.gun_rotation_progress = 0.0
        else:
            self.disable_self()

    def on_begin_fire(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, 1)
        self.radar_fire_id = IdManager.genid()
        self.send_event('E_GUN_MODEL_ANI_8033', 'idle')
        self.end_custom_sound('fire')
        self.start_custom_sound('fire')

    def on_end_fire(self):
        self.sub_index = 0

        def _fire():
            for i in range(self.shell_num):
                self.open_fire()

        global_data.game_mgr.get_logic_timer().register(func=_fire, interval=self.shoot_interval, times=self.shoot_times, mode=CLOCK)
        self.send_event('E_CALL_SYNC_METHOD', 'create_shock_warning', ((self.focus_pos.x, 0, self.focus_pos.z), self.bomb_radius))
        self.disable_self()

    def update(self, dt):
        super(DownpourShell, self).update(dt)

    def enter(self, enter_states):
        super(DownpourShell, self).exit(enter_states)
        self.sd.ref_cur_speed = 0
        self.send_event('E_SET_WALK_DIRECTION', math3d.vector(0, 0, 0))
        self.sub_state = self.STATE_SCAN
        self.send_event('E_UPDATE_RADAR_UI', True)
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self._cancle_scan)
        return

    def exit(self, enter_states):
        super(DownpourShell, self).exit(enter_states)
        self.sd.car_gun_rotation_pitch = None
        self.sd.car_gun_rotation_yaw = None
        self.sd.gun_rotation_progress = 0.0
        self.end_custom_sound('end')
        self.start_custom_sound('end')
        self.send_event('E_UPDATE_RADAR_UI', False)
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.send_event('E_STOP_MOVE_8033', 'DownpourShell', False)
        if self.sub_state == self.STATE_FIRE:
            self.send_event('E_GUN_MODEL_ANI_8033', 'juji_idle')
        self.sub_state = None
        return

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)

    def open_fire(self):
        if not self.focus_pos:
            return
        self.sub_index += 1
        random_angle = random.randint(1, 360) * math.pi / 180
        random_r = random.uniform(0, self.bomb_radius)
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': self.wp_kind,
           'position': (
                      self.focus_pos.x + random_r * math.cos(random_angle), self.ammo_height, self.focus_pos.z + random_r * math.sin(random_angle)),
           'dir': (0, -1, 0),
           'sub_idx': self.sub_index,
           'wp_pos': PART_WEAPON_POS_MAIN4,
           'ign_pos_vrf': True,
           'atk_uid': self.radar_fire_id,
           'bomb_center': (
                         self.focus_pos.x, 0, self.focus_pos.z),
           'bomb_radius': self.bomb_radius
           }
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)


@editor.state_exporter({('aim_duration', 'param'): {'zh_name': '\xe7\x9e\x84\xe5\x87\x86\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callbacks()
                               },
   ('fire_time1', 'param'): {'zh_name': '\xe7\xac\xac1\xe5\x8f\x91\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self.register_callbacks()
                             },
   ('fire_time2', 'param'): {'zh_name': '\xe7\xac\xac2\xe5\x8f\x91\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self.register_callbacks()
                             },
   ('fire_time3', 'param'): {'zh_name': '\xe7\xac\xac3\xe5\x8f\x91\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self.register_callbacks()
                             },
   ('fire_time4', 'param'): {'zh_name': '\xe7\xac\xac4\xe5\x8f\x91\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self.register_callbacks()
                             },
   ('fire_all_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe6\x80\xbb\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                },
   ('hold_duration', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x90\x8e\xe4\xbf\x9d\xe6\x8c\x81\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callbacks()
                                },
   ('fire_anim_rate', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self.register_callbacks()
                                 },
   ('pre_aim_ik_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe7\x94\xa8IK\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4'},('aim_ik_lerp_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe7\x94\xa8IK\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('support_exit_aim_ik_lerp', 'param'): {'zh_name': '\xe6\x94\xaf\xe6\x8c\x81\xe9\x80\x80\xe5\x87\xbaIK\xe6\x8f\x92\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1'},('exit_aim_ik_lerp_time', 'param'): {'zh_name': '\xe9\x80\x80\xe5\x87\xbaIK\xe6\x8f\x92\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('aim_ik_pitch_limit', 'param'): {'zh_name': 'IK\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbf\xaf\xe4\xbb\xb0\xe8\xa7\x92\xe9\x99\x90\xe5\x88\xb6'}})
class WeaponFire8033(StateBase):
    BIND_EVENT = {'G_CONTINUE_FIRE': 'continue_fire',
       'TRY_STOP_WEAPON_ATTACK': '_end_shoot'
       }
    STATE_AIM = 0
    STATE_FIRE = 1
    STATE_HOLD = 2

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8033, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.is_continue_fire = False
        self.low_body_idle_anim_replaced = False

    def read_data_from_custom_param(self):
        self.aim_duration = self.custom_param.get('aim_duration', 0.2)
        self.hold_duration = self.custom_param.get('hold_duration', 0.6)
        self.blend_time = self.custom_param.get('blend_time', 0.0)
        self.weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN1)
        self.slow_down_on_shoot = self.custom_param.get('slow_down_on_shoot', True)
        self.slow_down_speed = self.custom_param.get('slow_down_speed', None)
        if self.slow_down_speed:
            self.slow_down_speed *= NEOX_UNIT_SCALE
        self.weapon_intensify_pos = self.custom_param.get('weapon_intensify_pos', PART_WEAPON_POS_MAIN5)
        self.fire_anim_rate = self.custom_param.get('fire_anim_rate', 1.0)
        self.fire_time1 = self.custom_param.get('fire_time1', 0.033) / self.fire_anim_rate
        self.fire_time2 = self.custom_param.get('fire_time2', 0.168) / self.fire_anim_rate
        self.fire_time3 = self.custom_param.get('fire_time3', 0.327) / self.fire_anim_rate
        self.fire_time4 = self.custom_param.get('fire_time4', 0.532) / self.fire_anim_rate
        self.break_time = self.custom_param.get('break_time', 0.6)
        self.fire_all_time = self.custom_param.get('fire_all_time', 0.867)
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_pitch_limit = self.custom_param.get('aim_ik_pitch_limit', 80)
        self.support_exit_aim_ik_lerp = self.custom_param.get('support_exit_aim_ik_lerp', True)
        self.exit_aim_ik_lerp_time = self.custom_param.get('exit_aim_ik_lerp_time', 0.2)
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_AIM, 0, self.on_begin_aim)
        self.register_substate_callback(self.STATE_AIM, self.aim_duration, self.on_end_aim)
        self.register_substate_callback(self.STATE_FIRE, 0, self.play_fire_anim)
        self.register_substate_callback(self.STATE_FIRE, self.fire_time1, self.on_fire)
        self.register_substate_callback(self.STATE_FIRE, self.fire_time2, self.on_fire)
        self.register_substate_callback(self.STATE_FIRE, self.fire_time3, self.on_fire)
        self.register_substate_callback(self.STATE_FIRE, self.fire_time4, self.on_intensify_fire)
        self.register_substate_callback(self.STATE_FIRE, self.break_time, self.on_enable_break)
        self.register_substate_callback(self.STATE_FIRE, self.fire_all_time, self.on_round_fire_finished)
        self.register_substate_callback(self.STATE_HOLD, self.hold_duration, self.on_end_hold)

    def on_enable_break(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_RELOAD, MC_SECOND_WEAPON_ATTACK, MC_DASH, MC_TRANSFORM, MC_VEHICLE}, self.sid)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_intensify_pos)
        if weapon and weapon.get_bullet_num() == 0:
            self.send_event('E_TRY_RELOAD', self.weapon_intensify_pos)

    def on_begin_aim(self):
        self.send_event('E_POST_ACTION', 'shoot', UP_BODY, 7, blend_time=self.aim_duration, phase=1.0, need_trigger_anim_effect=False)

    def on_end_aim(self):
        self.sub_state = self.STATE_FIRE

    def play_fire_anim(self):
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_ANIM_RATE', UP_BODY, self.fire_anim_rate)
        self.send_event('E_POST_ACTION', 'shoot', UP_BODY, 7, blend_time=self.blend_time, force_trigger_effect=True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, 'shoot', blend_dir=1, loop=False, blend_time=0.1)
        self.low_body_idle_anim_replaced = True

    def on_fire(self):
        self.send_event('E_TEMP_CHANGE_WEAPON_POS', self.weapon_pos)
        self.ev_g_try_weapon_attack_begin(self.weapon_pos, extra_data={'ignore_diving': True})
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def on_intensify_fire(self):
        self.send_event('E_TEMP_CHANGE_WEAPON_POS', self.weapon_intensify_pos)
        self.ev_g_try_weapon_attack_begin(self.weapon_intensify_pos, extra_data={'ignore_diving': True})
        self.ev_g_try_weapon_attack_end(self.weapon_intensify_pos)

    def on_round_fire_finished(self):
        if self.is_continue_fire and self.can_fire_plus():
            self.reset_sub_state_timer()
        else:
            self.sub_state = self.STATE_HOLD

    def on_end_hold(self):
        self.disable_self()

    def continue_fire(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not self.ev_g_is_main_weapon_enable():
            return (False, self.weapon_pos)
        if weapon and weapon.get_data_by_key('iMode') == w_const.AUTO_MODE:
            return (self.is_continue_fire, self.weapon_pos)
        return (False, self.weapon_pos)

    def can_fire_plus(self):
        if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()):
            return False
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            return False
        return True

    def action_btn_down(self, ignore_reload=False):
        self.is_continue_fire = True
        if self.is_active:
            if self.sub_state == self.STATE_HOLD and self.can_fire_plus():
                self.sub_state = self.STATE_FIRE
            return True
        if not self.can_fire_plus():
            return False
        self.active_self()
        super(WeaponFire8033, self).action_btn_down()
        return True

    def enter(self, leave_states):
        self.send_event('E_SLOW_DOWN', self.slow_down_on_shoot, self.slow_down_speed, 'WeaponFire')
        super(WeaponFire8033, self).enter(leave_states)
        self.delay_call(self.pre_aim_ik_time, self._reset_aim_ik_param)
        self.sub_state = self.STATE_AIM

    def check_can_active(self, only_avatar=True):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not weapon:
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        return self.ev_g_status_check_pass(self.sid, only_avatar=only_avatar)

    def action_btn_up(self):
        self.is_continue_fire = False
        super(WeaponFire8033, self).action_btn_up()
        return True

    def _reset_aim_ik_param(self):
        if self.shoot_aim_ik:
            self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, self.support_exit_aim_ik_lerp)
            self.send_event('E_ENABLE_AIM_IK', True, self.aim_ik_pitch_limit)
            self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.exit_aim_ik_lerp_time)

    def exit(self, enter_states):
        super(WeaponFire8033, self).exit(enter_states)
        if self.low_body_idle_anim_replaced:
            self.low_body_idle_anim_replaced = False
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire')
        if self.sd.ref_up_body_anim == 'shoot':
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        return

    def destroy(self):
        self.send_event('E_STOP_WP_TRACK')
        super(WeaponFire8033, self).destroy()

    def try_weapon_attack_end(self):
        self.disable_self()


class CarWeaponFire8033(StateBase):
    BIND_EVENT = {'G_CONTINUE_FIRE': 'continue_fire',
       'TRY_STOP_WEAPON_ATTACK': '_end_shoot'
       }
    STATE_FIRE = 0
    STATE_END_FIRE = 1

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(CarWeaponFire8033, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.is_continue_fire = False

    def read_data_from_custom_param(self):
        self.anim_name = self.custom_param.get('anim_name', 'juji_shoot')
        self.weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN1)
        self.fire_time = self.custom_param.get('fire_time', 0.5)
        self.anim_duration = self.custom_param.get('anim_duration', 1.0)
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_pitch_limit = self.custom_param.get('aim_ik_pitch_limit', 80)
        self.support_exit_aim_ik_lerp = self.custom_param.get('support_exit_aim_ik_lerp', True)
        self.exit_aim_ik_lerp_time = self.custom_param.get('exit_aim_ik_lerp_time', 0.2)
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_FIRE, 0.0, self.on_pre_fire)
        self.register_substate_callback(self.STATE_FIRE, self.fire_time, self.on_fire)
        self.register_substate_callback(self.STATE_FIRE, self.anim_duration, self.on_end_fire)

    def on_pre_fire(self):
        self.play_fire_anim()

    def play_fire_anim(self):
        if self.anim_name and (self.is_active or self.check_can_active()):
            self.send_event('E_GUN_MODEL_ANI_8033', self.anim_name)

    def on_fire(self):
        self.try_weapon_attack_end()

    def on_end_fire(self):
        self.disable_self()

    def continue_fire(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not self.ev_g_is_main_weapon_enable():
            return (False, self.weapon_pos)
        if weapon and weapon.get_data_by_key('iMode') == w_const.AUTO_MODE:
            return (self.is_continue_fire, self.weapon_pos)
        return (False, self.weapon_pos)

    def action_btn_down(self, ignore_reload=False):
        if self.is_active and self.sub_state is not None:
            return True
        else:
            if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()):
                return False
            if self.ev_g_reloading():
                return False
            if self.ev_g_weapon_reloading(self.weapon_pos):
                return False
            self.is_continue_fire = True
            if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
                self.is_continue_fire = False
                return False
            if not self.ev_g_try_weapon_attack_begin(self.weapon_pos):
                self.is_continue_fire = False
                return False
            self.active_self()
            self.register_callbacks()
            self.sub_state = self.STATE_FIRE
            super(CarWeaponFire8033, self).action_btn_down()
            return True

    def enter(self, leave_states):
        super(CarWeaponFire8033, self).enter(leave_states)
        self.delay_call(self.pre_aim_ik_time, self._reset_aim_ik_param)

    def check_can_active(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not weapon:
            return False
        return self.ev_g_status_check_pass(self.sid)

    def action_btn_up(self):
        self.is_continue_fire = False
        if not self.try_weapon_attack_end():
            return False
        super(CarWeaponFire8033, self).action_btn_up()
        return True

    def _reset_aim_ik_param(self):
        if self.shoot_aim_ik:
            self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, self.support_exit_aim_ik_lerp)
            self.send_event('E_ENABLE_AIM_IK', True, self.aim_ik_pitch_limit)
            self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.exit_aim_ik_lerp_time)

    def exit(self, enter_states):
        super(CarWeaponFire8033, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire')
        if self.sd.ref_up_body_anim == self.anim_name:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        if enter_states:
            self.try_weapon_attack_end()

    def destroy(self):
        self.send_event('E_STOP_WP_TRACK')
        self.is_continue_fire = False
        super(CarWeaponFire8033, self).destroy()

    def _end_shoot(self, *args):
        self.disable_self()

    def try_weapon_attack_end(self):
        return self.ev_g_try_weapon_attack_end(self.weapon_pos)


class Reload8033(Reload):

    def play_anim(self):
        if self.sd.ref_is_car_shape and self.reload_anim:
            if self.bind_action_id:
                self.send_event('E_START_ACTION_CD', self.bind_action_id, self.reload_time)
            self.send_event('E_GUN_MODEL_ANI_8033', self.reload_anim)
        else:
            super(Reload8033, self).play_anim()


class Run8033(Run8009):

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_state_running_time_stamp < self.stop_anim_cost_time:
            self.end_run_stop_anim()
            return
        self.end_custom_sound('brake')
        self.start_custom_sound('brake')
        super(Run8009, self).begin_run_stop_anim()


class OnGround8033(OnGround):

    def check_transitions(self):
        if self.sd.ref_is_car_shape:
            return self.status_config.MC_STAND
        else:
            return super(OnGround8033, self).check_transitions()


class JumpUp8033(JumpUpWithForceDec):

    def try_jump(self):
        if not self.sd.ref_on_ground:
            return
        super(JumpUp8033, self).try_jump()