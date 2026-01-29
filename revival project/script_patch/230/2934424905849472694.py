# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8014.py
from __future__ import absolute_import
import six
from six.moves import range
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE, SOUND_TYPE_MECHA_FIRE
from .MoveLogic import Walk, Run
from .JumpLogic import JumpUp, JumpUpPure, SuperJumpUp, Fall, FallPure, OnGround
from .ShootLogic import WeaponFire, Reload
from common.utils.timer import CLOCK
from logic.gutils.character_ctrl_utils import get_forward_by_rocker_and_camera_without_y, apply_horizon_offset_speed_reference_camera, ray_check_on_ground, AirWalkDirectionSetter
from logic.gutils.slash_utils import SlashChecker, LockedTargetFinder
from math import pi, acos, fabs
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import world
from logic.gcommon import editor
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_8

class SlashSwitchController(object):

    def __init__(self, state):
        self.state = state
        self.count_down_timer = None
        self.is_on = False
        return

    def destroy(self):
        if self.count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
            self.count_down_timer = None
        return

    def on(self):
        if self.is_on:
            return
        state = self.state
        if not state.check_can_cast_skill():
            return
        state.send_event('E_DO_SKILL', state.skill_id)
        skill_obj = state.ev_g_skill(state.skill_id)
        if skill_obj:
            duration = skill_obj._data.get('ext_info', {}).get('lasting_time', 3.0)
        else:
            duration = 3.0
        self.count_down_timer = global_data.game_mgr.register_logic_timer(self.off, interval=duration, times=1, mode=CLOCK)
        state.send_event('E_SLASH_ACTIVATED', True, duration)
        self.is_on = True

    def off(self):
        self.state.send_event('E_BEGIN_RECOVER_MP', self.state.skill_id)
        self.state.send_event('E_SLASH_ACTIVATED', False)
        self.count_down_timer = None
        self.is_on = False
        return

    def abort(self):
        if self.count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
            self.count_down_timer = None
            self.off()
        self.is_on = False
        return


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6','post_setter': lambda self: self._register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                },
   ('end_anim_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6','post_setter': lambda self: self._register_callbacks()
                                    },
   ('end_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                },
   ('air_dash_speed', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._register_callbacks()
                                 },
   ('air_dash_duration', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                    },
   ('acc_speed', 'meter'): {'zh_name': '\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('burst_speed', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('brake_speed', 'meter'): {'zh_name': '\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'},('dash_blade_max_locked_dist', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x9c\x80\xe5\xa4\xa7\xe8\xbf\xbd\xe5\x87\xbb\xe9\x94\x81\xe5\xae\x9a\xe8\xb7\x9d\xe7\xa6\xbb','post_setter': lambda self: self._record_locked_target_finder_parameters()
                                             },
   ('dash_blade_max_locked_angle', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x9c\x80\xe5\xa4\xa7\xe9\x94\x81\xe5\xae\x9a\xe8\xa7\x92\xe5\xba\xa6(\xe6\xb0\xb4\xe5\xb9\xb3)','post_setter': lambda self: self._record_locked_target_finder_parameters()
                                              },
   ('dash_blade_dist_prior_angle', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe8\xb7\x9d\xe7\xa6\xbb\xe4\xbc\x98\xe5\x85\x88\xe8\xa7\x92\xe5\xba\xa6','post_setter': lambda self: self._record_locked_target_finder_parameters()
                                              }
   })
class BurstForm(StateBase):
    BIND_EVENT = {'E_FUEL_EXHAUSTED': 'on_fuel_exhausted',
       'E_ON_TOUCH_GROUND': 'on_touch_ground',
       'E_LOGIC_ON_GROUND': 'on_touch_ground',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start'
       }
    STATE_PRE = 0
    STATE_AIR_DASH = 1
    STATE_BURST = 2
    STATE_END = 3

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.common_skill_id = self.custom_param.get('common_skill_id', None)
        self.air_dash_skill_id = self.custom_param.get('air_dash_skill_id', None)
        self.air_burst_skill_id = self.custom_param.get('air_burst_skill_id', None)
        self.air_dash_speed = self.custom_param.get('air_dash_speed', 60) * NEOX_UNIT_SCALE
        self.air_dash_duration = self.custom_param.get('air_dash_duration', 0.7)
        self.acc_speed = self.custom_param.get('acc_speed', 90) * NEOX_UNIT_SCALE
        self.burst_speed = self.custom_param.get('burst_speed', 20) * NEOX_UNIT_SCALE
        self.brake_speed = self.custom_param.get('brake_speed', -120) * NEOX_UNIT_SCALE
        self.pre_anim = self.custom_param.get('pre_anim', 'thrust_f_fly')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.4)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.burst_idle_anim = self.custom_param.get('burst_idle_anim', 'dash_idle')
        self.burst_anim = self.custom_param.get('burst_anim', 'cut_rush')
        self.dash_air_anim = self.custom_param.get('dash_air_anim', 'dash_air_f')
        self.end_anim = self.custom_param.get('end_anim', 'thrust_f_landed')
        self.end_anim_duration = self.custom_param.get('end_anim_duration', 0.6)
        self.end_anim_rate = self.custom_param.get('end_anim_rate', 1.0)
        self._register_callbacks()
        self.dash_blade_max_locked_dist = self.custom_param.get('dash_blade_max_locked_dist', 60) * NEOX_UNIT_SCALE
        self.dash_blade_max_locked_angle = self.custom_param.get('dash_blade_max_locked_angle', 90)
        self.dash_blade_dist_prior_angle = self.custom_param.get('dash_blade_dist_prior_angle', 45)
        return

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration, self.on_finish_pre)
        self.register_substate_callback(self.STATE_AIR_DASH, 0, self.on_begin_air_dash)
        self.register_substate_callback(self.STATE_AIR_DASH, self.air_dash_duration, self.on_end_air_dash)
        self.register_substate_callback(self.STATE_BURST, 0, self.on_begin_burst)
        self.register_substate_callback(self.STATE_END, 0, self.on_begin_end)
        self.register_substate_callback(self.STATE_END, self.end_anim_duration, self.on_finish_end)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(BurstForm, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.last_rocker_dir = None
        self.ignore_gravity = False
        self.costing_fuel = False
        self.can_air_dash = False
        self.enable_param_changed_by_buff()
        return

    def _record_locked_target_finder_parameters(self):
        self.sd.ref_locked_target_finder.record_parameters(self.sid, self.dash_blade_max_locked_dist, self.dash_blade_max_locked_angle, self.dash_blade_dist_prior_angle)

    def on_init_complete(self):
        super(BurstForm, self).on_init_complete()
        self._record_locked_target_finder_parameters()

    def destroy(self):
        super(BurstForm, self).destroy()

    def on_leave_mecha_start(self):
        if self.ev_g_is_avatar():
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), None)
            self.sd.ref_locked_target_finder.end()
            self.sd.ref_slash_switch_controller.off()
        return

    def end_skill(self):
        if self.costing_fuel:
            self.send_event('E_END_SKILL', self.common_skill_id)
            self.send_event('E_END_SKILL', self.air_burst_skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', self.common_skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', self.air_burst_skill_id)
            self.costing_fuel = False

    def action_btn_down(self):
        if self.is_active:
            if self.sub_state != self.STATE_END:
                self.sub_state = self.STATE_END
        else:
            if not self.check_can_active():
                return
            if not self.check_can_cast_skill():
                return
            if not self.ev_g_can_cast_skill(self.common_skill_id):
                return
            self.active_self()
        super(BurstForm, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(BurstForm, self).enter(leave_states)
        on_ground = self.sd.ref_on_ground
        if self.can_air_dash and not on_ground and self.ev_g_can_cast_skill(self.air_dash_skill_id):
            self.can_air_dash = False
            self.sub_state = self.STATE_AIR_DASH
        else:
            if self.ignore_gravity and not on_ground:
                self.send_event('E_DO_SKILL', self.air_burst_skill_id)
                self.send_event('E_GRAVITY', 0)
                self.send_event('E_VERTICAL_SPEED', 0)
            self.sub_state = self.STATE_PRE
        self.send_event('E_DO_SKILL', self.common_skill_id)
        self.costing_fuel = True
        self.send_event('E_SWITCH_ACTION', 'action4', MC_DASH_BLADE_SLASH)
        self.send_event('E_SWITCH_ACTION', 'action5', MC_DASH_JUMP_1)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_DASH_JUMP_2)
        self.send_event('E_REPLACE_SHOOT_ANIM', 'dash_shoot', True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_RELOAD, 'dash_reload')
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        self.sd.ref_locked_target_finder.begin(self.sid)

    def on_begin_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 6)
        else:
            self.send_event('E_POST_ACTION', self.burst_idle_anim, LOW_BODY, 1, loop=True)

    def on_finish_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.sub_state = self.STATE_BURST

    def on_begin_air_dash(self):
        dash_dir = get_forward_by_rocker_and_camera_without_y(self)
        self.send_event('E_DO_SKILL', self.air_dash_skill_id)
        self.send_event('E_DISABLE_STATE', MC_JUMP_1)
        self.send_event('E_DISABLE_STATE', MC_JUMP_2)
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_POST_ACTION', self.dash_air_anim, LOW_BODY, 1, loop=True)
        dash_speed = self.air_dash_speed * self.ev_g_get_speed_scale()
        self.sd.ref_cur_speed = dash_speed
        self.send_event('E_SET_WALK_DIRECTION', dash_dir * dash_speed)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False

    def on_end_air_dash(self):
        self.sub_state = self.STATE_BURST
        if self.sd.ref_on_ground:
            self.send_event('E_RESET_GRAVITY')
        elif not self.ignore_gravity:
            self.send_event('E_RESET_FALL_GRAVITY')
            self.send_event('E_FALL')
        else:
            self.send_event('E_DO_SKILL', self.air_burst_skill_id)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True

    def on_begin_burst(self):
        if self.sd.ref_on_ground or self.ignore_gravity:
            if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_POST_ACTION', self.burst_anim, LOW_BODY, 6, loop=True)
            else:
                self.send_event('E_POST_ACTION', self.burst_idle_anim, LOW_BODY, 1, loop=True)

    def on_begin_end(self):
        self.end_skill()
        if not self.sd.ref_on_ground:
            self.on_finish_end()
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.end_anim_rate)
        self.send_event('E_POST_ACTION', self.end_anim, LOW_BODY, 6)
        MC_JUMP_2 in self.ev_g_cur_state() and self.send_event('E_DISABLE_STATE', MC_JUMP_2)

    def on_finish_end(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_CLEAR_SPEED')
        self.disable_self()
        if not self.sd.ref_on_ground:
            self.send_event('E_ACTIVE_STATE', MC_JUMP_2)

    def update(self, dt):
        super(BurstForm, self).update(dt)
        if self.ev_g_fuel() <= 0.0:
            self.on_fuel_exhausted()
            return
        else:
            if self.sub_state != self.STATE_AIR_DASH and (self.sd.ref_on_ground or self.ignore_gravity):
                rocker_dir = self.sd.ref_rocker_dir
                if rocker_dir != self.last_rocker_dir:
                    if self.sd.ref_on_ground or self.ignore_gravity:
                        if self.last_rocker_dir is None or self.last_rocker_dir.is_zero:
                            self.send_event('E_POST_ACTION', self.burst_anim, LOW_BODY, 6, loop=True)
                        elif rocker_dir is None or rocker_dir.is_zero:
                            self.send_event('E_POST_ACTION', self.burst_idle_anim, LOW_BODY, 1, loop=True)
                    self.last_rocker_dir = rocker_dir
                    rocker_dir is not None and self.send_event('E_ACTION_MOVE')
                if not rocker_dir or rocker_dir.is_zero:
                    walk_direction = self.ev_g_get_walk_direction()
                    if not walk_direction.is_zero:
                        walk_direction.normalize()
                else:
                    walk_direction = get_forward_by_rocker_and_camera_without_y(self)
                    if self.sd.ref_mecha_free_sight_mode_enabled:
                        self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', walk_direction)
                cur_speed = self.sd.ref_cur_speed
                acc = rocker_dir and not rocker_dir.is_zero and self.sub_state != self.STATE_END
                cur_speed += dt * (self.acc_speed if acc else self.brake_speed)
                cur_speed = clamp(cur_speed, 0, self.burst_speed * self.ev_g_get_speed_scale())
                self.sd.ref_cur_speed = cur_speed
                self.send_event('E_SET_WALK_DIRECTION', walk_direction * cur_speed)
            return

    def exit(self, enter_states):
        super(BurstForm, self).exit(enter_states)
        if self.ignore_gravity or self.sub_state == self.STATE_AIR_DASH:
            self.send_event('E_RESET_GRAVITY')
        self.end_skill()
        self.send_event('E_SWITCH_ACTION', 'action4', MC_BLADE_SLASH)
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_JUMP_2)
        self.send_event('E_RESET_SHOOT_ANIM')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_RELOAD, None)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        self.send_event('E_DO_SKILL', self.skill_id)
        if MC_DASH_BLADE_SLASH not in enter_states:
            self.sd.ref_locked_target_finder.begin(MC_BLADE_SLASH)
        elif self.sd.ref_locked_target_finder.is_cur_target_valid():
            self.sd.ref_locked_target_finder.end()
        return

    def refresh_action_param(self, action_param, custom_param):
        super(BurstForm, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()

    def on_touch_ground(self, *args):
        self.can_air_dash = True
        if not self.is_active:
            return
        self.on_begin_burst()
        self.send_event('E_DISABLE_STATE', MC_DASH_JUMP_1)
        self.send_event('E_DISABLE_STATE', MC_JUMP_2)

    def on_fuel_exhausted(self):
        if self.is_active:
            if self.sub_state != self.STATE_END:
                self.sub_state = self.STATE_END


class WeaponFire8014(WeaponFire):

    def on_post_init_complete(self, *args):
        super(WeaponFire8014, self).on_post_init_complete(*args)
        if self.ev_g_is_avatar():
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), None)
        return

    def enter(self, leave_states):
        super(WeaponFire8014, self).enter(leave_states)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), None)
        return

    def exit(self, enter_states):
        super(WeaponFire8014, self).exit(enter_states)
        is_controlled = MC_BEAT_BACK in enter_states or MC_IMMOBILIZE in enter_states or MC_FROZEN in enter_states
        if is_controlled or MC_RELOAD not in enter_states:
            self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)


class Reload8014(Reload):
    BIND_EVENT = Reload.BIND_EVENT.copy()

    def read_data_from_custom_param(self):
        super(Reload8014, self).read_data_from_custom_param()
        self.delay_enable_free_sight_duration = self.custom_param.get('delay_enable_free_sight_duration', 0.2)
        self.local_timer = None
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8014, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.is_cover_shoot = False

    def destroy(self):
        super(Reload8014, self).destroy()
        if self.local_timer:
            global_data.game_mgr.unregister_logic_timer(self.local_timer)
            self.local_timer = None
        return

    def enter(self, leave_states):
        super(Reload8014, self).enter(leave_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), None)
        self.is_cover_shoot = MC_SHOOT in leave_states
        return

    def reset_free_sight_mode(self):
        if MC_SHOOT not in self.ev_g_cur_state():
            self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
        self.local_timer = None
        return

    def exit(self, enter_states):
        super(Reload8014, self).exit(enter_states)
        if self.is_cover_shoot:
            self.local_timer = global_data.game_mgr.register_logic_timer(self.reset_free_sight_mode, self.delay_enable_free_sight_duration, times=1, mode=CLOCK)


def __editor_bladeslash_setter(self, value):
    self.hit_range = value
    self._reset_slash_hit_range()


def __editor_bladeslash_structure(self):
    slash_param_structure = []
    for i in range(self.slash_count):
        sub_structure = dict()
        sub_structure['anim_name'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d\xe7\xa7\xb0'}
        sub_structure['anim_duration'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf\xef\xbc\x88\xe5\x8f\xaf\xe6\x88\xaa\xe5\x8f\x96\xef\xbc\x89','type': 'float'}
        sub_structure['anim_rate'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','type': 'float'}
        sub_structure['play_sound_time'] = {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x9f\xb3\xe6\x95\x88\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['combo_time'] = {'zh_name': '\xe5\x8f\xaf\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['interrupt_time'] = {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['keep_time'] = {'zh_name': '\xe4\xb8\x8b\xe4\xb8\x80\xe5\x88\x80\xe5\xad\x98\xe7\x95\x99\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['begin_move_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['begin_brake_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['end_brake_time'] = {'zh_name': '\xe5\x81\x9c\xe6\xad\xa2\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['velocity'] = {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe7\xb1\xb3\xef\xbc\x89','type': 'float'}
        sub_structure['begin_attack_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['end_attack_time'] = {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['begin_damage_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['end_damage_time'] = {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
        sub_structure['hit_stop'] = {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe7\x9b\xae\xe6\xa0\x87\xe5\x81\x9c\xe6\xad\xa2\xe4\xbd\x8d\xe7\xa7\xbb','type': 'bool'}
        slash_param_structure.append({'zh_name': '\xe7\xac\xac%d\xe5\x88\x80' % (i + 1),'type': 'dict','kwargs': {'structure': sub_structure}})

    return slash_param_structure


@editor.state_exporter({('hit_range', 'param'): {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x88\xa4\xe5\xae\x9a\xe8\x8c\x83\xe5\x9b\xb4','param_type': 'list','structure': [{'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}],'setter': lambda self, value: __editor_bladeslash_setter(self, value)
                            },
   ('blade_max_locked_dist', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe9\x94\x81\xe5\xae\x9a\xe8\xb7\x9d\xe7\xa6\xbb','post_setter': lambda self: self._record_locked_target_finder_parameters()
                                        },
   ('blade_max_locked_angle', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe9\x94\x81\xe5\xae\x9a\xe8\xa7\x92\xe5\xba\xa6(\xe6\xb0\xb4\xe5\xb9\xb3\xe6\x96\xb9\xe5\x90\x91)','post_setter': lambda self: self._record_locked_target_finder_parameters()
                                         },
   ('blade_dist_prior_angle', 'param'): {'zh_name': '\xe9\x94\x81\xe5\xae\x9a\xe8\xb7\x9d\xe7\xa6\xbb\xe4\xbc\x98\xe5\x85\x88\xe8\xa7\x92\xe5\xba\xa6','post_setter': lambda self: self._record_locked_target_finder_parameters()
                                         },
   ('chase_interrupt_time', 'param'): {'zh_name': '\xe4\xb8\xad\xe6\x96\xad\xe8\xbf\xbd\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4'},('finish_chase_dist', 'meter'): {'zh_name': '\xe5\xae\x8c\xe6\x88\x90\xe8\xbf\xbd\xe5\x87\xbb\xe8\xb7\x9d\xe7\xa6\xbb'},('max_chasing_duration', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xbf\xbd\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_slash_callbacks()
                                       },
   ('chase_interrupt_time', 'meter'): {'zh_name': '\xe8\xbf\xbd\xe5\x87\xbb\xe7\xba\xbf\xe9\x80\x9f\xe5\xba\xa6'},('chasing_angular_velocity', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xbf\xbd\xe5\x87\xbb\xe8\xa7\x92\xe9\x80\x9f\xe5\xba\xa6(\xe5\x8d\x95\xe4\xbd\x8d:\xe5\xba\xa6)','min_val': 0.0,'max_val': 179.9,'getter': lambda self: self.chasing_angular_velocity * 180.0 / pi,
                                           'setter': --- This code section failed: ---

 424       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'pi'
           6  LOAD_FAST             1  'v'
           9  LOAD_GLOBAL           1  'pi'
          12  BINARY_MULTIPLY  
          13  LOAD_CONST            2  180.0
          16  BINARY_DIVIDE    
          17  CALL_FUNCTION_3       3 
          20  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 17
},
   ('chasing_step_height', 'meter'): {'zh_name': '\xe8\xbf\xbd\xe5\x87\xbb\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6(\xe8\xb2\x8c\xe4\xbc\xbc\xe6\xb2\xa1\xe5\x95\xa5\xe7\x94\xa8\xef\xbc\x8c\xe4\xb8\x8d\xe7\xa1\xae\xe5\xae\x9a)'},('slash_param_list', 'param'): {'zh_name': '\xe5\x9c\xb0\xe9\x9d\xa2\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_slash_callbacks(),
                                   'structure': lambda self: __editor_bladeslash_structure(self)
                                   },
   ('air_slash_param_list', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_slash_callbacks(),
                                       'structure': lambda self: __editor_bladeslash_structure(self)
                                       }
   })
class BladeSlash(StateBase):
    BIND_EVENT = {'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha'
       }
    STATE_NONE = -1
    STATE_INIT = 0
    STATE_CHASE = 100

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.damage_skill_id = self.custom_param.get('damage_skill_id', None)
        self.slash_count = self.custom_param.get('slash_count', 4)
        self.hit_range = self.custom_param.get('hit_range', [8, 10, 4])
        self.slash_sound_name_list = self.custom_param.get('slash_sound_name_list', [['m_8014_weapon1_a', 'nf'], ['m_8014_weapon1_b', 'nf'], ['m_8014_weapon1_c', 'nf'], ['m_8014_weapon1_d', 'nf']])
        self.slash_param_list = self.custom_param.get('slash_param_list', [])
        self.air_slash_param_list = self.custom_param.get('air_slash_param_list', [])
        self.hit_bone_map = self.custom_param.get('hit_bone_map', {})
        self.chasing_anim = self.custom_param.get('chasing_anim', 'slash_chase')
        self.chase_interrupt_time = self.custom_param.get('chase_interrupt_time', 0.5)
        self.max_chasing_duration = self.custom_param.get('max_chasing_duration', 2.0)
        self.finish_chase_dist = self.custom_param.get('finish_chase_dist', 3.0) * NEOX_UNIT_SCALE
        self.use_extended_angle = self.custom_param.get('use_extended_angle', 70) * pi / 180.0
        self.extended_finish_chase_dist = self.custom_param.get('extended_finish_chase_dist', 6.1) * NEOX_UNIT_SCALE
        self.chasing_linear_velocity = self.custom_param.get('chasing_linear_velocity', 30) * NEOX_UNIT_SCALE
        self.chasing_angular_velocity = self.custom_param.get('chasing_angular_velocity', 10) * pi / 180.0
        self.chasing_step_height = self.custom_param.get('chasing_step_height', 1.0) * NEOX_UNIT_SCALE
        self.blade_max_locked_dist = self.custom_param.get('blade_max_locked_dist', 40) * NEOX_UNIT_SCALE
        self.blade_max_locked_angle = self.custom_param.get('blade_max_locked_angle', 60)
        self.blade_dist_prior_angle = self.custom_param.get('blade_dist_prior_angle', 30)
        self._register_slash_callbacks()
        return

    def _register_slash_callbacks(self):
        self.reset_sub_states_callback()
        for state_index in range(self.slash_count):
            self._register_slash_state_callbacks(self.slash_param_list[state_index], state_index)
            self._register_slash_state_callbacks(self.air_slash_param_list[state_index], state_index + self.slash_count)

        self.register_substate_callback(self.STATE_CHASE, 0, self.begin_chase)
        self.register_substate_callback(self.STATE_CHASE, self.chase_interrupt_time, self.enable_chase_interrupted)
        self.register_substate_callback(self.STATE_CHASE, self.max_chasing_duration, self.end_chase)

    def _register_slash_state_callbacks(self, param, state_index):
        self.register_substate_callback(state_index, 0.0, self.begin_slash, param['anim_name'], param['anim_rate'])
        self.register_substate_callback(state_index, param['anim_duration'] / param['anim_rate'], self.end_slash)
        self.register_substate_callback(state_index, param['play_sound_time'] / param['anim_rate'], self.play_slash_sound)
        self.register_substate_callback(state_index, param['interrupt_time'] / param['anim_rate'], self.interrupt)
        self.register_substate_callback(state_index, param['begin_move_time'] / param['anim_rate'], self.begin_move)
        if param['begin_brake_time'] < param['end_brake_time']:
            self.register_substate_callback(state_index, param['begin_brake_time'] / param['anim_rate'], self.begin_brake)
            self.register_substate_callback(state_index, param['end_brake_time'] / param['anim_rate'], self.end_brake)
        else:
            self.register_substate_callback(state_index, param['end_brake_time'] / param['anim_rate'], self.end_brake)
        self.register_substate_callback(state_index, param['begin_attack_time'] / param['anim_rate'], self.begin_attack)
        self.register_substate_callback(state_index, param['end_attack_time'] / param['anim_rate'], self.end_attack)
        self.register_substate_callback(state_index, param['begin_damage_time'] / param['anim_rate'], self.begin_damage)
        self.register_substate_callback(state_index, param['end_damage_time'] / param['anim_rate'], self.end_damage)

    def _reset_slash_hit_range(self):
        hit_width = self.hit_range[0] * (1.0 + self.hit_range_increase_rate) * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * (1.0 + self.hit_range_increase_rate) * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * (1.0 + self.hit_range_increase_rate) * NEOX_UNIT_SCALE
        self.slash_checker.refresh_hit_range(hit_width, hit_height, hit_depth)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(BladeSlash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.hit_range_increase_rate = 0.0
        self.is_chasing = False
        self.last_chasing_dir = None
        self.is_attacking = False
        self.is_damaging = False
        self.read_data_from_custom_param()
        hit_width = self.hit_range[0] * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * NEOX_UNIT_SCALE
        self.slash_checker = SlashChecker(self, self.damage_skill_id, (hit_width, hit_height, hit_depth), check_from_biped_position=True)
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.sub_state = self.STATE_NONE
        self.cur_slash_begun = False
        self.cur_slash_begin_time = 0.0
        self.slash_interruptable = False
        self.is_braking = False
        self.sd.ref_locked_target_finder = LockedTargetFinder(self, self.get_candidate_targets_func, get_target_pos_func=self.get_target_pos_func, custom_check_target_valid_func=self.custom_check_target_valid_func, custom_check_cur_target_valid_func=self.custom_check_cur_target_valid_func)
        self.sd.ref_slash_switch_controller = SlashSwitchController(self)
        self.enable_param_changed_by_buff()
        return

    @staticmethod
    def get_candidate_targets_func():
        return six.itervalues(global_data.war_mechas)

    @staticmethod
    def get_target_pos_func(target):
        model = target.ev_g_model()
        if not model:
            return None
        else:
            matrix = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
            if matrix:
                return matrix.translation
            return model.position

    @staticmethod
    def custom_check_target_valid_func(target):
        model = target.ev_g_model()
        if not model or not model.is_visible_in_this_frame():
            return False
        if target.sd.ref_is_mecha and target.get_owner().is_share():
            if not target.sd.ref_driver_id:
                return False
        return True

    @staticmethod
    def custom_check_cur_target_valid_func(target):
        return (target.sd.ref_hp or 0) > 0

    def _record_locked_target_finder_parameters(self):
        self.sd.ref_locked_target_finder.record_parameters(self.sid, self.blade_max_locked_dist, self.blade_max_locked_angle, self.blade_dist_prior_angle)

    def on_init_complete(self):
        super(BladeSlash, self).on_init_complete()
        self._record_locked_target_finder_parameters()

    def destroy(self):
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        if self.sd.ref_locked_target_finder:
            self.sd.ref_locked_target_finder.destroy()
            self.sd.ref_locked_target_finder = None
        if self.sd.ref_slash_switch_controller:
            self.sd.ref_slash_switch_controller.destroy()
            self.sd.ref_slash_switch_controller = None
        super(BladeSlash, self).destroy()
        return

    def refresh_param_changed(self):
        self._reset_slash_hit_range()

    def _get_slash_param(self):
        if self.sub_state < self.slash_count:
            return self.slash_param_list[self.sub_state]
        return self.air_slash_param_list[self.sub_state - self.slash_count]

    def _check_on_ground--- This code section failed: ---

 583       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'ev_g_on_ground'
           6  CALL_FUNCTION_0       0 
           9  JUMP_IF_TRUE_OR_POP    21  'to 21'
          12  LOAD_GLOBAL           1  'ray_check_on_ground'
          15  LOAD_GLOBAL           1  'ray_check_on_ground'
          18  CALL_FUNCTION_2       2 
        21_0  COME_FROM                '9'
          21  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 18

    def try_next_slash(self, force=False):
        if self.sub_state == self.STATE_CHASE:
            if not self.can_interrupt_chasing and not force:
                return
            self.sub_state = self.STATE_NONE
        next_slash_state = self.sub_state + 1
        next_slash_state %= self.slash_count
        if self.sub_state != self.STATE_NONE:
            param = self._get_slash_param()
            if self.is_active:
                if param['combo_time'] / param['anim_rate'] > self.sub_sid_timer:
                    return
                self.send_event('E_CLEAR_WHITE_STATE', self.sid)
                self.slash_interruptable = False
            else:
                if param['keep_time'] < global_data.game_time - self.cur_slash_begin_time:
                    next_slash_state = self.STATE_INIT
                self.active_self()
            if not self._check_on_ground():
                next_slash_state += self.slash_count
            if self.cur_slash_begun:
                self.sub_state = next_slash_state
                self.cur_slash_begun = False
        else:
            if self.sd.ref_locked_target_finder.is_cur_target_valid():
                self.sub_state = self.STATE_CHASE
            self.cur_slash_begun = False
            self.sub_state = self.STATE_INIT if self._check_on_ground() else self.slash_count
            self.active_self()
        self.is_attacking and self.end_attack()
        self.is_damaging and self.end_damage()
        self.send_event('E_CLEAR_SPEED')

    def action_btn_down(self, force=False):
        if not self.check_can_active():
            return False
        if not (self.check_can_cast_skill() or self.sd.ref_slash_switch_controller.is_on or self.is_active and self.sub_state == self.STATE_CHASE):
            self.send_event('E_SOUND_TIP_CD')
            return False
        self.try_next_slash(force)
        return True

    def enter(self, leave_states):
        self.is_chasing = False
        self.can_interrupt_chasing = False
        self.last_chasing_dir = None
        self.is_attacking = False
        self.is_braking = False
        self.sd.ref_locked_target_finder.end()
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), 'sword_run_f', blend_dir=1, loop=True)
        if self.sub_state in (self.STATE_INIT, self.slash_count) and self.sd.ref_locked_target_finder.is_cur_target_valid():
            self.sub_state = self.STATE_CHASE
        super(BladeSlash, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False
        return

    def begin_chase(self):
        self.is_chasing = True
        self.air_walk_direction_setter.reset()
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_POST_ACTION', self.chasing_anim, LOW_BODY, 1, loop=True)
        self.send_event('E_STEP_HEIGHT', self.chasing_step_height)

    def enable_chase_interrupted(self):
        self.can_interrupt_chasing = True
        self.send_event('E_ADD_WHITE_STATE', {MC_DASH, MC_JUMP_1}, self.sid)

    def end_chase(self):
        self.is_chasing = False
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_RESET_STEP_HEIGHT')
        if not self.action_btn_down(force=True):
            self.disable_self()

    def begin_slash(self, anim_name, anim_rate):
        self.sd.ref_slash_switch_controller.on()
        slash_type = self.sub_state % self.slash_count
        self.send_event('E_DO_SKILL', self.damage_skill_id, slash_type, True)
        self.send_event('E_ANIM_RATE', LOW_BODY, anim_rate)
        self.send_event('E_POST_ACTION', anim_name, LOW_BODY, 1)
        if self.sub_state < self.slash_count:
            self.send_event('E_RESET_GRAVITY')
        else:
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)
        self.cur_slash_begun = True
        self.cur_slash_begin_time = global_data.game_time
        self.send_event('E_UPDATE_SLASH_TYPE', slash_type, self._get_slash_param()['keep_time'])

    def end_slash(self):
        self.disable_self()
        if self._check_on_ground():
            if self.sd.ref_rocker_dir:
                self.send_event('E_ACTIVE_STATE', MC_MOVE)
            else:
                self.send_event('E_CLEAR_SPEED')
                self.send_event('E_ACTIVE_STATE', MC_STAND)
        else:
            self.send_event('E_ACTIVE_STATE', MC_JUMP_2)

    def play_slash_sound(self):
        sound_name = self.slash_sound_name_list[self.sub_state % self.slash_count]
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)], True)

    def interrupt(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_JUMP_1, MC_JUMP_2, MC_JUMP_3, MC_SHOOT, MC_DRIVER_LEAVING}, self.sid)
        self.slash_interruptable = True

    def begin_move(self):
        if self.sd.ref_locked_target_finder.is_cur_target_valid():
            forward = self.sd.ref_locked_target_finder.cur_target.ev_g_position() - self.ev_g_position()
            forward.y = 0
            if not forward.is_zero:
                forward.normalize()
            self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', forward, max_lerp_duration=0.1, force=True)
        else:
            forward = get_forward_by_rocker_and_camera_without_y(self)
            self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', forward, max_lerp_duration=0.1, force=True)
        speed = self._get_slash_param()['velocity'] * NEOX_UNIT_SCALE
        self.sd.ref_cur_speed = speed
        self.send_event('E_SET_WALK_DIRECTION', forward * speed)

    def begin_brake(self):
        self.is_braking = True
        param = self._get_slash_param()
        self.brake_acc = param['velocity'] / (param['end_brake_time'] - param['begin_brake_time'])

    def end_brake(self):
        self.is_braking = False
        self.send_event('E_CLEAR_SPEED')

    def begin_attack(self):
        self.is_attacking = True
        self.slash_checker.begin_check(self._get_slash_param()['hit_stop'])

    def end_attack(self):
        self.is_attacking = False
        self.slash_checker.end_check()

    def begin_damage(self):
        self.is_damaging = True
        self.slash_checker.set_hit_bone_names(self.hit_bone_map[self.sub_state])
        self.slash_checker.set_damage_settlement_on(True)

    def end_damage(self):
        self.is_damaging = False
        self.slash_checker.set_damage_settlement_on(False)

    def update(self, dt):
        super(BladeSlash, self).update(dt)
        if self.is_chasing:
            if self.sd.ref_locked_target_finder.cur_target:
                self.sd.ref_locked_target_finder.cur_target.is_valid() or self.end_chase()
                return
            target_pos = self.sd.ref_locked_target_finder.cur_target.ev_g_position()
            cur_dir = target_pos - self.ev_g_position()
            if cur_dir.pitch < self.use_extended_angle:
                chase_dist = self.finish_chase_dist if 1 else self.extended_finish_chase_dist
                if cur_dir.length < chase_dist:
                    self.end_chase()
                    return
                cur_dir.normalize()
                if self.last_chasing_dir is None:
                    self.last_chasing_dir = cur_dir
                else:
                    angle = fabs(acos(clamp(self.last_chasing_dir.dot(cur_dir), -1.0, 1.0)))
                    if angle > self.chasing_angular_velocity:
                        self.end_chase()
                        return
                walk_direction = cur_dir * self.chasing_linear_velocity
                self.air_walk_direction_setter.execute(walk_direction)
                walk_direction.y = 0
                walk_direction.normalize()
                self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', walk_direction, force=True)
        elif self.is_braking and not self.slash_checker.moving_stopped:
            speed = self.sd.ref_cur_speed
            cur_speed = speed - self.brake_acc * dt
            if cur_speed >= 0:
                self.sd.ref_cur_speed = cur_speed
                self.send_event('E_SET_WALK_DIRECTION', self.ev_g_forward() * cur_speed)
        return

    def check_transitions(self):
        if self.slash_interruptable:
            if self._check_on_ground():
                if self.sd.ref_rocker_idr and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
            else:
                return MC_JUMP_2

    def exit(self, enter_states):
        super(BladeSlash, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_CLEAR_SPEED')
        self.is_attacking and self.end_attack()
        self.is_damaging and self.end_damage()
        self.sub_state >= self.slash_count and self.send_event('E_RESET_GRAVITY')
        if self.sub_state == self.STATE_CHASE:
            self.send_event('E_RESET_STEP_HEIGHT')
            self.sub_state = self.STATE_NONE
        self.sd.ref_locked_target_finder.begin(self.sid)
        if self.ev_g_immobilized():
            self.send_event('E_POST_ACTION', 'shake', LOW_BODY, 1)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar():
            self.sd.ref_locked_target_finder.begin(self.sid)
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)


def __editor_dashbladeslash_setter(self, value):
    self.hit_range = value
    self._reset_slash_hit_range()


@editor.state_exporter({('hit_range', 'param'): {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x88\xa4\xe5\xae\x9a\xe8\x8c\x83\xe5\x9b\xb4','param_type': 'list','structure': [{'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}],'setter': lambda self, value: __editor_dashbladeslash_setter(self, value)
                            },
   ('anim_name', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d\xe7\xa7\xb0'},('anim_duration', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf\xef\xbc\x88\xe5\x8f\xaf\xe6\x88\xaa\xe5\x8f\x96\xef\xbc\x89','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                },
   ('anim_rate', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                            },
   ('clear_speed_time', 'param'): {'zh_name': '\xe6\xb8\x85\xe7\xa9\xba\xe9\x80\x9f\xe5\xba\xa6\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                   },
   ('interrupt_time', 'param'): {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                 },
   ('begin_attack_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                    },
   ('end_attack_time', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                  },
   ('begin_damage_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                    },
   ('end_damage_time', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_callbacks()
                                  },
   ('hit_stop', 'param'): {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe7\x9b\xae\xe6\xa0\x87\xe5\x81\x9c\xe6\xad\xa2\xe4\xbd\x8d\xe7\xa7\xbb','param_type': 'bool','post_setter': lambda self: self._register_callbacks()
                           },
   ('dash_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe7\xa0\x8d\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe7\xb1\xb3\xef\xbc\x89','param_type': 'float'},('step_height', 'meter'): {'zh_name': '\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6'},('delay_find_new_target_time', 'param'): {'zh_name': '\xe7\xb4\xa2\xe6\x95\x8c\xe5\xbb\xb6\xe8\xbf\x9f\xe6\x97\xb6\xe9\x97\xb4','explain': '\xe5\x86\xb2\xe7\xa0\x8d\xe7\xbb\x93\xe6\x9d\x9f\xe5\x90\x8e\xe5\xbb\xb6\xe8\xbf\x9f\xe5\xa4\x9a\xe9\x95\xbf\xe6\x97\xb6\xe9\x97\xb4\xe6\x9f\xa5\xe6\x89\xbe\xe6\x96\xb0\xe7\x9a\x84\xe9\x94\x81\xe5\xae\x9a\xe7\x9b\xae\xe6\xa0\x87'}})
class DashBladeSlash(StateBase):
    BIND_EVENT = {}
    STATE_NONE = -1
    STATE_BEGIN = 0

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.damage_skill_id = self.custom_param.get('damage_skill_id', None)
        self.hit_range = self.custom_param.get('hit_range', [8, 10, 4])
        self.begin_attack_time = self.custom_param.get('begin_attack_time', 0)
        self.end_attack_time = self.custom_param.get('end_attack_time', 1.5)
        self.begin_damage_time = self.custom_param.get('begin_damage_time', 0)
        self.end_damage_time = self.custom_param.get('end_damage_time', 1.5)
        self.hit_stop = self.custom_param.get('hit_stop', False)
        self.anim_name = self.custom_param.get('anim_name', 'heavy_cut')
        self.anim_duration = self.custom_param.get('anim_duration', 2.1)
        self.anim_rate = self.custom_param.get('anim_rate', 1.0)
        self.clear_speed_time = self.custom_param.get('clear_speed_time', 0.6)
        self.interrupt_time = self.custom_param.get('interrupt_time', 1.5)
        self.dash_speed = self.custom_param.get('dash_speed', 5) * NEOX_UNIT_SCALE
        self.step_height = self.custom_param.get('step_height', 1.0) * NEOX_UNIT_SCALE
        self.delay_find_new_target_time = self.custom_param.get('delay_find_new_target_time', 1.0)
        self.hit_bone_name = self.custom_param.get('hit_bone_name', ('biped_bone06',
                                                                     'biped_bone09'))
        self._register_callbacks()
        return

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_BEGIN, 0, self.begin)
        self.register_substate_callback(self.STATE_BEGIN, self.clear_speed_time / self.anim_rate, self.clear_speed)
        self.register_substate_callback(self.STATE_BEGIN, self.interrupt_time / self.anim_rate, self.allow_interrupt)
        self.register_substate_callback(self.STATE_BEGIN, self.begin_attack_time, self.begin_attack)
        self.register_substate_callback(self.STATE_BEGIN, self.end_attack_time, self.end_attack)
        self.register_substate_callback(self.STATE_BEGIN, self.begin_damage_time, self.begin_damage)
        self.register_substate_callback(self.STATE_BEGIN, self.end_damage_time, self.end_damage)

    def _reset_slash_hit_range(self):
        hit_width = self.hit_range[0] * (1.0 + self.hit_range_increase_rate) * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * (1.0 + self.hit_range_increase_rate) * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * (1.0 + self.hit_range_increase_rate) * NEOX_UNIT_SCALE
        self.slash_checker.refresh_hit_range(hit_width, hit_height, hit_depth)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DashBladeSlash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.hit_range_increase_rate = 0.0
        self.is_attacking = False
        self.is_damaging = False
        self.moving = False
        self.move_direction = math3d.vector(0, 0, 1)
        self.read_data_from_custom_param()
        hit_width = self.hit_range[0] * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * NEOX_UNIT_SCALE
        self.slash_checker = SlashChecker(self, self.damage_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone_name, check_from_biped_position=True, only_damage_in_front=False)
        self.can_interrupt = False
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.enable_param_changed_by_buff()
        self._old_pos = None
        return

    def destroy(self):
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        super(DashBladeSlash, self).destroy()
        return

    def refresh_param_changed(self):
        self._reset_slash_hit_range()

    def action_btn_down(self):
        if not self.check_can_active():
            return
        if not (self.check_can_cast_skill() or self.sd.ref_slash_switch_controller.is_on):
            return
        if not self.ev_g_can_cast_skill(self.damage_skill_id):
            self.send_event('E_DISABLE_STATE', MC_DASH)
            self.send_event('E_SWITCH_ACTION', 'action4', MC_BLADE_SLASH)
            self.ev_g_action_down('action4')
            return
        self.active_self()
        return True

    def enter(self, leave_states):
        super(DashBladeSlash, self).enter(leave_states)
        self.sub_state = self.STATE_BEGIN
        self.sd.ref_slash_switch_controller.on()
        self.send_event('E_DO_SKILL', self.damage_skill_id)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), 'sword_run_f', blend_dir=1, loop=True)
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_STEP_HEIGHT', self.step_height)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def begin(self):
        if self.sd.ref_locked_target_finder.is_cur_target_valid():
            target_pos = self.sd.ref_locked_target_finder.cur_target.ev_g_position()
            direction = target_pos - self.ev_g_position()
            direction.normalize()
            forward = math3d.vector(direction)
            forward.y = 0
            forward.normalize()
            self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', forward, 0.0, True)
        else:
            direction = get_forward_by_rocker_and_camera_without_y(self)
            self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', direction, max_lerp_duration=0.0, force=True)
        self.moving = True
        self.move_direction = direction
        self.air_walk_direction_setter.reset()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, 1)
        self._old_pos = self.ev_g_position()
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False

    def clear_speed(self):
        self.moving = False
        if self.sd.ref_on_ground:
            self.send_event('E_CLEAR_SPEED')

    def allow_interrupt(self):
        self.can_interrupt = True
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_JUMP_1, MC_BLADE_SLASH}, self.sid)

    def begin_attack(self):
        self.is_attacking = True
        self.slash_checker.begin_check(self.hit_stop)

    def end_attack(self):
        self.is_attacking = False
        self.slash_checker.end_check()

    def begin_damage(self):
        self.is_damaging = True
        self.slash_checker.set_damage_settlement_on(True)

    def end_damage(self):
        self.is_damaging = False
        self.slash_checker.set_damage_settlement_on(False)

    def update(self, dt):
        super(DashBladeSlash, self).update(dt)
        if self.moving:
            self.air_walk_direction_setter.execute(self.move_direction * self.dash_speed)

    def check_transitions(self):
        if self.can_interrupt:
            if self.ev_g_on_ground() and self.sd.ref_rocker_dir:
                return MC_MOVE
        if self.elapsed_time >= self.anim_duration:
            self.disable_self()
            if self.ev_g_on_ground() or ray_check_on_ground(self):
                if self.sd.ref_rocker_dir:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(DashBladeSlash, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_RESET_STEP_HEIGHT')
        if MC_STAND in enter_states:
            self.send_event('E_CLEAR_SPEED')
        self.sub_state = self.STATE_NONE
        self.is_attacking and self.end_attack()
        self.is_damaging and self.end_damage()
        if self.sd.ref_locked_target_finder.is_cur_target_valid():
            self.sd.ref_locked_target_finder.begin(MC_BLADE_SLASH, self.delay_find_new_target_time)
        else:
            self.sd.ref_locked_target_finder.begin(MC_BLADE_SLASH)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self._check_slash_dist()
        self._old_pos = None
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True
        return

    def _check_slash_dist(self):
        if self._old_pos:
            dist = int((self.ev_g_position() - self._old_pos).length)
            if dist > 0:
                self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8014', MECHA_MEMORY_LEVEL_8, dist / NEOX_UNIT_SCALE), False, True)