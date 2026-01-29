# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8001.py
from __future__ import absolute_import
from .JumpLogic import JumpUpPure
from .BoostLogic import Dash
from .ShootLogic import WeaponFire
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata import jump_physic_config
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon import editor
import math

class JumpUp8001(JumpUpPure):

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(JumpUp8001, self).init_from_dict(unit_obj, bdict, sid, info)
        self.jump_height_add_scale = 0
        self.cur_jump_speed = self.jump_speed
        self.punishment_height_rate = 0.5
        self.punishment_dec_speed = 0
        self.enable_param_changed_by_buff()
        self.btn_down = False

    def get_jump_speed(self):
        return self.cur_jump_speed * self.extra_jump_speed_scale

    def refresh_param_changed(self):
        if self.jump_height_add_scale > 0:
            scale = 1.0 + self.jump_height_add_scale
            self.cur_jump_speed = math.sqrt(scale) * self.jump_speed
            sqr_jump_speed = self.cur_jump_speed * self.cur_jump_speed
            cur_jump_height = sqr_jump_speed / (2 * self.jump_gravity)
            punishment_height = cur_jump_height / (1 + self.jump_height_add_scale) * self.jump_height_add_scale * self.punishment_height_rate
            jump_height_with_punishment = cur_jump_height - punishment_height * (1 + self.jump_height_add_scale)
            self.punishment_dec_speed = sqr_jump_speed / jump_height_with_punishment / 2 - self.jump_gravity
        else:
            self.cur_jump_speed = self.jump_speed
            self.punishment_dec_speed = 0

    def action_btn_down(self):
        self.btn_down = True
        super(JumpUp8001, self).action_btn_down()

    def action_btn_up(self):
        self.btn_down = False
        if self.is_active and self.punishment_dec_speed > 0:
            self.send_event('E_GRAVITY', self.jump_gravity + self.punishment_dec_speed)

    def _do_jump(self):
        if global_data.game_time - self.last_jump_time < self.min_continual_jump_interval:
            return
        self.last_jump_time = global_data.game_time
        jump_speed = self.get_jump_speed()
        self.air_horizontal_offset_speed_setter.reset()
        if self.punishment_dec_speed > 0:
            if self.btn_down:
                self.send_event('E_GRAVITY', self.jump_gravity)
            else:
                self.send_event('E_GRAVITY', self.jump_gravity + self.punishment_dec_speed)
        else:
            self.send_event('E_GRAVITY', self.jump_gravity)
        self.send_event('E_JUMP', jump_speed)
        self.end_custom_sound('jump')
        self.start_custom_sound('jump')
        jump_up_duration = (jump_speed - jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE) / self.jump_gravity
        anim_rate = self.anim_duration / jump_up_duration
        self.send_event('E_ANIM_RATE', LOW_BODY, anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, self.anim_dir, force_trigger_effect=True)
        if self.sd.ref_cur_jump_count == 0:
            self.send_event('E_PLAY_CAMERA_STATE_TRK', self.jump_camera_trk_name)
        else:
            self.send_event('E_PLAY_CAMERA_STATE_TRK', self.air_jump_camera_trk_name)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sd.ref_cur_jump_count += 1


class Dash8001(Dash):
    BIND_EVENT = Dash.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_BREAKTHROUGH_8001_3': 'on_enable_breakthrough_8001_3'})

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Dash8001, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.breakthrough_8001_3 = False

    def on_enable_breakthrough_8001_3(self, enable):
        self.breakthrough_8001_3 = enable

    def enter(self, leave_states):
        super(Dash8001, self).enter(leave_states)
        if self.breakthrough_8001_3:
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, 3)
            self.ev_g_try_weapon_attack_begin(3)
            self.ev_g_try_weapon_attack_end(3)
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, 3)


class WeaponFire8001(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_BREAKTHROUGH_8001_4': 'on_enable_breakthrough_8001_4'})

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8001, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.breakthrough_8001_4 = False
        self.delta_time_bk_8001_4 = 0.5
        self.trigger_acc_time_bk_8001_4 = 0

    def on_enable_breakthrough_8001_4(self, enable, delta_time):
        self.breakthrough_8001_4 = enable
        self.delta_time_bk_8001_4 = delta_time
        self.trigger_acc_time_bk_8001_4 = 0

    def update(self, dt):
        super(WeaponFire8001, self).update(dt)
        if self.breakthrough_8001_4:
            self.trigger_acc_time_bk_8001_4 += dt
            if self.trigger_acc_time_bk_8001_4 >= self.delta_time_bk_8001_4:
                self.trigger_acc_time_bk_8001_4 = 0
                self.trigger_breakthrough_8001_4_grenade()

    def exit(self, enter_states):
        super(WeaponFire8001, self).exit(enter_states)
        if self.breakthrough_8001_4:
            self.trigger_acc_time_bk_8001_4 = 0

    def trigger_breakthrough_8001_4_grenade(self):
        self.ev_g_try_weapon_attack_begin(4)
        self.ev_g_try_weapon_attack_end(4)