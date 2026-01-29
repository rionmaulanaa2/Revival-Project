# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8017.py
from __future__ import absolute_import
from random import random
import six
from .StateBase import StateBase
from .ShootLogic import Reload, AccumulateShoot
from .JumpLogic import FallPure
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3, PART_WEAPON_POS_MAIN4, PART_WEAPON_POS_MAIN5
from logic.gcommon.common_const.weapon_const import AUTO_MODE
from .Logic8011 import ActionDrivenWeaponFire
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.character_ctrl_utils import get_forward_by_rocker_and_camera_without_y
from common.utils.timer import CLOCK
from logic.gcommon import editor
from math import fabs
import math3d
import world
import time
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_8
EPSILON = 0.01
CONTROLLED_STATES = {MC_BEAT_BACK, MC_IMMOBILIZE, MC_FROZEN}

def _get_normalize_rocker_dir--- This code section failed: ---

  30       0  LOAD_GLOBAL           0  'fabs'
           3  LOAD_FAST             0  'x'
           6  CALL_FUNCTION_1       1 
           9  LOAD_GLOBAL           1  'EPSILON'
          12  COMPARE_OP            0  '<'
          15  POP_JUMP_IF_FALSE    24  'to 24'
          18  LOAD_CONST            1  ''
          21  JUMP_FORWARD         18  'to 42'
          24  JUMP_FORWARD          2  'to 29'
          27  COMPARE_OP            0  '<'
          30  POP_JUMP_IF_FALSE    39  'to 39'
          33  LOAD_CONST            3  -1
          36  JUMP_FORWARD          3  'to 42'
          39  LOAD_CONST            4  1
        42_0  COME_FROM                '36'
        42_1  COME_FROM                '21'
          42  STORE_FAST            0  'x'

  31      45  LOAD_GLOBAL           0  'fabs'
          48  LOAD_FAST             1  'z'
          51  CALL_FUNCTION_1       1 
          54  LOAD_GLOBAL           1  'EPSILON'
          57  COMPARE_OP            0  '<'
          60  POP_JUMP_IF_FALSE    69  'to 69'
          63  LOAD_CONST            1  ''
          66  JUMP_FORWARD         21  'to 90'
          69  LOAD_FAST             1  'z'
          72  LOAD_CONST            2  ''
          75  COMPARE_OP            0  '<'
          78  POP_JUMP_IF_FALSE    87  'to 87'
          81  LOAD_CONST            3  -1
          84  JUMP_FORWARD          3  'to 90'
          87  LOAD_CONST            4  1
        90_0  COME_FROM                '84'
        90_1  COME_FROM                '66'
          90  STORE_FAST            1  'z'

  32      93  LOAD_FAST             0  'x'
          96  LOAD_FAST             1  'z'
          99  BUILD_TUPLE_2         2 
         102  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `COMPARE_OP' instruction at offset 27


@editor.state_exporter({('normal_anim_rate', 'param'): {'zh_name': '\xe5\xb8\xb8\xe8\xa7\x84\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('change_dir_hold_time', 'param'): {'zh_name': '\xe5\x88\x87\xe6\x8d\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x96\xb9\xe5\x90\x91\xe4\xbf\x9d\xe6\x8c\x81\xe6\x97\xb6\xe9\x97\xb4'},('change_dir_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x8d\xe5\x90\x91\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('switch_dir_anim_duration', 'param'): {'zh_name': '\xe5\x88\x87\xe6\x8d\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('switch_dir_anim_rate', 'param'): {'zh_name': '\xe5\x88\x87\xe6\x8d\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('slow_down_speed', 'meter'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'}})
class WeaponFire8017(StateBase):
    BIND_EVENT = {'G_CONTINUE_FIRE': 'get_continual_fire',
       'TRY_STOP_WEAPON_ATTACK': 'try_stop_weapon_attack',
       'E_FIRE': 'on_fire',
       'E_REFRESH_ENHANCE_WEAPON_AFTER_RELOAD': 'refresh_enhance_weapon_after_reload',
       'E_ENTER_STATE': 'on_enter_state',
       'E_LEAVE_STATE': 'on_leave_state'
       }
    ALL_JUMP_STATES = {
     MC_JUMP_1, MC_JUMP_2, MC_JUMP_3, MC_SUPER_JUMP}

    def read_data_from_custom_param(self):
        self.weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN1)
        self.normal_anim_rate = self.custom_param.get('normal_anim_rate', 1.0)
        self.change_dir_hold_time = self.custom_param.get('change_dir_hold_time', 1.0)
        self.change_dir_anim_rate = self.custom_param.get('change_dir_anim_rate', 1.0)
        self.switch_dir_anim_duration = self.custom_param.get('switch_dir_anim_duration', 0.5)
        self.switch_dir_anim_rate = self.custom_param.get('switch_dir_anim_rate', 1.0)
        self.slow_down_speed = self.custom_param.get('slow_down_speed', 4.0) * NEOX_UNIT_SCALE
        self.enhance_weapon_pos = self.custom_param.get('enhance_weapon_pos', PART_WEAPON_POS_MAIN3)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(WeaponFire8017, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.fire_hold_time = 0.1
        self.left_time = self.fire_hold_time
        self.front_back_anim_name_map = {(-1, 0): 'aim_idle_l',
           (-1, -1): 'aim_b_l',
           (-1, 1): 'aim_f_l',
           (1, 0): 'aim_idle_r',
           (1, -1): 'aim_b_r',
           (1, 1): 'aim_f_r'
           }
        self.left_right_anim_name_map = {(-1, 0): 'aim_l',
           (-1, -1): 'aim_bl',
           (-1, 1): 'aim_fl',
           (1, 0): 'aim_r',
           (1, -1): 'aim_br',
           (1, 1): 'aim_fr'
           }
        self.switch_anim_name_map = {(-1, 0): 'aim_switch_fl2r',
           (-1, -1): 'aim_switch_bl2r',
           (-1, 1): 'aim_switch_fl2r',
           (1, 0): 'aim_switch_fr2l',
           (1, -1): 'aim_switch_br2l',
           (1, 1): 'aim_switch_fr2l'
           }
        self.change_anim_name_map = {-1: 'aim_l2r',
           1: 'aim_r2l'
           }
        self.force_jump_anim_name_map = {-1: {MC_SUPER_JUMP: 'shoot_jump_l_01',
                MC_JUMP_1: 'shoot_jump_l_01',
                MC_JUMP_2: 'shoot_jump_l_02',
                MC_JUMP_3: 'shoot_jump_l_03'
                },
           1: {MC_SUPER_JUMP: 'shoot_jump_r_01',
               MC_JUMP_1: 'shoot_jump_r_01',
               MC_JUMP_2: 'shoot_jump_r_02',
               MC_JUMP_3: 'shoot_jump_r_03'
               }
           }
        self.force_anim_name = None
        self.force_anim_key = None
        self.cur_anim_dir_x = -1
        self.change_dir_passed_time = 0.0
        self.is_switching = False
        self.switch_dir_anim_passed_time = 0.0
        self.last_set_anim_time_stamp = 0.0
        self.fire_index = 0
        self.split_shoot_fire_count = 0
        self.refresh_enhance_weapon_prate = 0.0
        self.force_fire_enhance_weapon_next = False
        self.enable_param_changed_by_buff()
        return

    def on_post_init_complete(self, *args):
        super(WeaponFire8017, self).on_post_init_complete(*args)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        self.fire_hold_time = weapon.get_data_by_key('fHoldTime') if weapon else 0.05

    def refresh_param_changed(self):
        if self.split_shoot_fire_count <= 0:
            self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', False)

    def action_btn_down(self):
        super(WeaponFire8017, self).action_btn_down()
        if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_try_weapon_attack_begin(self.weapon_pos):
            return False
        if not self.is_active:
            self.active_self()
        return True

    def action_btn_up(self):
        super(WeaponFire8017, self).action_btn_up()
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def enter(self, leave_states):
        super(WeaponFire8017, self).enter(leave_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'idle')
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.send_event('E_SLOW_DOWN', True, self.slow_down_speed, 'WeaponFire')
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir is None:
            rocker_dir = math3d.vector(0, 0, 0)
        x, z = _get_normalize_rocker_dir(rocker_dir.x, rocker_dir.z)
        if x == 0:
            x = 1
        self.cur_anim_dir_x = x
        if self.force_anim_name:
            self.force_anim_name = self.force_jump_anim_name_map[self.cur_anim_dir_x][self.force_anim_key]
        self.change_dir_passed_time = 0.0
        self.is_switching = False
        self.switch_dir_anim_passed_time = 0.0
        self.last_set_anim_time_stamp = 0.0
        self.left_time = self.fire_hold_time
        return

    def update(self, dt):
        super(WeaponFire8017, self).update(dt)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir is None:
            rocker_dir = math3d.vector(0, 0, 0)
        x, z = _get_normalize_rocker_dir(rocker_dir.x, rocker_dir.z)
        cur_time_stamp = time.time()
        if x * self.cur_anim_dir_x < 0 and self.force_anim_name is None:
            if not self.is_switching:
                self.change_dir_passed_time += dt
                if self.change_dir_passed_time >= self.change_dir_hold_time:
                    self.change_dir_passed_time = 0.0
                    self.is_switching = True
                    self.send_event('E_ANIM_RATE', UP_BODY, self.switch_dir_anim_rate)
                    self.send_event('E_POST_ACTION', self.switch_anim_name_map[self.cur_anim_dir_x, z], UP_BODY, 1)
                    self.last_set_anim_time_stamp = cur_time_stamp
                    self.cur_anim_dir_x = x
        else:
            self.change_dir_passed_time = 0
        loop, force = True, False
        if self.force_anim_name:
            anim_name, anim_rate, loop, force = (
             self.force_anim_name, self.sd.ref_anim_rate[LOW_BODY], False, True)
        elif self.change_dir_passed_time > 0.0:
            anim_name, anim_rate = self.change_anim_name_map[self.cur_anim_dir_x], self.change_dir_anim_rate
        elif x == 0:
            anim_name, anim_rate = self.front_back_anim_name_map[self.cur_anim_dir_x, z], self.normal_anim_rate
        else:
            anim_name, anim_rate = self.left_right_anim_name_map[self.cur_anim_dir_x, z], self.normal_anim_rate
        if self.is_switching:
            self.switch_dir_anim_passed_time += dt
            if self.switch_dir_anim_passed_time >= self.switch_dir_anim_duration:
                self.switch_dir_anim_passed_time = 0.0
                self.is_switching = False
                self.send_event('E_ANIM_RATE', UP_BODY, anim_rate)
                self.send_event('E_POST_ACTION', anim_name, UP_BODY, 1, loop=loop)
        elif self.sd.ref_up_body_anim != anim_name and (cur_time_stamp - self.last_set_anim_time_stamp > 0.2 or force):
            self.send_event('E_ANIM_RATE', UP_BODY, anim_rate)
            self.send_event('E_POST_ACTION', anim_name, UP_BODY, 1, loop=loop, blend_time=0.2)
            self.last_set_anim_time_stamp = cur_time_stamp
        self.left_time -= dt
        if self.left_time < 0:
            self.disable_self()
        return

    def exit(self, enter_states):
        super(WeaponFire8017, self).exit(enter_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire')
        if enter_states:
            self.ev_g_try_weapon_attack_end(self.weapon_pos)
        if enter_states & CONTROLLED_STATES or MC_RELOAD not in enter_states:
            if MC_DASH in enter_states:
                self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION', 0.2)
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
            self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION')
        if MC_DASH in enter_states:
            self.send_event('E_ENABLE_AUTO_TRIGGER_WEAPON', self.weapon_pos, False)
            self.send_event('E_ENABLE_AUTO_TRIGGER_WEAPON', self.enhance_weapon_pos, False)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        return

    def get_continual_fire(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not self.ev_g_is_main_weapon_enable():
            return (False, self.weapon_pos)
        if weapon and weapon.get_data_by_key('iMode') == AUTO_MODE:
            return (self.continue_fire, self.weapon_pos)
        return (False, self.weapon_pos)

    def try_stop_weapon_attack(self, *args):
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        self.disable_self()

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        if weapon_pos != self.weapon_pos:
            return
        if self.split_shoot_fire_count > 0:
            self.fire_index += 1
            if self.fire_index == self.split_shoot_fire_count - 1:
                self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', True)
            if self.fire_index == self.split_shoot_fire_count:
                self.ev_g_try_weapon_attack_begin(PART_WEAPON_POS_MAIN4)
                self.ev_g_try_weapon_attack_end(PART_WEAPON_POS_MAIN4)
                self.fire_index = 0
                self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', False)
            if self.force_fire_enhance_weapon_next:
                self.force_fire_enhance_weapon_next = False
                self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', False)
            if self.refresh_enhance_weapon_prate and self.fire_index != self.split_shoot_fire_count - 1 and random() < self.refresh_enhance_weapon_prate:
                self.fire_index = self.split_shoot_fire_count - 1
                self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', True)
        elif self.force_fire_enhance_weapon_next:
            self.force_fire_enhance_weapon_next = False
            self.ev_g_try_weapon_attack_begin(PART_WEAPON_POS_MAIN4)
            self.ev_g_try_weapon_attack_end(PART_WEAPON_POS_MAIN4)
            self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', False)
        else:
            self.fire_index = 0
        if not self.is_active:
            if not self.check_can_active():
                self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
                return
            self.active_self()
        self.left_time = self.fire_hold_time + f_cdtime

    def on_enter_state(self, enter_state):
        if enter_state in self.ALL_JUMP_STATES:
            self.force_anim_name = self.force_jump_anim_name_map[self.cur_anim_dir_x][enter_state]
            self.force_anim_key = enter_state
            self.is_switching = False

    def on_leave_state(self, leave_state, new_state=None):
        cur_state = self.ev_g_cur_state()
        if cur_state is None:
            cur_state = set()
        and_state = self.ALL_JUMP_STATES & cur_state
        if len(and_state) == 1 and leave_state in self.ALL_JUMP_STATES and new_state not in self.ALL_JUMP_STATES:
            self.force_anim_name = None
            self.force_anim_key = None
        return

    def refresh_enhance_weapon_after_reload(self):
        if self.split_shoot_fire_count > 0:
            self.fire_index = self.split_shoot_fire_count - 1
        else:
            self.force_fire_enhance_weapon_next = True
        self.send_event('E_SHOW_SPLIT_MAIN_WEAPON', True)


class Reload8017(Reload):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8017, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.enable_param_changed_by_buff()
        self.is_cover_shoot = False
        self.refresh_enhance_weapon = False

    def enter(self, leave_states):
        super(Reload8017, self).enter(leave_states)
        self.send_event('E_ANIM_RATE', UP_BODY, self.timer_rate)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'reload_f')
        self.is_cover_shoot = MC_SHOOT in leave_states

    def exit(self, enter_states):
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        super(Reload8017, self).exit(enter_states)
        if self.is_cover_shoot:
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.refresh_enhance_weapon:
            self.send_event('E_REFRESH_ENHANCE_WEAPON_AFTER_RELOAD')
        return


class EnhanceWeaponFire(ActionDrivenWeaponFire):
    BIND_EVENT = ActionDrivenWeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_TRY_ENHANCE_WEAPON_FIRE': 'try_enhance_weapon_fire'
       })

    def read_data_from_custom_param(self):
        super(EnhanceWeaponFire, self).read_data_from_custom_param()
        self.skill_id = self.custom_param.get('skill_id', None)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(EnhanceWeaponFire, self).init_from_dict(unit_obj, bdict, sid, info)

    def action_btn_down(self):
        super(ActionDrivenWeaponFire, self).action_btn_down()
        self.continue_fire = True
        if not self.check_can_cast_skill():
            return False
        if not self.check_can_active():
            self.send_event('E_ACTIVATE_AUTO_TRIGGER_WEAPON', self.weapon_pos)
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        self.try_next_action()
        return True

    def action_btn_up(self):
        super(ActionDrivenWeaponFire, self).action_btn_up()
        self.send_event('E_ENABLE_AUTO_TRIGGER_WEAPON', self.weapon_pos, True)
        self.continue_fire = False

    def trigger_fire(self):
        super(EnhanceWeaponFire, self).trigger_fire()
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)

    def interrupt(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_SECOND_WEAPON_ATTACK}, self.sid)

    def exit(self, enter_states):
        super(ActionDrivenWeaponFire, self).exit(enter_states)
        self.send_event('E_CLEAR_BLACK_STATE')
        if MC_DASH in enter_states:
            self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION', 0.2)
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION')
        if self.is_moving:
            self.is_moving = False
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_CLEAR_SPEED')
            self.is_moving = False
        self.cur_state_exit_time = time.time()
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.send_event('E_SLOW_DOWN', False)
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.need_refresh_add_factor:
            self.need_refresh_add_factor = False
            self._refresh_add_factor()
        self.send_event('E_SLOW_DOWN', False)

    def get_continual_fire(self):
        return (
         False, self.weapon_pos)

    def try_enhance_weapon_fire(self, weapon_pos):
        if weapon_pos != self.weapon_pos:
            return
        self.action_btn_down()
        self.action_btn_up()


class AccumulateShoot8017(AccumulateShoot):

    def read_data_from_custom_param(self):
        super(AccumulateShoot8017, self).read_data_from_custom_param()
        self.normal_weapon_pos = self.weapon_pos
        self.enhanced_weapon_pos = self.custom_param.get('enhanced_weapon_pos', PART_WEAPON_POS_MAIN5)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateShoot8017, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.enable_param_changed_by_buff()
        self.enhanced_by_module = False

    def refresh_param_changed(self):
        if self.enhanced_by_module:
            self.weapon_pos = self.enhanced_weapon_pos
            self.send_event('E_ENHANCE_WEAPON', self.enhanced_by_module, self.normal_weapon_pos, self.enhanced_weapon_pos)
        else:
            self.weapon_pos = self.normal_weapon_pos
            self.send_event('E_ENHANCE_WEAPON', self.enhanced_by_module, self.enhanced_weapon_pos, self.normal_weapon_pos)

    def _post_action(self):
        super(AccumulateShoot8017, self)._post_action()
        if self.enhanced_by_module:
            self.send_event('E_SWITCH_ACTION', 'action4', MC_SHOOT_MODE)

    def enter(self, leave_states):
        super(AccumulateShoot8017, self).enter(leave_states)
        self.send_event('E_SUSPEND_RADIAL_WEAPON', False)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.hold_anim)
        global_data.emgr.play_game_voice.emit('second_weapon')

    def exit(self, enter_states):
        super(AccumulateShoot8017, self).exit(enter_states)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        if MC_DASH in enter_states:
            self.send_event('E_ENABLE_AUTO_TRIGGER_WEAPON', self.weapon_pos, False)
        return


class ComboSecondWeapon(ActionDrivenWeaponFire):
    BIND_EVENT = ActionDrivenWeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_TRY_ENHANCE_WEAPON_FIRE': 'try_enhance_weapon_fire',
       'E_ENHANCE_WEAPON': 'on_enhance_weapon'
       })

    def read_data_from_custom_param(self):
        super(ComboSecondWeapon, self).read_data_from_custom_param()
        self.skill_id = self.custom_param.get('skill_id', None)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ComboSecondWeapon, self).init_from_dict(unit_obj, bdict, sid, info)
        self.is_enhanced = False

    def action_btn_down(self):
        super(ActionDrivenWeaponFire, self).action_btn_down()
        self.continue_fire = True
        if not self.check_can_cast_skill():
            return False
        if not self.check_can_active():
            self.send_event('E_ACTIVATE_AUTO_TRIGGER_WEAPON', self.weapon_pos)
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        self.try_next_action()
        return True

    def action_btn_up(self):
        super(ActionDrivenWeaponFire, self).action_btn_up()
        self.send_event('E_ENABLE_AUTO_TRIGGER_WEAPON', self.weapon_pos, True)
        self.continue_fire = False

    def trigger_fire(self):
        super(ComboSecondWeapon, self).trigger_fire()
        self.send_event('E_DO_SKILL', self.skill_id)
        if self.is_enhanced:
            self.send_event('E_FORBID_TRIGGER_SUSPEND')
            self.send_event('E_SWITCH_ACTION', 'action4', MC_SHOOT_MODE)

    def interrupt(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_FULL_FORCE_SHOOT, MC_SECOND_WEAPON_ATTACK}, self.sid)

    def exit(self, enter_states):
        super(ActionDrivenWeaponFire, self).exit(enter_states)
        self.send_event('E_CLEAR_BLACK_STATE')
        if MC_DASH in enter_states:
            self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION', 0.2)
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION')
        if self.is_moving:
            self.is_moving = False
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_CLEAR_SPEED')
            self.is_moving = False
        self.cur_state_exit_time = time.time()
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.send_event('E_SLOW_DOWN', False)
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.need_refresh_add_factor:
            self.need_refresh_add_factor = False
            self._refresh_add_factor()
        self.send_event('E_SLOW_DOWN', False)
        if not self.ev_g_get_action_by_status(MC_SHOOT_MODE) and not self.ev_g_get_action_by_status(MC_SECOND_WEAPON_ATTACK):
            self.send_event('E_SWITCH_ACTION', 'action4', MC_SECOND_WEAPON_ATTACK)

    def get_continual_fire(self):
        return (
         False, self.weapon_pos)

    def try_enhance_weapon_fire(self, weapon_pos):
        if weapon_pos != self.weapon_pos:
            return
        self.action_btn_down()
        self.action_btn_up()

    def on_enhance_weapon(self, is_enhanced, old_weapon_pos, new_weapon_pos):
        if self.weapon_pos == old_weapon_pos:
            self.is_enhanced = is_enhanced
            self.weapon_pos = new_weapon_pos


class SuspendRadialWeapon(StateBase):
    BIND_EVENT = {'E_GRENADE_EXPLODED': 'on_grenade_exploded',
       'E_FORBID_TRIGGER_SUSPEND': 'on_forbid_trigger_suspend'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.weapon_id = self.custom_param.get('weapon_id', 801705)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SuspendRadialWeapon, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.forbidden = False

    def action_btn_down(self):
        if not self.forbidden and self.check_can_active():
            self.active_self()
        return True

    def action_btn_up(self):
        if self.forbidden:
            self.forbidden = False

    def enter(self, leave_states):
        super(SuspendRadialWeapon, self).enter(leave_states)
        self.send_event('E_SUSPEND_RADIAL_WEAPON', True)
        self.send_event('E_SWITCH_ACTION', 'action4', MC_SECOND_WEAPON_ATTACK)
        self.disable_self()

    def on_grenade_exploded(self, item_info):
        weapon_id = item_info.get('item_itype')
        if weapon_id == self.weapon_id and not self.is_active:
            self.send_event('E_SUSPEND_RADIAL_WEAPON', False)
            self.send_event('E_SWITCH_ACTION', 'action4', MC_SECOND_WEAPON_ATTACK)

    def on_forbid_trigger_suspend(self):
        self.forbidden = True


@editor.state_exporter({('acc_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks
                                    },
   ('acc_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('max_dash_duration', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks
                                    },
   ('dash_anim_rate', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('attack_interrupt_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\xaf\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks
                                        },
   ('on_ground_interrupt_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks
                                           },
   ('dec_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks
                                    },
   ('dec_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('dec_interrupt_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks
                                     },
   ('acc_move_speed', 'meter'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('dash_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('jump_speed', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6'},('jump_gravity', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x87\x8d\xe5\x8a\x9b'},('dec_move_speed', 'meter'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'}})
class Dash8017(StateBase):
    BIND_EVENT = {'E_ACTIVATE_AUTO_TRIGGER_WEAPON': 'activate_auto_trigger_weapon',
       'E_ENABLE_AUTO_TRIGGER_WEAPON': 'enable_auto_trigger_weapon'
       }
    STATE_NONE = -1
    STATE_ACC = 0
    STATE_DASH = 1
    STATE_DEC = 2

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.acc_anim = self.custom_param.get('acc_anim', None)
        self.acc_anim_duration = self.custom_param.get('acc_anim_duration', None)
        self.acc_anim_rate = self.custom_param.get('acc_anim_rate', 1.0)
        self.dash_anim = self.custom_param.get('dash_anim', None)
        self.max_dash_duration = self.custom_param.get('max_dash_duration', None)
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1.0)
        self.dec_anim = self.custom_param.get('dec_anim', None)
        self.attack_interrupt_time = self.custom_param.get('attack_interrupt_time', 1.1)
        self.on_ground_interrupt_time = self.custom_param.get('on_ground_interrupt_time', 1.0)
        self.dec_anim_duration = self.custom_param.get('dec_anim_duration', None)
        self.dec_anim_rate = self.custom_param.get('dec_anim_rate', 1.0)
        self.dec_interrupt_time = self.custom_param.get('dec_interrupt_time', 0.6)
        self.acc_move_speed = self.custom_param.get('acc_move_speed', 2.0) * NEOX_UNIT_SCALE
        self.dash_speed = self.custom_param.get('dash_speed', 30.0) * NEOX_UNIT_SCALE
        self.jump_speed = self.custom_param.get('jump_speed', 30.0) * NEOX_UNIT_SCALE
        self.jump_gravity = self.custom_param.get('jump_gravity', 40.0) * NEOX_UNIT_SCALE
        self.dec_move_speed = self.custom_param.get('dec_move_speed', 2.0) * NEOX_UNIT_SCALE
        self.fall_anim_name = self.custom_param.get('fall_anim_name', 'dash_jump02')
        self._register_callbacks()
        return

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_ACC, 0.0, self.begin_acc)
        self.register_substate_callback(self.STATE_ACC, self.acc_anim_duration, self.end_acc)
        self.register_substate_callback(self.STATE_DASH, 0.0, self.begin_dash)
        self.register_substate_callback(self.STATE_DASH, self.attack_interrupt_time, self.enable_attack_interrupt)
        self.register_substate_callback(self.STATE_DASH, self.on_ground_interrupt_time, self.enable_on_ground_interrupt)
        self.register_substate_callback(self.STATE_DASH, self.max_dash_duration, self.end_dash)
        self.register_substate_callback(self.STATE_DEC, 0.0, self.begin_dec)
        self.register_substate_callback(self.STATE_DEC, self.dec_interrupt_time, self.enable_dec_interrupt)
        self.register_substate_callback(self.STATE_DEC, self.dec_anim_duration, self.end_dec)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8017, self).init_from_dict(unit_obj, bdict, sid, info)
        self.speed_up_factor = 0.0
        self.speed_rate = 1.0
        self.read_data_from_custom_param()
        self.dash_direction = math3d.vector(0, 0, 0)
        self._old_pos = math3d.vector(0, 0, 0)
        self.anim_direction = 'f'
        self.attack_interrupt_enabled = False
        self.on_ground_event_registered = False
        self.dash_end = False
        self.action_switched = False
        self.auto_trigger_weapon_pos = None
        self.is_auto_trigger_enable = dict()
        self.enable_param_changed_by_buff()
        return

    def refresh_param_changed(self):
        self.speed_rate = 1.0 + self.speed_up_factor

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero or self.sd.ref_is_agent:
            self.dash_direction = self.ev_g_forward()
            self.anim_direction = 'f'
        else:
            self.dash_direction = get_forward_by_rocker_and_camera_without_y(self)
            if self.sd.ref_mecha_free_sight_mode_enabled:
                x, _ = _get_normalize_rocker_dir(self.sd.ref_rocker_dir.x, self.sd.ref_rocker_dir.z)
                if x < 0:
                    self.anim_direction = 'l'
                elif x > 0:
                    self.anim_direction = 'r'
                else:
                    self.anim_direction = 'f'
            else:
                self.anim_direction = 'f'
        self.active_self()
        super(Dash8017, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(Dash8017, self).enter(leave_states)
        self.sub_state = self.STATE_ACC
        self.dash_end = False
        self.auto_trigger_weapon_pos = None
        self.attack_interrupt_enabled = False
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.action_switched = False
        if self.ev_g_get_action_by_status(MC_SECOND_WEAPON_ATTACK):
            self.send_event('E_SWITCH_ACTION', 'action4', MC_CAST_SKILL)
            self.action_switched = True
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = False
        return

    def begin_acc(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.acc_anim_rate)
        self.send_event('E_POST_ACTION', self.acc_anim.replace('f', self.anim_direction), LOW_BODY, 1)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_GRAVITY', 0)
        speed = self.acc_move_speed * self.speed_rate
        self.sd.ref_cur_speed = speed
        self.send_event('E_SET_WALK_DIRECTION', self.dash_direction * speed)
        self.send_event('E_SET_FORWARD_IN_FREE_SIGHT_MODE', self.dash_direction)

    def end_acc(self):
        self.sub_state = self.STATE_DASH

    def begin_dash(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        self.send_event('E_POST_ACTION', self.dash_anim.replace('f', self.anim_direction), LOW_BODY, 1)
        speed = self.dash_speed * self.speed_rate
        self.sd.ref_cur_speed = speed
        self.send_event('E_SET_WALK_DIRECTION', self.dash_direction * speed)
        self.send_event('E_GRAVITY', self.jump_gravity)
        self.send_event('E_JUMP', self.jump_speed)
        self._old_pos = self.ev_g_position()

    def enable_attack_interrupt(self):
        if not self.attack_interrupt_enabled:
            self.attack_interrupt_enabled = True
            self.send_event('E_ADD_WHITE_STATE', {MC_FULL_FORCE_SHOOT, MC_CAST_SKILL}, self.sid)
            for key in six.iterkeys(self.is_auto_trigger_enable):
                self.is_auto_trigger_enable[key] = True

            if self.auto_trigger_weapon_pos:
                self.send_event('E_TRY_ENHANCE_WEAPON_FIRE', self.auto_trigger_weapon_pos)
                self.auto_trigger_weapon_pos = None
        return

    def enable_on_ground_interrupt(self):
        if not self.on_ground_event_registered:
            self.regist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            self.on_ground_event_registered = True
        if self.ev_g_on_ground():
            self.on_touch_ground()

    def end_dash(self):
        self.enable_attack_interrupt()
        if self.ev_g_on_ground():
            self.sub_state = self.STATE_DEC
        else:
            self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2}, self.sid)
            self.send_event('E_RESET_GRAVITY')
            self.dash_end = True
        dist = int((self.ev_g_position() - self._old_pos).length)
        if dist > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8017', MECHA_MEMORY_LEVEL_8, dist / NEOX_UNIT_SCALE), False, True)
        self.send_event('E_END_SKILL', self.skill_id)

    def begin_dec(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dec_anim_rate)
        self.send_event('E_POST_ACTION', self.dec_anim.replace('f', self.anim_direction), LOW_BODY, 1)
        speed = self.dec_move_speed * self.speed_rate
        self.sd.ref_cur_speed = speed
        self.send_event('E_SET_WALK_DIRECTION', self.dash_direction * speed)

    def enable_dec_interrupt(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_MOVE, MC_JUMP_1, MC_JUMP_2}, self.sid)

    def end_dec(self):
        self.send_event('E_RESET_GRAVITY')
        self.dash_end = True

    def update(self, dt):
        super(Dash8017, self).update(dt)
        if self.sub_state == self.STATE_DEC:
            speed = self.dec_move_speed * self.speed_rate * (1.0 - self.sub_sid_timer / self.dec_anim_duration)
            self.sd.ref_cur_speed = speed
            self.send_event('E_SET_WALK_DIRECTION', self.dash_direction * speed)

    def check_transitions(self):
        if self.sub_state == self.STATE_DEC:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
        if self.dash_end:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(Dash8017, self).exit(enter_states)
        self.sub_state = self.STATE_NONE
        if self.on_ground_event_registered:
            self.unregist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            self.on_ground_event_registered = False
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_RESET_GRAVITY')
        if MC_JUMP_2 not in enter_states:
            self.send_event('E_CLEAR_SPEED')
        else:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_JUMP_2, self.fall_anim_name)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.auto_trigger_weapon_pos = None
        if self.action_switched and MC_CAST_SKILL not in enter_states:
            self.send_event('E_SWITCH_ACTION', 'action4', MC_SECOND_WEAPON_ATTACK)
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True
        self.send_event('E_END_SKILL', self.skill_id)
        return

    def on_touch_ground(self, *args):
        if self.sub_state == self.STATE_DASH:
            self.end_dash()

    def activate_auto_trigger_weapon(self, weapon_pos):
        if self.is_active and self.auto_trigger_weapon_pos is None and self.is_auto_trigger_enable.get(weapon_pos, True):
            self.auto_trigger_weapon_pos = weapon_pos
        return

    def enable_auto_trigger_weapon(self, weapon_pos, flag):
        self.is_auto_trigger_enable[weapon_pos] = flag


class Fall8017(FallPure):

    def exit(self, enter_states):
        super(Fall8017, self).exit(enter_states)
        self.replace_action_trigger_anim(None)
        return