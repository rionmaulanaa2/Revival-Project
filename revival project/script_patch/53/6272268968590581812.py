# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/character_action_utils.py
from __future__ import absolute_import
from __future__ import print_function
import logic.gcommon.common_const.robot_animation_const as robot_animation_const
import game3d
import logic.gcommon.cdata.status_config as status_config
import data.weapon_action_config as weapon_action_config
import data.weapon_action_blend_config as weapon_action_blend_config
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_const.character_anim_const import *
import world

def __get_move_info_from_rock_or_keyboard(self):
    rocker_ui = global_data.ui_mgr.get_ui('MoveRockerUI')
    if rocker_ui:
        rocker_ui.check_run_lock()
    move_dir = None
    move_state = None
    if rocker_ui and (rocker_ui.is_run_lock or rocker_ui.is_rocker_enable):
        move_dir = rocker_ui.last_move_dir
        move_state = rocker_ui.last_move_state
    return (
     move_dir, move_state)


if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_android_pc or global_data.is_mumu_pc_control:

    def _get_move_info_from_rock_or_keyboard(self):
        move_dir, move_state = __get_move_info_from_rock_or_keyboard(self)
        ctrl_part = global_data.moveKeyboardMgr
        if ctrl_part and ctrl_part.last_move_dir:
            if not move_dir or move_dir.length == 0:
                return (ctrl_part.last_move_dir, ctrl_part.last_move_state)
        return (move_dir, move_state)


else:
    _get_move_info_from_rock_or_keyboard = __get_move_info_from_rock_or_keyboard

def convert_human_jump_anim(self, anim_name):
    if self.ev_g_get_state(status_config.ST_SKATE):
        anim_name = 'skate_' + anim_name
    elif self.ev_g_get_state(status_config.ST_EMPTY_HAND):
        anim_name = 'emptyhand_' + anim_name
    return anim_name


HUMAN_SLOW_DOWN_STATE = set([status_config.ST_SHOOT, status_config.ST_RIGHT_AIM, status_config.ST_AIM, status_config.ST_RELOAD, status_config.ST_RELOAD_LOOP, status_config.ST_LOAD, status_config.ST_SWITCH_WP_MODE, status_config.ST_USE_ITEM, status_config.ST_WEAPON_ACCUMULATE])
STATIC_STATE = (
 status_config.ST_STAND, status_config.ST_CROUCH, status_config.ST_TURN, status_config.ST_MECHA_PASSENGER, status_config.ST_VEHICLE_GUNNER, status_config.ST_VEHICLE_PASSENGER)
STAND_STATE = set([status_config.ST_STAND, status_config.ST_MOVE, status_config.ST_RUN])
CROUCH_STATE = set([status_config.ST_CROUCH, status_config.ST_CROUCH_MOVE, status_config.ST_CROUCH_RUN])
JUMP_STATE = set([status_config.ST_JUMP_1, status_config.ST_JUMP_2, status_config.ST_JUMP_3])
MOVE_STATE = set([status_config.ST_MOVE, status_config.ST_RUN, status_config.ST_CROUCH_MOVE, status_config.ST_CROUCH_RUN])

def is_stand(state):
    if not state:
        return False
    else:
        if isinstance(state, int):
            return state in STAND_STATE
        state = set(state)
        return state & STAND_STATE


def is_crouch(state):
    if not state:
        return False
    else:
        if isinstance(state, int):
            return state in CROUCH_STATE
        state = set(state)
        return state & CROUCH_STATE


def is_jump(state):
    if not state:
        return False
    else:
        if isinstance(state, int):
            return state in JUMP_STATE
        state = set(state)
        return state & JUMP_STATE


def get_idle_clip(self, status, old_clip_name=None):
    weapon_type = self.ev_g_weapon_type()
    weapon_config = weapon_action_config.weapon_type_2_action.get(weapon_type, None)
    if not weapon_config:
        print('[Error] weapon_type =', weapon_type, '--do not have weapon action')
        import traceback
        traceback.print_stack()
        return
    else:
        is_shoot = self.ev_g_action_is_shoot()
        if self.ev_g_is_jump() or status in JUMP_STATE:
            is_shoot = 1
        crouch_data = {}
        action_key = 'idle'
        if status in CROUCH_STATE:
            action_key = 'crouch_idle'
            crouch_data['anim_name'] = 'c_ak_stop'
        if is_shoot:
            crouch_data = None
            action_key = 'aim_' + action_key
        if self.ev_g_get_state(status_config.ST_SKATE):
            crouch_data = None
            skate_action_key = 'skate_' + action_key
            clip_list = self.ev_g_weapon_action_list(skate_action_key)
            if clip_list:
                action_key = skate_action_key
        idle_clip_list = weapon_config[action_key]
        if not idle_clip_list:
            idle_clip_list = weapon_action_config.weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][action_key]
        if not idle_clip_list:
            idle_clip_list = weapon_action_config.weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL]['idle']
        blend_out_time = 0.2
        clip_name = ''
        if status in STATIC_STATE:
            clip_name = idle_clip_list[-1]
        else:
            clip_name = idle_clip_list[0]
        if old_clip_name != clip_name and is_shoot == 0:
            blend_out_time = 0.3
        if self.ev_g_get_state(status_config.ST_MECHA_DRIVER):
            clip_name = self.ev_g_mecha_driver_idle_anim()
            blend_out_time = 0.2
        return (
         clip_name, blend_out_time, crouch_data)


def get_human_animation_by_key(self, action_key):
    weapon_type_2_action = weapon_action_config.weapon_type_2_action
    weapon_type = self.ev_g_weapon_type()
    action_config = weapon_type_2_action.get(weapon_type, None)
    if not action_config:
        return
    else:
        clip_list = action_config[action_key]
        if not clip_list:
            clip_list = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][action_key]
        return clip_list


def get_human_blend_type_by_key(self, action_key):
    weapon_type_2_action_blend = weapon_action_blend_config.weapon_type_2_action_blend
    weapon_type = self.ev_g_weapon_type()
    action_config = weapon_type_2_action_blend.get(weapon_type, None)
    if not action_config:
        return 0
    else:
        return action_config[action_key]


def change_human_walk_animation(self, action_key, part=LOW_BODY, **kwargs):
    use_cache_pos = kwargs.get('use_cache_pos', False)
    clip_list = get_human_animation_by_key(self, action_key)
    clip_len = len(clip_list)
    clip_name = clip_list[-1]
    if clip_len == 4 or clip_len == 6:
        clip_name = clip_name[:-2]
    self.send_event('E_POST_ACTION', clip_name, part, clip_len, loop=True, blend_time=0.2, keep_phase=True, use_cache_pos=use_cache_pos)
    if self.ev_g_get_state(status_config.ST_SKATE):
        self.send_event('E_CHANGE_SKATE_MOVE')


def change_human_4_dir_run_animation(self, action_key, loop=True):
    clip_list = get_human_animation_by_key(self, action_key)
    clip_len = len(clip_list)
    clip_name = clip_list[-1]
    if clip_len == 4:
        clip_name = clip_name[:-2]
    dir_type = 4
    yaw_list = [-1.57, 1.57, 0, 0]
    self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=loop, blend_time=0, keep_phase=False, yaw_list=yaw_list, ignore_sufix=True, use_cache_pos=True, cache_pos_blend_time=0.2)


def set_special_model_transparent_state(self, enter_transparent):
    from common.cfg import confmgr
    if not self.sd.ref_sfx_origin_alpha_percent:
        self.sd.ref_sfx_origin_alpha_percent = {}
    skin_info = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.sd.ref_dressed_clothing_id), default={})
    if skin_info.get('special_transparent_sockets', None):
        transparent_info = skin_info.get('special_transparent_sockets', None)
        model = self.ev_g_model()
        if model and model.valid:
            socket_list = transparent_info['socket_list']
            if enter_transparent:
                if not self.sd.ref_special_socket_opacity_states:
                    for i in range(len(socket_list)):
                        if model.has_socket(socket_list[i]):
                            socket_models = model.get_socket_objects(socket_list[i])
                            if socket_models:
                                for socket_model in socket_models:
                                    if type(socket_model) == world.model:
                                        self.send_event('E_FORCE_ENTER_MODEL_OPACITY', socket_model, transparent_info['alpha'][i])
                                    else:
                                        self.sd.ref_sfx_origin_alpha_percent[str(socket_model)] = socket_model.alpha_percent
                                        socket_model.alpha_percent *= transparent_info['alpha'][i]

                self.sd.ref_special_socket_opacity_states.add(self.sid)
            else:
                self.sd.ref_special_socket_opacity_states.discard(self.sid)
                if not self.sd.ref_special_socket_opacity_states:
                    for i in range(len(socket_list)):
                        if model.has_socket(socket_list[i]):
                            socket_models = model.get_socket_objects(socket_list[i])
                            if socket_models:
                                for socket_model in socket_models:
                                    if type(socket_model) == world.model:
                                        self.send_event('E_FORCE_LEAVE_MODEL_OPACITY', socket_model)
                                    else:
                                        socket_model.alpha_percent = self.sd.ref_sfx_origin_alpha_percent.get(str(socket_model), 1.0)

    return