# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8030.py
from __future__ import absolute_import
import world
import math3d
import time
from math import pi, sin, cos, tan, radians, degrees
import copy
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.ui_operation_const import ROCKER_DASH
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata import jump_physic_config
from logic.gutils.character_ctrl_utils import set_boost_dir
from logic.gcommon import editor
from .StateBase import StateBase, clamp
from .MoveLogic import Stand, Run
from .JumpLogic import JumpUp
from .ShootLogic import AccumulateShootPure
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.const import PART_WEAPON_POS_MAIN3
from logic.gcommon.component.client.com_mecha_effect.ComMechaEffect8030 import JUMP_CHARGE_EFFECT_ID, DASH_END_EFFECT_ID, DASH_END_EXTERN_BONE_EFFECT_ID
from logic.gcommon.common_const.ui_operation_const import ROCKER_JUMP_8030
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_8
from logic.gcommon.component.SimpleEventManager import com_bind_event, com_unbind_event
SHOW_DEBUG_CONTENT = False

@editor.state_exporter({('stop_anim_cost_time', 'param'): {'zh_name': '\xe6\x92\xad\xe6\x94\xbe\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x9c\x80\xe5\xb0\x91\xe8\xb7\x91\xe6\xad\xa5\xe6\x97\xb6\xe9\x97\xb4'}})
class Run8030(Run):

    def read_data_from_custom_param(self):
        super(Run8030, self).read_data_from_custom_param()
        self.stop_anim_cost_time = self.custom_param.get('stop_anim_cost_time', 3.0)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        self.enter_run_time_stamp = time.time() - 999.0
        super(Run8030, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def begin_run_anim(self):
        super(Run8030, self).begin_run_anim()
        self.enter_run_time_stamp = time.time()

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_run_time_stamp < self.stop_anim_cost_time:
            self.end_run_stop_anim()
            return
        super(Run8030, self).begin_run_stop_anim()


class Stand8030(Stand):
    BIND_EVENT = Stand.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REPLAY_STAND_ANIM': 'replay_anim'
       })

    def replay_anim(self):
        if self.is_active:
            self.play_replace_anim()


@editor.state_exporter({('min_accu_time', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe9\x97\xb4','explain': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe9\x97\xb4\xe5\xb0\x8f\xe4\xba\x8e\xe8\xbf\x99\xe4\xb8\xaa\xe5\x80\xbc\xe5\xb0\xb1\xe8\xae\xa4\xe4\xb8\xba\xe6\x98\xaf\xe6\x99\xae\xe9\x80\x9a\xe8\xb7\xb3\xe8\xb7\x83'},('max_accu_time', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe9\x97\xb4'},('max_accu_reinforce', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xb7\xb3\xe8\xb7\x83\xe5\xbc\xba\xe5\x8c\x96\xe5\x80\x8d\xe6\x95\xb0',
                                     'getter': lambda self: self.max_accu_reinforce + 1.0,
                                     'setter': --- This code section failed: ---

  71       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'max'
           6  LOAD_GLOBAL           1  'max'
           9  LOAD_FAST             1  'v'
          12  LOAD_CONST            2  1.0
          15  BINARY_SUBTRACT  
          16  LOAD_CONST            3  ''
          19  CALL_FUNCTION_2       2 
          22  CALL_FUNCTION_3       3 
          25  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 22
},
   ('accu_move_speed', 'meter'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('slow_down', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe5\x87\x8f\xe9\x80\x9f'},('charge_has_cd', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe8\xb7\xb3\xe6\x9c\x89cd'}})
class JumpCharge(StateBase):
    CHARGE_ICON = 'gui/ui_res_2/battle/mech_main/icon_mech8030_4.png'
    NORMAL_ICON = 'gui/ui_res_2/battle/mech_main/mech_jump.png'

    def on_skill_energy_change(self, skill_id, percent):
        if skill_id != self.skill_id:
            return
        charge_skill_ready = percent >= 1.0
        if charge_skill_ready ^ self.charge_skill_ready:
            self.charge_skill_ready = charge_skill_ready
            icon = self.CHARGE_ICON if self.charge_skill_ready else self.NORMAL_ICON
            self.send_event('E_SET_ACTION_ICON', 'action5', icon)

    def read_data_from_custom_param(self):
        self.normal_skill_id = self.custom_param.get('normal_skill_id', 803051)
        self.skill_id = self.custom_param.get('skill_id', 803054)
        self.min_accu_time = max(self.custom_param.get('min_accu_time', 0.3), 0.1)
        self.max_accu_time = max(self.custom_param.get('max_accu_time', 1.5), 0.1)
        self.max_accu_reinforce = max(self.custom_param.get('max_accu_reinforce', 2.0) - 1.0, 0.0)
        self.accu_move_speed = self.custom_param.get('accu_move_speed', 5) * NEOX_UNIT_SCALE
        self.sfx_change_accu_time = self.custom_param.get('sfx_change_accu_time', 0.3)
        self.enter_anim_name = self.custom_param.get('enter_anim_name', 'jump_01')
        self.enter_anim_len = self.custom_param.get('enter_anim_len', 0.2)
        self.enter_anim_rate = self.custom_param.get('enter_anim_rate', 1.0)
        self.loop_anim_name = self.custom_param.get('loop_anim_name', 'jump_02')
        self.slow_down = self.custom_param.get('slow_down', False)
        self.charge_has_cd = self.custom_param.get('charge_has_cd', False)
        if self.charge_has_cd:
            com_bind_event(self, {'E_ENERGY_CHANGE': 'on_skill_energy_change'})

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(JumpCharge, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.bind_action_id = bdict.get('bind_action_id', 0)
        self.read_data_from_custom_param()
        self.drag_jump_active = global_data.player.get_setting_2(ROCKER_JUMP_8030)
        self.enable_jump_rocker = False
        global_data.emgr.bind_events({'update_rocker_jump_8030': self.on_drag_jump})
        self.on_drag_jump(self.drag_jump_active)
        self.accu_timestamp = None
        self.sp_param = 0.0
        self.enable_param_changed_by_buff()
        self.charged = False
        self.full_charged = False
        self.charge_skill_ready = True
        self.charge_fail_showed = False
        return

    def action_btn_down(self):
        super(JumpCharge, self).action_btn_down()
        if self.drag_jump_active and not self.enable_jump_rocker:
            self.on_drag_jump(self.drag_jump_active)
        if self.is_active:
            return
        if not self.charge_skill_ready:
            self.send_event('E_SET_JUMP_FACTOR', 1.0, False)
            self.send_event('E_SET_JUMP_EFFECT_ENHANCE', False)
            self.ev_g_try_enter(MC_JUMP_1)
            return
        self.active_self()

    def action_btn_up(self):
        super(JumpCharge, self).action_btn_up()
        self.send_event('E_SHOW_CHARGE_FAIL', False)
        self.charge_fail_showed = False
        if self.is_active and self.charge_skill_ready:
            if self.charged and self.check_can_cast_skill():
                accu_time = clamp(get_server_time() - self.accu_timestamp, 0.0, self.max_accu_time)
                max_accu_reinforce = self.max_accu_reinforce
                reinforce_val = accu_time / self.max_accu_time * max_accu_reinforce + 1.0
                reinforce_val *= self.sp_param + 1.0
                self.send_event('E_SET_JUMP_FACTOR', reinforce_val, self.charged)
                self.send_event('E_SET_JUMP_EFFECT_ENHANCE', accu_time >= self.sfx_change_accu_time)
            else:
                self.send_event('E_SET_JUMP_FACTOR', 1.0, self.charged)
                self.send_event('E_SET_JUMP_EFFECT_ENHANCE', False)
            self.ev_g_try_enter(MC_JUMP_1)
        self.disable_self()

    def enter(self, leave_states):
        super(JumpCharge, self).enter(leave_states)
        self.charged = False
        self.full_charged = False

    def start_charge(self):
        if not self.check_can_cast_skill():
            if not self.charge_fail_showed:
                self.send_event('E_SHOW_CHARGE_FAIL', True)
                self.charge_fail_showed = True
            return
        self.charge_fail_showed = False
        self.sound_drive.start_custom_sound('start_charge')
        self.accu_timestamp = get_server_time()
        self.slow_down and self.send_event('E_SLOW_DOWN', True, self.accu_move_speed, 'JumpCharge')
        self.play_loop_anim()
        self.send_event('E_SHOW_JUMP_CHARGE', True, self.accu_timestamp, self.max_accu_time)
        self.charged = True

    def play_loop_anim(self):
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.loop_anim_name, loop=True)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.loop_anim_name, loop=True)
        self.send_event('E_SET_DEFAULT_EXTERN_BONE_ANIM', self.loop_anim_name, JUMP_CHARGE_EFFECT_ID)

    def update(self, dt):
        super(JumpCharge, self).update(dt)
        if not self.charged and self.elapsed_time >= self.min_accu_time:
            self.start_charge()
        elif self.charged and not self.full_charged and self.elapsed_time - self.min_accu_time >= self.max_accu_time:
            self.full_charged = True
            self.sound_drive.end_custom_sound('start_charge')
            self.sound_drive.custom_start()

    def exit(self, enter_states):
        super(JumpCharge, self).exit(enter_states)
        self.sound_drive.end_custom_sound('start_charge')
        self.sound_drive.custom_end()
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.slow_down and self.send_event('E_SLOW_DOWN', False, state='JumpCharge')
        self.send_event('E_SHOW_JUMP_CHARGE', False)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
        if self.sd.ref_up_body_anim in (self.enter_anim_name, self.loop_anim_name):
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_SET_DEFAULT_EXTERN_BONE_ANIM', None)
        return

    def on_drag_jump(self, flag):
        self.drag_jump_active = flag
        self.enable_jump_rocker = self.ev_g_set_action_rocker(self.bind_action_id, flag)


@editor.state_exporter({('jump_speed', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 200},('charge_jump_speed', 'meter'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 200},('h_offset_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6','explain': '\xe5\x9c\xa8\xe8\xa7\x92\xe8\x89\xb2\xe6\xb5\xae\xe7\xa9\xba\xe6\x97\xb6\xef\xbc\x8c\xe6\x91\x87\xe6\x9d\x86\xe5\x8f\xaf\xe4\xbb\xa5\xe7\xbb\x99\xe4\xb8\x8e\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_acc', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','explain': '\xe5\x9c\xa8\xe8\xa7\x92\xe8\x89\xb2\xe6\xb5\xae\xe7\xa9\xba\xe6\x97\xb6\xef\xbc\x8c\xe6\x91\x87\xe6\x9d\x86\xe5\x8f\xaf\xe4\xbb\xa5\xe7\xbb\x99\xe4\xb8\x8e\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('gravity', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x87\x8d\xe5\x8a\x9b','min_val': 0,'max_val': 200},('reinforced_val', 'meter'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe5\xa2\x9e\xe5\xbc\xba','min_val': 0,'max_val': 30,'explain': '6\xe5\x8f\xb7\xe6\x9c\xba\xe7\x94\xb2\xe7\x9a\x84\xe7\x89\xb9\xe6\xae\x8a\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\xbb\x91\xe7\xbf\x94\xe7\x9b\xb8\xe5\x85\xb3'},('advanced_glide_vertical_speed', 'meter'): {'zh_name': '\xe6\xbb\x91\xe7\xbf\x94\xe9\x80\x9f\xe5\xba\xa6','attr_name': '_advanced_glide_vertical_speed','explain': '6\xe5\x8f\xb7\xe6\x9c\xba\xe7\x94\xb2\xe7\x9a\x84\xe7\x89\xb9\xe6\xae\x8a\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\xbb\x91\xe7\xbf\x94\xe7\x9b\xb8\xe5\x85\xb3'},('h_speed_ratio', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6\xe8\xa1\xb0\xe5\x87\x8f','min_val': 0,'max_val': 1,'explain': '\xe8\xb5\xb7\xe8\xb7\xb3\xe7\x9e\xac\xe9\x97\xb4\xe7\x9a\x84\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6\xe8\xa1\xb0\xe5\x87\x8f\xe7\x8e\x870\xe4\xb8\xba\xe6\x9c\x80\xe5\xa4\xa7\xef\xbc\x8c1\xe4\xbf\x9d\xe6\x8c\x81\xe5\x8e\x9f\xe9\x80\x9f\xe5\xba\xa6'},('hover_ability', 'param'): {'zh_name': '\xe6\x94\xaf\xe6\x8c\x81\xe6\xb5\xae\xe7\xa9\xba','attr_name': '_hover_ability','explain': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x98\xaf\xe5\x90\xa6\xe8\x83\xbd\xe6\x8e\xa5\xe6\xb5\xae\xe7\xa9\xba\xef\xbc\x8c\xe4\xb8\xbb\xe8\xa6\x81\xe6\x98\xaf\xe7\x94\xa8\xe5\x9c\xa8\xe8\xb7\xb3\xe8\xb7\x83\xe6\x8e\xa5\xe6\xb5\xae\xe7\xa9\xba\xe7\x9a\x84\xe6\x9c\xba\xe7\x94\xb2\xe4\xb8\x8a\xef\xbc\x8c\xe7\x9b\xae\xe5\x89\x8d\xe6\x98\xaf3\xe5\x8f\xb7\xe6\x9c\xba\xe7\x94\xb2'},('anim_duration', 'param'): {'zh_name': '\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','explain': '\xe8\xb5\xb7\xe8\xb7\xb3\xe5\x8a\xa8\xe7\x94\xbb\xe7\x9a\x84\xe6\x97\xb6\xe9\x95\xbf','getter': lambda self: self.time_scale * self.jump_up_duration,
                                'setter': --- This code section failed: ---

 232       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'jump_up_duration'
           6  LOAD_FAST             1  'v'
           9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             1  'jump_up_duration'
          15  BINARY_DIVIDE    
          16  CALL_FUNCTION_3       3 
          19  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 16
},
   ('enable_float_gravity', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\x90\xaf\xe8\xb5\xb7\xe8\xb7\xb3\xe8\xa1\xb0\xe5\x87\x8f\xe9\x87\x8d\xe5\x8a\x9b'},('float_gravity', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe8\xa1\xb0\xe5\x87\x8f\xe9\x87\x8d\xe5\x8a\x9b','min_val': 0,'max_val': 30},('float_trigger_speed', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe8\xa1\xb0\xe5\x87\x8f\xe9\x87\x8d\xe5\x8a\x9b\xe8\xa7\xa6\xe5\x8f\x91\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 30}})
class JumpUp8030(JumpUp):
    BIND_EVENT = JumpUp.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SET_JUMP_FACTOR': 'set_jump_factor'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(JumpUp8030, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.jump_factor = 1.0

    def read_data_from_custom_param(self):
        super(JumpUp8030, self).read_data_from_custom_param()
        self.charge_jump_speed = self.custom_param.get('charge_jump_speed', 36) * NEOX_UNIT_SCALE
        self.normal_skill_id = self.custom_param.get('normal_skill_id', 803051)
        self.charge_skill_id = self.custom_param.get('charge_skill_id', 803054)
        self.normal_cam = self.custom_param.get('normal_cam', '194')
        self.charge_cam = self.custom_param.get('charge_cam', '195')

    def enter(self, leave_states):
        super(JumpUp, self).enter(leave_states)
        self.normal_jump(self.jump_factor)

    def set_jump_factor(self, factor, charge):
        self.jump_factor = factor
        self.skill_id = self.charge_skill_id if charge else self.normal_skill_id
        self.refresh_camera_param({'cam': self.charge_cam if charge else self.normal_cam})

    def get_jump_speed(self, speed_scale=1.0):
        jump_speed = self.jump_speed if self.skill_id == self.normal_skill_id else self.charge_jump_speed
        if self.enable_reinforced_jump:
            jump_speed += self.apply_refinforce_val
        jump_speed *= speed_scale
        return jump_speed


@editor.state_exporter({('dash_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._register_sub_state_callbacks()
                             },
   ('dash_dist', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe8\xb7\x9d\xe7\xa6\xbb','post_setter': lambda self: self._register_sub_state_callbacks()
                            },
   ('dash_stepheight', 'meter'): {'zh_name': '\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6'},('dash_anim_rate', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('dash_post_anim_rate', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('dash_post_break_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x90\x8e\xe6\x91\x87\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'}})
class Dash8030(StateBase):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_FORWARD = 2
    MOVE_BACK = 3
    DASH_START = 0
    DASH_POST = 1
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded'
       }

    @property
    def max_dash_dist(self):
        return self.dash_dist * (1.0 + self.sp_param)

    @property
    def max_dash_time(self):
        return self.max_dash_dist / self.dash_speed + 0.1

    def _register_sub_state_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.DASH_START, 0.0, self.start_dash)
        self.register_substate_callback(self.DASH_START, self.max_dash_time, lambda : setattr(self, 'sub_state', self.DASH_POST))
        self.register_substate_callback(self.DASH_POST, 0.0, self.after_dash)
        self.register_substate_callback(self.DASH_POST, self.dash_post_break_time, self.on_can_break)
        self.register_substate_callback(self.DASH_POST, self.dash_post_anim_length * self.dash_post_anim_rate, self.disable_self)

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.dash_speed = self.custom_param.get('dash_speed', 1000.0) * NEOX_UNIT_SCALE
        self.dash_dist = self.custom_param.get('dash_dist', 5.0) * NEOX_UNIT_SCALE
        self.dash_stepheight = self.custom_param.get('dash_stepheight', 2.0) * NEOX_UNIT_SCALE
        self.dash_anim = self.custom_param.get('dash_anim', ('dash', 6))
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1)
        self.dash_post_anim = self.custom_param.get('dash_post_anim', ('dash_end',
                                                                       6))
        self.dash_post_anim_length = self.custom_param.get('dash_post_anim_rate', 1.0)
        self.dash_post_anim_rate = self.custom_param.get('dash_post_anim_rate', 1)
        self.dash_post_break_time = self.custom_param.get('dash_post_break_time', 0.3)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8030, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.need_trigger_btn_up_when_action_forbidden = False
        self.drag_rush_active = global_data.player.get_setting(ROCKER_DASH)
        self.enable_rush_rocker = False
        global_data.emgr.bind_events({'player_enable_rocker_dash': self.on_drag_rush})
        self.on_drag_rush(self.drag_rush_active)
        self.dash_dir = self.MOVE_FORWARD
        self.dash_forward = math3d.vector(0, 0, 1)
        self.dash_start_pos = None
        self.dash_end = False
        self.can_break = False
        self.sp_param = 0.0
        self.enable_param_changed_by_buff()
        self._register_sub_state_callbacks()
        return

    def action_btn_down(self):
        if self.drag_rush_active:
            if not self.enable_rush_rocker:
                self.on_drag_rush(self.drag_rush_active)
            return True
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        return True

    def action_btn_up(self):
        super(Dash8030, self).action_btn_up()
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if self.is_active:
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(Dash8030, self).enter(leave_states)
        self.sub_state = self.DASH_START

    def start_dash--- This code section failed: ---

 375       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'skill_id'
           6  POP_JUMP_IF_FALSE    31  'to 31'

 376       9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             1  'send_event'
          15  LOAD_CONST            1  'E_DO_SKILL'
          18  LOAD_FAST             0  'self'
          21  LOAD_ATTR             0  'skill_id'
          24  CALL_FUNCTION_2       2 
          27  POP_TOP          
          28  JUMP_FORWARD          0  'to 31'
        31_0  COME_FROM                '28'

 377      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             1  'send_event'
          37  LOAD_CONST            2  'E_GRAVITY'
          40  LOAD_CONST            3  ''
          43  CALL_FUNCTION_2       2 
          46  POP_TOP          

 378      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             1  'send_event'
          53  LOAD_CONST            4  'E_VERTICAL_SPEED'
          56  LOAD_CONST            3  ''
          59  CALL_FUNCTION_2       2 
          62  POP_TOP          

 380      63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             1  'send_event'
          69  LOAD_CONST            5  'E_STEP_HEIGHT'
          72  LOAD_FAST             0  'self'
          75  LOAD_ATTR             2  'dash_stepheight'
          78  CALL_FUNCTION_2       2 
          81  POP_TOP          

 382      82  LOAD_GLOBAL           3  'math3d'
          85  LOAD_ATTR             4  'vector'
          88  LOAD_CONST            3  ''
          91  LOAD_CONST            3  ''
          94  LOAD_CONST            6  1
          97  CALL_FUNCTION_3       3 
         100  LOAD_FAST             0  'self'
         103  STORE_ATTR            5  'dash_forward'

 383     106  LOAD_GLOBAL           6  'set_boost_dir'
         109  LOAD_GLOBAL           7  'False'
         112  LOAD_GLOBAL           7  'False'
         115  CALL_FUNCTION_257   257 
         118  POP_TOP          

 384     119  LOAD_FAST             0  'self'
         122  LOAD_ATTR             8  'ev_g_yaw'
         125  CALL_FUNCTION_0       0 
         128  STORE_FAST            1  'yaw'

 385     131  LOAD_FAST             0  'self'
         134  LOAD_ATTR             5  'dash_forward'
         137  LOAD_GLOBAL           3  'math3d'
         140  LOAD_ATTR             9  'matrix'
         143  LOAD_ATTR            10  'make_rotation_y'
         146  LOAD_FAST             1  'yaw'
         149  CALL_FUNCTION_1       1 
         152  BINARY_MULTIPLY  
         153  STORE_FAST            2  'forward'

 386     156  LOAD_FAST             2  'forward'
         159  LOAD_ATTR            11  'normalize'
         162  CALL_FUNCTION_0       0 
         165  POP_TOP          

 387     166  LOAD_FAST             0  'self'
         169  LOAD_ATTR             1  'send_event'
         172  LOAD_CONST            8  'E_SET_WALK_DIRECTION'
         175  LOAD_FAST             2  'forward'
         178  LOAD_FAST             0  'self'
         181  LOAD_ATTR            12  'dash_speed'
         184  BINARY_MULTIPLY  
         185  CALL_FUNCTION_2       2 
         188  POP_TOP          

 388     189  LOAD_GLOBAL           7  'False'
         192  LOAD_FAST             0  'self'
         195  STORE_ATTR           13  'dash_end'

 389     198  LOAD_GLOBAL           7  'False'
         201  LOAD_FAST             0  'self'
         204  STORE_ATTR           14  'can_break'

 390     207  LOAD_FAST             0  'self'
         210  LOAD_ATTR            15  'ev_g_position'
         213  CALL_FUNCTION_0       0 
         216  LOAD_FAST             0  'self'
         219  STORE_ATTR           16  'dash_start_pos'

 391     222  LOAD_FAST             0  'self'
         225  LOAD_ATTR            17  'dash_anim'
         228  UNPACK_SEQUENCE_2     2 
         231  STORE_FAST            3  'dash_anim'
         234  STORE_FAST            4  'anim_dir'

 392     237  LOAD_FAST             0  'self'
         240  LOAD_ATTR             1  'send_event'
         243  LOAD_CONST            9  'E_POST_ACTION'
         246  LOAD_FAST             3  'dash_anim'
         249  LOAD_GLOBAL          18  'LOW_BODY'
         252  LOAD_FAST             4  'anim_dir'
         255  LOAD_CONST           10  'timeScale'
         258  LOAD_FAST             0  'self'
         261  LOAD_ATTR            19  'dash_anim_rate'
         264  CALL_FUNCTION_260   260 
         267  POP_TOP          

 393     268  LOAD_FAST             0  'self'
         271  LOAD_ATTR             1  'send_event'
         274  LOAD_CONST           11  'E_SHOW_TAIL_EFFECT'
         277  LOAD_FAST             0  'self'
         280  LOAD_ATTR            16  'dash_start_pos'
         283  LOAD_FAST             2  'forward'
         286  CALL_FUNCTION_3       3 
         289  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 115

    def update(self, dt):
        super(Dash8030, self).update(dt)
        if self.sub_state != self.DASH_START or self.dash_start_pos is None:
            return
        else:
            dash_dist = self.ev_g_position() - self.dash_start_pos
            dash_dist.y = 0
            if dash_dist.length >= self.max_dash_dist:
                self.sub_state = self.DASH_POST
            return

    def after_dash(self):
        dash_post_anim, blend_dir = self.dash_post_anim
        self.send_event('E_POST_ACTION', dash_post_anim, LOW_BODY, blend_dir, timeScale=self.dash_post_anim_rate)
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_PLAY_EXTERN_BONE_ANIM', dash_post_anim, self.dash_post_anim_length, DASH_END_EXTERN_BONE_EFFECT_ID)
        self.send_event('E_TRIGGER_STATE_EFFECT', 'dash_end', DASH_END_EFFECT_ID, force=True, need_sync=True)
        end_pos = self.ev_g_position()
        if end_pos and self.dash_start_pos:
            dist = int((self.dash_start_pos - end_pos).length)
            dist > 0 and self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8030', MECHA_MEMORY_LEVEL_8, dist / NEOX_UNIT_SCALE), False, True)

    def on_can_break(self):
        self.can_break = True

    def check_transitions(self):
        if self.sub_state != self.DASH_POST or not self.can_break:
            return
        if not self.ev_g_on_ground():
            self.disable_self()
            return self.status_config.MC_JUMP_2
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            self.disable_self()
            return self.status_config.MC_MOVE

    def exit(self, enter_states):
        super(Dash8030, self).exit(enter_states)
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_END_SKILL', self.skill_id)
        self.dash_start_pos = None
        return

    def on_drag_rush(self, flag):
        self.drag_rush_active = flag
        self.enable_rush_rocker = self.ev_g_set_action_rocker(self.bind_action_id, flag, not flag)

    def refresh_action_param(self, action_param, custom_param):
        super(Dash8030, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()


def __editor_pitch_postsetter(self):
    self.swp_sin_cos = (
     sin(self.sub_weapon_pitch), cos(self.sub_weapon_pitch))


@editor.state_exporter({('sub_weapon_pitch', 'param'): {'zh_name': '\xe5\xad\x90\xe6\xa6\xb4\xe5\xbc\xb9\xe5\x8f\x91\xe5\xb0\x84\xe4\xbb\xb0\xe8\xa7\x92(-90~90\xe5\xba\xa6)',
                                   'min_val': -90.0,
                                   'max_val': 90.0,'getter': lambda self: degrees(self.sub_weapon_pitch),
                                   'setter': --- This code section failed: ---

 734       0  LOAD_GLOBAL           0  'setattr'
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
class ClusterShoot(AccumulateShootPure):
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD}

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ClusterShoot, self).init_from_dict(unit_obj, bdict, sid, info)
        self.explode_position = None
        self.pos_dir_getter_setted = False
        return

    def read_data_from_custom_param(self):
        super(ClusterShoot, self).read_data_from_custom_param()
        self.main_weapon_id = self.custom_param.get('main_weapon_id', 803002)
        self.sub_weapon_pos = self.custom_param.get('sub_weapon_pos', PART_WEAPON_POS_MAIN3)
        self.sub_weapon_pitch = radians(self.custom_param.get('sub_weapon_pitch', 0))
        self.swp_sin_cos = (sin(self.sub_weapon_pitch), cos(self.sub_weapon_pitch))
        self.post_anim_blend_time = self.custom_param.get('post_anim_blend_time', 0.0)

    def enter(self, leave_states):
        super(ClusterShoot, self).enter(leave_states)
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_SHOW_SEC_AIM', True)
        self.sound_drive.custom_start()
        self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')

    def exit(self, enter_states):
        super(ClusterShoot, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_SHOW_SEC_AIM', False)
        self.sound_drive.custom_end()
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')

    def _fire(self):
        self.ev_g_try_weapon_attack_begin(self.sub_weapon_pos)
        self.ev_g_try_weapon_attack_end(self.sub_weapon_pos)
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def on_grenade_exploded(self, item_info):
        pass

    def sub_weapon_pos_dir_getter(self, sub_idx, pellets):
        yaw = pi * 2.0 * sub_idx / pellets
        direction = math3d.vector(sin(yaw) * self.swp_sin_cos[1], self.swp_sin_cos[0], cos(yaw) * self.swp_sin_cos[1])
        return (
         self.explode_position, direction)

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


class ExternBoneAnim(StateBase):
    BIND_EVENT = {'E_PLAY_EXTERN_BONE_ANIM': 'play_anim',
       'E_SET_DEFAULT_EXTERN_BONE_ANIM': 'set_default_anim'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ExternBoneAnim, self).init_from_dict(unit_obj, bdict, sid, info)
        self.default_anim_name = None
        self.default_effect_id = ''
        self.anim_name = None
        self.anim_length = None
        self.effect_id = ''
        self.bone_tree = self.custom_param.get('bone_tree', (
         ('biped root', 0), ('bones_04', 1), ('bones_07', 1), ('bones_22', 1), ('bones_23', 1),
         ('bones_24', 1), ('bones_25', 1), ('bones_26', 1), ('bones_27', 1)))
        return

    def play_anim(self, anim_name=None, length=None, effect_id=''):
        if anim_name is None and self.is_active:
            if self.default_anim_name:
                self.anim_name = self.default_anim_name
                self.anim_length = None
                self.effect_id = self.default_effect_id
                self.enter(set())
            else:
                self.anim_name = None
                self.anim_length = None
                self.disable_self()
        elif anim_name is not None:
            self.anim_name = anim_name
            self.anim_length = length
            self.effect_id = effect_id
            if self.is_active:
                self.enter(set())
            else:
                self.active_self()
        return

    def set_default_anim(self, anim_name=None, effect_id=''):
        old_default_anim_name = self.default_anim_name
        self.default_anim_name = anim_name
        self.default_effect_id = effect_id
        if self.is_active:
            if self.anim_name == old_default_anim_name:
                self.play_anim(self.default_anim_name, effect_id=self.default_effect_id)
        elif anim_name:
            self.play_anim(anim_name, effect_id=self.default_effect_id)

    def action_btn_down(self):
        super(ExternBoneAnim, self).action_btn_down()
        self.enter(set())
        return True

    def enter(self, leave_states):
        super(ExternBoneAnim, self).enter(leave_states)
        if self.anim_name is None:
            self.play_anim()
        self.send_event('E_POST_EXTERN_ACTION', self.anim_name, True, subtree=self.bone_tree)
        self.send_event('E_SHOW_EXTERN_BONE_EFFECT', self.effect_id)
        return

    def update(self, dt):
        super(ExternBoneAnim, self).update(dt)
        if self.anim_length is not None:
            self.anim_length -= dt
            if self.anim_length <= 0.0:
                self.play_anim()
        return

    def exit(self, enter_states):
        super(ExternBoneAnim, self).exit(enter_states)
        self.send_event('E_POST_EXTERN_ACTION', self.anim_name, False)
        self.send_event('E_SHOW_EXTERN_BONE_EFFECT', self.effect_id, end=True)