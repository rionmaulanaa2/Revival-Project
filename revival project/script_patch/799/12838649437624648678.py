# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8028.py
from __future__ import absolute_import
from six.moves import range
from .StateBase import StateBase
from .ShootLogic import Reload, AccumulateShootPure
from .Logic8009 import Run8009
from .Logic8011 import ActionDrivenWeaponFire, StandWithGuard
from .StateLogic import Immobilize, OnFrozen, BeatBack
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.common_const.mecha_const import MECHA_8028_FORM_RABBIT
from logic.gcommon.const import NEOX_UNIT_SCALE, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN6, PART_WEAPON_POS_MAIN8
from logic.gutils.character_ctrl_utils import get_forward_by_rocker_and_camera_without_y
from logic.comsys.control_ui.ShotChecker import ShotChecker
from common.utils.timer import CLOCK
from logic.gcommon import editor
from math import sqrt
import math3d
import time
import random
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_8

@editor.state_exporter({('fairy_horizontal_speed', 'meter'): {'zh_name': '\xe4\xbb\x99\xe5\xa5\xb3\xe6\x82\xac\xe6\xb5\xae\xe5\xbc\x80\xe7\x81\xab\xe6\xb0\xb4\xe5\xb9\xb3\xe6\x96\xb9\xe5\x90\x91\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('fairy_rise_speed', 'meter'): {'zh_name': '\xe4\xbb\x99\xe5\xa5\xb3\xe6\x82\xac\xe6\xb5\xae\xe5\xbc\x80\xe7\x81\xab\xe4\xb8\x8a\xe5\x8d\x87\xe9\x80\x9f\xe5\xba\xa6'},('fairy_fall_speed', 'meter'): {'zh_name': '\xe4\xbb\x99\xe5\xa5\xb3\xe6\x82\xac\xe6\xb5\xae\xe5\xbc\x80\xe7\x81\xab\xe4\xb8\x8b\xe8\x90\xbd\xe9\x80\x9f\xe5\xba\xa6'}})
class WeaponFire8028(ActionDrivenWeaponFire):
    BIND_EVENT = {'G_CONTINUE_FIRE': 'get_continual_fire',
       'TRY_STOP_WEAPON_ATTACK': 'disable_self'
       }

    def read_data_from_custom_param(self):
        super(WeaponFire8028, self).read_data_from_custom_param()
        self.fairy_horizontal_speed = self.custom_param.get('fairy_horizontal_speed', 10) * NEOX_UNIT_SCALE
        self.fairy_rise_speed = self.custom_param.get('fairy_rise_speed', 5) * NEOX_UNIT_SCALE
        self.fairy_fall_speed = self.custom_param.get('fairy_fall_speed', 5) * NEOX_UNIT_SCALE

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(WeaponFire8028, self).init_from_dict(unit_obj, bdict, sid, info)
        self.move_anim_replaced = False

    def enter(self, leave_states):
        super(WeaponFire8028, self).enter(leave_states)
        if self.sd.ref_is_fairy_shape:
            self.send_event('E_FAIRY_FIRE_SLOW_DOWN', True, self.fairy_horizontal_speed, self.fairy_rise_speed, self.fairy_fall_speed)
        else:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), 'rabt_run', blend_dir=6, loop=True, keep_phase=True)
            self.move_anim_replaced = True
            self.send_event('E_SLOW_DOWN', True, self.move_action_slow_speed)

    def exit(self, enter_states):
        super(ActionDrivenWeaponFire, self).exit(enter_states)
        if MC_RELOAD not in enter_states:
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        if self.is_moving:
            self.is_moving = False
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_CLEAR_SPEED')
            self.is_moving = False
        self.cur_state_exit_time = global_data.game_time
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_FAIRY_FIRE_SLOW_DOWN', False)
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
        if self.move_anim_replaced:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE, MC_RUN), None)
            self.move_anim_replaced = False
        return


@editor.state_exporter({('break_in_advance_time', 'param'): {'zh_name': '\xe6\x8f\x90\xe5\x89\x8d\xe8\xa2\xab\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'}})
class Reload8028(Reload):
    BIND_EVENT = Reload.BIND_EVENT.copy()
    BIND_EVENT.update({'E_TRY_FAIRY_RELOAD': 'action_btn_down'
       })
    ALL_SHOOT_STATES = {
     MC_SHOOT, MC_FULL_FORCE_SHOOT}

    def read_data_from_custom_param(self):
        super(Reload8028, self).read_data_from_custom_param()
        self.break_in_advance_time = self.custom_param.get('break_in_advance_time', 1.3)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8028, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.is_cover_shoot = False

    def enter(self, leave_states):
        super(Reload8028, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'rabt_reload')
        self.is_cover_shoot = self.ALL_SHOOT_STATES & leave_states

    def check_transitions(self):
        if self.break_in_advance_time <= self.elapsed_time and MC_MOVE in self.ev_g_cur_state():
            self.disable_self()
            return
        else:
            if self.reloaded:
                self.disable_self()
            continue_fire, _ = self.ev_g_continue_fire() or (False, None)
            if continue_fire:
                if self.weapon_pos == PART_WEAPON_POS_MAIN2:
                    return MC_FULL_FORCE_SHOOT
                return MC_SHOOT
            return

    def exit(self, enter_states):
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        super(Reload8028, self).exit(enter_states)
        if self.is_cover_shoot:
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        return

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        self.reloaded = True
        continue_fire, fire_weapon_pos = self.ev_g_continue_fire() or (False, None)
        if continue_fire and fire_weapon_pos == weapon_pos:
            self.continue_fire = True
        return


@editor.state_exporter({('accumulate_interval', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe9\x97\xb4\xe9\x9a\x94'},('max_accumulate_count', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\x93\x84\xe5\x8a\x9b\xe5\xad\x90\xe5\xbc\xb9\xe6\x95\xb0'},('auto_fire_time', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe5\xae\x8c\xe6\x88\x90\xe5\x90\x8e\xe8\x87\xaa\xe5\x8a\xa8\xe5\x8f\x91\xe5\xb0\x84\xe6\x97\xb6\xe9\x97\xb4'},('fire_interval', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe9\x97\xb4\xe9\x9a\x94'}})
class AccumulateShoot8028(AccumulateShootPure):
    BIND_EVENT = AccumulateShootPure.BIND_EVENT.copy()
    BIND_EVENT.update({'E_USE_DASH_WEAPON_POS': 'use_dash_weapon_pos'
       })

    def read_data_from_custom_param(self):
        super(AccumulateShoot8028, self).read_data_from_custom_param()
        self.special_weapon_pos = self.custom_param.get('special_weapon_pos', self.weapon_pos)
        self.accumulate_interval = self.custom_param.get('accumulate_interval', 0.4)
        self.max_accumulate_count = self.custom_param.get('max_accumulate_count', 6)
        self.auto_fire_time = self.custom_param.get('auto_fire_time', 1.2)
        self.fire_interval = self.custom_param.get('fire_interval', 0.05)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateShoot8028, self).init_from_dict(unit_obj, bdict, sid, info)
        self.sd.ref_accumulate_pre_anim_duration = self.pre_anim_duration
        self.sd.ref_accumulate_interval = self.accumulate_interval
        self.accumulate_count = 0
        self.fire_index = 0
        self.cur_max_accumulate_count = self.max_accumulate_count
        self.sd.ref_cur_max_accumulate_index = self.cur_max_accumulate_count - 1
        self.last_tag_time = 0
        self.accumulating = False
        self.firing = False
        self.breakable = False
        self.enhanced_weapon_pos = PART_WEAPON_POS_MAIN6
        self.enhanced_special_weapon_pos = PART_WEAPON_POS_MAIN8
        self.is_rabbit_enhanced = False
        self.is_fairy_enhanced = False
        self.first_shoot_after_switch = False
        self.dashing = False
        self.enable_param_changed_by_buff()

    def refresh_param_changed(self):
        if self.sd.ref_is_fairy_shape or self.is_rabbit_enhanced:
            if self.dashing:
                self.weapon_pos = self.enhanced_special_weapon_pos if 1 else self.enhanced_weapon_pos
            else:
                self.weapon_pos = self.special_weapon_pos if self.dashing else self.custom_param['weapon_pos']

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
            if self.sd.ref_is_fairy_shape:
                weapon = self.sd.ref_wp_bar_mp_weapons[self.weapon_pos]
                if weapon.get_bullet_num() < weapon.get_cost_ratio():
                    self.send_event('E_TRY_FAIRY_RELOAD')
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(AccumulateShoot8028, self).enter(leave_states)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        if self.sd.ref_is_fairy_shape:
            self.accumulate_count = 1
            self.fire_index = 0
            weapon = self.sd.ref_wp_bar_mp_weapons[self.weapon_pos]
            bullet_num = int(weapon.get_bullet_num() / weapon.get_cost_ratio())
            self.cur_max_accumulate_count = min(bullet_num, self.max_accumulate_count)
            self.sd.ref_cur_max_accumulate_index = self.cur_max_accumulate_count - 1
            self.accumulating = False
            self.firing = False
            self.send_event('E_SHOW_FAIRY_ACCUMULATE_WEAPON_ENHANCED_UI', self.first_shoot_after_switch and self.is_fairy_enhanced)
            self.send_event('E_TEMP_CHANGE_WEAPON_POS', self.weapon_pos)
        self.breakable = False

    def on_begin_loop(self):
        super(AccumulateShoot8028, self).on_begin_loop()
        if self.sd.ref_is_fairy_shape:
            self.last_tag_time = global_data.game_time
            self.send_event('E_PLAY_FAIRY_ACCUMULATE_EFFECT', 0)
            self.end_custom_sound('accumulate')
            self.start_custom_sound('accumulate')
            self.accumulating = True
            self.send_event('E_ADD_BLACK_STATE', {MC_TRANSFORM})
            self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')

    def on_begin_post(self):
        super(AccumulateShoot8028, self).on_begin_post()
        self.accumulating = False
        self.firing = True

    def on_enable_break_post(self):
        self.send_event('E_ADD_WHITE_STATE', self.BREAK_POST_STATES, self.sid)
        self.breakable = True

    def _finish_fairy_firing(self):
        self.send_event('E_SHOW_FAIRY_ACCUMULATE_WEAPON_ENHANCED_UI', False)
        self.send_event('E_ADD_WHITE_STATE', {MC_RELOAD}, self.sid)
        self.send_event('E_CLEAR_BLACK_STATE')

    def update(self, dt):
        super(AccumulateShoot8028, self).update(dt)
        if self.sd.ref_is_fairy_shape:
            if self.accumulating:
                if self.accumulate_count < self.cur_max_accumulate_count:
                    if global_data.game_time - self.last_tag_time >= self.accumulate_interval:
                        self.send_event('E_PLAY_FAIRY_ACCUMULATE_EFFECT', self.accumulate_count)
                        self.end_custom_sound('accumulate')
                        self.start_custom_sound('accumulate')
                        self.accumulate_count += 1
                        self.last_tag_time += self.accumulate_interval
                elif global_data.game_time - self.last_tag_time >= self.auto_fire_time:
                    self.sub_state = self.STATE_POST
                if self.sd.ref_transform_action_recorded:
                    self.send_event('E_ACTION_UP', self.bind_action_id)
            elif self.firing and self.accumulate_count:
                if global_data.game_time - self.last_tag_time >= self.fire_interval:
                    self.last_tag_time += self.fire_interval
                    self.accumulate_count -= 1
                    self.send_event('E_STOP_FAIRY_ACCUMULATE_EFFECT', self.fire_index)
                    self.fire_index += 1
                    if self.accumulate_count == 0:
                        self._finish_fairy_firing()
                    self.ev_g_try_weapon_attack_begin(self.weapon_pos)
                    self.ev_g_try_weapon_attack_end(self.weapon_pos)
                    self.end_custom_sound('fire')
                    self.start_custom_sound('fire')
        if self.breakable and self.ev_g_cur_state() & self.BREAK_POST_STATES:
            self.disable_self()

    def _fire(self):
        if self.sd.ref_is_fairy_shape:
            self.send_event('E_SET_SOCKET_INDEX', self.weapon_pos, 0)
            self.last_tag_time = global_data.game_time
            self.ev_g_try_weapon_attack_begin(self.weapon_pos)
            self.ev_g_try_weapon_attack_end(self.weapon_pos)
            self.accumulate_count -= 1
            self.send_event('E_STOP_FAIRY_ACCUMULATE_EFFECT', self.fire_index)
            self.fire_index += 1
            self.first_shoot_after_switch = False
            self.end_custom_sound('fire')
            self.start_custom_sound('fire')
            self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
            if self.accumulate_count == 0:
                self._finish_fairy_firing()
        else:
            self.ev_g_try_weapon_attack_begin(self.weapon_pos)
            self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def exit(self, enter_states):
        super(AccumulateShoot8028, self).exit(enter_states)
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        if self.sd.ref_is_fairy_shape:
            self.send_event('E_RECOVER_WEAPON_POS_CHANGE')
        for i in range(self.cur_max_accumulate_count):
            self.send_event('E_STOP_FAIRY_ACCUMULATE_EFFECT', i)

        self.send_event('E_SHOW_FAIRY_ACCUMULATE_WEAPON_ENHANCED_UI', False)
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')

    def refresh_action_param(self, action_param, custom_param):
        super(AccumulateShoot8028, self).refresh_action_param(action_param, custom_param)
        self.send_event('E_SWITCH_ACTION_BIND_SKILL_ID', self.bind_action_id, self.skill_id)
        self.sd.ref_accumulate_pre_anim_duration = self.pre_anim_duration
        self.sd.ref_accumulate_interval = self.accumulate_interval
        self.first_shoot_after_switch = self.sd.ref_is_fairy_shape
        if not self.sd.ref_is_fairy_shape and self.is_rabbit_enhanced:
            self.weapon_pos = self.enhanced_weapon_pos

    def use_dash_weapon_pos(self, flag):
        if self.dashing ^ flag:
            if flag:
                self.weapon_pos = self.enhanced_special_weapon_pos if self.is_rabbit_enhanced else self.special_weapon_pos
            else:
                self.weapon_pos = self.enhanced_weapon_pos if self.is_rabbit_enhanced else self.custom_param['weapon_pos']
            self.dashing = flag


class Dash8028(StateBase):
    BIND_EVENT = {'E_END_DASH_PRE_ACTION': 'on_end_dash_pre_action',
       'E_ENERGY_EXHAUSTED': 'on_energy_exhausted'
       }
    STATE_PRE = 0
    STATE_LOOP = 1
    STATE_POST = 2

    def read_data_from_custom_param(self):
        self.dash_skill_id = self.custom_param.get('dash_skill_id', 802851)
        self.skill_id = self.custom_param.get('skill_id', 802852)
        self._dash_dis = 0
        self._old_pos = None
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_POST, 0, self.on_begin_post)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8028, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.btn_down = False
        self.playing_move_effect = False
        self.playing_screen_effect = False
        self.max_duration = 1.0

    def action_btn_down(self):
        if not self.sd.ref_is_fairy_shape and self.btn_down:
            return
        self.btn_down = True
        if self.is_active:
            if self.sub_state == self.STATE_LOOP:
                self.sub_state = self.STATE_POST
            return
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_can_cast_skill(self.dash_skill_id):
            return False
        self.active_self()
        return True

    def action_btn_up(self):
        self.btn_down = False

    def enter(self, leave_states):
        super(Dash8028, self).enter(leave_states)
        self.sub_state = self.STATE_PRE
        cost_rate_per_second = self.ev_g_energy_cost(self.dash_skill_id)
        self.max_duration = 1.0 / cost_rate_per_second + 0.1
        self.send_event('E_DO_SKILL', self.dash_skill_id)
        self.send_event('E_SET_SKILL_TICK_INTERVAL', self.dash_skill_id, 0)
        self.send_event('E_SET_DASH_UI_VISIBLE', True)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        self.send_event('E_REPLACE_STATE_PARAM', MC_STAND, MC_OTHER_STAND, include_camera_param=True)
        self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, MC_OTHER_MOVE, include_camera_param=True)
        self.send_event('E_SWITCH_ACTION', 'action5', MC_DASH_JUMP_1)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_DASH_JUMP_2)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_FULL_FORCE_SHOOT, False)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_FULL_FORCE_SHOOT, False)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_FULL_FORCE_SHOOT, False)
        self.send_event('E_TEMP_CHANGE_WEAPON_POS', PART_WEAPON_POS_MAIN2)
        self.send_event('E_USE_DASH_WEAPON_POS', True)
        self.send_event('E_PLAY_RABBIT_DASH_STATE_EFFECT', True)
        self.playing_move_effect = False
        self.playing_screen_effect = False
        self._start_cal_dash_dist()

    def on_begin_pre(self):
        self.send_event('E_ACTIVE_STATE', MC_DASH_1)

    def on_begin_post(self):
        self.send_event('E_ACTIVE_STATE', MC_DASH_2)
        self.disable_self()

    def update(self, dt):
        super(Dash8028, self).update(dt)
        none_up_body_anim = not self.sd.ref_up_body_anim
        in_correspond_states = False
        cur_state = self.ev_g_cur_state()
        if cur_state:
            in_correspond_states = bool(self.ev_g_cur_state() & {MC_MOVE, MC_DASH_JUMP_1, MC_JUMP_2, MC_SUPER_JUMP})
        need_play_move_effect = none_up_body_anim and in_correspond_states
        if self.playing_move_effect ^ need_play_move_effect:
            self.send_event('E_PLAY_RABBIT_DASH_MOVE_EFFECT', need_play_move_effect)
            self.playing_move_effect = need_play_move_effect
        if self.playing_screen_effect ^ in_correspond_states:
            self.send_event('E_PLAY_RABBIT_DASH_SCREEN_EFFECT', in_correspond_states)
            self.playing_screen_effect = in_correspond_states
        if self.elapsed_time > self.max_duration:
            self.on_begin_post()

    def exit(self, enter_states):
        super(Dash8028, self).exit(enter_states)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_END_SKILL', self.dash_skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.dash_skill_id)
        self.send_event('E_SET_SKILL_TICK_INTERVAL', self.dash_skill_id, 0.1)
        self.send_event('E_SET_DASH_UI_VISIBLE', False)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        self.send_event('E_REPLACE_STATE_PARAM', MC_STAND, MC_STAND, include_camera_param=True)
        self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, MC_MOVE, include_camera_param=True)
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_JUMP_2)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_SHOOT, False)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_SHOOT, False)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_SHOOT, False)
        self.send_event('E_RECOVER_WEAPON_POS_CHANGE')
        self.send_event('E_USE_DASH_WEAPON_POS', False)
        self.send_event('E_PLAY_RABBIT_DASH_STATE_EFFECT', False)
        if self.playing_move_effect:
            self.send_event('E_PLAY_RABBIT_DASH_MOVE_EFFECT', False)
            self.playing_move_effect = False
        if self.playing_screen_effect:
            self.send_event('E_PLAY_RABBIT_DASH_SCREEN_EFFECT', False)
            self.playing_screen_effect = False
        self._finish_cal_dash_dist()

    def on_end_dash_pre_action(self):
        if self.is_active and self.sub_state == self.STATE_PRE:
            self.sub_state = self.STATE_LOOP

    def on_energy_exhausted(self, skill_id):
        if self.dash_skill_id != skill_id:
            return
        if self.is_active:
            self.sub_state = self.STATE_POST

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8028', MECHA_MEMORY_LEVEL_8, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf'},('pre_anim_rate', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'}})
class DashPreAction8028(StateBase):
    BIND_EVENT = {}

    def read_data_from_custom_param(self):
        self.pre_anim_name = self.custom_param.get('pre_anim_name', 'rabt_dash_start')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.16)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DashPreAction8028, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()

    def enter(self, leave_states):
        super(DashPreAction8028, self).enter(leave_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim_name, LOW_BODY, 1)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def update(self, dt):
        super(DashPreAction8028, self).update(dt)

    def check_transitions(self):
        if self.elapsed_time > self.pre_anim_duration:
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_MOVE, MC_JUMP_2}, self.sid)
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(DashPreAction8028, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_END_DASH_PRE_ACTION')


@editor.state_exporter({('idle_post_anim_duration', 'param'): {'zh_name': '\xe7\xab\x99\xe7\xab\x8b\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf'},('idle_post_anim_rate', 'param'): {'zh_name': '\xe7\xab\x99\xe7\xab\x8b\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('idle_post_break_time', 'param'): {'zh_name': '\xe7\xab\x99\xe7\xab\x8b\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'},('idle_end_move_time', 'param'): {'zh_name': '\xe7\xab\x99\xe7\xab\x8b\xe5\x90\x8e\xe6\x91\x87\xe5\x81\x9c\xe6\xad\xa2\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'},('idle_speed', 'meter'): {'zh_name': '\xe7\xab\x99\xe7\xab\x8b\xe5\x90\x8e\xe6\x91\x87\xe9\x80\x9f\xe5\xba\xa6'},('roll_post_anim_duration', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf'},('roll_post_anim_rate', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('roll_post_break_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x90\x8e\xe6\x91\x87\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'},('roll_post_stop_move_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x90\x8e\xe6\x91\x87\xe5\x81\x9c\xe6\xad\xa2\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'}})
class DashPostAction8028(StateBase):
    BIND_EVENT = {}
    STATE_IDLE_POST = 0
    STATE_ROLL_POST = 1

    def read_data_from_custom_param(self):
        self.idle_post_anim_name = self.custom_param.get('idle_post_anim_name', 'rabt_run_stop')
        self.idle_post_anim_duration = self.custom_param.get('idle_post_anim_duration', 0.96)
        self.idle_post_anim_rate = self.custom_param.get('idle_post_anim_rate', 1.0)
        self.idle_post_break_time = self.custom_param.get('idle_post_break_time', 0.4)
        self.idle_end_move_time = self.custom_param.get('idle_end_move_time', 0.4)
        self.idle_speed = self.custom_param.get('idle_speed', 8) * NEOX_UNIT_SCALE
        self.roll_post_anim_name = self.custom_param.get('roll_post_anim_name', 'rabt_dash_somersault')
        self.roll_post_anim_duration = self.custom_param.get('roll_post_anim_duration', 0.8)
        self.roll_post_anim_rate = self.custom_param.get('roll_post_anim_rate', 1.0)
        self.roll_post_break_time = self.custom_param.get('roll_post_break_time', 0.5)
        self.roll_post_stop_move_time = self.custom_param.get('roll_post_stop_move_time', 0.5)
        self.register_callbacks()

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_IDLE_POST, 0, self.on_begin_idle_post)
        self.register_substate_callback(self.STATE_IDLE_POST, self.idle_post_break_time, self.enable_break)
        self.register_substate_callback(self.STATE_IDLE_POST, self.idle_end_move_time, self.on_end_idle_move)
        self.register_substate_callback(self.STATE_IDLE_POST, self.idle_post_anim_duration, self.on_end_idle_post)
        self.register_substate_callback(self.STATE_ROLL_POST, 0, self.on_begin_roll_post)
        self.register_substate_callback(self.STATE_ROLL_POST, self.roll_post_break_time, self.enable_break)
        self.register_substate_callback(self.STATE_ROLL_POST, self.roll_post_stop_move_time, self.roll_stop_move)
        self.register_substate_callback(self.STATE_ROLL_POST, self.roll_post_anim_duration, self.on_end_roll_post)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DashPostAction8028, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.breakable = False
        self.idle_moving = False
        self.end = False
        self.roll_speed = 0
        self.enable_param_changed_by_buff()

    def enter(self, leave_states):
        super(DashPostAction8028, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.breakable = False
        self.end = False
        if self.roll_speed and self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
            self.sub_state = self.STATE_ROLL_POST
        else:
            self.sub_state = self.STATE_IDLE_POST
            self.idle_moving = False
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False

    def enable_break(self):
        self.breakable = True
        self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_MOVE, MC_JUMP_1, MC_JUMP_2, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_TRANSFORM}, self.sid)

    def on_begin_idle_post(self):
        if self.ev_g_on_ground() and self.sd.ref_cur_speed:
            self.sd.ref_cur_speed = self.idle_speed
            self.idle_moving = True
            self.send_event('E_SET_WALK_DIRECTION', self.ev_g_forward() * self.idle_speed)
        self.end_custom_sound('idle')
        self.start_custom_sound('idle')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.idle_post_anim_rate)
        self.send_event('E_POST_ACTION', self.idle_post_anim_name, LOW_BODY, 1)

    def on_end_idle_move(self):
        if self.ev_g_on_ground() and self.idle_moving:
            self.send_event('E_CLEAR_SPEED')

    def on_end_idle_post(self):
        self.end = True

    def on_begin_roll_post(self):
        self.end_custom_sound('roll')
        self.start_custom_sound('roll')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.roll_post_anim_rate)
        self.send_event('E_POST_ACTION', self.roll_post_anim_name, LOW_BODY, 1)
        move_dir = get_forward_by_rocker_and_camera_without_y(self)
        self.sd.ref_cur_speed = self.roll_speed * NEOX_UNIT_SCALE
        self.send_event('E_SET_WALK_DIRECTION', move_dir * self.sd.ref_cur_speed)

    def roll_stop_move(self):
        if self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')

    def on_end_roll_post(self):
        self.end = True

    def check_transitions(self):
        if self.end:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2
        if self.breakable:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
            else:
                return MC_JUMP_2

    def exit(self, enter_states):
        super(DashPostAction8028, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True


@editor.state_exporter({('switch_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf'},('switch_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('vertical_speed', 'meter'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe4\xbb\x99\xe5\xa5\xb3\xe5\x8d\x87\xe8\xb5\xb7\xe9\x80\x9f\xe5\xba\xa6'}})
class FairySwitch(StateBase):
    BIND_EVENT = {'E_TRY_END_FAIRY_SHAPE': 'action_btn_down',
       'E_ON_FROZEN': 'on_be_controlled',
       'E_IMMOBILIZED': 'on_be_controlled',
       'E_ON_BEAT_BACK': 'on_be_controlled'
       }
    STATE_SWITCH = 0
    BREAK_STATES = {MC_SHOOT, MC_SECOND_WEAPON_ATTACK}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 802858)
        self.switch_anim_name = self.custom_param.get('switch_anim_name', 'rabttogirl_start')
        self.switch_anim_dir_type = self.custom_param.get('switch_anim_dir_type', 7)
        self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 0.6)
        self.switch_anim_rate = self.custom_param.get('switch_anim_rate', 1.0)
        self.vertical_speed = self.custom_param.get('vertical_speed', 20) * NEOX_UNIT_SCALE
        self.register_callbacks()

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_SWITCH, 0.0, self.on_begin_switch)
        self.register_substate_callback(self.STATE_SWITCH, self.switch_anim_duration, self.on_end_switch)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(FairySwitch, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.new_custom_param = self.custom_param
        self.sound_param_delay_refresh = True
        self.switch_to_fairy = False
        self.controlled = False
        self.sd.ref_transform_action_recorded = False

    def action_btn_down(self):
        super(FairySwitch, self).action_btn_down()
        self.sd.ref_transform_action_recorded = True
        if not self.check_can_active():
            return False
        if not self.sd.ref_is_fairy_shape and not self.check_can_cast_skill():
            return False
        if not self.sd.ref_is_fairy_shape and not self.ev_g_check_can_switch_fairy_shape():
            return False
        if not self.is_active:
            self.active_self()
        return True

    def check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()
            self._check_sound_param_refresh()

    def enter(self, leave_states):
        super(FairySwitch, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        self.sub_state = self.STATE_SWITCH
        self.switch_done = False
        self.controlled = False
        self.send_event('E_DISABLE_STATE', MC_RELOAD)

    def on_begin_switch(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.switch_anim_rate)
        self.send_event('E_POST_ACTION', self.switch_anim_name, LOW_BODY, self.switch_anim_dir_type)
        if self.sd.ref_is_fairy_shape:
            self.send_event('E_END_FAIRY_SHAPE_COST_IN_ADVANCE')
            self.send_event('E_RESET_GRAVITY')
            self.send_event('E_PLAY_SWITCH_RABBIT_SHAPE_EFFECT')
            self.switch_to_fairy = False
        else:
            self.send_event('E_DO_SKILL', self.skill_id)
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', self.vertical_speed)
            self.send_event('E_PLAY_SWITCH_FAIRY_SHAPE_EFFECT')
            self.switch_to_fairy = True

    def on_end_switch(self):
        if self.switch_to_fairy:
            self.send_event('E_ACTIVE_STATE', MC_OTHER_SHAPE)
            self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_DEFAULT_ENABLED', False)
            self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_HOVER}, self.sid)
        else:
            self.send_event('E_END_SKILL', self.skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
            self.send_event('E_DISABLE_STATE', MC_OTHER_SHAPE)
            self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_DEFAULT_ENABLED', True)
            self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_MOVE, MC_JUMP_2}, self.sid)
        self.switch_done = True

    def update(self, dt):
        super(FairySwitch, self).update(dt)

    def check_transitions(self):
        if self.switch_done:
            if self.switch_to_fairy != self.sd.ref_is_fairy_shape:
                if self.switch_to_fairy:
                    self.send_event('E_ACTIVE_STATE', MC_OTHER_SHAPE)
                else:
                    self.send_event('E_DISABLE_STATE', MC_OTHER_SHAPE)
                return
            if self.controlled:
                self.disable_self()
                return
            if self.switch_to_fairy:
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_HOVER
                return MC_STAND
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(FairySwitch, self).exit(enter_states)
        self.check_custom_param_refreshed()
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)

    def refresh_action_param(self, action_param, custom_param):
        if custom_param:
            self.new_custom_param = custom_param
            if not self.is_active:
                self.check_custom_param_refreshed()

    def on_be_controlled(self, flag, *args, **kwargs):
        self.controlled = flag
        if self.is_active and flag:
            self.send_event('E_RESET_GRAVITY')


class FairyShape(StateBase):
    BIND_EVENT = {'G_IS_USING_SECOND_MODEL': 'get_is_rabbit_shape',
       'E_SWITCH_MECHA_MODEL': 'on_switch_mecha_model',
       'G_CHECK_CAN_SWITCH_FAIRY_SHAPE': 'check_can_cast_skill',
       'E_END_FAIRY_SHAPE_COST_IN_ADVANCE': 'end_skill_in_advance',
       'E_FUEL_EXHAUSTED': 'on_fuel_exhausted'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(FairyShape, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.sd.ref_is_fairy_shape = False
        self.doing_skill = False
        self.fuel_exhausted = False
        self.is_rabbit = bdict.get('shape_form', MECHA_8028_FORM_RABBIT) == MECHA_8028_FORM_RABBIT

    def _do_skill(self, flag):
        if self.doing_skill ^ flag:
            event_name = 'E_DO_SKILL' if flag else 'E_END_SKILL'
            self.send_event(event_name, self.skill_id)
            self.doing_skill = flag

    def enter(self, leave_states):
        super(FairyShape, self).enter(leave_states)
        self.sd.ref_is_fairy_shape = True
        self.sd.ref_transform_action_recorded = False
        self.fuel_exhausted = False
        self._do_skill(True)
        self.send_event('E_PLAY_DEFAULT_IDLE_ANIM')
        self.send_event('E_SWITCH_MECHA_MODEL', False)
        self.send_event('E_REFRESH_STATE_PARAM')
        self.send_event('E_SWITCH_ACTION', 'action5', MC_OTHER_JUMP_1)
        self.send_event('E_SWITCH_ACTION', 'action6', MC_OTHER_JUMP_2)
        self.send_event('E_DISABLE_MECHA_JUMP_OPACITY')
        self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8028_7.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8028_7.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', 'gui/ui_res_2/battle/mech_main/icon_mech8028_7.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8028_8.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action5', 'gui/ui_res_2/battle/mech_main/icon_mech8028_6.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8028_5.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action7', 'gui/ui_res_2/battle/mech_main/icon_mech8028_3.png', 'show')
        self.send_event('E_PLAY_FAIRY_STATE_EFFECT', True)

    def update(self, dt):
        super(FairyShape, self).update(dt)
        if self.sd.ref_transform_action_recorded or self.fuel_exhausted:
            self.send_event('E_TRY_END_FAIRY_SHAPE')

    def exit(self, enter_states):
        super(FairyShape, self).exit(enter_states)
        self.sd.ref_is_fairy_shape = False
        self._do_skill(False)
        self.send_event('E_PLAY_DEFAULT_IDLE_ANIM')
        self.send_event('E_SWITCH_MECHA_MODEL', True)
        self.send_event('E_RESET_STATE_PARAM')
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH)
        self.send_event('E_TRY_FAIRY_RISE', False)
        self.send_event('E_TRY_FAIRY_FALL', False)
        self.send_event('E_RESET_MECHA_JUMP_OPACITY')
        self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8028_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8028_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', 'gui/ui_res_2/battle/mech_main/icon_mech8028_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8028_2.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action5', 'gui/ui_res_2/battle/mech_main/mech_jump.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8028_9.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action7', 'gui/ui_res_2/battle/mech_main/icon_mech8028_4.png')
        self.send_event('E_PLAY_FAIRY_STATE_EFFECT', False)

    def get_is_rabbit_shape(self):
        return self.is_rabbit

    def on_switch_mecha_model(self, flag):
        self.is_rabbit = flag

    def end_skill_in_advance(self):
        self._do_skill(False)

    def on_fuel_exhausted(self):
        if self.is_active:
            self.fuel_exhausted = True


class StandWithGuard8028(StandWithGuard):
    BIND_EVENT = StandWithGuard.BIND_EVENT.copy()
    BIND_EVENT.update({'E_PLAY_DEFAULT_IDLE_ANIM': 'play_default_idle_anim'
       })

    def enter(self, leave_states):
        super(StandWithGuard8028, self).enter(leave_states)
        if self.sd.ref_is_fairy_shape:
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_STAND')

    def check_transitions(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            if self.sd.ref_is_fairy_shape:
                return MC_HOVER
            return MC_MOVE

    def play_default_idle_anim(self):
        self.send_event('E_POST_ACTION', self.default_anim, LOW_BODY, 1, loop=True)
        self.end_custom_sound('guard')


@editor.state_exporter({('acc_speed', 'meter'): {'zh_name': '\xe6\x91\x87\xe6\x9d\x86\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('max_speed', 'meter'): {'zh_name': '\xe6\x91\x87\xe6\x9d\x86\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('dec_speed', 'meter'): {'zh_name': '\xe6\x91\x87\xe6\x9d\x86\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'},('max_vertical_speed', 'meter'): {'zh_name': '\xe6\x91\x87\xe6\x9d\x86\xe6\x9c\x80\xe5\xa4\xa7\xe7\xab\x96\xe7\x9b\xb4\xe6\x96\xb9\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6'},('rise_speed', 'meter'): {'zh_name': '\xe5\x8d\x87\xe7\xa9\xba\xe9\x80\x9f\xe5\xba\xa6'},('fall_speed', 'meter'): {'zh_name': '\xe4\xb8\x8b\xe9\x99\x8d\xe9\x80\x9f\xe5\xba\xa6'}})
class FairyHover(StateBase):
    BIND_EVENT = {'E_TRY_FAIRY_RISE': 'try_fairy_rise',
       'E_TRY_FAIRY_FALL': 'try_fairy_fall',
       'E_FAIRY_FIRE_SLOW_DOWN': 'on_fire_slow_down'
       }

    def read_data_from_custom_param(self):
        self.acc_speed = self.custom_param.get('acc_speed', 40) * NEOX_UNIT_SCALE
        self.max_speed = self.custom_param.get('max_speed', 20) * NEOX_UNIT_SCALE
        self.dec_speed = self.custom_param.get('dec_speed', 50) * NEOX_UNIT_SCALE
        self.max_vertical_speed = self.custom_param.get('max_vertical_speed', 8) * NEOX_UNIT_SCALE
        self.rise_skill_id = self.custom_param.get('rise_skill_id', None)
        self.rise_speed = self.custom_param.get('rising_speed', 18) * NEOX_UNIT_SCALE
        self.fall_speed = self.custom_param.get('fall_speed', 18) * NEOX_UNIT_SCALE
        self.max_height = self.custom_param.get('max_height', 2450)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(FairyHover, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.cur_speed_value = 0
        self.last_move_dir = math3d.vector(0, 0, 0)
        self.action_event_registered = False
        self.rising = False
        self.falling = False
        self.doing_rising_skill = False
        self.cur_sound_key = ''

    def enter(self, leave_states):
        super(FairyHover, self).enter(leave_states)
        self.cur_speed_value = 0
        self.last_move_dir = math3d.vector(0, 0, 0)
        self.sd.ref_forbid_zero_anim_dir = False
        self.send_event('E_POST_ACTION', 'girl_move', LOW_BODY, 7, loop=True)
        self.doing_rising_skill = False
        self.send_event('E_ACTION_MOVE')

    def _do_rise_skill(self, flag):
        if self.doing_rising_skill ^ flag:
            event_name = 'E_DO_SKILL' if flag else 'E_END_SKILL'
            self.send_event(event_name, self.rise_skill_id)
            self.doing_rising_skill = flag

    def _play_sound(self, sound_key):
        if self.cur_sound_key == sound_key:
            return
        if self.cur_sound_key:
            self.end_custom_sound(self.cur_sound_key)
        if sound_key:
            self.start_custom_sound(sound_key)
        self.cur_sound_key = sound_key

    def update(self, dt):
        super(FairyHover, self).update(dt)
        rocker_dir = self.sd.ref_rocker_dir
        need_update_speed = True
        dragging_rocker = rocker_dir and not rocker_dir.is_zero
        if dragging_rocker:
            if self.cur_speed_value < self.max_speed:
                self.cur_speed_value += self.acc_speed * dt
                if self.cur_speed_value > self.max_speed:
                    self.cur_speed_value = self.max_speed
        elif self.cur_speed_value:
            self.cur_speed_value -= self.dec_speed * dt
            if self.cur_speed_value < 0:
                self.cur_speed_value = 0
        else:
            need_update_speed = False
        vertical_speed = 0
        if need_update_speed:
            if dragging_rocker:
                rot = self.ev_g_rotation()
                move_dir = rot.rotate_vector(rocker_dir)
                self.last_move_dir = move_dir
            else:
                move_dir = self.last_move_dir
            if move_dir.y > 0 and rocker_dir.z > 0:
                vertical_speed = move_dir.y * self.cur_speed_value
                if vertical_speed > self.max_vertical_speed:
                    vertical_speed = self.max_vertical_speed
                horizontal_speed = sqrt(self.cur_speed_value * self.cur_speed_value - vertical_speed * vertical_speed)
            else:
                vertical_speed = 0
                horizontal_speed = self.cur_speed_value
            move_dir.y = 0
            move_dir.normalize()
            horizontal_speed *= self.ev_g_get_speed_scale()
            self.send_event('E_SET_WALK_DIRECTION', move_dir * horizontal_speed)
            self.sd.ref_cur_speed = horizontal_speed
        elif self.sd.ref_cur_speed:
            self.send_event('E_CLEAR_SPEED')
        vertical_move_anim_name = ''
        if self.rising or self.falling:
            if self.rising:
                vertical_speed += self.rise_speed
                vertical_move_anim_name = 'girl_up'
                self._play_sound('rise')
            else:
                vertical_speed -= self.fall_speed
                vertical_move_anim_name = 'girl_down'
                self._play_sound('fall')
        else:
            self._play_sound('fly')
        if dragging_rocker:
            if self.sd.ref_low_body_anim != 'girl_move':
                self.send_event('E_POST_ACTION', 'girl_move', LOW_BODY, 7, loop=True)
                self._play_sound('fly')
        elif vertical_move_anim_name and self.sd.ref_low_body_anim != vertical_move_anim_name:
            self.send_event('E_POST_ACTION', vertical_move_anim_name, LOW_BODY, 1, loop=True)
        self._do_rise_skill(self.rising)
        if self.ev_g_position().y >= self.max_height and vertical_speed > 0:
            vertical_speed = 0
        self.send_event('E_VERTICAL_SPEED', vertical_speed * self.ev_g_get_speed_scale())

    def check_transitions(self):
        if self.cur_speed_value == 0 and not self.rising and not self.falling:
            return MC_STAND

    def exit(self, enter_states):
        super(FairyHover, self).exit(enter_states)
        self.sd.ref_forbid_zero_anim_dir = True
        self._do_rise_skill(False)
        self._play_sound('')
        if MC_STAND in enter_states:
            self._play_sound('stop')

    def refresh_action_param(self, action_param, custom_param):
        super(FairyHover, self).refresh_action_param(action_param, custom_param)
        self.custom_param = custom_param
        self.read_data_from_custom_param()

    def try_fairy_rise(self, flag):
        self.rising = flag and self.ev_g_can_cast_skill(self.rise_skill_id)
        if flag:
            if self.falling:
                self.falling = False
            if not self.is_active:
                self.active_self()

    def try_fairy_fall(self, flag):
        self.falling = flag
        if flag:
            if self.rising:
                self.rising = False
            if not self.is_active:
                self.active_self()

    def on_fire_slow_down(self, slow_down, *args):
        if slow_down:
            self.max_speed, self.rise_speed, self.fall_speed = args
        else:
            self.max_speed = self.custom_param.get('max_speed', 20) * NEOX_UNIT_SCALE
            self.rise_speed = self.custom_param.get('rising_speed', 18) * NEOX_UNIT_SCALE
            self.fall_speed = self.custom_param.get('fall_speed', 18) * NEOX_UNIT_SCALE


class FairyRise(StateBase):

    def action_btn_down(self):
        self.send_event('E_TRY_FAIRY_RISE', True)

    def action_btn_up(self):
        self.send_event('E_TRY_FAIRY_RISE', False)


class FairyFall(StateBase):

    def action_btn_down(self):
        self.send_event('E_TRY_FAIRY_FALL', True)

    def action_btn_up(self):
        self.send_event('E_TRY_FAIRY_FALL', False)


class Immobilize8028(Immobilize):

    def enter(self, leave_states):
        super(Immobilize, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        if not self.fall:
            self.send_event('E_ACTION_SYNC_ACC', 0)
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)
        elif self.sd.ref_is_fairy_shape:
            self.send_event('E_RESET_GRAVITY')

    def check_transitions(self):
        if not self._immobilized:
            self.disable_self()
            if self.sd.ref_is_fairy_shape:
                return MC_STAND
            else:
                if self.sd.ref_on_ground:
                    return MC_STAND
                return MC_JUMP_2


class OnFrozen8028(OnFrozen):

    def enter(self, leave_states):
        super(OnFrozen, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        if not self.fall:
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_ACTION_SYNC_ACC', 0)
            self.send_event('E_GRAVITY', 0)
        elif self.sd.ref_is_fairy_shape:
            self.send_event('E_RESET_GRAVITY')

    def check_transitions(self):
        if not self._frozen:
            self.disable_self()
            if self.sd.ref_is_fairy_shape:
                return MC_STAND
            else:
                if self.sd.ref_on_ground:
                    return MC_STAND
                return MC_JUMP_2


class BeatBack8028(BeatBack):

    def check_transitions(self):
        if self.sd.ref_is_fairy_shape:
            if self.ev_g_vertical_speed() < 0:
                self.disable_self()
                return MC_STAND


class Run8028(Run8009):

    def begin_run_anim(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        if self.forbid_default_up_body_anim:
            if self.ev_g_is_showing_default_up_body_anim():
                self.send_event('E_POST_ACTION', self.run_anim, UP_BODY, 7, loop=True, ignore_sufix=self.run_ignore_sufix)
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.run_anim, 7)
        self.send_event('E_POST_ACTION', self.run_anim, LOW_BODY, self.run_anim_dir_type, loop=True, ignore_sufix=self.run_ignore_sufix, yaw_list=self.run_anim_yaw_list, keep_phase=True)
        self.enter_state_running_time_stamp = time.time()

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_state_running_time_stamp < self.stop_anim_cost_time:
            self.end_run_stop_anim()
            return
        self.end_custom_sound('brake')
        self.start_custom_sound('brake')
        super(Run8009, self).begin_run_stop_anim()