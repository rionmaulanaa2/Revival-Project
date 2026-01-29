# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8009.py
from __future__ import absolute_import
import math3d
import world
import math
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.comsys.control_ui.ShotChecker import ShotChecker
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.const import NEOX_UNIT_SCALE, PART_WEAPON_POS_MAIN6
from logic.gcommon.common_const import mecha_const
import logic.gcommon.const as g_const
from .ShootLogic import Reload, WeaponFire
from .MoveLogic import Run
from logic.gcommon.component.client.com_mecha_effect.ComMechaEffect8009 import STATE_NO_FULL_FORCE, STATE_FULL_FORCE_BEGIN, STATE_FULL_FORCE_END
from .MountLogic import UnMount
from logic.gcommon.behavior.StateBase import clamp
from logic.gcommon.time_utility import get_server_time
import time
from logic.gcommon import editor

@editor.state_exporter({('take_back_anim_duration', 'param'): {'zh_name': '\xe6\x94\xbe\xe5\x9b\x9e\xe6\xad\xa6\xe5\x99\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6'},('take_back_anim_rate', 'param'): {'zh_name': '\xe6\x94\xbe\xe5\x9b\x9e\xe6\xad\xa6\xe5\x99\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('take_out_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x96\xe5\x87\xba\xe6\xad\xa6\xe5\x99\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6'},('take_out_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x96\xe5\x87\xba\xe6\xad\xa6\xe5\x99\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('min_take_out_duration', 'param'): {'zh_name': '\xe5\x8f\x96\xe5\x87\xba\xe6\xad\xa6\xe5\x99\xa8\xe6\x9c\x80\xe7\x9f\xad\xe6\x97\xb6\xe9\x97\xb4'}})
class TrioSwitchWeapon(StateBase):
    BIND_EVENT = {'E_SHOW_WEAPON_SWITCH_PROCESS': 'on_show_weapon_switch_process',
       'E_ENABLE_BEHAVIOR': ('on_enable_behavior', 99)
       }
    STATE_TAKE_BACK = 0
    STATE_TAKE_OUT = 1

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 800951)
        self.default_up_body_anim = self.custom_param.get('default_up_body_anim', None)
        self.take_back_anim = self.custom_param.get('take_back_anim', 'switch_fanghuibuqiang')
        self.take_back_anim_duration = self.custom_param.get('take_back_anim_duration', 1.1) * self.switch_scale
        self.take_back_anim_rate = self.custom_param.get('take_back_anim_rate', 1.0) / self.switch_scale
        self.take_out_anim = self.custom_param.get('take_out_anim', 'switch_nachuxiandanqiang')
        self.take_out_anim_duration = self.custom_param.get('take_out_anim_duration', 1.0) * self.switch_scale
        self.take_out_anim_rate = self.custom_param.get('take_out_anim_rate', 1.0) / self.switch_scale
        self.min_take_out_duration = self.custom_param.get('min_take_out_duration', 1.5) * self.switch_scale
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_TAKE_BACK, 0, self.on_take_back)
        self.register_substate_callback(self.STATE_TAKE_BACK, self.take_back_anim_duration, self.on_take_back_end)
        self.register_substate_callback(self.STATE_TAKE_OUT, 0, self.on_take_out)
        self.register_substate_callback(self.STATE_TAKE_OUT, self.take_out_anim_duration, self.on_take_out_end)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TrioSwitchWeapon, self).init_from_dict(unit_obj, bdict, sid, info)
        self.switch_accelerate_scale = 0.0
        self.switch_scale = 1.0 - self.switch_accelerate_scale
        self.read_data_from_custom_param()
        self.to_switch_id = None
        self.ready_to_switch = False
        self.last_take_out_anim = None
        self.take_out_end_run = False
        self.take_back_end_run = False
        self.enable_param_changed_by_buff()
        return

    def on_enable_behavior(self, *args):
        if self.ev_g_is_avatar():
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.default_up_body_anim)
            self.send_event('E_CLEAR_UP_BODY_ANIM')

    def action_btn_down(self):
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()
        super(TrioSwitchWeapon, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(TrioSwitchWeapon, self).enter(leave_states)
        self.sub_state = self.STATE_TAKE_BACK
        self.to_switch_id = None
        self.ready_to_switch = False
        self.finish_switch = False
        self.enable_break = False
        self.take_back_end_run = False
        self.take_out_end_run = False
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_SET_ACTION_FORBIDDEN', 'action6', True)
        return

    def update(self, dt):
        super(TrioSwitchWeapon, self).update(dt)

    def on_take_back(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.take_back_anim_rate)
        self.send_event('E_POST_ACTION', self.take_back_anim, UP_BODY, 1)

    def on_take_back_end(self):
        if self.to_switch_id:
            self.sub_state = self.STATE_TAKE_OUT
        self.ready_to_switch = True
        self.take_back_end_run = True

    def on_take_out(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.take_out_anim_rate)
        self.send_event('E_POST_ACTION', self.take_out_anim, UP_BODY, 1)

    def on_take_out_end(self):
        if not self.enable_break:
            self.enable_break = True
            self.send_event('E_REFRESH_STATE_PARAM', self.to_switch_id)
        self.disable_self()
        self.take_out_end_run = True

    def check_transitions(self):
        if self.sub_state == self.STATE_TAKE_OUT and self.sub_sid_timer > self.min_take_out_duration and not self.enable_break:
            self.enable_break = True
            self.send_event('E_REFRESH_STATE_PARAM', self.to_switch_id)
            self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_RELOAD}, self.sid)

    def exit(self, enter_states):
        super(TrioSwitchWeapon, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.sub_state = None
        if self.sd.ref_up_body_anim == self.last_take_out_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_SET_ACTION_FORBIDDEN', 'action6', False)
        voice_name = ''
        if self.to_switch_id == '8009_S':
            voice_name = 'transform_a'
        elif self.to_switch_id == '8009_R':
            voice_name = 'transform_b'
        elif self.to_switch_id == '8009':
            voice_name = 'transform_c'
        if voice_name:
            global_data.emgr.play_game_voice.emit(voice_name)
        return

    def on_show_weapon_switch_process(self, switch_id):
        if self.ready_to_switch:
            self.sub_state = self.STATE_TAKE_OUT
        self.to_switch_id = switch_id

    def refresh_param_changed(self):
        self.switch_scale = 1.0 - self.switch_accelerate_scale
        self.read_data_from_custom_param()
        if self.sub_state == self.STATE_TAKE_BACK and not self.take_back_end_run:
            self.sub_sid_timer = 0.1
        elif self.sub_state == self.STATE_TAKE_OUT and not self.take_out_end_run:
            self.sub_sid_timer = 0.1

    def refresh_action_param(self, action_param, custom_param):
        super(TrioSwitchWeapon, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.last_take_out_anim = self.take_out_anim
            self.read_data_from_custom_param()
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.default_up_body_anim)


class ShoulderGrenade(WeaponFire):

    def _end_shoot(self, *args):
        self.try_weapon_attack_end()


class Reload8009(Reload):
    BIND_EVENT = Reload.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_SHOULDER_GRENADE': 'enable_shoulder_grenade'
       })

    def read_data_from_custom_param(self):
        super(Reload8009, self).read_data_from_custom_param()
        self.extern_weapon_pos = self.custom_param.get('extern_weapon_pos', 7)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8009, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.shoulder_grenade_enabled = False

    def on_reloading_bullet(self, *args):
        super(Reload8009, self).on_reloading_bullet(*args)
        if self.shoulder_grenade_enabled:
            self.send_event('E_WEAPON_FIRE_BUTTON_DOWN', self.extern_weapon_pos)

    def enable_shoulder_grenade(self, flag):
        self.shoulder_grenade_enabled = flag


@editor.state_exporter({('start_anim_cd', 'param'): {'zh_name': '\xe9\x80\x80\xe5\x87\xba\xe8\xb7\x91\xe6\xad\xa5\xe5\x90\x8e\xe5\xbf\xbd\xe7\x95\xa5\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x95\xbf'},('stop_anim_cost_time', 'param'): {'zh_name': '\xe6\x92\xad\xe6\x94\xbe\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x9c\x80\xe5\xb0\x91\xe8\xb7\x91\xe6\xad\xa5\xe6\x97\xb6\xe9\x97\xb4'}})
class Run8009(Run):

    def read_data_from_custom_param(self):
        super(Run8009, self).read_data_from_custom_param()
        self.start_anim_sound = self.custom_param.get('start_anim_sound', None)
        self.start_anim_cd = self.custom_param.get('start_anim_cd', 5.0)
        self.stop_anim_cost_time = self.custom_param.get('stop_anim_cost_time', 3.0)
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        self.exit_run_time_stamp = time.time() - 999.0
        self.enter_state_running_time_stamp = self.exit_run_time_stamp
        super(Run8009, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def enter(self, leave_states):
        self.brakeing = False
        super(Run, self).enter(leave_states)
        if self._up_bone_strategy:
            self.send_event('E_UPBODY_BONE', self._up_bone_strategy['enter'])
        if self.run_start_anim:
            self.sub_state = self.STATE_START
        elif self.run_anim:
            self.sub_state = self.STATE_RUN

    def begin_run_start_anim(self):
        if time.time() - self.exit_run_time_stamp < self.start_anim_cd:
            self.end_run_start_anim()
            return
        if self.start_anim_sound:
            global_data.sound_mgr.play_event(self.start_anim_sound)
        super(Run8009, self).begin_run_start_anim()

    def begin_run_anim(self):
        super(Run8009, self).begin_run_anim()
        self.enter_state_running_time_stamp = time.time()

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_state_running_time_stamp < self.stop_anim_cost_time and self.sd.ref_rocker_dir:
            return
        super(Run8009, self).begin_run_stop_anim()

    def exit(self, enter_states):
        super(Run8009, self).exit(enter_states)
        self.exit_run_time_stamp = time.time()


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6'},('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('drop_anim_duration', 'param'): {'zh_name': '\xe4\xb8\xa2\xe5\xbc\x83\xe6\xad\xa6\xe5\x99\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6'},('drop_anim_rate', 'param'): {'zh_name': '\xe4\xb8\xa2\xe5\xbc\x83\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('end_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x96\xe5\x87\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6'},('end_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x96\xe5\x87\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('min_take_out_duration', 'param'): {'zh_name': '\xe5\x8f\x96\xe5\x87\xba\xe6\xad\xa6\xe5\x99\xa8\xe6\x9c\x80\xe7\x9f\xad\xe6\x97\xb6\xe9\x97\xb4'}})
class SwitchFullForce(StateBase):
    BIND_EVENT = {'E_SET_ENTER_FULL_FORCE': 'set_is_enter',
       'G_FULL_FORCE_SKILL_ID': 'get_skill_id',
       'E_CLEAR_FULL_FORCE_ADVANCE_PERFORMANCE': 'clear_advance_performance'
       }
    STATE_PRE = 0
    STATE_POST = 1

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 800952)
        self.default_up_body_anim = self.custom_param.get('default_up_body_anim', 'idle_m')
        self.pre_anim = self.custom_param.get('pre_anim', 'huoliquankai_01')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 1.9)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.hold_anim = self.custom_param.get('hold_anim', 'huoliquankai_idle')
        self.drop_anim = self.custom_param.get('drop_anim', 'huoliquankai_03')
        self.drop_anim_duration = self.custom_param.get('drop_anim_duration', 0.6)
        self.drop_anim_rate = self.custom_param.get('drop_anim_rate', 1.0)
        self.end_anim = self.custom_param.get('end_anim', 'switch_nachubuqiang')
        self.end_anim_duration = self.custom_param.get('end_anim_duration', 1.0)
        self.end_anim_rate = self.custom_param.get('end_anim_rate', 1.0)
        self.enter_camera_state = self.custom_param.get('enter_camera_state', '58')
        self.leave_camera_state = self.custom_param.get('leave_camera_state', '35')
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration, self.on_finish_pre)
        self.register_substate_callback(self.STATE_POST, 0, self.on_begin_post)

        def callback():
            self.send_event('E_ANIM_RATE', UP_BODY, self.end_anim_rate)
            self.send_event('E_POST_ACTION', self.end_anim, UP_BODY, 1)
            self.sound_drive.run_end()

        self.register_substate_callback(self.STATE_POST, self.drop_anim_duration, callback)
        self.register_substate_callback(self.STATE_POST, self.drop_anim_duration + self.end_anim_duration, self.on_finish_post)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SwitchFullForce, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.is_enter = True

    def action_btn_down(self):
        if not self.check_can_active():
            return
        if MC_TRANSFORM in self.ev_g_cur_state():
            self.send_event('E_ACTIVE_FULL_FORCE', False, 0, 0)
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()
        super(SwitchFullForce, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(SwitchFullForce, self).enter(leave_states)
        if self.is_enter:
            self.sub_state = self.STATE_PRE
        else:
            self.sub_state = self.STATE_POST
            self.is_enter = True

    def on_begin_pre(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, UP_BODY, 1)
        self.send_event('E_REFRESH_MECHA_CONTROL_BUTTON_ICON', True)
        self.send_event('E_SWITCH_LETTER_EFFECT', 'FullForce')
        self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, MC_FULL_FORCE_MOVE)
        self.send_event('E_SWITCH_FULL_FORCE_EFFECT', STATE_FULL_FORCE_BEGIN)
        self.send_event('E_SET_ACTION_SELECTED', 'action6', True)
        self.send_event('E_SET_ACTION_FORBIDDEN', 'action4', True)

    def on_finish_pre(self):
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_DELAY_CLEAR_ADVANCE_FULL_FORCE')
        self.send_event('E_DO_SKILL', self.skill_id)

    def on_begin_post(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.drop_anim_rate)
        self.send_event('E_POST_ACTION', self.drop_anim, UP_BODY, 1)

    def on_finish_post(self):
        self.disable_self()

    def exit(self, enter_states):
        super(SwitchFullForce, self).exit(enter_states)
        if self.sub_state == self.STATE_POST:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            if self.sd.ref_up_body_anim in (None, self.drop_anim, self.end_anim):
                self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_SET_ACTION_SELECTED', 'action6', False)
            self.send_event('E_SET_ACTION_FORBIDDEN', 'action4', False)
            self.send_event('E_SWITCH_FULL_FORCE_EFFECT', STATE_NO_FULL_FORCE)
            self.send_event('E_END_SKILL', self.skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        elif MC_TRANSFORM not in enter_states:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            if self.sd.ref_up_body_anim in (None, self.pre_anim):
                self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.clear_advance_performance()
        return

    def refresh_action_param(self, action_param, custom_param):
        super(SwitchFullForce, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()

    def set_is_enter(self, flag):
        self.is_enter = flag

    def get_skill_id(self):
        return self.skill_id

    def clear_advance_performance(self):
        self.send_event('E_REFRESH_MECHA_CONTROL_BUTTON_ICON')
        self.send_event('E_SWITCH_LETTER_EFFECT', self.ev_g_trio_state())
        self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, MC_MOVE)
        self.send_event('E_SWITCH_FULL_FORCE_EFFECT', STATE_FULL_FORCE_END)
        self.send_event('E_SET_ACTION_SELECTED', 'action6', False)
        self.send_event('E_SET_ACTION_FORBIDDEN', 'action4', False)


class FullForce(StateBase):
    BIND_EVENT = {'E_ACTIVE_FULL_FORCE': 'active_full_force'
       }

    def read_data_from_custom_param(self):
        self.default_up_body_anim = self.custom_param.get('default_up_body_anim', 'idle_m')
        self.hold_anim = self.custom_param.get('hold_anim', 'huoliquankai_idle')
        self.enter_camera_state = self.custom_param.get('enter_camera_state', '58')
        self.leave_camera_state = self.custom_param.get('leave_camera_state', '35')

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(FullForce, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.left_time = 0
        self.full_force_ended = True

    def action_btn_down(self):
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()
        super(FullForce, self).action_btn_down()
        return True

    def _end_full_force(self):
        if not self.full_force_ended:
            self.full_force_ended = True
            self.send_event('E_SET_ENTER_FULL_FORCE', False)
            if self.ev_g_status_check_pass(MC_DASH, only_avatar=True):
                self.send_event('E_ACTIVE_STATE', MC_DASH)
            else:
                self.disable_self()

    def enter(self, leave_states):
        super(FullForce, self).enter(leave_states)
        pre_anim_played = MC_DASH in leave_states
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_RESET_RELOAD_STATE')
        self.send_event('E_SET_SHOOT_BLEND_TIME', 0.2)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.hold_anim)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        if not pre_anim_played:
            self.send_event('E_SET_ACTION_SELECTED', 'action6', True)
            self.send_event('E_SET_ACTION_FORBIDDEN', 'action4', True)
            self.send_event('E_REFRESH_MECHA_CONTROL_BUTTON_ICON', True)
            self.send_event('E_SWITCH_LETTER_EFFECT', 'FullForce')
        self.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, PART_WEAPON_POS_MAIN6)
        self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', self.enter_camera_state)
        self.on_action_switch(True)
        self.on_move_switch(True)

    def update(self, dt):
        super(FullForce, self).update(dt)
        self.left_time -= dt
        if self.full_force_ended:
            self.disable_self()
            return
        if self.left_time <= 0:
            self._end_full_force()

    def exit(self, enter_states):
        super(FullForce, self).exit(enter_states)
        self.send_event('E_SET_SHOOT_BLEND_TIME', 0.0)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.default_up_body_anim)
        self.send_event('E_REFRESH_MECHA_CONTROL_BUTTON_ICON')
        self.send_event('E_SWITCH_LETTER_EFFECT', self.ev_g_trio_state())
        self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, PART_WEAPON_POS_MAIN6)
        self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', self.leave_camera_state)
        self.on_action_switch(False)
        self.on_move_switch(False)
        if MC_DASH not in enter_states:
            if self.sd.ref_up_body_anim == self.hold_anim:
                self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_SET_ACTION_SELECTED', 'action6', False)
            self.send_event('E_SET_ACTION_FORBIDDEN', 'action4', False)
            self.send_event('E_SWITCH_FULL_FORCE_EFFECT', STATE_NO_FULL_FORCE)
            skill_id = self.ev_g_full_force_skill_id()
            self.send_event('E_END_SKILL', skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', skill_id)
            self.send_event('E_SET_ENTER_FULL_FORCE', True)

    def on_action_switch(self, flag):
        state = MC_FULL_FORCE_SHOOT if flag else MC_SHOOT
        self.send_event('E_SWITCH_ACTION', 'action1', state, False)
        self.send_event('E_SWITCH_ACTION', 'action2', state, False)
        self.send_event('E_SWITCH_ACTION', 'action3', state, False)

    def on_move_switch(self, flag):
        state = MC_FULL_FORCE_MOVE if flag else MC_MOVE
        self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, state)
        effect_state = STATE_FULL_FORCE_BEGIN if flag else STATE_FULL_FORCE_END
        self.send_event('E_SWITCH_FULL_FORCE_EFFECT', effect_state)

    def active_full_force(self, flag, total_time, finish_time_stamp):
        if flag:
            if not self.is_active:
                self.active_self()
                self.left_time = finish_time_stamp - get_server_time()
                self.full_force_ended = False
        elif self.is_active:
            self._end_full_force()

    def refresh_action_param(self, action_param, custom_param):
        super(FullForce, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()


class UnMount8009(UnMount):

    def enter(self, leave_states):
        super(UnMount8009, self).enter(leave_states)
        self.send_event('E_SWITCH_FULL_FORCE_EFFECT', STATE_NO_FULL_FORCE)