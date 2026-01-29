# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/SkillLogic.py
from __future__ import absolute_import
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.common_utils import status_utils
import logic.gcommon.const as g_const
import game3d
import world
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.character_anim_const import EXTERN_BODY_1
from logic.comsys.control_ui.ShotChecker import ShotChecker
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gcommon.common_const import attr_const
from logic.gcommon import editor

class SwordEnergy(StateBase):
    MAX_ATTACK_STAGE = 3
    ATTACK_END = 0
    ATTACK_1 = 1
    ATTACK_2 = 2
    ATTACK_3 = 3
    BIND_EVENT = {'E_ON_TOUCH_GROUND': 'on_ground',
       'E_LOGIC_ON_GROUND': 'on_ground'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SwordEnergy, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param['skill_id']
        self.attack_param = self.custom_param['attack_param']
        self.attack_param_air = self.custom_param['attack_param_air']
        self.combo_move_status = status_utils.convert_status(self.custom_param.get('break_states', set([MC_MOVE, MC_JUMP_1, MC_DASH])))
        self.sub_state = self.ATTACK_END
        self.fire_forward, self.fire_position = (None, None)
        self.continue_fire = False
        self.can_combo_attack = False
        self.can_move = False
        self.is_bounce = False
        self.max_height = 0
        self.need_transparent = not self.ev_g_is_agent() and 201800254 <= self.ev_g_mecha_fashion_id() <= 201800256
        return None

    def reset_attack_events(self, stage):
        self.reset_sub_states_callback()
        param = self.attack_param if self.ev_g_on_ground() else self.attack_param_air
        self.register_attack_events(stage, param[stage])
        clip, part, blend_dir = param[stage]['anim']
        self.send_event('E_POST_ACTION', clip, UP_BODY, blend_dir, timeScale=self.timer_rate)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)

    def register_attack_events(self, substate, param):
        pos_factor_name = 'fShootSpeedFactor_pos_{}'.format(1)
        pos_factor = self.ev_g_add_attr(pos_factor_name)
        common_factor = self.ev_g_add_attr(attr_const.ATTR_SHOOTSPEED_FACTOR)
        factor = 1 / (1 + pos_factor + common_factor)
        fire, combo_move, combo, end = (param['fire'], param['combo_move'], param['combo'], param['end'])
        fire *= factor
        combo_move *= factor
        combo *= factor
        end *= factor
        combo_break = combo_move + 0.1
        self.register_substate_callback(substate, 0, self.reset_param)
        self.register_substate_callback(substate, fire, self.fire)
        self.register_substate_callback(substate, combo_move, self.combo_move)
        self.register_substate_callback(substate, combo_break, self.combo_break)
        self.register_substate_callback(substate, end, self.end_attack)
        start_bounce_param = param.get('start_bounce', None)
        if start_bounce_param:
            start_bounce_time, max_move_height = start_bounce_param['time'], start_bounce_param['max_move_height']
            max_move_height *= NEOX_UNIT_SCALE
            up_pass_time, dest_up_vertical_speed = start_bounce_param['up_pass_time'], start_bounce_param['up_vertical_speed']
            dest_up_vertical_speed *= NEOX_UNIT_SCALE
            self.register_substate_callback(substate, start_bounce_time, self.up_bounce, up_pass_time, dest_up_vertical_speed)
            down_pass_time = start_bounce_param['down_pass_time']
            down_bounce_time = start_bounce_time + up_pass_time
            self.register_substate_callback(substate, down_bounce_time, self.down_bounce, down_pass_time)
            end_bounce_time = down_bounce_time + down_pass_time
            self.register_substate_callback(substate, end_bounce_time, self.end_bounce)
            allow_max_height = 0
            physical_position = self.ev_g_phy_position()
            if physical_position:
                allow_max_height = max_move_height + physical_position.y
            if self.max_height > 0:
                if allow_max_height > self.max_height:
                    allow_max_height = self.max_height
            self.send_event('E_ADD_BLACK_STATE', set([MC_MOVE, MC_RUN]))
            self.send_event('E_CLEAR_SPEED')
            self.send_event('E_ENABLE_MOVE_IN_AIR', False)
            if allow_max_height > 0:
                self.max_height = allow_max_height
        self.register_substate_callback(substate, combo, self.combo)
        return

    def setup_fire_direction(self):
        if self.ev_g_is_agent():
            self.fire_forward = self.ev_g_forward()
            self.fire_position = self.ev_g_position()
        else:
            scn = world.get_active_scene()
            camera = scn.active_camera
            self.fire_forward = camera.rotation_matrix.forward
            self.fire_position = camera.position

    def reset_param(self, *args):
        self.can_combo_attack = False
        self.can_move = False
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)

    def on_ground(self, *args):
        self.max_height = 0
        self.send_event('E_CLEAR_BLACK_STATE')

    def fire(self, *args):
        self.setup_fire_direction()
        self.send_event('E_SWORD_ENERGY_FIRE', self.sub_state)
        self.send_event('E_DO_SKILL', self.skill_id, self.sub_state, self.fire_position, self.fire_forward)

    def combo_move(self, *args):
        self.send_event('E_ADD_WHITE_STATE', self.combo_move_status, self.sid)
        if self.ev_g_on_ground():
            self.send_event('E_ADD_WHITE_STATE', {MC_MOVE}, self.sid)

    def combo(self, *args):
        self.can_combo_attack = True
        if self.continue_fire and self.ev_g_can_cast_skill(self.skill_id):
            self.combo_attack()
        self.send_event('E_ADD_WHITE_STATE', {MC_CUT_RUSH}, self.sid)

    def combo_break(self, *args):
        self.can_move = True

    def up_bounce(self, pass_time, dest_up_vertical_speed, *args):
        if self.ev_g_on_ground():
            return
        self.send_event('E_VERTICAL_SPEED', dest_up_vertical_speed)
        self.is_bounce = True

    def down_bounce(self, pass_time, *args):
        if self.ev_g_on_ground():
            return
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_RESET_GRAVITY')

    def end_bounce(self, *args):
        self.send_event('E_UNLIMIT_HEIGHT')
        self.send_event('E_RESET_GRAVITY')
        self.is_bounce = False

    def end_attack(self):
        self.disable_self()
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        return

    def combo_attack(self):
        if not self.can_combo_attack:
            return
        self.sub_state = self.ev_g_attack_stage()
        self.sub_state += 1
        if self.sub_state > self.MAX_ATTACK_STAGE:
            self.sub_state = 1
        self.send_event('E_ATTACK_STAGE', self.sub_state)
        self.reset_attack_events(self.sub_state)
        self.can_combo_attack = False

    def action_btn_down(self):
        if ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.ev_g_can_cast_skill(self.skill_id):
            return
        if not self.is_active:
            self.active_self()
        else:
            self.combo_attack()
        self.continue_fire = True
        return True

    def action_btn_up(self):
        self.continue_fire = False
        return True

    def enter(self, leave_states):
        self.fired_time = 0
        if self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')
        self.can_combo_attack = True
        self.combo_attack()
        super(SwordEnergy, self).enter(leave_states)
        if self.need_transparent and not self.sd.ref_on_ground:
            from data.camera_state_const import MECHA_8002_SS_AIR_SHOOT
            global_data.player.logic.send_event('E_MECHA_CAMERA', MECHA_8002_SS_AIR_SHOOT)

    def update(self, dt):
        super(SwordEnergy, self).update(dt)

    def check_transitions(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero and self.can_move:
            return MC_MOVE

    def exit(self, enter_states):
        self.send_event('E_UNLIMIT_HEIGHT')
        self.send_event('E_ENABLE_MOVE_IN_AIR', True)
        super(SwordEnergy, self).exit(enter_states)
        if self.is_bounce:
            self.end_bounce()
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_ANIM_RATE', UP_BODY, 1)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if self.need_transparent:
            from data.camera_state_const import MELEE_MECHA_MODE
            global_data.player.logic.send_event('E_MECHA_CAMERA', MELEE_MECHA_MODE)

    def destroy(self):
        super(SwordEnergy, self).destroy()


class SwordCore(StateBase):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SwordCore, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param['skill_id']
        self.anim_duration = self.custom_param.get('anim_duration', 1.8)
        self.do_skill_time = self.custom_param.get('do_skill_time', 0.4)

    def action_btn_down(self):
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(SwordCore, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        self.delay_call(self.do_skill_time, lambda : self.send_event('E_DO_SKILL', self.skill_id))

    def update(self, dt):
        super(SwordCore, self).update(dt)

    def check_transitions(self):
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero and self.elapsed_time > self.do_skill_time + 0.25:
            return MC_MOVE
        if self.elapsed_time > self.anim_duration:
            return MC_STAND


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('pre_time', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.init_sub_state_events
                           },
   ('post_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.init_sub_state_events
                            },
   ('post_anim_blend_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe8\x9e\x8d\xe5\x90\x88\xe6\x97\xb6\xe9\x95\xbf'},('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.init_sub_state_events
                                  },
   ('force_pre', 'param'): {'zh_name': '\xe6\x98\xaf\xe5\x90\xa6\xe5\xbc\xba\xe5\x88\xb6\xe5\x89\x8d\xe6\x91\x87','attr_name': '_force_pre'}})
class AccumulateSkill(StateBase):
    BIND_EVENT = {'TRY_STOP_WEAPON_ATTACK': 'disable_self'
       }
    STATE_NONE = 0
    STATE_PRE = 1
    STATE_HOLD = 2
    STATE_FIRE = 3
    STATE_KEEP_AIM = 4
    STATE_POST = 5
    IGNORE_PRE_STATE = set([STATE_HOLD])

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateSkill, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.up_bone = self.custom_param.get('up_bone', None)
        self.read_anim_param_from_local()
        self.post_forbid_state = self.custom_param.get('post_forbid_state', None)
        if self.post_forbid_state:
            self.post_forbid_state = status_utils.convert_status(self.post_forbid_state)
        self.sub_state = self.STATE_NONE
        self.can_break = False
        self.action_hold = False
        self._show_track = self.custom_param.get('show_track', False)
        self._repalce_stand = self.custom_param.get('replace_stand', True)
        self.init_sub_state_events()
        self._force_pre = self.custom_param.get('force_pre', False)
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.aim_ai_pitch_limit = self.custom_param.get('aim_ai_pitch_limit', None)
        return

    def init_sub_state_events(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, self.pre_time, self.pre_end)
        self.register_substate_callback(self.STATE_POST, self.post_break_time, self.post_break)
        self.register_substate_callback(self.STATE_POST, self.post_time, self.post_end)

    def pre_end(self):
        if self.sub_state != self.STATE_PRE:
            return
        self.sub_state = self.STATE_HOLD
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.hold_anim, True, loop=True)
        else:
            self.send_event('E_POST_ACTION', self.hold_anim, UP_BODY, 1, loop=True, blend_time=0.0)
        if not self.action_hold:
            self.do_skill()
            return
        self.replace_stand(self.hold_anim, True)
        self.show_track(True)

    def do_skill(self, is_quick_attack=False):
        self.sub_state = self.STATE_POST
        self.show_track(False)
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.post_anim, True)
        else:
            self.send_event('E_POST_ACTION', self.post_anim, UP_BODY, 1, loop=False, blend_time=self.post_anim_blend_time)
            self.replace_stand(self.post_anim, False)
        self.replace_move(None)
        if self.post_forbid_state:
            self.send_event('E_ADD_BLACK_STATE', self.post_forbid_state)
            self.send_event('E_BRAKE')
        scn = world.get_active_scene()
        camera = scn.active_camera
        self.fire_forward = camera.rotation_matrix.forward
        self.fire_position = camera.position

        def delay_do_skill():
            if not self or not self.is_valid():
                return
            self.send_event('E_DO_SKILL', self.skill_id, 0, self.fire_position, self.fire_forward)
            super(AccumulateSkill, self).sound_custom_end()

        global_data.game_mgr.next_exec(delay_do_skill)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        return

    def post_break(self):
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_ACC_SKILL_END', self.skill_id)
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE}, self.sid)
        self.replace_move(None, True)
        self.can_break = True
        return

    def post_end(self):
        self.can_break = False
        self.sub_state = self.STATE_NONE
        self.disable_self()
        self.send_event('E_ACTION_UP', self.bind_action_id)
        if self._show_track:
            self.send_event('E_STOP_ACC_WP_TRACK')

    def action_btn_down(self):
        super(AccumulateSkill, self).action_btn_down()
        if ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        super(AccumulateSkill, self).sound_custom_start()
        if self.can_break:
            return self.enter(set())
        self.active_self()
        if not self.action_hold:
            self.send_event('E_RESET_ROTATION')
        self.action_hold = True
        return True

    def action_btn_up(self):
        super(AccumulateSkill, self).action_btn_up()
        if not self.is_active:
            return
        self.action_hold = False
        if self._force_pre:
            acted = self.sub_state == self.STATE_HOLD
        else:
            acted = True
        if acted and self.STATE_NONE < self.sub_state < self.STATE_POST:
            self.do_skill()
        return True

    def enter(self, leave_states):
        super(AccumulateSkill, self).enter(leave_states)
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.pre_anim, True)
        else:
            self.send_event('E_POST_ACTION', self.pre_anim, UP_BODY, 1)
        self.replace_stand(self.pre_anim, False)
        self.replace_move(self.hold_move_anim, True)
        if self.up_bone:
            self.send_event('E_UPBODY_BONE', self.up_bone['enter'], EXTERN_BODY_1)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.sub_state = self.STATE_PRE
        self.can_break = False
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_ACC_SKILL_BEGIN', self.skill_id)
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.post_end)

        def reset_param():
            if self.shoot_aim_ik:
                self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik)
                args = (True, self.aim_ai_pitch_limit) if self.aim_ai_pitch_limit else (True,)
                self.send_event('E_ENABLE_AIM_IK', *args)
                self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time)

        self.delay_call(self.pre_aim_ik_time, reset_param)
        return

    def update(self, dt):
        super(AccumulateSkill, self).update(dt)

    def check_transitions(self):
        if self.sub_state == self.STATE_NONE:
            self.disable_self()

    def show_track(self, show):
        if not self._show_track:
            return
        if show:
            self.send_event('E_SHOW_ACC_WP_TRACK')
        else:
            self.send_event('E_STOP_ACC_WP_TRACK')

    def exit(self, enter_states):
        super(AccumulateSkill, self).exit(enter_states)
        self.sub_state = self.STATE_NONE
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.replace_move(None, True)
        self.replace_stand(None, True)
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_SLOW_DOWN', False)
        self.send_event('E_ACC_SKILL_END', self.skill_id)
        if self.up_bone:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.show_track(False)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        return

    def refresh_action_param(self, action_param, custom_param):
        super(AccumulateSkill, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_anim_param_from_local()

    def read_anim_param_from_local(self):
        self.pre_anim = self.custom_param.get('pre_anim', None)
        self.hold_anim = self.custom_param.get('hold_anim', None)
        self.hold_move_anim = self.custom_param.get('hold_move_anim', None)
        self.post_anim = self.custom_param.get('post_anim', None)
        self.pre_time = self.custom_param.get('pre_time', 0.53)
        self.post_time = self.custom_param.get('post_time', 1.67)
        self.post_anim_blend_time = self.custom_param.get('post_anim_blend_time', 0.2)
        self.post_break_time = self.custom_param.get('post_break_time', 0.9)
        return

    def can_set_anim_param(self):
        return self.sub_state == self.STATE_NONE

    def replace_stand(self, anim, is_loop=False):
        if self._repalce_stand:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, anim, loop=is_loop)

    def replace_move(self, anim, is_loop=False):
        if self.hold_move_anim:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, anim, loop=is_loop)


class AccumulateSkill_M8(AccumulateSkill):
    IGNORE_PRE_STATE = set([AccumulateSkill.STATE_PRE, AccumulateSkill.STATE_HOLD, AccumulateSkill.STATE_FIRE, AccumulateSkill.STATE_KEEP_AIM])

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(AccumulateSkill_M8, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.hold_time = self.custom_param.get('hold_time', 2.0)
        self.fire_time = self.custom_param.get('fire_time', 2.0)
        self.aim_time = self.custom_param.get('aim_time', 2.0)
        self.fire_anim = self.custom_param.get('fire_anim', None)
        self.aim_anim = self.custom_param.get('aim_anim', None)
        self.fire_interval = self.custom_param.get('fire_interval', 0.1)
        self.last_fire_time = -1
        self.exit_default_anim = self.custom_param.get('exit_default_anim', 'idle_tower')
        return

    def enter(self, leave_states):
        super(AccumulateSkill_M8, self).enter(leave_states)
        self.send_event('E_SHOW_TOWER_RANGE', self.skill_id)
        self.register_substate_callback(self.STATE_PRE, self.pre_time, self.pre_end)

    def do_skill(self, is_quick_attack=False):
        self.show_track(False)
        self.send_event('E_STOP_TOWER_RANGE', self.skill_id)
        self.replace_move(None)
        self.reset_sub_state_timer()
        if is_quick_attack:
            self.hold_end()
        else:
            self.reset_sub_state_callback(self.STATE_HOLD)
            self.register_substate_callback(self.STATE_HOLD, self.hold_time, self.hold_end)
        if self.elapsed_time - self.last_fire_time >= self.fire_interval:
            scn = world.get_active_scene()
            camera = scn.active_camera
            self.fire_forward = camera.rotation_matrix.forward
            self.fire_position = camera.position
            self.send_event('E_DO_SKILL', self.skill_id, 0, self.fire_position, self.fire_forward)
            self.last_fire_time = self.elapsed_time
            global_data.sound_mgr.play_sound_optimize('m_8008_weapon1_fire_1p', self.unit_obj, None, ('m_8008_weapon1_fire_1p',
                                                                                                      'nf'))
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        return

    def keep_aim_end(self):
        self.sub_state = self.STATE_POST
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.post_anim, True)
        else:
            self.send_event('E_POST_ACTION', self.post_anim, UP_BODY, 1, loop=False)
            self.replace_stand(self.post_anim, False)
        if self.post_forbid_state:
            self.send_event('E_ADD_BLACK_STATE', self.post_forbid_state)
            self.send_event('E_BRAKE')

    def fire_end(self):
        self.sub_state = self.STATE_KEEP_AIM
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.aim_anim, True, loop=True)
        else:
            self.send_event('E_POST_ACTION', self.aim_anim, UP_BODY, 1, loop=True)
            self.replace_stand(self.aim_anim, False)
        self.reset_sub_state_timer()
        self.reset_sub_state_callback(self.STATE_KEEP_AIM)
        self.register_substate_callback(self.STATE_KEEP_AIM, self.aim_time, self.keep_aim_end)

    def hold_end(self):
        self.sub_state = self.STATE_FIRE
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.fire_anim, True)
        else:
            self.send_event('E_POST_ACTION', self.fire_anim, UP_BODY, 1)
            self.replace_stand(self.fire_anim, False)
        self.reset_sub_state_timer()
        self.reset_sub_state_callback(self.STATE_FIRE)
        self.register_substate_callback(self.STATE_FIRE, self.fire_time, self.fire_end)

    def action_btn_down(self):
        super(AccumulateSkill_M8, self).action_btn_down()
        if self.action_hold:
            return
        else:
            if self.is_active and self.sub_state in self.IGNORE_PRE_STATE:
                self.action_hold = True
                self.reset_sub_state_timer()
                if self.ev_g_is_avatar():
                    from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                    MechaCancelUI(None, self.post_end)
                if self.ev_g_can_cast_skill(self.skill_id):
                    for one_sub_state in self.IGNORE_PRE_STATE:
                        self.reset_sub_state_callback(one_sub_state)

                    self.show_track(True)
                    self.send_event('E_SHOW_TOWER_RANGE', self.skill_id)
            return

    def action_btn_up(self):
        super(AccumulateSkill, self).action_btn_up()
        self.action_hold = False
        if not self.is_active:
            return
        if self.sub_state in self.IGNORE_PRE_STATE and self.ev_g_can_cast_skill(self.skill_id):
            self.do_skill(True)
        return True

    def exit(self, enter_states):
        super(AccumulateSkill_M8, self).exit(enter_states)
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.exit_default_anim, False)
        for one_sub_state in self.IGNORE_PRE_STATE:
            self.reset_sub_state_callback(one_sub_state)

        self.send_event('E_STOP_TOWER_RANGE', self.skill_id)
        self.last_fire_time = -1
        self.action_hold = False


class MaxHeat(StateBase):
    BIND_EVENT = {'E_TRY_IN_MAX_HEAT': 'try_in_max_heat',
       'E_TRY_OUT_MAX_HEAT': 'try_out_max_heat'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MaxHeat, self).init_from_dict(unit_obj, bdict, sid, info)
        self.max_heat_enter_time = self.ev_g_max_heat_enter_time()

    def enter(self, leave_states):
        super(MaxHeat, self).enter(leave_states)
        self.need_in_max_heat = True
        self.need_out_max_heat = False
        self.send_event('E_POST_ADD_ANIMATION', True, 'pose_b', 'pose_a')

    def update(self, dt):
        super(MaxHeat, self).update(dt)
        if self.need_in_max_heat:
            self.send_event('E_REFRESH_STATE_PARAM')
            self.need_in_max_heat = False
        if self.need_out_max_heat:
            self.send_event('E_RESET_STATE_PARAM')
            self.disable_self()

    def exit(self, enter_states):
        self.send_event('E_POST_ADD_ANIMATION', False)
        super(MaxHeat, self).exit(enter_states)

    def action_btn_down(self):
        if self.is_active:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'enter_max_heat_state', (), True)

    def try_in_max_heat(self, **args):
        if self.check_can_active():
            self.active_self()
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8004_weapon1_start',
                                                                'nf'), 0, 0, None, None)
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8004_weapon1_loop',
                                                                'nf'), 0, 1, None, None)
        else:
            log_error('\xe8\xbf\x9b\xe5\x85\xa5\xe7\x83\xad\xe7\x88\x86\xe7\x8a\xb6\xe6\x80\x81\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe7\x8a\xb6\xe6\x80\x81\xe8\xa1\xa8\xef\xbc\x81\xef\xbc\x81')
        return

    def try_out_max_heat(self):
        self.need_out_max_heat = True
        self.send_event('E_RESET_STATE_PARAM')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, ('m_8004_weapon1_loop',
                                                            'nf'), 0, 1, None, None)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8004_weapon1_end', 'nf'), 0, 0, None, None)
        return


class PhotonShield(StateBase):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(PhotonShield, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param['skill_id']
        self._extern_anim = self.custom_param.get('anim', 'tower_shield')
        self.up_bone = self.custom_param.get('up_bone', None)
        self._total_time = self.custom_param.get('total_time', 0.5)
        return

    def action_btn_down(self):
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(PhotonShield, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.skill_id)

    def check_transitions(self):
        if self.elapsed_time > self._total_time:
            self.disable_self()

    def exit(self, enter_states):
        super(PhotonShield, self).exit(enter_states)


class PhotonAttack(StateBase):
    BIND_EVENT = {}
    ATTACK_BEGIN = 0

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(PhotonAttack, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param['skill_id']
        self._extern_anim = self.custom_param.get('anim', 'laser_backpack')
        self.up_bone = self.custom_param.get('up_bone', None)
        self._laser_time = self.custom_param.get('laser_time', 0.5)
        self._total_time = self.custom_param.get('total_time', 1)
        return

    def action_btn_down(self):
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(PhotonAttack, self).enter(leave_states)
        if self.up_bone:
            self.send_event('E_UPBODY_BONE', self.up_bone['enter'], EXTERN_BODY_1)
            self.send_event('E_POST_EXTERN_ACTION', self._extern_anim, True)
            self.delay_call(self._laser_time, self._laser_attack)
            self.send_event('E_SHOW_BACK_WEAPON_ANIM')

    def _laser_attack(self):
        self.send_event('E_DO_SKILL', self.skill_id)

    def check_transitions(self):
        if self.elapsed_time > self._total_time:
            self.disable_self()

    def exit(self, enter_states):
        super(PhotonAttack, self).exit(enter_states)
        if self.up_bone:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
            self.send_event('E_POST_EXTERN_ACTION', 'idle_tower', False)


class PhotonReload(StateBase):
    BIND_EVENT = {}
    ATTACK_BEGIN = 0

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(PhotonReload, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._extern_anim = self.custom_param.get('anim', 'reload_tower')
        self.up_bone = self.custom_param.get('up_bone', None)
        self._total_time = self.custom_param.get('total_time', 1)
        return

    def enter(self, leave_states):
        super(PhotonReload, self).enter(leave_states)
        if self.up_bone:
            self.send_event('E_UPBODY_BONE', self.up_bone['enter'], EXTERN_BODY_1)
            self.send_event('E_POST_EXTERN_ACTION', self._extern_anim, True)

    def check_transitions(self):
        if self.elapsed_time > self._total_time:
            self.disable_self()

    def exit(self, enter_states):
        super(PhotonReload, self).exit(enter_states)
        if self.up_bone:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
            self.send_event('E_POST_EXTERN_ACTION', 'idle_tower', False)


class CommonCastSkill(StateBase):
    BIND_EVENT = {}

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(CommonCastSkill, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.skill_anim = self.custom_param.get('skill_anim', 0)
        self.anim_time = self.custom_param.get('anim_time', 0)
        self.cast_time = self.custom_param.get('cast_time', 0)
        self.hard_time = self.custom_param.get('hard_time', 0)
        self.hard_state = self.custom_param.get('hard_state', None)
        self.ignore_reload_anim = self.custom_param.get('ignore_reload_anim', False)
        if self.hard_state:
            self.hard_state = status_utils.convert_status(self.hard_state)
        return

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        self.active_self()
        self.send_event('E_RESET_ROTATION')
        super(CommonCastSkill, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(CommonCastSkill, self).enter(leave_states)
        if self.skill_anim:
            self.send_event('E_POST_ACTION', self.skill_anim, UP_BODY, 1)
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.skill_anim, loop=False)
        self.delay_call(self.cast_time, self.cast_skill)
        if self.ignore_reload_anim:
            self.send_event('E_IGNORE_RELOAD_ANIM', True)

    def check_transitions(self):
        if self.elapsed_time > self.anim_time:
            self.disable_self()

    def cast_skill(self):
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        if not self.hard_time or not self.hard_state:
            return
        if self.hard_state:
            self.send_event('E_ADD_BLACK_STATE', self.hard_state)
            self.send_event('E_BRAKE')
            self.delay_call(self.hard_time, self.post_break)

    def post_break(self):
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE}, self.sid)

    def exit(self, enter_states):
        super(CommonCastSkill, self).exit(enter_states)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.ignore_reload_anim:
            self.send_event('E_IGNORE_RELOAD_ANIM', False)
        return