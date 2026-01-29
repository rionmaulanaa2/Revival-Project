# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8011.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from .StateBase import StateBase
from .MoveLogic import Stand
from .JumpLogic import JumpUp
from .ShootLogic import Reload, AccumulateShoot
from logic.comsys.control_ui.ShotChecker import ShotChecker
from .BoostLogic import Dash, OxRushNew
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from data import camera_state_const
from logic.gcommon.const import NEOX_UNIT_SCALE, PART_WEAPON_POS_MAIN1
from logic.gutils.character_ctrl_utils import apply_horizon_offset_speed_reference_camera, ray_check_on_ground
from logic.gutils.slash_utils import SlashChecker
import logic.gcommon.common_const.weapon_const as w_const
from logic.gcommon.common_const import attr_const
from common.utils.timer import CLOCK
from logic.gcommon import editor
from logic.comsys.battle.BattleUtils import can_fire
import world
import math3d
import collision
from .Logic8009 import Run8009
import random

@editor.state_exporter({('action_count', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\xbe\xaa\xe7\x8e\xaf\xe8\xbd\xae\xe6\xac\xa1'},('action_param_list', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_action_callbacks(),
                                    'structure': lambda self: self._get_action_param_structure(len(self.action_param_list))},
   ('air_action_count', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\x94\xbb\xe5\x87\xbb\xe5\xbe\xaa\xe7\x8e\xaf\xe8\xbd\xae\xe6\xac\xa1'},('air_action_param_list', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\x94\xbb\xe5\x87\xbb\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_action_callbacks(),
                                        'structure': lambda self: self._get_action_param_structure(len(self.air_action_param_list))},
   ('normal_slow_speed', 'meter'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('move_action_slow_speed', 'meter'): {'zh_name': '\xe8\xbf\x88\xe6\xad\xa5\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('weapon_pos', 'param'): {'zh_name': '\xe6\xad\xa6\xe5\x99\xa8\xe4\xbd\x8d\xe7\xbd\xae'}})
class ActionDrivenWeaponFire(StateBase):
    BIND_EVENT = {'G_CONTINUE_FIRE': 'get_continual_fire',
       'TRY_STOP_WEAPON_ATTACK': 'disable_self',
       'E_JUMP': 'on_jump_begin'
       }
    BIND_ATTR_CHANGE = {attr_const.ATTR_SHOOTSPEED_FACTOR: 'on_speed_rate_changed',
       attr_const.ATTR_SHOOTSPEED_FACTOR_POS_1: 'on_speed_rate_changed'
       }
    STATE_NONE = -1
    STATE_INIT = 0
    FORBID_STATE = {
     MC_MOVE, MC_RUN}

    def read_data_from_custom_param(self):
        self.tick_interval = 0.03
        self.action_count = self.custom_param.get('action_count', 0)
        self.action_param_list = self.custom_param.get('action_param_list', [])
        self.air_action_count = self.custom_param.get('air_action_count', 0)
        self.air_action_param_list = self.custom_param.get('air_action_param_list', [])
        self.anim_dir = self.custom_param.get('anim_dir', 1)
        self.normal_slow_speed = self.custom_param.get('normal_slow_speed', 8.5) * NEOX_UNIT_SCALE
        self.move_action_slow_speed = self.custom_param.get('move_action_slow_speed', 3) * NEOX_UNIT_SCALE
        self.common_weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN1)
        self.weapon_pos = self.common_weapon_pos
        self.new_weapon_pos = self.weapon_pos
        self.is_aim_spread = self.custom_param.get('is_aim_spread', False)
        self.spread_recover_off_time = self.custom_param.get('spread_recover_off_time', 0)
        self.enhanced_weapon_pos = self.custom_param.get('enhanced_weapon_pos', PART_WEAPON_POS_MAIN1)
        self.additional_weapon_pos = self.custom_param.get('additional_weapon_pos')
        self._register_action_callbacks()

    def _get_action_param_structure(self, action_count):
        action_param_structure = []
        for i in range(action_count):
            sub_structure = dict()
            sub_structure['anim_name'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d\xe7\xa7\xb0'}
            sub_structure['trigger_fire_time'] = {'zh_name': '\xe8\xa7\xa6\xe5\x8f\x91\xe5\xbc\x80\xe7\x81\xab\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','type': 'float'}
            sub_structure['anim_duration'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf\xef\xbc\x88\xe5\x8f\xaf\xe6\x88\xaa\xe5\x8f\x96\xef\xbc\x89','type': 'float'}
            sub_structure['anim_rate'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','type': 'float'}
            sub_structure['blend_time'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
            sub_structure['combo_time'] = {'zh_name': '\xe5\x8f\xaf\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
            sub_structure['interrupt_time'] = {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
            sub_structure['keep_time'] = {'zh_name': '\xe4\xb8\x8b\xe4\xb8\x80\xe5\x87\xbb\xe5\xad\x98\xe7\x95\x99\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88-1\xe8\xa1\xa8\xe7\xa4\xba\xe6\xb0\xb8\xe4\xb9\x85\xe7\x95\x99\xe5\xad\x98\xef\xbc\x89','type': 'float'}
            sub_structure['begin_move_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
            sub_structure['end_move_time'] = {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4','type': 'float'}
            sub_structure['move_dist'] = {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe8\xb7\x9d\xe7\xa6\xbb(\xe7\xb1\xb3)','type': 'float'}
            sub_structure['use_up_body_bone'] = {'zh_name': '\xe4\xbd\xbf\xe7\x94\xa8\xe4\xb8\x8a\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe4\xbd\x9c\xe4\xb8\xba\xe5\x85\xa8\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c','type': 'bool'}
            action_param_structure.append({'zh_name': '\xe7\xac\xac%d\xe5\x87\xbb' % (i + 1),'type': 'dict','kwargs': {'structure': sub_structure}})

        return action_param_structure

    def _register_action_callbacks(self):
        self.reset_sub_states_callback()
        for state_index in range(self.action_count):
            self._register_action_state_callbacks(self.action_param_list[state_index], state_index)

        for state_index in range(self.air_action_count):
            self._register_action_state_callbacks(self.air_action_param_list[state_index], state_index + self.action_count)

    def _register_action_state_callbacks(self, param, state_index):
        self.all_shoot_anim.add(param['anim_name'])
        self.register_substate_callback(state_index, 0.0, self.play_fire_animation)
        self.register_substate_callback(state_index, param['trigger_fire_time'] / (param['anim_rate'] * self.add_factor), self.trigger_fire)
        self.register_substate_callback(state_index, param['interrupt_time'] / (param['anim_rate'] * self.add_factor), self.interrupt)
        if param['move_dist'] > 0.0:
            self.register_substate_callback(state_index, param['begin_move_time'] / (param['anim_rate'] * self.add_factor), self.begin_move)
            self.register_substate_callback(state_index, param['end_move_time'] / (param['anim_rate'] * self.add_factor), self.end_move)
        self.register_substate_callback(state_index, param['anim_duration'] / (param['anim_rate'] * self.add_factor), self.fire_animation_finished)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ActionDrivenWeaponFire, self).init_from_dict(unit_obj, bdict, sid, info)
        self.additional_weapon_enabled = False
        self.need_refresh_add_factor = False
        self.add_factor = 1.0
        self.all_shoot_anim = set()
        self.read_data_from_custom_param()
        self.continue_fire = False
        self.sub_state = self.STATE_NONE
        self.cur_state_exit_time = 0.0
        self.last_fire_time = 0.0
        self.cur_action_begun = False
        self.is_moving = False
        self.is_enhanced = False
        self.enable_param_changed_by_buff()

    def _check_weapon_pos_refreshed(self):
        if self.weapon_pos != self.new_weapon_pos:
            if self.is_active:
                return
            self.weapon_pos = self.new_weapon_pos

    def refresh_param_changed(self):
        self.new_weapon_pos = self.enhanced_weapon_pos if self.is_enhanced else self.common_weapon_pos
        self._check_weapon_pos_refreshed()

    def _refresh_add_factor(self):
        pos_factor_name = attr_const.ATTR_SHOOTSPEED_FACTOR_POS_1
        pos_factor = self.ev_g_add_attr(pos_factor_name)
        common_factor = self.ev_g_add_attr(attr_const.ATTR_SHOOTSPEED_FACTOR)
        self.add_factor = 1.0 + pos_factor + common_factor
        self._register_action_callbacks()

    def on_init_complete(self):
        super(ActionDrivenWeaponFire, self).on_init_complete()
        self._refresh_add_factor()

    def on_speed_rate_changed(self, attr, *args):
        if attr == attr_const.ATTR_SHOOTSPEED_FACTOR_POS_1 or attr == attr_const.ATTR_SHOOTSPEED_FACTOR:
            if self.is_active:
                self.need_refresh_add_factor = True
            else:
                self._refresh_add_factor()

    def on_jump_begin(self, *args):
        param = self._get_action_param()
        if param['use_up_body_bone'] and self.air_action_count > 0:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)

    def _get_action_param(self):
        if self.sub_state < self.action_count:
            return self.action_param_list[self.sub_state]
        return self.air_action_param_list[self.sub_state - self.action_count]

    def try_next_action(self):
        next_action_state = self.sub_state + 1
        next_action_state %= self.action_count
        if self.sub_state != self.STATE_NONE:
            param = self._get_action_param()
            if self.is_active:
                if self.sub_sid_timer < param['combo_time'] / (param['anim_rate'] * self.add_factor):
                    return
                self.cur_state_exit_time = global_data.game_time
                self.send_event('E_CLEAR_WHITE_STATE', self.sid)
            else:
                cur_time = global_data.game_time
                if cur_time - self.last_fire_time < param['combo_time'] / (param['anim_rate'] * self.add_factor):
                    return
                if 0.0 < param['keep_time'] < cur_time - self.cur_state_exit_time:
                    next_action_state = self.STATE_INIT
                self.active_self()
            on_ground = self.ev_g_on_ground()
            if self.air_action_count > 0:
                if self.sub_state < self.action_count and not on_ground:
                    next_action_state = self.action_count
                elif self.sub_state >= self.action_count and on_ground:
                    next_action_state = self.STATE_INIT
                elif not on_ground:
                    next_action_state %= self.air_action_count
                    next_action_state += self.action_count
            if self.sub_state == next_action_state:
                self.reset_sub_state_timer()
            if self.cur_action_begun:
                self.sub_state = next_action_state
                self.cur_action_begun = False
        else:
            self.cur_action_begun = False
            self.sub_state = self.action_count if self.air_action_count > 0 and not self.ev_g_on_ground() else self.STATE_INIT
            self.active_self()

    def action_btn_down(self):
        super(ActionDrivenWeaponFire, self).action_btn_down()
        self.continue_fire = True
        if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()):
            return False
        if not self.check_can_active():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        self.try_next_action()
        return True

    def action_btn_up(self):
        super(ActionDrivenWeaponFire, self).action_btn_up()
        self.continue_fire = False

    def enter(self, leave_states):
        super(ActionDrivenWeaponFire, self).enter(leave_states)
        param = self._get_action_param()
        param['move_dist'] > 0.0 and self.send_event('E_SLOW_DOWN', True, self.normal_slow_speed)
        if self.is_aim_spread:
            self.send_event('E_SET_SPREAD_RECOVER_OFF_TIME', self.spread_recover_off_time)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)

    def play_fire_animation(self):
        if self.ev_g_check_can_weapon_attack(self.weapon_pos):
            param = self._get_action_param()
            param['move_dist'] > 0 and self.send_event('E_SLOW_DOWN', True, self.normal_slow_speed)
            if param['use_up_body_bone']:
                self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
            else:
                self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
            self.send_event('E_ANIM_RATE', UP_BODY, param['anim_rate'] * self.add_factor)
            self.send_event('E_POST_ACTION', param['anim_name'], UP_BODY, self.anim_dir, blend_time=param['blend_time'], force_trigger_effect=True)
        self.cur_action_begun = True

    def trigger_fire(self):
        self.last_fire_time = global_data.game_time
        self.send_event('E_SET_SOCKET_INDEX', self.weapon_pos, self.sub_state)
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        if self.additional_weapon_enabled and self.additional_weapon_pos:
            self.ev_g_try_weapon_attack_begin(self.additional_weapon_pos)
            self.ev_g_try_weapon_attack_end(self.additional_weapon_pos)

    def interrupt(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_SECOND_WEAPON_ATTACK}, self.sid)

    def begin_move(self):
        self.send_event('E_SLOW_DOWN', True, self.move_action_slow_speed)
        if self.sd.ref_cur_speed:
            return
        param = self._get_action_param()
        velocity = param['move_dist'] * NEOX_UNIT_SCALE / (param['end_move_time'] - param['begin_move_time'])
        self.sd.ref_cur_speed = velocity
        self.send_event('E_SET_WALK_DIRECTION', world.get_active_scene().active_camera.rotation_matrix.forward * velocity)
        self.is_moving = True

    def end_move(self):
        self.send_event('E_SLOW_DOWN', True, self.normal_slow_speed)
        if self.is_moving:
            self.is_moving = False
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_CLEAR_SPEED')

    def fire_animation_finished(self):
        self.disable_self()

    def exit(self, enter_states):
        super(ActionDrivenWeaponFire, self).exit(enter_states)
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
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

    def refresh_action_param(self, action_param, custom_param):
        super(ActionDrivenWeaponFire, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()
            self.sub_state = self.STATE_NONE
            if self.is_active:
                self.disable_self()

    def get_continual_fire(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not self.ev_g_is_main_weapon_enable():
            return (False, self.weapon_pos)
        if weapon and weapon.get_data_by_key('iMode') == w_const.AUTO_MODE:
            return (self.continue_fire, self.weapon_pos)
        return (False, self.weapon_pos)

    def try_weapon_attack_end(self, is_cancel=False):
        self.ev_g_try_weapon_attack_end(self.weapon_pos, is_cancel)

    def on_action_switched(self):
        self.continue_fire = False


@editor.state_exporter({('use_up_body_bone', 'param'): {'zh_name': '\xe4\xbd\xbf\xe7\x94\xa8\xe4\xb8\x8a\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe4\xbd\x9c\xe4\xb8\xba\xe5\x85\xa8\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c'}})
class Reload8011(Reload):

    def read_data_from_custom_param(self):
        super(Reload8011, self).read_data_from_custom_param()
        self.use_up_body_bone = self.custom_param.get('use_up_body_bone', False)
        self.reload_anim = self.custom_param.get('reload_anim', 'j_reload')
        self.common_weapon_pos = self.weapon_pos
        self.new_weapon_pos = self.weapon_pos
        self.enhanced_weapon_pos = self.custom_param.get('enhanced_weapon_pos', PART_WEAPON_POS_MAIN1)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8011, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.is_enhanced = False
        self.enable_param_changed_by_buff()

    def _check_weapon_pos_refreshed(self):
        if self.weapon_pos != self.new_weapon_pos:
            if self.is_active:
                return
            self.weapon_pos = self.new_weapon_pos

    def refresh_param_changed(self):
        self.new_weapon_pos = self.enhanced_weapon_pos if self.is_enhanced else self.common_weapon_pos
        self._check_weapon_pos_refreshed()

    def enter(self, leave_states):
        super(Reload8011, self).enter(leave_states)
        self.use_up_body_bone and self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_POST_ACTION', self.reload_anim, UP_BODY, 1)

    def exit(self, enter_states):
        super(Reload8011, self).exit(enter_states)
        self._check_weapon_pos_refreshed()

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        self.reloaded = True
        continue_fire, fire_weapon_pos = self.ev_g_continue_fire()
        if continue_fire and fire_weapon_pos == weapon_pos:
            self.continue_fire = True


class AccumulateShoot8011(AccumulateShoot):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateShoot8011, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.new_custom_param = self.custom_param
        self.enhance_module_installed = False
        self.enhanced = False
        self.enable_param_changed_by_buff()

    def refresh_param_changed(self):
        if not self.is_active:
            self._check_weapon_enhance_refreshed()

    def _check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()

    def _check_weapon_enhance_refreshed(self):
        self.enhanced = self.enhance_module_installed
        key = 'enhanced_weapon_pos' if self.enhanced else 'weapon_pos'
        self.weapon_pos = self.custom_param[key]

    def enter(self, leave_states):
        super(AccumulateShoot8011, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, 'idle', blend_dir=1)

    def exit(self, enter_states):
        super(AccumulateShoot8011, self).exit(enter_states)
        self._check_custom_param_refreshed()
        self._check_weapon_enhance_refreshed()
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        return

    def refresh_action_param(self, action_param, custom_param):
        super(AccumulateShoot, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.new_custom_param = custom_param
            if not self.is_active:
                self._check_custom_param_refreshed()
                self._check_weapon_enhance_refreshed()


@editor.state_exporter({('guard_anim_duration', 'param'): {'zh_name': '\xe8\xad\xa6\xe8\xa7\x89\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6','post_setter': lambda self: self._register_callbacks()
                                      },
   ('switch_guard_interval', 'param'): {'zh_name': '\xe5\x88\x87\xe6\x8d\xa2\xe8\xad\xa6\xe8\xa7\x89\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x97\xb4\xe9\x9a\x94','post_setter': lambda self: self._register_callbacks()
                                        }
   })
class StandWithGuard(Stand):
    STATE_DEFAULT = -1
    STATE_GUARD = 0

    def read_data_from_custom_param(self):
        super(StandWithGuard, self).read_data_from_custom_param()
        self.default_anim = self.custom_param.get('default_anim', None)
        self.switch_guard_interval = self.custom_param.get('switch_guard_interval', 1.0)
        self.guard_anim = self.custom_param.get('guard_anim', None)
        self.guard_anim_duration = self.custom_param.get('guard_anim_duration', 1.0)
        self.is_guard_anim_loop = self.custom_param.get('guard_anim_loop', True)
        self.guard_sound_key = 'guard'
        self.reset_sub_states_callback()
        self.max_guard_anim_index = 0
        self._register_callbacks()
        return

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        if self.guard_anim:
            self.register_substate_callback(self.STATE_DEFAULT, self.switch_guard_interval, self.switch_to_guard)
            if type(self.guard_anim) is str:
                self.guard_anim = (
                 self.guard_anim,)
                self.guard_anim_duration = (self.guard_anim_duration,)
                self.guard_sound_key = ('guard', )
            else:
                self.guard_sound_key = [ 'guard_%d' % i for i in range(1, len(self.guard_anim) + 1) ]
            self.max_guard_anim_index = len(self.guard_anim) - 1
            for index, anim in enumerate(self.guard_anim):
                self.register_substate_callback(self.STATE_GUARD + index, self.guard_anim_duration[index], self.switch_to_default)

    def enter(self, leave_states):
        super(StandWithGuard, self).enter(leave_states)
        self.switch_to_default()

    def switch_to_guard(self):
        if self.sd.ref_up_body_anim:
            self.reset_sub_state_timer()
            return
        guard_anim_index = random.randint(0, self.max_guard_anim_index) if self.max_guard_anim_index > 0 else 0
        self.sub_state = guard_anim_index
        self.send_event('E_POST_ACTION', self.guard_anim[guard_anim_index], LOW_BODY, 1, loop=self.is_guard_anim_loop)
        self.start_custom_sound(self.guard_sound_key[guard_anim_index])

    def switch_to_default(self):
        self.send_event('E_POST_ACTION', self.default_anim, LOW_BODY, 1, loop=True)
        self.end_custom_sound(self.guard_sound_key[self.sub_state])
        self.sub_state = self.STATE_DEFAULT

    def update(self, dt):
        super(StandWithGuard, self).update(dt)
        if self.sd.ref_up_body_anim:
            if self.sub_state == self.STATE_DEFAULT:
                self.reset_sub_state_timer()
            else:
                self.switch_to_default()

    def exit(self, enter_states):
        super(StandWithGuard, self).exit(enter_states)
        self.end_custom_sound(self.guard_sound_key[self.sub_state])

    def refresh_action_param(self, action_param, custom_param):
        super(Stand, self).refresh_action_param(action_param, custom_param)
        self.custom_param = custom_param
        self.read_data_from_custom_param()
        if not self.is_active:
            return
        if self.sub_state == self.STATE_DEFAULT:
            self.reset_sub_state_timer()
        self.switch_to_default()


def __editor_risingdragon_setter(self, v):
    self.hit_range = v
    self._reset_hit_range()


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                },
   ('begin_move_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe4\xbd\x8d\xe7\xa7\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                  },
   ('end_move_time', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbd\x8d\xe7\xa7\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                },
   ('move_dist', 'meter'): {'zh_name': '\xe4\xbd\x8d\xe7\xa7\xbb\xe8\xb7\x9d\xe7\xa6\xbb(\xe7\xb1\xb3)'},('begin_jump_time', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks()
                                  },
   ('hit_range', 'param'): {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe5\x88\xa4\xe5\xae\x9a\xe8\x8c\x83\xe5\x9b\xb4','param_type': 'list','setter': lambda self, v: __editor_risingdragon_setter(self, v),
                            'structure': [{'zh_name': '\xe5\x88\xa4\xe5\xae\x9a\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe5\x88\xa4\xe5\xae\x9a\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe5\x88\xa4\xe5\xae\x9a\xe9\x95\xbf\xe5\xba\xa6(\xe7\xba\xb5\xe6\xb7\xb1)','type': 'float'}]},
   ('begin_damage_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks(),
                                    'param_type': 'float'},
   ('end_damage_time', 'param'): {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self._register_callbacks(),
                                  'param_type': 'float'},
   ('activate_duration', 'param'): {'zh_name': '\xe5\x8d\x87\xe9\xbe\x99\xe6\x8b\xb3\xe6\xbf\x80\xe6\xb4\xbb\xe6\x97\xb6\xe9\x97\xb4'}})
class RisingDragon(JumpUp):
    BIND_EVENT = JumpUp.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_SECTOR_HIT_TARGET': 'activate_rising_dragon'
       })
    STATE_NONE = -1
    STATE_BEGIN = 0

    def read_data_from_custom_param(self):
        super(RisingDragon, self).read_data_from_custom_param()
        self.pre_anim = self.custom_param.get('pre_anim', None)
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.73)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.jump_anim = self.custom_param.get('jump_anim', 'q_jump_02')
        self.begin_move_time = self.custom_param.get('begin_move_time', 0.3)
        self.end_move_time = self.custom_param.get('end_move_time', 0.65)
        self.move_dist = self.custom_param.get('move_dist', 5) * NEOX_UNIT_SCALE
        self.begin_jump_time = self.custom_param.get('begin_jump_time', 0.65)
        self.begin_damage_time = self.custom_param.get('begin_damage_time', 0)
        self.end_damage_time = self.custom_param.get('0.3')
        self.hit_skill_id = self.custom_param.get('hit_skill_id', None)
        self.hit_enabled = self.custom_param.get('hit_enabled', False)
        self.hit_range = self.custom_param.get('hit_range', [8, 5, 4])
        self.activate_duration = self.custom_param.get('activate_duration', 2.0)
        self.hit_bone_name = self.custom_param.get('hit_bone_name', ('shou_bone_08',
                                                                     'shou_bone_09',
                                                                     'biped r calf'))
        self._register_callbacks()
        return

    def _reset_hit_range(self):
        hit_width = self.hit_range[0] * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * NEOX_UNIT_SCALE
        self.slash_checker.refresh_hit_range(hit_width, hit_height, hit_depth)

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        if self.pre_anim:
            self.register_substate_callback(self.STATE_BEGIN, 0.0, self.perform_pre_anim)
            self.register_substate_callback(self.STATE_BEGIN, self.pre_anim_duration / self.pre_anim_rate, self.perform_jump_anim)
            self.register_substate_callback(self.STATE_BEGIN, self.begin_move_time, self.begin_move)
            self.register_substate_callback(self.STATE_BEGIN, self.end_move_time, self.end_move)
            self.register_substate_callback(self.STATE_BEGIN, self.begin_jump_time, self.perform_jump)
        else:
            self.register_substate_callback(self.STATE_BEGIN, 0.0, self.perform_jump)
        if self.hit_enabled:
            self.register_substate_callback(self.STATE_BEGIN, self.begin_damage_time, self.begin_damage)
            self.register_substate_callback(self.STATE_BEGIN, self.end_damage_time, self.end_damage)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        self.is_attacking = False
        self.is_damaging = False
        super(RisingDragon, self).init_from_dict(unit_obj, bdict, sid, state_info)
        hit_width = self.hit_range[0] * NEOX_UNIT_SCALE
        hit_height = self.hit_range[1] * NEOX_UNIT_SCALE
        hit_depth = self.hit_range[2] * NEOX_UNIT_SCALE
        self.slash_checker = SlashChecker(self, self.hit_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone_name)
        self.new_custom_param = self.custom_param
        self.activate_timer = None
        return

    def destroy(self):
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        self._release_activate_timer()
        super(RisingDragon, self).destroy()
        return

    def enter(self, leave_states):
        super(JumpUp, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.STATE_BEGIN
        if self.pre_anim:
            self.send_event('E_IGNORE_RELOAD_ANIM', True)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
            cur_state = self.ev_g_cur_state()
            MC_SHOOT in cur_state and self.send_event('E_DISABLE_STATE', MC_SHOOT)
            MC_SECOND_WEAPON_ATTACK in cur_state and self.send_event('E_DISABLE_STATE', MC_SECOND_WEAPON_ATTACK)
            self.send_event('E_ADD_BLACK_STATE', {MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_JUMP_3})
        if self.hit_enabled:
            self.is_attacking = True
            self.slash_checker.begin_check(False)
            self.send_event('E_DO_SKILL', self.hit_skill_id)

    def perform_pre_anim(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def perform_jump_anim(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.time_scale)
        self.send_event('E_POST_ACTION', self.jump_anim, LOW_BODY, 1)
        self.send_event('E_CLEAR_BLACK_STATE')

    def begin_move(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            camera = world.get_active_scene().active_camera
            cam_matrix = camera.rotation_matrix
            rot = math3d.matrix_to_rotation(cam_matrix)
            forward = rot.rotate_vector(rocker_dir)
            forward.y = 0
            forward.normalize()
        else:
            forward = self.ev_g_forward()
        speed = self.move_dist / (self.end_move_time - self.begin_move_time)
        self.sd.ref_cur_speed = speed
        self.send_event('E_SET_WALK_DIRECTION', forward * speed)

    def end_move(self):
        self.send_event('E_CLEAR_SPEED')

    def perform_jump(self):
        self.reinforced_jump_time = 0
        self.reinforced_val = self.custom_param.get('reinforced_val', 15) * NEOX_UNIT_SCALE
        self.reinforced_val *= self.reinforced_jump_factor
        self.apply_refinforce_val = self.reinforced_val
        self.can_reinforce = True
        if self.modify_h_speed:
            walk_direction = self.ev_g_char_walk_direction()
            if not walk_direction:
                walk_direction = math3d.vector(0, 0, 0)
            self.send_event('E_SET_WALK_DIRECTION', walk_direction * self.h_speed_ratio)
            self.modify_h_speed = False
        self.send_event('E_JET_CAMERA_SHAKE')
        self.send_event('E_GRAVITY', self.gravity)
        jump_speed = self.jump_speed + self.apply_refinforce_val if self.enable_reinforced_jump else self.jump_speed
        self.send_event('E_JUMP', jump_speed)
        self.last_vertical_speed = jump_speed

    def begin_damage(self):
        self.is_damaging = True
        self.slash_checker.set_damage_settlement_on(True)

    def end_damage(self):
        self.is_damaging = False
        self.slash_checker.set_damage_settlement_on(False)

    def update(self, dt):
        super(JumpUp, self).update(dt)
        apply_horizon_offset_speed_reference_camera(self, dt, self.h_offset_speed, self.h_offset_acc * self.h_offset_acc_percent, None, self.sd.ref_mecha_free_sight_mode_enabled)
        self.apply_reinforce(dt)
        return

    def _check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()
            if self.is_attacking and not self.hit_enabled:
                self.is_attacking = False

    def exit(self, enter_states):
        super(RisingDragon, self).exit(enter_states)
        if self.pre_anim:
            self.send_event('E_CLEAR_BLACK_STATE')
            self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self._check_custom_param_refreshed()
        self.sub_state = self.STATE_NONE
        self.is_attacking = False
        self.slash_checker.end_check()
        self.is_damaging and self.end_damage()
        if self.activate_timer:
            self._release_activate_timer()
            self._deactivate_rising_dragon()

    def refresh_action_param(self, action_param, custom_param):
        super(JumpUp, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.new_custom_param = custom_param
            if not self.is_active:
                self._check_custom_param_refreshed()

    def _release_activate_timer(self):
        if self.activate_timer:
            global_data.game_mgr.unregister_logic_timer(self.activate_timer)
            self.activate_timer = None
        return

    def _deactivate_rising_dragon(self):
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_SET_ACTION_ICON', 'action5', 'gui/ui_res_2/battle/mech_main/mech_jump.png', 'show')
        self.activate_timer = None
        return

    def activate_rising_dragon(self):
        if self.activate_duration > 0.0:
            if not self.activate_timer:
                self.send_event('E_SWITCH_ACTION', 'action5', MC_DASH_JUMP_1)
                self.send_event('E_SET_ACTION_ICON', 'action5', 'gui/ui_res_2/battle/mech_main/icon_mech8011_5.png', 'show')
            self._release_activate_timer()
            self.activate_timer = global_data.game_mgr.register_logic_timer(self._deactivate_rising_dragon, interval=self.activate_duration, times=1, mode=CLOCK)


class DragonSidestep(Dash):

    def read_data_from_custom_param(self):
        self.dash_speed_enhance = self.custom_param.get('dash_speed_enhance', 0) * NEOX_UNIT_SCALE
        super(DragonSidestep, self).read_data_from_custom_param()
        self.refresh_param_changed()

    def exit(self, enter_states):
        super(DragonSidestep, self).exit(enter_states)
        if MC_DRAGON_SHAPE in self.ev_g_cur_state():
            self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH)
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8011_4.png', 'show')

    def refresh_param_changed--- This code section failed: ---

 729       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'spd_dis_enhance'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    57  'to 57'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'spd_dis_enhance'
          18  POP_JUMP_IF_FALSE    57  'to 57'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  'dash_speed_enhance'
        27_0  COME_FROM                '18'
        27_1  COME_FROM                '9'
          27  POP_JUMP_IF_FALSE    57  'to 57'

 730      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             2  'dash_speed_enhance'
          36  LOAD_FAST             0  'self'
          39  STORE_ATTR            3  'dash_speed'

 731      42  LOAD_FAST             0  'self'
          45  LOAD_ATTR             2  'dash_speed_enhance'
          48  LOAD_FAST             0  'self'
          51  STORE_ATTR            4  '_init_dash_speed'
          54  JUMP_FORWARD         24  'to 81'

 733      57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             5  '_dash_speed'
          63  LOAD_FAST             0  'self'
          66  STORE_ATTR            3  'dash_speed'

 734      69  LOAD_FAST             0  'self'
          72  LOAD_ATTR             5  '_dash_speed'
          75  LOAD_FAST             0  'self'
          78  STORE_ATTR            4  '_init_dash_speed'
        81_0  COME_FROM                '54'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def __editor_dragonrush_postsetter(self):
    self.acc_speed = self.max_rush_speed / (self.pre_anim_duration - self.start_acc_time)
    self.brake_speed = self.max_rush_speed / self.end_brake_time
    self._register_sub_state_callbacks()


@editor.state_exporter({('max_rush_speed', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                 },
   ('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                },
   ('start_acc_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_dragonrush_postsetter(self),
                                 'explain': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe5\x8a\xa0\xe9\x80\x9f\xe5\x88\xb0\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},
   ('max_rush_duration', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                    },
   ('hit_anim_duration', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                    },
   ('hit_anim_rate', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                },
   ('break_hit_time', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: __editor_dragonrush_postsetter(self),
                                 'explain': '\xe7\x9b\xae\xe5\x89\x8d\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe7\x8a\xb6\xe6\x80\x81\xe6\x9c\x89\xef\xbc\x9a\xe7\xa7\xbb\xe5\x8a\xa8\xef\xbc\x8c\xe8\xb7\xb3\xe8\xb7\x83\xef\xbc\x8c\xe8\x90\xbd\xe5\x9c\xb0\xef\xbc\x8c\xe5\xb0\x84\xe5\x87\xbb'},
   ('dash_stepheight', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6(m)','min_val': 1.0,'max_val': 3.5},('combo_time', 'param'): {'zh_name': '\xe5\x8d\x87\xe9\xbe\x99\xe6\x8b\xb3\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4'},('break_rush_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8f\xaf\xe4\xb8\xad\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_dragonrush_postsetter(self)
                                  }
   })
class DragonRush(OxRushNew):

    def read_data_from_custom_param(self):
        self.additional_weapon_pos = self.custom_param.get('additional_weapon_pos', None)
        self.combo_time = self.custom_param.get('combo_time', 0.1)
        self.pre_anim_list = self.custom_param.get('pre_anim_list', [])
        self.rush_anim_list = self.custom_param.get('rush_anim_list', [])
        self.hit_anim_list = self.custom_param.get('hit_anim_list', [])
        self.anim_count = len(self.pre_anim_list)
        self.break_rush_time = self.custom_param.get('break_rush_time', 0.01)
        self.max_speed_enhance = self.custom_param.get('max_speed_enhance', 0) * NEOX_UNIT_SCALE
        super(DragonRush, self).read_data_from_custom_param()
        self.refresh_param_changed()
        return

    def refresh_param_changed--- This code section failed: ---

 771       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'spd_dis_enhance'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    45  'to 45'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'spd_dis_enhance'
          18  POP_JUMP_IF_FALSE    45  'to 45'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  'max_speed_enhance'
        27_0  COME_FROM                '18'
        27_1  COME_FROM                '9'
          27  POP_JUMP_IF_FALSE    45  'to 45'

 772      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             2  'max_speed_enhance'
          36  LOAD_FAST             0  'self'
          39  STORE_ATTR            3  'max_rush_speed'
          42  JUMP_FORWARD         12  'to 57'

 774      45  LOAD_FAST             0  'self'
          48  LOAD_ATTR             4  'max_speed'
          51  LOAD_FAST             0  'self'
          54  STORE_ATTR            3  'max_rush_speed'
        57_0  COME_FROM                '42'

 775      57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             5  'refresh_speed'
          63  CALL_FUNCTION_0       0 
          66  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def _register_sub_state_callbacks(self):
        super(DragonRush, self)._register_sub_state_callbacks()
        self.register_substate_callback(self.STATE_RUSH, self.break_rush_time, self.enable_break_rush)
        self.register_substate_callback(self.STATE_HIT, self.combo_time, self.on_add_combo_white_state)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        self.spd_dis_enhance = False
        super(DragonRush, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.additional_weapon_enabled = False
        self.anim_index = 0
        self.can_break_rush = False
        self.new_custom_param = self.custom_param
        self.enable_param_changed_by_buff()

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        else:
            if self.can_break_rush and self.is_active and self.sub_state == self.STATE_RUSH:
                self.on_hit_target(None)
                return True
            if not self.check_can_cast_skill():
                return False
            self.active_self()
            super(OxRushNew, self).action_btn_down()
            self.sound_custom_start()
            return True

    def enter(self, leave_states):
        super(DragonRush, self).enter(leave_states)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.pre_anim = self.pre_anim_list[self.anim_index]
        self.rush_anim = self.rush_anim_list[self.anim_index]
        self.hit_anim = self.hit_anim_list[self.anim_index]
        self.anim_index = (self.anim_index + 1) % self.anim_count
        self.can_break_rush = False

    def on_end_rush(self):
        self.is_moving = False
        self.on_hit_target(None)
        return

    def on_begin_hit(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.hit_anim_rate)
        self.send_event('E_POST_ACTION', self.hit_anim, LOW_BODY, 1, blend_time=0.0)
        if self.additional_weapon_enabled and self.additional_weapon_pos:
            self.ev_g_try_weapon_attack_begin(self.additional_weapon_pos)
            self.ev_g_try_weapon_attack_end(self.additional_weapon_pos)
        self.sound_drive.run_end()
        self.is_moving = False
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)

    def enable_break_rush(self):
        self.can_break_rush = True

    def on_add_combo_white_state(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_DASH_JUMP_1}, self.sid)

    def on_add_hit_white_state(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_JUMP_1, MC_JUMP_2}, self.sid)
        if self.ev_g_on_ground() or ray_check_on_ground(self):
            self.send_event('E_RESET_GRAVITY')
            self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT}, self.sid)
            self.can_break_by_move = True
        else:
            self.send_event('E_FALL')

    def _check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()

    def exit(self, enter_states):
        super(OxRushNew, self).exit(enter_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        global_data.emgr.enable_camera_yaw.emit(True)
        global_data.emgr.destroy_screen_effect.emit('MeleeRushEffect')
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        if self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')
        elif self.air_dash_end_speed:
            scn = world.get_active_scene()
            cam_forward = scn.active_camera.rotation_matrix.forward
            self.cur_speed = self.air_dash_end_speed
            walk_direction = cam_forward * self.cur_speed
            walk_direction.y = 0
            self.send_event('E_SET_WALK_DIRECTION', walk_direction)
        self.send_event('E_FORBID_ROTATION', False)
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_OX_END_RUSH')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
        self._check_custom_param_refreshed()
        if MC_DRAGON_SHAPE not in self.ev_g_cur_state():
            self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH_1)
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/mech_rush.png', 'show')

    def on_hit_target(self, target):
        if self.sub_state != self.STATE_RUSH:
            return
        else:
            if self.target_hitted:
                return
            super(OxRushNew, self).sound_custom_end()
            if target and target.MASK & self.RUSH_DAMAGE_TARGET_TAG_VALUE:
                from logic.gcommon.skill.client.SkillOxRush import STAGE_DMG
                self.send_event('E_DO_SKILL', self.hit_skill_id, [target.id], self.ev_g_position(), None, STAGE_DMG)
                return
            self.target_hitted = target
            self.send_event('E_FORBID_ROTATION', False)
            self.send_event('E_RESET_ROTATION')
            self.send_event('E_CLEAR_SPEED')
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_OX_END_RUSH')
            self.sub_state = self.STATE_HIT
            if not self.ev_g_is_agent():
                global_data.player.logic.send_event('E_MECHA_CAMERA', camera_state_const.MECHA_MODE_FOUR)
            self.send_event('E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED')
            scn = world.get_active_scene()
            camera = scn.active_camera
            fire_forward = camera.rotation_matrix.forward
            fire_position = camera.position
            if self.is_hit_play_skill:
                self.send_event('E_DO_SKILL', self.attack_skill_id, 0, fire_position, fire_forward)
            return

    def refresh_action_param(self, action_param, custom_param):
        super(DragonRush, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.new_custom_param = custom_param
            if not self.is_active:
                self._check_custom_param_refreshed()


@editor.state_exporter({('switch_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe9\x95\xbf\xe5\xba\xa6','post_setter': lambda self: self._register_callbacks()
                                       },
   ('switch_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                   },
   ('switch_time', 'param'): {'zh_name': '\xe5\xbd\xa2\xe6\x80\x81\xe8\xbd\xac\xe6\x8d\xa2\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks(),
                              'explain': '\xe5\x85\xb3\xe9\x97\xad\xe4\xb8\x8a\xe5\x8d\x8a\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe4\xbd\x9c\xe4\xb8\xba\xe5\x85\xa8\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8a\x9f\xe8\x83\xbd\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'},
   ('switch_anim_break_time', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x89\x93\xe6\x96\xad\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks(),
                                         'explain': '\xe5\x9c\xa8\xe8\xbf\x99\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9\xe4\xb9\x8b\xe5\x90\x8e\xe6\x89\x8d\xe5\x85\x81\xe8\xae\xb8\xe5\xa5\x94\xe8\xb7\x91\xe3\x80\x81\xe8\xb7\xb3\xe8\xb7\x83\xe3\x80\x81\xe6\x94\xbb\xe5\x87\xbb'}
   })
class SwitchDragonShape(StateBase):
    BIND_EVENT = {'E_IMMOBILIZED': 'on_immobilized',
       'E_BEAT_BACK': 'on_immobilized',
       'E_REFRESH_DRAGON_SWITCH_PARAM': '_check_custom_param_refreshed',
       'E_BEGIN_RECOVER_DRAGON_SWITCH_SKILL_MP': 'begin_recover_mp',
       'E_SKILL_INIT_COMPLETE': 'on_skill_init_complete'
       }
    STATE_NONE = 0
    STATE_SWITCH = 1

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 801151)
        self.switch_anim = self.custom_param.get('switch_anim', 'j_variant_01')
        self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 0.8)
        self.switch_anim_rate = self.custom_param.get('switch_anim_rate', 1.0)
        self.switch_time = self.custom_param.get('switch_time', 0.2)
        self.switch_anim_break_time = self.custom_param.get('switch_anim_break_time', 0.3)
        self._register_callbacks()

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_SWITCH, 0, self.begin_switch_anim)
        self.register_substate_callback(self.STATE_SWITCH, self.switch_time, self.do_switch)
        self.register_substate_callback(self.STATE_SWITCH, self.switch_anim_break_time, self.set_anim_can_break)
        self.register_substate_callback(self.STATE_SWITCH, self.switch_anim_duration, self.end_switch_anim)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SwitchDragonShape, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.new_custom_param = self.custom_param
        self.sound_param_delay_refresh = True
        self.skill_ended = False
        self.action_forbidden = False

    def action_btn_down(self):
        if self.is_active:
            if self.sub_state == self.STATE_NONE:
                self.sub_state = self.STATE_SWITCH
        else:
            if self.ev_g_in_dragon_shape():
                if not self.skill_ended:
                    self.send_event('E_END_SKILL', self.skill_id)
                    self.skill_ended = True
                return
            if not self.check_can_active():
                return
            if not self.check_can_cast_skill():
                return
            self.active_self()
        super(SwitchDragonShape, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(SwitchDragonShape, self).enter(leave_states)
        if MC_DRAGON_SHAPE not in leave_states:
            self._check_custom_param_refreshed()
            self.send_event('E_DO_SKILL', self.skill_id)
            self.skill_ended = False
            self.send_event('E_SET_ACTION_FORBIDDEN', self.bind_action_id, True)
            self.action_forbidden = True
        self.sub_state = self.STATE_SWITCH
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def begin_switch_anim(self):
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE, is_interpolate=True, blend_time=0.2)
        self.send_event('E_ANIM_RATE', UP_BODY, self.switch_anim_rate)
        self.send_event('E_POST_ACTION', self.switch_anim, UP_BODY, 1)

    def do_switch(self):
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE, is_interpolate=True, blend_time=0.2)

    def set_anim_can_break(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_DASH_1, MC_DASH}, self.sid)

    def _clear_up_body_anim(self):
        if self.is_active and self.sd.ref_up_body_anim == self.switch_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)

    def _check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()
            self._check_sound_param_refresh()

    def end_switch_anim(self):
        self._clear_up_body_anim()
        self.disable_self()
        self._check_custom_param_refreshed()
        self.sub_state = self.STATE_NONE

    def update(self, dt):
        super(SwitchDragonShape, self).update(dt)

    def exit(self, enter_states):
        if self.sub_state == self.STATE_SWITCH:
            self._clear_up_body_anim()
            self._check_custom_param_refreshed()
            self.sub_state = self.STATE_NONE
        if self.action_forbidden:
            self.send_event('E_SET_ACTION_FORBIDDEN', self.bind_action_id, False)
            self.action_forbidden = False
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        super(SwitchDragonShape, self).exit(enter_states)

    def refresh_action_param(self, action_param, custom_param):
        super(SwitchDragonShape, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.new_custom_param = custom_param

    def on_immobilized(self, *args):
        self._clear_up_body_anim()

    def begin_recover_mp(self):
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def on_skill_init_complete(self):
        if self.ev_g_dragon_shape_left_time()[1] <= 0 and not self.check_can_cast_skill():
            self.begin_recover_mp()


class DragonShape(StateBase):
    BIND_EVENT = {'E_TRANS_TO_DRAGON': 'trans_to_dragon',
       'G_IN_DRAGON_SHAPE': 'in_dragon_shape',
       'G_DRAGON_SHAPE_LEFT_TIME': 'get_left_time'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DragonShape, self).init_from_dict(unit_obj, bdict, sid, info)
        self.buff_data = None
        self.left_time = 0
        self.dragon_shape_ended = True
        return

    def enter(self, leave_states):
        super(DragonShape, self).enter(leave_states)
        self.send_event('E_REFRESH_STATE_PARAM')
        self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', True)
        if MC_TRANSFORM not in self.ev_g_cur_state():
            self.send_event('E_REFRESH_DRAGON_SWITCH_PARAM')
        if not self.ev_g_is_agent():
            self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', True)
            self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_DEFAULT_ENABLED', True)
        self.send_event('E_SET_ACTION_VISIBLE', 'action8', False)
        self.send_event('E_SET_ACTION_SELECTED', 'action7', True)
        if MC_DASH_1 not in self.ev_g_cur_state():
            self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH)
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/icon_mech8011_4.png', 'show')
        self.send_event('E_ENABLE_MECHA_FOOT_IK', True)

    def _end_dragon_shape(self):
        if not self.dragon_shape_ended:
            self.dragon_shape_ended = True
            if self.ev_g_status_check_pass(MC_TRANSFORM, only_avatar=True):
                self.send_event('E_ACTIVE_STATE', MC_TRANSFORM)
            else:
                self.disable_self()

    def update(self, dt):
        super(DragonShape, self).update(dt)
        self.left_time -= dt
        if self.dragon_shape_ended:
            self.disable_self()
            return
        if self.left_time <= 0:
            self._end_dragon_shape()

    def exit(self, enter_states):
        super(DragonShape, self).exit(enter_states)
        self.send_event('E_RESET_STATE_PARAM')
        self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', False)
        self.send_event('E_ENABLE_MECHA_FREE_SIGHT_MODE', False)
        self.send_event('E_SET_MECHA_FREE_SIGHT_MODE_DEFAULT_ENABLED', False)
        self.send_event('E_SET_ACTION_VISIBLE', 'action8', True)
        self.send_event('E_SET_ACTION_SELECTED', 'action7', False)
        if MC_DASH not in self.ev_g_cur_state():
            self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH_1)
            self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/mech_rush.png', 'show')
        self.send_event('E_BEGIN_RECOVER_DRAGON_SWITCH_SKILL_MP')
        self.send_event('E_ENABLE_MECHA_FOOT_IK', False)

    def trans_to_dragon(self, data, left_time):
        self.buff_data = data
        self.left_time = left_time
        if not self.is_active:
            if left_time > 0:
                self.active_self()
                self.dragon_shape_ended = False
        elif left_time <= 0:
            self._end_dragon_shape()

    def in_dragon_shape(self):
        return self.is_active

    def get_left_time(self):
        return (
         self.buff_data, self.left_time)