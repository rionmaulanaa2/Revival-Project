# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic10011.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import math3d
import world
import math
from .StateBase import StateBase
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils import timer
import logic.gcommon.const as g_const
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.cdata.status_config as status_config
from common.cfg import confmgr
from logic.gcommon.cdata import state_physic_arg
from logic.gcommon.cdata import speed_physic_arg
from logic.gutils import character_action_utils
import data.weapon_action_config as weapon_action_config
from logic.gcommon.common_const.skill_const import SKILL_ROLL
from logic.gcommon.common_const import ui_operation_const
from logic.gutils import character_ctrl_utils
import logic.gcommon.common_const.collision_const as collision_const
from logic.gcommon.common_const import water_const
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.utility import enum
from common.framework import Functor
import logic.gutils.move_utils as move_utils
from logic.gcommon.common_utils import parachute_utils
import weakref
import game3d
from logic.gcommon import editor
from common.animate import animator
from ext_package.ext_decorator import has_skin_ext
from logic.gutils import weapon_utils

class RightAim(StateBase):
    BIND_EVENT = {'E_LEAVE_STATE': '_leave_states',
       'E_SUCCESS_RIGHT_AIM': 'try_right_aim',
       'E_QUIT_RIGHT_AIM': 'quit_right_aim'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(RightAim, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.shoot_aim_ik = self.custom_param.get('shoot_aim_ik', None)
        self.aim_ik_lerp_time = self.custom_param.get('aim_ik_lerp_time', 0.2)
        self.pre_aim_ik_time = self.custom_param.get('pre_aim_ik_time', 0.2)
        self.aim_ik_pitch_limit = self.custom_param.get('aim_ik_pitch_limit', 80)
        self.support_exit_aim_ik_lerp = self.custom_param.get('support_exit_aim_ik_lerp', False)
        self.exit_aim_ik_lerp_time = self.custom_param.get('exit_aim_ik_lerp_time', 0.2)
        return

    def on_init_complete(self):
        super(RightAim, self).on_init_complete()
        is_in_right_aim = self.ev_g_attr_get('right_aim_state', False)
        if is_in_right_aim:
            self.try_right_aim()

    def _leave_states(self, leave_state, new_state=None):
        if leave_state != new_state and new_state is not None:
            if leave_state == self.sid:
                self.send_event('E_QUIT_RIGHT_AIM')
        return

    def enter(self, leave_states):
        super(RightAim, self).enter(leave_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY, blend_time=0)
        self.send_event('E_ACTION_IS_SHOOT', 1)
        self.send_event('E_CHANGE_SHOOT_STATE')
        self.send_event('S_ATTR_SET', 'right_aim_state', True)
        self.send_event('E_CALL_SYNC_METHOD', 'right_aim_state', (True,), True)
        if self.ev_g_get_state(self.status_config.ST_STAND):
            clip_name, _, _ = character_action_utils.get_idle_clip(self, self.status_config.ST_STAND)
            dir_type = 1
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=True, blend_time=0.2)
        elif self.ev_g_get_state(self.status_config.ST_CROUCH):
            clip_name, _, _ = character_action_utils.get_idle_clip(self, self.status_config.ST_CROUCH)
            dir_type = 1
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=True, blend_time=0.2)
        elif self.ev_g_get_state(self.status_config.ST_VEHICLE_PASSENGER):
            pass
        else:
            action_key = 'stand_shoot_move'
            if self.ev_g_get_state(status_config.ST_SKATE):
                skate_state = self.ev_g_skate_action()
                skate_action_key = 'skate_' + action_key
                clip_list = self.ev_g_weapon_action_list(skate_action_key)
                if clip_list:
                    action_key = skate_action_key
            character_action_utils.change_human_walk_animation(self, action_key)
        self._reset_aim_ik_param()

    def exit(self, enter_states):
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)

    def _reset_aim_ik_param(self):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return None
        else:
            open_ik = confmgr.get('firearm_config', str(obj_weapon.get_item_id()), 'iOpenIk')
            if not open_ik:
                return None
            if self.shoot_aim_ik:
                self.send_event('E_AIM_IK_PARAM', self.shoot_aim_ik, self.support_exit_aim_ik_lerp)
                self.send_event('E_ENABLE_AIM_IK', True, self.aim_ik_pitch_limit)
                self.send_event('E_AIM_LERP_TIME', self.aim_ik_lerp_time, self.exit_aim_ik_lerp_time)
            return None

    def try_right_aim(self):
        if self.is_active:
            return
        if not self.check_can_active():
            return
        self.active_self()

    def quit_right_aim(self):
        self.send_event('S_ATTR_SET', 'right_aim_state', False)
        self.send_event('E_CALL_SYNC_METHOD', 'right_aim_state', (False,), True)
        self.send_event('E_CHANGE_SPEED')


class Aim(StateBase):
    BIND_EVENT = {'E_SUCCESS_AIM': '_try_aim',
       'E_QUIT_AIM': '_quit_aim',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_MOVE': 'on_move'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Aim, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def on_init_complete(self):
        super(Aim, self).on_init_complete()
        is_in_aim = self.ev_g_attr_get('aim_state', False)
        if is_in_aim:
            self._try_aim()

    def enter_states(self, new_state):
        if new_state == self.sid:
            global_data.emgr.ui_enter_aim.emit()

    def _leave_states(self, leave_state, new_state=None):
        if leave_state != new_state:
            if leave_state == self.sid:
                global_data.emgr.ui_leave_aim.emit()
                self.send_event('E_QUIT_AIM')

    def enter(self, leave_states):
        super(Aim, self).enter(leave_states)
        self.send_event('E_ACTION_IS_SHOOT', 1)
        self.send_event('E_CALL_SYNC_METHOD', 'aim_state', (True,), True)
        animator = self.ev_g_animator()
        if animator:
            animator.enable_force_update(True)

    def exit(self, enter_states):
        super(Aim, self).exit(enter_states)
        self.send_event('E_CHANGE_SPEED')
        self.send_event('E_CALL_SYNC_METHOD', 'aim_state', (False,), True)
        animator = self.ev_g_animator()
        if animator:
            animator.enable_force_update(False)

    def on_move(self, move_dir, target_callback=None, target_pos=None):
        if not self.is_active:
            return
        if not move_dir or move_dir.is_zero:
            return
        self.send_event('E_ACTION_MOVE', move_dir)

    def _quit_aim(self):
        if not self.is_active:
            return
        self.disable_self()

    def _try_aim(self):
        if self.is_active:
            return
        if not self.check_can_active():
            return
        self.active_self()


class WeaponAccumulate(StateBase):
    BIND_EVENT = {'E_SUCCESS_AIM': 'try_aim',
       'E_QUIT_AIM': 'quit_aim'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponAccumulate, self).init_from_dict(unit_obj, bdict, sid, state_info)
        global_data.emgr.ion_gun_accumulate_aim_cancel_event += self.on_cancel_change

    def on_cancel_change(self):
        self.show_cancel_in_aim = weapon_utils.ion_gun_accumulate_aim_cancel_enable()

    def on_init_complete(self):
        super(WeaponAccumulate, self).on_init_complete()
        self.is_in_aim = self.ev_g_attr_get('aim_state', False)
        self.on_cancel_change()

    def enter(self, leave_states):
        super(WeaponAccumulate, self).enter(leave_states)
        if self.ev_g_is_avatar() and (not self.is_in_aim or self.show_cancel_in_aim):
            from logic.comsys.battle.HumanCancelUI import HumanCancelUI
            HumanCancelUI(None, self.disable_self)
        return

    def exit(self, enter_states):
        super(WeaponAccumulate, self).exit(enter_states)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('HumanCancelUI')

    def try_aim(self):
        self.is_in_aim = True

    def quit_aim(self):
        self.is_in_aim = False


@editor.state_exporter({('roll_duration', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe6\x97\xb6\xe9\x95\xbf','min_val': 0.0,'max_val': 5},('damp_duration', 'param'): {'zh_name': '\xe9\x80\x9f\xe5\xba\xa6\xe5\xbc\x80\xe5\xa7\x8b\xe8\xa1\xb0\xe5\x87\x8f\xe6\x97\xb6\xe9\x97\xb4','min_val': 0.0,'max_val': 5},('default_roll_speed', 'meter'): {'zh_name': '\xe9\xbb\x98\xe8\xae\xa4\xe7\xbf\xbb\xe6\xbb\x9a\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 150},('first_adjust_speed', 'meter'): {'zh_name': '\xe5\x9f\xba\xe5\x87\x86\xe7\xbb\xa7\xe6\x89\xbf\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 150},('roll_end_speed', 'meter'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe6\x9c\xab\xe5\xb0\xbe\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 150},('anim_scale', 'param'): {'zh_name': '\xe7\xbf\xbb\xe6\xbb\x9a\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','min_val': 0.01,'max_val': 20}})
class Roll(StateBase):
    BIND_EVENT = {'E_CTRL_ROLL': 'roll',
       'E_WAIT_FINISH_ROLL_EVENT': '_set_wait_event',
       'E_ENERGY_CHANGE': '_roll_cd_change',
       'E_LEAVE_STATE': 'leave_states',
       'G_ROLL_DIR': 'get_roll_dir'
       }
    HIGH_STEP_HEIGHT_FRAMES = 10

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Roll, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.default_roll_speed = self.custom_param.get('default_roll_speed', 10) * NEOX_UNIT_SCALE
        self.first_adjust_speed = self.custom_param.get('first_adjust_speed', 4) * NEOX_UNIT_SCALE
        self.roll_end_speed = self.custom_param.get('roll_end_speed', 2) * NEOX_UNIT_SCALE
        self.roll_duration = self.custom_param.get('roll_duration', 1)
        self.damp_duration = self.custom_param.get('damp_duration', 0.6)
        self.anim_scale = self.custom_param.get('anim_scale', 1)
        self._is_stand_before_roll = True
        self._tick_index = 0
        self._wait_event = None
        self._cur_stage = 0
        self._acc_dest_speed = 0
        self._deacc_speed = 0
        self._end_roll_anim = False
        self._move_dir = math3d.vector(0, 0, 0)
        self._roll_dir = animation_const.ROLL_FRONT
        if self.ev_g_is_avatar():
            self.drag_rush_active = global_data.player.get_setting(ui_operation_const.ROCKER_DASH)
            global_data.emgr.player_enable_rocker_dash += self.on_rocker_dash
        else:
            self.drag_rush_active = False
        return

    def leave_states(self, leave_state, new_state=None):
        if not self.is_active:
            return
        else:
            if leave_state == self.sid:
                if self._wait_event:
                    self.send_event(self._wait_event[0], *self._wait_event[1])
                    self._wait_event = None
                if self._end_roll_anim:
                    is_enter_jump = self.ev_g_check_enter_jump()
                    if is_enter_jump:
                        return
                    if self._is_stand_before_roll:
                        self.send_event('E_CTRL_STAND', ignore_col=True, is_break_run=False)
                    else:
                        self.send_event('E_CTRL_SQUAT', is_break_run=False)
                if self.ev_g_is_avatar():
                    self.send_event('E_ON_ROLL_END')
            self.send_event('E_CTRL_ROLL_END')
            return

    def on_rocker_dash(self, flag):
        self.drag_rush_active = flag

    def _set_wait_event(self, event):
        self._wait_event = event

    def _roll_cd_change(self, skill_id, percent):
        if skill_id == SKILL_ROLL:
            self.send_event('S_ROLL_STAMINA', percent * 100)

    def get_rock_dir(self):
        return character_ctrl_utils.get_human_boost_rock_dir(self)

    def enter(self, leave_states):
        super(Roll, self).enter(leave_states)
        self._end_roll_anim = False
        vertical_speed = self.ev_g_vertical_speed() or 0
        if vertical_speed > 0:
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_RESET_GRAVITY')
        stepheight = state_physic_arg.roll_stepheight1 * NEOX_UNIT_SCALE
        self.send_event('E_STEP_HEIGHT', stepheight)
        self._is_stand_before_roll = not character_action_utils.is_crouch(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt_crs_server', [bcast.E_CTRL_ROLL, ()], False)
        self.send_event('E_RESET_ROTATION', 0)
        self.send_event('E_SET_HAND_IK')
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_ROLL)
        self.send_event('E_ACTION_BEGIN_ROLL')
        self.send_event('E_CLEAR_UP_BODY_ANIM', blend_time=0)
        self.send_event('E_CLEAR_UP_BODY_ANIM', blend_time=0, part=LOWER_UP_BODY)
        rocker_dir = character_ctrl_utils.get_human_boost_rock_dir(self)
        self._rotate_model(rocker_dir)
        self._begin_roll(rocker_dir)
        self.send_event('E_FORBID_ROTATION', True)

    def exit(self, enter_states):
        super(Roll, self).exit(enter_states)
        self.send_event('E_FORBID_ROTATION', False)
        stepheight = state_physic_arg.stepheight * NEOX_UNIT_SCALE
        self.send_event('E_STEP_HEIGHT', stepheight)
        self.sd.ref_logic_trans.yaw_offset = 0

    def _rotate_model(self, rock_dir):
        if not rock_dir:
            return
        if abs(rock_dir.z) < 0.01:
            if rock_dir.x < 0.0:
                self.set_move_dir(animation_const.ROLL_LEFT)
            elif rock_dir.x > 0.0:
                self.set_move_dir(animation_const.ROLL_RIGHT)
            else:
                self.set_move_dir(animation_const.ROLL_FRONT)
            return
        if rock_dir.z < 0.0:
            self.set_move_dir(animation_const.ROLL_BACK)
        else:
            self.set_move_dir(animation_const.ROLL_FRONT)
        yaw = rock_dir.yaw
        if rock_dir.z < 0.0:
            yaw = math.pi + yaw
        else:
            self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')
        self.sd.ref_logic_trans.yaw_offset = yaw

    def _get_cur_speed(self):
        speed = self.default_roll_speed
        cur_speed = self.sd.ref_cur_speed
        if cur_speed:
            if self._cur_stage == 0:
                speed = self.sd.ref_cur_speed - self.first_adjust_speed + self.default_roll_speed
            elif self._cur_stage == 1:
                speed = self.roll_end_speed
            else:
                speed = 6 * NEOX_UNIT_SCALE
        extra_rush_dist_factor = self.ev_g_attr_get('fExtraRushDistFactor', 0.0)
        speed *= 1.0 + extra_rush_dist_factor
        return speed

    def _begin_roll(self, rock_dir):
        cur_pos = self.ev_g_position()
        if not isinstance(cur_pos, math3d.vector):
            return
        self._cur_stage = 0
        self._deacc_speed = 0
        speed = self._get_cur_speed()
        if self.sd.ref_is_agent:
            if not rock_dir or rock_dir.is_zero:
                yaw = self.ev_g_yaw()
                if not yaw:
                    rock_dir = math3d.matrix.make_rotation_y(yaw).forward
                    rock_dir.normalize()
                else:
                    rock_dir = math3d.vector(0, 0, 1)
        self.sd.ref_cur_speed = speed
        self.send_event('E_MOVE', rock_dir)
        self._move_dir = rock_dir
        self._tick_index = 0

    def get_roll_dir(self):
        return self._roll_dir

    def set_move_dir(self, move_dir):
        self._roll_dir = move_dir
        weapon_type_2_action = weapon_action_config.weapon_type_2_action
        weapon_type = self.ev_g_weapon_type()
        action_config = weapon_type_2_action.get(weapon_type, None)
        if not action_config:
            return
        else:
            action_key = 'roll'
            clip_list = action_config[action_key]
            if not clip_list:
                clip_list = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][action_key]
            clip_name = clip_list[animation_const.ROLL_FRONT]
            if move_dir >= 0 and move_dir < len(clip_list):
                clip_name = clip_list[move_dir]
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, timeScale=self.anim_scale)
            return

    def roll(self):
        if self.ev_g_is_attach():
            return
        if not self.check_can_active():
            return
        if self.ev_g_is_avatar():
            self.send_event('E_DO_SKILL', SKILL_ROLL)
        self.active_self()

    def update(self, dt):
        super(Roll, self).update(dt)
        speed = self.sd.ref_cur_speed
        if speed is None:
            return
        else:
            if self._cur_stage == 0:
                if self.elapsed_time >= self.damp_duration:
                    self._cur_stage = 1
                    self._acc_dest_speed = self._get_cur_speed()
                    leave_time = self.roll_duration - self.elapsed_time
                    leave_time = max(leave_time, 0)
                    leave_time = leave_time or 0.1
                    self._deacc_speed = (self._acc_dest_speed - speed) / leave_time
            if self._deacc_speed:
                speed = speed + dt * self._deacc_speed
                self.sd.ref_cur_speed = speed
                self.send_event('E_MOVE', self._move_dir)
            is_end = self.elapsed_time >= self.roll_duration
            self._tick_index += 1
            if self._tick_index >= self.HIGH_STEP_HEIGHT_FRAMES:
                stepheight = state_physic_arg.roll_stepheight2 * NEOX_UNIT_SCALE
                self.send_event('E_STEP_HEIGHT', stepheight)
            if is_end:
                self.disable_self()
                self._end_roll_anim = True
                self.send_event('E_END_ROLL')
            return


class Pick(StateBase):
    BIND_EVENT = {'E_TRY_PICK_UP': '_try_pick_up',
       'E_NOTIFY_MOVE_STATE_CHANGE': '_on_change_move_state',
       'E_CHANGE_GUN_STATE': 'on_change_gun_state',
       'E_CHANGE_ANIM_STATE': 'on_change_aim_state',
       'E_LEAVE_STATE': 'leave_states'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Pick, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.no_anim_state = self.custom_param.get('no_anim_state', ())
        self.no_anim_state = self.ev_g_get_state_value(self.no_anim_state)
        self._pick_position = animation_const.PICK_POSITION_LOW
        self._pick_type = animation_const.PICK_TYPE_NONE
        self._clip_name = ''
        self._anim_duration = 0

    def leave_states(self, leave_state, new_state=None):
        if leave_state == self.sid:
            weapon_type = self.ev_g_weapon_type()

    def enter(self, leave_states):
        import data.pick_clip_config as pick_clip_config
        super(Pick, self).enter(leave_states)
        self.on_pick_anim_param_value_change()
        self._on_change_move_state()
        weapon_type = self.ev_g_weapon_type()

    def exit(self, enter_states):
        super(Pick, self).exit(enter_states)
        subtree = (('biped root', 0), ('biped spine', 1))
        self.send_event('E_CLEAR_UP_BODY_ANIM', subtree)
        if self._pick_type in animation_const.PICK_TYPE_HAVE_GUN_LIST:
            self.send_event('E_RESET_ROTATE_WEAPON')
        self._pick_type = animation_const.PICK_TYPE_NONE
        hand_action = self.ev_g_hand_action()
        if hand_action == animation_const.HAND_STATE_PICK:
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)

    def update(self, dt):
        super(Pick, self).update(dt)
        if self.elapsed_time >= self._anim_duration:
            self.disable_self()

    def update_pick_type(self):
        import data.pick_clip_config as pick_clip_config
        no_transit_state_idx = self.ev_g_no_transit_anim_state()
        move_action = self.ev_g_move_state()
        pick_position = self._pick_position
        is_have_gun = self.ev_g_is_have_gun()
        if pick_position is None or is_have_gun is None:
            return
        else:
            state_pick_type_conf = pick_clip_config.param_2_pick_type_conf.get(no_transit_state_idx, pick_clip_config.param_2_pick_type_conf[animation_const.STATE_STAND])
            move_pick_type_conf = state_pick_type_conf.get(move_action, state_pick_type_conf[animation_const.MOVE_STATE_STAND])
            if not move_pick_type_conf:
                return
            pick_type = move_pick_type_conf[pick_position][is_have_gun]
            self._pick_type = pick_type
            return

    def get_mask_subtree(self, clip_name):
        param_config_list = animation_const.DYNAMIC_MASK_BONE_CLIP.get(clip_name)
        if not param_config_list:
            return (
             animation_const.ENABLE_FULL_BODY_BONE, None)
        else:
            move_action = self.ev_g_move_state()
            subtree = None
            for one_param_config in param_config_list:
                parameters = one_param_config['param']
                if parameters != animation_const.NO_LIMIT_PARAM:
                    for param_name, def_value in six_ex.items(parameters):
                        if isinstance(def_value, int):
                            if def_value == move_action:
                                return (
                                 one_param_config['subtree'], one_param_config['param'])
                        elif move_action in def_value:
                            return (
                             one_param_config['subtree'], one_param_config['param'])

                else:
                    return (
                     one_param_config['subtree'], one_param_config['param'])

            return (
             animation_const.ENABLE_FULL_BODY_BONE, None)

    def _on_change_move_state(self, *args):
        if not self.is_active:
            return
        self.on_pick_anim_param_value_change()
        self.on_change_subtree()

    def on_change_subtree(self):
        if not self._clip_name:
            return
        subtree, params = self.get_mask_subtree(self._clip_name)
        if not subtree:
            return
        self.send_event('E_UPBODY_BONE', subtree)

    def on_change_gun_state(self):
        self.on_pick_anim_param_value_change()

    def on_change_aim_state(self):
        self.on_pick_anim_param_value_change()

    def on_pick_anim_param_value_change(self, *args):
        if not self.is_active:
            return
        else:
            import data.pick_clip_config as pick_clip_config
            old_pick_type = self._pick_type
            self.update_pick_type()
            if old_pick_type == self._pick_type:
                return
            clip_name = pick_clip_config.pick_type_clip_conf.get(self._pick_type, None)
            self._clip_name = clip_name
            if clip_name:
                self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=False, keep_phase=True)
                self._anim_duration = self.ev_g_get_anim_length(self._clip_name)
            else:
                print(('test--[error]--****--_pick_type =', self._pick_type, '--have no clip_name'))
            if self._pick_type in animation_const.PICK_TYPE_HAVE_GUN_LIST:
                self.send_event('E_ROTATE_WEAPON')
            return

    def _set_pick_position(self, pick_position):
        self._pick_position = pick_position

    def _try_pick_up(self, item_position, player_position):
        if not self.check_can_active():
            return
        if self.ev_g_is_in_any_state(self.no_anim_state):
            return
        self.active_self()
        if self.is_active:
            self.send_event('E_ANIM_PHASE', UP_BODY, 0)
            return
        old_pos = math3d.vector(player_position)
        if self.ev_g_is_stand():
            player_position.y += collision_const.CHARACTER_STAND_HEIGHT / 2.0
        dif_y = abs(item_position.y - player_position.y)
        p0 = item_position
        self.send_event('E_CALL_SYNC_METHOD', 'ap_try_pick_up', [(p0.x, p0.y, p0.z), (old_pos.x, old_pos.y, old_pos.z)], True)
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_PICK)
        pick_position = animation_const.PICK_POSITION_LOW
        dif_y = abs(dif_y)
        far_dist = 0.2 * NEOX_UNIT_SCALE
        if item_position.y >= player_position.y or dif_y < far_dist:
            pick_position = animation_const.PICK_POSITION_HIGH
        self._set_pick_position(pick_position)


CLIMB_FROM_GROUND = 0
CLIMB_FROM_IN_AIR = 1
AIR_MAX_HEIGHT = 8
AIR_MAX_Z = 20
AIR_ADJUST_HEIGHT = 1.45

class Climb(StateBase):
    BIND_EVENT = {'E_CLIMB': '_on_climb'
       }
    CLIMB_ANIMATION = {CLIMB_FROM_GROUND: {animation_const.CLIMB_STATE_CLIMB_UP: 'vaulting_start',animation_const.CLIMB_STATE_STAND_BARRIER: 'vaulting_up'},CLIMB_FROM_IN_AIR: {animation_const.CLIMB_STATE_CLIMB_UP: 'climbing_foward_start',animation_const.CLIMB_STATE_STAND_BARRIER: 'climbing_foward_up'}}
    AIR_TRACK_TEST = [
     (
      0.0, (0, 0, 0)), (0.1, (0, AIR_MAX_HEIGHT + AIR_ADJUST_HEIGHT, 0)), (0.343, (0, AIR_MAX_HEIGHT + AIR_ADJUST_HEIGHT, AIR_MAX_Z * 0.8)), (0.4, (0, AIR_MAX_HEIGHT, AIR_MAX_Z))]

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Climb, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._climb_state = animation_const.CLIMB_STATE_NONE
        self._clim_anim1_duration = 0
        self._stand_barrier_duration = 0
        self._climb_from_type = CLIMB_FROM_GROUND
        self._climb_type = 0
        self._climb_pos = math3d.vector(0, 0, 0)
        from logic.gutils.track_reader import TrackReader
        self._track_reader = TrackReader()
        self._init_foot_position = math3d.vector(0, 0, 0)

    def destroy(self):
        super(Climb, self).destroy()

    def _on_climb(self, *args):
        if not self.check_can_active():
            return
        self._climb_type = args[0]
        self._climb_pos = args[1]
        if self._climb_type <= g_const.CLIMB_TO_DROP:
            self._climb_from_type = CLIMB_FROM_IN_AIR
            self._climb_pos.y = self._climb_pos.y
        else:
            self._climb_from_type = CLIMB_FROM_GROUND
        self._init_foot_position = self.ev_g_foot_position()
        self.send_event('E_CLEAR_SPEED')
        self.active_self()

    def enter(self, leave_states):
        if self._climb_from_type == CLIMB_FROM_IN_AIR:
            self.auto_delay_camera = True
            self.delay_camera_param = self.custom_param.get('clime_from_in_air_camera_param')
        else:
            self.auto_delay_camera = False
            self.delay_camera_param = {}
        super(Climb, self).enter(leave_states)
        self.send_event('E_ENABLE_TEST_POS', False)
        self.send_event('E_FORBID_ROTATION', True)
        if self._climb_from_type == CLIMB_FROM_IN_AIR:
            self.change_camera_follow_speed(True, 0.01, last_time=0.1)
        cur_pos = self._init_foot_position
        yaw = self.ev_g_yaw()
        time_scale = 7.3
        track_test = None
        if self._climb_from_type == CLIMB_FROM_IN_AIR:
            track_test = self.AIR_TRACK_TEST
        self._track_reader.read_track('test', yaw, cur_pos, self._climb_pos, track_test)
        if self._climb_from_type == CLIMB_FROM_GROUND and not (self._climb_type == g_const.CLIMB_TO_TOP_STAND or self._climb_type == g_const.THROW_OVER_TO_TOP_STAND):
            width = collision_const.CHARACTER_CLIMB_WIDTH
            height = collision_const.CHARACTER_CLIMB_HEIGHT
            self.send_event('E_RESIZE_DRIVER_CHARACTER', width, height, collision_const.ALIGN_TYPE_DOWN)
        clim_up_duration = self._track_reader.get_track_time()
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_CLIMB)
        self._set_climb_state(animation_const.CLIMB_STATE_CLIMB_UP)
        clip_name = self.get_climb_anim()
        actual_anim_time = clim_up_duration or 0.1
        anim_time = self.ev_g_get_anim_length(clip_name)
        self._clim_anim1_duration = anim_time
        self.send_event('E_SET_SMOOTH_DURATION', LOW_BODY_SELECT, 0)
        self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, loop=False, timeScale=global_data.clime_scale1, blend_time=0.05)
        return

    def exit(self, enter_states):
        self.auto_delay_camera = False
        self.delay_camera_param = {}
        super(Climb, self).exit(enter_states)
        self.send_event('E_ENABLE_TEST_POS', True)
        self.send_event('E_FORBID_ROTATION', False)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            self.send_event('E_ACTIVE_STATE', self.status_config.MC_MOVE)
        else:
            self.send_event('E_MOVE', math3d.vector(0, 0, 0))
            self.send_event('E_CTRL_STAND', is_break_run=False)
            self.sd.ref_cur_speed = 0

    def get_climb_anim(self):
        clip_name = self.CLIMB_ANIMATION.get(self._climb_from_type, self.CLIMB_ANIMATION[CLIMB_FROM_GROUND])[self._climb_state]
        is_have_gun = self.ev_g_is_have_gun()
        if is_have_gun:
            clip_name = clip_name + '_gun'
        return clip_name

    def update(self, dt):
        delay_time = global_data.clime_delay_time
        last_elapsed_time = self.elapsed_time - delay_time
        super(Climb, self).update(dt)
        elapsed_time = self.elapsed_time - delay_time
        if elapsed_time < 0:
            return
        is_end = False
        clim_up_duration = self._track_reader.get_track_time()
        pass_time = elapsed_time - clim_up_duration
        if last_elapsed_time < clim_up_duration:
            pos, is_end = self._track_reader.get_cur_pos(elapsed_time)
            self.send_event('E_FOOT_POSITION', pos)
        elif elapsed_time > clim_up_duration:
            if self._climb_from_type == CLIMB_FROM_GROUND and not (self._climb_type == g_const.CLIMB_TO_TOP_STAND or self._climb_type == g_const.THROW_OVER_TO_TOP_STAND):
                if pass_time <= 1:
                    self._climb_move_tick()
            else:
                self.disable_self()
        if last_elapsed_time < self._clim_anim1_duration and elapsed_time >= self._clim_anim1_duration:
            self._set_climb_state(animation_const.CLIMB_STATE_STAND_BARRIER)
            clip_name = self.get_climb_anim()
            self._stand_barrier_duration = self._clim_anim1_duration + self.ev_g_get_anim_length(clip_name) - clim_up_duration
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, loop=False, timeScale=global_data.clime_scale2)
        last_pass_time = last_elapsed_time - clim_up_duration
        if pass_time > 0:
            if last_pass_time < self._stand_barrier_duration and pass_time >= self._stand_barrier_duration:
                self.disable_self()

    def _climb_move_tick(self):
        self.sd.ref_cur_speed = speed_physic_arg.climb_move
        self.send_event('E_MOVE', math3d.vector(0, 0, 1))
        player_pos = self.ev_g_position()
        if not player_pos:
            return
        if (self._climb_pos - player_pos).length_sqr > g_const.LEAVE_CLIMB_POINT_DISTANCE ** 2:
            if self._climb_from_type == CLIMB_FROM_GROUND:
                width = collision_const.CHARACTER_STAND_WIDTH
                height = collision_const.CHARACTER_STAND_HEIGHT
                self.send_event('E_RESIZE_DRIVER_CHARACTER', width, height, collision_const.ALIGN_TYPE_DOWN)
                self.try_move_out_col()
            self.disable_self()

    def disable_self(self):
        super(Climb, self).disable_self()

    def _set_climb_state(self, climb_state):
        self._climb_state = climb_state

    def try_move_out_col(self):
        physical_position = self.ev_g_phy_position()
        if not physical_position:
            return
        offset = collision_const.CHARACTER_STAND_HEIGHT * 0.5 + collision_const.CHARACTER_STAND_WIDTH - (collision_const.CHARACTER_CLIMB_HEIGHT * 0.5 + collision_const.CHARACTER_CLIMB_WIDTH)
        physical_position.y = physical_position.y + 0.1 * NEOX_UNIT_SCALE + offset
        is_hit = self.ev_g_static_test(position=physical_position, ignore_col_id_list=True)
        if is_hit:
            forward_dir = self.ev_g_model_forward()
            offset = 0.02 * NEOX_UNIT_SCALE
            direction = forward_dir * offset
            col_result = self.ev_g_sweep_test(direction)
            is_hit_forward = col_result[0]
            if is_hit_forward:
                direction = -direction
                col_result = self.ev_g_sweep_test(direction)
                is_hit_backward = col_result[0]
                if is_hit_backward:
                    up_dir = self.ev_g_model_up()
                    direction = up_dir * (offset + self.ev_g_character_total_height())
                    col_result = self.ev_g_sweep_test(direction, self.ev_g_foot_position())
                    is_hit_up = col_result[0]
                    if is_hit_up:
                        self.send_event('E_FOOT_POSITION', self._init_foot_position)


@editor.state_exporter({('swim_run', 'meter'): {'zh_name': '\xe6\xb8\xb8\xe6\xb3\xb3\xe8\xb7\x91\xe6\xad\xa5\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100}})
class Swim(StateBase):
    BIND_EVENT = {'E_CHARACTER_ATTR': '_change_character_attr',
       'E_CHANGE_WATER_INFO': '_change_water_info',
       'E_CHANGE_WATER_LIMIT': 'on_change_water_limit',
       'E_PLAY_WATER_EFFECT_BY_AIM_TYPE': '_play_water_effect_by_anim_type',
       'E_PLAY_WATER_EFFECT_BY_PATH': '_play_water_effect_by_path',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_FOOT_ON_WATER': '_foot_on_water_event',
       'E_POSITION': 'update_player_pos',
       'E_CLEAR_SWIM_EFFECT': '_clear_swim_loop_effect',
       'E_CHANGE_ANIM_MOVE_DIR': 'change_anim_move_dir',
       'E_START_SWIM': 'start_swim',
       'E_STOP_SWIM': 'stop_swim',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': 'leave_states',
       'E_ANIM_MGR_INIT': 'on_anim_mgr_init'
       }
    AIM_TYPE = enum(('ANIM_TYPE_IDLE', 'ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_LEFT', 'ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_RIGHT',
                     'ANIM_TYPE_WALK_ON_DEEP_SPRAY_LEFT', 'ANIM_TYPE_WALK_ON_DEEP_SPRAY_RIGHT',
                     'ANIM_TYPE_SWIM_BACK_SPRAY_FRONT', 'ANIM_TYPE_SWIM_BACK_SPRAY_BACK',
                     'ANIM_TYPE_SWIM_LEFT_FRONT_HAND', 'ANIM_TYPE_SWIM_RIGHT_FRONT_HAND',
                     'ANIM_TYPE_SWIM_LEFT_BACK_HAND', 'ANIM_TYPE_SWIM_RIGHT_BACK_HAND'), 1)
    WALK_ON_WATER_ANIM_TYPE = (
     AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_LEFT, AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_RIGHT,
     AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_LEFT, AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_RIGHT)
    SWIM_EVENT_CONFIG = {animation_const.SWIM_EVENT_IDLE: ({'anim_type': AIM_TYPE.ANIM_TYPE_IDLE,'trigger': ('swim_1', 'swim_2')},),animation_const.SWIM_EVENT_MOVE_FRONT: ({'anim_type': AIM_TYPE.ANIM_TYPE_SWIM_LEFT_FRONT_HAND,'trigger': ('swim_f1', )}, {'anim_type': AIM_TYPE.ANIM_TYPE_SWIM_RIGHT_FRONT_HAND,'trigger': ('swim_f2', )}, {'anim_type': AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_FRONT,'trigger': ('swim_f3', )}),animation_const.SWIM_EVENT_MOVE_BACK: ({'anim_type': AIM_TYPE.ANIM_TYPE_SWIM_LEFT_BACK_HAND,'trigger': ('swim_b1', )}, {'anim_type': AIM_TYPE.ANIM_TYPE_SWIM_RIGHT_BACK_HAND,'trigger': ('swim_b2', )}, {'anim_type': AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_BACK,'trigger': ('swim_b3', )})}
    MAX_EFFECT_TIME = 1.5
    GROUND_SHE_SHUI_MAX_HEIGHT = 0.6 * NEOX_UNIT_SCALE
    SHE_SHUI_HAND_EFFECT_PATH = 'effect/fx/water/sheshui_hand.sfx'
    SHALLOW_SPRAY_EFFECT_PATH = 'effect/fx/water/sheshui.sfx'
    DEEP_SPRAY_EFFECT_PATH = 'effect/fx/water/sheshui_shen.sfx'
    LOWER_WATER_DIFF_HEIGHT = 2 * NEOX_UNIT_SCALE
    LOWER_SWIM_DIFF_HEIGHT = 9
    ANIM_TYPE_2_EFFECT_CONFIG = {AIM_TYPE.ANIM_TYPE_IDLE: {'effect': {'res_path': 'effect/fx/water/piaofu.sfx',
                                            'loop': True,
                                            'exclude_anim_type': (
                                                                AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_FRONT, AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_BACK)
                                            }
                                 },
       AIM_TYPE.ANIM_TYPE_SWIM_LEFT_FRONT_HAND: {'effect': {'res_path': SHE_SHUI_HAND_EFFECT_PATH,
                                                            'bind_point': 'fx_water_zuo',
                                                            'is_moment_pos': True,
                                                            'life_time': MAX_EFFECT_TIME
                                                            }
                                                 },
       AIM_TYPE.ANIM_TYPE_SWIM_RIGHT_FRONT_HAND: {'effect': {'res_path': SHE_SHUI_HAND_EFFECT_PATH,
                                                             'bind_point': 'fx_water_you',
                                                             'is_moment_pos': True,
                                                             'life_time': MAX_EFFECT_TIME
                                                             }
                                                  },
       AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_FRONT: {'effect': {'res_path': 'effect/fx/water/youyong.sfx',
                                                             'bind_point': 'fx_water_tuowei',
                                                             'bind_type': world.BIND_TYPE_ALL,
                                                             'loop': True,
                                                             'exclude_anim_type': (
                                                                                 AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_BACK,)
                                                             }
                                                  },
       AIM_TYPE.ANIM_TYPE_SWIM_LEFT_BACK_HAND: {'effect': {'res_path': SHE_SHUI_HAND_EFFECT_PATH,
                                                           'bind_point': 'fx_water_yangyong_zuo',
                                                           'is_moment_pos': True,
                                                           'life_time': MAX_EFFECT_TIME
                                                           }
                                                },
       AIM_TYPE.ANIM_TYPE_SWIM_RIGHT_BACK_HAND: {'effect': {'res_path': SHE_SHUI_HAND_EFFECT_PATH,
                                                            'bind_point': 'fx_water_yangyong_you',
                                                            'is_moment_pos': True,
                                                            'life_time': MAX_EFFECT_TIME
                                                            }
                                                 },
       AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_BACK: {'effect': {'res_path': 'effect/fx/water/youyong_back.sfx',
                                                            'bind_point': 'fx_water_yangyong_tuowei',
                                                            'bind_type': world.BIND_TYPE_ALL,
                                                            'loop': True,
                                                            'exclude_anim_type': (
                                                                                AIM_TYPE.ANIM_TYPE_SWIM_BACK_SPRAY_FRONT,)
                                                            }
                                                 },
       AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_LEFT: {'effect': {'res_path': SHALLOW_SPRAY_EFFECT_PATH,
                                                                  'is_moment_pos': True,
                                                                  'bind_point': 'foot_spray_left'
                                                                  }
                                                       },
       AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_RIGHT: {'effect': {'res_path': SHALLOW_SPRAY_EFFECT_PATH,
                                                                   'is_moment_pos': True,
                                                                   'bind_point': 'foot_spray_right'
                                                                   }
                                                        },
       AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_LEFT: {'effect': {'res_path': DEEP_SPRAY_EFFECT_PATH,
                                                               'loop': True,
                                                               'is_moment_pos': True,
                                                               'bind_point': 'foot_spray_left'
                                                               }
                                                    },
       AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_RIGHT: {'effect': {'res_path': DEEP_SPRAY_EFFECT_PATH,
                                                                'loop': True,
                                                                'is_moment_pos': True,
                                                                'bind_point': 'foot_spray_right'
                                                                }
                                                     }
       }
    CLIP_DICT = {animation_const.SWIM_ACTION_IDLE: {'clip_name': 'swim_idle','loop': True,'dir_type': 1},animation_const.SWIM_ACTION_DIRECT_FRONT: {'clip_name': 'swim_f','loop': True},animation_const.SWIM_ACTION_BACK_2_FRONT: {'clip_name': 'swim_b_transmit_f','loop': False},animation_const.SWIM_ACTION_STAND_2_FRONT: {'clip_name': 's_transmit_swim_f','loop': False},animation_const.SWIM_ACTION_DIRECT_BACK: {'clip_name': 'swim_b','loop': True},animation_const.SWIM_ACTION_FRONT_2_BACK: {'clip_name': 'swim_f_transmit_b','loop': False},animation_const.SWIM_ACTION_STAND_2_BACK: {'clip_name': 's_transmit_swim_b','loop': False},animation_const.SWIM_ACTION_HORIZON: {'clip_name': 'swim_f','loop': True}}
    TRANSIT_ACTION = [
     animation_const.SWIM_ACTION_BACK_2_FRONT, animation_const.SWIM_ACTION_STAND_2_FRONT, animation_const.SWIM_ACTION_FRONT_2_BACK, animation_const.SWIM_ACTION_STAND_2_BACK]

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Swim, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._water_height = 0
        self._loop_effect = {}
        self._swim_action = -1
        self._dir_y = 0
        self._transit_duration = 0
        self.cur_speed = 0
        self.swim_run = self.custom_param.get('swim_run', 4) * NEOX_UNIT_SCALE
        self._is_float_up = False
        self._is_float_down = False
        self.is_swimming = False
        self._float_speed = speed_physic_arg.swim_vertical_speed

    def refresh_param_changed(self):
        self.swim_run = self.custom_param.get('swim_run', 4) * NEOX_UNIT_SCALE

    def _change_character_attr(self, name, *arg):
        if name == 'water_info' or name == 'animator_info':
            current_posture_state = self.ev_g_anim_state()
            loop_effect = {}
            for anim_type, item in six.iteritems(self._loop_effect):
                sfx = item[1]
                if sfx and sfx.valid:
                    loop_effect[anim_type] = (
                     sfx.filename, sfx)

            if loop_effect:
                print(('test--ComSwim.animator_info--step2--loop_effect =', loop_effect))

    def on_anim_mgr_init(self):
        anim_state = self.ev_g_attr_get('human_state')
        if anim_state == animation_const.STATE_SWIM or self.ev_g_get_state(self.sid):
            if self.ev_g_is_avatar():
                self.active_self()

    def on_load_animator_complete(self, *args):
        self._register_swim_event()

    def enter_states(self, new_state):
        if new_state == self.status_config.ST_STAND or new_state == self.status_config.ST_CROUCH:
            self._clear_swim_loop_effect()

    def _register_swim_event(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        else:
            model = self.ev_g_model()
            if not model:
                return
            role_id = self.ev_g_role_id()
            for clip_name_list, event_type in animation_const.SWIM_EVENT_LIST:
                for clip_name in clip_name_list:
                    if role_id in animation_const.SWIM_USE_MILA_ANI_IDS:
                        new_clip_name = clip_name + '_' + str(animation_const.ROLE_ID_MI_LA)
                        if model.has_anim(new_clip_name):
                            clip_name = new_clip_name
                    one_type_swim_config = self.SWIM_EVENT_CONFIG.get(event_type, '')
                    for one_swim_config in one_type_swim_config:
                        triggers = one_swim_config['trigger']
                        for trigger_name in triggers:
                            callback = self._swim_in_water_event
                            if one_swim_config.get('callback', None):
                                callback = getattr(self, one_swim_config['callback'], None)
                            data = one_swim_config['anim_type']
                            if len(clip_name_list) > 1:
                                animator.add_trigger_clip(clip_name, trigger_name, callback, data)
                            else:
                                self.send_event('E_REGISTER_ANIM_KEY_EVENT', clip_name, trigger_name, callback, data)

            return

    def get_swim_clip(self, swim_action):
        clip_name = self.CLIP_DICT.get(swim_action, {}).get('clip_name', 'swim_idle')
        model = self.ev_g_model()
        if not model:
            return clip_name
        role_id = self.ev_g_role_id()
        if role_id in animation_const.SWIM_USE_MILA_ANI_IDS:
            new_clip_name = clip_name + '_' + str(animation_const.ROLE_ID_MI_LA)
            if model.has_anim(new_clip_name):
                clip_name = new_clip_name
        return clip_name

    def _show_swim_ui_list(self, ui_list, flag):
        if not self.ev_g_is_avatar():
            return
        if not flag:
            for ui in ui_list:
                ui = global_data.ui_mgr.get_ui(ui)
                if ui:
                    ui.add_hide_count('swim')

        else:
            for ui in ui_list:
                ui = global_data.ui_mgr.get_ui(ui)
                if ui:
                    ui.add_show_count('swim')

    def float_up_in_water_tick(self, *args):
        if not self._is_float_up:
            return
        phy_pos = self.ev_g_phy_position()
        if not phy_pos:
            return
        limit_lower_height = self._water_height - self.LOWER_SWIM_DIFF_HEIGHT
        vertical_speed = self.ev_g_vertical_speed()
        if vertical_speed != self._float_speed:
            self.send_event('E_VERTICAL_SPEED', self._float_speed)
        if phy_pos.y >= limit_lower_height:
            self._is_float_up = False
            self.on_change_water_limit()
            self.send_event('E_VERTICAL_SPEED', 0)

    def float_down_in_water_tick(self, *args):
        if not self._is_float_down:
            return
        phy_pos = self.ev_g_phy_position()
        if not phy_pos:
            return
        limit_lower_height = self._water_height - self.LOWER_SWIM_DIFF_HEIGHT
        vertical_speed = self.ev_g_vertical_speed()
        if vertical_speed != -self._float_speed:
            self.send_event('E_VERTICAL_SPEED', -self._float_speed)
        if phy_pos.y <= limit_lower_height:
            self._is_float_down = False
            self.on_change_water_limit()
            self.send_event('E_VERTICAL_SPEED', 0)

    def start_swim(self, *args):
        if not self.check_can_active() and not self.ev_g_get_state(self.sid) and not self.ev_g_get_state(self.status_config.ST_FROZEN):
            return
        self.is_swimming = True
        self._water_height = args[0] or 0
        self.ev_g_status_try_trans(self.sid, sync=True)
        self.on_change_water_limit()

    def stop_swim(self, *args):
        if not self.ev_g_get_state(self.sid):
            return
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CTRL_STOP_SWIM, ()], False)
        self.disable_self()
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_UNLIMIT_HEIGHT')
        self.send_event('E_UNLIMIT_LOWER_HEIGHT')
        self.is_swimming = False

    def swim(self):
        self._swim_action = -1
        current_posture_state = self.ev_g_anim_state()
        if current_posture_state != animation_const.STATE_SWIM:
            rocker_dir = self.sd.ref_rocker_dir
            if not rocker_dir or rocker_dir.is_zero:
                self.set_swim_action(animation_const.SWIM_ACTION_IDLE)
            else:
                dir_y = 0
                if rocker_dir:
                    dir_y = rocker_dir.z
                if dir_y > 0:
                    self.set_swim_action(animation_const.SWIM_ACTION_STAND_2_FRONT)
                elif dir_y < 0:
                    self.set_swim_action(animation_const.SWIM_ACTION_STAND_2_BACK)
                else:
                    self.set_swim_action(animation_const.SWIM_ACTION_IDLE)
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_SWIM)
        self.send_event('E_SWIM')

    def update_player_pos(self, pos):
        model = self.ev_g_model()
        if not model:
            return
        else:
            left_exist_sfx_item = self._loop_effect.get(self.AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_LEFT, None)
            right_exist_sfx_item = self._loop_effect.get(self.AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_RIGHT, None)
            if not (left_exist_sfx_item or right_exist_sfx_item):
                return
            position = model.world_position
            position = math3d.vector(position.x, self._water_height, position.z)
            items = (left_exist_sfx_item, right_exist_sfx_item)
            for item in items:
                if item and item[1]:
                    item[1].world_position = position

            return

    def get_swim_action(self):
        return self._swim_action

    def set_swim_action(self, swim_action):
        if self._swim_action == swim_action:
            return
        else:
            if self._swim_action == animation_const.SWIM_ACTION_IDLE or swim_action == animation_const.SWIM_ACTION_IDLE:
                self._clear_swim_loop_effect()
            self._swim_action = swim_action
            clip_config = self.CLIP_DICT.get(swim_action, self.CLIP_DICT[animation_const.SWIM_ACTION_IDLE])
            dir_type = clip_config.get('dir_type', 4)
            loop = clip_config.get('loop', False)
            clip_name = self.get_swim_clip(swim_action)
            yaw_list = None
            if dir_type > 1:
                if swim_action == animation_const.SWIM_ACTION_DIRECT_BACK:
                    yaw_list = [
                     1.57, -1.57, 0, 0]
                else:
                    yaw_list = [
                     -1.57, 1.57, 0, 0]
            blend_time = 0.2
            if self._swim_action == animation_const.SWIM_ACTION_IDLE:
                blend_time = 0.5
            self.send_event('E_SET_SMOOTH_DURATION', LOW_BODY_SELECT, blend_time)
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=loop, yaw_list=yaw_list, ignore_sufix=True)
            self._transit_duration = 0
            if swim_action in self.TRANSIT_ACTION:
                self._transit_duration = self.ev_g_get_anim_length(clip_name)
            else:
                self._transit_duration = 0
            return

    def leave_states(self, leave_state, new_state=None):
        if leave_state == self.sid:
            self.send_event('E_UNLIMIT_HEIGHT')
            self.send_event('E_UNLIMIT_LOWER_HEIGHT')
            self._clear_swim_loop_effect()
            self.is_swimming = False

    def enter(self, leave_states):
        super(Swim, self).enter(leave_states)
        self.send_event('E_LEAVE_SKATE_INTERACTION_ZONE')
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_CTRL_SWIM')
        self.swim()
        phy_pos = self.ev_g_phy_position()
        if not phy_pos:
            print('test--Swim.enter--phy_pos =', phy_pos)
            import traceback
            traceback.print_stack()
            return
        self._is_float_up = False
        self._is_float_down = False
        self.check_float()
        self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_SET_MAX_SLOPE', 90)
        self.cur_speed = move_utils.get_human_speed(self)
        self._show_swim_ui_list(['FireRockerUI', 'PostureControlUI', 'ThrowRockerUI', 'BulletReloadUI'], False)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.update_player_pos, 0.1)

    def check_float(self):
        phy_pos = self.ev_g_phy_position()
        if not phy_pos:
            return
        limit_lower_height = self._water_height - self.LOWER_SWIM_DIFF_HEIGHT
        if phy_pos.y > limit_lower_height or self.ev_g_get_state(self.status_config.ST_FROZEN):
            self._is_float_down = True
        elif phy_pos.y == limit_lower_height:
            self._is_float_down = False
            self._is_float_up = False
        else:
            self._is_float_up = True

    def exit(self, enter_states):
        super(Swim, self).exit(enter_states)
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.update_player_pos)
        self.send_event('E_SET_MAX_SLOPE', state_physic_arg.max_slope)
        self._clear_swim_loop_effect()
        self.sd.ref_cur_speed = 0
        self.send_event('E_MOVE', math3d.vector(0, 0, 0))
        self.send_event('E_CTRL_STAND', is_break_run=False)
        self._show_swim_ui_list(['FireRockerUI', 'PostureControlUI', 'ThrowRockerUI', 'BulletReloadUI'], True)
        self._swim_action = -1
        self._is_float_up = False
        self._is_float_down = False
        self.is_swimming = False

    def dir_360_to_dir_3(self, dir_360):
        move_vertical_dir = 0
        if abs(dir_360) < 0.001:
            move_vertical_dir = 0
        elif dir_360 > 0.0:
            move_vertical_dir = 1
        else:
            move_vertical_dir = -1
        return move_vertical_dir

    def change_anim_move_dir(self, dir_x, dir_y, *args):
        if not self.is_active:
            return
        physical_position = self.ev_g_phy_position()
        low_height = self.ev_g_limit_lower_height()
        if physical_position and physical_position.y - low_height > 2:
            is_hit = self.ev_g_static_test(position=physical_position)
            if not is_hit:
                self.send_event('E_TELEPORT', physical_position)
        move_vertical_dir = self.dir_360_to_dir_3(dir_y)
        old_move_vertical_dir = self.dir_360_to_dir_3(self._dir_y)
        move_horizon_dir = self.dir_360_to_dir_3(dir_x)
        if old_move_vertical_dir == 0:
            if move_vertical_dir > 0:
                self.set_swim_action(animation_const.SWIM_ACTION_DIRECT_FRONT)
            elif move_vertical_dir < 0:
                self.set_swim_action(animation_const.SWIM_ACTION_DIRECT_BACK)
        elif move_vertical_dir != 0:
            if old_move_vertical_dir != move_vertical_dir:
                if move_vertical_dir > 0:
                    self.set_swim_action(animation_const.SWIM_ACTION_BACK_2_FRONT)
                else:
                    self.set_swim_action(animation_const.SWIM_ACTION_FRONT_2_BACK)
        if move_vertical_dir == 0:
            if move_horizon_dir == 0:
                self.set_swim_action(animation_const.SWIM_ACTION_IDLE)
            else:
                self.set_swim_action(animation_const.SWIM_ACTION_HORIZON)

    def update(self, dt):
        last_elapsed_time = self.elapsed_time
        super(Swim, self).update(dt)
        self.check_float()
        self.float_up_in_water_tick()
        self.float_down_in_water_tick()
        if self._transit_duration > 0 and last_elapsed_time < self._transit_duration and self.elapsed_time >= self._transit_duration:
            if self._swim_action == animation_const.SWIM_ACTION_BACK_2_FRONT or self._swim_action == animation_const.SWIM_ACTION_STAND_2_FRONT:
                self.set_swim_action(animation_const.SWIM_ACTION_DIRECT_FRONT)
            elif self._swim_action == animation_const.SWIM_ACTION_FRONT_2_BACK or self._swim_action == animation_const.SWIM_ACTION_STAND_2_BACK:
                self.set_swim_action(animation_const.SWIM_ACTION_DIRECT_BACK)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            self.sd.ref_cur_speed = self.cur_speed
            self.send_event('E_MOVE', rocker_dir)
        else:
            self.sd.ref_cur_speed = 0
            self.send_event('E_MOVE', math3d.vector(0, 0, 0))

    def _change_water_info(self, water_height, water_status):
        self._water_height = water_height or 0
        if water_status == water_const.WATER_NONE or water_status == water_const.WATER_DEEP_LEVEL:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CHANGE_WATER_INFO, (water_height, water_status)], False)
            self._clear_swim_loop_effect()

    def on_change_water_limit(self):
        if not self.is_swimming:
            return
        limit_lower_height = self._water_height - self.LOWER_SWIM_DIFF_HEIGHT
        self.send_event('E_LIMIT_HEIGHT', self._water_height)
        self.send_event('E_LIMIT_LOWER_HEIGHT', limit_lower_height)

    def _clear_swim_loop_effect(self, *args):
        if not self._loop_effect:
            return
        for _, sfx_item in six.iteritems(self._loop_effect):
            if sfx_item:
                global_data.sfx_mgr.remove_sfx(sfx_item[1])

        self._loop_effect = {}

    def del_loop_effect_item(self, anim_type):
        sfx_item = self._loop_effect.get(anim_type, None)
        if sfx_item:
            self._loop_effect.pop(anim_type)
            global_data.sfx_mgr.remove_sfx(sfx_item[1])
        return

    def create_effect_cb(self, sfx, data):
        res_path, anim_type, loop = data
        sfx_loop = sfx.loop or sfx.is_end_less_play()
        water_status = self.sd.ref_water_status
        if water_status == water_const.WATER_NONE:
            global_data.sfx_mgr.remove_sfx(sfx)
            return
        else:
            if anim_type in self.WALK_ON_WATER_ANIM_TYPE:
                move_action = self.ev_g_move_state()
                if move_action not in (animation_const.MOVE_STATE_WALK, animation_const.MOVE_STATE_RUN):
                    global_data.sfx_mgr.remove_sfx(sfx)
                    return
            if loop:
                sfx_item = self._loop_effect.get(anim_type, None)
                if sfx_item:
                    if sfx_item[1]:
                        global_data.sfx_mgr.remove_sfx(sfx_item[1])
                    sfx_item[1] = sfx
                else:
                    self._loop_effect[anim_type] = [
                     None, sfx]
            return

    def _play_water_effect_by_anim_type(self, anim_type):
        if not self.ev_g_get_state(self.sid):
            return
        else:
            effect_config = self.ANIM_TYPE_2_EFFECT_CONFIG.get(anim_type)
            if not effect_config:
                return
            res_paracm_config = effect_config['effect']
            res_path = res_paracm_config.get('res_path', '')
            bind_point = res_paracm_config.get('bind_point', '')
            loop = res_paracm_config.get('loop', False)
            is_moment_pos = res_paracm_config.get('is_moment_pos', False)
            life_time = res_paracm_config.get('life_time', 0)
            bind_type = res_paracm_config.get('bind_type', None)
            exclude_anim_type = res_paracm_config.get('exclude_anim_type', None)
            if exclude_anim_type:
                for one_exclude_anim_type in exclude_anim_type:
                    self.del_loop_effect_item(one_exclude_anim_type)

            if loop:
                life_time = -1
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_WATER_EFFECT_BY_AIM_TYPE, (anim_type,)], False)
            model = self.ev_g_model()
            if not model:
                return
            sfx_item = self._loop_effect.get(anim_type, None)
            if sfx_item:
                if sfx_item[1] and not bind_point:
                    position = model.world_position
                    position.y = self._water_height
                    sfx_item[1].world_position = position
                return
            if bind_point:
                socket_matrix = model.get_socket_matrix(bind_point, world.SPACE_TYPE_WORLD)
                position = None
                if is_moment_pos and socket_matrix:
                    position = socket_matrix.translation
                    position.y = self._water_height
                    bind_point = ''
            else:
                position = model.world_position
                position.y = self._water_height
            on_create_func = Functor(self.create_effect_cb, data=(res_path, anim_type, loop))
            if bind_point:
                global_data.sfx_mgr.create_sfx_on_model(res_path, self.ev_g_model(), bind_point, duration=life_time, on_create_func=on_create_func)
            else:
                global_data.sfx_mgr.create_sfx_in_scene(res_path, position, duration=life_time, on_create_func=on_create_func)
            return

    def _play_water_effect_by_path(self, res_path):
        model = self.ev_g_model()
        if not model:
            return
        else:
            position = model.world_position
            if not position:
                return
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_WATER_EFFECT_BY_PATH, (res_path,)], False)
            position.y = self._water_height
            on_create_func = Functor(self.create_effect_cb, data=(res_path, None, False))
            global_data.sfx_mgr.create_sfx_in_scene(res_path, position, on_create_func=on_create_func)
            return

    def _foot_on_water_event(self, model, anim_name, key, data=None):
        if key == 'step1':
            data = self.AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_LEFT
        else:
            data = self.AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_RIGHT
        water_height = self.ev_g_water_diff_height()
        if water_height > self.GROUND_SHE_SHUI_MAX_HEIGHT:
            if data == self.AIM_TYPE.ANIM_TYPE_WALK_ON_SHALLOW_SPRAY_LEFT:
                data = self.AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_LEFT
            else:
                data = self.AIM_TYPE.ANIM_TYPE_WALK_ON_DEEP_SPRAY_RIGHT
        self._swim_in_water_event(model, anim_name, key, data)

    def _swim_in_water_event(self, model, anim_name, key, data=None):
        if not self.ev_g_get_state(self.sid):
            return
        anim_type = data
        self._play_water_effect_by_anim_type(anim_type)
        if anim_type != self.AIM_TYPE.ANIM_TYPE_IDLE:
            self.send_event('E_PLAY_FOOTSTEP_SOUND', animation_const.SOUND_TYPE_SWIM)


class Parachute(StateBase):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_CHANGE_ANIM_MOVE_DIR': '_change_anim_move_dir',
       'E_CTRL_SWIM': '_on_swim',
       'E_CTRL_STAND': '_on_stand',
       'E_LAND': '_on_land',
       'E_START_PARACHUTE': '_start_parachute_stage',
       'E_PARACHUTE_MOVE': '_move_toward',
       'E_REMOVE_PARACHUTE': 'parachute_land',
       'E_DO_REMOVE_PARACHUTE': '_remove_parachute',
       'E_PARACHUTE_MOVE_STOP': '_move_stop',
       'E_EQUIP_PARACHUTE': '_equip_parachute',
       'G_PARACHUTE_ANIMATOR': 'get_parachute_animator',
       'G_PARACHUTE_MODEL': 'get_parachute_model',
       'E_NOTIFY_MOVE_STATE_CHANGE': '_on_change_move_state'
       }
    DEFAULT_XML = 'animator_conf/parachute.xml'
    DELAY_CLEAR_TIME = 0.93
    SOFTBONE_SOCKET_CONF = {'mx_qiqiu': 'soft_bone_param_mx_qiqiu'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Parachute, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._parachute = None
        self._parachute_animator = None
        self.load_model_callback = None
        self.move_vector = math3d.vector(0, 0, 0)
        self._parachute_state = animation_const.PARACHUTE_STATE_CLOSE
        self._remove_parachute_timer_id = None
        self._delay_remove_parachute_timer_id = None
        self._anim_duration = 0
        self._dir_x = 0
        self._dir_y = 0
        self.is_avatar = False
        self.opening_anim = self.custom_param.get('opening_anim', None)
        self.ground_anim = self.custom_param.get('ground_anim', None)
        self.close_anim_config = self.custom_param.get('close_anim', None)
        self.finish_open_anim_config = self.custom_param.get('finish_open_anim', None)
        self.leave_anim = self.custom_param.get('leave_anim', None)
        self._skin_anim_postfix = ''
        self._hide_trail = False
        return

    def on_init_complete(self):
        super(Parachute, self).on_init_complete()
        self.is_avatar = self.ev_g_is_avatar()

    def destroy(self):
        super(Parachute, self).destroy()
        if self._parachute_animator:
            self._parachute_animator.destroy()
            self._parachute_animator = None
        self._parachute = None
        return

    def on_load_model_complete(self, *args):
        if self.load_model_callback:
            self.load_model_callback()
            self.load_model_callback = None
        return

    def on_load_animator_complete(self, *args):
        self.on_load_model_complete()
        if self.sd.ref_parachute_stage == parachute_utils.STAGE_PARACHUTE_DROP:
            self.switch_to_parachute_status()
            self._equip_parachute()
        self._set_parachute_state(self._parachute_state)

    def _change_character_attr(self, name, *arg):
        if not self.ev_g_get_state(self.sid):
            return
        if name == 'animator_info':
            only_active = arg[0]
            print(('test--Parachute._change_character_attr--animator_info--_parachute_state =', self._parachute_state, '--only_active =', only_active, '--unit_obj =', self.unit_obj))
            if self._parachute_animator:
                self._parachute_animator.print_info(active=only_active)

    def get_parachute_animator(self):
        return self._parachute_animator

    def get_parachute_model(self):
        model = self._parachute() if self._parachute else None
        if model and model.valid:
            return model
        else:
            return
            return

    def enter(self, leave_states):
        super(Parachute, self).enter(leave_states)
        self.update_animtion_postfix()
        if self.sd.ref_parachute_follow_target:
            self.send_event('E_REFRESH_PARACHUTE_FOLLOW_FREE_SIGHT_CAMERA')

    def exit(self, enter_states):
        super(Parachute, self).exit(enter_states)
        self._end_parachute()
        self._set_parachute_state(animation_const.PARACHUTE_STATE_NONE)
        self._anim_duration = 0
        self.send_event('E_SET_PARACHUTE_FORCE_SPD', math3d.vector(0, 0, 0))

    def update(self, dt):
        last_anim_duration = self._anim_duration
        super(Parachute, self).update(dt)
        self._anim_duration -= dt
        if last_anim_duration > 0 and self._anim_duration <= 0:
            if self._parachute_state == animation_const.PARACHUTE_STATE_OPENING:
                self._end_open_parachute()
            elif self._parachute_state == animation_const.PARACHUTE_STATE_ON_GROUND:
                self._end_parachute_on_ground()

    def _end_open_parachute(self, *args):
        if self._parachute_state != animation_const.PARACHUTE_STATE_OPENING:
            return
        self._set_parachute_state(animation_const.PARACHUTE_STATE_FINISH_OPEN)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', self.move_vector.x, self.move_vector.z)

    def _end_parachute_on_ground(self, *args):
        if self._parachute_state != animation_const.PARACHUTE_STATE_ON_GROUND:
            return
        self._set_parachute_state(animation_const.PARACHUTE_STATE_NONE)
        self._end_parachute()
        self.send_event('E_ON_GROUND_FINISH')

    def _change_anim_move_dir(self, dir_x, dir_y, *args):
        if dir_x is None or dir_y is None:
            return
        else:
            if not self.is_active:
                self._dir_x = dir_x
                self._dir_y = dir_y
                return
            if self._parachute_state == animation_const.PARACHUTE_STATE_CLOSE:
                if self._dir_y * dir_y < 0.0:
                    clip_name = ''
                    if self._dir_y > 0:
                        clip_name = self.close_anim_config['move']['f']
                    else:
                        clip_name = self.close_anim_config['move']['b']
                    self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, loop=True, blend_time=0.2)
                elif self._dir_x * dir_x < 0.0:
                    if self._dir_x > 0:
                        clip_name = self.close_anim_config['move']['r']
                    else:
                        clip_name = self.close_anim_config['move']['l']
                    self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, loop=True, blend_time=0.2)
            self._dir_x = dir_x
            self._dir_y = dir_y
            if dir_x != 0.0 or dir_y != 0.0:
                self.send_event('E_MOVE_STATE', animation_const.MOVE_STATE_WALK)
            else:
                self.send_event('E_MOVE_STATE', animation_const.MOVE_STATE_STAND)
            if self._parachute_animator:
                self._parachute_animator.SetFloat('dir_x', dir_x)
                self._parachute_animator.SetFloat('dir_y', dir_y)
            return

    def _on_change_move_state(self, *args):
        if not self.is_active:
            return
        clip_name = ''
        bind_clip_name = ''
        loop = True
        dir_type = 1
        if self._parachute_state == animation_const.PARACHUTE_STATE_CLOSE:
            clip_name = self.get_close_anim()
        elif self._parachute_state == animation_const.PARACHUTE_STATE_FINISH_OPEN:
            clip_name, dir_type = self.get_finish_open_anim()
            bind_clip_name = clip_name
        if clip_name:
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=loop, blend_time=0.2)
        if bind_clip_name:
            self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_PARACHUTE, bind_clip_name, dir_type, loop=loop, blend_time=0.2)

    def get_close_anim(self):
        move_action = self.ev_g_move_state()
        if move_action == animation_const.MOVE_STATE_STAND:
            return self.close_anim_config['idle']
        if self._dir_y > 0:
            return self.close_anim_config['move']['f']
        if self._dir_y < 0:
            return self.close_anim_config['move']['b']
        if self._dir_x > 0:
            return self.close_anim_config['move']['r']
        if self._dir_x < 0:
            return self.close_anim_config['move']['l']

    def get_finish_open_anim(self):
        move_action = self.ev_g_move_state()
        if move_action == animation_const.MOVE_STATE_STAND:
            return (self.finish_open_anim_config['idle'], 1)
        else:
            return (
             self.finish_open_anim_config['move'], 4)

    def _set_parachute_state(self, parachute_state):
        if not self.ev_g_get_state(self.sid):
            return
        self._parachute_state = parachute_state
        clip_name = ''
        bind_clip_name = ''
        self._anim_duration = 0
        loop = False
        dir_type = 1
        if self._parachute_state == animation_const.PARACHUTE_STATE_CLOSE:
            clip_name = self.get_close_anim()
            loop = True
        elif self._parachute_state == animation_const.PARACHUTE_STATE_OPENING:
            clip_name = self.opening_anim
            bind_clip_name = clip_name
        elif self._parachute_state == animation_const.PARACHUTE_STATE_FINISH_OPEN:
            clip_name, dir_type = self.get_finish_open_anim()
            bind_clip_name = clip_name
            loop = True
        elif self._parachute_state == animation_const.PARACHUTE_STATE_ON_GROUND:
            clip_name = self.ground_anim
            bind_clip_name = clip_name
        elif self._parachute_state == animation_const.PARACHUTE_STATE_NONE:
            bind_clip_name = self.leave_anim
        if clip_name:
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=loop, blend_time=0.2)
            if not loop:
                self._anim_duration = self.ev_g_get_anim_length(clip_name)
        if bind_clip_name:
            new_clip_name = bind_clip_name + self._skin_anim_postfix
            parachute_model = self.get_parachute_model()
            if new_clip_name != bind_clip_name and parachute_model and parachute_model.has_anim(new_clip_name):
                bind_clip_name = new_clip_name
            self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_PARACHUTE, bind_clip_name, dir_type, loop=loop, blend_time=0.2)
            if self._hide_trail:
                parachute_model = self.get_parachute_model()
                if parachute_model:
                    all_sockets_obj = parachute_model.get_all_objects_on_sockets()
                    for one_sfx in all_sockets_obj:
                        one_sfx.visible = False

    def _on_swim(self, *args):
        self._remove_parachute()

    def _on_stand(self, *args, **kwargs):
        self.on_end_parachute()

    def _move_toward(self, move_vec):
        if not move_vec:
            return
        if self.sd.ref_parachute_follow_target and self.is_avatar:
            return
        self.move_vector = math3d.vector(move_vec)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', move_vec.x, move_vec.z)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_PARA_TOWARD, (move_vec.x, move_vec.z)], False)

    def _move_stop(self):
        self.send_event('E_ACTION_MOVE_STOP')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_PARA_STOP, ()], False)

    def switch_to_parachute_status(self):
        current_posture_state = self.ev_g_anim_state()
        if current_posture_state != animation_const.STATE_PARACHUTE:
            self.send_event('E_SWITCH_STATUS', animation_const.STATE_PARACHUTE)
            self.send_event('E_PAUSE_TWIST_ROTATE')

    def _equip_parachute(self, path='model_new/vehicle/glide/502/glide.gim'):
        if self.ev_g_is_pure_mecha():
            return
        else:
            if self._remove_parachute_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._remove_parachute_timer_id)
                self._remove_parachute_timer_id = None
            self._remove_parachute()
            if not self.ev_g_animator():
                return
            if not self.ev_g_status_try_trans(self.sid):
                self.send_event('E_DUMP_STATE')
                return
            self.switch_to_parachute_status()
            fashion_id = self.get_fashion_item_id()
            if fashion_id is not None:
                from logic.gutils import dress_utils
                clothing_path = dress_utils.get_vehicle_res(fashion_id)
                if clothing_path is not None:
                    path = clothing_path
            self.ev_g_load_model(path, self._parachute_load_callback, None, None, game3d.ASYNC_HIGH, animator_path=self.DEFAULT_XML, use_cache_model=True, is_unbind_socket_obj=False)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EQUIP_PARACHUTE, ()], False)
            return

    def _parachute_load_callback(self, model, user_data, *args):
        if not self.ev_g_get_state(self.sid):
            log_error('test--_parachute_load_callback--step1--unit_obj =', self.unit_obj)
            self.send_event('E_DUMP_STATE')
            self.send_event('E_UNLOAD_MODEL', model, None, is_reset_material=False)
            return
        else:
            if self._remove_parachute_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._remove_parachute_timer_id)
                self._remove_parachute_timer_id = None
            if self._delay_remove_parachute_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._delay_remove_parachute_timer_id)
                self._delay_remove_parachute_timer_id = None
            if self._parachute:
                old_model = self.get_parachute_model()
                if old_model:
                    human_model = self.ev_g_model()
                    if human_model:
                        human_model.unbind(old_model)
                    self.send_event('E_UNLOAD_MODEL', old_model, self._parachute_animator, is_reset_material=False)
                self._parachute_animator = None
            model.remove_from_parent()
            model.world_position = math3d.vector(0, 0, 0)
            model.rotation_matrix = math3d.matrix()
            model.world_rotation_matrix = math3d.matrix()
            model.scale = math3d.vector(1, 1, 1)
            self._parachute = weakref.ref(model)
            cache_animator = None
            if len(args) > 0:
                cache_animator = args[0]

            def _wait_load_model(p_model):
                model = self.ev_g_model()
                model.bind('glide', p_model)
                glide_fx_id = self.ev_g_glide_effect()
                skin_id = self.get_fashion_item_id()
                Parachute.equip_glide_effect(p_model, skin_id, glide_fx_id)
                p_model.cast_shadow = True
                self.on_equip_parachute(cache_animator)

            self._add_load_model_callback(_wait_load_model, model)
            self.send_event('E_OPEN_PARACHUTE_SOUND')
            if model.get_file_path().endswith('empty.gim'):
                model.set_submesh_visible('empty', False)
            return

    @staticmethod
    def equip_glide_effect(p_model, skin_id, glide_fx_id):
        if glide_fx_id is not None:
            from logic.gutils.role_skin_utils import load_glide_model_effect_and_model, get_glide_effect_socket_data
            sockets_data = get_glide_effect_socket_data(skin_id, glide_fx_id)
            load_glide_model_effect_and_model(p_model, sockets_data)
        return

    def on_equip_parachute(self, cache_animator):
        self._parachute_animator = cache_animator
        if self._parachute_animator:
            self.do_load_parachute_animator()
        else:
            parachute_model = self.get_parachute_model()
            p_model = self.ev_g_model()
            if p_model:
                parachute_model.visible = p_model.visible
            else:
                parachute_model.visible = True
            self._parachute_animator = animator.Animator(parachute_model, self.DEFAULT_XML, self.unit_obj)
            self._parachute_animator.Load(True, self.do_load_parachute_animator)

    def update_animtion_postfix(self):
        if not self._parachute_animator:
            return
        fashion_id = self.get_fashion_item_id()
        if not fashion_id:
            return
        action_postfix = confmgr.get('items_skin_conf', 'VehicleSkinConfig', 'Content', str(fashion_id), 'action_postfix')
        if not action_postfix:
            return
        self._skin_anim_postfix = action_postfix

    def get_fashion_item_id(self):
        if not has_skin_ext():
            return
        else:
            parachute_item_id = 502
            fashion_dic = self.ev_g_item_fashion(parachute_item_id)
            from logic.gcommon.item.item_const import FASHION_POS_SUIT
            fashion_id = fashion_dic.get(FASHION_POS_SUIT, None)
            return fashion_id

    def do_load_parachute_animator(self, *args):
        if not self._parachute_animator:
            log_error('test--do_load_parachute_animator--step1--unit_obj =', self.unit_obj)
            return
        from logic.gcommon.common_const.attr_const import HUMAN_ATTR_SHOW_TAIL_EFFECT_ON_MECHA_DIE
        hide_trail = False
        if self.ev_g_attr_get(HUMAN_ATTR_SHOW_TAIL_EFFECT_ON_MECHA_DIE, 1) <= 0:
            opposite = not global_data.cam_lplayer or not self.ev_g_is_campmate(global_data.cam_lplayer.ev_g_camp_id())
            hide_trail = opposite
        self._hide_trail = hide_trail
        self._set_parachute_state(animation_const.PARACHUTE_STATE_CLOSE)
        parachute_model = self.get_parachute_model()
        all_sockets_obj = parachute_model.get_all_objects_on_sockets()
        for one_sfx in all_sockets_obj:
            if one_sfx.__class__.__name__ != 'sfx':
                continue
            one_sfx.restart()
            one_sfx.visible = not hide_trail and parachute_model.visible

        animator = self.ev_g_animator()
        if animator:
            move_action = self.ev_g_move_state()
            rocker_dir = self.sd.ref_rocker_dir
            dir_x = 0
            dir_y = 0
            if rocker_dir:
                dir_x = rocker_dir.x
                dir_y = rocker_dir.z
            self._parachute_animator.SetFloat('dir_x', dir_x)
            self._parachute_animator.SetFloat('dir_y', dir_y)
        if self.ev_g_get_state(self.sid):
            if self.ev_g_is_avatar():
                self._set_parachute_state(animation_const.PARACHUTE_STATE_OPENING)
            else:
                self._set_parachute_state(animation_const.PARACHUTE_STATE_FINISH_OPEN)
        else:
            self._on_land()
        for socket_name, soft_bone_param in six.iteritems(self.SOFTBONE_SOCKET_CONF):
            soft_bone_model = parachute_model.get_socket_obj(socket_name)
            if soft_bone_model:
                from logic.gutils.dress_utils import init_spring_anim
                init_spring_anim(soft_bone_model, confmgr.get(soft_bone_param))

    def parachute_land(self):
        if not self.ev_g_is_avatar():
            self._remove_parachute(is_delay_clear=True)

    def _end_parachute(self, *args):
        self.send_event('PARACHUTE_LAND_FINISHED')
        self.on_end_parachute()

    def on_end_parachute(self):
        self.ev_g_cancel_state(self.sid)
        if not self._parachute_animator and not self._parachute:
            return
        clip_length = 1
        if self._parachute_animator:
            animation_node = self._parachute_animator.find('ground')
            if animation_node:
                clip_length = animation_node.length * 1.1
        if clip_length <= Parachute.DELAY_CLEAR_TIME:
            log_error('parachute DELAY_CLEAR_TIME will fail!!!', clip_length, Parachute.DELAY_CLEAR_TIME)
            import traceback
            traceback.print_stack()
        if self._remove_parachute_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._remove_parachute_timer_id)
        self._remove_parachute_timer_id = global_data.game_mgr.register_logic_timer(self._remove_parachute_tick, clip_length, times=-1, mode=timer.CLOCK)

    def _remove_parachute_tick(self, *args):
        parachute_model = self.get_parachute_model()
        if not parachute_model:
            return timer.RELEASE
        self._remove_parachute(is_delay_clear=True)

    def _remove_parachute(self, is_delay_clear=False):
        parachute_model = self.get_parachute_model()
        if not parachute_model:
            return
        else:
            if not (self.unit_obj and self.unit_obj._event_mgr):
                return
            if self.ev_g_is_pure_mecha():
                return
            if self.ev_g_is_avatar() and self.ev_g_get_state(self.sid):
                print(('test--_remove_parachute--unit_obj =', self.unit_obj))
                import traceback
                traceback.print_stack()
            if self._remove_parachute_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._remove_parachute_timer_id)
                self._remove_parachute_timer_id = None
            if self._delay_remove_parachute_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._delay_remove_parachute_timer_id)
                self._delay_remove_parachute_timer_id = None
            if parachute_model:
                if is_delay_clear:
                    self._delay_remove_parachute_timer_id = global_data.game_mgr.register_logic_timer(self._parachute_delay_clear, Parachute.DELAY_CLEAR_TIME, times=1, mode=timer.CLOCK)
                    parachute_model.visible = False
                else:
                    self._parachute_delay_clear()
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_DO_REMOVE_PARACHUTE, ()], True)
            return

    def _parachute_delay_clear(self):
        parachute_model = self.get_parachute_model()
        if not parachute_model:
            return
        else:
            p_model = parachute_model
            human_model = self.ev_g_model()
            if p_model and p_model.valid and human_model and human_model.valid:
                from logic.gutils.role_skin_utils import clear_glide_model_effect_and_model
                clear_glide_model_effect_and_model(parachute_model)
                human_model.unbind(parachute_model)
                self.send_event('E_UNLOAD_MODEL', parachute_model, self._parachute_animator, is_reset_material=False)
            self._parachute = None
            if self._parachute_animator:
                self._parachute_animator.destroy()
                self._parachute_animator = None
            return

    def _switch_parachute_bind_pos(self):
        p_model = self.get_parachute_model()
        if not p_model:
            return
        model = self.ev_g_model()
        if not model:
            return
        glide_matrix = model.get_socket_matrix('glide', world.SPACE_TYPE_WORLD)
        forward = self.ev_g_model_right()
        p_model.inherit_flag = world.INHERIT_VISIBLE
        p_model.world_position = glide_matrix.translation
        p_model.world_rotation_matrix = math3d.matrix.make_orient(forward, math3d.vector(0, 1, 0))
        from logic.gutils.role_skin_utils import get_glide_model_effect_and_model

        def clear_sfx():
            p_model = self.get_parachute_model()
            if not p_model:
                return
            sub_model_list, sub_sfx_list = get_glide_model_effect_and_model(p_model)
            for sub_sfx_id in sub_sfx_list:
                sub_sfx = global_data.sfx_mgr.get_sfx_by_id(sub_sfx_id)
                if not sub_sfx:
                    continue
                if not self._hide_trail:
                    sub_sfx.inherit_flag = world.INHERIT_TRANSLATION
                sub_sfx.shutdown(False)

        global_data.game_mgr.delay_exec(0.3, clear_sfx)

    def _on_land(self, *args):
        self._set_parachute_state(animation_const.PARACHUTE_STATE_ON_GROUND)
        self._switch_parachute_bind_pos()
        self._end_parachute()
        self.send_event('E_RESET_PHY')
        model = self.ev_g_model()
        if model:
            model.receive_shadow = True

    def _add_load_model_callback(self, added_cb, *args):
        model = self.ev_g_model()
        if model:
            added_cb(*args)
        elif self.load_model_callback:
            original_cb = self.load_model_callback
            self.load_model_callback = lambda : original_cb() and added_cb(*args)
        else:
            self.load_model_callback = lambda : added_cb(*args)

    def _start_parachute_stage(self, *args):

        def _wait_load_model():
            if self.sd.ref_parachute_stage != parachute_utils.STAGE_LAND:
                self.start_parachute()

        self._add_load_model_callback(_wait_load_model)

    def start_parachute(self):
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_PARACHUTE)
        self._set_parachute_state(animation_const.PARACHUTE_STATE_CLOSE)