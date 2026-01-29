# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8035.py
from .StateBase import StateBase, clamp
from .ShootLogic import Reload, AccumulateShootPure
from .MoveLogic import Run
from .Logic8009 import Run8009
from .Logic8011 import ActionDrivenWeaponFire
from .JumpLogic import OnGround
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gutils.character_ctrl_utils import get_forward_by_rocker_and_camera_without_y, AirWalkDirectionSetter, ray_check_on_ground
from logic.gutils.slash_utils import SlashChecker
from logic.gutils.detection_utils import CanContainMechaChecker
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_8
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK, RELEASE
from logic.gcommon import editor
import math3d
import time
STATES_WITH_FREE_SIGHT_OPERATION = {
 MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_RELOAD, MC_DASH}

class Run8035(Run8009):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Run8035, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_keep_phase = False
        self.sd.ref_force_inherit_cam_transformation = True

    def enter(self, leave_states):
        super(Run8035, self).enter(leave_states)
        self.need_keep_phase = MC_MOVE in leave_states

    def begin_run_anim(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_POST_ACTION', self.run_anim, LOW_BODY, self.run_anim_dir_type, loop=True, keep_phase=self.need_keep_phase)

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_state_running_time_stamp < self.stop_anim_cost_time and self.sd.ref_rocker_dir:
            return
        self.exit_camera()
        super(Run8009, self).begin_run_stop_anim()

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
        cur_speed += dt * (self.move_acc if acc and can_run else self.brake_acc)
        cur_speed = clamp(cur_speed, 0, max_speed)
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_MOVE', rocker_dir)
        if self.enable_dynamic_speed_rate and self.sub_state == self.STATE_RUN or self.sub_state == -1:
            self.send_event('E_ANIM_RATE', LOW_BODY, cur_speed / self.run_speed * self.dynamic_speed_rate)
        return


class ActionDrivenWeaponFire8035(ActionDrivenWeaponFire):
    BIND_EVENT = {'G_CONTINUE_FIRE': 'get_continual_fire',
       'TRY_STOP_WEAPON_ATTACK': 'disable_self'
       }

    def enter(self, leave_states):
        super(ActionDrivenWeaponFire8035, self).enter(leave_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'idle')

    def exit(self, enter_states):
        super(ActionDrivenWeaponFire, self).exit(enter_states)
        if self.is_moving:
            self.is_moving = False
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_CLEAR_SPEED')
            self.is_moving = False
        self.cur_state_exit_time = global_data.game_time
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.send_event('E_SLOW_DOWN', False)
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.need_refresh_add_factor:
            self.need_refresh_add_factor = False
            self._refresh_add_factor()
        if self.is_aim_spread:
            self.send_event('E_SET_SPREAD_RECOVER_OFF_TIME', 0)
        self._check_weapon_pos_refreshed()
        if not enter_states & STATES_WITH_FREE_SIGHT_OPERATION:
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        return


@editor.state_exporter({('post_anim_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_action_callbacks()
                                     },
   ('post_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'}})
class ShiranuiFan(ActionDrivenWeaponFire):
    BIND_EVENT = {'TRY_STOP_WEAPON_ATTACK': 'disable_self'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.post_anim_name = self.custom_param.get('post_anim_name', 'slash02')
        self.post_anim_duration = self.custom_param.get('post_anim_duration', 1.7)
        self.post_anim_rate = self.custom_param.get('post_anim_rate', 1.0)
        super(ShiranuiFan, self).read_data_from_custom_param()
        self.all_shoot_anim.add(self.post_anim_name)
        return

    def _register_action_state_callbacks(self, param, state_index):
        self.all_shoot_anim.add(param['anim_name'])
        self.register_substate_callback(state_index, 0.0, self.play_fire_animation)
        self.register_substate_callback(state_index, param['trigger_fire_time'] / (param['anim_rate'] * self.add_factor), self.trigger_fire)
        self.register_substate_callback(state_index, param['interrupt_time'] / (param['anim_rate'] * self.add_factor), self.interrupt)
        if param['move_dist'] > 0.0:
            self.register_substate_callback(state_index, param['begin_move_time'] / (param['anim_rate'] * self.add_factor), self.begin_move)
            self.register_substate_callback(state_index, param['end_move_time'] / (param['anim_rate'] * self.add_factor), self.end_move)
        self.register_substate_callback(state_index, param['anim_duration'] / (param['anim_rate'] * self.add_factor), self.fire_animation_finished)
        self.register_substate_callback(state_index, param['anim_duration'] / (param['anim_rate'] * self.add_factor) + self.post_anim_duration, self.post_animation_finished)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(ShiranuiFan, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()

    def action_btn_down(self):
        if not self.check_can_cast_skill():
            return False
        return super(ShiranuiFan, self).action_btn_down()

    def trigger_fire(self):
        super(ShiranuiFan, self).trigger_fire()
        self.send_event('E_DO_SKILL', self.skill_id)

    def interrupt(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_RELOAD, MC_SHOOT, MC_OTHER_DASH, MC_DASH}, self.sid)

    def fire_animation_finished(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.post_anim_rate)
        self.send_event('E_POST_ACTION', self.post_anim_name, UP_BODY, 1)

    def post_animation_finished(self):
        self.disable_self()

    def end_shoot(self):
        if self.is_active:
            self.disable_self()

    def exit(self, enter_states):
        super(ActionDrivenWeaponFire, self).exit(enter_states)
        if self.is_moving:
            self.is_moving = False
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_CLEAR_SPEED')
            self.is_moving = False
        self.cur_state_exit_time = global_data.game_time
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.send_event('E_SLOW_DOWN', False)
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.need_refresh_add_factor:
            self.need_refresh_add_factor = False
            self._refresh_add_factor()
        if self.is_aim_spread:
            self.send_event('E_SET_SPREAD_RECOVER_OFF_TIME', 0)
        self._check_weapon_pos_refreshed()
        if not enter_states & STATES_WITH_FREE_SIGHT_OPERATION:
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')


@editor.state_exporter({('post_combo_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8f\xaf\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callbacks()
                                  },
   ('end_anim_duration', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                    },
   ('end_anim_rate', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'}})
class AccumulateShoot8035(AccumulateShootPure):
    BIND_EVENT = {'TRY_STOP_WEAPON_ATTACK': 'interrupt_shoot',
       'E_SKILL_BUTTON_BOUNDED': 'on_skill_button_bounded'
       }
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD, MC_DASH, MC_OTHER_DASH}

    def read_data_from_custom_param(self):
        self.sub_skill_id = self.custom_param.get('sub_skill_id', 803557)
        self.post_combo_time = self.custom_param.get('post_combo_time', 0.4)
        self.end_anim_name = self.custom_param.get('end_anim', 'slash_end')
        self.end_anim_duration = self.custom_param.get('end_anim_duration', 1.0)
        self.end_anim_rate = self.custom_param.get('end_anim_rate', 1.0)
        super(AccumulateShoot8035, self).read_data_from_custom_param()
        self.all_anim_name_set.add(self.end_anim_name)

    def register_callbacks(self):
        super(AccumulateShoot8035, self).register_callbacks()
        self.register_substate_callback(self.STATE_POST, self.post_combo_time, self.on_enable_combo)
        self.register_substate_callback(self.STATE_POST, self.post_anim_duration + self.end_anim_duration, self.on_end)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateShoot8035, self).init_from_dict(unit_obj, bdict, sid, info)
        self.combo_enabled = False
        self.can_enable_combo = True

    def check_can_cast_skill(self):
        if not self.skill_id or not self.sub_skill_id:
            return True
        return self.ev_g_can_cast_skill(self.skill_id) and self.ev_g_can_cast_skill(self.sub_skill_id)

    def action_btn_down(self):
        super(AccumulateShootPure, self).action_btn_down()
        self.btn_down = True
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        if self.is_active:
            if self.combo_enabled:
                self.sub_state = self.STATE_LOOP
                self.acc_skill_ended = False
                self.send_event('E_ACC_SKILL_BEGIN', self.weapon_pos)
                return True
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(AccumulateShoot8035, self).enter(leave_states)
        self.combo_enabled = False
        self.can_enable_combo = True
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'idle')

    def on_begin_post(self):
        self.send_event('E_DO_SKILL', self.sub_skill_id)
        super(AccumulateShoot8035, self).on_begin_post()

    def on_end_post(self):
        self.send_event('E_ANIM_RATE', self.PART, self.end_anim_rate)
        self.send_event('E_POST_ACTION', self.end_anim_name, self.PART, 1)

    def on_enable_combo(self):
        if self.can_enable_combo:
            self.combo_enabled = True

    def on_end(self):
        self.disable_self()

    def exit(self, enter_states):
        super(AccumulateShoot8035, self).exit(enter_states)
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        return

    def cancel_shoot(self):
        self.sub_state = self.STATE_POST
        self.sub_sid_timer = self.post_anim_duration
        self.on_enable_break_post()
        self.can_enable_combo = False
        self.send_event('E_ACTION_UP', self.bind_action_id)

    def interrupt_shoot(self):
        if self.is_active:
            self.send_event('E_ACTION_UP', self.bind_action_id)
            self.disable_self()

    def on_skill_button_bounded(self, skill_id):
        if self.skill_id != skill_id:
            return
        self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)


@editor.state_exporter({('break_in_advance_time', 'param'): {'zh_name': '\xe6\x8f\x90\xe5\x89\x8d\xe8\xa2\xab\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'}})
class Reload8035(Reload):

    def read_data_from_custom_param(self):
        super(Reload8035, self).read_data_from_custom_param()
        self.break_in_advance_time = self.custom_param.get('break_in_advance_time', 1.3)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8035, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.is_cover_shoot = False

    def enter(self, leave_states):
        super(Reload8035, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'reload')
        self.is_cover_shoot = MC_SHOOT in leave_states

    def check_transitions(self):
        if self.break_in_advance_time <= self.elapsed_time and MC_MOVE in self.ev_g_cur_state():
            self.disable_self()
            return
        else:
            if self.reloaded:
                self.disable_self()
            continue_fire, _ = self.ev_g_continue_fire() or (False, None)
            if continue_fire:
                return MC_SHOOT
            return

    def exit(self, enter_states):
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        super(Reload8035, self).exit(enter_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if not enter_states & STATES_WITH_FREE_SIGHT_OPERATION:
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        return

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        self.reloaded = True
        continue_fire, fire_weapon_pos = self.ev_g_continue_fire() or (False, None)
        if continue_fire and fire_weapon_pos == weapon_pos:
            self.continue_fire = True
        return


UP_BODY_STATES = {
 MC_SHOOT, MC_SECOND_WEAPON_ATTACK}

@editor.state_exporter({('dash_duration', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4'},('dash_anim_rate', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                 },
   ('dash_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6'},('finish_acc_time', 'param'): {'zh_name': '\xe5\xae\x8c\xe6\x88\x90\xe5\x8a\xa0\xe9\x80\x9f\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                  },
   ('begin_dec_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                 },
   ('finish_dec_time', 'param'): {'zh_name': '\xe5\xae\x8c\xe6\x88\x90\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                  },
   ('enable_active_break_time', 'param'): {'zh_name': '\xe5\x85\x81\xe8\xae\xb8\xe4\xb8\xbb\xe5\x8a\xa8\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks()
                                           },
   ('enable_passive_break_time', 'param'): {'zh_name': '\xe5\x85\x81\xe8\xae\xb8\xe8\xa2\xab\xe5\x8a\xa8\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks()
                                            },
   ('exit_state_camera_in_advance_time', 'param'): {'zh_name': '\xe6\x8f\x90\xe5\x89\x8d\xe9\x80\x80\xe5\x87\xba\xe7\x8a\xb6\xe6\x80\x81\xe9\x95\x9c\xe5\xa4\xb4\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks()
                                                    }
   })
class Dash8035(StateBase):
    BIND_EVENT = {}
    STATE_ACC = 0
    STATE_DASH = 1
    ACTIVE_BREAK_STATES = {
     MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_OTHER_DASH}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 803552)
        self.dash_anim_name = self.custom_param.get('dash_anim_name', 'dash_f')
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1.0)
        self.finish_acc_time = self.custom_param.get('finish_acc_time', 0.3)
        self.begin_dec_time = self.custom_param.get('begin_dec_time', 0.9)
        self.finish_dec_time = self.custom_param.get('finish_dec_time', 1.0)
        self.enable_active_break_time = self.custom_param.get('enable_active_break_time', 0.8)
        self.enable_passive_break_time = self.custom_param.get('enable_passive_break_time', 0.8)
        self.exit_state_camera_in_advance_time = self.custom_param.get('exit_state_camera_in_advance_time', 0.9)
        self.dash_speed = self.custom_param.get('dash_speed', 40) * NEOX_UNIT_SCALE
        self.dash_duration = self.custom_param.get('dash_duration', 1.0)
        self._register_callbacks()

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_ACC, 0, self.on_begin_acc)
        self.register_substate_callback(self.STATE_ACC, self.finish_acc_time / self.dash_anim_rate, self.on_finish_acc)
        self.register_substate_callback(self.STATE_DASH, 0, self.on_begin_uniform_dash)
        self.register_substate_callback(self.STATE_DASH, (self.begin_dec_time - self.finish_acc_time) / self.dash_anim_rate, self.on_begin_dec)
        self.register_substate_callback(self.STATE_DASH, (self.finish_dec_time - self.finish_acc_time) / self.dash_anim_rate, self.on_finish_dec)
        self.register_substate_callback(self.STATE_DASH, (self.enable_active_break_time - self.finish_acc_time) / self.dash_anim_rate, self.on_enable_active_break)
        self.register_substate_callback(self.STATE_DASH, (self.enable_passive_break_time - self.finish_acc_time) / self.dash_anim_rate, self.on_enable_passive_break)
        self.register_substate_callback(self.STATE_DASH, (self.exit_state_camera_in_advance_time - self.finish_acc_time) / self.dash_anim_rate, self.on_exit_camera)
        self.register_substate_callback(self.STATE_DASH, (self.dash_duration - self.finish_acc_time) / self.dash_anim_rate, self.on_end_dash)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8035, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.moving = False
        self.need_update_speed = False
        self.can_passive_break = False
        self.need_reset_gravity = False
        self.need_exit_camera_in_advance = False
        self.dash_end = False
        self.walk_direction = math3d.vector(0, 0, 1)
        self.dash_dir = math3d.vector(0, 0, 1)
        self.acc_speed = 0
        self.cur_speed = 0
        self.speed_add_scale = 0
        self._dash_dis = 0
        self.enable_param_changed_by_buff()

    def refresh_param_changed(self):
        self.dash_speed = self.custom_param.get('dash_speed', 40) * NEOX_UNIT_SCALE * (1 + self.speed_add_scale)

    def destroy(self):
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        super(Dash8035, self).destroy()
        return

    def action_btn_down(self):
        if self.is_active:
            return True
        if not self.check_can_cast_skill():
            return False
        if self.ev_g_try_fly_to_fan():
            return True
        if not self.check_can_active():
            return False
        self.active_self()
        super(Dash8035, self).action_btn_down()
        return True

    def enter(self, leave_states):
        start_phase = 0
        if not self.ev_g_on_ground():
            self.send_event('E_GRAVITY', 0)
            self.need_reset_gravity = True
            start_phase = 0.1
            self.sub_state = self.STATE_DASH
            self.need_exit_camera_in_advance = False
            self.auto_delay_camera = False
        else:
            self.sub_state = self.STATE_ACC
            self.need_exit_camera_in_advance = True
            self.auto_delay_camera = True
        super(Dash8035, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.skill_id, False)
        self.send_event('E_DO_DASH_SKILL')
        self.air_walk_direction_setter.reset()
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        dash_dir = get_forward_by_rocker_and_camera_without_y(self)
        self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', dash_dir)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        self.send_event('E_POST_ACTION', self.dash_anim_name, LOW_BODY, 1, phase=start_phase)
        self._start_cal_dash_dist()
        self.walk_direction = dash_dir * self.dash_speed
        self.dash_dir = dash_dir
        self.moving = True
        self.need_update_speed = False
        self.can_passive_break = False
        self.dash_end = False
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8035', MECHA_MEMORY_LEVEL_8, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def on_begin_acc(self):
        self.cur_speed = 0
        self.acc_speed = self.dash_speed / self.finish_acc_time
        self.need_update_speed = True

    def on_finish_acc(self):
        self.need_update_speed = False
        self.sub_state = self.STATE_DASH

    def on_begin_uniform_dash(self):
        self.send_event('E_SHOW_DASH_EFFECT', True)
        self.cur_speed = self.dash_speed

    def on_begin_dec(self):
        self.cur_speed = self.dash_speed
        self.acc_speed = -self.dash_speed / (self.finish_dec_time - self.begin_dec_time)
        self.need_update_speed = True

    def _reset_gravity(self):
        if self.need_reset_gravity or self.air_walk_direction_setter.gravity_removed:
            self.send_event('E_RESET_GRAVITY')
            self.need_reset_gravity = False
            self.air_walk_direction_setter.gravity_removed = False

    def on_finish_dec(self):
        self.moving = False
        self.need_update_speed = False
        self.send_event('E_CLEAR_SPEED')
        if self.ev_g_on_ground() or ray_check_on_ground(self):
            self._reset_gravity()

    def on_enable_active_break(self):
        self.send_event('E_ADD_WHITE_STATE', self.ACTIVE_BREAK_STATES, self.sid)

    def on_enable_passive_break(self):
        self.can_passive_break = True

    def on_exit_camera(self):
        if not self.need_exit_camera_in_advance:
            return
        self.exit_camera()
        self.send_event('E_SHOW_DASH_EFFECT', False)

    def on_end_dash(self):
        self.dash_end = True

    def update(self, dt):
        super(Dash8035, self).update(dt)
        if self.moving:
            if self.need_update_speed:
                self.cur_speed = self.cur_speed + self.acc_speed * dt
                self.air_walk_direction_setter.execute(self.dash_dir * self.cur_speed)
                self.sd.ref_cur_speed = self.cur_speed
            else:
                self.air_walk_direction_setter.execute(self.walk_direction)

    def _get_cover_state(self, state_id):
        self.send_event('E_ADD_WHITE_STATE', {state_id}, self.sid)
        return state_id

    def check_transitions(self):
        if self.can_passive_break:
            physical_on_ground = self.ev_g_on_ground()
            if physical_on_ground or ray_check_on_ground(self):
                self._reset_gravity()
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero and physical_on_ground:
                    return self._get_cover_state(MC_MOVE)
                if self.dash_end:
                    return self._get_cover_state(MC_STAND)
            else:
                return self._get_cover_state(MC_JUMP_2)

    def exit(self, enter_states):
        super(Dash8035, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        if UP_BODY_STATES & enter_states:
            physical_on_ground = self.ev_g_on_ground()
            if physical_on_ground or ray_check_on_ground(self):
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero and physical_on_ground:
                    self.send_event('E_ACTIVE_STATE', MC_MOVE)
                else:
                    self.send_event('E_ACTIVE_STATE', MC_STAND)
            else:
                self.send_event('E_ACTIVE_STATE', MC_JUMP_2)
        self._reset_gravity()
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True
        self.send_event('E_SHOW_DASH_EFFECT', False)
        self._finish_cal_dash_dist()
        self.send_event('E_IGNORE_RELOAD_ANIM', False)


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('dance_anim_duration', 'param'): {'zh_name': '\xe8\x88\x9e\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks()
                                      },
   ('dance_anim_rate', 'param'): {'zh_name': '\xe8\x88\x9e\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                  },
   ('begin_damage_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                    },
   ('end_damage_time', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                  },
   ('enable_active_break_time', 'param'): {'zh_name': '\xe5\x85\x81\xe8\xae\xb8\xe4\xb8\xbb\xe5\x8a\xa8\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','explain': '\xe4\xb8\xbb\xe5\x89\xaf\xe6\xad\xa6\xe5\x99\xa8/\xe5\x86\xb2\xe5\x88\xba\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks()
                                           },
   ('enable_passive_break_time', 'param'): {'zh_name': '\xe5\x85\x81\xe8\xae\xb8\xe8\xa2\xab\xe5\x8a\xa8\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','explain': '\xe4\xb8\x8b\xe8\x90\xbd\xe5\x92\x8c\xe6\x93\x8d\xe4\xbd\x9c\xe6\x91\x87\xe6\x9d\x86\xe4\xbd\x8d\xe7\xa7\xbb\xe7\x9a\x84\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks()
                                            },
   ('fly_speed', 'meter'): {'zh_name': '\xe9\xa3\x9e\xe8\xa1\x8c\xe9\x80\x9f\xe5\xba\xa6'},('dance_range', 'param'): {'zh_name': '\xe8\x88\x9e\xe5\x8a\xa8\xe4\xbc\xa4\xe5\xae\xb3\xe5\x88\xa4\xe5\xae\x9a\xe8\x8c\x83\xe5\x9b\xb4',
                              'param_type': 'list','structure': [{'zh_name': '\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}],'post_setter': lambda self: self._reset_dance_range()
                              },
   ('lock_miss_threshold', 'param'): {'zh_name': '\xe9\x94\x81\xe5\xae\x9a\xe5\x85\x81\xe8\xae\xb8\xe8\xaf\xaf\xe5\xb7\xae\xe6\x97\xb6\xe9\x97\xb4'}})
class FlyToFan(StateBase):
    BIND_EVENT = {'G_TRY_FLY_TO_FAN': 'try_fly_to_fan'
       }
    STATE_PRE = 0
    STATE_FLY = 1
    STATE_DANCE = 2
    ACTIVE_BREAK_STATES = {
     MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_DASH}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.damage_skill_id = self.custom_param.get('damage_skill_id', None)
        self.pre_anim_name = self.custom_param.get('pre_anim_name', 'dash_fly_start')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.2)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.loop_anim_name = self.custom_param.get('loop_anim_name', 'dash_fly_loop')
        self.dance_anim_name = self.custom_param.get('dance_anim_name', 'dash_fly_dance')
        self.dance_anim_duration = self.custom_param.get('dance_anim_duration', 2.2)
        self.dance_anim_rate = self.custom_param.get('dance_anim_rate', 1.0)
        self.begin_damage_time = self.custom_param.get('begin_damage_time', 0.0)
        self.end_damage_time = self.custom_param.get('end_damage_time', 1.6)
        self.enable_active_break_time = self.custom_param.get('enable_active_break_time', 1.7)
        self.enable_passive_break_time = self.custom_param.get('enable_passive_break_time', 1.7)
        self.fly_speed = self.custom_param.get('fly_speed', 60) * NEOX_UNIT_SCALE
        self.dance_range = self.custom_param.get('dance_range', [10, 10, 10])
        self.hit_bone_name = self.custom_param.get('hit_bone_name', ('bone_wing_l_mid',
                                                                     'bone_wing_r_mid'))
        self.lock_miss_threshold = self.custom_param.get('lock_miss_threshold', 0.1)
        self._register_callbacks()
        return

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration, self.on_end_pre)
        self.register_substate_callback(self.STATE_FLY, 0, self.on_begin_fly)
        self.register_substate_callback(self.STATE_DANCE, 0, self.on_begin_dance)
        self.register_substate_callback(self.STATE_DANCE, self.begin_damage_time / self.dance_anim_rate, self.on_begin_damage)
        self.register_substate_callback(self.STATE_DANCE, self.end_damage_time / self.dance_anim_rate, self.on_end_damage)
        self.register_substate_callback(self.STATE_DANCE, self.enable_active_break_time / self.dance_anim_rate, self.on_enable_active_break)
        self.register_substate_callback(self.STATE_DANCE, self.enable_passive_break_time / self.dance_anim_rate, self.on_enable_passive_break)
        self.register_substate_callback(self.STATE_DANCE, self.dance_anim_duration / self.dance_anim_rate, self.on_end_dance)

    def _reset_dance_range(self):
        hit_width = self.dance_range[0] * NEOX_UNIT_SCALE
        hit_height = self.dance_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.dance_range[2] * NEOX_UNIT_SCALE
        self.slash_checker.refresh_hit_range(hit_width, hit_height, hit_depth)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(FlyToFan, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        hit_width = self.dance_range[0] * NEOX_UNIT_SCALE
        hit_height = self.dance_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.dance_range[2] * NEOX_UNIT_SCALE
        self.slash_checker = SlashChecker(self, self.damage_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone_name, check_from_biped_position=True, damage_settlement_always_on=True, only_damage_in_front=False)
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.can_contain_mecha_checker = CanContainMechaChecker(8035)
        self.is_moving = False
        self.cur_group = None
        self.cur_mask = None
        self.need_reset_gravity = False
        self.teleport_timer = None
        self.cur_target_fan_unit = None
        self.can_passive_break = False
        self.fly_target_pos = None
        self.dance_end = False
        self.action_forbidden = False
        self.lock_range_add_scale = 0
        self.sd.ref_shiranui_fan_lock_range_add_scale = 0
        self.enable_param_changed_by_buff()
        self._dash_dis = 0
        return

    def refresh_param_changed(self):
        self.sd.ref_shiranui_fan_lock_range_add_scale = self.lock_range_add_scale
        self.send_event('E_SHIRANUI_FAN_LOCK_RANGE_ADD_SCALE_CHANGED')

    def _unregister_teleport_timer(self):
        if self.teleport_timer:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.teleport_timer)
            self.teleport_timer = None
        return

    def destroy(self):
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        if self.can_contain_mecha_checker:
            self.can_contain_mecha_checker.destroy()
            self.can_contain_mecha_checker = None
        self._unregister_teleport_timer()
        super(FlyToFan, self).destroy()
        return

    def enter(self, leave_states):
        super(FlyToFan, self).enter(leave_states)
        self.sub_state = self.STATE_PRE
        self.can_passive_break = False
        self.dance_end = False
        self.send_event('E_GRAVITY', 0)
        self.need_reset_gravity = True
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_DO_SKILL', self.skill_id, True)
        self.send_event('E_DO_DASH_SKILL')
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        if self.cur_target_fan_unit and self.cur_target_fan_unit.is_valid():
            self.send_event('E_SHIRANUI_FAN_DESTROYED', self.cur_target_fan_unit)
        direction = self.fly_target_pos - self.ev_g_position()
        direction.y = 0
        if not direction.is_zero:
            direction.normalize()
            self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', direction)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False
        self._start_cal_dash_dist()
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8035', MECHA_MEMORY_LEVEL_8, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def _try_reset_collision_state(self):
        if self.cur_group:
            self.send_event('E_SET_CHAR_GROUP', self.cur_group)
            self.cur_group = None
        if self.cur_mask:
            self.send_event('E_SET_CHAR_MASK', self.cur_mask)
            self.cur_mask = None
        return

    def teleport(self, dt):
        cur_pos = self.ev_g_position()
        vec = self.fly_target_pos - cur_pos
        dist = vec.length
        fly_dist = self.fly_speed * dt
        if dist < 3 * NEOX_UNIT_SCALE:
            self.can_contain_mecha_checker.check(cur_pos) and self._try_reset_collision_state()
        if dist < fly_dist:
            self.sub_state = self.STATE_DANCE
            self.send_event('E_FOOT_POSITION', self.fly_target_pos)
            if self.cur_target_fan_unit and self.cur_target_fan_unit.is_valid():
                self.cur_target_fan_unit.send_event('E_REACH_SHIRANUI_FAN')
            self.teleport_timer = None
            return RELEASE
        else:
            vec.normalize()
            self.send_event('E_FOOT_POSITION', cur_pos + vec * fly_dist)
            return

    def _try_begin_move(self):
        if self.teleport_timer:
            return
        self.teleport_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self.teleport, interval=1, times=-1, timedelta=True)
        self.cur_group = self.ev_g_char_group()
        self.cur_mask = self.ev_g_char_mask()
        self.send_event('E_SET_CHAR_GROUP', 0)
        self.send_event('E_SET_CHAR_MASK', 0)
        self.start_custom_sound('fly')

    def on_begin_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim_name, LOW_BODY, 1)
        self._try_begin_move()

    def on_end_pre(self):
        self.sub_state = self.STATE_FLY

    def on_begin_fly(self):
        self.send_event('E_POST_ACTION', self.loop_anim_name, LOW_BODY, 1, loop=True)
        self._try_begin_move()

    def _try_end_move(self):
        self._unregister_teleport_timer()
        self._try_reset_collision_state()

    def on_begin_dance(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dance_anim_rate)
        self.send_event('E_POST_ACTION', self.dance_anim_name, LOW_BODY, 1)
        self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', self.sd.ref_effective_camera_rot.get_forward())
        self._try_end_move()
        self.end_custom_sound('fly')
        self.start_custom_sound('arrived')

    def on_begin_damage(self):
        self.send_event('E_DO_SKILL', self.damage_skill_id)
        self.slash_checker.begin_check(False)
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_1}, self.sid)

    def on_end_damage(self):
        self.slash_checker.end_check()

    def _reset_gravity(self):
        if self.need_reset_gravity:
            self.send_event('E_RESET_GRAVITY')
            self.need_reset_gravity = False

    def on_enable_active_break(self):
        self.send_event('E_ADD_WHITE_STATE', self.ACTIVE_BREAK_STATES, self.sid)
        if self.ev_g_on_ground() or ray_check_on_ground(self):
            self._reset_gravity()

    def on_enable_passive_break(self):
        self.can_passive_break = True

    def on_end_dance(self):
        self.dance_end = True

    def update(self, dt):
        super(FlyToFan, self).update(dt)

    def _get_cover_state(self, state_id):
        self.send_event('E_ADD_WHITE_STATE', {state_id}, self.sid)
        return state_id

    def check_transitions(self):
        if self.can_passive_break:
            physical_on_ground = self.ev_g_on_ground()
            if physical_on_ground or ray_check_on_ground(self):
                self._reset_gravity()
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero and physical_on_ground:
                    return self._get_cover_state(MC_MOVE)
                if self.dance_end:
                    return self._get_cover_state(MC_STAND)
            else:
                return self._get_cover_state(MC_JUMP_2)

    def exit(self, enter_states):
        super(FlyToFan, self).exit(enter_states)
        if UP_BODY_STATES & enter_states:
            physical_on_ground = self.ev_g_on_ground()
            if physical_on_ground or ray_check_on_ground(self):
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero and physical_on_ground:
                    self.send_event('E_ACTIVE_STATE', MC_MOVE)
                else:
                    self.send_event('E_ACTIVE_STATE', MC_STAND)
            else:
                self.send_event('E_ACTIVE_STATE', MC_JUMP_2)
        self._reset_gravity()
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        self.slash_checker.end_check()
        self._unregister_teleport_timer()
        self.cur_target_fan_unit = None
        self._try_reset_collision_state()
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True
        self.end_custom_sound('fly')
        self.end_custom_sound('arrived')
        self._finish_cal_dash_dist()
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        return

    def try_fly_to_fan(self):
        if self.is_active:
            return False
        else:
            if not self.check_can_active():
                return False
            valid_fan_unit = None
            if self.sd.ref_cur_locked_fan_unit:
                valid_fan_unit = self.sd.ref_cur_locked_fan_unit
            else:
                fan_unit = self.sd.ref_last_locked_fan_unit
                if fan_unit and fan_unit.is_valid() and global_data.game_time - self.sd.ref_switch_locked_fan_unit_time < self.lock_miss_threshold:
                    m = fan_unit.ev_g_model()
                    if m and m.is_visible_in_this_frame():
                        valid_fan_unit = fan_unit
                if valid_fan_unit is None:
                    return False
                target_pos = valid_fan_unit.ev_g_try_suspend_shiranui_fan()
                if not target_pos:
                    return False
            self.cur_target_fan_unit = valid_fan_unit
            self.fly_target_pos = target_pos
            self.active_self()
            super(FlyToFan, self).action_btn_down()
            return True