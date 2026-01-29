# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8025.py
from __future__ import absolute_import
from six.moves import range
from .StateBase import StateBase
from .JumpLogic import JumpUp
from .MoveLogic import Walk
from .ShootLogic import Reload
from logic.gcommon import editor
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gutils.character_ctrl_utils import get_forward_by_rocker_and_camera_without_y

class Walk8025(Walk):

    def enter(self, leave_states):
        super(Walk8025, self).enter(leave_states)
        if MC_RUN not in leave_states:
            self.start_custom_sound('start')
        self.start_custom_sound('loop')

    def exit(self, enter_states):
        super(Walk8025, self).exit(enter_states)
        self.end_custom_sound('start')
        self.end_custom_sound('loop')
        if MC_RUN not in enter_states:
            self.end_custom_sound('end')
            self.start_custom_sound('end')


class JumpUp8025(JumpUp):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(JumpUp8025, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.add_ratio = 0.0
        self.enable_param_changed_by_buff()

    def get_jump_speed(self, speed_scale=1.0):
        jump_speed = super(JumpUp8025, self).get_jump_speed(speed_scale)
        return jump_speed * (1.0 + self.add_ratio)


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_settor': lambda self: self.register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('loop_duration', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\xbe\xaa\xe7\x8e\xaf\xe6\x97\xb6\xe9\x95\xbf','post_settor': lambda self: self.register_callbacks()
                                },
   ('post_anim_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_settor': lambda self: self.register_callbacks()
                                     },
   ('post_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_settor': lambda self: self.register_callbacks()
                                 },
   ('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','post_settor': lambda self: self.register_callbacks()
                                  },
   ('max_speed', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6','post_settor': lambda self: self.register_callbacks()
                            },
   ('acc_duration', 'param'): {'zh_name': '\xe5\x8a\xa0\xe9\x80\x9f\xe6\x97\xb6\xe9\x95\xbf','post_settor': lambda self: self.register_callbacks()
                               },
   ('dec_duration', 'param'): {'zh_name': '\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x95\xbf','post_settor': lambda self: self.register_callbacks()
                               },
   ('step_height', 'meter'): {'zh_name': '\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6'}})
class Dash8025(StateBase):
    BIND_EVENT = {}
    STATE_NONE = 0
    STATE_PRE = 1
    STATE_LOOP = 2
    STATE_POST = 3

    def _update_acc_dec_speed(self):
        self.acc_speed = self.max_speed / self.acc_duration
        self.dec_speed = self.max_speed / self.dec_duration

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.pre_anim_name = self.custom_param.get('pre_anim_name', 'dash_01')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.4)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.loop_anim_name = self.custom_param.get('loop_anim_name', 'dash_02')
        self.loop_duration = self.custom_param.get('loop_duration', 1.6)
        self.post_anim_name = self.custom_param.get('post_anim_name', 'dash_03')
        self.post_anim_duration = self.custom_param.get('post_anim_duration', 1.1)
        self.post_anim_rate = self.custom_param.get('post_anim_rate', 1.0)
        self.post_break_time = self.custom_param.get('post_break_time', 0.6)
        self.max_speed = self.custom_param.get('max_speed', 20) * NEOX_UNIT_SCALE
        self.acc_duration = self.custom_param.get('acc_duration', 0.5)
        self.dec_duration = self.custom_param.get('dec_duration', 0.8)
        self.step_height = self.custom_param.get('step_height', 2) * NEOX_UNIT_SCALE
        self._update_acc_dec_speed()
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0.0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration, self.on_end_pre)
        self.register_substate_callback(self.STATE_LOOP, 0.0, self.on_begin_loop)
        self.register_substate_callback(self.STATE_LOOP, self.loop_duration, self.on_end_loop)
        self.register_substate_callback(self.STATE_POST, 0.0, self.on_begin_post)
        self.register_substate_callback(self.STATE_POST, self.post_break_time, self.enable_post_break)
        self.register_substate_callback(self.STATE_POST, self.post_anim_duration, self.on_end_post)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8025, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.need_check_quit = False
        self.move_dir = None
        self.model_forward_locked = False
        return

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        return True

    def _lock_model_forward(self, flag):
        if self.model_forward_locked ^ flag:
            self.model_forward_locked = flag
            self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', not flag)
            if flag:
                yaw_target = self.move_dir.yaw
            else:
                yaw_target = self.sd.ref_effective_camera_rot.get_forward().yaw
            self.sd.ref_logic_trans.yaw_target = yaw_target
            self.sd.ref_common_motor.set_yaw_time(0.2)

    def enter(self, leave_states):
        super(Dash8025, self).enter(leave_states)
        self.send_event('E_STOP_ACTION_CD', 'action8')
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        self.send_event('E_ENABLE_TWIST_PITCH', False, True)
        self.send_event('E_STEP_HEIGHT', self.step_height)
        move_dir = get_forward_by_rocker_and_camera_without_y(self, False)
        self.move_dir = move_dir
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.model_forward_locked = False
        self.need_check_quit = False
        self._lock_model_forward(True)
        self.sub_state = self.STATE_PRE
        self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def on_begin_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim_name, LOW_BODY, 1)

    def on_end_pre(self):
        self.sub_state = self.STATE_LOOP

    def on_begin_loop(self):
        self.send_event('E_POST_ACTION', self.loop_anim_name, LOW_BODY, 1)

    def on_end_loop(self):
        if self.ev_g_on_ground():
            self.sub_state = self.STATE_POST
        else:
            self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2, MC_STAND, MC_MOVE}, self.sid)
            self.need_check_quit = True

    def on_begin_post(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.post_anim_rate)
        self.send_event('E_POST_ACTION', self.post_anim_name, LOW_BODY, 1)
        self.send_event('E_RESET_GRAVITY')
        self._lock_model_forward(False)

    def enable_post_break(self):
        self.need_check_quit = True
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_1, MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK}, self.sid)

    def on_end_post(self):
        self.disable_self()

    def update(self, dt):
        super(Dash8025, self).update(dt)
        cur_speed = self.sd.ref_cur_speed
        if cur_speed < self.max_speed:
            cur_speed += self.acc_speed * dt
        if cur_speed > self.max_speed:
            cur_speed = self.max_speed
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_SET_WALK_DIRECTION', self.move_dir * cur_speed)

    def check_transitions(self):
        if self.need_check_quit:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            else:
                return MC_JUMP_2

    def exit(self, enter_states):
        super(Dash8025, self).exit(enter_states)
        self._lock_model_forward(False)
        self.send_event('E_ENABLE_TWIST_PITCH', True, True)
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_IGNORE_RELOAD_ANIM', False)


class Reload8025(Reload):
    BIND_EVENT = Reload.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BEGIN_FORCE_HEAT_DISSIPATION': 'on_begin_force_heat_dissipation',
       'E_END_FORCE_HEAT_DISSIPATION': 'on_end_force_heat_dissipation'
       })
    MIN_RELOAD_DURATION = 1.1
    HEAT_WEAPON_ID = 802501

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8025, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.dissipation_completed = False

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.reloaded:
            return False
        self.send_event('E_FORCE_EXECUTE_HEAT_DISSIPATION', self.HEAT_WEAPON_ID)
        super(Reload, self).action_btn_down()
        return True

    def exit(self, enter_states):
        super(Reload8025, self).exit(enter_states)
        if self.dissipation_completed and not self.reloaded:
            self.reloaded = True

    def check_transitions(self):
        if self.dissipation_completed and self.elapsed_time >= self.anim_time:
            self.reloaded = True
            self.disable_self()
        continue_fire, _ = self.ev_g_continue_fire() or (False, None)
        if continue_fire:
            return MC_SHOOT
        else:
            return

    def on_begin_force_heat_dissipation(self, key, dissipation_duration):
        if key != self.HEAT_WEAPON_ID:
            return
        self.reload_time = max(self.MIN_RELOAD_DURATION, dissipation_duration)
        self.dissipation_completed = False
        if not self.ignore_anim:
            self.active_self()

    def on_end_force_heat_dissipation(self, key):
        if key != self.HEAT_WEAPON_ID:
            return
        else:
            self.dissipation_completed = True
            if self.is_active:
                self.reloaded = self.elapsed_time >= self.reload_time
            else:
                self.reloaded = True
                continue_fire, fire_weapon_pos = self.ev_g_continue_fire() or (False, None)
                if continue_fire:
                    if self.ev_g_try_weapon_attack_begin(self.weapon_pos):
                        self.continue_fire = True
            return


@editor.state_exporter({('common_weapon_lock_cd', 'param'): {'zh_name': '\xe6\x99\xae\xe9\x80\x9a\xe5\xbd\xa2\xe6\x80\x81\xe6\x96\xb0\xe5\xa2\x9e\xe5\x8f\x91\xe5\xb0\x84\xe6\x95\xb0\xe9\x97\xb4\xe9\x9a\x94'},('enhanced_weapon_lock_cd', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x8c\x96\xe5\xbd\xa2\xe6\x80\x81\xe6\x96\xb0\xe5\xa2\x9e\xe5\x8f\x91\xe5\xb0\x84\xe6\x95\xb0\xe9\x97\xb4\xe9\x9a\x94'}})
class ExternShoulderGrenade8025(StateBase):
    BIND_EVENT = {'TRY_STOP_WEAPON_ATTACK': 'end_shoot',
       'E_WPBAR_INIT': 'refresh_fire_param'
       }
    STATE_NONE = 0
    STATE_OPENING = 1
    STATE_OPENED = 2
    STATE_FIRE = 3
    STATE_CLOSING = 4

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.bullet_skill_id = self.custom_param.get('bullet_skill_id', None)
        self.common_weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN2)
        self.common_weapon_lock_cd = self.custom_param.get('common_weapon_lock_cd', 0.3)
        self.weapon_pos = self.common_weapon_pos
        self.cur_lock_cd = self.common_weapon_lock_cd
        self.enhanced_weapon_pos = self.custom_param.get('enhanced_weapon_pos', PART_WEAPON_POS_MAIN2)
        self.enhanced_weapon_lock_cd = self.custom_param.get('enhanced_weapon_lock_cd', 0.15)
        self.extern_bone_tree = self.custom_param.get('extern_bone_tree', None)
        self.open_anim_name = self.custom_param.get('open_anim_name', 'pan_start')
        self.open_anim_duration = self.custom_param.get('open_anim_duration', 0.2)
        self.open_anim_rate = self.custom_param.get('open_anim_rate', 1.0)
        self.fire_anim_name = self.custom_param.get('fire_anim_name', 'pan_fire')
        self.fire_anim_duration = self.custom_param.get('fire_anim_duration', 0.2)
        self.close_anim_name = self.custom_param.get('close_anim_name', 'pan_end')
        self.close_anim_duration = self.custom_param.get('close_anim_duration', 0.2)
        self.close_anim_rate = self.custom_param.get('close_anim_rate', 1.0)
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_OPENING, 0.0, self.on_begin_opening)
        self.register_substate_callback(self.STATE_OPENING, self.open_anim_duration, self.on_end_opening)
        self.register_substate_callback(self.STATE_OPENED, 0.0, self.on_begin_opened)
        self.register_substate_callback(self.STATE_FIRE, 0.0, self.on_fire)
        self.register_substate_callback(self.STATE_FIRE, self.fire_anim_duration, self.on_end_fire)
        self.register_substate_callback(self.STATE_CLOSING, 0.0, self.on_begin_closing)
        self.register_substate_callback(self.STATE_CLOSING, 0.0, self.on_end_closing)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ExternShoulderGrenade8025, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.new_weapon_pos = self.weapon_pos
        self.is_enhanced = False
        self.enable_param_changed_by_buff()
        self.btn_down = False
        self.aiming = False
        self.valid_bullet_count = 0
        self.fire_start_index = 0
        self.fire_index_count = 4
        self.sd.ref_need_sync_socket_index = False
        self.sd.ref_is_first_grenade = False

    def _check_weapon_pos_refreshed(self):
        if self.weapon_pos != self.new_weapon_pos:
            if self.is_active:
                return
            self.weapon_pos = self.new_weapon_pos
            self.cur_lock_cd = self.enhanced_weapon_lock_cd if self.is_enhanced else self.common_weapon_lock_cd
            self.fire_start_index = self.ev_g_socket_index(self.weapon_pos) / 2

    def refresh_param_changed(self):
        self.new_weapon_pos = self.enhanced_weapon_pos if self.is_enhanced else self.common_weapon_pos
        self._check_weapon_pos_refreshed()

    def action_btn_down(self):
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_can_cast_skill(self.bullet_skill_id):
            return False
        self.btn_down = True
        if not self.is_active:
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
            self.active_self()
        return True

    def action_btn_up(self):
        self.btn_down = False
        if self.is_active and self.sub_state == self.STATE_OPENED:
            self.sub_state = self.STATE_FIRE

    def _aim(self, flag):
        if self.aiming ^ flag:
            self.aiming = flag
            if flag:
                self.send_event('E_ACC_SKILL_BEGIN', self.weapon_pos)
            else:
                self.send_event('E_ACC_SKILL_END', self.weapon_pos)
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', flag, self.weapon_pos)

    def enter(self, leave_states):
        super(ExternShoulderGrenade8025, self).enter(leave_states)
        self.sub_state = self.STATE_OPENING
        self._aim(True)
        self.valid_bullet_count = 0
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.end_shoot)
        return

    def on_begin_opening(self):
        self.send_event('E_POST_EXTERN_ACTION', self.open_anim_name, True, subtree=self.extern_bone_tree, timeScale=self.open_anim_rate)

    def on_end_opening(self):
        self.sub_state = self.STATE_OPENED

    def on_begin_opened(self):
        if not self.btn_down:
            self.sub_state = self.STATE_FIRE

    def _fire(self, aim_target_index):
        self.send_event('E_DO_SKILL', self.bullet_skill_id)
        self.ev_g_try_weapon_attack_begin(self.weapon_pos, aim_target_index=aim_target_index)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)

    def on_fire(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sd.ref_need_sync_socket_index = True
        self.sd.ref_is_first_grenade = True
        if len(self.sd.ref_aim_targets[self.weapon_pos]) > 0:
            for index in range(self.valid_bullet_count):
                self._fire(index)
                self.sd.ref_is_first_grenade = False

        else:
            for index in range(self.valid_bullet_count):
                self._fire(-1)
                self.sd.ref_is_first_grenade = False

        index_list = [ self._validate_fire_index(self.fire_start_index + i) for i in range(self.valid_bullet_count) ]
        self.send_event('E_PLAY_SECOND_WEAPON_FIRE_EFFECT', index_list)
        self.fire_start_index = self._validate_fire_index(index_list[-1] + 1)
        self.sd.ref_need_sync_socket_index = False
        self._aim(False)

    def on_end_fire(self):
        self.sub_state = self.STATE_CLOSING

    def on_begin_closing(self):
        self.send_event('E_POST_EXTERN_ACTION', self.close_anim_name, True, subtree=self.extern_bone_tree, timeScale=self.close_anim_rate)

    def on_end_closing(self):
        self.disable_self()

    def _update_valid_bullet_count(self):
        can_lock_count = int(self.elapsed_time / self.cur_lock_cd) + 1
        valid_bullet_count = self.ev_g_skill_valid_cast_count(self.bullet_skill_id)
        valid_bullet_count = min(can_lock_count, valid_bullet_count)
        if self.valid_bullet_count != valid_bullet_count:
            self.send_event('E_SET_MULTIPLE_AIM_TARGET_MAX_COUNT', self.weapon_pos, valid_bullet_count, force_update=True)
            if self.valid_bullet_count < valid_bullet_count:
                index_list = [ self._validate_fire_index(self.fire_start_index + i) for i in range(self.valid_bullet_count, valid_bullet_count) ]
                self.send_event('E_PLAY_SECOND_WEAPON_HOLD_EFFECT', index_list)
            else:
                index_list = [ self._validate_fire_index(self.fire_start_index + i) for i in range(valid_bullet_count, self.valid_bullet_count) ]
                self.send_event('E_STOP_SECOND_WEAPON_HOLD_EFFECT', index_list)
            self.valid_bullet_count = valid_bullet_count

    def _validate_fire_index(self, index):
        return index % self.fire_index_count

    def update(self, dt):
        super(ExternShoulderGrenade8025, self).update(dt)
        if self.aiming:
            self._update_valid_bullet_count()

    def _clear_all_holding_effect(self):
        if self.valid_bullet_count > 0:
            index_list = [ self._validate_fire_index(self.fire_start_index + i) for i in range(0, self.valid_bullet_count) ]
            self.send_event('E_STOP_SECOND_WEAPON_HOLD_EFFECT', index_list)

    def exit(self, enter_states):
        super(ExternShoulderGrenade8025, self).exit(enter_states)
        self.send_event('E_POST_EXTERN_ACTION', None, False)
        self.sub_state = self.STATE_NONE
        self._aim(False)
        self._clear_all_holding_effect()
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self._check_weapon_pos_refreshed()
        return

    def end_shoot(self):
        if self.is_active:
            self._clear_all_holding_effect()
            self.sub_state = self.STATE_CLOSING
        self.send_event('E_ACTION_UP', self.bind_action_id)