# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8022.py
from __future__ import absolute_import
from .StateBase import StateBase
from .ShootLogic import WeaponFire, Reload, AccumulateShootPure
from .JumpLogic import JetJump, Fall
from .MoveLogic import Walk, Run
from .MountLogic import UnMount
from .StateLogic import Die
from .Logic8020 import check_space_enough_for_trans_to_human
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gutils.character_ctrl_utils import apply_horizon_offset_speed_with_dec
from logic.gcommon.common_const.mecha_const import MECHA_8022_FORM_NORMAL, MECHA_8022_FORM_VEHICLE
from logic.gcommon.common_const.ui_operation_const import JUMP_TRIGGER_PRESS_8022, MAIN_FIRE_ON_RELEASE_8022
from logic.gcommon.component.client.com_mecha_effect.ComMechaEffect8022 import TRANSFORM_WEAPON_SHUTDOWN, TRANSFORM_WEAPON_RELOADING, TRANSFORM_WEAPON_READY
from data.camera_state_const import MECHA_8022_DEFAULT_CAM_MODE, MECHA_8022_DASH_CAM_MODE, MECHA_8022_CANNON_CAM_MODE
from common.utils.timer import CLOCK
from logic.gcommon import editor
from math import pi, radians
import math3d
import world
MOVE_SOUND_RTPC_VALUE_UPDATE_SPEED = 100 / 2.0
cur_move_sound_rtpc_value = -1
target_move_sound_rtpc_value = -1

def update_move_sound_rtpc_value(self, dt):
    global target_move_sound_rtpc_value
    global cur_move_sound_rtpc_value
    if not self.sd.ref_rocker_dir:
        new_target_rtpc_value = 50
    else:
        x = self.sd.ref_rocker_dir.x
        if x == 0.0:
            new_target_rtpc_value = 50
        else:
            new_target_rtpc_value = 50 + 50 * x * self.sd.ref_rocker_move_percent
    if new_target_rtpc_value != target_move_sound_rtpc_value:
        target_move_sound_rtpc_value = new_target_rtpc_value
    if cur_move_sound_rtpc_value != target_move_sound_rtpc_value:
        if target_move_sound_rtpc_value > cur_move_sound_rtpc_value:
            cur_move_sound_rtpc_value += MOVE_SOUND_RTPC_VALUE_UPDATE_SPEED * dt
            if cur_move_sound_rtpc_value > target_move_sound_rtpc_value:
                cur_move_sound_rtpc_value = target_move_sound_rtpc_value
        else:
            cur_move_sound_rtpc_value -= MOVE_SOUND_RTPC_VALUE_UPDATE_SPEED * dt
            if cur_move_sound_rtpc_value < target_move_sound_rtpc_value:
                cur_move_sound_rtpc_value = target_move_sound_rtpc_value
        global_data.sound_mgr.set_rtpc_ex('air_injection', cur_move_sound_rtpc_value)


@editor.state_exporter({('blend_time', 'param'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x86\x85\xe9\x83\xa8\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'}})
class Walk8022(Walk):
    BIND_EVENT = Walk.BIND_EVENT.copy()
    BIND_EVENT.update({'E_NOTIFY_TURN_MOVE_PARAM': 'on_notify_turn_move_param',
       'E_FORBID_MOVE_APPEARANCE': 'on_forbid_move_appearance'
       })
    LEFT_DIR = 'l'
    RIGHT_DIR = 'r'

    def read_data_from_custom_param(self):
        super(Walk8022, self).read_data_from_custom_param()
        self.tick_interval = 0.03
        self.blend_time = self.custom_param.get('blend_time', 0.2)
        self.blend_dir = self.custom_param.get('blend_dir', None)
        self.need_move_turn = self.custom_param.get('need_move_turn', False)
        self.need_move_dust_tail = self.custom_param.get('need_move_dust_tail', False)
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Walk8022, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.last_trigger_turn_move_time = 0
        self.last_rocker_dir_time = {self.LEFT_DIR: 0,self.RIGHT_DIR: 0}
        self.opposite_dir = {self.LEFT_DIR: self.RIGHT_DIR,self.RIGHT_DIR: self.LEFT_DIR}
        self.temporarily_forbid_change_move_dust_tail_sfx = False
        self.sound_rtpc_value = -1
        self.move_appearance_forbiden = False

    def enter(self, leave_states):
        self.blend_dir and self.send_event('E_SET_BLEND_NODE_SMOOTH_DURATION', LOW_BODY, self.blend_dir, self.blend_time)
        super(Walk8022, self).enter(leave_states)
        self.temporarily_forbid_change_move_dust_tail_sfx = False
        not self.move_appearance_forbiden and self.start_custom_sound('loop')
        if MC_RUN in leave_states:
            self.temporarily_forbid_change_move_dust_tail_sfx = True
            if not self.need_move_dust_tail:
                self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', False)
        else:
            not self.move_appearance_forbiden and self.start_custom_sound('start')

    def _get_cur_direction(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            yaw = rocker_dir.yaw
            if self.left_min_angle <= yaw <= self.left_max_angle:
                return self.LEFT_DIR
            if self.right_min_angle <= yaw <= self.right_max_angle:
                return self.RIGHT_DIR
        return None

    def update(self, dt):
        super(Walk8022, self).update(dt)
        if self.need_move_turn and self.elapsed_time >= self.begin_trigger_time:
            if global_data.game_time - self.last_trigger_turn_move_time >= self.trigger_cd:
                cur_dir = self._get_cur_direction()
                if cur_dir is not None and global_data.game_time - self.last_rocker_dir_time[self.opposite_dir[cur_dir]] <= self.effective_trigger_interval:
                    self.send_event('E_TRIGGER_MOVE_TURN', cur_dir)
                    self.last_trigger_turn_move_time = global_data.game_time
                self.last_rocker_dir_time[cur_dir] = global_data.game_time
        if self.need_move_dust_tail and not self.move_appearance_forbiden:
            flag = self.sd.ref_cur_speed == self.walk_speed * self.ev_g_get_speed_scale()
            if self.temporarily_forbid_change_move_dust_tail_sfx:
                if flag:
                    self.temporarily_forbid_change_move_dust_tail_sfx = False
                else:
                    return
            self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', flag, self.blend_time)
        if not self.sd.ref_is_cannon_shape:
            update_move_sound_rtpc_value(self, dt)
        return

    def exit(self, enter_states):
        self.blend_dir and self.send_event('E_SET_BLEND_NODE_SMOOTH_DURATION', LOW_BODY, self.blend_dir, 0.2)
        super(Walk8022, self).exit(enter_states)
        self.end_custom_sound('start')
        self.end_custom_sound('loop')
        if MC_RUN not in enter_states:
            self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', False)
            self.end_custom_sound('end')
            self.start_custom_sound('end')

    def on_notify_turn_move_param(self, begin_trigger_time, effective_trigger_interval, trigger_cd, left_min_angle, left_max_angle, right_min_angle, right_max_angle):
        self.begin_trigger_time = begin_trigger_time
        self.effective_trigger_interval = effective_trigger_interval
        self.trigger_cd = trigger_cd
        self.left_min_angle = left_min_angle
        self.left_max_angle = left_max_angle
        self.right_min_angle = right_min_angle
        self.right_max_angle = right_max_angle

    def on_forbid_move_appearance(self, flag):
        self.move_appearance_forbiden = flag
        if self.is_active:
            if flag:
                self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', False)
                self.end_custom_sound('start')
                self.end_custom_sound('loop')
            else:
                self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', True)
                self.start_custom_sound('loop')

    def refresh_action_param(self, action_param, custom_param):
        if self.is_active:
            self.blend_dir and self.send_event('E_SET_BLEND_NODE_SMOOTH_DURATION', LOW_BODY, self.blend_dir, 0.2)
        cur_need_move_dust_tail = self.need_move_dust_tail
        super(Walk8022, self).refresh_action_param(action_param, custom_param)
        if self.is_active:
            self.blend_dir and self.send_event('E_SET_BLEND_NODE_SMOOTH_DURATION', LOW_BODY, self.blend_dir, self.blend_time)
            if not self.need_move_dust_tail and cur_need_move_dust_tail:
                self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', False)


@editor.state_exporter({('l2r_anim_duration', 'param'): {'zh_name': '\xe5\xb7\xa6\xe8\xbd\xac\xe5\x8f\xb3\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.update_anim_parameters()
                                    },
   ('l2r_anim_rate', 'param'): {'zh_name': '\xe5\xb7\xa6\xe8\xbd\xac\xe5\x8f\xb3\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self.update_anim_parameters()
                                },
   ('r2l_anim_duration', 'param'): {'zh_name': '\xe5\x8f\xb3\xe8\xbd\xac\xe5\xb7\xa6\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.update_anim_parameters()
                                    },
   ('r2l_anim_rate', 'param'): {'zh_name': '\xe5\x8f\xb3\xe8\xbd\xac\xe5\xb7\xa6\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self.update_anim_parameters()
                                },
   ('begin_trigger_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x90\x8e\xe5\xa4\x9a\xe4\xb9\x85\xe5\x8f\xaf\xe4\xbb\xa5\xe6\x92\xad\xe6\x94\xbe\xe8\xbd\xac\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c','post_setter': lambda self: self.notify_outer_parameters()
                                     },
   ('effective_trigger_interval', 'param'): {'zh_name': '\xe6\x9c\x89\xe6\x95\x88\xe6\x91\x87\xe6\x9d\x86\xe6\x96\xb9\xe5\x90\x91\xe5\x88\x87\xe6\x8d\xa2\xe9\x97\xb4\xe9\x9a\x94','post_setter': lambda self: self.notify_outer_parameters()
                                             },
   ('trigger_cd', 'param'): {'zh_name': '\xe8\xbd\xac\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe8\xa7\xa6\xe5\x8f\x91cd','post_setter': lambda self: self.notify_outer_parameters()
                             },
   ('trigger_angle', 'angle'): {'zh_name': '\xe6\x91\x87\xe6\x9d\x86\xe5\xb7\xa6\xe5\x8f\xb3\xe5\x8c\xba\xe5\x9f\x9f\xe5\x88\x92\xe5\x88\x86\xe8\xa7\x92\xe5\xba\xa6','post_setter': lambda self: self.notify_outer_parameters()
                                }
   })
class MoveTurn(StateBase):
    BIND_EVENT = {'E_TRIGGER_MOVE_TURN': 'on_trigger_move_turn'
       }
    ANIM_DIR = ('l2r', 'r2l')
    FINAL_DIR_MAP = {'l': 'r2l','r': 'l2r'}
    ANIM_PARAM_NAME = ('anim_name', 'anim_duration', 'anim_rate')

    def read_data_from_custom_param(self):
        self.l2r_anim_name = self.custom_param.get('l2r_anim_name', None)
        self.l2r_anim_duration = self.custom_param.get('l2r_anim_duration', 0.9)
        self.l2r_anim_rate = self.custom_param.get('l2r_anim_rate', 1.0)
        self.r2l_anim_name = self.custom_param.get('r2l_anim_name', None)
        self.r2l_anim_duration = self.custom_param.get('r2l_anim_duration', 0.9)
        self.r2l_anim_rate = self.custom_param.get('r2l_anim_rate', 1.0)
        self.begin_trigger_time = self.custom_param.get('begin_trigger_time', 2.0)
        self.effective_trigger_interval = self.custom_param.get('effective_trigger_interval', 0.3)
        self.trigger_cd = self.custom_param.get('trigger_cd', 2.0)
        self.trigger_angle = radians(self.custom_param.get('trigger_angle', 60.0))
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MoveTurn, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.cur_anim_name, self.cur_anim_duration, self.cur_anim_rate = (None, 0.9,
                                                                          1.0)
        self.sd.ref_move_turning = False
        return None

    def update_anim_parameters(self):
        self.anim_params = dict()
        for anim_dir in self.ANIM_DIR:
            self.anim_params[anim_dir] = [ getattr(self, anim_dir + '_' + param_name) for param_name in self.ANIM_PARAM_NAME ]

    def notify_outer_parameters(self):
        right_min_angle = (pi - self.trigger_angle) / 2
        right_max_angle = right_min_angle + self.trigger_angle
        left_max_angle = -right_min_angle
        left_min_angle = -right_max_angle
        self.send_event('E_NOTIFY_TURN_MOVE_PARAM', self.begin_trigger_time, self.effective_trigger_interval, self.trigger_cd, left_min_angle, left_max_angle, right_min_angle, right_max_angle)

    def on_init_complete(self):
        super(MoveTurn, self).on_init_complete()
        self.update_anim_parameters()
        self.notify_outer_parameters()

    def enter(self, leave_states):
        super(MoveTurn, self).enter(leave_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.cur_anim_name, blend_dir=1, loop=False)
        self.sd.ref_move_turning = True

    def update(self, dt):
        super(MoveTurn, self).update(dt)
        if self.elapsed_time > self.cur_anim_duration:
            self.disable_self()

    def exit(self, enter_states):
        super(MoveTurn, self).exit(enter_states)
        if MC_SECOND_WEAPON_ATTACK not in enter_states:
            self.send_event('E_REFRESH_CUR_STATE_ANIM')
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, None)
        self.sd.ref_move_turning = False
        return

    def on_trigger_move_turn(self, final_dir):
        if self.check_can_active():
            self.cur_anim_name, self.cur_anim_duration, self.cur_anim_rate = self.anim_params[self.FINAL_DIR_MAP[final_dir]]
            self.active_self()


class Run8022(Run):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Run8022, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.tick_interval = 0.03

    def enter(self, leave_states):
        super(Run8022, self).enter(leave_states)
        self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', True)

    def update(self, dt):
        super(Run8022, self).update(dt)
        update_move_sound_rtpc_value(self, dt)

    def exit(self, enter_states):
        super(Run8022, self).exit(enter_states)
        if MC_MOVE not in enter_states:
            self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', False)


@editor.state_exporter({('jump_speed', 'meter'): {'zh_name': '\xe6\x94\x80\xe5\x8d\x87\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_speed', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe6\x9c\x80\xe5\xa4\xa7\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_acc', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_dec_duration', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x95\xbf'},('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('post_anim_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                     },
   ('post_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'}})
class JetJump8022(JetJump):
    BIND_EVENT = JetJump.BIND_EVENT.copy()
    BIND_EVENT.update({'E_FORCE_REPLACE_JUMP_UP_ANIM': 'on_force_replace_anim'
       })

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(JetJump8022, self).init_from_dict(unit_obj, bdict, sid, info)
        self.force_anim = None
        return

    def enter(self, leave_states):
        super(JetJump8022, self).enter(leave_states)
        if self.sd.ref_is_cannon_shape:
            self.ev_g_on_ground() and self.send_event('E_PLAY_TRANSFORM_JUMP_DUST_SFX')
        else:
            self.send_event('E_PLAY_JUMP_BURST_SFX', True)

    def _play_sub_state_anim(self):
        if self.force_anim:
            anim_name, anim_rate = self.force_anim, 1.0
        else:
            anim_name, anim_rate = self.sub_state_anim_param[self.sub_state]
        if self.sd.ref_low_body_anim == anim_name:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, anim_rate)
        loop = self.sub_state == self.STATE_LOOP
        self.send_event('E_POST_ACTION', anim_name, LOW_BODY, 1, loop=loop)

    def exit(self, enter_states):
        super(JetJump8022, self).exit(enter_states)
        self.send_event('E_PLAY_JUMP_BURST_SFX', False)

    def on_force_replace_anim(self, anim):
        self.force_anim = anim
        if self.is_active:
            self._play_sub_state_anim()


@editor.state_exporter({('h_offset_dec', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'}})
class Fall8022(Fall):

    def read_data_from_custom_param(self):
        super(Fall8022, self).read_data_from_custom_param()
        self.h_offset_dec = self.custom_param.get('h_offset_dec', 100) * NEOX_UNIT_SCALE

    def refresh_action_param(self, action_param, custom_param):
        super(Fall8022, self).refresh_action_param(action_param, custom_param)
        self.custom_param = custom_param
        self.read_data_from_custom_param()

    def update(self, dt):
        super(Fall, self).update(dt)
        self.air_move_enabled and apply_horizon_offset_speed_with_dec(self, dt, self.get_max_h_offset_speed(), self.get_h_offset_acc() * self.h_offset_acc_percent, self.h_offset_dec)
        self.check_logic_on_ground(dt)


class DashFall8022(Fall8022):
    BIND_EVENT = {}


class WeaponFire8022(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REFRESH_CUR_STATE_ANIM': 'on_refresh_cur_state_anim'
       })

    def read_data_from_custom_param(self):
        super(WeaponFire8022, self).read_data_from_custom_param()
        self.fire_on_release = self.fire_on_release and global_data.player.get_setting_2(MAIN_FIRE_ON_RELEASE_8022)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8022, self).init_from_dict(unit_obj, bdict, sid, state_info)
        global_data.emgr.update_main_fire_on_release_8022 += self.on_update_fire_on_release

    def destroy(self):
        global_data.emgr.update_main_fire_on_release_8022 -= self.on_update_fire_on_release
        super(WeaponFire8022, self).destroy()

    def action_btn_down(self, ignore_reload=False):
        from logic.comsys.battle.BattleUtils import can_fire
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
        if not self.fire_on_release:
            if not self.try_weapon_attack_begin():
                self.is_continue_fire = False
                return False
            if self.is_active:
                self.re_enter()
            self.can_fire_attack()
            self.active_self()
        super(WeaponFire, self).action_btn_down()
        return True

    def action_btn_up(self):
        self.is_continue_fire = False
        self.want_to_fire = False
        if self.fire_on_release:
            if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
                return False
            self.active_self()
            self.try_weapon_attack_begin()
        if not self.try_weapon_attack_end():
            return False
        super(WeaponFire, self).action_btn_up()
        return True

    def enter(self, leave_states):
        super(WeaponFire8022, self).enter(leave_states)
        if not self.sd.ref_move_turning and self.aim_anim:
            self.send_event('E_POST_ACTION', self.aim_anim, UP_BODY, self.aim_anim_blend_type)
        if self.weapon_pos == PART_WEAPON_POS_MAIN3:
            self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_SHUTDOWN)

    def update(self, dt):
        super(WeaponFire8022, self).update(dt)
        if self.sd.ref_is_cannon_shape:
            return None
        else:
            if self.ev_g_on_ground():
                if self.anim_blend_type == 1:
                    self.anim_blend_type = self.custom_param.get('shoot_anim', (None,
                                                                                'upper',
                                                                                1))[2]
                    self.aim_anim_blend_type = self.custom_param.get('aim_anim', (None,
                                                                                  'upper',
                                                                                  1))[2]
                    self.on_refresh_cur_state_anim()
            elif self.anim_blend_type != 1:
                self.anim_blend_type = 1
                self.aim_anim_blend_type = 1
                self.on_refresh_cur_state_anim()
            return None

    def on_update_fire_on_release(self, flag):
        self.fire_on_release = self.custom_param.get('fire_on_release', False) and flag

    def check_transitions(self):
        if self.fired_time > self.fire_anim_time:
            self.disable_self()
        elif self.aim_anim and self.play_aim_anim_time <= self.fired_time and not self.aim_anim_played and not self.sd.ref_move_turning:
            self.send_event('E_POST_ACTION', self.aim_anim, UP_BODY, self.aim_anim_blend_type)
            self.aim_anim_played = True

    def refresh_action_param(self, action_param, custom_param):
        super(WeaponFire8022, self).refresh_action_param(action_param, custom_param)
        self.fire_on_release = self.fire_on_release and global_data.player.get_setting_2(MAIN_FIRE_ON_RELEASE_8022)

    def try_play_fire_anim(self, fired_socket_index):
        if self.sd.ref_move_turning:
            self.send_event('E_PLAY_MAIN_WEAPON_FIRE_SFX', fired_socket_index)
            return
        self.play_fire_anim(fired_socket_index)

    def on_refresh_cur_state_anim(self):
        if self.is_active:
            self.send_event('E_POST_ACTION', self.aim_anim, UP_BODY, self.aim_anim_blend_type)
            self.aim_anim_played = True


class Reload8022(Reload):
    BIND_EVENT = Reload.BIND_EVENT.copy()
    BIND_EVENT.update({'E_DO_RELOAD_SFX_AND_VOICE_APPEARANCE': 'do_reload_sfx_and_voice_appearance'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8022, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.last_on_ground = True
        self.tick_interval = 0.03

    def enter(self, leave_states):
        super(Reload8022, self).enter(leave_states)
        self.last_on_ground = True
        if self.weapon_pos == PART_WEAPON_POS_MAIN3:
            self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_RELOADING)

    def update(self, dt):
        super(Reload8022, self).update(dt)
        if self.last_on_ground != self.ev_g_on_ground() and not self.sd.ref_is_cannon_shape:
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
        super(Reload8022, self).exit(enter_states)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
        if self.weapon_pos == PART_WEAPON_POS_MAIN3:
            self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_READY)

    def on_reloading_bullet(self, time, times, weapon_pos):
        if self.weapon_pos != weapon_pos:
            return
        self.reload_time = time
        if self.weapon_pos == PART_WEAPON_POS_MAIN1:
            self.do_reload_sfx_and_voice_appearance(True)
        if not self.ignore_anim:
            self.active_self()

    def do_reload_sfx_and_voice_appearance(self, flag):
        self.send_event('E_PLAY_RELOAD_SFX', flag)
        self.end_custom_sound('reload')
        if flag:
            self.start_custom_sound('reload')


class AccumulateShoot8022(AccumulateShootPure):
    BIND_EVENT = AccumulateShootPure.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HOVER_STATE_CHANGED': 'on_hover_state_changed'
       })
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD, MC_MOVE, MC_JUMP_1, MC_JUMP_2, MC_JUMP_3, MC_SUPER_JUMP, MC_TRANSFORM}

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateShoot8022, self).init_from_dict(unit_obj, bdict, sid, info)
        self.tick_interval = 0.03
        self.hovering = False

    def activate_hover(self, flag):
        if self.hovering == flag:
            return
        if flag:
            self.send_event('E_ACTIVE_STATE', MC_HOVER)

    def enter(self, leave_states):
        super(AccumulateShoot8022, self).enter(leave_states)
        self.send_event('E_FORBID_MOVE_APPEARANCE', True)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', {MC_MOVE, MC_RUN}, self.loop_anim_name, blend_dir=1)
        self.hovering = False
        if self.ev_g_on_ground():
            self.send_event('E_GRAVITY', 0.1)
        else:
            self.activate_hover(True)

    def on_begin_post(self):
        super(AccumulateShoot8022, self).on_begin_post()
        self.send_event('E_ACTIVE_STATE', MC_FALL_BACK)

    def update(self, dt):
        super(AccumulateShoot8022, self).update(dt)
        if self.sub_state != self.STATE_POST:
            self.activate_hover(not self.ev_g_on_ground())

    def exit(self, enter_states):
        super(AccumulateShootPure, self).exit(enter_states)
        self.send_event('E_FORBID_MOVE_APPEARANCE', False)
        if not self.acc_skill_ended:
            self.send_event('E_ACC_SKILL_END', self.weapon_pos)
            self.acc_skill_ended = True
        if self.PART == UP_BODY and self.sd.ref_up_body_anim in self.all_anim_name_set:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM', blend_time=0.1)
            if self.use_up_body_bone:
                global_data.game_mgr.register_logic_timer(lambda : self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', {MC_MOVE, MC_RUN}, None)
        if self.hovering:
            self.send_event('E_END_HOVER')
        else:
            self.send_event('E_RESET_GRAVITY')
        self.end_custom_sound('pre')
        self.end_custom_sound('hold')
        self.end_custom_sound('post')
        return

    def on_hover_state_changed(self, flag):
        self.hovering = flag


@editor.state_exporter({('hover_acc_speed', 'meter'): {'zh_name': '\xe6\x82\xac\xe6\xb5\xae\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('hover_speed', 'meter'): {'zh_name': '\xe6\x82\xac\xe6\xb5\xae\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('hover_dec_speed', 'meter'): {'zh_name': '\xe6\x82\xac\xe6\xb5\xae\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'}})
class Hover8022(StateBase):
    BIND_EVENT = {'E_FUEL_EXHAUSTED': 'on_fuel_exhausted',
       'E_END_HOVER': 'on_fuel_exhausted'
       }
    GROUND_STATES = {
     MC_STAND, MC_MOVE, MC_RUN, MC_JUMP_3}

    def read_data_from_custom_param(self):
        self.hover_skill_id = self.custom_param.get('hover_skill_id', None)
        self.hover_acc_speed = self.custom_param.get('hover_acc_speed', 30) * NEOX_UNIT_SCALE
        self.hover_speed = self.custom_param.get('hover_speed', 10) * NEOX_UNIT_SCALE
        self.hover_dec_speed = self.custom_param.get('hover_dec_speed', 30) * NEOX_UNIT_SCALE
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Hover8022, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.tick_interval = 0.03
        self.hovering = False
        self.need_leave_hover = False

    def enter(self, leave_states):
        super(Hover8022, self).enter(leave_states)
        if MC_SECOND_WEAPON_ATTACK not in self.ev_g_cur_state() or not self.ev_g_can_cast_skill(self.hover_skill_id):
            self.need_leave_hover = True
            return
        self.need_leave_hover = False
        self.hovering = True
        self.send_event('E_HOVER_STATE_CHANGED', True)
        self.send_event('E_DO_SKILL', self.hover_skill_id)
        self.send_event('E_GRAVITY', 0)
        if not self.GROUND_STATES & leave_states:
            self.send_event('E_VERTICAL_SPEED', 0)

    def update(self, dt):
        super(Hover8022, self).update(dt)
        cur_speed = self.sd.ref_cur_speed
        if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
            rotation = self.ev_g_rotation()
            if rotation:
                cur_speed += self.hover_acc_speed * dt
                if cur_speed > self.hover_speed:
                    cur_speed = self.hover_speed
                self.sd.ref_cur_speed = cur_speed
                walk_direction = rotation.rotate_vector(self.sd.ref_rocker_dir)
                self.send_event('E_SET_WALK_DIRECTION', walk_direction * cur_speed)
        else:
            cur_speed -= self.hover_dec_speed * dt
            if cur_speed < 0:
                cur_speed = 0
            self.sd.ref_cur_speed = cur_speed
            walk_direction = self.ev_g_get_walk_direction()
            if not walk_direction.is_zero:
                walk_direction.normalize()
            self.send_event('E_SET_WALK_DIRECTION', walk_direction * cur_speed)

    def check_transitions(self):
        on_ground = self.ev_g_on_ground()
        if self.need_leave_hover or on_ground:
            if on_ground:
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(Hover8022, self).exit(enter_states)
        if self.hovering:
            self.send_event('E_HOVER_STATE_CHANGED', False)
            self.send_event('E_END_SKILL', self.hover_skill_id)
            if self.ev_g_on_ground():
                self.send_event('E_GRAVITY', 0.1)
            else:
                self.send_event('E_RESET_GRAVITY')

    def on_fuel_exhausted(self, *args):
        self.need_leave_hover = True


@editor.state_exporter({('back_off_speed', 'meter'): {'zh_name': '\xe5\x90\x8e\xe9\x80\x80\xe9\x80\x9f\xe5\xba\xa6'},('back_off_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe9\x80\x80\xe6\x97\xb6\xe9\x97\xb4'}})
class FallBack(StateBase):

    def read_data_from_custom_param(self):
        self.back_off_speed = self.custom_param.get('back_off_speed', 6) * NEOX_UNIT_SCALE
        self.back_off_duration = self.custom_param.get('back_off_duration', 0.6)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(FallBack, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.tick_interval = 0.03
        self.back_off_direction = math3d.vector(0, 0, 1)
        self.back_off_walk_direction = self.back_off_direction
        self.finished = False

    def enter(self, leave_states):
        super(FallBack, self).enter(leave_states)
        self.back_off_direction = -world.get_active_scene().active_camera.rotation_matrix.forward
        self.back_off_walk_direction = self.back_off_direction * self.back_off_speed
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        self.finished = False

    def update(self, dt):
        super(FallBack, self).update(dt)
        ratio = 1.0 - self.elapsed_time / self.back_off_duration
        if ratio < 0.0:
            ratio = 0.0
        cur_walk_direction = self.back_off_walk_direction * ratio
        self.send_event('E_VERTICAL_SPEED', cur_walk_direction.y)
        cur_walk_direction.y = 0
        self.sd.ref_cur_speed = cur_walk_direction.length
        self.send_event('E_SET_WALK_DIRECTION', cur_walk_direction)

    def check_transitions(self):
        if self.elapsed_time >= self.back_off_duration:
            self.finished = True
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(FallBack, self).exit(enter_states)
        self.sd.ref_logic_trans.yaw_target = world.get_active_scene().active_camera.rotation_matrix.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        if not self.finished:
            self.send_event('E_RESET_GRAVITY')
            self.send_event('E_CLEAR_SPEED')
            self.send_event('E_VERTICAL_SPEED', 0)


@editor.state_exporter({('switch_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('switch_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'},('switch_back_time', 'param'): {'zh_name': '\xe8\xbf\x9e\xe7\xbb\xad\xe5\x8f\x98\xe5\xbd\xa2\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'},('break_time', 'param'): {'zh_name': '\xe5\x8f\x98\xe5\xbd\xa2\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'}})
class CannonSwitch(StateBase):
    BIND_EVENT = {'E_FORCE_TELL_SERVER_SWITCH_TO_NORMAL': 'force_switch_to_normal'
       }
    STATE_SWITCH = 0
    BREAK_STATES = {MC_SHOOT, MC_SECOND_WEAPON_ATTACK}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.switch_anim_name = self.custom_param.get('switch_anim_name', None)
        self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 1.0)
        self.switch_anim_rate = self.custom_param.get('switch_anim_rate', 1.0)
        self.switch_back_time = self.custom_param.get('switch_back_time', 0.8)
        self.break_time = self.custom_param.get('break_time', 0.6)
        self.register_callbacks()
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_SWITCH, 0.0, self.on_begin_switch)
        self.register_substate_callback(self.STATE_SWITCH, self.break_time, self.on_enable_break_switch)
        self.register_substate_callback(self.STATE_SWITCH, self.switch_anim_duration, self.on_end_switch)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(CannonSwitch, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.new_custom_param = self.custom_param
        self.sound_param_delay_refresh = True

    def action_btn_down(self):
        super(CannonSwitch, self).action_btn_down()
        if not self.check_can_active():
            return False
        if self.sd.ref_is_cannon_shape and not check_space_enough_for_trans_to_human(self):
            return False
        if not self.check_can_cast_skill():
            return False
        if self.is_active:
            if self.sub_sid_timer < self.switch_back_time:
                return False
            self.check_custom_param_refreshed()
            self.reset_sub_state_timer()
        else:
            self.active_self()
        return True

    def check_custom_param_refreshed(self):
        if self.custom_param is not self.new_custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()
            self._check_sound_param_refresh()

    def enter(self, leave_states):
        super(CannonSwitch, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.sub_state = self.STATE_SWITCH
        self.send_event('E_DO_RELOAD_SFX_AND_VOICE_APPEARANCE', False)

    def on_begin_switch(self):
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_ANIM_RATE', UP_BODY, self.switch_anim_rate)
        self.send_event('E_POST_ACTION', self.switch_anim_name, UP_BODY, 1)
        if self.sd.ref_is_cannon_shape:
            self.send_event('E_DO_SKILL', self.skill_id, MECHA_8022_FORM_NORMAL)
            self.send_event('E_DISABLE_STATE', MC_OTHER_SHAPE)
        else:
            self.send_event('E_DO_SKILL', self.skill_id, MECHA_8022_FORM_VEHICLE)
            self.send_event('E_ACTIVE_STATE', MC_OTHER_SHAPE)

    def on_enable_break_switch(self):
        self.send_event('E_ADD_WHITE_STATE', self.BREAK_STATES, self.sid)

    def on_end_switch(self):
        self.disable_self()

    def update(self, dt):
        super(CannonSwitch, self).update(dt)

    def exit(self, enter_states):
        super(CannonSwitch, self).exit(enter_states)
        if self.sd.ref_is_cannon_shape:
            self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_READY)
        else:
            global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)
        if self.sd.ref_up_body_anim == self.switch_anim_name:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.check_custom_param_refreshed()
        self.send_event('E_IGNORE_RELOAD_ANIM', False)

    def refresh_action_param(self, action_param, custom_param):
        if custom_param:
            self.new_custom_param = custom_param
            if not self.is_active:
                self.check_custom_param_refreshed()

    def force_switch_to_normal(self):
        self.send_event('E_DO_SKILL', self.skill_id, MECHA_8022_FORM_NORMAL)


class CannonShape(StateBase):
    BIND_EVENT = {'E_ENABLE_BEHAVIOR': ('on_enable_behavior', 99)
       }
    MAX_TWIST_ANGLE = 7

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(CannonShape, self).init_from_dict(unit_obj, bdict, sid, info)
        self.sd.ref_is_cannon_shape = bdict.get('shape_form', MECHA_8022_FORM_NORMAL) == MECHA_8022_FORM_VEHICLE
        if self.sd.ref_is_cannon_shape:
            self.sd.ref_forbid_show_action_anim = True

    def on_init_complete(self):
        super(CannonShape, self).on_init_complete()
        self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', self.sd.ref_is_cannon_shape)
        self.send_event('E_ADD_LOCK_AIM_DIR_CAM_MODE_MAP', {MECHA_8022_DEFAULT_CAM_MODE: MECHA_8022_CANNON_CAM_MODE,
           MECHA_8022_DASH_CAM_MODE: MECHA_8022_CANNON_CAM_MODE,
           MECHA_8022_CANNON_CAM_MODE: MECHA_8022_DEFAULT_CAM_MODE
           })

    def enter(self, leave_states):
        self.send_event('E_RECORD_CUR_CAM_AIM_DIR')
        super(CannonShape, self).enter(leave_states)
        if self.sd.ref_is_cannon_shape:
            self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_READY)
        else:
            self.sd.ref_is_cannon_shape = True
            self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', self.sd.ref_is_cannon_shape)
        self.send_event('E_REFRESH_STATE_PARAM', include_camera_param=True)
        self.send_event('E_ENABLE_ALIGN_ON_GROUND', True, self.MAX_TWIST_ANGLE)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', 'transform_idle')
        self.send_event('E_REPLACE_UNMOUNT_ANIM', 'transform_idle', 1)
        self.send_event('E_PLAY_MOVE_DUST_TAIL_SFX', False)
        self.send_event('E_SET_ACTION_VISIBLE', 'action4', False)
        self.send_event('E_SET_ACTION_VISIBLE', 'action6', False)
        self.send_event('E_SET_ACTION_VISIBLE', 'action8', False)
        self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8022_5.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8022_5.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', 'gui/ui_res_2/battle/mech_main/icon_mech8022_5.png', 'show')
        self.send_event('E_ENABLE_MECHA_FOOT_IK', False)

    def exit(self, enter_states):
        self.send_event('E_RECORD_CUR_CAM_AIM_DIR')
        super(CannonShape, self).exit(enter_states)
        self.sd.ref_is_cannon_shape = False
        self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', self.sd.ref_is_cannon_shape)
        self.send_event('E_RESET_STATE_PARAM', include_camera_param=True)
        self.send_event('E_ENABLE_ALIGN_ON_GROUND', False, self.MAX_TWIST_ANGLE)
        self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
        self.send_event('E_REPLACE_UNMOUNT_ANIM', None, 1)
        self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_SHUTDOWN)
        self.send_event('E_SET_ACTION_VISIBLE', 'action4', True)
        self.send_event('E_SET_ACTION_VISIBLE', 'action6', True)
        self.send_event('E_SET_ACTION_VISIBLE', 'action8', True)
        self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8022_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8022_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', 'gui/ui_res_2/battle/mech_main/icon_mech8022_1.png', 'show')
        self.send_event('E_ENABLE_MECHA_FOOT_IK', True)
        return

    def on_enable_behavior(self, *args):
        if self.sd.ref_is_cannon_shape:
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
            self.active_self()
        else:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)


class UnMount8022(UnMount):
    BIND_EVENT = UnMount.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REPLACE_UNMOUNT_ANIM': 'replace_unmount_anim'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(UnMount8022, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.replaced_anim_name = None
        self.replaced_anim_dir = 1
        return

    def enter(self, leave_states):
        super(UnMount, self).enter(leave_states)
        self.send_event('E_STOP_WP_TRACK')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_CLEAR_TWIST_PITCH')
        self.delay_call(self.eject_time, lambda : self.send_event('E_NOTIFY_PASSENGER_LEAVE'))
        if self.action_param:
            if self.eject_anim_time_tag:
                self.send_event('E_ANIM_RATE', LOW_BODY, self.eject_anim_time / self.eject_time)
            trigger_time, anim_info = self.convert_anim_info(self.action_param)
            clip_name, part, blend_dir, kwargs = anim_info
            if self.replaced_anim_name:
                clip_name = self.replaced_anim_name
                blend_dir = self.replaced_anim_dir
            self.send_event('E_POST_ACTION', clip_name, part, blend_dir, **kwargs)
        bat = self.unit_obj.get_battle()
        if bat and bat.is_in_settle_celebrate_stage() and self.unit_obj.get_owner().is_share():
            self.check_show_celebrate()
        if MC_OTHER_SHAPE in leave_states:
            self.send_event('E_FORCE_TELL_SERVER_SWITCH_TO_NORMAL')

    def replace_unmount_anim(self, anim_name, blend_dir):
        self.replaced_anim_name = anim_name
        self.replaced_anim_dir = blend_dir


class Die8022(Die):

    def enter(self, leave_states):
        super(Die8022, self).enter(leave_states)
        if self.ev_g_is_avatar():
            if self.sd.ref_is_cannon_shape:
                self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_SHUTDOWN)
                self.send_event('E_SET_DEFAULT_UP_BODY_ANIM', None)
                self.send_event('E_CLEAR_UP_BODY_ANIM')
        else:
            self.send_event('E_PLAY_TRANSFORM_WEAPON_STATE_SFX', TRANSFORM_WEAPON_SHUTDOWN)
        return


class Dash8022(StateBase):
    BIND_EVENT = {'E_FUEL_EXHAUSTED': 'on_fuel_exhausted',
       'E_ON_TOUCH_GROUND': 'on_touch_ground',
       'E_LOGIC_ON_GROUND': 'on_touch_ground',
       'E_AIR_BURST_DURATION': 'set_air_burst_duration'
       }
    STATE_NONE = 0
    STATE_AIR_BURST = 1
    STATE_SPEED_UP = 2

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.speed_up_skill_id = self.custom_param.get('speed_up_skill_id', None)
        return

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_AIR_BURST, 0.0, self.on_begin_burst)
        self.register_substate_callback(self.STATE_AIR_BURST, self.burst_duration, self.on_end_burst)
        self.register_substate_callback(self.STATE_SPEED_UP, 0.0, self.on_begin_speed_up)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8022, self).init_from_dict(unit_obj, bdict, sid, info)
        self.costing_fuel = False
        self.can_air_burst = True
        self.last_on_ground = True
        self.read_data_from_custom_param()

    def action_btn_down(self):
        super(Dash8022, self).action_btn_down()
        if self.is_active:
            if self.sub_state == self.STATE_AIR_BURST:
                self.send_event('E_CLEAR_SPEED')
            self.sub_state = self.STATE_NONE
            self.disable_self()
            return True
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if self.can_air_burst and not self.ev_g_on_ground():
            if self.ev_g_check_can_air_dash():
                self.sub_state = self.STATE_AIR_BURST
            else:
                return False
        else:
            self.sub_state = self.STATE_SPEED_UP
        self.active_self()
        return True

    def enter(self, leave_states):
        super(Dash8022, self).enter(leave_states)
        self.start_custom_sound('start')
        self.sd.ref_forbid_zero_anim_dir = False
        self.send_event('E_FORCE_REPLACE_JUMP_UP_ANIM', 'dash_lod_idle')
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.send_event('E_PLAY_DASH_BURST_SFX', True)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.last_on_ground = False

    def on_begin_burst(self):
        self.send_event('E_ACTIVATE_AIR_DASH')
        self.can_air_burst = False

    def on_end_burst(self):
        self.send_event('E_END_AIR_DASH')
        self.sub_state = self.STATE_SPEED_UP

    def on_begin_speed_up(self):
        if not self.ev_g_can_cast_skill(self.speed_up_skill_id):
            self.disable_self()
            return
        if MC_RUN in self.ev_g_cur_state():
            if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_ACTIVE_STATE', MC_MOVE)
            else:
                self.send_event('E_ACTIVE_STATE', MC_STAND)
        self.costing_fuel = True
        self.send_event('E_DO_SKILL', self.speed_up_skill_id)
        self.send_event('E_REPLACE_STATE_PARAM', MC_STAND, MC_OTHER_STAND)
        self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, MC_OTHER_MOVE, include_camera_param=True)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_OTHER_JUMP_2)

    def update(self, dt):
        super(Dash8022, self).update(dt)
        if self.last_on_ground != self.ev_g_on_ground():
            self.last_on_ground = not self.last_on_ground
            self.send_event('E_PLAY_DASH_DUST_SFX', self.last_on_ground)

    def exit(self, enter_states):
        super(Dash8022, self).exit(enter_states)
        self.end_custom_sound('start')
        self.end_custom_sound('end')
        self.start_custom_sound('end')
        self.sd.ref_forbid_zero_anim_dir = True
        self.send_event('E_FORCE_REPLACE_JUMP_UP_ANIM', None)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_PLAY_DASH_BURST_SFX', False)
        self.send_event('E_PLAY_DASH_DUST_SFX', False)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_END_AIR_DASH')
        if self.costing_fuel:
            self.costing_fuel = False
            self.send_event('E_END_SKILL', self.speed_up_skill_id)
            self.send_event('E_BEGIN_RECOVER_MP', self.speed_up_skill_id)
            self.send_event('E_REPLACE_STATE_PARAM', MC_STAND, MC_STAND)
            self.send_event('E_REPLACE_STATE_PARAM', MC_MOVE, MC_MOVE, include_camera_param=True)
            self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_JUMP_2)
        return

    def on_fuel_exhausted(self, *args):
        if self.is_active:
            if self.sub_state == self.STATE_SPEED_UP:
                self.disable_self()

    def on_touch_ground(self, *args):
        self.can_air_burst = True
        if self.is_active:
            self.send_event('E_DISABLE_STATE', MC_JUMP_2)
            if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                self.send_event('E_ACTIVE_STATE', MC_MOVE)
            else:
                self.send_event('E_ACTIVE_STATE', MC_STAND)

    def set_air_burst_duration(self, duration):
        self.burst_duration = duration
        self.register_callbacks()


@editor.state_exporter({('burst_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe7\xaa\x81\xe8\xbf\x9b\xe9\x80\x9f\xe5\xba\xa6'},('burst_duration', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe7\xaa\x81\xe8\xbf\x9b\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.on_init_complete()
                                 }
   })
class AirDash(StateBase):
    BIND_EVENT = {'G_CHECK_CAN_AIR_DASH': 'check_can_air_dash',
       'E_ACTIVATE_AIR_DASH': 'activate_air_dash',
       'E_END_AIR_DASH': 'on_end_air_dash'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.burst_anim_name = self.custom_param.get('burst_anim_name', None)
        self.burst_speed = self.custom_param.get('burst_speed', 30) * NEOX_UNIT_SCALE
        self.burst_duration = self.custom_param.get('burst_duration', 0.5)
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AirDash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.waiting_enter = False
        self.need_end_air_dash = False

    def on_init_complete(self):
        super(AirDash, self).on_init_complete()
        self.send_event('E_AIR_BURST_DURATION', self.burst_duration)

    def enter(self, leave_states):
        super(AirDash, self).enter(leave_states)
        self.waiting_enter = False
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_POST_ACTION', self.burst_anim_name, LOW_BODY, 6, loop=True)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', 0)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            rotation = self.ev_g_rotation()
            move_dir = rotation.rotate_vector(rocker_dir)
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', rocker_dir.x, rocker_dir.z)
        else:
            move_dir = self.ev_g_forward()
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        self.sd.ref_cur_speed = self.burst_speed
        self.send_event('E_SET_WALK_DIRECTION', move_dir * self.burst_speed)

    def check_transitions(self):
        if self.elapsed_time >= self.burst_duration or self.need_end_air_dash:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                else:
                    return MC_STAND

            else:
                return MC_JUMP_2

    def exit(self, enter_states):
        super(AirDash, self).exit(enter_states)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
        self.send_event('E_RESET_GRAVITY')
        if self.need_end_air_dash:
            self.need_end_air_dash = False

    def check_can_air_dash(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        return True

    def activate_air_dash(self):
        self.active_self()
        self.waiting_enter = True
        self.need_end_air_dash = False

    def on_end_air_dash(self):
        if self.waiting_enter or self.is_active:
            self.need_end_air_dash = True