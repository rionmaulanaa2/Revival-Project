# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComJumpLobby.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from logic.gcommon.cdata import status_config
import logic.gcommon.common_const.animation_const as animation_const
import common.utils.timer as timer
import time
import world
from logic.gcommon.cdata import jump_physic_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata import speed_physic_arg
import math3d
import data.weapon_action_config as weapon_action_config
from logic.gutils import character_ctrl_utils
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_utils import parachute_utils
import logic.gcommon.common_const.water_const as water_const
from common.cfg import confmgr
from logic.gcommon.common_const.skill_const import SKILL_AIR_JUMP
from logic.gcommon.component.client.com_lobby_char.ComJumpLobbyBase import ComJumpLobbyBase

class ComJumpLobby(ComJumpLobbyBase):
    JUMP_TYPE_NORMAL = 1
    JUMP_TYPE_SMALL_SUPER_JUMP = 2
    JUMP_TYPE_BIG_SUPER_JUMP = 3
    JUMP_STATE = (
     status_config.ST_JUMP,)
    BIND_EVENT = ComJumpLobbyBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_ACTION_SWITCH_TO_JUMP': '_on_jump',
       'E_CHANGE_JUMP_STATE': '_change_jump_state',
       'G_FALL_ON_GROUND_TYPE': '_get_fall_on_ground_type',
       'G_ACTION_IS_JUMP': 'action_is_jump',
       'E_ON_GROUND_FINISH': 'on_action_ground_finish',
       'E_CTRL_JUMP': '_jump',
       'E_SET_JUMP_RECOVER_TIME': '_on_set_jump_recover_time',
       'E_FALL': '_fall',
       'E_CANCEL_JUMP': '_cancel_jump',
       'E_CLEAN_JUMP': '_clean_jump',
       'G_JUMP_STATE': 'get_jump_state',
       'E_LEAVE_STATE': '_leave_states',
       'E_ON_SYNC_BEGIN_JUMP': '_on_sync_begin_jump',
       'E_ON_SYNC_SET_JUMP_UPBODY_BLEND': 'set_jump_upbody_blend',
       'E_FORCE_ON_GROUND': '_on_ground',
       'E_ACTION_SYNC_ON_GROUND': '_on_ground',
       'G_GET_INVALID_JUMP_HEIGHT': 'get_invalid_jump_height',
       'E_CLEAR_INVALID_JUMP_HEIGHT': 'clear_invalid_jump_height',
       'G_CAN_JUMP': 'can_jump'
       })

    def __init__(self):
        super(ComJumpLobby, self).__init__()
        self._jump_state = None
        self._fall_on_ground_type = animation_const.FALL_ON_GROUND_LOW_SPEED
        self.jump_track_start_time = 0
        self._jump_track_duration = 0
        self._last_jump_pass_time = 0
        self._jump_timer_id = None
        self._falling_timer_id = None
        self._jump_track = None
        self._stage = 0
        self._max_stage = 1
        self._delay_ground_timer_id = None
        self._jump_upbody_blend = 0
        self._start_position = None
        self._jump_type = self.JUMP_TYPE_NORMAL
        self._invalid_jump_height = 0
        self._max_jump_config = {}
        self.ON_GROUND_TIME_SCALE = 0.1
        self._jumping = False
        self._enable_all_log = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComJumpLobby, self).init_from_dict(unit_obj, bdict)
        self._max_jump_config = confmgr.get('anti_cheat_params_config', 'check_param_config', 'Content', 'jump_max', 'param_value', default={'normal_max_jump_height': 3,'super_max_jump_height': 25,'max_super_jump_speed': 21})

    def destroy(self):
        super(ComJumpLobby, self).destroy()
        self._clean_delay_ground_timer()
        self._clean_failling_timer()
        self._clean_jump_timer()

    def _try_trans_status(self, status):
        from logic.gutils.lobby_jump_utils import can_jump
        if not can_jump(self.unit_obj):
            return False
        return True

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        else:
            self.send_event('E_REGISTER_ANIM_ACTIVE', animation_const.BEGIN_FALL_GROUND_EVENT, self.begin_jump_fall_ground)
            self.send_event('E_REGISTER_ANIM_STATE_EXIT', animation_const.END_JUMP_UP_EVENT, self._end_jump_up)
            if self._jump_state is not None:
                self._set_jump_state(self._jump_state)
            self._set_fall_on_ground_type(self._fall_on_ground_type)
            return

    def _leave_states(self, leave_state, new_state=None):
        if leave_state == status_config.ST_JUMP:
            self._clear_jump_acceleration()
            if new_state:
                self._on_end_jump()

    def _is_jump(self):
        return self._jumping

    def _on_set_jump_recover_time(self, recover_time):
        self._delay_on_ground(recover_time)

    def _on_ground(self, *args):
        if self._enable_all_log:
            print('_on_ground')
        self._on_end_jump()
        is_input_moving = self.ev_g_is_move()
        if is_input_moving:
            self.ON_GROUND_TIME_SCALE = 0.1
        else:
            self.send_event('E_CHARACTER_WALK', math3d.vector(0, 0, 0))
            self.send_event('E_ACTION_SYNC_VEL', math3d.vector(0, 0, 0))
            self.ON_GROUND_TIME_SCALE = 0.6
        self._clean_failling_timer()
        touch_ground_speed = args[0]
        force_onground = False
        if len(args) == 2:
            force_onground = args[1]
        if self._enable_all_log:
            print('test--_on_ground--step2--touch_ground_speed =', touch_ground_speed)
        self.send_event('E_ACTION_SYNC_JUMP', animation_const.JUMP_STATE_FALL_GROUND, -touch_ground_speed)
        self._clear_jump_acceleration()
        can_ground = self.ev_g_is_jump()
        if not can_ground:
            if self._enable_all_log:
                self.send_event('E_DUMP_STATE')
        self.send_event('E_CHANGE_JUMP_STATE', animation_const.JUMP_STATE_FALL_GROUND, touch_ground_speed)
        fall_on_ground_type = self.ev_g_fall_on_ground_type()
        if self._enable_all_log:
            print('test--_on_ground--fall_on_ground_type =', fall_on_ground_type)
        if fall_on_ground_type == animation_const.FALL_ON_GROUND_HIGH_SPEED or fall_on_ground_type == animation_const.FALL_ON_GROUND_MEDIUM_SPEED:
            self.send_event('E_CHARACTER_WALK', math3d.vector(0, 0, 0))
        character = self.sd.ref_character
        if character:
            character.setOnTouchGroundCallback(None)
        jump_recover_time = 0.5
        if force_onground:
            jump_recover_time = 0
        self._delay_on_ground(jump_recover_time, force_onground)
        self.send_event('E_ON_GROUND')
        return

    def _clean_failling_timer(self):
        if self._falling_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._falling_timer_id)
        self._falling_timer_id = None
        return

    def _on_end_jump(self):
        self._stage = 0

    def _delay_on_ground(self, jump_recover_time, force_onground=False):
        self._clean_delay_ground_timer()
        jump_recover_time *= self.ON_GROUND_TIME_SCALE
        if jump_recover_time:
            character = self.sd.ref_character
            if character:
                move_dir = character.getWalkDirection()
                if not move_dir.is_zero:
                    self.send_event('E_CHANGE_SPEED', 0.5)
            self._delay_ground_timer_id = global_data.game_mgr.register_logic_timer(self._on_ground_finish, jump_recover_time, times=1, mode=timer.CLOCK)
        else:
            self._on_ground_finish(force_onground)

    def _on_ground_finish(self, force_onground=False):
        character = self.sd.ref_character
        self._on_end_jump()
        self._jumping = False
        if not force_onground:
            is_avatar = self.unit_obj.__class__.__name__ is 'LLobbyAvatar'
            if is_avatar and not (character and character.onGround()):
                return
        if self._jump_state == animation_const.JUMP_STATE_UP:
            return
        else:
            self._delay_ground_timer_id = None
            if not self.is_valid():
                return
            self.send_event('E_RESET_GRAVITY')
            self._clear_jump_acceleration()
            self.ev_g_cancel_state(status_config.ST_JUMP)
            can_stand = self._try_trans_status(status_config.ST_STAND)
            if self._enable_all_log:
                print('test--_on_ground_finish--step1--can_stand =', can_stand)
            if can_stand:
                self.send_event('E_ON_GROUND_FINISH')
                self.send_event('E_CHECK_CONTINUE_MOVE')
            return

    def _fall(self):
        if self.ev_g_is_jump():
            return
        self.send_event('E_CTRL_JUMP', True)

    def set_jump_upbody_blend(self, jump_upbody_blend):
        self._jump_upbody_blend = jump_upbody_blend
        self.send_event('E_SET_ANIMATOR_INT_STATE', 'jump_upbody_blend', jump_upbody_blend)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ON_SYNC_SET_JUMP_UPBODY_BLEND, (jump_upbody_blend,)], True)

    def can_jump(self):
        if self.ev_g_is_climb():
            return False
        else:
            if self.ev_g_is_jump():
                return False
            character = self.sd.ref_character
            if character:
                if character.canJump():
                    return True
                if self._enable_all_log:
                    print('test--can_jump--isJumping =', character.isJumping(), '--isFalling =', character.isFalling(), '--isSliding =', character.isSliding())
                if not character.isJumping() and not character.isFalling() and not character.isSliding():
                    return True
                return False
            is_avatar = self.unit_obj.__class__.__name__ is 'LLobbyAvatar'
            return not is_avatar

    def _jump(self, fall=False):
        if self._enable_all_log:
            print('test--_jump--step1')
        character = self.sd.ref_character
        waiting_active = self.ev_g_char_waiting()
        if waiting_active:
            return
        else:
            jump_upbody_blend = 1
            self.set_jump_upbody_blend(jump_upbody_blend)
            if not fall:
                if self._enable_all_log:
                    print('test--_jump--step2--_stage =', self._stage, '--_max_stage =', self._max_stage, '--can_jump =', self.can_jump())
                if self._stage == 0 and not self.can_jump():
                    return
                if self._stage >= self._max_stage:
                    return
                if character and self.ev_g_is_jump():
                    self.ev_g_cancel_state(status_config.ST_JUMP)
                if self._enable_all_log:
                    print('test--_jump--step3--_stage =', self._stage)
                    self.send_event('E_DUMP_STATE')
                if not self._try_trans_status(status_config.ST_JUMP):
                    return
                self._jumping = True
                self._stage += 1
                self.send_event('E_PLAY_JUMP_SOUND', self._stage)
                self.send_event('E_ACTION_SWITCH_TO_JUMP', animation_const.JUMP_STATE_UP)
                self.send_event('E_ACTION_SYNC_JUMP', animation_const.JUMP_STATE_UP)
                if jump_upbody_blend == 0:
                    node_name = animation_const.RUN_JUMP_NODE_NAME
                else:
                    node_name = animation_const.NOT_RUN_JUMP_NODE_NAME
                self._start_position = self.ev_g_position()
                self._jump_type = self.JUMP_TYPE_NORMAL
                self.begin_jump_up('', node_name)
                if self._enable_all_log:
                    print('test--_jump--step4--_stage =', self._stage, '--node_name =', node_name)
                self._clean_delay_ground_timer()
            else:
                if not self._try_trans_status(status_config.ST_JUMP):
                    return
                self.send_event('E_ACTION_SWITCH_TO_JUMP', animation_const.JUMP_STATE_IN_AIR)
                self._start_position = None
                self.send_event('E_ACTION_SYNC_JUMP', animation_const.JUMP_STATE_IN_AIR)
            character and character.setOnTouchGroundCallback(self._on_ground)
            world_move_dir = self.ev_g_human_move_dir()
            if world_move_dir and not world_move_dir.is_zero:
                self._begin_jump_acceleration()
            return

    def _clean_delay_ground_timer(self):
        if self._delay_ground_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._delay_ground_timer_id)
        self._delay_ground_timer_id = None
        return

    def action_is_jump(self):
        current_posture_state = self.ev_g_anim_state()
        return current_posture_state == animation_const.STATE_JUMP

    def _set_fall_on_ground_type(self, fall_on_ground_type):
        self._fall_on_ground_type = fall_on_ground_type
        self.send_event('E_SET_ANIMATOR_INT_STATE', 'fall_on_ground_type', self._fall_on_ground_type)

    def _get_fall_on_ground_type(self):
        return self._fall_on_ground_type

    def _cancel_jump(self, *args):
        if self.ev_g_is_in_any_state(self.JUMP_STATE):
            for state in self.JUMP_STATE:
                self.ev_g_cancel_state(state)

            self._on_ground_finish(True)

    def _clean_jump(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            char_ctrl.setOnTouchGroundCallback(None)
        return

    def _on_jump(self, *arg):
        jump_state = animation_const.JUMP_STATE_UP
        if len(arg) > 0:
            jump_state = arg[0]
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_SWITCH_TO_JUMP, ()], True)
        self.send_event('E_CHANGE_JUMP_STATE', jump_state)
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_JUMP, False)
        self.send_event('E_JUMP')

    def get_invalid_jump_height(self):
        return self._invalid_jump_height

    def clear_invalid_jump_height(self, *args):
        self._invalid_jump_height = 0

    def _change_jump_state(self, state, *arg):
        sync_arg = [
         state]
        sync_arg.extend(arg)
        if state == animation_const.JUMP_STATE_FALL_GROUND:
            gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
            if self._enable_all_log:
                print('test--_change_jump_state--JUMP_STATE_FALL_GROUND--gravity =', gravity)
            touch_ground_speed = 0
            if len(arg) > 0:
                touch_ground_speed = arg[0]
            if not touch_ground_speed:
                touch_ground_speed = 0
            fall_on_ground_type = animation_const.FALL_ON_GROUND_LOW_SPEED
            if -touch_ground_speed <= speed_physic_arg.fall_speed_threshold_large:
                fall_on_ground_type = animation_const.FALL_ON_GROUND_HIGH_SPEED
            elif -touch_ground_speed <= speed_physic_arg.fall_speed_threshold:
                fall_on_ground_type = animation_const.FALL_ON_GROUND_MEDIUM_SPEED
            self._set_fall_on_ground_type(fall_on_ground_type)
        elif state == animation_const.JUMP_STATE_IN_AIR:
            gravity = jump_physic_config.jump_fall_gravity * NEOX_UNIT_SCALE
            self.send_event('E_SET_GRAVITY', gravity)
            if self._jump_upbody_blend == 0:
                node_name = animation_const.RUN_JUMP_IN_AIR_NODE_NAME
            else:
                node_name = animation_const.NOT_RUN_JUMP_IN_AIR_NODE_NAME
            if self._start_position:
                position = self.ev_g_position()
                if position:
                    cur_max_jump_height = position.y - self._start_position.y
                    cur_max_jump_height /= NEOX_UNIT_SCALE
                    if self._jump_type != self.JUMP_TYPE_BIG_SUPER_JUMP:
                        def_max_jump_height = self._max_jump_config.get('super_max_jump_height', 10)
                        if self._jump_type == self.JUMP_TYPE_NORMAL:
                            def_max_jump_height = self._max_jump_config.get('normal_max_jump_height', 3)
                            if self._max_stage > 0:
                                def_max_jump_height *= self._max_stage
                        if self._enable_all_log:
                            print(('test--_change_jump_state--_jump_type =', self._jump_type, '--cur_max_jump_height =', cur_max_jump_height, '--def_max_jump_height =', def_max_jump_height, '*********'))
                        if cur_max_jump_height > def_max_jump_height:
                            self._invalid_jump_height = cur_max_jump_height
            self.begin_jump_in_air('', node_name)
        self.send_event('E_ON_JUMP_STATE_CHANGE', state)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CHANGE_JUMP_STATE, sync_arg], True)
        self._set_jump_state(state)

    def _set_jump_state(self, jump_state):
        if self._enable_all_log:
            print('test--_set_jump_state--jump_state =', jump_state, '--unit_obj =', self._jump_state, jump_state, self.unit_obj)
        if self._jump_state == jump_state:
            return
        self._jump_state = jump_state
        animator = self.ev_g_animator()
        if animator:
            from logic.gcommon.common_const.lobby_ani_const import STATE_JUMP
            self.send_event('E_SET_ANIMATOR_INT_STATE', 'state_idx', STATE_JUMP)
            self.send_event('E_SET_ANIMATOR_INT_STATE', 'jump_state', jump_state)
        if jump_state in (animation_const.JUMP_STATE_IN_AIR, animation_const.JUMP_STATE_FALL_GROUND):
            if self._enable_all_log:
                print('test--_set_jump_state--step1')
                self.send_event('E_DUMP_STATE')

    def get_jump_state(self):
        return self._jump_state

    def _jump_tick(self, *args):
        pass_time = time.time() - self.jump_track_start_time
        pass_time *= 1000
        if self._enable_all_log:
            print('test--_jump_tick--step1--pass_time = ', pass_time, '--_jump_track_duration =', self._jump_track_duration)
        _jump_track_duration = 0.9 * self._jump_track_duration
        character = self.sd.ref_character
        if self._last_jump_pass_time >= _jump_track_duration and pass_time > _jump_track_duration:
            if character:
                character.verticalVelocity = 0
            self._jump_timer_id = None
            return timer.RELEASE
        else:
            pass_time = min(pass_time, _jump_track_duration)
            cur_key_index = self._jump_track.get_key_index(pass_time)
            cur_key_time = self._jump_track.get_key_time(cur_key_index)
            key_count = self._jump_track.get_key_count()
            self._last_jump_pass_time = pass_time
            next_key_index = cur_key_index + 1
            next_key_time = self._jump_track.get_key_time(next_key_index)
            cur_key_pos = self._jump_track.get_position(cur_key_time)
            next_key_pos = self._jump_track.get_position(next_key_time)
            if character:
                duration = (next_key_time - cur_key_time) / 1000.0
                diff_height = next_key_pos.y - cur_key_pos.y
                speed = diff_height / duration
                character.verticalVelocity = speed
                if self._enable_all_log:
                    print('test--_jump_tick--step1--pass_time = ', pass_time, '--_jump_track_duration =', self._jump_track_duration, '--cur_key_index =', cur_key_index, '--between_key_duration =', next_key_time - cur_key_time, '--verticalVelocity =', speed, '--next_key_pos.y =', next_key_pos.y, '--cur_key_pos.y =', cur_key_pos.y, '--diff_height =', diff_height, '--key_count =', key_count)
            return

    def _on_sync_begin_jump(self, arg, node_name):
        self._try_trans_status(status_config.ST_JUMP)
        self.begin_jump_up(arg, node_name)

    def update_jump_node(self, arg, node_name):
        animator = self.ev_g_animator()
        if not animator:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ON_SYNC_BEGIN_JUMP, (arg, node_name)], True)
        animation_node = animator.find(node_name)
        if not animation_node:
            return
        if self._enable_all_log:
            print('test--begin_jump_up--step1--node_name =', node_name, '--arg =', arg)
        self.replace_jump_clip(animation_node, 'jump_stage_1', listen_change=False)

    def begin_jump_up(self, arg, node_name):
        self.update_jump_node(arg, node_name)
        if self.ev_g_is_jump():
            self._begin_normal_jump_up(arg, node_name)

    def begin_jump_in_air(self, arg, node_name):
        animator = self.ev_g_animator()
        if not animator:
            return
        animation_node = animator.find(node_name)
        if self._enable_all_log:
            print('test--begin_jump_in_air--node_name =', node_name, '--arg =', arg)
        if not animation_node:
            return
        root_node = animator.find(animation_const.JUMP_ROOT_NODE_NAME)
        if root_node:
            root_node.timeScale = 1
        self.replace_jump_clip(animation_node, 'jump_stage_2')

    def _on_jump_anim_param_value_change(self, node_name, param_name, value, data):
        animator = self.ev_g_animator()
        if not animator:
            return
        else:
            animation_node = animator.find(node_name)
            if not animation_node or not animation_node.IsWillActiveInHierarchy():
                return
            action_key = data
            weapon_type = self.ev_g_weapon_type()
            weapon_type_2_action = weapon_action_config.weapon_type_2_action
            action_config = weapon_type_2_action.get(weapon_type, None)
            jump_stage_list = None
            if action_config:
                jump_stage_list = action_config[action_key]
            if not jump_stage_list:
                jump_stage_list = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][action_key]
            self.replace_jump_node_clip(animation_node, jump_stage_list)
            return

    def replace_jump_node_clip(self, animation_node, jump_stage_list):
        animator = self.ev_g_animator()
        if not animator:
            return
        if animation_const.SOURCE_NODE_TYPE in animation_node.nodeType:
            clip_name = jump_stage_list[0]
            animation_node.SetMaxBlendOutTime(0)
            animator.replace_clip_name(animation_node, clip_name, True)
        elif animation_const.BLEND_NODE_TYPE in animation_node.nodeType:
            all_child_states = animation_node.GetChildStates()
            for index in range(len(jump_stage_list)):
                one_child_state = all_child_states[index]
                one_source_node = one_child_state.childNode
                if animation_const.SOURCE_NODE_TYPE not in one_source_node.nodeType:
                    continue
                clip_name = jump_stage_list[index]
                one_source_node.SetMaxBlendOutTime(0)
                animator.replace_clip_name(one_source_node, clip_name, True)

            one_child_state = all_child_states[4]
            one_source_node = one_child_state.childNode
            if animation_const.SOURCE_NODE_TYPE in one_source_node.nodeType:
                clip_name = jump_stage_list[-2]
                one_source_node.SetMaxBlendOutTime(0)
                animator.replace_clip_name(one_source_node, clip_name, True)
            last_clip_name = jump_stage_list[-1]
            if len(all_child_states) >= 7:
                for index in range(5, 7):
                    one_child_state = all_child_states[index]
                    one_source_node = one_child_state.childNode
                    if animation_const.SOURCE_NODE_TYPE not in one_source_node.nodeType:
                        continue
                    clip_name = last_clip_name
                    one_source_node.SetMaxBlendOutTime(0)
                    animator.replace_clip_name(one_source_node, clip_name, True)

            if self._enable_all_log:
                print('test--replace_jump_clip--nodeName =', animation_node.nodeName)
                self.send_event('E_CHARACTER_ATTR', 'animator_info', True)
                self.send_event('E_CHARACTER_ATTR', 'animator_info_for_duration', 1.0)

    def replace_jump_clip(self, animation_node, action_key, listen_change=True):
        if not animation_node:
            return
        else:
            if animation_const.SOURCE_NODE_TYPE in animation_node.nodeType:
                action_key = 'run_' + action_key
            weapon_type = self.ev_g_weapon_type()
            weapon_type_2_action = weapon_action_config.weapon_type_2_action
            action_config = weapon_type_2_action.get(weapon_type, None)
            jump_stage_list = None
            if action_config:
                jump_stage_list = action_config[action_key]
            if not jump_stage_list:
                jump_stage_list = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][action_key]
            if listen_change:
                self.send_event('E_REGISTER_CHANGE_CLIP_EVENT', animation_node.nodeName, animation_const.JUMP_RELATE_PARAMS, self._on_jump_anim_param_value_change, action_key)
            self.replace_jump_node_clip(animation_node, jump_stage_list)
            return

    def _clean_jump_timer(self):
        if self._jump_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._jump_timer_id)
        self._jump_timer_id = None
        return

    def _begin_normal_jump_up(self, arg, node_name):
        animator = self.ev_g_animator()
        if not animator:
            return
        if self._enable_all_log:
            print('test--_begin_normal_jump_up--step1--node_name =', node_name, '--arg =', arg)
        animation_node = animator.find(node_name)
        character = self.sd.ref_character
        track_name = ''
        track = global_data.track_cache.create_track_default_none(track_name)
        if track:
            if self._enable_all_log:
                print('test--_begin_normal_jump_up--track_name =', track_name)
            self._jump_track = track
            self._jump_track_duration = self._jump_track.duration
            self.jump_track_start_time = time.time()
            self._clean_jump_timer()
            self._jump_timer_id = global_data.game_mgr.register_logic_timer(self._jump_tick, 1, mode=timer.LOGIC)
            self._jump_tick()
            if character:
                position = character.position
                position.y = position.y + 0.1
                character.position = position
                self.send_event('E_SET_JUMP_SPEED', 0)
                self.send_event('E_SET_GRAVITY', 0)
                character.jump()
        else:
            self.send_event('E_RESET_GRAVITY', True)
            jump_speed = 0
            extra_jump_factor = 0.0
            gravity = jump_physic_config.skate_up_gravity * NEOX_UNIT_SCALE
            if character:
                if self._enable_all_log:
                    print('test--_begin_normal_jump_up--step1--jump_speed =', jump_speed / NEOX_UNIT_SCALE)
                if extra_jump_factor != 0 and self._stage == self._max_stage:
                    jump_speed = jump_physic_config.jump_speed * (1.0 + extra_jump_factor) * NEOX_UNIT_SCALE
                elif self._stage == 2:
                    jump_speed = jump_physic_config.double_jump_speed_vertical * NEOX_UNIT_SCALE
                else:
                    jump_speed = jump_physic_config.jump_speed * NEOX_UNIT_SCALE
                self.send_event('E_SET_JUMP_SPEED', jump_speed)
                character.jump()
                gravity = character.getGravity()
                if self._enable_all_log:
                    print('jump_stage: ', self._stage)
                if self._stage > 1:
                    pass
            jump_up_duration = abs(jump_speed / gravity)
            jump_up_duration = jump_up_duration or 0.5
            if animation_node:
                time_scale = animation_node.duration / jump_up_duration
                if self._enable_all_log:
                    print('test--_begin_normal_jump_up--jump_up_duration =', jump_up_duration, '--animation_node.duration =', animation_node.duration, '--node_name =', animation_node.nodeName, '--time_scale =', time_scale, '--jump_speed =', jump_speed / NEOX_UNIT_SCALE, '--gravity =', gravity / NEOX_UNIT_SCALE)
                    self.send_event('E_CHARACTER_ATTR', 'animator_info_for_duration', 1)
                    print('test--_begin_normal_jump_up--jump_up_duration =', jump_up_duration, '--time_scale =', time_scale, '--verticalVelocity =', character.verticalVelocity / NEOX_UNIT_SCALE, '--gravity =', character.getGravity() / NEOX_UNIT_SCALE)
                root_node = animator.find(animation_const.JUMP_ROOT_NODE_NAME)
                root_node.timeScale = time_scale
                self.send_event('E_JUMP_ANIM_TIME_SCALE', time_scale)

    def _end_jump_up(self, arg, node_name):
        animator = self.ev_g_animator()
        if not animator:
            return
        source_node = animator.find(node_name)
        if not source_node or not source_node.IsWillActiveInHierarchy():
            return
        if self._enable_all_log:
            print('test--_end_jump_up--node_name =', node_name, '--arg =', arg)
        if not self.ev_g_is_jump():
            return
        self._end_normal_jump_up()

    def _end_normal_jump_up(self, *args):
        character = self.sd.ref_character
        if character:
            character.verticalVelocity = 0
        self.send_event('E_RESET_GRAVITY')
        if not self.ev_g_is_jump():
            return
        self.send_event('E_CHANGE_JUMP_STATE', animation_const.JUMP_STATE_IN_AIR)

    def begin_jump_fall_ground(self, arg, node_name):
        if self._jump_state != animation_const.JUMP_STATE_FALL_GROUND:
            return
        animator = self.ev_g_animator()
        if not animator:
            return
        if self._enable_all_log:
            print('test--begin_jump_fall_ground--step1--node_name =', node_name, '--arg =', arg)
        animation_node = animator.find(node_name)
        if not animation_node:
            return
        if self._enable_all_log:
            print('test--begin_jump_fall_ground--step2--node_name =', node_name, '--arg =', arg)
        fall_on_ground_type = self.ev_g_fall_on_ground_type()
        action_key = 'jump_stage_3'
        if fall_on_ground_type == animation_const.FALL_ON_GROUND_HIGH_SPEED:
            action_key = 'jump_stage_3_large'
        self.replace_jump_clip(animation_node, action_key)
        duration = 0
        if animation_const.BLEND_NODE_TYPE in animation_node.nodeType:
            duration = animation_node.duration
            all_child_states = animation_node.GetChildStates()
            one_child_state = all_child_states[-1]
            one_source_node = one_child_state.childNode
            duration = one_source_node.duration
        else:
            duration = animation_node.duration
        if self._enable_all_log:
            print('test--begin_jump_fall_ground--node_name =', node_name, '--duration =', animation_node.duration)
            if duration > 1:
                self.send_event('E_CHARACTER_ATTR', 'animator_info', True)
        self.send_event('E_SET_JUMP_RECOVER_TIME', duration)

    def on_action_ground_finish(self):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ON_GROUND_FINISH, ()], True)