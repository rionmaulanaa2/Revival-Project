# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8019.py
from __future__ import absolute_import
from .StateBase import StateBase
from logic.gcommon import editor
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from logic.gcommon.cdata.mecha_status_config import *
from .ShootLogic import WeaponFire, Reload, AccumulateShoot
from .BoostLogic import OxRushNew
from .MoveLogic import Run, Turn
from logic.gcommon.common_const.mecha_const import DEFEND_ON, DEFEND_OFF
from logic.gcommon.common_utils.bcast_utils import E_8019_SEC_BEGIN, E_8019_SEC_END, E_8019_SEC_HOLD, E_8019_SEC_POST
from logic.gcommon.const import SOUND_TYPE_MECHA_FOOTSTEP
from logic.gcommon.common_utils.bcast_utils import E_EXECUTE_MECHA_ACTION_SOUND
from .JumpLogic import JumpUp, Fall, OnGround
from logic.gcommon.common_const.ui_operation_const import DASH_AUTO_DEFEND_8019
from logic.gutils.screen_effect_utils import create_screen_effect_directly
import copy
import world
import math
DEFEND_ANIM = 'shd_idle'
DEFEND_EXIT_ANIM = 'shd_end'

class JumpUp8019(JumpUp):
    BIND_EVENT = JumpUp.BIND_EVENT.copy()
    BIND_EVENT.update({'E_UP_RUN_ANIM_8019': 'on_update_jump_anim'
       })

    def on_update_jump_anim(self, tag):
        if tag == DEFEND_ON:
            self.refresh_action_param((0, ['shd_jump_01', 'lower', 1]), self.custom_param)
        else:
            self.refresh_action_param((0, ['jump_01', 'lower', 1]), self.custom_param)


class Fall8019(Fall):
    BIND_EVENT = Fall.BIND_EVENT.copy()
    BIND_EVENT.update({'E_UP_RUN_ANIM_8019': 'on_update_jump_anim'
       })

    def on_update_jump_anim(self, tag):
        if tag == DEFEND_ON:
            self.refresh_action_param((0, ['shd_jump_02', 'lower', 1, {'loop': False}]), self.custom_param)
        else:
            self.refresh_action_param((0, ['jump_02', 'lower', 1, {'loop': False}]), self.custom_param)


class OnGround8019(OnGround):
    BIND_EVENT = OnGround.BIND_EVENT.copy()
    BIND_EVENT.update({'E_UP_RUN_ANIM_8019': 'on_update_jump_anim'
       })

    def on_update_jump_anim(self, tag):
        if tag == DEFEND_ON:
            self.refresh_action_param((0, ['shd_jump_03', 'lower', 1, {'blend_time': 0}]), self.custom_param)
        else:
            self.refresh_action_param((0, ['jump_03', 'lower', 1, {'blend_time': 0}]), self.custom_param)


class Run8019(Run):
    ANIM_PARAM = {DEFEND_OFF: (
                  'run', 4, True),
       DEFEND_ON: (
                 'shd_run', 4, True)
       }
    BIND_EVENT = Run.BIND_EVENT.copy()
    BIND_EVENT.update({'E_UP_RUN_ANIM_8019': 'on_update_run_anim'
       })

    def read_data_from_custom_param(self):
        super(Run8019, self).read_data_from_custom_param()
        tag = self.ev_g_handy_shield_state()
        self.run_anim, self.run_anim_dir_type, self.run_ignore_sufix = self.ANIM_PARAM[tag]
        self.refresh_sub_state_callback()

    def on_update_run_anim(self, tag):
        _, self.run_anim_dir_type, self.run_ignore_sufix = self.ANIM_PARAM[tag]
        self.on_replace_run_anim(self.ANIM_PARAM[tag][0])

    def enter(self, leave_states):
        if self.ev_g_handy_shield_state():
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
            if self.sd.ref_up_body_anim in (DEFEND_ANIM, DEFEND_EXIT_ANIM):
                self.send_event('E_CLEAR_UP_BODY_ANIM')
        super(Run8019, self).enter(leave_states)
        return

    def exit(self, enter_states):
        if self.ev_g_handy_shield_state():
            cur_state = self.ev_g_cur_state()
            if MC_RELOAD not in cur_state and MC_SECOND_WEAPON_ATTACK not in cur_state:
                self.send_event('E_POST_ACTION', DEFEND_ANIM, UP_BODY, 1)
                self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', DEFEND_ANIM, loop=False)
        super(Run8019, self).exit(enter_states)


class Turn8019(Turn):
    TURN_ANIM = [
     'turnleft_90', 'turnright_90']
    TURN_SHD_ANIM = ['shd_turnleft_90', 'shd_turnright_90']

    def on_enter(self):
        anim = self.ev_g_handy_shield_state() or self.TURN_ANIM[self.turn_dir] if 1 else self.TURN_SHD_ANIM[self.turn_dir]
        self.send_event('E_POST_ACTION', anim, LOW_BODY, 1, loop=True, ignore_sufix=True)


class WeaponFire8019(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SWITCH_8019': 'on_switch'
       })
    IK_1 = (
     'aim1', ['biped spine', 'biped spine1', 'biped r clavicle', 'biped r upperarm', 'biped r forearm'])
    IK_2 = ('aim2', ['biped spine', 'biped spine1', 'biped r clavicle', 'biped r upperarm', 'biped r forearm'])

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8019, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.enable_param_changed_by_buff()

    def read_data_from_custom_param(self):
        super(WeaponFire8019, self).read_data_from_custom_param()
        self.all_shoot_anim.add('shoot_idle')
        self.switching = False
        self.is_sp = False

    def _reset_aim_ik_param(self):
        self.shoot_aim_ik = self.ev_g_handy_shield_state() or self.IK_1 if 1 else self.IK_2
        super(WeaponFire8019, self)._reset_aim_ik_param()

    def on_switch(self, tag):
        self.switching = tag

    def check_transitions(self):
        if self.switching:
            self._end_shoot()
            return
        super(WeaponFire8019, self).check_transitions()

    def action_btn_down(self, ignore_reload=False):
        if self.switching:
            return False
        return super(WeaponFire8019, self).action_btn_down(ignore_reload)

    def exit(self, enter_states):
        super(WeaponFire, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False, state='WeaponFire')
        if self.sd.ref_up_body_anim in self.all_shoot_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.fired = False
        if enter_states:
            self.try_weapon_attack_end()
        if not self.ev_g_handy_shield_state():
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, None)
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_low_move_anim_states, None)
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        return

    def refresh_param_changed(self):
        self.on_weapon_change()
        if self.is_sp:
            self.weapon_pos = 2
        else:
            self.weapon_pos = 1
        self.send_event('E_8019_SWITCH_WEAPON', self.weapon_pos)


class Reload8019(Reload):

    def read_data_from_custom_param(self):
        super(Reload8019, self).read_data_from_custom_param()

    def enter(self, leave_states):
        self.reload_anim = 'shd_reload' if self.ev_g_is_defending() else 'reload'
        super(Reload8019, self).enter(leave_states)

    def exit(self, enter_states):
        if self.ev_g_handy_shield_state():
            self.send_event('E_POST_ACTION', DEFEND_ANIM, UP_BODY, 1)
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', DEFEND_ANIM, loop=False)
        super(Reload, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, None)
            self.send_event('E_UPBODY_BONE', (('biped root', 0), ('biped spine', 1)))
        if not self.continue_fire:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False)
        return


class AccumulateShoot8019(AccumulateShoot):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateShoot8019, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.enable_param_changed_by_buff()

    def read_data_from_custom_param(self):
        super(AccumulateShoot8019, self).read_data_from_custom_param()
        self.pre_anim_normal = self.custom_param.get('pre_anim', 'pan_start')
        self.pre_anim_defend = self.custom_param.get('pre_anim_defend', 'shd_pan_start')
        self.post_anim_normal = self.custom_param.get('post_anim', 'pan_end')
        self.post_anim_defend = self.custom_param.get('post_anim_defend', 'shd_pan_fire_pinjie')
        self._shoot_move_anim_beginning = 'enter'
        self.all_up_body_anim.add(self.pre_anim_normal)
        self.all_up_body_anim.add(self.pre_anim_defend)
        self.all_up_body_anim.add(self.post_anim_normal)
        self.all_up_body_anim.add(self.post_anim_defend)
        self._force_pre = True
        self.hold_tag = False
        self.post_tag = False
        self.is_sp = False

    def enter(self, leave_states):
        self.pre_anim = self.pre_anim_defend if self.ev_g_handy_shield_state() else self.pre_anim_normal
        super(AccumulateShoot8019, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_8019_SEC_BEGIN, ()], True)
        self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')

    def update(self, dt):
        super(AccumulateShoot8019, self).update(dt)
        if self.sub_state == self.SUB_ST_HOLD:
            if not self.hold_tag:
                self.send_event('E_8019_SEC_HOLD')
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_8019_SEC_HOLD, ()], True)
                self.hold_tag = True

    def _post_action(self):
        if self.ev_g_handy_shield_state():
            self.post_anim = self.post_anim_defend if 1 else self.post_anim_normal
            super(AccumulateShoot8019, self)._post_action()
            self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
            self.post_tag or self.send_event('E_8019_SEC_POST')
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_8019_SEC_POST, ()], True)
            self.post_tag = True

    def exit(self, enter_states):
        super(AccumulateShoot8019, self).exit(enter_states)
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        if self.ev_g_handy_shield_state():
            self.send_event('E_POST_ACTION', DEFEND_ANIM, UP_BODY, 1)
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', DEFEND_ANIM, loop=False)
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, DEFEND_ANIM)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_8019_SEC_END, ()], True)
        self.send_event('E_8019_SEC_EXIT')
        self.hold_tag = False
        self.post_tag = False

    def refresh_param_changed(self):
        if self.is_sp:
            self.weapon_pos = 4
        else:
            self.weapon_pos = 3


class Dash8019(OxRushNew):
    BIND_EVENT = OxRushNew.BIND_EVENT.copy()
    BIND_EVENT.update({'E_EXIT_DEFEND': 'on_exit_defend',
       'E_SWITCH_8019': 'on_switch'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Dash8019, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.enable_param_changed_by_buff()
        self.rush_duration_add = 0
        self.max_rush_duration = self.custom_param.get('max_rush_duration', 2.5) + self.rush_duration_add
        self.max_rush_duration_is_dirty = False
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted,
           'dash_auto_defend_8019': self.dash_setting
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self, *args):
        if not self.ev_g_is_avatar():
            return
        self.keep_defend_tag = global_data.player.get_setting_2(DASH_AUTO_DEFEND_8019)

    def destroy(self):
        self.process_event(False)
        super(Dash8019, self).destroy()

    def dash_setting(self, tag):
        self.keep_defend_tag = tag

    def read_data_from_custom_param(self):
        self.range_pitch_angle = self.custom_param.get('range_pitch_angle', [-60, -30])
        self.range_pitch_speed_ratio = self.custom_param.get('range_pitch_speed_ratio', [1.0, 0.3])
        min_angle, max_angle = self.range_pitch_angle
        min_ratio, max_ratio = self.range_pitch_speed_ratio
        self.one_angle_ratio = (max_ratio - min_ratio) / (max_angle - min_angle)
        self.pre_anim_defend = self.custom_param.get('pre_anim_defend', 'shd_dash_01')
        self.hit_anim_defend = self.custom_param.get('hit_anim_defend', 'dash_06')
        self.miss_anim_defend = self.custom_param.get('miss_anim_defend', 'dash_04')
        self.defend_state = DEFEND_OFF
        self.switching = False
        super(Dash8019, self).read_data_from_custom_param()

    def refresh_param_changed(self):
        self.max_rush_duration = self.custom_param.get('max_rush_duration', 2.5) + self.rush_duration_add
        if self.is_active:
            self.max_rush_duration_is_dirty = True
        else:
            self._register_sub_state_callbacks()

    def enter(self, leave_states):
        self.defend_state = copy.deepcopy(self.ev_g_handy_shield_state())
        if self.defend_state:
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
            if self.sd.ref_up_body_anim in (DEFEND_ANIM, DEFEND_EXIT_ANIM):
                self.send_event('E_CLEAR_UP_BODY_ANIM')
        elif self.keep_defend_tag:
            self.send_event('E_DASH_AUTO_DEFEND')
        super(Dash8019, self).enter(leave_states)
        return

    def exit(self, enter_states):
        if self.ev_g_handy_shield_state() and self.keep_defend_tag:
            self.send_event('E_POST_ACTION', DEFEND_ANIM, UP_BODY, 1)
            self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', DEFEND_ANIM, loop=False)
        if self.max_rush_duration_is_dirty:
            self.max_rush_duration_is_dirty = False
            self._register_sub_state_callbacks()
        super(Dash8019, self).exit(enter_states)

    def on_exit_defend(self):
        self.defend_state = DEFEND_OFF

    def on_begin_pre(self):
        pre_anim = self.ev_g_handy_shield_state() or self.pre_anim if 1 else self.pre_anim_defend
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', pre_anim, LOW_BODY, 1)

    def on_begin_rush(self):
        self.is_moving = True
        self.cur_speed = self.max_rush_speed
        self.send_event('E_ANIM_RATE', LOW_BODY, self.rush_anim_rate)
        self.send_event('E_POST_ACTION', self.rush_anim, LOW_BODY, 1, loop=True, blend_time=0.1)
        self.send_event('E_SHOW_DASH_LEFT_DURATION', self.max_rush_duration)

    def on_begin_hit(self):
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        hit_anim = self.ev_g_handy_shield_state() or self.hit_anim if 1 else self.hit_anim_defend
        self.send_event('E_ANIM_RATE', LOW_BODY, self.hit_anim_rate)
        self.send_event('E_POST_ACTION', hit_anim, LOW_BODY, 1, blend_time=0)
        self.sound_drive.run_end()
        self.is_moving = False
        create_screen_effect_directly('effect/fx/mecha/8019/camera/fx/dash_03.sfx')

    def on_begin_miss(self):
        miss_anim = self.ev_g_handy_shield_state() or self.miss_anim if 1 else self.miss_anim_defend
        self.send_event('E_ANIM_RATE', LOW_BODY, self.miss_anim_rate)
        self.send_event('E_POST_ACTION', miss_anim, LOW_BODY, 1)
        self.is_braking = True
        global_data.sound_mgr.play_sound_2d('m_8019_sprint_end_1p')

    def on_switch(self, tag):
        self.switching = tag

    def update(self, dt):
        StateBase.update(self, dt)
        if self.is_accelerating:
            self.cur_speed += self.acc_speed * dt
            if self.cur_speed > self.max_rush_speed:
                self.cur_speed = self.max_rush_speed
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.is_moving:
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            cam_forward = scn.active_camera.rotation_matrix.forward
            cam_pitch = scn.active_camera.rotation_matrix.pitch
            angle = math.degrees(cam_pitch)
            min_angle, max_angle = self.range_pitch_angle
            min_ratio, max_ratio = self.range_pitch_speed_ratio
            if angle > min_angle and angle < max_angle:
                cur_ratio = (angle - min_angle) * self.one_angle_ratio + min_ratio
            elif angle <= min_angle:
                cur_ratio = min_ratio
            else:
                cur_ratio = max_ratio
            walk_direction = self.get_walk_direction(cam_forward, cur_ratio)
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)

    def on_cam_rotate(self, *args):
        if self.is_active and self.is_moving:
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            cam_forward = scn.active_camera.rotation_matrix.forward
            cam_pitch = scn.active_camera.rotation_matrix.pitch
            angle = abs(math.degrees(cam_pitch))
            min_angle, max_angle = self.range_pitch_angle
            min_ratio, max_ratio = self.range_pitch_speed_ratio
            if angle > min_angle and angle < max_angle:
                cur_ratio = (angle - min_angle) * self.one_angle_ratio + min_ratio
            elif angle <= min_angle:
                cur_ratio = min_ratio
            else:
                cur_ratio = max_ratio
            walk_direction = cam_forward * (self.cur_speed * cur_ratio)
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)


class Defend(StateBase):
    BIND_EVENT = {'G_IS_DEFENDING': '_is_defending',
       'E_SWITCH_DEFEND': '_on_switch_defend',
       'E_TRY_SWITCH_DEFEND': '_on_try_switch_defend',
       'E_8019_SEC_BEGIN': '_on_sec_weapon_begin',
       'E_8019_SEC_END': '_on_sec_weapon_end',
       'E_DASH_AUTO_DEFEND': '_on_dash_auto_defend',
       'E_NOTIFY_CLEAR_RESET': '_on_clear_reset'
       }

    def _on_clear_reset(self):
        self._try_exit_defend()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Defend, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)

    def init_params(self):
        self.skill_id = self.custom_param.get('skill_id', 801953)
        self.defend_anim = self.custom_param.get('defend_anim', DEFEND_ANIM)
        self.defend_enter_anim = self.custom_param.get('defend_enter_anim', 'shd_start')
        self.defend_enter_anim_dur = self.custom_param.get('defend_enter_anim_dur', 0.6)
        self.defend_exit_anim = self.custom_param.get('defend_exit_anim', DEFEND_EXIT_ANIM)
        self.defend_exit_anim_dur = self.custom_param.get('defend_exit_anim_dur', 0.5)
        self.defend_shoot_anim = self.custom_param.get('defend_shoot_anim', 'shd_shoot')
        self.cur_try_state = None
        self.in_sec_weapon = False
        return

    def on_init_complete(self):
        super(Defend, self).on_init_complete()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self, *args):
        if not self.ev_g_is_avatar():
            return
        defend_state = self.ev_g_handy_shield_state()
        if defend_state == DEFEND_ON:
            if not self.is_active:
                if not self.check_can_active():
                    return
                self.active_self()
            self._try_enter_defend(upload=False, ignore_check=True)
        else:
            self.send_event('E_DO_SKILL', self.skill_id)
            self.cur_try_state = DEFEND_OFF
            self.send_event('E_EXIT_DEFEND')
            self.disable_self()

    def check_can_active(self, only_avatar=True):
        if self.ev_g_is_avatar():
            cur_state = self.ev_g_cur_state()
            if MC_DASH not in cur_state:
                ret = self.ev_g_check_enter_defend()
                if not ret:
                    return False
        return self.ev_g_status_check_pass(self.sid, only_avatar=only_avatar)

    def check_can_deactive(self):
        cur_state = self.ev_g_cur_state()
        if MC_DASH not in cur_state and MC_SECOND_WEAPON_ATTACK not in cur_state:
            return True
        return False

    def check_transitions(self):
        pass

    def enter(self, leave_states):
        super(Defend, self).enter(leave_states)

    def update(self, dt):
        super(Defend, self).update(dt)

    def exit(self, enter_states):
        super(Defend, self).exit(enter_states)
        if enter_states & {MC_DEAD, MC_DRIVER_LEAVING}:
            self._try_exit_defend()

    def _on_dash_auto_defend(self):
        super(Defend, self).action_btn_down()
        if not self.check_can_cast_skill():
            return False
        cur_state = self.ev_g_cur_state()
        if MC_DASH in cur_state or MC_SECOND_WEAPON_ATTACK in cur_state:
            return False
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_SWITCH_8019', True)
        self.send_event('E_POST_ACTION', self.defend_enter_anim, UP_BODY, 7)

        def _enter_defend_anim():
            cur_state = self.ev_g_cur_state()
            if not {
             MC_RUN, MC_SECOND_WEAPON_ATTACK, MC_DASH} & cur_state:
                self.send_event('E_POST_ACTION', self.defend_anim, UP_BODY, 1)
                self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.defend_anim, loop=False)
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_SHOOT, self.defend_shoot_anim, loop=False)
            self.send_event('E_REPLACE_SHOOT_ANIM', self.defend_shoot_anim)
            self.send_event('E_SWITCH_8019', False)

        self.send_event('E_UP_RUN_ANIM_8019', DEFEND_ON)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.defend_anim)
        self.delay_call(0.1, _enter_defend_anim)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8019_shd_on', 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND,
         (
          1, ('m_8019_shd_on', 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)
        self.cur_try_state = DEFEND_ON
        self._upload_state(state=DEFEND_ON, ignore_hp=True)

    def action_btn_down(self):
        super(Defend, self).action_btn_down()
        if not self.check_can_cast_skill():
            return False
        if self.is_active and not self.check_can_deactive():
            return False
        cur_state = self.ev_g_cur_state()
        if MC_DASH in cur_state or MC_SECOND_WEAPON_ATTACK in cur_state:
            return False
        if not self.is_active:
            self._try_enter_defend()
        else:
            self._try_exit_defend()
        return True

    def _on_try_switch_defend(self, state, ignore_check=False):
        if state == DEFEND_ON:
            self._try_enter_defend(upload=False, ignore_check=ignore_check)
            self._do_enter_defend(ignore_check=ignore_check)
        elif state == DEFEND_OFF:
            self._try_exit_defend(upload=False)
            self._do_exit_defend(positive=False)

    def _on_switch_defend(self, state, ret):
        if ret:
            if state == DEFEND_ON:
                self._do_enter_defend()
            elif state == DEFEND_OFF:
                self._do_exit_defend(positive=True)
        elif self.is_active and (self.cur_try_state == DEFEND_OFF or not self.cur_try_state):
            self._try_enter_defend(upload=False)
        elif not self.is_active and (self.cur_try_state == DEFEND_ON or not self.cur_try_state):
            self._try_exit_defend(upload=False)

    def _upload_state(self, state, ignore_hp=False):
        self.send_event('E_CALL_SYNC_METHOD', 'try_switch_defend', (state, ignore_hp), True)

    def _try_enter_defend(self, upload=True, ignore_check=False):
        if not ignore_check:
            if not self.check_can_active():
                return
        self.send_event('E_DO_SKILL', self.skill_id)
        self._play_enter_anim()
        self.cur_try_state = DEFEND_ON
        if upload:
            self._upload_state(state=DEFEND_ON)

    def _play_enter_anim(self):
        self.send_event('E_SWITCH_8019', True)
        self.send_event('E_POST_ACTION', self.defend_enter_anim, UP_BODY, 7)

        def _enter_defend_anim():
            cur_state = self.ev_g_cur_state()
            if not {
             MC_RUN, MC_SECOND_WEAPON_ATTACK, MC_DASH} & cur_state:
                self.send_event('E_POST_ACTION', self.defend_anim, UP_BODY, 1)
                self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.defend_anim, loop=False)
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_SHOOT, self.defend_shoot_anim, loop=False)
            self.send_event('E_REPLACE_SHOOT_ANIM', self.defend_shoot_anim)
            self.send_event('E_SWITCH_8019', False)

        self.send_event('E_UP_RUN_ANIM_8019', DEFEND_ON)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.defend_anim)
        self.delay_call(self.defend_enter_anim_dur, _enter_defend_anim)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8019_shd_on', 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, ('m_8019_shd_on', 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)

    def _do_enter_defend(self, ignore_check=False):
        if not self.is_active:
            if not ignore_check:
                if not self.check_can_active():
                    return
            self.active_self()
            self.send_event('E_ENTER_DEFEND')

    def _try_exit_defend(self, upload=True):
        self.send_event('E_DO_SKILL', self.skill_id)
        self._play_exit_anim()
        self.cur_try_state = DEFEND_OFF
        if upload:
            self._upload_state(DEFEND_OFF)

    def _play_exit_anim(self):
        self.send_event('E_SWITCH_8019', True)
        if self.ev_g_is_avatar():
            cur_state = self.ev_g_cur_state()
            if MC_SECOND_WEAPON_ATTACK not in cur_state:
                self.send_event('E_POST_ACTION', self.defend_exit_anim, UP_BODY, 7)
        elif not self.in_sec_weapon:
            self.send_event('E_POST_ACTION', self.defend_exit_anim, UP_BODY, 7)
        self.send_event('E_UP_RUN_ANIM_8019', DEFEND_OFF)
        global_data.game_mgr.delay_exec(self.defend_exit_anim_dur, self._exit_defend_anim)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8019_shd_off', 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, ('m_8019_shd_off', 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)

    def _exit_defend_anim(self):
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
        if self.sd.ref_up_body_anim in (self.defend_anim, self.defend_exit_anim):
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.ev_g_is_avatar():
            cur_state = self.ev_g_cur_state()
            if MC_SECOND_WEAPON_ATTACK not in cur_state:
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        elif not self.in_sec_weapon:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_SHOOT, None)
        self.send_event('E_RESET_SHOOT_ANIM')
        self.send_event('E_SWITCH_8019', False)
        return

    def _do_exit_defend(self, positive=True):
        if not positive:
            self.send_event('E_EXIT_DEFEND_N')
        else:
            self.send_event('E_EXIT_DEFEND_P')
        self.send_event('E_EXIT_DEFEND')
        self.disable_self()

    def _on_sec_weapon_begin(self, *args):
        self.in_sec_weapon = True

    def _on_sec_weapon_end(self, *args):
        self.in_sec_weapon = False

    def refresh_action_param(self, action_param, custom_param):
        super(Defend, self).refresh_action_param(action_param, custom_param)

    def refresh_param_changed(self):
        super(Defend, self).refresh_param_changed()

    def _is_defending(self):
        return self.is_active

    def destroy(self):
        self.process_event(False)
        super(Defend, self).destroy()