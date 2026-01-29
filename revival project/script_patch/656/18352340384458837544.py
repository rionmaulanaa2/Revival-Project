# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8007.py
from __future__ import absolute_import
import six
from .StateBase import StateBase
from .ShootLogic import Reload
from .JumpLogic import Fall, OnGround, SuperJumpUp
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from logic.gutils.character_ctrl_utils import apply_horizon_offset_speed
from logic.gutils import detection_utils
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from data.camera_state_const import AIM_MODE
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gcommon.common_utils import status_utils
from logic.gcommon.common_const.attr_const import ATTR_ACCUMULATE_ENERGY_INIT_VALUE_RATIO
from common.utils.timer import CLOCK
from logic.gcommon import editor
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import world
import wwise

@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid','explain': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x8a\x80\xe8\x83\xbdid\xef\xbc\x8c\xe5\xa6\x82\xe6\x9e\x9c\xe4\xb8\x8d\xe5\xa1\xab\xe5\x88\x99\xe9\x80\x9a\xe5\xb8\xb8\xe4\xb8\x8d\xe6\x89\xa3\xe9\x99\xa4\xe7\x87\x83\xe6\x96\x99'},('jump_speed', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 200},('jump_acc', 'meter'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 50},('h_offset_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6','explain': '\xe5\x9c\xa8\xe8\xa7\x92\xe8\x89\xb2\xe6\xb5\xae\xe7\xa9\xba\xe6\x97\xb6\xef\xbc\x8c\xe6\x91\x87\xe6\x9d\x86\xe5\x8f\xaf\xe4\xbb\xa5\xe7\xbb\x99\xe4\xb8\x8e\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_acc', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','explain': '\xe5\x9c\xa8\xe8\xa7\x92\xe8\x89\xb2\xe6\xb5\xae\xe7\xa9\xba\xe6\x97\xb6\xef\xbc\x8c\xe6\x91\x87\xe6\x9d\x86\xe5\x8f\xaf\xe4\xbb\xa5\xe7\xbb\x99\xe4\xb8\x8e\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('h_speed_ratio', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6\xe8\xa1\xb0\xe5\x87\x8f','min_val': 0,'max_val': 1,'explain': '\xe8\xb5\xb7\xe8\xb7\xb3\xe7\x9e\xac\xe9\x97\xb4\xe7\x9a\x84\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6\xe8\xa1\xb0\xe5\x87\x8f\xe7\x8e\x870\xe4\xb8\xba\xe6\x9c\x80\xe5\xa4\xa7\xef\xbc\x8c1\xe4\xbf\x9d\xe6\x8c\x81\xe5\x8e\x9f\xe9\x80\x9f\xe5\xba\xa6'}})
class JumpUp8007(StateBase):
    BIND_EVENT = {'E_ENABLE_BREAK_BY_STAND': 'enable_break_by_stand'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.jump_speed = self.custom_param.get('jump_speed', 5) * NEOX_UNIT_SCALE
        self.jump_acc = self.custom_param.get('jump_acc', 20) * NEOX_UNIT_SCALE
        self.h_offset_speed = self.custom_param.get('h_offset_speed', 15) * NEOX_UNIT_SCALE
        self.h_offset_acc = self.custom_param.get('h_offset_acc', 25) * NEOX_UNIT_SCALE
        self.h_speed_ratio = self.custom_param.get('h_speed_ratio', 1.0)
        self.duration = self.custom_param.get('duration', 2)
        anim_duration = self.custom_param.get('anim_duration', 0.667)
        self.time_scale = anim_duration / self.duration
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(JumpUp8007, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()

    def action_btn_down(self):
        if self.ev_g_can_quick_jump():
            self.send_event('E_ADD_WHITE_STATE', {self.sid}, self.sid + 1)
            self.send_event('E_DISABLE_STATE', self.sid + 1)
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        if not self.is_active:
            self.active_self()

    def enter(self, leave_states):
        if MC_DASH in self.ev_g_cur_state():
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_RESET_GRAVITY')
        super(JumpUp8007, self).enter(leave_states)
        self.passed_time = 0
        self.cur_jump_speed = self.jump_speed
        self.send_event('E_ANIM_RATE', LOW_BODY, self.time_scale)
        walk_direction = self.ev_g_char_walk_direction()
        self.send_event('E_SET_WALK_DIRECTION', walk_direction * self.h_speed_ratio)
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)

    def update(self, dt):
        super(JumpUp8007, self).update(dt)
        self.passed_time += dt
        if self.passed_time >= self.duration:
            return
        super(JumpUp8007, self).update(dt)
        self.cur_jump_speed += self.jump_acc * dt
        self.send_event('E_JUMP', self.cur_jump_speed)
        apply_horizon_offset_speed(self, dt, self.h_offset_speed, self.h_offset_acc)

    def exit(self, enter_states):
        super(JumpUp8007, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1)
        if MC_JUMP_2 not in enter_states:
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)

    def refresh_action_param(self, action_param, custom_param):
        super(JumpUp8007, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()

    def enable_break_by_stand(self):
        if self.is_active:
            self.passed_time = self.duration
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)


class Fall8007(Fall):
    BIND_EVENT = Fall.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_BREAK_BY_STAND': 'enable_break_by_stand'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Fall8007, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.is_in_dash = False

    def _exit_coyote_time(self):
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        if self.is_in_dash:
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)

    def enter(self, leave_states):
        super(Fall8007, self).enter(leave_states)
        if MC_JUMP_1 not in leave_states and MC_SUPER_JUMP not in leave_states:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.is_in_dash = False
        if MC_DASH in self.ev_g_cur_state():
            self.is_in_dash = True
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)

    def exit(self, enter_states):
        super(Fall8007, self).exit(enter_states)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE, is_interpolate=True)

    def enable_break_by_stand(self):
        if self.is_active:
            self.is_in_dash = True
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)


class OnGround8007(OnGround):

    def on_ground(self, *args):
        cur_states = self.ev_g_cur_state()
        if MC_DASH in cur_states:
            if MC_STAND not in cur_states:
                self.send_event('E_ACTIVE_STATE', MC_STAND)
            return
        super(OnGround8007, self).on_ground(*args)


class SuperJumpUp8007(SuperJumpUp):
    BIND_EVENT = SuperJumpUp.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_BREAK_BY_STAND': 'enable_break_by_stand'
       })

    def enter(self, leave_states):
        super(SuperJumpUp8007, self).enter(leave_states)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if MC_DASH in self.ev_g_cur_state():
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)

    def enable_break_by_stand(self):
        if self.is_active:
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)


class Reload8007(Reload):
    BIND_EVENT = Reload.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ANIMATOR_LOADED': ('on_load_animator_complete', 99)
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8007, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.last_on_ground = True
        self.tick_interval = 0.03

    def enter(self, leave_states):
        super(Reload8007, self).enter(leave_states)
        self.last_on_ground = True

    def update(self, dt):
        super(Reload8007, self).update(dt)
        if self.last_on_ground != self.ev_g_on_ground():
            self.last_on_ground = not self.last_on_ground
            if self.last_on_ground:
                self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
                if self.sd.ref_rocker_dir is not None:
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', self.sd.ref_rocker_dir.x, self.sd.ref_rocker_dir.z)
            else:
                self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
                self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
        return

    def exit(self, enter_states):
        super(Reload8007, self).exit(enter_states)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)

    def on_reloading_bullet(self, *args, **kwargs):
        super(Reload8007, self).on_reloading_bullet(*args, **kwargs)
        self.sound_custom_start()

    def on_reloaded(self, *args, **kwargs):
        super(Reload8007, self).on_reloaded(*args, **kwargs)
        self.sound_custom_end()

    def on_load_animator_complete(self, *args):
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)


class OpenAimCamera(StateBase):
    BIND_EVENT = {'E_FIRE': 'on_fire',
       'E_DEATH': 'on_mecha_death',
       'G_AIM_SWITCHING': 'get_is_switching',
       'E_MOD_INIT_ENERY': 'modify_init_energy',
       'E_ACC_ACCUMULATE_CD': 'acc_accumulate_cd',
       'TRY_STOP_WEAPON_ATTACK': 'disable_self',
       'G_AUTO_ENERGY': 'get_accumulate_energy',
       'E_WEAPON_BULLET_CHG': 'on_reloaded',
       'E_RELOADING': 'on_reloading_begin',
       'E_TRY_QUIT_OPEN_AIM': 'try_quit_open_aim',
       'E_EXIT_FOCUS_CAMERA': 'on_celebrate'
       }
    AIM_NOT_OPEN = 0
    AIM_OPENING = 1
    AIM_OPENED = 2
    AIM_CLOSING = 3
    AIM_ANIM_IDLE = 0
    AIM_ANIM_FIRE = 1
    AIM_ANIM_RELOAD = 2
    energy_sound_dict = {0: 52,
       5: 60,
       10: 80,
       15: 100
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(OpenAimCamera, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.aim_lens = self.custom_param.get('aim_lens', 0)
        self.switch_action = self.custom_param.get('switch_action', {})
        self.open_aim_anim = self.custom_param.get('open_aim_anim', None)
        self.open_aim_duration = self.custom_param.get('open_aim_duration', 1.3)
        self.close_aim_anim = self.custom_param.get('close_aim_anim', None)
        self.close_aim_duration = self.custom_param.get('close_aim_duration', 1.0)
        self.idle_anim = self.custom_param.get('idle_anim', None)
        self.snipe_idle_anim = self.custom_param.get('snipe_idle_anim', None)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.close_break_time = self.custom_param.get('close_break_time', self.close_aim_duration)
        self.close_break_states = self.custom_param.get('close_break_states', [])
        self.close_break_states = status_utils.convert_status(self.close_break_states)
        state_exit_trigger_setting_type = self.custom_param.get('state_exit_trigger_setting_type', None)
        self._exit_trigger_setting_key = self.convert_to_exit_trigger_setting_key(state_exit_trigger_setting_type)
        self.aim_state = self.AIM_NOT_OPEN
        self.can_close = False
        self.close_aim_clock = 0
        self.can_break_close = False
        self.aim_model = None
        self.aim_sfx = None
        self.is_open = False
        self.default_energy = 0
        self.cur_energy = 0
        self.max_energy = 2
        self.fire_weapon = None
        self.energy_sound_id = None
        self.aim_anim_status = self.AIM_ANIM_IDLE
        self.aim_anim_duration = 0.0
        return

    def on_init_complete(self):
        super(OpenAimCamera, self).on_init_complete()
        self.send_event('E_ADD_LOCK_AIM_DIR_CAM_MODE', AIM_MODE)

    def exit_by_setting_when_btn_up(self):
        if self._exit_trigger_setting_key is not None and self.ev_g_is_avatar():
            setting_val = global_data.player.get_setting_2(self._exit_trigger_setting_key)
            if setting_val is not None:
                if setting_val:
                    return True
        return False

    @classmethod
    def convert_to_exit_trigger_setting_key(cls, state_exit_trigger_setting_type):
        from logic.gcommon.common_const import ui_operation_const as uoc
        if state_exit_trigger_setting_type == 8007:
            return uoc.AIM_TRIGGER_PRESS_8007
        else:
            return None
            return None

    def action_btn_down(self):
        if self.aim_state == self.AIM_CLOSING:
            self.disable_self()
        if not self.check_can_active():
            return False
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        super(OpenAimCamera, self).action_btn_down()
        if self.aim_state == self.AIM_NOT_OPEN:
            if not self.check_can_active():
                return False
            self.active_self()
        else:
            self.can_close = True
        return True

    def enter(self, leave_states):
        super(OpenAimCamera, self).enter(leave_states)
        self.can_close = False
        self.close_aim_clock = 0
        self.can_break_close = False
        self.aim_state = self.AIM_OPENING
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.fire_weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        self.send_event('E_OPEN_AIM_CAMERA_ENTER', PART_WEAPON_POS_MAIN2)
        self.send_event('E_SET_ACTION_SELECTED', 'action4', True)
        self.send_event('E_POST_ACTION', self.open_aim_anim, UP_BODY, 1, loop=False)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', self.snipe_idle_anim, loop=True)
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_CHANGE_WEAPON_POS', PART_WEAPON_POS_MAIN2)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if weapon:
            self.max_energy = weapon.get_accumulate_max_time()
            self.default_energy = self.max_energy * self.unit_obj.ev_g_add_attr(ATTR_ACCUMULATE_ENERGY_INIT_VALUE_RATIO, weapon.get_item_id())
        self.cur_energy = self.default_energy
        if not self.energy_sound_id:
            if not self.ev_g_reloading():
                self.play_energy_sound()
        else:
            global_data.sound_mgr.stop_playing_id(self.energy_sound_id)
            self.energy_sound_id = None
        return

    def update(self, dt):
        super(OpenAimCamera, self).update(dt)
        if self.fire_weapon.get_bullet_num() >= self.fire_weapon.get_cost_ratio() and not self.ev_g_reloading():
            self.cur_energy += dt
        self.cur_energy = min(self.cur_energy, self.max_energy)
        if self.aim_state == self.AIM_OPENING:
            if self.elapsed_time >= self.open_aim_duration:
                self.send_event('E_SET_ACTION_SELECTED', 'action4', True)
                self.send_event('E_CLEAR_UP_BODY_ANIM')
                self.send_event('E_RESET_ROTATION', 0)
                if self.aim_anim_status == self.AIM_ANIM_IDLE:
                    self.send_event('E_OPEN_AIM_CAMERA_ANIM')
                self.on_switch_action(1)
                self.on_open_camera(True)
                self.aim_state = self.AIM_OPENED
        elif self.aim_state == self.AIM_OPENED:
            self.send_event('E_SET_ACTION_SELECTED', 'action4', True)
            if self.aim_anim_status != self.AIM_ANIM_IDLE:
                self.aim_anim_duration -= dt
                if self.aim_anim_duration <= 0:
                    self.aim_anim_status = self.AIM_ANIM_IDLE
                    self.send_event('E_OPEN_AIM_CAMERA_ANIM')
        elif self.aim_state == self.AIM_CLOSING:
            self.close_aim_clock += dt
            if not self.can_break_close and self.close_aim_clock >= self.close_break_time:
                self.can_break_close = True
                self.send_event('E_ADD_WHITE_STATE', self.close_break_states, self.sid)
                self.send_event('E_IGNORE_RELOAD_ANIM', False)
            if self.close_aim_clock >= self.close_aim_duration:
                self.disable_self()

    def exit(self, enter_states):
        super(OpenAimCamera, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.exit_aim_state()
        self.aim_state = self.AIM_NOT_OPEN
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
        if MC_RELOAD not in self.ev_g_cur_state():
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CHANGE_WEAPON_POS', PART_WEAPON_POS_MAIN1)
        if self.energy_sound_id:
            global_data.sound_mgr.stop_playing_id(self.energy_sound_id)
            self.energy_sound_id = None
        return

    def destroy(self):
        self.send_event('E_OPEN_AIM_CAMERA_EXIT')
        super(OpenAimCamera, self).destroy()

    def on_reloading_begin(self, time, times, weapon_pos):
        if self.is_active:
            self.send_event('E_OPEN_AIM_CAMERA_RELOAD')
            self.aim_anim_status = self.AIM_ANIM_RELOAD
            self.aim_anim_duration = time

    def on_reloaded(self, *args):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_RELOADED, ()))
        if not self.energy_sound_id and self.aim_state == self.AIM_OPENED:
            self.play_energy_sound()
        if self.aim_anim_status == self.AIM_ANIM_RELOAD:
            self.aim_anim_status = self.AIM_ANIM_IDLE

    def action_btn_up(self):
        super(OpenAimCamera, self).action_btn_up()
        exit_by_setting_when_btn_up = self.exit_by_setting_when_btn_up()
        if not self.is_active:
            if exit_by_setting_when_btn_up:
                self.disable_self()
                return True
            else:
                return False

        if self.can_close or exit_by_setting_when_btn_up:
            self.exit_aim_state()
            self.sound_drive.run_end()
            if self.energy_sound_id:
                global_data.sound_mgr.stop_playing_id(self.energy_sound_id)
                self.energy_sound_id = None
        self.can_close = True
        return True

    def on_celebrate(self, *args):
        if not self.is_active:
            return
        else:
            self.disable_self()
            self.exit_aim_state()
            self.sound_drive.run_end()
            if self.energy_sound_id:
                global_data.sound_mgr.stop_playing_id(self.energy_sound_id)
                self.energy_sound_id = None
            return

    def on_open_camera(self, is_open):
        if not self.aim_lens:
            return
        self.is_open = is_open
        self.send_event('E_RECORD_CUR_CAM_AIM_DIR')
        if is_open:
            self.send_event('E_OPEN_AIM_CAMERA_PLACE')
            weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
            if weapon and weapon.get_bullet_num() < weapon.get_cost_ratio():
                self.send_event('E_TRY_RELOAD', PART_WEAPON_POS_MAIN2)
        self.send_event('E_OPEN_AIM_CAMERA', is_open)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_OPEN_AIM_CAMERA, (is_open,)))

    def on_switch_action(self, index):
        if not self.switch_action:
            return
        for key, val in six.iteritems(self.switch_action):
            self.send_event('E_SWITCH_ACTION', key, val[index], False)

    def on_fire(self, f_cdtime, weapon_pos, *args):
        self.cur_energy = 0
        if weapon_pos != PART_WEAPON_POS_MAIN2:
            return
        else:
            if self.is_active and self.aim_anim_status == self.AIM_ANIM_IDLE:
                self.send_event('E_OPEN_AIM_CAMERA_ON_FIRE')
                self.aim_anim_status = self.AIM_ANIM_FIRE
                self.aim_anim_duration = f_cdtime - 0.1
            if self.energy_sound_id:
                global_data.sound_mgr.stop_playing_id(self.energy_sound_id)
                self.energy_sound_id = None
            self.play_energy_sound()
            return

    def exit_aim_state(self):
        if self.aim_state == self.AIM_OPENED:
            self.on_open_camera(False)
        if self.aim_state != self.AIM_CLOSING:
            self.aim_state = self.AIM_CLOSING
            self.on_switch_action(0)
            self.send_event('E_POST_ACTION', self.close_aim_anim, UP_BODY, 1)
        self.send_event('E_SET_ACTION_SELECTED', 'action4', False)
        self.send_event('E_OPEN_AIM_CAMERA_EXIT')

    def get_accumulate_energy(self):
        return (
         PART_WEAPON_POS_MAIN2, self.cur_energy)

    def get_is_switching(self):
        is_switching = False
        if self.aim_state == self.AIM_OPENING:
            is_switching = True
        elif self.aim_state == self.AIM_CLOSING and not self.can_break_close:
            is_switching = True
        return is_switching

    def modify_init_energy(self, ratio):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if weapon:
            self.max_energy = weapon.get_accumulate_max_time()
            self.unit_obj.send_event('E_MOD_ADD_ATTR', ATTR_ACCUMULATE_ENERGY_INIT_VALUE_RATIO, ratio, weapon.get_item_id())

    def acc_accumulate_cd(self, dec_percent, wp_pos):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if weapon:
            weapon.set_accumulate_dec_percent(dec_percent)
        rtpc_val = self.energy_sound_dict.get(dec_percent, None)
        if rtpc_val:
            wwise.SoundEngine.SetRTPCValue('mecha8007_weapon1_power_notice', rtpc_val)
        return

    def try_quit_open_aim(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_DASH}, self.sid)
        self.action_btn_down()
        self.action_btn_up()

    def play_energy_sound(self):
        self.energy_sound_id = global_data.sound_mgr.play_sound_2d('m_8007_weapon1_power_notice_1p')


def __editor_dash8007_setter(self, v):
    self.ini_max_jump_dist = v * NEOX_UNIT_SCALE
    self.max_jump_dist = self.ini_max_jump_dist + self.max_jump_dist_add * NEOX_UNIT_SCALE


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('max_jump_dist', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe6\xa3\x80\xe6\xb5\x8b\xe8\xb7\x9d\xe7\xa6\xbb','explain': '\xe8\xa7\x92\xe8\x89\xb2\xe7\x9a\x84\xe8\xb5\xb0\xe8\xb7\xaf\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc','getter': lambda self: self.ini_max_jump_dist / NEOX_UNIT_SCALE,
                                'setter': lambda self, v: __editor_dash8007_setter(self, v)
                                },
   ('pre_time', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4'},('cast_time', 'param'): {'zh_name': '\xe6\x96\xbd\xe6\xb3\x95\xe6\x97\xb6\xe9\x97\xb4'},('cast_anim_time', 'param'): {'zh_name': '\xe6\x96\xbd\xe6\xb3\x95\xe5\x8a\xa8\xe7\x94\xbb\xe6\x80\xbb\xe9\x95\xbf\xe5\xba\xa6'},('cast_shadow_time', 'param'): {'zh_name': '\xe6\xae\x8b\xe5\xbd\xb1\xe5\x8f\x91\xe5\xb0\x84\xe7\x9a\x84\xe5\x85\xb3\xe9\x94\xae\xe5\xb8\xa7'},('post_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe6\x97\xb6\xe9\x95\xbf'},('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe7\xa1\xac\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'},('shadow_stay_time', 'param'): {'zh_name': '\xe6\xae\x8b\xe5\xbd\xb1\xe6\xae\x8b\xe7\x95\x99\xe6\x97\xb6\xe9\x97\xb4'},('timer_rate', 'param'): {'zh_name': '\xe6\x95\xb4\xe4\xbd\x93\xe6\xb5\x81\xe7\xa8\x8b\xe9\x80\x9f\xe7\x8e\x87\xe7\xbc\xa9\xe6\x94\xbe'}})
class Dash8007(StateBase):
    BIND_EVENT = {'E_IMMOBILIZED': 'end_detecting',
       'E_ON_FROZEN': 'end_detecting'
       }
    PRE = 0
    SCAN = 1
    PREVIEW = 2
    TELEPORT = 3
    POST = 4

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8007, self).init_from_dict(unit_obj, bdict, sid, info)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.mecha_id = str(bdict['mecha_id'])
        self.skill_id = self.custom_param.get('skill_id', 800751)
        self.ini_max_jump_dist = self.custom_param.get('max_jump_dist', 50) * NEOX_UNIT_SCALE
        self.max_jump_dist = self.ini_max_jump_dist
        self.max_jump_dist_add = 0.0
        self.pre_anim = self.custom_param.get('pre_anim', 'teleport_01')
        self.hold_anim = self.custom_param.get('hold_anim', 'teleport_02')
        self.cast_anim = self.custom_param.get('cast_anim', 'teleport_03')
        self.post_anim = self.custom_param.get('post_anim', 'teleport_04')
        self.pre_time = self.custom_param.get('pre_time', 0.8)
        self.cast_time = self.custom_param.get('cast_time', 1.0)
        self.cast_anim_time = self.custom_param.get('cast_anim_time', 2.3)
        self.cast_shadow_time = self.custom_param.get('cast_shadow_time', 0.26)
        self.post_time = self.custom_param.get('post_time', 0.6)
        self.post_break_time = self.custom_param.get('post_break_time', 0.4)
        self.shadow_stay_time = self.custom_param.get('shadow_stay_time', 0.3)
        self.cast_fast_forward_time = 0.2
        self.timer_rate = self.custom_param.get('timer_rate', 1.5)
        self.last_move_time = 0
        self.post_forbid_state = self.custom_param.get('post_forbid_state', None)
        if self.post_forbid_state:
            self.post_forbid_state = status_utils.convert_status(self.post_forbid_state)
        self.sub_state = -1
        self.target_pos = None
        self.target_sfx = None
        self.target_sfx_id = None
        self.detecting = False
        self.in_free_cam = False
        self.immediately_teleport = False
        self.need_reset_gravity = False
        self.register_substate_callback(self.PRE, 0, self.on_pre)
        self.register_substate_callback(self.SCAN, 0, self.on_scan)
        self.register_substate_callback(self.PREVIEW, 0, self.on_preview)
        self.register_substate_callback(self.TELEPORT, 0, self.on_teleport)
        self.register_substate_callback(self.POST, 0, self.on_post)
        self.enable_param_changed_by_buff()
        return

    def refresh_param_changed(self):
        self.max_jump_dist = self.ini_max_jump_dist + self.max_jump_dist_add * NEOX_UNIT_SCALE

    def on_pre(self):
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.action_cancel, True)
        self.detecting = True
        detection_utils.start_jump_pos_detect(self, self.max_jump_dist, detect_callback=self.detecting_callback)
        detection_utils.detect_jump_pos_wrapper()
        self.send_event('E_POST_ACTION', self.pre_anim, UP_BODY, 1, loop=False, timeScale=self.timer_rate)

        def swich_to_scan():
            self.sub_state = self.SCAN

        self.delay_call(self.pre_time, swich_to_scan)
        return

    def on_scan(self):
        self.send_event('E_POST_ACTION', self.hold_anim, UP_BODY, 1, loop=True, timeScale=self.timer_rate)
        if self.immediately_teleport:
            self.end_detecting()
            if self.target_pos:
                self.sub_state = self.PREVIEW
            else:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(80704))
                self.disable_self()

    def _enter_free_camera(self):
        if global_data.player and global_data.player.logic and self.is_active:
            global_data.player.logic.send_event('E_FREE_CAMERA_STATE', True)
            self.in_free_cam = True

    def on_preview(self):
        if self.ev_g_is_avatar():
            global_data.game_mgr.delay_exec(0.1, self._enter_free_camera)
        if self.post_forbid_state:
            self.send_event('E_ADD_BLACK_STATE', self.post_forbid_state)
            self.send_event('E_BRAKE')
        start_pos = self.ev_g_position()
        start_pos = (start_pos.x, start_pos.y, start_pos.z)
        end_pos = (self.target_pos.x, self.target_pos.y, self.target_pos.z)
        self.delay_call(self.cast_shadow_time, lambda : self.send_event('E_SHOW_VISUAL_PATH', start_pos, end_pos, self.cast_time, self.shadow_stay_time))
        self.on_teleport()

    def on_teleport(self):
        self.send_event('E_DO_SKILL', self.skill_id, self.target_pos, self.cast_time)
        self.send_event('E_POST_ACTION', self.cast_anim, UP_BODY, 1, loop=False, timeScale=self.timer_rate)

        def fast_forward():
            last_time = self.cast_anim_time - self.cast_time + self.cast_fast_forward_time
            scale = last_time / self.cast_fast_forward_time
            self.send_event('E_ANIM_RATE', UP_BODY, scale)

        self.delay_call(self.cast_time - self.cast_fast_forward_time, fast_forward)
        self.delay_call(self.cast_time + self.cast_shadow_time, lambda : self.set_sub_state(self.POST))
        self.send_event('E_GRAVITY', 0)
        self.need_reset_gravity = True
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_STEP_HEIGHT', 6 * NEOX_UNIT_SCALE)
        self.send_event('E_ENABLE_POS_CHANGE_NOTIFY', False)
        self.last_move_time = self.cast_time + self.cast_shadow_time
        self.sound_custom_start()
        global_data.emgr.play_game_voice.emit('rush')

    def reach_target_cb(self):
        if self.need_reset_gravity:
            self.send_event('E_RESET_GRAVITY')
            self.need_reset_gravity = False
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_RESET_STEP_HEIGHT')
        pos = self.ev_g_foot_position()
        self.send_event('E_SET_POSITION_FORCE', pos)

    def _leave_free_camera(self):
        if self.in_free_cam:
            camera = world.get_active_scene().active_camera
            global_data.emgr.force_set_last_camera_tarns.emit(camera.rotation_matrix)
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_FREE_CAMERA_STATE', False)
            self.in_free_cam = False

    def on_post(self):
        if self.ev_g_is_avatar():
            self._leave_free_camera()
        self.send_event('E_POST_ACTION', self.post_anim, UP_BODY, 1, loop=False, timeScale=self.timer_rate)
        self.send_event('E_ENABLE_POS_CHANGE_NOTIFY', True)
        self.reach_target_cb()

        def break_post():
            self.send_event('E_CLEAR_BLACK_STATE')

        self.delay_call(self.post_break_time, break_post)
        self.delay_call(self.post_time, self.disable_self)

    def enter(self, leave_states):
        super(Dash8007, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.create_detect_sfx()
        self.sub_state = self.PRE
        self.target_pos = None
        self.immediately_teleport = False
        self.need_reset_gravity = False
        self.send_event('E_ENABLE_BREAK_BY_STAND')
        return

    def update(self, dt):
        super(Dash8007, self).update(dt)
        self.last_move_time -= dt * self.timer_rate
        if self.last_move_time >= 0.03:
            from_pos = self.ev_g_foot_position()
            direct = from_pos - self.target_pos
            dash_speed = -direct * (1 / self.last_move_time)
            self.send_event('E_SET_WALK_DIRECTION', dash_speed, self.reach_target_cb, self.target_pos)

    def set_sub_state(self, state):
        self.sub_state = state

    def exit(self, enter_states):
        self.sound_custom_end()
        if self.ev_g_is_avatar():
            self._leave_free_camera()
        super(Dash8007, self).exit(enter_states)
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.target_pos = None
        self.sub_state = -1
        self.end_detecting()
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_ANIM_RATE', UP_BODY, 1)
        if self.need_reset_gravity:
            self.send_event('E_RESET_GRAVITY')
            self.need_reset_gravity = False
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_HIDE_VISUAL_PATH')
        self.send_event('E_ENABLE_POS_CHANGE_NOTIFY', True)
        self.last_move_time = 0
        return

    def destroy(self):
        if self.ev_g_is_avatar():
            self._leave_free_camera()
        self.end_detecting()
        super(Dash8007, self).destroy()

    def action_btn_down(self):
        if self.is_active:
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.check_can_active():
            if MC_SECOND_WEAPON_ATTACK in self.ev_g_cur_state():
                self.send_event('E_TRY_QUIT_OPEN_AIM')
                if self.check_can_active():
                    super(Dash8007, self).action_btn_down()
                    self.active_self()
                    return True
            return False
        super(Dash8007, self).action_btn_down()
        self.active_self()
        return True

    def action_btn_up(self):
        super(Dash8007, self).action_btn_up()
        if not self.detecting:
            if self.sub_state == self.PRE:
                self.immediately_teleport = True
            return
        if self.sub_state != self.SCAN:
            self.immediately_teleport = True
            return
        self.end_detecting()
        if self.target_pos:
            self.sub_state = self.PREVIEW
        else:
            self.disable_self()

    def action_cancel(self):
        self.detecting = False
        detection_utils.stop_jump_pos_detect(self)
        self.disable_self()
        self.send_event('E_ACTION_UP', self.bind_action_id)

    def end_detecting(self, *args):
        self.send_event('E_SHOW_TELEPORT_FORBID', False)
        detection_utils.clear_tmp_col()
        self.del_detect_sfx()
        self.detecting = False
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        detection_utils.stop_jump_pos_detect(self)

    def detecting_callback(self, valid_pos, *args):
        self.target_pos = None
        if valid_pos and detection_utils.can_teleport(valid_pos, self.ev_g_position()):
            self.target_pos = valid_pos + math3d.vector(0, 5, 0)
        self.send_event('E_SHOW_TELEPORT_FORBID', self.target_pos is None)
        self.update_sfx_visible()
        return

    def update_sfx_visible(self):
        if not self.target_sfx:
            return
        if self.target_pos and not self.target_sfx.visible:
            self.target_sfx.visible = True
        elif not self.target_pos and self.target_sfx.visible:
            self.target_sfx.visible = False
        if self.target_pos:
            self.target_sfx.world_position = self.target_pos

    def create_detect_sfx(self):
        if self.target_sfx:
            return

        def create_cb(sfx):
            sfx.loop = True
            self.target_sfx = sfx
            self.update_sfx_visible()

        self.target_sfx_id = self.ev_g_show_teleport_position_effect(create_cb)[0]

    def del_detect_sfx(self):
        global_data.sfx_mgr.remove_sfx_by_id(self.target_sfx_id)
        self.target_sfx = None
        return