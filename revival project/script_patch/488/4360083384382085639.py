# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8036.py
from __future__ import absolute_import
from .StateBase import StateBase, clamp
from .MoveLogic import Run
from .ShootLogic import AccumulateShootPure, WeaponFire, Reload
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN5, PART_WEAPON_POS_MAIN4, PART_WEAPON_POS_MAIN6
from logic.gcommon.editor import state_exporter
import six
import math3d
import world
import math
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_9
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
from logic.gcommon import time_utility as tutil

def __editor_exlposive_dash_postsetter(self):
    self.register_callbacks()


class Run8036(Run):

    def read_data_from_custom_param(self):
        super(Run8036, self).read_data_from_custom_param()
        self.is_enter_run_stop = False
        self.stop_anim_cost_time = self.custom_param.get('stop_anim_cost_time', 3.0)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        self.enter_run_time_stamp = tutil.time() - 999.0
        super(Run8036, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def enter(self, leave_states):
        super(Run8036, self).enter(leave_states)
        self.sd.ref_forbid_zero_anim_dir = False

    def begin_run_anim(self):
        self.enter_run_time_stamp = tutil.time()
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        if self.forbid_default_up_body_anim:
            if self.ev_g_is_showing_default_up_body_anim():
                self.send_event('E_POST_ACTION', self.run_anim, UP_BODY, 7, loop=True, ignore_sufix=self.run_ignore_sufix)
            if not self.keep_default_up_body_anim:
                self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.run_anim, 7)
        self.send_event('E_POST_ACTION', self.run_anim, LOW_BODY, self.run_anim_dir_type, loop=True, ignore_sufix=self.run_ignore_sufix, yaw_list=self.run_anim_yaw_list, keep_phase=True)

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
        if tutil.time() - self.enter_run_time_stamp > self.stop_anim_cost_time and not self.is_enter_run_stop:
            self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
            self.is_enter_run_stop = True
        if self.is_enter_run_stop and rocker_dir and not rocker_dir.is_zero:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', rocker_dir.x, rocker_dir.z)
        cur_speed = self.sd.ref_cur_speed
        speed_scale = self.ev_g_get_speed_scale() or 1
        max_speed = speed_scale * self.run_speed
        acc = rocker_dir and not rocker_dir.is_zero
        cur_speed += dt * (self.move_acc if acc and can_run else self.brake_acc)
        cur_speed = clamp(cur_speed, 0, max_speed)
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_MOVE', rocker_dir)
        if self.enable_dynamic_speed_rate and self.sub_state == self.STATE_RUN:
            self.send_event('E_ANIM_RATE', LOW_BODY, cur_speed / self.run_speed * self.dynamic_speed_rate)
        return

    def exit(self, enter_states):
        super(Run8036, self).exit(enter_states)
        if self.is_enter_run_stop:
            self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
        self.is_enter_run_stop = False
        self.sd.ref_forbid_zero_anim_dir = True

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if not self.is_enter_run_stop:
            if not self.sd.ref_rocker_dir:
                self.end_run_stop_anim()
            return
        if self.sd.ref_rocker_dir:
            return
        super(Run8036, self).begin_run_stop_anim()


class Reload8036(Reload):

    def enter(self, leave_states):
        super(Reload8036, self).enter(leave_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.action_trigger_data[0][1][0], loop=False)

    def exit(self, enter_states):
        super(Reload8036, self).exit(enter_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        return


class WeaponFire8036(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACCUMULATE_DURATION_CHANGED': 'on_energy_change',
       'E_ANIMATOR_LOADED': ('on_load_animator_complete', 99),
       'E_WEAPON_RECHARGE_FINISH': 'on_recharge_finish',
       'E_FIRE_END': 'on_fire_end',
       'E_SET_SHOOT_IK_ENABLE': 'on_set_shoot_ik_enable',
       'E_RELOADING': 'on_reloading_bullet'
       })

    def on_post_init_complete(self, *args):
        super(WeaponFire8036, self).on_post_init_complete(*args)
        self.normal_shoot_anim = self.shoot_anim
        self.fire_weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        self.send_event('E_BEGIN_WEAPON_ACCUMULATE', self.weapon_pos)
        self.max_accumulate_time = self.fire_weapon.get_accumulate_max_time()
        effect_config = {'weapon_pos': self.weapon_pos,'args': {'free_accumulate_max_time': self.max_accumulate_time}}
        self.send_event('E_ADD_WP_CUSTOM_PARAM', None, None, effect_config)
        self.all_shoot_anim.update({self.accumulate_shoot_anim, 'vice_attack_02_turn_f', 'vice_attack_02_turn_b', 'vice_attack_02_turn_br',
         'vice_attack_02_turn_bl', 'vice_attack_02_turn_fr', 'vice_attack_02_turn_fl'})
        self.normal_shoot_ik = self.shoot_aim_ik
        self.dash_shoot_ik = ('aim', ['biped r upperarm'])
        return

    def read_data_from_custom_param(self):
        super(WeaponFire8036, self).read_data_from_custom_param()
        self.extra_weapon_pos = self.custom_param.get('extra_weapon_pos', PART_WEAPON_POS_MAIN6)
        self.accumulate_shoot_anim = self.custom_param.get('accumulate_shoot_anim', 'shoot_cluster')

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8036, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.sd.ref_turn_dir = 0.0

    def enter(self, leave_states):
        super(WeaponFire8036, self).enter(leave_states)
        if not self.sd.ref_in_dash_drag:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.shoot_anim, loop=False)

    def exit(self, enter_states):
        super(WeaponFire, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire')
        self.fired = False
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        if not self.sd.ref_in_dash_drag:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        self.send_event('E_POST_EXTERN_ACTION', None, False, level=1)
        return

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        super(WeaponFire8036, self).on_fire(f_cdtime, weapon_pos, fired_socket_index)
        if weapon_pos != self.weapon_pos:
            return
        self.ev_g_try_weapon_attack_begin(self.extra_weapon_pos)
        self.ev_g_try_weapon_attack_end(self.extra_weapon_pos)

    def _reset_aim_ik_param(self):
        if not self.sd.ref_in_dash_drag:
            self.shoot_aim_ik = self.normal_shoot_ik
        else:
            self.shoot_aim_ik = self.dash_shoot_ik
        self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, self.support_exit_aim_ik_lerp)
        self.send_event('E_ENABLE_AIM_IK', True, self.aim_ik_pitch_limit)
        self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.exit_aim_ik_lerp_time)

    def on_reloading_bullet(self, time, times, weapon_pos):
        if weapon_pos != self.weapon_pos:
            return
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def action_btn_up(self):
        self.is_continue_fire = False
        self.want_to_fire = False
        super(WeaponFire, self).action_btn_up()
        return True

    def check_transitions(self):
        if self.fired_time > self.fire_anim_time:
            self.disable_self()
        return super(WeaponFire8036, self).check_transitions()

    def on_set_shoot_ik_enable(self, enable):
        self.forbid_ik = not enable

    def play_fire_anim(self, fired_socket_index):
        if self.shoot_anim and (self.is_active or self.check_can_active()):
            if not self.sd.ref_in_dash_drag and not self.ev_g_on_ground():
                ignore_sufix = True
            else:
                ignore_sufix = False
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
                    if not self.sd.ref_in_dash_drag:
                        self.send_event('E_ANIM_RATE', part, self.shoot_anim_rate)
                        self.send_event('E_POST_ACTION', self.shoot_anim, part, self.anim_blend_type, blend_time=self.blend_time, force_trigger_effect=True, socket_index=fired_socket_index, ignore_sufix=ignore_sufix)
                    else:
                        model = self.ev_g_model()
                        if model and model.valid and model.has_anim('vice_attack_02_turn_f'):
                            dir_x = self.sd.ref_anim_param['dir_x']
                            dir_y = self.sd.ref_anim_param['dir_y']
                            anim_list = self.get_air_shoot_anim()
                            self.send_event('E_POST_ANIM_LIST_ACTION', anim_list, abs(dir_x) * self.sd.ref_turn_dir, abs(dir_y) * self.sd.ref_turn_dir)
                            self.send_event('E_POST_EXTERN_ACTION', self.shoot_anim, True, subtree=(('biped root', 0), ('biped r upperarm', 1)), loop=False, blend_time=0, level=1)
                if self.sub_bone_tree:
                    self.send_event('E_POST_EXTERN_ACTION', self.shoot_anim, True, subtree=self.sub_bone_tree)
                if self.shoot_anim_index != -1:
                    self.shoot_anim_index = (self.shoot_anim_index + 1) % self.shoot_anim_count
                    self.shoot_anim = self._nl_shoot_anim[self.shoot_anim_index]

    def on_fire_end(self, weapon_pos):
        if weapon_pos != self.weapon_pos:
            return
        self.shoot_anim = self.normal_shoot_anim
        self.ev_g_try_weapon_attack_end(self.weapon_pos, False)

    def get_air_shoot_anim(self):
        if self.sd.ref_anim_param is None:
            return ('vice_attack_02_turn_f', 'vice_attack_02_turn_f')
        else:
            dir_x = self.sd.ref_anim_param['dir_x']
            dir_y = self.sd.ref_anim_param['dir_y']
            anim_list = []
            if dir_x > 0:
                if dir_y > 0:
                    anim_list = ('vice_attack_02_turn_f', 'vice_attack_02_turn_fr')
                else:
                    anim_list = ('vice_attack_02_turn_b', 'vice_attack_02_turn_br')
            elif dir_x == 0:
                if dir_y > 0:
                    anim_list = ('vice_attack_02_turn_f', 'vice_attack_02_turn_f')
                else:
                    anim_list = ('vice_attack_02_turn_b', 'vice_attack_02_turn_b')
            elif dir_y > 0:
                anim_list = ('vice_attack_02_turn_f', 'vice_attack_02_turn_fl')
            else:
                anim_list = ('vice_attack_02_turn_b', 'vice_attack_02_turn_bl')
            if abs(dir_x) > abs(dir_y):
                return anim_list[::-1]
            return anim_list

    def on_recharge_finish(self):
        self.shoot_anim = self.accumulate_shoot_anim


@state_exporter({('enter_recharge_delay_time', 'param'): {'zh_name': '\xe5\xb0\x84\xe5\x87\xbb\xe5\x90\x8e\xe9\x87\x8d\xe6\x96\xb0\xe8\xbf\x9b\xe5\x85\xa5\xe5\x85\x85\xe8\x83\xbd\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                            },
   ('recharge_anim_time', 'param'): {'zh_name': '\xe5\x85\x85\xe8\x83\xbd\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                     }
   })
class WeaponRecharge(StateBase):
    BIND_EVENT = {'E_FIRE_END': 'on_fire',
       'E_RELOADING': 'on_reloading_bullet',
       'E_WEAPON_BULLET_CHG': 'on_reloaded',
       'E_ACCUMULATE_DURATION_CHANGED': 'on_energy_change',
       'G_AUTO_ENERGY': 'get_accumulate_energy',
       'E_ANIMATOR_LOADED': ('on_animator_loaded', 999)
       }
    STATE_SHOOT_ENTER_RECHAGRE = 1
    STATE_FORCE_ENTER_RECHARGE = 2
    STATE_WAIT_ENTER_RECHARGE = 3
    STATE_RECHARGING = 4
    STATE_FINISH_RECHARGE = 5

    def on_post_init_complete(self, bidct):
        super(WeaponRecharge, self).on_post_init_complete(bidct)
        self.fire_weapon = self.sd.ref_wp_bar_mp_weapons.get(self.recharge_weapon_pos)
        self.max_accumulate_time = self.fire_weapon.get_accumulate_max_time()

    def read_data_from_custom_param(self):
        self.recharge_weapon_pos = self.custom_param.get('recharge_weapon_pos', PART_WEAPON_POS_MAIN1)
        self.recharge_enter_delay_time = self.custom_param.get('enter_recharge_delay_time', 0.8)
        self.recharge_anim_time = self.custom_param.get('recharge_anim_time', 0.667)
        self.recharge_anim = self.custom_param.get('recharge_anim', 'gun_charging')
        self.recharge_finish_anim = self.custom_param.get('recharge_finish_anim', 'gun_ready')
        self.recharge_extern_bone_tree = self.custom_param.get('recharge_extern_bone_tree', (('biped root', 0), ('bone_wp_r_root', 1)))

    def register_callbacks(self):
        self.register_substate_callback(self.STATE_FORCE_ENTER_RECHARGE, 0.0, self.on_begin_recharge_anim)
        self.register_substate_callback(self.STATE_SHOOT_ENTER_RECHAGRE, self.recharge_enter_delay_time, self.on_begin_recharge_anim)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(WeaponRecharge, self).init_from_dict(unit_obj, bdict, sid, info)
        self.last_energy = 0.0
        self.recharge_start = False
        self.read_data_from_custom_param()
        self.register_callbacks()

    def enter(self, leave_states):
        super(WeaponRecharge, self).enter(leave_states)

    def get_accumulate_energy(self):
        return (
         PART_WEAPON_POS_MAIN1, self.last_energy)

    def on_fire(self, weapon_pos):
        if weapon_pos != self.recharge_weapon_pos:
            return
        if self.sub_state == self.STATE_SHOOT_ENTER_RECHAGRE:
            self.reset_sub_state_timer()
        else:
            self.sub_state = self.STATE_SHOOT_ENTER_RECHAGRE
        self.on_disable_recharge_anim()
        self.active_self()

    def on_reloading_bullet(self, time, times, weapon_pos):
        if weapon_pos != self.recharge_weapon_pos:
            return
        self.sub_state = self.STATE_WAIT_ENTER_RECHARGE
        self.on_disable_recharge_anim()

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        if weapon_pos != self.recharge_weapon_pos:
            return
        self.sub_state = self.STATE_FORCE_ENTER_RECHARGE
        self.send_event('E_REFRESH_SPREAD_AIM_UI')
        self.reset_sub_state_timer()
        self.active_self()

    def on_disable_recharge_anim(self):
        self.last_energy = 0.0
        self.end_custom_sound('recharge')
        self.send_event('E_TRIGGER_FREE_ACCUMULATE', self.recharge_weapon_pos, None)
        self.send_event('E_POST_EXTERN_ACTION', None, False, level=2)
        self.send_event('E_END_WEAPON_ACCUMULATE', self.recharge_weapon_pos)
        self.send_event('E_DISABLE_WEAPON_ACCUMULATE', self.recharge_weapon_pos, True)
        self.send_event('E_HIDE_FINISH_ENERGY_EFFECT')
        return

    def on_begin_recharge_anim(self):
        self.sub_state = self.STATE_RECHARGING
        self.start_custom_sound('recharge')
        self.send_event('E_TRIGGER_FREE_ACCUMULATE', self.recharge_weapon_pos, 1)
        self.send_event('E_ATTACK_END', self.recharge_weapon_pos)
        self.send_event('E_POST_EXTERN_ACTION', self.recharge_anim, True, subtree=self.recharge_extern_bone_tree, loop=False, level=2)
        self.send_event('E_ANIM_RATE', EXTERN_BODY_1, self.recharge_anim_time / self.max_accumulate_time)
        self.send_event('E_DISABLE_WEAPON_ACCUMULATE', self.recharge_weapon_pos, False)
        self.send_event('E_BEGIN_WEAPON_ACCUMULATE', self.recharge_weapon_pos)

    def on_energy_change(self, weapon_pos, cur_energy, touch_energy):
        if weapon_pos != self.recharge_weapon_pos:
            return
        if cur_energy == 0.0:
            pass
        if not self.fire_weapon:
            return
        if self.sub_state != self.STATE_RECHARGING:
            return
        if self.last_energy < self.max_accumulate_time and cur_energy >= self.max_accumulate_time:
            self.on_finish_recharge_anim()
        self.last_energy = cur_energy

    def on_animator_loaded(self, *args):
        self.on_finish_recharge_anim()

    def on_finish_recharge_anim(self):
        self.sub_state = self.STATE_FINISH_RECHARGE
        self.send_event('E_WEAPON_RECHARGE_FINISH')
        self.send_event('E_POST_EXTERN_ACTION', self.recharge_finish_anim, True, subtree=self.recharge_extern_bone_tree, loop=False, level=2)
        self.send_event('E_SHOW_FINISH_ENERGY_EFFECT')
        self.send_event('E_REFRESH_SPREAD_AIM_UI')
        self.end_custom_sound('recharge_finish')
        self.start_custom_sound('recharge_finish')
        self.disable_self()


class AccumulateShoot8036(AccumulateShootPure):
    BIND_EVENT = AccumulateShootPure.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACCUMULATE_DURATION_CHANGED': 'on_energy_change'
       })
    BREAK_POST_STATES = set([])

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateShoot8036, self).init_from_dict(unit_obj, bdict, sid, info)
        self.fire_weapon = None
        self.last_energy = 0.0
        self.energy_stage_func = {0: self.on_accumulate_mid,
           1: self.on_accumulate_full
           }
        return

    def read_data_from_custom_param(self):
        super(AccumulateShoot8036, self).read_data_from_custom_param()
        self.extern_bone_tree = self.custom_param.get('extern_bone_tree', {})
        self.normal_post_anim_name = self.post_anim_name
        self.full_post_anim_name = self.custom_param.get('full_post_anim_name', 'shoot_cluster')
        self.extern_bone_pre_time = self.custom_param.get('extern_bone_pre_time', 0.667)
        self.extern_bone_pre_anim = self.custom_param.get('extern_bone_pre_anim', None)
        self.extern_bone_loop_anim = self.custom_param.get('extern_bone_loop_anim', None)
        self.all_anim_name_set.add(self.full_post_anim_name)
        return

    def on_post_init_complete(self, *args):
        super(AccumulateShoot8036, self).on_post_init_complete(*args)
        self.fire_weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN1)

    def action_btn_down(self):
        super(AccumulateShootPure, self).action_btn_down()
        self.btn_down = True
        if self.is_active:
            return False
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if self.ev_g_reloading():
            return False
        if self.ev_g_weapon_reloading(self.weapon_pos):
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        self.active_self()
        return True

    def on_accumulate_full(self):
        self.post_anim_name = self.full_post_anim_name

    def on_accumulate_mid(self):
        pass

    def on_energy_change(self, weapon_pos, cur_energy, touch_energy):
        if weapon_pos != self.weapon_pos:
            return
        else:
            if not self.fire_weapon:
                return
            acc_level = self.fire_weapon.get_acc_levels()
            for i in range(len(acc_level)):
                if cur_energy >= acc_level[i] and self.last_energy < acc_level[i]:
                    func = self.energy_stage_func.get(i, None)
                    if func:
                        func()

            self.last_energy = cur_energy
            return

    def enter(self, leave_states):
        super(AccumulateShoot8036, self).enter(leave_states)
        self.post_anim_name = self.normal_post_anim_name
        if self.extern_bone_tree:
            self.send_event('E_UPBODY_BONE', self.extern_bone_tree['enter'], EXTERN_BODY_1)
            if self.fire_weapon:
                max_accumulate_time = self.fire_weapon.get_accumulate_max_time()
                self.send_event('E_ANIM_RATE', EXTERN_BODY_1, self.extern_bone_pre_time / max_accumulate_time)

    def on_begin_pre(self):
        super(AccumulateShoot8036, self).on_begin_pre()
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)

    def on_begin_post(self):
        super(AccumulateShoot8036, self).on_begin_post()
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_ANIM_RATE', EXTERN_BODY_1, 1.0)

    def exit(self, enter_states):
        super(AccumulateShoot8036, self).exit(enter_states)
        self.last_energy = 0

    def _fire(self):
        self.ev_g_try_weapon_attack_end(self.weapon_pos)


@state_exporter({('roll_speed', 'meter'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                             },
   ('roll_dec_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x87\x8f\xe9\x80\x9f\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                },
   ('roll_dec_value', 'meter'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x8c\x80\xe5\x87\x8f\xe9\x80\x9f\xe6\x95\xb0\xe5\x80\xbc'},('roll_anim_rate', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                 },
   ('roll_anim_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                 },
   ('roll_shoot_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\xb0\x84\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                  },
   ('roll_end_anim_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe5\xb8\xb8','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                     },
   ('roll_end_anim_rate', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                     },
   ('roll_break_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                  },
   ('roll_ghost_show_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe6\xae\x8b\xe5\xbd\xb1\xe5\x87\xba\xe7\x8e\xb0\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                       },
   ('roll_ghost_hide_time', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe6\xae\x8b\xe5\xbd\xb1\xe6\xb6\x88\xe5\xa4\xb1\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                       },
   ('roll_ghost_anim_start_time', 'param'): {'zh_name': '\xe6\xae\x8b\xe5\xbd\xb1\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe5\x90\xaf\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'},('dash_dec_value', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe5\x8c\x80\xe5\x87\x8f\xe9\x80\x9f\xe6\x95\xb0\xe5\x80\xbc'},('dash_dec_time', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe5\x87\x8f\xe9\x80\x9f\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                },
   ('dash_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                             },
   ('dash_time', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe6\x80\xbb\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                            },
   ('dash_shoot_time', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe5\xb0\x84\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                  },
   ('dash_anim_rate', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                 }
   })
class Roll8036(StateBase):
    ROLL_NONE = 0
    ROLL_START = 1
    ROLL_END = 2
    ROLL_SHOOT = 3
    DASH_START = 4
    DASH_END = 6
    ROLL = 'roll'
    DASH = 'dash'
    BIND_EVENT = {'E_SKILL_BUTTON_BOUNDED': 'on_skill_button_bounded'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Roll8036, self).init_from_dict(unit_obj, bdict, sid, info)
        self.start_dec = False
        self.dec_time = 0
        self.enter_state = self.ROLL
        self.enhanced_by_module = bdict.get('enhanced_by_module', False)
        self.force_dir_anim = ''
        self.read_data_from_custom_param()
        self.register_callbacks()

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 803654)
        self.sub_skill_id = self.custom_param.get('sub_skill_id', 803655)
        self.roll_end_weapon_pos = self.custom_param.get('roll_end_weapon_pos', PART_WEAPON_POS_MAIN5)
        self.roll_speed = self.custom_param.get('roll_speed', 20.0) * NEOX_UNIT_SCALE
        self.roll_anim = self.custom_param.get('roll_anim', 'dash')
        self.roll_dec_time = self.custom_param.get('roll_dec_time', 0.5)
        self.roll_dec_value = self.custom_param.get('roll_dec_value', 15.0) * NEOX_UNIT_SCALE
        self.roll_anim_time = self.custom_param.get('roll_anim_time', 1.167)
        self.roll_anim_rate = self.custom_param.get('roll_anim_rate', 1.0)
        self.roll_shoot_time = self.custom_param.get('roll_shoot_time', 0.8)
        self.roll_end_anim = self.custom_param.get('roll_end_anim', 'dash_end')
        self.roll_end_anim_time = self.custom_param.get('roll_end_anim_time', 0.633)
        self.roll_end_anim_rate = self.custom_param.get('roll_end_anim_rate', 1.0)
        self.roll_break_time = self.custom_param.get('roll_break_time', 0.2)
        self.roll_ghost_show_time = self.custom_param.get('roll_ghost_show_time', 0.3)
        self.roll_ghost_hide_time = self.custom_param.get('roll_ghost_hide_time', 0.6)
        self.roll_ghost_anim_start_time = self.custom_param.get('roll_ghost_anim_start_time', 0.3)
        self.dash_speed = self.custom_param.get('dash_speed', 20.0) * NEOX_UNIT_SCALE
        self.dash_anim = self.custom_param.get('dash_anim', 'dash_air')
        self.dash_anim_time = self.custom_param.get('dash_time', 1.167)
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1.0)
        self.dash_shoot_time = self.custom_param.get('dash_shoot_time', 0.8)
        self.dash_dec_time = self.custom_param.get('dash_dec_time', 0.2)
        self.dash_dec_value = self.custom_param.get('dash_dec_value', 15.0) * NEOX_UNIT_SCALE
        self.extra_weapon_pos = self.custom_param.get('extra_weapon_pos', PART_WEAPON_POS_MAIN6)

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.ROLL_START, 0.0, self.on_roll_start)
        self.register_substate_callback(self.ROLL_START, self.roll_dec_time, self.on_roll_dec)
        self.register_substate_callback(self.ROLL_START, self.roll_ghost_show_time, self.on_roll_ghost_show)
        self.register_substate_callback(self.ROLL_START, self.roll_ghost_hide_time, self.on_roll_ghost_hide)
        self.register_substate_callback(self.ROLL_START, self.roll_shoot_time, self.on_roll_shoot)
        self.register_substate_callback(self.ROLL_START, self.roll_anim_time, self.on_roll_end)
        self.register_substate_callback(self.ROLL_END, 0.0, self.on_roll_end_start)
        self.register_substate_callback(self.ROLL_END, self.roll_break_time, self.on_roll_break)
        self.register_substate_callback(self.ROLL_END, self.roll_end_anim_time, self.on_roll_end_end)
        self.register_substate_callback(self.DASH_START, 0.0, self.on_dash_start)
        self.register_substate_callback(self.DASH_START, self.dash_dec_time, self.on_dash_dec)
        self.register_substate_callback(self.DASH_START, self.dash_shoot_time, self.on_dash_shoot)
        self.register_substate_callback(self.DASH_START, self.dash_anim_time, self.on_dash_end)

    def on_skill_button_bounded(self, skill_id):
        if skill_id != self.skill_id or self.enhanced_by_module:
            return
        self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)

    def action_btn_down(self):
        super(Roll8036, self).action_btn_down()
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        return True

    def check_can_cast_skill(self):
        if not self.skill_id:
            return True
        return self.ev_g_can_cast_skill(self.skill_id) and (self.enhanced_by_module or not self.enhanced_by_module and self.ev_g_can_cast_skill(self.sub_skill_id))

    def enter(self, leave_states):
        super(Roll8036, self).enter(leave_states)
        if self.ev_g_on_ground():
            self.sub_state = self.ROLL_START
        else:
            self.sub_state = self.DASH_START
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_SKILL', self.sub_skill_id)

    def get_roll_dir(self):
        rocker_dir = self.sd.ref_rocker_dir
        if not rocker_dir or rocker_dir.is_zero:
            rocker_dir = math3d.vector(0, 0, 1)
        return rocker_dir

    def refresh_param_changed(self):
        if self.enhanced_by_module:
            self.send_event('E_DEL_ACTION_SUB_SKILL_ID', self.bind_action_id)
        else:
            self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)

    def on_shoot(self):
        self.ev_g_try_weapon_attack_begin(self.roll_end_weapon_pos)
        self.ev_g_try_weapon_attack_end(self.roll_end_weapon_pos)
        self.ev_g_try_weapon_attack_begin(self.extra_weapon_pos)
        self.ev_g_try_weapon_attack_end(self.extra_weapon_pos)

    def on_roll_start(self):
        self.enter_state = self.ROLL
        self.sd.ref_cur_speed = self.roll_speed
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
        self.roll_dir = self.get_roll_dir()
        self.force_dir_anim = self.roll_anim + self.get_anim_dir_force()
        self.send_event('E_POST_ACTION', self.roll_anim, LOW_BODY, 8, loop=False)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.roll_anim_rate)
        self.send_event('E_MOVE', self.roll_dir)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', self.roll_dir.x, self.roll_dir.z)
        self.start_custom_sound(self.force_dir_anim)
        self.end_custom_sound(self.force_dir_anim)
        self.on_update_aim_help_state(True)

    def get_anim_dir_force(self):
        if self.roll_dir.x > 0 and abs(self.roll_dir.z) <= self.roll_dir.x:
            return '_r'
        else:
            if self.roll_dir.x < 0 and self.roll_dir.z < abs(self.roll_dir.x):
                return '_l'
            if self.roll_dir.z > 0 and abs(self.roll_dir.x) <= self.roll_dir.z:
                return '_f'
            return '_b'

    def on_roll_ghost_show(self):
        anim = self.roll_anim
        anim += self.get_anim_dir_force()
        self.send_event('E_SHOW_GHOST_EFFECT', self.ev_g_position(), self.ev_g_yaw(), anim, self.roll_ghost_anim_start_time)

    def on_roll_ghost_hide(self):
        self.send_event('E_HIDE_GHOST_EFFECT')

    def on_roll_end(self):
        self.sub_state = self.ROLL_END

    def on_roll_dec(self):
        self.start_dec = True

    def on_roll_end_start(self):
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.roll_end_anim_rate)
        self.send_event('E_POST_ACTION', self.roll_end_anim, LOW_BODY, 8, loop=False)

    def on_roll_break(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_SHOOT}, self.sid)

    def on_roll_end_end(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_JUMP_2}, self.sid)

    def on_roll_shoot(self):
        self.on_shoot()

    def on_dash_start(self):
        self.enter_state = self.DASH
        self.sd.ref_cur_speed = self.roll_speed
        self.roll_dir = self.get_roll_dir()
        self.force_dir_anim = self.dash_anim + self.get_anim_dir_force()
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
        self.send_event('E_POST_ACTION', self.dash_anim, LOW_BODY, 4, loop=False, yaw_list=[0, 0, 0, 0])
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        self.send_event('E_MOVE', self.roll_dir)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', self.roll_dir.x, self.roll_dir.z)
        self.end_custom_sound(self.force_dir_anim)
        self.start_custom_sound(self.force_dir_anim)
        self.on_update_aim_help_state(True)

    def on_dash_shoot(self):
        self.on_shoot()

    def on_dash_end(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_STAND, MC_JUMP_2}, self.sid)

    def on_dash_dec(self):
        self.start_dec = True

    def on_update_aim_help_state(self, enable):
        self.send_event('E_ENABLE_WEAPON_AIM_HELPER', enable, PART_WEAPON_POS_MAIN5)
        self.send_event('E_ENABLE_HIT_BY_RAY_IN_ADVANCE', enable, PART_WEAPON_POS_MAIN5)

    def check_transitions(self):
        super(Roll8036, self).check_transitions()
        if self.ev_g_on_ground():
            if not self.sd.ref_rocker_dir:
                return MC_STAND
            else:
                return MC_MOVE

        else:
            return MC_JUMP_2

    def exit(self, enter_states):
        super(Roll8036, self).exit(enter_states)
        self.force_dir_anim = ''
        self.dec_time = 0
        self.start_dec = False
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
        self.on_update_aim_help_state(False)
        self.on_roll_ghost_hide()

    def update(self, dt):
        super(Roll8036, self).update(dt)
        if self.start_dec:
            self.dec_time += dt
            if self.enter_state == self.ROLL:
                now_speed = self.roll_speed - self.dec_time * self.roll_dec_value
            else:
                now_speed = self.dash_speed - self.dec_time * self.dash_dec_value
            if now_speed <= 0:
                now_speed = 0
            self.sd.ref_cur_speed = now_speed
            self.send_event('E_MOVE', self.roll_dir)


@state_exporter({('miss_anim_duration', 'param'): {'zh_name': '\xe6\x9c\xaa\xe5\x91\xbd\xe4\xb8\xad\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                     },
   ('hook_recovery_time', 'param'): {'zh_name': '\xe7\xbb\xb3\xe7\xb4\xa2\xe5\x9b\x9e\xe6\x94\xb6\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                     },
   ('miss_anim_rate', 'param'): {'zh_name': '\xe6\x9c\xaa\xe5\x91\xbd\xe4\xb8\xad\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: __editor_exlposive_dash_postsetter(self)
                                 },
   ('max_break_angle', 'param'): {'zh_name': '\xe9\x95\x9c\xe5\xa4\xb4\xe5\x81\x8f\xe7\xa6\xbb\xe7\x9b\xae\xe6\xa0\x87\xe7\x82\xb9\xe5\xaf\xbc\xe8\x87\xb4\xe9\x92\xa9\xe9\x94\x81\xe6\x96\xad\xe5\xbc\x80\xe7\x9a\x84\xe8\xa7\x92\xe5\xba\xa6'},('dash_acc_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x88\xb0\xe7\x9b\xae\xe6\xa0\x87\xe7\x82\xb9\xe7\x9a\x84\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('swing_acc_speed', 'meter'): {'zh_name': '\xe5\x9c\x86\xe5\x91\xa8\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('max_swing_speed', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x9c\x86\xe5\x91\xa8\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('max_dash_speed', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6'},('max_inherit_speed', 'meter'): {'zh_name': '\xe9\x92\xa9\xe9\x94\x81\xe6\x96\xad\xe5\xbc\x80\xe5\x90\x8e\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('horizon_acc_speed', 'meter'): {'zh_name': '\xe5\x9e\x82\xe7\x9b\xb4\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('vertical_dec_speed', 'meter'): {'zh_name': '\xe5\x9e\x82\xe7\x9b\xb4\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'},('vertical_acc_speed', 'meter'): {'zh_name': '\xe5\x90\x91\xe5\xbf\x83\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('hit_mecha_dash_acc_rate', 'param'): {'zh_name': '\xe5\x8b\xbe\xe4\xb8\xad\xe6\x9c\xba\xe7\x94\xb2\xe5\x90\x8e\xe5\x86\xb2\xe5\x88\xba\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6\xe5\x8f\x98\xe5\x8c\x96\xe7\x8e\x87'},('hit_mecha_swing_acc_rate', 'param'): {'zh_name': '\xe5\x8b\xbe\xe4\xb8\xad\xe6\x9c\xba\xe7\x94\xb2\xe5\x90\x8e\xe5\x9c\x86\xe5\x91\xa8\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6\xe5\x8f\x98\xe5\x8c\x96\xe7\x8e\x87'},('can_jump_time', 'param'): {'zh_name': '\xe9\x92\xa9\xe9\x94\x81\xe5\x8b\xbe\xe4\xb8\xad\xe5\x90\x8e\xe5\x8f\xaf\xe8\xb7\xb3\xe8\xb7\x83\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4'},('max_dash_time', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe9\xa3\x9e\xe8\xa1\x8c\xe6\x97\xb6\xe9\x95\xbf'}})
class AccumulateViceShoot(AccumulateShootPure):
    STATE_MISS = 3
    STATE_DRAG = 4
    STATE_DRAG_END = 5
    BIND_EVENT = AccumulateShootPure.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CLAW_TARGET': 'on_claw_target',
       'E_ACTIVE_STATE': 'on_active_state',
       'E_ENABLE_FORCE_SET_SPEED': 'on_force_set_speed',
       'E_SKILL_BUTTON_BOUNDED': 'on_skill_button_bounded',
       'E_ENABLE_TEST_POST_TIME': 'on_set_enable_test_post_time'
       })
    UP_DIR = math3d.vector(0, 1, 0)
    RIGHT_DIR = math3d.vector(1, 0, 0)
    CLAW_TARGET = 1
    CLAW_SCENE = 2
    CLAW_NONE = 3
    CHECK_SHOW_END_DIS = 2.0
    CHECK_SHOW_END_ROT = 0.9
    PART = UP_BODY
    BREAK_POST_STATES = {}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.fly_skill_id = self.custom_param.get('fly_skill_id', 803652)
        self.sub_skill_id = self.custom_param.get('sub_skill_id', 803656)
        self.weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN4)
        self.force_pre = self.custom_param.get('force_pre', True)
        self.pre_anim_name = self.custom_param.get('pre_anim_name', 'vice_aim')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.5)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.loop_anim_name = self.custom_param.get('loop_anim_name', 'vice_aim')
        self.post_anim_name = self.custom_param.get('post_anim_name', 'vice_shoot')
        self.post_anim_blend_time = self.custom_param.get('post_anim_blend_time', 0.2)
        self.post_anim_duration = self.custom_param.get('post_anim_duration', 1.5)
        self.post_anim_rate = self.custom_param.get('post_anim_rate', 1.0)
        self.use_up_body_bone = self.custom_param.get('use_up_body_bone', False)
        self.hit_anim_name = self.custom_param.get('hit_anim_name', 'vice_attact_02')
        self.all_anim_name_set = {self.loop_anim_name, self.post_anim_name}
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', ('hook', ['biped l upperarm', 'biped l forearm']))
        self.max_break_angle = self.custom_param.get('max_break_angle', 90)
        self.dash_acc_speed = self.custom_param.get('dash_acc_speed', 30.0) * NEOX_UNIT_SCALE
        self.swing_acc_speed = self.custom_param.get('swing_acc_speed', 60.0) * NEOX_UNIT_SCALE
        self.swing_dec_speed = self.custom_param.get('swing_dec_speed', 60.0) * NEOX_UNIT_SCALE
        self.max_swing_speed = self.custom_param.get('max_swing_speed', 200.0) * NEOX_UNIT_SCALE
        self.max_dash_speed = self.custom_param.get('max_dash_speed', 60.0) * NEOX_UNIT_SCALE
        self.max_inherit_speed = self.custom_param.get('max_inherit_speed', 60.0) * NEOX_UNIT_SCALE
        self.max_vertical_speed = self.custom_param.get('max_vertical_speed', 60.0) * NEOX_UNIT_SCALE
        self.max_horizontal_speed = self.custom_param.get('max_horizontal_speed', 60.0) * NEOX_UNIT_SCALE
        self.horizon_acc_speed = self.custom_param.get('horizon_acc_speed', 20.0) * NEOX_UNIT_SCALE
        self.vertical_acc_speed = self.custom_param.get('vertical_acc_speed', 20.0) * NEOX_UNIT_SCALE
        self.vertical_dec_speed = self.custom_param.get('vertical_dec_speed', 20.0) * NEOX_UNIT_SCALE
        self.can_jump_time = self.custom_param.get('can_jump_time', 1.0)
        self.max_dash_time = self.custom_param.get('max_dash_time', 5.0)
        self.post_forbid_states = self.custom_param.get('post_forbid_states', [])
        self.hit_mecha_swing_acc_rate = self.custom_param.get('hit_mecha_swing_acc_rate', 1.0)
        self.hit_mecha_dash_acc_rate = self.custom_param.get('hit_mecha_dash_acc_rate', 1.0)
        self.enable_test_post_time = False
        self.max_wait_post_time = self.custom_param.get('max_wait_post_time', 3.0)
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0.0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration, self.on_end_pre)
        self.register_substate_callback(self.STATE_LOOP, 0.0, self.on_begin_loop)
        self.register_substate_callback(self.STATE_POST, 0.0, self.on_begin_post)
        self.register_substate_callback(self.STATE_POST, self.max_wait_post_time, self.on_reach_max_post_time)
        self.register_substate_callback(self.STATE_DRAG, self.can_jump_time, self.on_can_jump)
        self.register_substate_callback(self.STATE_DRAG, self.max_dash_time, self.on_end_drag)
        self.register_substate_callback(self.STATE_DRAG_END, 0.0, self.on_drag_end)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateViceShoot, self).init_from_dict(unit_obj, bdict, sid, info)
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.drag_end = False
        self.claw_state = self.CLAW_NONE
        self.init_walk_direction = math3d.vector(0, 0, 0)
        self.last_walk_direction = math3d.vector(0, 0, 0)
        self.swing_direction = math3d.vector(0, 0, 0)
        self.vertical_speed_direction = math3d.vector(0, 0, 0)
        self.horizon_speed_direction = math3d.vector(0, 0, 0)
        self.enhanced_by_module = bdict.get('enhanced_by_module', False)
        self.cur_swing_speed = 0
        self.cur_swing_acc_rate = 1.0
        self.cur_dash_acc_rate = 1.0
        self.swing_acc_time = 0.0
        self.cur_hor_speed = 0.0
        self.can_jump = False
        self._dash_dis = 0.0
        self._old_pos = 0.0
        self.force_speed = False
        self.read_data_from_custom_param()
        self.enable_param_changed_by_buff()

    def on_post_init_complete(self, bidct):
        super(AccumulateViceShoot, self).on_post_init_complete(bidct)

    def check_can_cast_skill(self):
        if not self.skill_id:
            return True
        return self.ev_g_can_cast_skill(self.skill_id) and (not self.enhanced_by_module or self.enhanced_by_module and self.ev_g_can_cast_skill(self.sub_skill_id))

    def refresh_param_changed(self):
        if self.enhanced_by_module:
            self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)
        else:
            self.send_event('E_DEL_ACTION_SUB_SKILL_ID', self.bind_action_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def on_skill_button_bounded(self, skill_id):
        if skill_id != self.skill_id or not self.enhanced_by_module:
            return
        self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)

    def on_active_state(self, sid):
        if not self.is_active:
            return
        if sid != MC_JUMP_1:
            return
        if self.can_jump:
            self.sub_state = self.STATE_DRAG_END
            self.end_custom_sound('dash_end')
            self.start_custom_sound('dash_end')
            self.disable_self()

    def on_end_pre(self):
        super(AccumulateViceShoot, self).on_end_pre()
        self.enable_ik()
        self.send_event('E_SHOW_HOOK_TRACK_SFX', self.weapon_pos)
        self.send_event('E_UPDATE_SFX_STATE', True)

    def enable_ik(self):
        if self.shoot_aim_ik:
            self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik)
            self.send_event('E_ENABLE_AIM_IK', True)
            self.send_event('E_AIM_LERP_TIME', 0.1)

    def disable_ik(self):
        self.send_event('E_ENABLE_AIM_IK', False)

    def cancel_shoot(self):
        if self.is_active and self.sub_state not in (self.STATE_DRAG, self.STATE_POST):
            self.send_event('E_ACTION_UP', self.bind_action_id)
            self.disable_self()

    def on_begin_post(self):
        self.skill_id and self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_SKILL', self.sub_skill_id)
        self.send_event('E_ACC_SKILL_END', self.weapon_pos)
        self.acc_skill_ended = True
        self._fire()
        self.send_event('E_ANIM_RATE', self.PART, self.post_anim_rate)
        self.send_event('E_POST_ACTION', self.post_anim_name, self.PART, 7, blend_time=self.post_anim_blend_time)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.end_custom_sound('hold')
        self.end_custom_sound('post')
        self.start_custom_sound('post')
        self.send_event('E_SHOW_CLAW_TARGET_EFFECT')
        self.send_event('E_HIDE_HOOK_TRACK_SFX')

    def on_begin_pre(self):
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_RUN, self.pre_anim_name, loop=True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.pre_anim_name, loop=True)
        self.send_event('E_ANIM_RATE', self.PART, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim_name, self.PART, 7)
        self.end_custom_sound('pre')
        self.start_custom_sound('pre')
        self.send_event('E_ADD_BLACK_STATE', {MC_SHOOT})

    def on_begin_loop(self):
        self.send_event('E_ANIM_RATE', self.PART, 1.0)
        self.send_event('E_POST_ACTION', self.loop_anim_name, self.PART, 7, loop=True)
        self.end_custom_sound('hold')
        self.start_custom_sound('hold')

    def on_reach_max_post_time(self):
        self.disable_self()

    def on_end_drag(self):
        self.sub_state = self.STATE_DRAG_END

    def on_can_jump(self):
        self.can_jump = True
        self.send_event('E_DEL_BLACK_STATE', {MC_JUMP_1})

    def on_set_enable_test_post_time(self, enable):
        pass

    def on_claw_target(self, explosive_info):
        if self.enable_test_post_time:
            return
        if not self.is_active:
            return
        cobj, pos, model, normal, target_id, throw_info = explosive_info
        self.claw_state = self.CLAW_NONE
        if cobj and target_id:
            self.claw_state = self.CLAW_TARGET
            self.cur_dash_acc_rate = self.hit_mecha_dash_acc_rate
            self.cur_swing_acc_rate = self.hit_mecha_swing_acc_rate
        else:
            if cobj and not target_id:
                self.claw_state = self.CLAW_SCENE
            self.send_event('E_CALL_SYNC_METHOD', 'on_claw_hit', (self.claw_state, target_id, pos))
            if self.sub_state != self.STATE_POST:
                self.disable_self()
                return
        self.sub_state = self.STATE_DRAG
        self.target_pos = pos
        self.init_walk_direction = self.ev_g_char_walk_direction()
        self._start_cal_dash_dist()
        self.disable_ik()
        self.air_walk_direction_setter.reset()
        self.sd.ref_rotatedata.set_body_pitch_to_head(0.1)
        self.send_event('E_BRAKE')
        self.send_event('E_DISABLE_STATE', (MC_RUN, MC_MOVE, MC_STAND, MC_SUPER_JUMP, MC_JUMP_1, MC_JUMP_2, MC_JUMP_3))
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_DO_SKILL', self.fly_skill_id)
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_POST_ACTION', self.hit_anim_name, LOW_BODY, 6, loop=True, blend_time=0.5)
        self.send_event('E_UPDATE_HOOK_STATE', 2, {'hook_target_pos': (self.target_pos.x, self.target_pos.y, self.target_pos.z)}, need_sync=True)
        self.send_event('E_ADD_BLACK_STATE', {MC_MOVE, MC_JUMP_1, MC_JUMP_2, MC_JUMP_3, MC_STAND, MC_SUPER_JUMP, MC_RUN})
        self.send_event('E_DEL_BLACK_STATE', {MC_SHOOT})
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
        self.send_event('E_SHOW_CLAW_DRAG_SCRREN_EFFECT')
        self.send_event('E_SHOW_HOOK_END_EFFECT', 1 if self.claw_state == self.CLAW_TARGET else 2, (self.target_pos.x, self.target_pos.y, self.target_pos.z))
        self.start_custom_sound('dash')
        self.sd.ref_in_dash_drag = True

    def on_drag_end(self):
        self.drag_end = True
        self.end_custom_sound('dash_end')
        self.start_custom_sound('dash_end')
        self.send_event('E_CLEAR_BLACK_STATE')

    def enter(self, leave_states):
        super(AccumulateViceShoot, self).enter(leave_states)

    def exit(self, enter_states):
        super(AccumulateViceShoot, self).exit(enter_states)
        self.recorrect_inherit_speed()
        self.sd.ref_in_dash_drag = False
        self.can_jump = False
        self.drag_end = False
        self.cur_swing_speed = 0.0
        self.cur_swing_acc_rate = 1.0
        self.cur_dash_acc_rate = 1.0
        self.swing_acc_time = 0.0
        self.cur_hor_speed = 0.0
        self.swing_direction = math3d.vector(0, 0, 0)
        self.last_walk_direction = math3d.vector(0, 0, 0)
        self.vertical_speed_direction = math3d.vector(0, 0, 0)
        self.horizon_speed_direction = math3d.vector(0, 0, 0)
        self.disable_ik()
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_HIDE_HOOK_END_EFFECT')
        self.send_event('E_END_SKILL', self.fly_skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.sub_skill_id)
        self.send_event('E_CANCLE_CLAW_TARGET_EFFECT')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_RUN, None)
        self.send_event('E_HIDE_HOOK_TRACK_SFX')
        self.send_event('E_UPDATE_SFX_STATE', False)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
        self.send_event('E_HIDE_CLAW_DRAG_SCRREN_EFFECT')
        self.send_event('E_CANCEL_CLAW_TARGET_EFFECT')
        scn = world.get_active_scene()
        camera = scn.active_camera
        self.sd.ref_rotatedata.set_body_pitch_to_zero(0.5)
        self.sd.ref_logic_trans.yaw_target = camera.rotation_matrix.forward.yaw
        self._finish_cal_dash_dist()
        self.end_custom_sound('dash')
        return

    def check_transitions(self):
        if not self.drag_end:
            return
        self.disable_self()
        if not self.ev_g_on_ground():
            return MC_JUMP_2
        return MC_STAND

    def recorrect_inherit_speed(self):
        if self.last_walk_direction and not self.last_walk_direction.is_zero:
            if self.last_walk_direction.length > self.max_inherit_speed:
                self.last_walk_direction = self.last_walk_direction * (self.max_inherit_speed / self.last_walk_direction.length)
            self.air_walk_direction_setter.execute(self.last_walk_direction)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8036', MECHA_MEMORY_LEVEL_9, self._dash_dis / NEOX_UNIT_SCALE), False, True)
        self._dash_dis = 0

    def on_force_set_speed(self, state):
        pass

    def update(self, dt):
        super(AccumulateViceShoot, self).update(dt)
        if self.sub_state == self.STATE_DRAG:
            if not self.target_pos:
                return
            model = self.ev_g_model()
            if not model or not model.valid:
                return
            scn = world.get_active_scene()
            camera = scn.active_camera
            if not camera:
                return
            pos = self.ev_g_position()
            pos_head = model.get_bone_matrix('biped head', world.SPACE_TYPE_WORLD).translation
            pos_dir = self.target_pos - pos
            if not pos_dir.is_zero:
                pos_dir.normalize()
            pos_dir_y = math3d.vector(0.0, pos_dir.y, 0.0)
            pos_dir_xz = math3d.vector(pos_dir.x, 0.0, pos_dir.z)
            pos_right = pos_dir.cross(pos_dir_xz)
            pos_forward = pos_right.cross(pos_dir)
            is_use_look_down = pos_head.y - self.target_pos.y > self.CHECK_SHOW_END_DIS * NEOX_UNIT_SCALE and pos_dir_xz.dot(pos_dir) < self.CHECK_SHOW_END_ROT
            pitch = pos_forward.pitch
            yaw = pos_forward.yaw
            if pos_dir.y < 0:
                if is_use_look_down:
                    pitch -= 0.785
                pitch = -pitch
            self.sd.ref_logic_trans.pitch_target = pitch
            self.sd.ref_logic_trans.yaw_target = yaw
            tangent_dir = self.UP_DIR.cross(pos_dir)
            if not tangent_dir.is_zero:
                tangent_dir.normalize()
            rocker_dir = self.sd.ref_rocker_dir
            if not rocker_dir or rocker_dir.x == 0:
                swing_dir = 0.0
                if self.cur_swing_speed > 0:
                    self.cur_swing_speed -= dt * self.swing_dec_speed * self.cur_swing_acc_rate
                    if not self.swing_direction.is_zero:
                        self.swing_direction.normalize()
                    self.swing_direction *= self.cur_swing_speed
                else:
                    self.cur_swing_speed = 0.0
                    self.swing_direction = math3d.vector(0, 0, 0)
            else:
                swing_dir = abs(rocker_dir.x) / rocker_dir.x
                self.swing_acc_time += dt
                self.swing_direction += tangent_dir * swing_dir * dt * self.swing_acc_speed * self.cur_swing_acc_rate
                self.cur_swing_speed = self.swing_direction.length
            if self.swing_direction.length > self.max_swing_speed:
                self.swing_direction = self.swing_direction * (self.max_swing_speed / self.swing_direction.length)
            if self.vertical_speed_direction.y * pos_head.y < 0.0:
                self.vertical_speed_direction += pos_dir_y * self.vertical_acc_speed * dt * self.cur_dash_acc_rate
            else:
                self.vertical_speed_direction += pos_dir_y * self.vertical_dec_speed * dt * self.cur_dash_acc_rate
            if self.vertical_speed_direction.length > self.max_vertical_speed:
                self.vertical_speed_direction = self.vertical_speed_direction * (self.max_vertical_speed / self.vertical_speed_direction.length)
            self.cur_hor_speed += dt * self.horizon_acc_speed * self.cur_dash_acc_rate
            self.horizon_speed_direction = pos_dir_xz * self.cur_hor_speed
            if self.horizon_speed_direction.length > self.max_horizontal_speed:
                self.horizon_speed_direction = self.horizon_speed_direction * (self.max_horizontal_speed / self.horizon_speed_direction.length)
            self.last_walk_direction = self.swing_direction + self.vertical_speed_direction + self.horizon_speed_direction + self.init_walk_direction
            anim_dir_x = 0.0
            anim_dir_y = 0.0
            dir_swing = self.last_walk_direction.cross(pos_dir)
            if dir_swing.y != 0:
                anim_dir_x = abs(dir_swing.y) / dir_swing.y * (1.0 - abs(self.last_walk_direction.dot(pos_dir) / self.last_walk_direction.length))
            if abs(anim_dir_x) < 0.2:
                anim_dir_x = 0
            if is_use_look_down:
                anim_dir_y = pos_dir.y
            else:
                anim_dir_y = abs(pos_dir.y)
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', anim_dir_x, anim_dir_y)
            self.air_walk_direction_setter.execute(self.force_speed or self.last_walk_direction if 1 else math3d.vector(0, 0, 0))
            dst = self.target_pos - pos
            cam_forward = camera.rotation_matrix.forward
            self.sd.ref_turn_dir = cam_forward.cross(pos_dir_xz).y * 4.0
            if dst.length < 8.0 * NEOX_UNIT_SCALE or math.acos(cam_forward.dot(pos_dir_xz)) > math.pi * self.max_break_angle / 180.0:
                self.sub_state = self.STATE_DRAG_END

    def destroy(self):
        super(AccumulateViceShoot, self).destroy()
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        return