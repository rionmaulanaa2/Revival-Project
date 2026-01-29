# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8005.py
from __future__ import absolute_import
from .StateBase import StateBase
from .JumpLogic import SuperJumpUpPure, on_super_jump_success
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gutils.character_ctrl_utils import cal_jump_param
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata import jump_physic_config
from logic.gcommon.common_const import mecha_const
from logic.gcommon.common_utils import status_utils
from logic.gutils import detection_utils
import math3d
import math

class RocketJump(StateBase):
    JUMP_UP = 0
    JUMP_FALL = 1
    JUMP_GROUND = 2
    BIND_EVENT = {'E_SKILL_INIT_COMPLETE': ('on_skill_init_complete', 10),
       'E_UPDATE_SKILL_ATTR': ('on_skill_attr_update', 10),
       'E_IMMOBILIZED': 'end_button_down',
       'E_ON_FROZEN': 'end_button_down',
       'E_ENTER_STATE': 'enter_states'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(RocketJump, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.tick_interval = self.custom_param.get('tick_interval', 0.2)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.base_jump_height = self.custom_param.get('base_jump_height', 15) * NEOX_UNIT_SCALE
        self.fall_anim = self.custom_param.get('fall_anim', 'jump_02')
        self.on_ground_anim = self.custom_param.get('on_ground_anim', 'jump_03')
        self.recover_time = self.custom_param.get('recover_time', 1)
        self.jump_gravity = self.custom_param.get('jump_gravity', 100) * NEOX_UNIT_SCALE
        self.max_jump_dist = self.custom_param.get('max_dist', 70) * NEOX_UNIT_SCALE
        self.break_states = status_utils.convert_status(self.custom_param.get('break_states', set([MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_JUMP_1, MC_DASH])))
        self.break_time = self.custom_param.get('break_time', 0.5)
        self.onground_sfx_type = self.custom_param.get('onground_sfx_type', None)
        self.onground_sfx_time = self.custom_param.get('onground_sfx_time', 0.1)
        self.register_substate_callback(self.JUMP_GROUND, self.break_time, lambda : self.send_event('E_ADD_WHITE_STATE', self.break_states, self.sid))
        self.hold_stand_anim = self.custom_param.get('hold_stand_anim', 'shockwave_02')
        self.hold_move_anim = self.custom_param.get('hold_move_anim', 'shockwave_move')
        self.on_ground_time = 0
        self.sub_state = -1
        self.vertical_speed = 0
        self.detecting = False
        self.target_pos = None
        self.showing_dash_hint = False
        skill_obj = self.ev_g_skill(self.skill_id)
        if skill_obj:
            data = skill_obj._data or {}
            jump_distance_rate = data.get('ext_info', {}).get('jump_distance_rate', 0)
            if jump_distance_rate > 1.0:
                self.max_jump_dist *= jump_distance_rate
        self.sd.ref_last_rocket_jump_hor_speed = 0
        self.sd.ref_last_rocket_jump_hor_dir = None
        return

    def enter_states(self, state):
        if state in (MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_DEAD, MC_SUPER_JUMP, MC_BEAT_BACK):
            self.end_button_down()

    def destroy(self):
        self.end_button_down()
        if self.detecting:
            detection_utils.stop_jump_pos_detect(self)
        self.unregist_event('E_FALL', self.on_fall)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        super(RocketJump, self).destroy()

    def on_skill_init_complete(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        data = skill_obj._data
        self.max_jump_dist = self.custom_param.get('max_dist', 70) * NEOX_UNIT_SCALE * data.get('ext_info', {}).get('jump_distance_rate', 1)

    def on_skill_attr_update(self, skill_id, *args):
        if skill_id == self.skill_id:
            skill_obj = self.ev_g_skill(self.skill_id)
            data = skill_obj._data
            self.max_jump_dist = self.custom_param.get('max_dist', 70) * NEOX_UNIT_SCALE * data['ext_info']['jump_distance_rate']

    def _show_dash_hint(self, flag):
        if self.showing_dash_hint ^ flag:
            self.showing_dash_hint = flag
            self.send_event('E_SHOW_DASH_HINT', flag)
            if flag:
                self.send_event('E_HIDE_JUMP_TRACK')

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        else:
            if not self.check_can_cast_skill():
                return False
            if self.detecting:
                if not self.ev_g_is_agent():
                    if not detection_utils.get_valid_jump_pos():
                        self._show_dash_hint(True)
            else:
                if self.ev_g_is_avatar():
                    from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                    MechaCancelUI(None, self.end_button_down, True)
                self.detecting = True
                detection_utils.start_jump_pos_detect(self, self.max_jump_dist, detect_callback=self.cal_jump_param)
                detection_utils.detect_jump_pos_wrapper()
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.hold_stand_anim, loop=True)
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, self.hold_move_anim, loop=True)
                self.send_event('E_SLOW_DOWN', True)
            super(RocketJump, self).action_btn_down()
            return True

    def action_btn_up(self):
        if not self.detecting:
            return
        if self.ev_g_is_agent():
            target_pos = self.ev_g_rocket_jump_pos()
        else:
            target_pos = detection_utils.get_valid_jump_pos()
        if target_pos:
            self.target_pos = target_pos
            self.active_self()
        self.end_button_down()
        super(RocketJump, self).action_btn_up()

    def enter(self, leave_states):
        super(RocketJump, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.JUMP_UP
        move_dir = self.cal_jump_param(self.target_pos, False)
        self.send_event('E_SET_WALK_DIRECTION', move_dir)
        self.sd.ref_cur_speed = self.horizon_speed
        self.sd.ref_last_rocket_jump_hor_speed = self.horizon_speed
        move_dir.normalize()
        self.sd.ref_last_rocket_jump_hor_dir = move_dir
        self.send_event('E_GRAVITY', self.jump_gravity)
        self.send_event('E_JUMP', self.vertical_speed)
        self.send_event('E_JET_CAMERA_SHAKE')
        self.regist_event('E_FALL', self.on_fall)
        self.regist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.target_pos = None
        return

    def check_transitions(self):
        if self.sub_state == self.JUMP_GROUND:
            if self.elapsed_time - self.on_ground_time >= self.recover_time:
                self.disable_self()
                return MC_STAND
            rocker_dir = self.sd.ref_rocker_dir
            if rocker_dir and not rocker_dir.is_zero:
                return MC_MOVE

    def exit(self, enter_states):
        super(RocketJump, self).exit(enter_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)

    def on_fall(self, *args):
        if self.sub_state == self.JUMP_GROUND:
            return
        self.sub_state = self.JUMP_FALL
        self.send_event('E_POST_ACTION', self.fall_anim, LOW_BODY, 1)
        self.unregist_event('E_FALL', self.on_fall)

    def on_ground(self, *args):
        if self.sub_state != self.JUMP_FALL:
            self.unregist_event('E_FALL', self.on_fall)
        self.sub_state = self.JUMP_GROUND
        self.send_event('E_POST_ACTION', self.on_ground_anim, LOW_BODY, 1, blend_time=0)
        self.send_event('E_CLEAR_SPEED')
        self.on_ground_time = self.elapsed_time
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.send_event('E_ACTION_SYNC_GROUND', -args[0], mecha_const.MECHA_JUMP_TYPE_ROCKET)
        if self.onground_sfx_type:
            self.delay_call(self.onground_sfx_time, lambda : self.send_event('E_SHOW_ONGROUND_SFX', self.onground_sfx_type))
        self.sound_drive.run_end()
        self.send_event('E_END_SKILL', self.skill_id)

    def cal_jump_param(self, target_pos, show_track=True):
        end_pos = target_pos
        start_pos = self.ev_g_position()
        delta_dir = end_pos - start_pos
        h = self.base_jump_height / self.sd.ref_gravity_scale
        delta_s = math3d.vector(delta_dir.x, 0, delta_dir.z).length
        delta_h = abs(delta_dir.y)
        h_up = delta_h + h if delta_dir.y > 0 else h
        real_gravity = self.jump_gravity * self.sd.ref_gravity_scale
        t_up = math.sqrt(2 * h_up / real_gravity)
        h_fall = delta_h + h if delta_dir.y < 0 else h
        t_fall = math.sqrt(2 * h_fall / real_gravity)
        self.vertical_speed = abs(t_up * real_gravity)
        self.horizon_speed = delta_s / (t_up + t_fall)
        forward = end_pos - start_pos
        forward.y = 0
        if forward.is_zero:
            forward = math3d.vector(0, 0, 1)
        else:
            forward.normalize()
        move_dir = forward * self.horizon_speed
        if show_track:
            self._show_dash_hint(False)
            self.send_event('E_SHOW_JUMP_TRACK', 'effect/fx/niudan/tishitexiao_jiantou.sfx', start_pos, math3d.vector(move_dir.x, self.vertical_speed, move_dir.z), -real_gravity, target_pos)
        return move_dir

    def end_button_down(self, *args):
        if not self.detecting:
            return
        else:
            if self.ev_g_is_avatar():
                global_data.ui_mgr.close_ui('MechaCancelUI')
                self._show_dash_hint(False)
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND, MC_MOVE), None)
            self.send_event('E_SLOW_DOWN', False)
            self.detecting = False
            detection_utils.stop_jump_pos_detect(self)
            self.send_event('E_HIDE_JUMP_TRACK')
            self.send_event('E_ACTION_UP', self.bind_action_id)
            return


class SuperJumpUp8005(SuperJumpUpPure):

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SuperJumpUp8005, self).init_from_dict(unit_obj, bdict, sid, info)
        self.is_normal_jump = False

    def enter(self, leave_states):
        super(SuperJumpUpPure, self).enter(leave_states)
        if MC_DASH in leave_states and self.is_normal_jump:
            h_max_speed = self.jump_args['h_speed'] * NEOX_UNIT_SCALE
            cur_h_scale = self.jump_args['h_scale']
            speed = self.sd.ref_last_rocket_jump_hor_speed or 0
            speed *= cur_h_scale
            self.cur_h_speed = h_max_speed if speed > h_max_speed else speed
            self.cur_jump_dir = self.sd.ref_last_rocket_jump_hor_dir
        self.send_event('E_GRAVITY', self.jump_gravity)
        self.send_event('E_JUMP', self.cur_v_speed)
        self.sd.ref_cur_speed = self.cur_h_speed
        if self.cur_jump_dir is not None:
            self.send_event('E_SET_WALK_DIRECTION', self.cur_jump_dir * self.cur_h_speed)
        self.air_horizontal_offset_speed_setter.reset()
        jump_up_duration = (self.cur_v_speed - jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE) / self.jump_gravity
        self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_duration / jump_up_duration)
        self.send_event('E_JET_CAMERA_SHAKE')
        on_super_jump_success(self.unit_obj, self.jump_args)
        return

    def super_jump(self, jump_args=None):
        jump_args = jump_args or {}
        fixed_jump_pos = jump_args.get('fixed_jump_pos', None)
        fixed_jump_dir = jump_args.get('fixed_jump_dir', None)
        self.is_normal_jump = False
        if fixed_jump_pos:
            from_pos = self.ev_g_position()
            fixed_jump_pos = math3d.vector(*fixed_jump_pos)
            self.cur_jump_dir, self.cur_h_speed, self.cur_v_speed = cal_jump_param(from_pos, fixed_jump_pos, self.jump_gravity, self.jump_gravity)
        elif fixed_jump_dir:
            self.cur_v_speed = jump_args['v_speed'] * NEOX_UNIT_SCALE
            self.cur_h_speed = jump_args['h_speed'] * NEOX_UNIT_SCALE
            self.cur_jump_dir = math3d.vector(*fixed_jump_dir)
            self.cur_jump_dir.normalize()
        else:
            self.is_normal_jump = True
            self.cur_v_speed = jump_args['v_speed'] * NEOX_UNIT_SCALE * jump_args.get('bouncer_speed', 1)
            h_max_speed = jump_args['h_speed'] * NEOX_UNIT_SCALE
            cur_h_scale = jump_args['h_scale']
            speed = self.sd.ref_cur_speed or 0
            speed *= cur_h_scale
            self.cur_h_speed = h_max_speed if speed > h_max_speed else speed
            self.cur_jump_dir = self.ev_g_move_dir()
            if 'top_h_speed' in jump_args:
                self.top_h_speed = jump_args['top_h_speed']
            else:
                self.top_h_speed = None
        self.jump_args = jump_args
        self.active_self()
        return