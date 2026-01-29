# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/ShootLogic.py
from __future__ import absolute_import
import six
from six.moves import range
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
import logic.gcommon.const as g_const
import game3d
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_const.mecha_const as m_const
import logic.gcommon.common_const.weapon_const as w_const
from logic.comsys.control_ui.ShotChecker import ShotChecker
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_utils import status_utils
import wwise
from logic.gutils import character_ctrl_utils
from common.utils.timer import CLOCK
from copy import deepcopy
from logic.gcommon.common_const.attr_const import ATTR_ACCUMULATE_ENERGY_INIT_VALUE_RATIO
from logic.gcommon import editor
from logic.comsys.battle.BattleUtils import can_fire
from common.cfg import confmgr
_HASH_Rim_intensity = game3d.calc_string_hash('Rim_intensity')
_HASH_AlphaFix = game3d.calc_string_hash('AlphaFix')

@editor.state_exporter({('pre_aim_ik_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe7\x94\xa8IK\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4'},('aim_ik_lerp_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe7\x94\xa8IK\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('support_exit_aim_ik_lerp', 'param'): {'zh_name': '\xe6\x94\xaf\xe6\x8c\x81\xe9\x80\x80\xe5\x87\xbaIK\xe6\x8f\x92\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1'},('exit_aim_ik_lerp_time', 'param'): {'zh_name': '\xe9\x80\x80\xe5\x87\xbaIK\xe6\x8f\x92\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('aim_ik_pitch_limit', 'param'): {'zh_name': 'IK\xe6\x9c\x80\xe5\xa4\xa7\xe4\xbf\xaf\xe4\xbb\xb0\xe8\xa7\x92\xe9\x99\x90\xe5\x88\xb6'}})
class WeaponFire(StateBase):
    BIND_EVENT = {'E_FIRE': 'on_fire',
       'E_IN_AIR': 'on_in_air',
       'E_SET_FIRE_ON_RELEASE': 'set_fire_on_release',
       'G_CONTINUE_FIRE': 'continue_fire',
       'E_WEAPON_CHANGED': 'on_weapon_change',
       'E_SET_SHOOT_BLEND_TIME': 'set_shoot_blend_time',
       'E_REPLACE_SHOOT_ANIM': 'on_replace_shoot_anim',
       'E_RESET_SHOOT_ANIM': 'on_reset_shoot_anim',
       'E_TEMP_CHANGE_WEAPON_POS': 'temporarily_change_weapon_pos',
       'E_RECOVER_WEAPON_POS_CHANGE': 'recover_weapon_pos_change',
       'TRY_STOP_WEAPON_ATTACK': '_end_shoot',
       'E_WEAPON_FIRE_BUTTON_DOWN': 'action_btn_down_from_event'
       }

    def read_data_from_custom_param(self):
        self._nl_shoot_anim, self.anim_part, self.anim_blend_type = self.custom_param.get('shoot_anim', (None,
                                                                                                         'upper',
                                                                                                         1))
        self.extern_bone_tree = self.custom_param.get('extern_bone_tree', None)
        self.sub_bone_tree = self.custom_param.get('sub_bone_tree', None)
        self.aim_anim, self.aim_anim_part, self.aim_anim_blend_type = self.custom_param.get('aim_anim', (None,
                                                                                                         'upper',
                                                                                                         1))
        self.aim_anim_kwargs = self.custom_param.get('aim_anim_kwargs', {})
        if type(self._nl_shoot_anim) == str:
            self.shoot_anim = self._nl_shoot_anim
            self.shoot_anim_index = -1
            self.all_shoot_anim = {self._nl_shoot_anim, 'air_' + self._nl_shoot_anim}
        else:
            self.shoot_anim_index = 0
            self.shoot_anim_count = len(self._nl_shoot_anim)
            self.shoot_anim = self._nl_shoot_anim[0]
            self.all_shoot_anim = set(self._nl_shoot_anim)
        self.shoot_anim_rate = self.custom_param.get('shoot_anim_rate', 1.0)
        self.idle_hold_time = self.custom_param.get('idle_hold_time')
        self.blend_time = self.custom_param.get('blend_time', 0.0)
        self.play_shoot_anim_per_active = self.custom_param.get('play_shoot_anim_per_active', False)
        self.aim_anim and self.all_shoot_anim.add(self.aim_anim)
        self.need_keep_last_fire_time = self.custom_param.get('need_keep_fire_time', False)
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.weapon_pos_set = self.custom_param.get('weapon_pos_set', set())
        self.fire_on_release = self.custom_param.get('fire_on_release', False)
        self.fire_anim_time = self.custom_param.get('anim_time', 0.5)
        self.slow_down_on_shoot = self.custom_param.get('slow_down_on_shoot', True)
        self.slow_down_speed = self.custom_param.get('slow_down_speed', None)
        if self.slow_down_speed:
            self.slow_down_speed *= NEOX_UNIT_SCALE
        self.use_up_anim_bone = self.custom_param.get('use_up_anim_bone', None)
        self.use_up_anim_states = deepcopy(self.custom_param.get('use_up_anim_states', []))
        status_desc_2_num = character_ctrl_utils.get_status_desc_2_num(self)
        for i in range(len(self.use_up_anim_states)):
            self.use_up_anim_states[i] = status_desc_2_num[self.use_up_anim_states[i]]

        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_pitch_limit = self.custom_param.get('aim_ik_pitch_limit', 80)
        self.support_exit_aim_ik_lerp = self.custom_param.get('support_exit_aim_ik_lerp', True)
        self.exit_aim_ik_lerp_time = self.custom_param.get('exit_aim_ik_lerp_time', 0.2)
        self.aim_move_anim_arg = self.custom_param.get('aim_move_anim', None)
        self.use_low_move_anim_states = deepcopy(self.custom_param.get('use_low_move_anim_states', []))
        for i in range(len(self.use_low_move_anim_states)):
            self.use_low_move_anim_states[i] = status_desc_2_num[self.use_low_move_anim_states[i]]

        self.check_update_up_body_skin_anim()
        return

    def check_update_up_body_skin_anim(self):
        if not self.need_check_skin_anim:
            return
        all_anim = list(self.all_shoot_anim)
        for anim in all_anim:
            if anim in self.skin_anim_map:
                self.all_shoot_anim.add(self.skin_anim_map[anim])

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_check_skin_anim = False
        self.read_data_from_custom_param()
        self.fired = False
        self.fired_time = 0
        self.is_continue_fire = False
        self.want_to_fire = False
        self.is_diving = False
        self.play_aim_anim_time = self.fire_anim_time
        self.aim_anim_played = True
        self.is_show_track = False
        self.fire_hold_time = 0.05
        self.forbid_ik = False

    def on_init_complete(self):
        super(WeaponFire, self).on_init_complete()
        skin_id = self.ev_g_mecha_fashion_id()
        skin_anim_conf = confmgr.get('mecha_skin_anim')
        anim_index = skin_anim_conf['skin_anim_index'].get(str(skin_id), None)
        if anim_index:
            self.need_check_skin_anim = True
            self.skin_anim_map = skin_anim_conf['skin_anim_info'][anim_index]
            self.check_update_up_body_skin_anim()
        return

    def on_post_init_complete(self, *args):
        super(WeaponFire, self).on_post_init_complete(*args)
        if self.idle_hold_time:
            self.fire_hold_time = self.idle_hold_time
        elif self.sd.ref_wp_bar_mp_weapons is not None:
            weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
            self.fire_hold_time = weapon.get_data_by_key('fHoldTime') if weapon else 0.05
        return

    def continue_fire(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not self.ev_g_is_main_weapon_enable():
            return (False, self.weapon_pos)
        if weapon and weapon.get_data_by_key('iMode') == w_const.AUTO_MODE:
            return (self.is_continue_fire, self.weapon_pos)
        return (False, self.weapon_pos)

    def set_fire_on_release(self, fire_on_release):
        self.fire_on_release = fire_on_release

    def action_btn_down(self, ignore_reload=False):
        if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()):
            return False
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        self.is_continue_fire = True
        self.want_to_fire = True
        if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            self.is_continue_fire = False
            self.can_not_fire_attack()
            return False
        if not self.try_weapon_attack_begin():
            self.is_continue_fire = False
            return False
        if self.is_active:
            self.re_enter()
        self.can_fire_attack()
        shoot_mode = self.ev_g_shoot_mode()
        if shoot_mode != m_const.MECHA_SHOOT_QUICK:
            self.show_track_data = self.custom_param.get('show_track', {})
            if self.show_track_data and not self.is_show_track:
                self.send_event('E_SET_TRACK_DATA', self.show_track_data, self.weapon_pos)
                self.is_show_track = True
        if not self.fire_on_release:
            self.active_self()
        super(WeaponFire, self).action_btn_down()
        return True

    def can_not_fire_attack(self):
        pass

    def can_fire_attack(self):
        pass

    def check_can_active(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not weapon:
            return False
        return self.ev_g_status_check_pass(self.sid)

    def action_btn_up(self):
        self.is_continue_fire = False
        self.want_to_fire = False
        if self.ev_g_shoot_mode() != m_const.MECHA_SHOOT_QUICK:
            self.is_show_track = False
        if not self.try_weapon_attack_end():
            return False
        if self.fire_on_release:
            self.active_self()
        super(WeaponFire, self).action_btn_up()
        return True

    def re_enter(self):
        super(WeaponFire, self).enter(set())
        self.fired_time = 0
        self.aim_anim_played = False
        if self.fired:
            self.elapsed_time = 0.1

    def _reset_aim_ik_param(self):
        if self.shoot_aim_ik:
            self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, self.support_exit_aim_ik_lerp)
            self.send_event('E_ENABLE_AIM_IK', True, self.aim_ik_pitch_limit)
            self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.exit_aim_ik_lerp_time)

    def enter(self, leave_states):
        self.fired_time = 0
        self.aim_anim_played = False
        self.send_event('E_SLOW_DOWN', self.slow_down_on_shoot, self.slow_down_speed, 'WeaponFire')
        super(WeaponFire, self).enter(leave_states)
        if self.fired:
            self.elapsed_time = 0.1
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, self.use_up_anim_bone)
        if self.aim_move_anim_arg:
            aim_move_anim, aim_anim_part, aim_anim_blend_type, anim_args = self.aim_move_anim_arg
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_low_move_anim_states, aim_move_anim, **anim_args)
        not self.forbid_ik and self.delay_call(self.pre_aim_ik_time, self._reset_aim_ik_param)

    def update(self, dt):
        if self.fired:
            self.fired_time += dt
        super(WeaponFire, self).update(dt)

    def check_transitions(self):
        if self.fired_time > self.fire_anim_time:
            self.disable_self()
        elif self.aim_anim and self.play_aim_anim_time <= self.fired_time and not self.aim_anim_played:
            part = LOW_BODY if self.aim_anim_part == 'lower' else UP_BODY
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, self.aim_anim, loop=False)
            self.send_event('E_POST_ACTION', self.aim_anim, part, self.aim_anim_blend_type, **self.aim_anim_kwargs)
            self.aim_anim_played = True

    def try_weapon_attack_begin(self):
        if self.weapon_pos_set:
            flag = True
            for weapon_pos in self.weapon_pos_set:
                if not self.ev_g_try_weapon_attack_begin(weapon_pos):
                    flag = False

            return flag
        return self.ev_g_try_weapon_attack_begin(self.weapon_pos)

    def try_weapon_attack_end(self, is_cancel=False):
        if self.weapon_pos_set:
            flag = True
            for weapon_pos in self.weapon_pos_set:
                if not self.ev_g_try_weapon_attack_end(weapon_pos, is_cancel):
                    flag = False

            return flag
        return self.ev_g_try_weapon_attack_end(self.weapon_pos, is_cancel)

    def exit(self, enter_states):
        super(WeaponFire, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire')
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.fired = False
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, None)
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if enter_states:
            self.try_weapon_attack_end()
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, None)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_low_move_anim_states, None)
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False)
        return

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        if weapon_pos != self.weapon_pos:
            return
        if not self.is_active and not self.check_can_active():
            self.try_weapon_attack_end(True)
            if self.sd.ref_up_body_anim in self.all_shoot_anim:
                self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.try_play_fire_anim(fired_socket_index)
        self.fired = True
        self.fired_time = 0
        self.aim_anim_played = False
        self.fire_anim_time = f_cdtime + self.fire_hold_time
        if not self.is_active:
            if not self.check_can_active():
                self.fired = False
            self.active_self()

    def try_play_fire_anim(self, fired_socket_index):
        self.play_fire_anim(fired_socket_index)

    def play_fire_anim(self, fired_socket_index):
        if self.shoot_anim and (self.is_active or self.check_can_active()):
            if self.shoot_anim_index != -1 and self.shoot_anim_index % 2 != fired_socket_index % 2:
                self.shoot_anim_index = fired_socket_index % 2
                self.shoot_anim = self._nl_shoot_anim[self.shoot_anim_index]
            if self.anim_part == 'lower':
                part = LOW_BODY if 1 else UP_BODY
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, self.shoot_anim, loop=False)
                if self.extern_bone_tree and (not self.play_shoot_anim_per_active or fired_socket_index == 0):
                    self.send_event('E_POST_EXTERN_ACTION', self.shoot_anim, True, subtree=self.extern_bone_tree, force_trigger_effect=True, socket_index=fired_socket_index)
            else:
                if not self.play_shoot_anim_per_active or fired_socket_index == 0:
                    self.send_event('E_ANIM_RATE', part, self.shoot_anim_rate)
                    self.send_event('E_POST_ACTION', self.shoot_anim, part, self.anim_blend_type, blend_time=self.blend_time, force_trigger_effect=True, socket_index=fired_socket_index)
                if self.sub_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.shoot_anim, True, subtree=self.sub_bone_tree)
                if self.shoot_anim_index != -1:
                    self.shoot_anim_index = (self.shoot_anim_index + 1) % self.shoot_anim_count
                    self.shoot_anim = self._nl_shoot_anim[self.shoot_anim_index]

    def on_in_air(self, is_in_air):
        if type(self._nl_shoot_anim) == str:
            self.shoot_anim = 'air_' + self._nl_shoot_anim if is_in_air else self._nl_shoot_anim
        else:
            shoot_anim = self._nl_shoot_anim[self.shoot_anim_index]
            self.shoot_anim = 'air_' + shoot_anim if is_in_air else shoot_anim

    def refresh_action_param(self, action_param, custom_param):
        super(WeaponFire, self).refresh_action_param(action_param, custom_param)
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False)
        if custom_param:
            need_active_weapon_attack = False
            old_weapon_pos = self.weapon_pos
            new_weapon_pos = custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
            if old_weapon_pos != new_weapon_pos and self.need_keep_last_fire_time:
                if self.is_active:
                    self.try_weapon_attack_end(True)
                    need_active_weapon_attack = True
            else:
                if self.is_continue_fire:
                    self.try_weapon_attack_end()
                self.custom_param = custom_param
                self.read_data_from_custom_param()
                if need_active_weapon_attack:
                    self.send_event('E_RECOVER_LAST_FIRE_TIME', old_weapon_pos, self.weapon_pos)
                    self.try_weapon_attack_begin()
                    if not self.want_to_fire:
                        self.try_weapon_attack_end()
                    return
        elif self.is_continue_fire:
            self.try_weapon_attack_end()
        if self.is_continue_fire:
            self.try_weapon_attack_begin()
        return

    def destroy(self):
        self.try_weapon_attack_end()
        self.send_event('E_STOP_WP_TRACK')
        self.is_continue_fire = False
        super(WeaponFire, self).destroy()

    def on_weapon_change(self, *args):
        self.try_weapon_attack_end(True)

    def set_shoot_blend_time(self, blend_time):
        self.blend_time = blend_time

    def on_replace_shoot_anim(self, anim_name, forbid_ik=False):
        self.all_shoot_anim.add(anim_name)
        if self.shoot_aim_ik and forbid_ik:
            self.forbid_ik = True
            self.send_event('E_ENABLE_AIM_IK', False)
        self.shoot_anim = anim_name

    def on_reset_shoot_anim(self):
        if self.forbid_ik:
            self.shoot_aim_ik and self.is_active and self.elapsed_time > self.pre_aim_ik_time and self._reset_aim_ik_param()
            self.forbid_ik = False
        if type(self._nl_shoot_anim) == str:
            self.shoot_anim = self._nl_shoot_anim
        else:
            self.shoot_anim = self._nl_shoot_anim[self.shoot_anim_index]

    def temporarily_change_weapon_pos(self, weapon_pos):
        self.try_weapon_attack_end()
        self.weapon_pos = weapon_pos

    def recover_weapon_pos_change(self):
        self.try_weapon_attack_end()
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)

    def _end_shoot(self, *args):
        self.try_weapon_attack_end()
        self.disable_self()

    def action_btn_down_from_event(self, weapon_pos):
        if weapon_pos == self.weapon_pos:
            self.action_btn_down()
            self.action_btn_up()


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('pre_anim', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c'},('hold_anim', 'param'): {'zh_name': '\xe5\xb0\xb1\xe7\xbb\xaa\xe5\x8a\xa8\xe4\xbd\x9c'},('post_anim', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c'},('pre_time', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('post_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('post_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'},('force_pre', 'param'): {'zh_name': '\xe6\x98\xaf\xe5\x90\xa6\xe5\xbc\xba\xe5\x88\xb6\xe5\x89\x8d\xe6\x91\x87','attr_name': '_force_pre'},('hold_anim_loop', 'param'): {'zh_name': 'hold\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x98\xaf\xe5\x90\xa6\xe5\xbe\xaa\xe7\x8e\xaf\xe6\x92\xad\xe6\x94\xbe','enum': [True, False]},('hold_time_scale', 'param'): {'zh_name': 'hold\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('acc_speed_factor', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe5\x9c\xa8\xe7\xa9\xba\xe4\xb8\xad\xe7\x9a\x84\xe9\x80\x9f\xe5\xba\xa6\xe7\xb3\xbb\xe6\x95\xb0'},('acc_gravity_factor', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe5\x9c\xa8\xe7\xa9\xba\xe4\xb8\xad\xe9\x87\x8d\xe5\x8a\x9b\xe7\xb3\xbb\xe6\x95\xb0'},('acc_air_time', 'param'): {'zh_name': '\xe8\x93\x84\xe5\x8a\x9b\xe6\xb5\xae\xe7\xa9\xba\xe6\x97\xb6\xe9\x97\xb4'}})
class AccumulateShoot(StateBase):
    BIND_EVENT = {'E_LEAVE_JUMP_GROUND': 'on_ground',
       'E_IN_AIR': 'on_in_air',
       'TRY_STOP_WEAPON_ATTACK': '_end_shoot',
       'E_END_FLIGHT': 'end_flight',
       'E_SET_ACCUMULATE_SHOOT_ANIM_PARAM': 'set_anim_param',
       'E_RESET_ACCUMULATE_SHOOT_ANIM_PARAM': 'reset_anim_param',
       'E_ACC_ACCUMULATE_CD': 'acc_accumulate_cd'
       }
    SUB_ST_PRE = 1
    SUB_ST_HOLD = 2
    SUB_ST_POST = 3

    def read_data_from_custom_param(self):
        self.all_up_body_anim = set()
        self.skill_id = self.custom_param.get('skill_id', None)
        self.hover_skill_id = self.custom_param.get('hover_skill_id', None)
        self.forbid_state = deepcopy(self.custom_param.get('forbid_state', None))
        if self.forbid_state:
            status_desc_2_num = character_ctrl_utils.get_status_desc_2_num(self)
            for i in range(len(self.forbid_state)):
                self.forbid_state[i] = status_desc_2_num[self.forbid_state[i]]

            self.forbid_state = set(self.forbid_state)
        if self.forbid_state is None:
            self.forbid_state = {
             MC_TURN, MC_JUMP_1, MC_DASH, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_TRANSFORM, MC_MOVE}
        self._nl_pre_anim = self.custom_param.get('pre_anim', None)
        self._nl_hold_anim = self.custom_param.get('hold_anim', None)
        self._nl_post_anim = self.custom_param.get('post_anim', None)
        self.acc_post_anim = self.custom_param.get('acc_post_anim', [])
        self.extern_bone_tree = self.custom_param.get('extern_bone_tree', None)
        self.sub_bone_tree = self.custom_param.get('sub_bone_tree', None)
        self.pre_anim = self._nl_pre_anim
        self.hold_anim = self._nl_hold_anim
        self.post_anim = self._nl_post_anim
        self.pre_anim and self.all_up_body_anim.add(self.pre_anim)
        self.hold_anim and self.all_up_body_anim.add(self.hold_anim)
        self.post_anim and self.all_up_body_anim.add(self.post_anim)
        for anim in self.acc_post_anim:
            self.all_up_body_anim.add(anim)

        self.pre_time = self.custom_param.get('pre_time', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.post_time = self.custom_param.get('post_time', 0.5)
        self.post_anim_rate = self.custom_param.get('post_anim_rate', 1.0)
        self.post_break_time = self.custom_param.get('post_break_time', 0.9)
        self._force_pre = self.custom_param.get('force_pre', False)
        self._shoot_move_anim = self.custom_param.get('shoot_move_anim', None)
        self._shoot_move_anim_beginning = self.custom_param.get('shoot_move_anim', 'enter')
        self.use_up_anim_bone = self.custom_param.get('use_up_anim_bone', None)
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN2)
        self.hold_anim_loop = self.custom_param.get('hold_anim_loop', True)
        self.hold_time_scale = self.custom_param.get('hold_time_scale', 1.0)
        self.acc_speed_factor = self.custom_param.get('acc_speed_factor', 1.0)
        self.acc_gravity_factor = self.custom_param.get('acc_gravity_factor', 1.0)
        self.acc_air_time = self.custom_param.get('acc_air_time', 1.0)
        self._bind_actions = self.custom_param.get('bind_actions', [])
        self.use_up_anim_states = deepcopy(self.custom_param.get('use_up_anim_states', []))
        for i in range(len(self.use_up_anim_states)):
            self.use_up_anim_states[i] = desc_2_num[self.use_up_anim_states[i]]

        self.save_gravity = 0.0
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.check_update_up_body_skin_anim()
        return

    def check_update_up_body_skin_anim(self):
        if not self.need_check_skin_anim:
            return
        all_anim = list(self.all_up_body_anim)
        for anim in all_anim:
            if anim in self.skin_anim_map:
                self.all_up_body_anim.add(self.skin_anim_map[anim])

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateShoot, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_check_skin_anim = False
        self.read_data_from_custom_param()
        self.action_hold = False
        self.acted = False
        self._skip_acc_state = False
        self.post_cnt = 0
        self.acc_skill_ended = True
        self.need_trigger_up = False

    def on_init_complete(self):
        super(AccumulateShoot, self).on_init_complete()
        skin_id = self.ev_g_mecha_fashion_id()
        skin_anim_conf = confmgr.get('mecha_skin_anim')
        anim_index = skin_anim_conf['skin_anim_index'].get(str(skin_id), None)
        if anim_index:
            self.need_check_skin_anim = True
            self.skin_anim_map = skin_anim_conf['skin_anim_info'][anim_index]
            self.check_update_up_body_skin_anim()
        return

    def action_btn_down(self):
        self.need_trigger_up = False
        if self.is_active:
            return False
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_is_weapon_can_fire(self.weapon_pos):
            return False
        self.sub_state = self.SUB_ST_PRE
        self.active_self()
        self.action_hold = True
        super(AccumulateShoot, self).action_btn_down()
        return True

    def action_btn_up(self):
        self.btn_down = False
        if self.sub_state == self.SUB_ST_POST:
            super(AccumulateShoot, self).action_btn_cancel()
            return
        if not self.is_active:
            self.need_trigger_up = True
            return False
        if self._force_pre:
            end_pre = self.pre_time < self.elapsed_time
            self.acted = end_pre
        else:
            self.acted = True
        if not self.acted:
            self._skip_acc_state = True
            self.delay_call(self.pre_time - self.elapsed_time, self._post_action)
        else:
            self._post_action()
        self.action_hold = False
        super(AccumulateShoot, self).action_btn_up()
        return True

    def enter(self, leave_states):
        super(AccumulateShoot, self).enter(leave_states)
        if not self.ev_g_try_weapon_attack_begin(self.weapon_pos):
            self.disable_self()
            return
        else:
            self.send_event('E_RESET_ROTATION')
            self.acted = False
            self._skip_acc_state = False
            self.post_cnt = 0
            self.send_event('E_SLOW_DOWN', True)
            self.send_event('E_ACC_SKILL_BEGIN', self.weapon_pos)
            self.acc_skill_ended = False
            if self.pre_time:
                if self.extern_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.pre_anim, True, subtree=self.extern_bone_tree)
                else:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.pre_anim, loop=False)
                    self.send_event('E_POST_ACTION', self.pre_anim, UP_BODY, 1)
                    if self.sub_bone_tree:
                        self.send_event('E_POST_EXTERN_ACTION', self.pre_anim, True, subtree=self.sub_bone_tree)
                    self.send_event('E_ANIM_RATE', UP_BODY, self.pre_anim_rate)
                    self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
                    if self._shoot_move_anim and self._shoot_move_anim_beginning == 'enter':
                        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self._shoot_move_anim)
            if self.use_up_anim_states and self.hold_anim:
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, self.hold_anim, loop=True)
            if self.use_up_anim_bone:
                self.send_event('E_UPBODY_BONE', self.use_up_anim_bone['enter'])
            if self.ev_g_is_avatar():
                from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                MechaCancelUI(None, self._end_shoot)

            def reset_param():
                if self.shoot_aim_ik:
                    self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik)
                    self.send_event('E_ENABLE_AIM_IK', True)
                    self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time)

            self.delay_call(self.pre_aim_ik_time, reset_param)
            if self.need_trigger_up:
                self.action_btn_up()
                self.need_trigger_up = False
            return

    def update(self, dt):
        if not self.acted and not self._skip_acc_state:
            if self.elapsed_time <= self.pre_time <= self.elapsed_time + dt:
                if self.extern_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.hold_anim, True, subtree=self.extern_bone_tree, loop=True)
                else:
                    if self.hold_time_scale != 1.0:
                        play_scale = self.ev_g_accumulate_scale(self.weapon_pos)
                        self.send_event('E_POST_ACTION', self.hold_anim, UP_BODY, 1, timeScale=self.hold_time_scale * play_scale, loop=self.hold_anim_loop)
                    else:
                        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.hold_anim, loop=True)
                        self.send_event('E_POST_ACTION', self.hold_anim, UP_BODY, 1, loop=self.hold_anim_loop)
                    if self.sub_bone_tree:
                        self.send_event('E_POST_EXTERN_ACTION', self.hold_anim, True, subtree=self.sub_bone_tree)
                    if self._shoot_move_anim and self._shoot_move_anim_beginning == 'hold':
                        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self._shoot_move_anim)
                self.sub_state = self.SUB_ST_HOLD
                if self.ev_g_on_ground() or self.acc_gravity_factor != 1.0:
                    self.save_gravity = self.sd.ref_gravity
                    self.send_event('E_GRAVITY', self.save_gravity * self.acc_gravity_factor)
                    if self.hover_skill_id:
                        self.send_event('E_DO_SKILL', self.hover_skill_id)
                if self.acc_speed_factor != 1.0:
                    cur_dir = self.ev_g_get_walk_direction()
                    self.send_event('E_SET_WALK_DIRECTION', cur_dir * self.acc_speed_factor)
                    cur_ver_speed = self.ev_g_vertical_speed()
                    self.send_event('E_VERTICAL_SPEED', cur_ver_speed * self.acc_speed_factor)
        elif self.sub_state == self.SUB_ST_HOLD:
            if self.save_gravity != 0.0:
                hold_pass_time = self.elapsed_time - self.pre_time
                if hold_pass_time > self.acc_air_time:
                    self.send_event('E_GRAVITY', self.save_gravity)
                    self.save_gravity = 0.0
                    if self.hover_skill_id:
                        self.send_event('E_END_SKILL', self.hover_skill_id)
        if self.acted:
            self.post_cnt += dt
        super(AccumulateShoot, self).update(dt)

    def _post_action(self):
        self.acted = True
        acc_level, max_level = self.ev_g_accumulate_level(self.weapon_pos)
        post_anim = self.post_anim
        if self.acc_post_anim:
            post_anim = self.acc_post_anim[acc_level]
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        self.send_event('E_ACC_SKILL_END')
        self.acc_skill_ended = True
        if self.hover_skill_id:
            self.send_event('E_END_SKILL', self.hover_skill_id)
        if post_anim:
            self.send_event('E_ANIM_RATE', UP_BODY, self.post_anim_rate)
            self.send_event('E_ANIM_RATE', LOW_BODY, self.post_anim_rate)
            self.sub_state = self.SUB_ST_POST
            if self.extern_bone_tree:
                self.send_event('E_POST_EXTERN_ACTION', post_anim, True, subtree=self.extern_bone_tree)
            else:
                if self.use_up_anim_states:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, post_anim, loop=False)
                else:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, post_anim, loop=False)
                if self.hold_time_scale != 1.0:
                    self.send_event('E_POST_ACTION', post_anim, UP_BODY, 1, timeScale=1.0)
                else:
                    self.send_event('E_POST_ACTION', post_anim, UP_BODY, 1)
                if self.sub_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', post_anim, True, subtree=self.sub_bone_tree)
                if not self.use_up_anim_states:
                    self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
            if self.forbid_state:
                self.send_event('E_ADD_BLACK_STATE', self.forbid_state)
                if MC_MOVE in self.forbid_state:
                    self.send_event('E_BRAKE')
            if self.save_gravity != 0.0:
                self.send_event('E_GRAVITY', self.save_gravity)
                self.save_gravity = 0.0
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        return

    def check_transitions(self):
        if self.post_cnt > self.post_break_time:
            self.send_event('E_CLEAR_BLACK_STATE')
            self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_SHOOT}, self.sid)
        if self.post_cnt > self.post_time:
            self.disable_self()

    def exit(self, enter_states):
        super(AccumulateShoot, self).exit(enter_states)
        if self.hover_skill_id:
            self.send_event('E_END_SKILL', self.hover_skill_id)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND, MC_MOVE, MC_HOVER), None)
        if self.sd.ref_up_body_anim in self.all_up_body_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        if self.save_gravity != 0.0:
            self.send_event('E_GRAVITY', self.save_gravity)
            self.save_gravity = 0.0
        if self.action_hold or not self.acc_skill_ended:
            self.send_event('E_ACC_SKILL_END')
            self.acc_skill_ended = True
        if self.use_up_anim_bone:
            self.send_event('E_UPBODY_BONE', self.use_up_anim_bone['exit'])
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        return

    def on_in_air(self, is_in_air):
        self.pre_anim = is_in_air and 'air_' + self._nl_pre_anim if 1 else self._nl_pre_anim
        self.hold_anim = 'air_' + self._nl_hold_anim if is_in_air else self._nl_hold_anim
        self.post_anim = 'air_' + self._nl_post_anim if is_in_air else self._nl_post_anim
        if self.pre_anim not in self.all_up_body_anim:
            self.all_up_body_anim.add(self.pre_anim)
        if self.hold_anim not in self.all_up_body_anim:
            self.all_up_body_anim.add(self.hold_anim)
        if self.post_anim not in self.all_up_body_anim:
            self.all_up_body_anim.add(self.post_anim)

    def on_ground(self, *args):
        if not self.is_active:
            return
        if self.hover_skill_id:
            self.send_event('E_END_SKILL', self.hover_skill_id)

    def _end_shoot(self):
        self.sub_state = self.SUB_ST_POST
        self.disable_self()
        self.send_event('E_ACTION_UP', self.bind_action_id)
        for action_id in self._bind_actions:
            self.send_event('E_ACTION_UP', action_id)

    def end_flight(self):
        if self.is_active:
            self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_1}, self.sid)

    def set_anim_param(self, anim_dict):
        self.pre_anim, self.pre_time = anim_dict.get('pre_param', (None, 0))
        self.hold_anim = anim_dict.get('hold_param', None)
        self.post_anim, self.post_time = anim_dict.get('post_param', (None, 0.5))
        return

    def reset_anim_param(self):
        self.pre_anim = self.custom_param.get('pre_anim', None)
        self.hold_anim = self.custom_param.get('hold_anim', None)
        self.post_anim = self.custom_param.get('post_anim', None)
        self.pre_time = self.custom_param.get('pre_time', 0)
        self.post_time = self.custom_param.get('post_time', 0.5)
        return

    def destroy(self):
        super(AccumulateShoot, self).destroy()
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')

    def acc_accumulate_cd(self, dec_percent, wp_pos=None):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(wp_pos if wp_pos else self.weapon_pos)
        if weapon:
            weapon.set_accumulate_dec_percent(dec_percent)

    def refresh_action_param(self, action_param, custom_param):
        super(AccumulateShoot, self).refresh_action_param(action_param, custom_param)
        if self.extern_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()
        return


@editor.state_exporter({('weapon_pos', 'param'): {'zh_name': '\xe6\xad\xa6\xe5\x99\xa8\xe4\xbd\x8d\xe7\xbd\xae'},('force_pre', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x88\xb6\xe5\x89\x8d\xe6\x91\x87','param_type': 'bool'},('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('post_anim_blend_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('post_anim_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                     },
   ('post_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('post_forbid_states', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe9\x98\xb6\xe6\xae\xb5\xe7\xa6\x81\xe6\xad\xa2\xe7\x8a\xb6\xe6\x80\x81','post_setter': lambda self: self._convert_forbid_states()
                                     },
   ('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self.register_callbacks()
                                  },
   ('use_up_body_bone', 'param'): {'zh_name': '\xe4\xbd\xbf\xe7\x94\xa8\xe4\xb8\x8a\xe5\x8d\x8a\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe4\xbd\x9c\xe4\xb8\xba\xe5\x85\xa8\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c','param_type': 'bool'}})
class AccumulateShootPure(StateBase):
    BIND_EVENT = {'TRY_STOP_WEAPON_ATTACK': 'cancel_shoot'
       }
    STATE_PRE = 0
    STATE_LOOP = 1
    STATE_POST = 2
    PART = UP_BODY
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD, MC_MOVE, MC_JUMP_1}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN2)
        self.force_pre = self.custom_param.get('force_pre', True)
        self.pre_anim_name = self.custom_param.get('pre_anim_name', None)
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 1.0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.loop_anim_name = self.custom_param.get('loop_anim_name', None)
        self.loop_anim_dir_type = self.custom_param.get('loop_anim_dir_type', 1)
        self.post_anim_name = self.custom_param.get('post_anim_name', None)
        self.post_anim_blend_time = self.custom_param.get('post_anim_blend_time', 0.2)
        self.post_anim_duration = self.custom_param.get('post_anim_duration', 1.0)
        self.post_anim_rate = self.custom_param.get('post_anim_rate', 1.0)
        self.post_forbid_states = self.custom_param.get('post_forbid_states', [])
        self.post_break_time = self.custom_param.get('post_break_time', 0.5)
        self.use_up_body_bone = self.custom_param.get('use_up_body_bone', False)
        self.all_anim_name_set = {self.loop_anim_name, self.post_anim_name}
        self.pre_anim_name and self.all_anim_name_set.add(self.pre_anim_name)
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0.0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration, self.on_end_pre)
        self.register_substate_callback(self.STATE_LOOP, 0.0, self.on_begin_loop)
        self.register_substate_callback(self.STATE_POST, 0.0, self.on_begin_post)
        self.register_substate_callback(self.STATE_POST, self.post_break_time, self.on_enable_break_post)
        self.register_substate_callback(self.STATE_POST, self.post_anim_duration, self.on_end_post)

    def _convert_forbid_states(self):
        self.real_post_forbid_states = set()
        for forbid_state in self.post_forbid_states:
            self.real_post_forbid_states.add(desc_2_num[forbid_state])

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateShootPure, self).init_from_dict(unit_obj, bdict, sid, info)
        self.btn_down = False
        self.skill_ended = False
        self.need_clear_black_state = False
        self.read_data_from_custom_param()
        self._convert_forbid_states()

    def action_btn_down(self):
        super(AccumulateShootPure, self).action_btn_down()
        self.btn_down = True
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.check_can_weapon_attack():
            return False
        if self.is_active:
            return True
        self.active_self()
        return True

    def check_can_weapon_attack(self):
        return self.ev_g_check_can_weapon_attack(self.weapon_pos)

    def action_btn_up(self):
        super(AccumulateShootPure, self).action_btn_up()
        self.btn_down = False
        if self.is_active and self.sub_state == self.STATE_LOOP:
            self.sub_state = self.STATE_POST

    def enter(self, leave_states):
        super(AccumulateShootPure, self).enter(leave_states)
        self.acc_skill_ended = False
        self.send_event('E_ACC_SKILL_BEGIN', self.weapon_pos)
        if self.use_up_body_bone and self.PART == UP_BODY:
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        if self.btn_down:
            if self.pre_anim_name:
                self.sub_state = self.STATE_PRE
            else:
                self.sub_state = self.STATE_LOOP
        elif self.force_pre and self.pre_anim_name:
            self.sub_state = self.STATE_PRE
        else:
            self.sub_state = self.STATE_POST
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.cancel_shoot)
        return

    def on_begin_pre(self):
        self.send_event('E_ANIM_RATE', self.PART, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim_name, self.PART, 1)
        self.end_custom_sound('pre')
        self.start_custom_sound('pre')

    def on_end_pre(self):
        if self.btn_down:
            self.sub_state = self.STATE_LOOP
        else:
            self.sub_state = self.STATE_POST

    def on_begin_loop(self):
        self.send_event('E_ANIM_RATE', self.PART, 1.0)
        self.send_event('E_POST_ACTION', self.loop_anim_name, self.PART, self.loop_anim_dir_type, loop=True)
        self.end_custom_sound('hold')
        self.start_custom_sound('hold')

    def _fire(self):
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def on_begin_post(self):
        self.skill_id and self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ACC_SKILL_END', self.weapon_pos)
        self.acc_skill_ended = True
        self._fire()
        self.send_event('E_ANIM_RATE', self.PART, self.post_anim_rate)
        self.send_event('E_POST_ACTION', self.post_anim_name, self.PART, 1, blend_time=self.post_anim_blend_time)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        if self.real_post_forbid_states:
            self.send_event('E_ADD_BLACK_STATE', self.real_post_forbid_states)
            self.need_clear_black_state = True
            if MC_MOVE in self.real_post_forbid_states:
                self.send_event('E_BRAKE')
        self.end_custom_sound('hold')
        self.end_custom_sound('post')
        self.start_custom_sound('post')

    def _clear_black_states(self):
        if self.need_clear_black_state:
            self.send_event('E_CLEAR_BLACK_STATE')
            self.need_clear_black_state = False

    def on_enable_break_post(self):
        self._clear_black_states()
        self.send_event('E_ADD_WHITE_STATE', self.BREAK_POST_STATES, self.sid)

    def on_end_post(self):
        self.disable_self()

    def exit(self, enter_states):
        super(AccumulateShootPure, self).exit(enter_states)
        if not self.acc_skill_ended:
            self.send_event('E_ACC_SKILL_END', self.weapon_pos)
            self.acc_skill_ended = True
        if self.PART == UP_BODY and self.sd.ref_up_body_anim in self.all_anim_name_set:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            if self.use_up_body_bone:
                global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self._clear_black_states()
        self.end_custom_sound('pre')
        self.end_custom_sound('hold')
        self.end_custom_sound('post')

    def cancel_shoot(self):
        if self.is_active:
            self.send_event('E_ACTION_UP', self.bind_action_id)
            self.disable_self()

    def refresh_action_param(self, action_param, custom_param):
        super(AccumulateShootPure, self).refresh_action_param(action_param, custom_param)
        self.custom_param = custom_param
        self.read_data_from_custom_param()
        self._convert_forbid_states()


class AccumulateShootHover(AccumulateShoot):

    def read_data_from_custom_param(self):
        super(AccumulateShootHover, self).read_data_from_custom_param()
        self.check_hover_skill_id = self.custom_param.get('check_hover_skill_id', 800456)

    def action_btn_down(self):
        if super(AccumulateShootHover, self).action_btn_down():
            if not self.ev_g_on_ground() and self.ev_g_can_cast_skill(self.check_hover_skill_id):
                self.ev_g_try_enter(MC_HOVER)
            return True
        return False

    def action_btn_up(self):
        ret = super(AccumulateShootHover, self).action_btn_up()
        if not self.acted and not self.ev_g_on_ground() and self.is_active and MC_HOVER in self.ev_g_cur_state():
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)
        return ret

    def _post_action(self):
        super(AccumulateShootHover, self)._post_action()
        if not self.ev_g_on_ground():
            self.send_event('E_STOP_HOVER')
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)

    def on_in_air(self, is_in_air):
        pass

    def enter(self, leave_states):
        super(AccumulateShootHover, self).enter(leave_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.hold_anim, blend_dir=1)

    def exit(self, enter_states):
        super(AccumulateShootHover, self).exit(enter_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        return

    def check_transitions(self):
        if self.post_cnt > self.post_break_time:
            if self.ev_g_on_ground():
                self.send_event('E_CLEAR_BLACK_STATE')
                self.send_event('E_ADD_WHITE_STATE', {MC_MOVE}, self.sid)
            else:
                if self.ev_g_get_state(MC_JUMP_2):
                    self.send_event('E_RESET_FALL_GRAVITY')
                else:
                    self.send_event('E_ACTIVE_STATE', MC_JUMP_2)
                self.disable_self()
        if self.post_cnt > self.post_time:
            self.disable_self()

    def _end_shoot(self):
        super(AccumulateShootHover, self)._end_shoot()
        if not self.ev_g_on_ground():
            if self.ev_g_get_state(MC_JUMP_2):
                self.send_event('E_RESET_FALL_GRAVITY')
            else:
                self.send_event('E_ACTIVE_STATE', MC_JUMP_2)


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('pre_anim', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c'},('shoot_anim', 'param'): {'zh_name': '\xe5\xb0\x84\xe5\x87\xbb\xe5\x8a\xa8\xe7\x94\xbb'},('post_anim', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c'},('pre_anim_time', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('fire_anim_time', 'param'): {'zh_name': '\xe5\xb0\x84\xe5\x87\xbb\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf'},('post_anim_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'}})
class SequenceShoot(StateBase):
    BIND_EVENT = {'E_FIRE': 'on_fire'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.pre_anim, self.pre_anim_time = self.custom_param.get('pre_anim', (None,
                                                                               0.1))
        self.extern_bone_tree = self.custom_param.get('extern_bone_tree', None)
        self.shoot_anim, self.fire_anim_time = self.custom_param.get('shoot_anim', (None,
                                                                                    0.2))
        self.post_anim, self.post_anim_time = self.custom_param.get('post_anim', (None,
                                                                                  0.2))
        self.anim_part = self.custom_param.get('anim_part', 'upper')
        self.blend_dir = self.custom_param.get('blend_dir', 1)
        self.fire_on_release = self.custom_param.get('fire_on_release', False)
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.is_breakable = self.custom_param.get('is_breakable', False)
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SequenceShoot, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.fired = False
        self.btn_up = False
        self.fired_time, self.last_fired_time = (0, 0)
        self.brake_on_fire = self.anim_part == 'lower'

    def action_btn_down(self):
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if self.is_active:
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_try_weapon_attack_begin(self.weapon_pos):
            if self.fired and self.is_breakable and self.btn_up:
                self.send_event('E_STOP_BATCH_ATTACK', self.weapon_pos)
            return False
        if not self.fire_on_release:
            self.active_self()
        super(SequenceShoot, self).action_btn_down()
        return True

    def action_btn_drag(self):
        pass

    def action_btn_up(self):
        if not self.ev_g_try_weapon_attack_end(self.weapon_pos):
            return False
        if self.fire_on_release:
            self.active_self()
        self.btn_up = True
        super(SequenceShoot, self).action_btn_up()
        return True

    def enter(self, leave_states):
        self.fired_time = 0
        self.post_anim_playing = False
        self.btn_up = False
        self.send_event('E_SET_SECOND_WEAPON_ATTACK', True)
        if self.brake_on_fire:
            self.send_event('E_CLEAR_SPEED')
        else:
            self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_SHOULDER_CANNON_START')
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        super(SequenceShoot, self).enter(leave_states)

        def reset_param():
            if self.shoot_aim_ik:
                self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik)
                self.send_event('E_ENABLE_AIM_IK', True)
                self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time)

        self.delay_call(self.pre_aim_ik_time, reset_param)

    def update(self, dt):
        if self.fired:
            self.fired_time += dt
        super(SequenceShoot, self).update(dt)

    def check_transitions(self):
        if self.fired_time > self.fire_anim_time >= self.last_fired_time:
            if self.post_anim:
                part = LOW_BODY if self.anim_part == 'lower' else UP_BODY
                if self.extern_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.post_anim, True, subtree=self.extern_bone_tree)
                else:
                    self.send_event('E_POST_ACTION', self.post_anim, part, self.blend_dir)
                self.delay_call(self.post_anim_time, self.exit_to_stand)
            else:
                self.disable_self()
        self.last_fired_time = self.fired_time

    def exit_to_stand(self):
        self.disable_self()
        self.send_event('E_ACTIVE_STATE', MC_STAND)

    def exit(self, enter_states):
        super(SequenceShoot, self).exit(enter_states)
        self.fired = False
        if self.extern_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False)
        self.send_event('E_SHOULDER_CANNON_END')
        self.send_event('E_SET_SECOND_WEAPON_ATTACK', False)
        if not self.brake_on_fire:
            self.send_event('E_SLOW_DOWN', False)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        return

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        if weapon_pos != self.weapon_pos:
            return
        if not (self.is_active or self.check_can_active()):
            return
        if self.shoot_anim:
            if self.extern_bone_tree:
                self.send_event('E_POST_EXTERN_ACTION', self.shoot_anim, True, subtree=self.extern_bone_tree, force_trigger_effect=True)
            else:
                part = LOW_BODY if self.anim_part == 'lower' else UP_BODY
                self.send_event('E_POST_ACTION', self.shoot_anim, part, self.blend_dir, blend_time=0, force_trigger_effect=True)
        self.fired = True
        self.fired_time = 0
        self.fire_anim_time = f_cdtime + 0.05
        self.send_event('E_PLAY_CAMERA_TRK', 'SHOULDER_CANNON')
        if not self.is_active and not self.fire_on_release:
            self.active_self()

    def refresh_action_param(self, action_param, custom_param):
        super(SequenceShoot, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()


@editor.state_exporter({('extern_enter_blend_time', 'param'): {'zh_name': '\xe8\xbf\x9b\xe5\x85\xa5\xe5\xa4\x96\xe9\xaa\xa8\xe9\xaa\xbc\xe5\x8a\xa8\xe4\xbd\x9c\xe8\x9e\x8d\xe5\x90\x88\xe6\x97\xb6\xe9\x97\xb4'},('extern_exit_blend_time', 'param'): {'zh_name': '\xe9\x80\x80\xe5\x87\xba\xe5\xa4\x96\xe9\xaa\xa8\xe9\xaa\xbc\xe5\x8a\xa8\xe4\xbd\x9c\xe8\x9e\x8d\xe5\x90\x88\xe6\x97\xb6\xe9\x97\xb4'}})
class Reload(StateBase):
    BIND_EVENT = {'E_CHANGE_WEAPON_POS': 'on_reload_weapon_pos',
       'E_TEMP_CHANGE_WEAPON_POS': 'on_reload_weapon_pos',
       'E_RECOVER_WEAPON_POS_CHANGE': 'recover_weapon_pos_change',
       'E_RELOADING': 'on_reloading_bullet',
       'E_WEAPON_BULLET_CHG': 'on_reloaded',
       'E_IGNORE_RELOAD_ANIM': 'on_ignore_reload_anim',
       'G_RELOADING': 'on_reloading',
       'E_WEAPON_CHANGED': 'on_weapon_change',
       'E_RESET_RELOAD_STATE': 'on_reset_reload_state'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.continue_fire = False
        self.reloaded = True
        self.ignore_anim = False

    def read_data_from_custom_param(self):
        self.slow_on_reload = self.custom_param.get('slow_on_reload', True)
        self.reload_anim = self.custom_param.get('reload_anim', None)
        self.extern_bone_tree = self.custom_param.get('extern_bone_tree', None)
        self.sub_bone_tree = self.custom_param.get('sub_bone_tree', None)
        self.reload_anim_dir = self.custom_param.get('reload_anim_dir', 1)
        self.extern_enter_blend_time = self.custom_param.get('extern_enter_blend_time')
        self.extern_exit_blend_time = self.custom_param.get('extern_exit_blend_time')
        self.need_reset_reloaded_when_transform = self.custom_param.get('need_reset_reloaded_when_transform', True)
        self.anim_time = self.custom_param.get('anim_duration', 2)
        self.reload_time = self.custom_param.get('reload_time', self.anim_time)
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.use_up_anim_bone = self.custom_param.get('use_up_anim_bone', None)
        self.use_up_anim_states = deepcopy(self.custom_param.get('use_up_anim_states', []))
        status_desc_2_num = character_ctrl_utils.get_status_desc_2_num(self)
        for i in range(len(self.use_up_anim_states)):
            self.use_up_anim_states[i] = status_desc_2_num[self.use_up_anim_states[i]]

        return

    def on_reload_weapon_pos(self, weapon_pos):
        self.weapon_pos = weapon_pos

    def recover_weapon_pos_change(self):
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN1)

    def on_ignore_reload_anim(self, ignore):
        self.ignore_anim = ignore

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.reloaded:
            return False
        if self.ev_g_aim_switching():
            return
        self.send_event('E_TRY_RELOAD', self.weapon_pos)
        super(Reload, self).action_btn_down()
        return True

    def on_reloading_bullet(self, time, times, weapon_pos):
        if weapon_pos != self.weapon_pos:
            return
        self.reload_time = time
        if not self.ignore_anim:
            self.active_self()

    def refresh_action_param(self, action_param, custom_param):
        super(Reload, self).refresh_action_param(action_param, custom_param)
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False, blend_time=self.extern_exit_blend_time)
        if custom_param:
            self.custom_param = custom_param
            old_weapon_pos = self.weapon_pos
            self.read_data_from_custom_param()
            if self.weapon_pos != old_weapon_pos and self.need_reset_reloaded_when_transform:
                self.reloaded = True
        return

    def enter(self, leave_states):
        super(Reload, self).enter(leave_states)
        self.continue_fire = False
        self.reloaded = False
        self.send_event('E_SLOW_DOWN', self.slow_on_reload, state='Reload')
        self.timer_rate = self.anim_time / self.reload_time
        self.sync_timer_rate_to_anim(True)
        self.send_event('E_BEGIN_RELOAD')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_BEGIN_RELOAD, ()))
        self.play_anim()

    def play_anim(self):
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, self.use_up_anim_bone)
        if self.bind_action_id:
            self.send_event('E_START_ACTION_CD', self.bind_action_id, self.reload_time)
        if self.reload_anim:
            if self.extern_bone_tree:
                self.send_event('E_POST_EXTERN_ACTION', self.reload_anim, True, subtree=self.extern_bone_tree, timeScale=self.timer_rate, blend_time=self.extern_enter_blend_time)
            else:
                self.send_event('E_POST_ACTION', self.reload_anim, UP_BODY, self.reload_anim_dir, timeScale=self.timer_rate)
                if self.sub_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.reload_anim, True, subtree=self.sub_bone_tree, timeScale=self.timer_rate, blend_time=self.extern_enter_blend_time)

    def update(self, dt):
        super(Reload, self).update(dt)

    def check_transitions(self):
        if self.reloaded:
            self.disable_self()
        continue_fire, _ = self.ev_g_continue_fire() or (False, None)
        if continue_fire:
            return MC_SHOOT
        else:
            return

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        self.reloaded = True
        continue_fire, fire_weapon_pos = self.ev_g_continue_fire() or (False, None)
        if continue_fire and fire_weapon_pos == weapon_pos:
            if self.ev_g_try_weapon_attack_begin(self.weapon_pos):
                self.continue_fire = True
        return

    def on_weapon_change(self, weapon_pos):
        self.reloaded = True

    def on_reset_reload_state(self):
        self.reloaded = True

    def on_reloading(self):
        return not self.reloaded

    def exit(self, enter_states):
        super(Reload, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False, state='Reload')
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, None)
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if not self.continue_fire:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False, blend_time=self.extern_exit_blend_time)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, None)
        return


class ShootModeChange(StateBase):
    BIND_EVENT = {'E_WPBAR_INIT': 'set_shoot_mode',
       'G_SHOOT_MODE': 'get_shoot_mode',
       'E_INIT_SHOOT_MODE': 'init_shoot_mode',
       'E_WEAPON_CHANGED': 'reset_shoot_mode'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(ShootModeChange, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.changing = False
        self.ch_wp_pos = self.custom_param['weapon_pos']
        self.change_conf = self.custom_param['change_conf']
        self.track_conf = self.custom_param['show_track']
        self.cur_mode = bdict.get('shoot_mode', m_const.MECHA_SHOOT_QUICK)
        self.show_track = self.track_conf[self.cur_mode]
        self.is_changing = False

    def init_shoot_mode(self):
        if self.ev_g_is_avatar():
            self.cur_mode = m_const.MECHA_SHOOT_QUICK
            self.set_shoot_mode()

    def set_shoot_mode(self):
        if self.ev_g_is_avatar():
            self.send_event('E_ON_SHOOT_MODE_CHANGED', self.cur_mode)
            self.show_track = self.track_conf[self.cur_mode]
            self.set_wp_conf()
            self.send_event('E_SET_TRACK_DATA', self.show_track, self.ch_wp_pos)
            if self.show_track:
                self.send_event('E_SHOW_WP_TRACK')
            else:
                self.send_event('E_STOP_WP_TRACK')

    def reset_shoot_mode(self, cur_put_pos):
        self.send_event('E_STOP_WP_TRACK')
        self.show_track = self.track_conf[self.cur_mode]
        self.set_wp_conf()
        self.send_event('E_SET_TRACK_DATA', self.show_track, self.ch_wp_pos)
        if self.show_track:
            self.send_event('E_SHOW_WP_TRACK')

    def get_shoot_mode(self):
        return self.cur_mode

    def set_wp_conf(self):
        wp_effective_conf = self.change_conf.get(self.cur_mode, {})
        for key, value in six.iteritems(wp_effective_conf):
            if key == 'iControl':
                if value == w_const.CONTROL_MODEL_BEGIN:
                    self.send_event('E_SET_FIRE_ON_RELEASE', False)
                else:
                    self.send_event('E_SET_FIRE_ON_RELEASE', True)
            weapon = self.sd.ref_wp_bar_mp_weapons.get(self.ch_wp_pos)
            if weapon:
                effect_conf = weapon.get_effective_config()
                effect_conf[key] = value

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if self.is_changing:
            return
        self.is_changing = True
        self.cur_mode = m_const.MECHA_SHOOT_QUICK if self.cur_mode == m_const.MECHA_SHOOT_NORMAL else m_const.MECHA_SHOOT_NORMAL
        self.send_event('E_CALL_SYNC_METHOD', 'mecha_mode_change', (self.cur_mode,), True)
        self.show_track = self.track_conf[self.cur_mode]
        self.set_shoot_mode()
        super(ShootModeChange, self).action_btn_down()
        return True

    def action_btn_up(self):
        self.is_changing = False
        super(ShootModeChange, self).action_btn_up()
        return True

    def exit(self, enter_states):
        self.send_event('E_STOP_WP_TRACK')
        super(ShootModeChange, self).exit(enter_states)

    def destroy(self):
        self.send_event('E_STOP_WP_TRACK')
        super(ShootModeChange, self).destroy()