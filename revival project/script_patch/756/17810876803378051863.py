# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/WeaponLogic10011.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import math3d
import world
import math
from .StateBase import StateBase
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.component.client.com_character_ctrl.ComAnimMgr import DEFAULT_ANIM_NAME
import time
import weakref
import data.weapon_action_config as weapon_action_config
import logic.gcommon.common_const.animation_const as animation_const
from common.cfg import confmgr
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const import weapon_const
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.framework import Functor
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_utils import parachute_utils
import common.utils.timer as timer
import logic.gcommon.const as const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils import model_utils
from logic.gutils import weapon_skin_utils
import logic.gcommon.component.client.com_human_appearance.WeaponAction as WeaponAction
from logic.gutils import character_action_utils
from common.utils import scale_timer
KAIHUO_BIND_POINT = 'kaihuo'
RIGHT_BULLET_BIND_POINT = 'bullet'
LEFT_BULLET_BIND_POINT = 'left_bullet'
STATIC_ACTION = (
 animation_const.MOVE_STATE_STAND, animation_const.MOVE_STATE_TURN_LEFT, animation_const.MOVE_STATE_TURN_RIGHT)

def _play_weapon_bullet_sfx(self, weapon_pos, socket, sync=False):
    obj_weapon = self.sd.ref_wp_bar_cur_weapon
    conf = confmgr.get('firearm_res_config', str(obj_weapon.get_item_id()))
    sfx_bullet = conf.get('cSfxBullet', None)
    if sfx_bullet:
        delay_interval = conf.get('fSfxBulletDelay', 0.0)

        def func--- This code section failed: ---

  48       0  BUILD_MAP_1           1 
           3  LOAD_DEREF            1  'socket'
           6  BUILD_LIST_1          1 
           9  LOAD_DEREF            0  'sfx_bullet'
          12  STORE_MAP        
          13  STORE_FAST            0  'bullet_effect'

  49      16  LOAD_DEREF            2  'self'
          19  LOAD_ATTR             0  'send_event'
          22  LOAD_CONST            1  'E_CREATE_GUN_MODEL_EFFECT'
          25  LOAD_DEREF            3  'weapon_pos'
          28  LOAD_DEREF            2  'self'
          31  LOAD_DEREF            4  'sync'
          34  CALL_FUNCTION_259   259 
          37  POP_TOP          

Parse error at or near `CALL_FUNCTION_259' instruction at offset 34

        if delay_interval > 0.0:
            global_data.game_mgr.register_logic_timer(func, interval=delay_interval, times=1, mode=timer.CLOCK)
        else:
            func()
    return


def update_bone_tree(self):
    if not self.is_active:
        return
    subtree = animation_const.ENABLE_UP_BODY_BONE
    self.send_event('E_UPBODY_BONE', subtree)


def _decide_single_or_blend_clip(self, action_key, action_id, loop=False, scale_time=None, phase=0, use_single=False, blend_time=0.2, do_post=True):
    default_action_key = action_key
    if isinstance(action_key, (list, tuple)):
        default_action_key = action_key[0]
        select_action_key = None
        if len(action_key) > 2:
            if self.ev_g_is_jump():
                select_action_key = action_key[2]
        if not select_action_key:
            if self.ev_g_is_crouch():
                crouch_action_key = action_key[1]
                clip_list = self.ev_g_weapon_action_list(crouch_action_key)
                if clip_list:
                    select_action_key = crouch_action_key
        if not select_action_key:
            select_action_key = action_key[0]
        if self.ev_g_get_state(status_config.ST_SKATE):
            skate_action_key = 'skate_' + select_action_key
            clip_list = self.ev_g_weapon_action_list(skate_action_key)
            if clip_list:
                select_action_key = skate_action_key
        action_key = select_action_key
    weapon_type_2_action = weapon_action_config.weapon_type_2_action
    action_config = weapon_type_2_action.get(action_id, None)
    if not action_config:
        return
    else:
        clip_list = action_config[action_key]
        if not clip_list:
            clip_list = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][default_action_key]
        time_scale = 1
        if scale_time:
            anim_time = self.ev_g_get_anim_length(clip_list[0])
            time_scale = anim_time / scale_time
        return_clip_list = []
        if len(clip_list) > 1 and not use_single:
            if len(clip_list) == 2:
                move_action = self.ev_g_move_state()
                if move_action in STATIC_ACTION:
                    clip_name = clip_list[1]
                else:
                    clip_name = clip_list[0]
                return_clip_list.append(clip_name)
                if do_post:
                    self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=loop, blend_time=blend_time, phase=phase, timeScale=time_scale)
            else:
                dir_type = len(clip_list)
                clip_name = clip_list[-1]
                return_clip_list = clip_list
                if do_post:
                    self.send_event('E_POST_ACTION', clip_name, UP_BODY, dir_type, loop=loop, blend_time=blend_time, phase=phase, timeScale=time_scale)
        else:
            clip_name = clip_list[-1]
            return_clip_list.append(clip_name)
            dir_type = 1
            if do_post:
                self.send_event('E_POST_ACTION', clip_name, UP_BODY, dir_type, loop=loop, blend_time=blend_time, phase=phase, timeScale=time_scale)
        if do_post:
            update_bone_tree(self)
        self.send_event('E_CHANGE_WEAPON_ANIMATION', list(return_clip_list), False, loop, time_scale)
        return return_clip_list


def common_enter_states(self, new_state, crouch_callback=None, jump_callback=None):
    if character_action_utils.is_jump(new_state):
        update_bone_tree(self)
        if jump_callback:
            jump_callback()
    elif character_action_utils.is_crouch(new_state):
        if crouch_callback:
            crouch_callback()


def common_leave_states(self, leave_state, new_state, crouch_callback=None, jump_callback=None):
    if character_action_utils.is_jump(leave_state) and not character_action_utils.is_jump(new_state):
        update_bone_tree(self)
        if jump_callback:
            jump_callback()
    elif character_action_utils.is_crouch(leave_state) and not character_action_utils.is_crouch(new_state):
        if crouch_callback:
            crouch_callback()


class HumanSwitchWeapon(StateBase):
    BIND_EVENT = {'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_ACTION_SWITCHING': '_begin_switch_gun',
       'G_IS_GUN_POS': '_is_gun_pos',
       'E_UNBIND_ALL_WEAPON': '_unbind_all_weapon',
       'E_ANIM_MGR_INIT': 'on_anim_mgr_init',
       'E_WEAPON_DATA_DELETED': '_put_off_gun',
       'E_REEQUIP_WEAPON': 'reequip_weapon',
       'E_CHECK_REEQUIP_WEAPON': 'check_reequip_weapon',
       'E_SHOW_ALL_GUN': 'show_all_gun',
       'E_HIDE_ALL_GUN': 'hide_all_gun',
       'G_IS_ACTION_ENABLE_HAND_IK': 'is_action_enable_hand_ik',
       'G_IS_FIX_EQUIP_POS': 'is_fix_equip_pos',
       'E_WPBAR_INIT': '_check_weapon_bar_cur_weapon',
       'E_OPEN_PARACHUTE': ('on_open_parachute', 1),
       'E_LAND': ('on_land', 1),
       'G_WEAPON_ACTION_LIST': 'get_weapon_action_list',
       'E_DECIDE_GUN_VISIBLE': '_decide_gun_visibility',
       'E_EQUIP_GUN_BY_POS': '_equip_gun_by_pos',
       'E_NOTIFY_MOVE_STATE_CHANGE': 'change_switch_animation',
       'E_FINISH_SWITCH_GUN': '_end_switch_gun',
       'E_ACTION_END_SWITCH': '_stop_switch_gun',
       'E_CREATE_TEST_GUN': 'create_test_gun',
       'E_TEST_GUN_ANIMATION': 'test_gun_animation',
       'G_IS_SHOW_GUN': 'is_show_gun',
       'G_GUN_BIND_POINT': 'get_gun_bind_point_list'
       }
    CLIP_EVENT_TIME = {}
    NEED_BIND_WEAPON_SKATE_STATE = set([status_config.ST_SKATE_MOVE, status_config.ST_SKATE_BRAKE, status_config.ST_SKATE])
    SWITCH_WEAPON_ACTION = set([animation_const.HAND_STATE_GET_NEW_GUN])
    FAST_SWITCH_WEAPON_ACTION_TYPE = set([animation_const.WEAPON_TYPE_SHRAPNEL])

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanSwitchWeapon, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.new_weapon_pos = const.PART_WEAPON_POS_NONE
        self.cur_weapon_action = None
        self._registed_switch_gun_delay = None
        self._switch_gun_state = {}
        self.weapon_model_task_ids = {}
        self._anim_duration = 0
        self._all_timer_ids = []
        self._delay_switch_info = None
        self._gun_bind_point_list = [None, None]
        self._gun_visible_state = {animation_const.WEAPON_POS_LEFT: True,animation_const.WEAPON_POS_RIGHT: True}
        return

    def on_anim_mgr_init(self):
        weapon_pos = self.sd.ref_wp_bar_cur_pos or 0
        if weapon_pos > 0:
            self._end_switch_gun(weapon_pos)
        self.send_event('E_ACTION_SET_EMPTY_HAND', weapon_pos == 0)
        self._register_switch_weapon_event()

    def _enter_states(self, new_state):
        if new_state in self.NEED_BIND_WEAPON_SKATE_STATE:
            self.rebind_all_weapon(True)
        common_enter_states(self, new_state, self.change_switch_animation)

    def _leave_states(self, leave_state, new_state=None):
        if leave_state == status_config.ST_SKATE:
            self.send_event('E_CHANGE_WEAPON_IDLE')
        if leave_state in self.NEED_BIND_WEAPON_SKATE_STATE:
            if self.ev_g_is_in_any_state(self.NEED_BIND_WEAPON_SKATE_STATE):
                self.rebind_all_weapon(True)
            else:
                self.rebind_all_weapon(False)
        elif leave_state == self.sid:
            self.leave_switch()
        common_leave_states(self, leave_state, new_state, self.change_switch_animation)

    def _change_character_attr(self, name, *arg):
        if name == 'weapon_info' or name == 'animator_info':
            import world
            bullet_bind_point = None
            weapon_obj = self.sd.ref_wp_bar_cur_weapon
            if weapon_obj:
                weapon_id = weapon_obj.get_item_id()
                weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
                if weapon_res_def:
                    bullet_bind_point = weapon_res_def['cBindPointBullet']
            right_weapon = self.sd.ref_hand_weapon_model
            right_weapon_visible = False
            cur_right_anim_time = 0
            cur_right_anim_length = 0
            cur_right_anim_name = ''
            cur_right_is_playing = False
            right_weapon_anim_name = ''
            bullets_model = None
            right_model_file_list = []
            if right_weapon:
                right_weapon_visible = right_weapon.visible
                right_weapon_anim_ctrl = right_weapon.get_anim_ctrl(world.ANIM_TYPE_SKELETAL)
                cur_right_anim_time = right_weapon_anim_ctrl.anim_time
                cur_right_anim_length = right_weapon_anim_ctrl.anim_length
                cur_right_anim_name = right_weapon.cur_anim_name
                right_weapon_anim_name = right_weapon.cur_anim_name
                cur_right_is_playing = right_weapon_anim_ctrl.is_playing
                right_model_file_list.append(right_weapon.filename)
                mesh_count = right_weapon.get_submesh_count()
                if hasattr(right_weapon, 'get_submesh_filename'):
                    for mesh_idx in range(0, mesh_count):
                        file_name = right_weapon.get_submesh_filename(mesh_idx)
                        right_model_file_list.append(file_name)

                if bullet_bind_point:
                    bullets_model = model_utils.get_socket_objects(right_weapon, bullet_bind_point)
            left_weapon = self.sd.ref_left_hand_weapon_model
            left_weapon_visible = False
            left_weapon_anim_name = ''
            left_model_file_list = []
            if left_weapon:
                left_weapon_visible = left_weapon.visible
                left_weapon_anim_name = left_weapon.cur_anim_name
                left_model_file_list.append(left_weapon.filename)
                mesh_count = left_weapon.get_submesh_count()
                if hasattr(left_weapon, 'get_submesh_filename'):
                    for mesh_idx in range(0, mesh_count):
                        file_name = left_weapon.get_submesh_filename(mesh_idx)
                        left_model_file_list.append(file_name)

            weapon_obj = self.sd.ref_wp_bar_cur_weapon
            weapon_id = 0
            if weapon_obj:
                weapon_id = weapon_obj.get_item_id()
            action_id = self.ev_g_weapon_action_id()
            weapon_pos = self.sd.ref_wp_bar_cur_pos
            print('test--HumanSwitchWeapon--weapon_info--ev_g_is_can_fire =', self.ev_g_is_can_fire(), '--is_shoot -', self.ev_g_action_is_shoot(), '--weapon_pos =', weapon_pos, '--weapon_id =', weapon_id, '--action_id =', action_id, '--right_weapon =', right_weapon, '--right_model_file_list =', right_model_file_list, '--right_weapon_visible =', right_weapon_visible, '--left_weapon =', left_weapon, '--left_model_file_list =', left_model_file_list, '--left_weapon_visible =', left_weapon_visible, '--right_weapon_anim_name =', right_weapon_anim_name, '--left_weapon_anim_name =', left_weapon_anim_name)
        elif name == 'weapon_action_info':
            print(('test--HumanSwitchWeapon--weapon_action_info--self.cur_weapon_action =', self.cur_weapon_action))
        elif name == 'do_not_reset_camera_on_fire':
            from logic.comsys.control_ui.ShotChecker import ShotChecker
            do_not_reset_camera_on_fire = bool(arg[0])
            ShotChecker().do_not_reset_camera_on_fire = do_not_reset_camera_on_fire
            print('test--do_not_reset_camera_on_fire =', do_not_reset_camera_on_fire)
        return

    def _register_switch_weapon_event(self):
        if self.CLIP_EVENT_TIME:
            return
        is_two_hand = 0
        all_hand_pos = [animation_const.PUT_ON_RIGHT_POS_GUN]
        all_trigger_name = [animation_const.RIGHT_WEAPON_TRIGGER]
        self._register_one_weapon_switch_event(is_two_hand, all_hand_pos, all_trigger_name)
        is_two_hand = 1
        all_hand_pos = (animation_const.PUT_ON_LEFT_POS_GUN, animation_const.PUT_ON_RIGHT_POS_GUN)
        all_trigger_name = (animation_const.LEFT_WEAPON_TRIGGER, animation_const.RIGHT_WEAPON_TRIGGER)
        self._register_one_weapon_switch_event(is_two_hand, all_hand_pos, all_trigger_name)

    def _register_one_weapon_switch_event(self, is_two_hand, all_hand_pos, all_trigger_name):
        model = self.ev_g_model()
        if not model:
            print('test--_register_one_weapon_switch_event--model=None')
            import traceback
            traceback.print_stack()
            return
        all_change_key = ('get_new_gun', 'skate_get_new_gun', 'crouch_get_new_gun')
        all_anims = set()
        for one_config in six_ex.values(weapon_action_config.weapon_type_2_action):
            if is_two_hand != one_config['is_two_hand']:
                continue
            for one_key in all_change_key:
                if one_config[one_key]:
                    all_anims.add(one_config[one_key])

        for clip_list in all_anims:
            one_clip_list = clip_list
            if len(clip_list) > 2:
                one_clip_list = [
                 clip_list[-1]]
            clip_name = weapon_action_config.get_main_anim(one_clip_list[-1])
            for index, trigger_name in enumerate(all_trigger_name):
                event_time = model.get_anim_event_time(clip_name, trigger_name) / 1000.0
                data = all_hand_pos[index]
                self.CLIP_EVENT_TIME.setdefault(clip_name, []).append((data, event_time))

    def is_show_gun(self):
        control_target = self.ev_g_control_target()
        if control_target and control_target.logic:
            if control_target.logic.__class__.__name__ == 'LMotorcycle':
                seat_index = control_target.logic.ev_g_passenger_seat_index(self.unit_obj.id)
                return seat_index == 2
            else:
                return False

        return True

    def add_gun_bind_point(self, bind_point):
        self._gun_bind_point_list.append(bind_point)
        self._gun_bind_point_list.pop(0)

    def get_gun_bind_point_list(self):
        return self._gun_bind_point_list

    def enter(self, leave_states):
        super(HumanSwitchWeapon, self).enter(leave_states)
        self.send_event('E_KEEP_SHOOT_TIME', 0)
        self.send_event('E_ACTION_IS_SHOOT', 0)

    def leave_switch(self):
        for timer_id in self._all_timer_ids:
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self._all_timer_ids = []
        self.send_event('E_EXIT_WEAPON_ACTION')
        if self.cur_weapon_action and self.cur_weapon_action.TYPE in self.SWITCH_WEAPON_ACTION:
            self.cur_weapon_action.exit()
        self.cur_weapon_action = None
        self.show_all_gun()
        if self.ev_g_get_state(status_config.ST_CROUCH):
            clip_name, _, crouch_data = character_action_utils.get_idle_clip(self, status_config.ST_CROUCH)
            if crouch_data:
                self.send_event('E_POST_ACTION', crouch_data['anim_name'], LOW_BODY, 1, loop=True)
                self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=True)
        return

    def exit(self, enter_states):
        super(HumanSwitchWeapon, self).exit(enter_states)

    def get_weapon_action_list(self, action_key):
        weapon_type_2_action = weapon_action_config.weapon_type_2_action
        action_id = self.ev_g_weapon_action_id()
        action_config = weapon_type_2_action.get(action_id, None)
        if not action_config:
            action_config = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL]
        clip_list = action_config.get(action_key, None)
        if not clip_list:
            clip_list = weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL].get(action_key, None)
        return clip_list

    def _check_weapon_bar_cur_weapon(self, *args):
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        if weapon_pos > 0:
            self.cur_weapon_action = None
            self._end_switch_gun(weapon_pos)
        return

    def is_fix_equip_pos(self, weapon_pos):
        weapon_obj = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon_obj:
            return (True, animation_const.WEAPON_POS_RIGHT)
        equip_pos = weapon_pos
        weapon_id = weapon_obj.get_item_id()
        is_fix_pos = False
        weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
        if weapon_res_def['cBindPointLeft']:
            equip_pos = animation_const.WEAPON_POS_LEFT
            is_fix_pos = True
        elif weapon_res_def['cBindPoint']:
            equip_pos = animation_const.WEAPON_POS_RIGHT
            is_fix_pos = True
        return (
         is_fix_pos, equip_pos)

    def _is_gun_pos(self, pos):
        return pos in const.MAIN_WEAPON_LIST

    def _is_two_hand_weapon(self, pos):
        if self._is_gun_pos(pos):
            weapon_obj = self.sd.ref_wp_bar_mp_weapons.get(pos)
            if not weapon_obj:
                return False
            weapon_id = weapon_obj.get_item_id()
            weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
            if not weapon_res_def:
                return False
            return self.get_left_weapon_bind_point(weapon_res_def) and self.get_right_weapon_bind_point(weapon_res_def)
        return False

    def change_switch_animation(self):
        if not self.is_active:
            return
        if not self.cur_weapon_action:
            return
        self.play_switch_animation(self.cur_weapon_action, is_reset=False)

    def play_switch_animation(self, weapon_action, is_reset=True):
        weapon_id = weapon_action.weapon_id
        action_id = confmgr.get('firearm_res_config', str(weapon_id), 'iActionType')
        action_key = ('get_new_gun', 'crouch_get_new_gun')
        weapon_obj = self.cur_weapon_action.weapon_data
        if weapon_obj:
            take_tiime = weapon_obj.get_effective_value('fTakeTime')
        else:
            print('test--play_switch_animation--[error]--weapon_obj None')
        phase = 0
        if not is_reset:
            phase = 0
            if self._anim_duration > 0:
                phase = self.sub_sid_timer / self._anim_duration
            phase = min(phase, 1)
            if self.sub_sid_timer >= self._anim_duration:
                self._do_end_get_new_weapon()
                return
        take_time_factor = self.ev_g_attr_get('weapon_take_time_factor', 0)
        scale_action_time = (0.9 + take_time_factor) * take_tiime
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, scale_time=scale_action_time, phase=phase)
        if action_id in self.FAST_SWITCH_WEAPON_ACTION_TYPE:
            self.send_event('E_SET_SMOOTH_SPEED', UP_BODY, 0)
        if action_id == animation_const.WEAPON_TYPE_GRENADE:
            self.send_event('E_CHANGE_WEAPON_IDLE')
        main_clip = weapon_action_config.get_main_anim(clip_list[-1])
        event_list = self.CLIP_EVENT_TIME.get(main_clip, [])
        if not event_list:
            print(('test--play_switch_animation--error--event_list empty--weapon_id =', weapon_id, '--action_id =', action_id, '--clip_list =', clip_list))
            print(('test--play_switch_animation--error--CLIP_EVENT_TIME =', self.CLIP_EVENT_TIME))
            import traceback
            traceback.print_stack()
            return
        for timer_id in self._all_timer_ids:
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self._all_timer_ids = []
        if is_reset:
            for one_event_info in event_list:
                data, event_time = one_event_info
                timer_id = global_data.game_mgr.register_logic_timer(Functor(self._switch_gun_callback, data), event_time, times=1, mode=timer.CLOCK)
                self._all_timer_ids.append(timer_id)

        else:
            for one_event_info in event_list:
                data, event_time = one_event_info
                state = self._switch_gun_state.get(data, 0)
                if not state:
                    if self.sub_sid_timer >= event_time:
                        self._switch_gun_callback(data)
                    else:
                        timer_id = global_data.game_mgr.register_logic_timer(Functor(self._switch_gun_callback, data), event_time, times=1, mode=timer.CLOCK)
                        self._all_timer_ids.append(timer_id)

        end_time = scale_action_time
        if not end_time:
            end_time = self.ev_g_get_anim_length(main_clip)
        end_time = end_time or 0.01
        self._anim_duration = end_time
        timer_id = global_data.game_mgr.register_logic_timer(self._do_end_get_new_weapon, end_time, times=1, mode=timer.CLOCK)
        self._all_timer_ids.append(timer_id)

    def _do_end_get_new_weapon(self, *args):
        old_weapon_pos = const.PART_WEAPON_POS_NONE
        old_weapon_action = self.cur_weapon_action
        if self.cur_weapon_action:
            self.cur_weapon_action.exit()
            self.cur_weapon_action = None
        self.send_event('E_SET_HAND_IK')
        return

    def delay_begin_switch_gun(self):
        new_weapon_pos = self._delay_switch_info['new_weapon_pos']
        old_weapon_pos = self._delay_switch_info['old_weapon_pos']
        self._begin_switch_gun(new_weapon_pos, old_weapon_pos)
        self._delay_switch_info = None
        self.unit_obj.unregist_event('E_QUIT_AIM', self.delay_begin_switch_gun)
        return

    def _begin_switch_gun(self, new_weapon_pos, old_weapon_pos=None):
        for one_pos in six_ex.keys(self.weapon_model_task_ids):
            self.weapon_model_cancle_load_task(one_pos)

        for timer_id in self._all_timer_ids:
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self._all_timer_ids = []
        if not self.ev_g_get_state(self.sid):
            if not self.ev_g_status_try_trans(self.sid):
                self._end_switch_gun(new_weapon_pos)
                return
        is_in_aim = self.sd.ref_in_aim
        if is_in_aim:
            if self._delay_switch_info:
                self.unit_obj.unregist_event('E_QUIT_AIM', self.delay_begin_switch_gun)
            self._delay_switch_info = {'new_weapon_pos': new_weapon_pos,'old_weapon_pos': old_weapon_pos}
            self.unit_obj.regist_event('E_QUIT_AIM', self.delay_begin_switch_gun)
            return
        else:
            new_obj_weapon = self.sd.ref_wp_bar_mp_weapons.get(new_weapon_pos)
            old_obj_weapon = self.sd.ref_wp_bar_mp_weapons.get(old_weapon_pos)
            if not new_obj_weapon:
                if not old_obj_weapon:
                    put_off_action = WeaponAction.ImmediatePutOffWeaponAction(0, new_weapon_pos, self)
                    if self.cur_weapon_action:
                        self.cur_weapon_action.exit()
                        self.cur_weapon_action = None
                    put_off_action.enter()
                    self.send_event('E_ACTION_SET_EMPTY_HAND', True)
                    return
            now_get_new_weapon_action = None
            new_weapon_id = 0
            if new_obj_weapon:
                new_weapon_id = new_obj_weapon.get_item_id()
                now_get_new_weapon_action = WeaponAction.GetNewGunAction(new_weapon_id, new_weapon_pos, self)
            else:
                now_get_new_weapon_action = WeaponAction.ImmediatePutOffWeaponAction(0, new_weapon_pos, self)
            if self.cur_weapon_action:
                if now_get_new_weapon_action and now_get_new_weapon_action.weapon_id != self.cur_weapon_action.weapon_id:
                    self.cur_weapon_action.exit(False)
                    self.cur_weapon_action = None
            self._change_equip_weapon_info(new_weapon_pos)
            self._unbind_all_weapon()
            if now_get_new_weapon_action.TYPE == animation_const.HAND_STATE_NONE:
                now_get_new_weapon_action.enter()
            else:
                self.cur_weapon_action = now_get_new_weapon_action
            if self.cur_weapon_action:
                if self.cur_weapon_action.is_start_after_model_loaded():
                    self._bind_new_weapon(self.cur_weapon_action.TYPE)
                else:
                    self.start_switch_animation()
                self.cur_weapon_action.enter()
            self.send_event('E_ACTION_SET_EMPTY_HAND', not new_obj_weapon)
            return

    def _bind_new_weapon(self, hand_action):
        weapon_pos = self.new_weapon_pos
        if weapon_pos <= 0:
            return
        self._equip_gun_by_pos(weapon_pos, hand_action)

    def get_left_weapon_bind_point(self, weapon_res_def):
        bind_point = ''
        if self.ev_g_is_in_any_state(self.NEED_BIND_WEAPON_SKATE_STATE) or self.ev_g_get_state(status_config.ST_SKATE) and weapon_res_def['iActionType'] == animation_const.WEAPON_TYPE_SHIELD:
            bind_point = weapon_res_def['cSkateBindPointLeft']
        if bind_point:
            return bind_point
        return weapon_res_def['cBindPointLeft']

    def get_right_weapon_bind_point(self, weapon_res_def):
        bind_point = ''
        if self.ev_g_is_in_any_state(self.NEED_BIND_WEAPON_SKATE_STATE) or self.ev_g_get_state(status_config.ST_SKATE) and weapon_res_def['iActionType'] == animation_const.WEAPON_TYPE_SHIELD:
            bind_point = weapon_res_def['cSkateBindPoint']
        if bind_point:
            return bind_point
        return weapon_res_def['cBindPoint']

    def _equip_gun_by_pos(self, weapon_pos, hand_action=None):
        from logic.gutils import dress_utils
        if weapon_pos <= 0:
            self.equip_gun(None)
            return
        else:
            weapon_obj = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            if not weapon_obj:
                return
            weapon_id = weapon_obj.get_item_id()
            weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
            from logic.gutils.mode_utils import get_mapped_res_path
            left_res = weapon_res_def['cResLeft']
            right_res = get_mapped_res_path(weapon_res_def['cRes'])
            fashion = weapon_obj.get_fashion()
            fashion_id = fashion.get(FASHION_POS_SUIT, None)
            if fashion_id is not None:
                tmp_right_res, tmp_left_res = dress_utils.get_weapon_skin_res(fashion_id)
                if tmp_left_res is not None:
                    left_res = tmp_left_res
                if tmp_right_res is not None:
                    right_res = tmp_right_res
            bind_weapons = []
            if weapon_res_def['cBindPointLeft']:
                bind_weapons.append((left_res, self.get_left_weapon_bind_point(weapon_res_def), animation_const.WEAPON_POS_LEFT))
            if weapon_res_def['cBindPoint']:
                bind_weapons.append((right_res, self.get_right_weapon_bind_point(weapon_res_def), animation_const.WEAPON_POS_RIGHT))
            if not bind_weapons:
                bind_weapons.append((right_res, 'gun', animation_const.WEAPON_POS_RIGHT))
            for res_path, bind_point, hand_pos in bind_weapons:
                res_path = res_path.replace('h.gim', 'empty.gim')
                user_data = {'bind_point': bind_point,'pos': weapon_pos,'weapon_id': weapon_id,'hand_pos': hand_pos,'res_path': res_path,'up_body_action': hand_action}
                self.equip_gun(res_path, user_data)

            return

    def equip_gun(self, path='model/weapon/1001_ak.gim', cb_data=None):
        import game3d
        if cb_data is None:
            cb_data = {}
        pos = cb_data.get('hand_pos', animation_const.WEAPON_POS_RIGHT)
        if path:
            self.weapon_model_cancle_load_task(pos)
            self.weapon_model_task_ids[pos] = self.ev_g_load_model_task_id(path, self._gun_load_callback, cb_data, None, sync_priority=game3d.ASYNC_VERY_HIGH)
        else:
            self._gun_load_callback(None, None)
        return

    def create_test_gun(self):
        if self.sd.ref_left_hand_weapon_model:
            self.sd.ref_left_hand_weapon_model.destroy()
            self.sd.ref_left_hand_weapon_model = None
        if self.sd.ref_hand_weapon_model:
            self.sd.ref_hand_weapon_model.destroy()
            self.sd.ref_hand_weapon_model = None
        path = 'character/weapons/1001_ak/1001/test_ak.gim'
        gun_model = world.model(path, None)
        human_model = self.ev_g_model()
        bind_point = 'ak'
        human_model.bind(bind_point, gun_model)
        self.sd.ref_hand_weapon_model = gun_model
        gun_model.play_animation('test_ak')
        return

    def test_gun_animation(self):
        self.send_event('E_POST_ACTION', 'test_ak', UP_BODY, 1, loop=False)
        gun_model = self.sd.ref_hand_weapon_model
        gun_model.play_animation('s_ak_reload')

    def _gun_load_callback(self, gun_model, user_data):
        if not user_data:
            self._unbind_all_weapon()
            return
        else:
            if global_data.enable_other_model_shadowmap or self.unit_obj.__class__.__name__ == 'LAvatar':
                if gun_model and gun_model.valid:
                    gun_model.cast_shadow = True
            hand_pos = user_data.get('hand_pos', animation_const.WEAPON_POS_RIGHT)
            if hand_pos == animation_const.WEAPON_POS_LEFT:
                if self.sd.ref_left_hand_weapon_model:
                    self.sd.ref_left_hand_weapon_model.destroy()
                    self.sd.ref_left_hand_weapon_model = None
            else:
                if self.sd.ref_hand_weapon_model:
                    self.sd.ref_hand_weapon_model.destroy()
                    self.sd.ref_hand_weapon_model = None
                weapon_pos = user_data.get('pos', const.PART_WEAPON_POS_NONE)
                loaded_weapon_id = user_data.get('weapon_id', 0)
                now_weapon_id = 0
                new_obj_weapon = self.sd.ref_wp_bar_mp_weapons.get(self.new_weapon_pos)
                if new_obj_weapon:
                    now_weapon_id = new_obj_weapon.get_item_id()
                if weapon_pos != self.new_weapon_pos or loaded_weapon_id != now_weapon_id:
                    if gun_model:
                        gun_model.destroy()
                    return
            if gun_model:
                gun_model.receive_shadow = False
                if hand_pos == animation_const.WEAPON_POS_LEFT:
                    self.sd.ref_left_hand_weapon_model = gun_model
                else:
                    self.sd.ref_hand_weapon_model = gun_model
                bind_point = 'gun'
                res_path = ''
                hand_action = None
                weapon_id = 0
                if user_data:
                    bind_point = user_data.get('bind_point', 'gun')
                    res_path = user_data.get('res_path', '')
                    hand_action = user_data.get('up_body_action', None)
                    weapon_id = user_data.get('weapon_id', None)
                human_model = self.ev_g_model()
                if human_model:
                    weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
                    adjust_bind_point = ''
                    if hand_pos == animation_const.WEAPON_POS_RIGHT:
                        adjust_bind_point = self.get_right_weapon_bind_point(weapon_res_def)
                    elif hand_pos == animation_const.WEAPON_POS_LEFT:
                        adjust_bind_point = self.get_left_weapon_bind_point(weapon_res_def)
                    if adjust_bind_point:
                        bind_point = adjust_bind_point
                    human_model.bind(bind_point, gun_model)
                    self.add_gun_bind_point(bind_point)
                now_weapon = self.sd.ref_wp_bar_cur_weapon
                if now_weapon and now_weapon.get_kind() == weapon_const.WP_SPELL:
                    self.send_event('E_LOAD_FIRESTREAM_SFX', now_weapon)
                self.send_event('E_CHANGE_WEAPON_MODEL', gun_model, hand_pos, weapon_id)
                is_all_gun_loaded = True
                if self._is_two_hand_weapon(weapon_pos):
                    is_all_gun_loaded = self.sd.ref_hand_weapon_model and self.sd.ref_left_hand_weapon_model
                if is_all_gun_loaded:
                    if hand_action is not None:
                        self.start_switch_animation()
                    else:
                        self.send_event('E_CHANGE_WEAPON_IDLE')
                hand_action = self.ev_g_hand_action()
                if hand_action == animation_const.HAND_STATE_NONE:
                    self.send_event('E_CHANGE_WEAPON_IDLE')
                is_visible = True
                if self.ev_g_is_avatar():
                    if hand_action is None:
                        is_visible = True
                    elif self.cur_weapon_action:
                        is_visible = False
                    else:
                        is_visible = True
                is_visible = is_visible and self.sd.ref_parachute_stage != parachute_utils.STAGE_PARACHUTE_DROP and self._gun_visible_state.get(hand_pos, True)
                self._decide_gun_visibility(gun_model, is_visible)
            pos = const.PART_WEAPON_POS_NONE
            if user_data:
                pos = user_data.get('pos', const.PART_WEAPON_POS_NONE)
            self.send_event('E_GUN_MODEL_LOADED', gun_model, self.is_gun_enable_hand_ik(pos), hand_pos)
            return

    def start_switch_animation(self):
        if self.cur_weapon_action:
            self.cur_weapon_action.set_up_animator_param()
            self.play_switch_animation(self.cur_weapon_action)
        else:
            action_id = self.ev_g_weapon_action_id()
            self.send_event('E_SET_WEAPON_TYPE', action_id)
        self._switch_gun_state = {}

    def on_open_parachute(self, *args):
        self.on_parachute_stage_changed(False)

    def on_parachute_stage_changed(self, gun_model_visible):
        if gun_model_visible:
            self.show_all_gun()
        else:
            self.hide_all_gun()

    def on_land(self, *args):
        self.on_parachute_stage_changed(True)

    def is_gun_enable_hand_ik(self, weapon_pos):
        if self._is_gun_pos(weapon_pos) > 0:
            weapon_data = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            weapon_id = weapon_data.get_item_id()
            action_id = confmgr.get('firearm_res_config', str(weapon_id), 'iActionType')
            return self.is_action_enable_hand_ik(action_id)
        return False

    def is_action_enable_hand_ik(self, action_id):
        if global_data.cam_lplayer and self.unit_obj and global_data.cam_lplayer.id == self.unit_obj.id:
            return False
        else:
            action_enable = action_id not in (animation_const.WEAPON_TYPE_SHIELD, animation_const.WEAPON_TYPE_GRENADE, animation_const.WEAPON_TYPE_FLAMER,
             animation_const.WEAPON_TYPE_BAZOOKA, animation_const.WEAPON_TYPE_SHRAPNEL)
            if not action_enable:
                return False
            weapon_type = self.ev_g_weapon_type()
            ik_role_sockets = weapon_action_config.weapon_type_2_action.get(weapon_type, {}).get('ik_role_sockets', None)
            if ik_role_sockets == None:
                return False
            return True

    def _switch_gun_callback(self, data=None):
        hand_action = self.ev_g_hand_action()
        if hand_action not in (animation_const.HAND_STATE_GET_NEW_GUN,):
            return
        else:
            self._switch_gun_state[data] = 1
            weapon_pos = self.new_weapon_pos
            if weapon_pos > 0:
                put_on_weapon = None
                if self._is_two_hand_weapon(weapon_pos):
                    if data == animation_const.PUT_ON_LEFT_POS_GUN:
                        put_on_weapon = self.sd.ref_left_hand_weapon_model
                    elif data == animation_const.PUT_ON_RIGHT_POS_GUN:
                        put_on_weapon = self.sd.ref_hand_weapon_model
                else:
                    put_on_weapon = self.sd.ref_hand_weapon_model
                if put_on_weapon:
                    self._decide_gun_visibility(put_on_weapon, True)
            return

    def _decide_gun_visibility(self, gun_model, hint_visibile):
        if not gun_model:
            return
        model = self.ev_g_model()
        human_model_visibile = True
        if model:
            human_model_visibile = model.visible
        visible = hint_visibile
        if not human_model_visibile:
            visible = False
        gun_model.visible = visible
        self.send_event('E_DECIDE_IGNITION_VISIBLE', visible)

    def _end_switch_gun(self, weapon_pos):
        self.send_event('E_CLEAR_FIRESTREAM_SFX')
        self._unbind_all_weapon()
        self.send_event('E_ACTION_SET_EMPTY_HAND', weapon_pos == 0)
        if self.sd.ref_wp_bar_mp_weapons is not None:
            new_obj_weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        else:
            new_obj_weapon = None
        if self.cur_weapon_action:
            self.cur_weapon_action.exit()
            self.cur_weapon_action = None
        hand_action = self.ev_g_hand_action()
        if hand_action in self.SWITCH_WEAPON_ACTION:
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        if not new_obj_weapon:
            self.equip_gun(None)
            self.send_event('E_SET_HAND_IK')
            return
        else:
            new_weapon_id = new_obj_weapon.get_item_id()
            self._change_equip_weapon_info(weapon_pos)
            self._equip_gun_by_pos(weapon_pos)
            self.send_event('E_DECIDE_RELOAD_TYPE', weapon_pos, first_reload=True)
            if self._is_gun_pos(weapon_pos):
                action_id = confmgr.get('firearm_res_config', str(new_weapon_id), 'iActionType')
                self.send_event('E_SET_WEAPON_TYPE', action_id)
            else:
                import logic.gcommon.const as const
                if weapon_pos > const.PART_WEAPON_POS_NONE:
                    self.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_NORMAL)
                else:
                    self.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_EMPTY_HAND)
            self.send_event('E_SET_HAND_IK')
            return

    def _stop_switch_gun(self, new_state):
        hand_action = self.ev_g_hand_action()
        if new_state != self.sid:
            if self.cur_weapon_action:
                self.cur_weapon_action.exit()
                self.cur_weapon_action = None
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        new_obj_weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if new_obj_weapon:
            new_weapon_id = new_obj_weapon.get_item_id()
            if self._is_gun_pos(weapon_pos):
                action_id = confmgr.get('firearm_res_config', str(new_weapon_id), 'iActionType')
                self.send_event('E_SET_WEAPON_TYPE', action_id)
            else:
                import logic.gcommon.const as const
                if weapon_pos > const.PART_WEAPON_POS_NONE:
                    self.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_NORMAL)
                else:
                    self.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_EMPTY_HAND)
        if hand_action not in self.SWITCH_WEAPON_ACTION:
            return
        else:
            self._end_switch_gun(weapon_pos)
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
            self.send_event('E_DECIDE_RELOAD_TYPE', weapon_pos, first_reload=True)
            return

    def rebind_all_weapon(self, use_skate_bind_point):
        if self.is_active:
            return
        else:
            weapon_obj = self.sd.ref_wp_bar_cur_weapon
            if not weapon_obj:
                return
            weapon_id = weapon_obj.get_item_id()
            weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
            if not weapon_res_def:
                return
            if self.ev_g_get_state(status_config.ST_SKATE) and weapon_res_def['iActionType'] == animation_const.WEAPON_TYPE_SHIELD:
                use_skate_bind_point = True
            gun_model = self.sd.ref_left_hand_weapon_model
            if gun_model and weapon_res_def['cSkateBindPointLeft']:
                bind_point = weapon_res_def['cBindPointLeft']
                if use_skate_bind_point:
                    bind_point = weapon_res_def['cSkateBindPointLeft']
                self._rebind_one_weapon(gun_model, bind_point)
            gun_model = self.sd.ref_hand_weapon_model
            bind_point = weapon_res_def['cBindPoint']
            if gun_model:
                change_bind_point = None
                if self.ev_g_get_state(status_config.ST_LOAD) and weapon_res_def.get('cLoadBindPoint', None):
                    change_bind_point = weapon_res_def['cLoadBindPoint']
                if not change_bind_point and use_skate_bind_point and weapon_res_def['cSkateBindPoint']:
                    change_bind_point = weapon_res_def['cSkateBindPoint']
                if change_bind_point:
                    bind_point = change_bind_point
                self._rebind_one_weapon(gun_model, bind_point)
            return

    def _rebind_one_weapon(self, gun_model, bind_point):
        if not gun_model:
            return
        if not bind_point:
            return
        human_model = self.ev_g_model()
        if not human_model:
            return
        human_model.unbind(gun_model)
        human_model.bind(bind_point, gun_model)
        self.add_gun_bind_point(bind_point)

    def check_reequip_weapon(self):
        is_need_reequip = False
        if self.cur_weapon_action and self.cur_weapon_action.TYPE in self.SWITCH_WEAPON_ACTION:
            is_need_reequip = True
        if not is_need_reequip:
            return
        self.reequip_weapon()

    def reequip_weapon(self):
        if self.cur_weapon_action and self.cur_weapon_action.TYPE in self.SWITCH_WEAPON_ACTION:
            print(('test--reequip_weapon--step1--cur_weapon_action =', self.cur_weapon_action))
            self.cur_weapon_action.exit()
            self.cur_weapon_action = None
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        if weapon_pos > 0:
            self._change_equip_weapon_info(weapon_pos)
            self._equip_gun_by_pos(weapon_pos)
        self.disable_self()
        self.send_event('E_SET_HAND_IK')
        return

    def _unbind_all_weapon(self):
        self._destroy_left_gun()
        self._destroy_right_gun()
        self.send_event('E_CLEAR_FIRESTREAM_SFX')

    def show_all_gun(self):
        left_gun_model = self.sd.ref_left_hand_weapon_model
        if left_gun_model:
            self._decide_gun_visibility(left_gun_model, True)
        right_gun_model = self.sd.ref_hand_weapon_model
        if right_gun_model:
            self._decide_gun_visibility(right_gun_model, True)
        self._gun_visible_state[animation_const.WEAPON_POS_LEFT] = True
        self._gun_visible_state[animation_const.WEAPON_POS_RIGHT] = True
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_ALL_GUN, tuple()], True)

    def hide_all_gun(self):
        left_gun_model = self.sd.ref_left_hand_weapon_model
        if left_gun_model:
            self._decide_gun_visibility(left_gun_model, False)
        right_gun_model = self.sd.ref_hand_weapon_model
        if right_gun_model:
            self._decide_gun_visibility(right_gun_model, False)
        self._gun_visible_state[animation_const.WEAPON_POS_LEFT] = False
        self._gun_visible_state[animation_const.WEAPON_POS_RIGHT] = False
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_HIDE_ALL_GUN, tuple()], True)

    def _put_off_gun(self, leave_weapon_pos):
        cur_weapon_pos = self.sd.ref_wp_bar_cur_pos
        if leave_weapon_pos == cur_weapon_pos or cur_weapon_pos == 0:
            if self.cur_weapon_action and self.cur_weapon_action.TYPE in self.SWITCH_WEAPON_ACTION:
                self.cur_weapon_action.exit()
                self.cur_weapon_action = None
            put_off_action = WeaponAction.ImmediatePutOffWeaponAction(0, cur_weapon_pos, self)
            put_off_action.enter()
            self.send_event('E_ACTION_SET_EMPTY_HAND', True)
        return

    def _destroy_left_gun(self):
        model = self.ev_g_model()
        if not model:
            return
        else:
            pos = animation_const.WEAPON_POS_LEFT
            self.weapon_model_cancle_load_task(pos)
            gun_model = self.sd.ref_left_hand_weapon_model
            if gun_model and gun_model.valid:
                model.unbind(gun_model)
                self.send_event('E_DESTROY_WEAPON_MODEL', animation_const.WEAPON_POS_LEFT)
                gun_model.destroy()
            self.sd.ref_left_hand_weapon_model = None
            return

    def _destroy_right_gun(self):
        model = self.ev_g_model()
        if not model:
            return
        else:
            pos = animation_const.WEAPON_POS_RIGHT
            self.weapon_model_cancle_load_task(pos)
            gun_model = self.sd.ref_hand_weapon_model
            if gun_model and gun_model.valid:
                model.unbind(gun_model)
                self.send_event('E_DESTROY_WEAPON_MODEL', animation_const.WEAPON_POS_RIGHT)
                gun_model.destroy()
            self.sd.ref_hand_weapon_model = None
            return

    def weapon_model_cancle_load_task(self, pos):
        if pos in self.weapon_model_task_ids and self.weapon_model_task_ids[pos]:
            self.send_event('E_CANCEL_LOAD_TASK', self.weapon_model_task_ids[pos])
            del self.weapon_model_task_ids[pos]

    def _change_equip_weapon_info(self, weapon_pos):
        self.new_weapon_pos = weapon_pos


class HumanWeaponFire(StateBase):
    BIND_EVENT = {'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_NOTIFY_MOVE_STATE_CHANGE': 'change_fire_animation',
       'E_CLEAR_FIRESTREAM_SFX': 'clear_firestream_sfx',
       'E_LOAD_FIRESTREAM_SFX': 'load_firestream_sfx',
       'E_DECIDE_IGNITION_VISIBLE': '_decide_ignition_visible',
       'G_IS_LOAD_FIRESTREAM_SFX': 'is_load_firestream_sfx',
       'E_SET_FIRESTREAM_SFX_SCALE_Z': 'set_firestream_sfx_scale_z',
       'E_ON_FROZEN': '_on_frozen',
       'E_ON_EQUIP_ATTACHMENT': 'on_attachment_changed',
       'E_ON_TAKE_OFF_ATTACHMENT': 'on_attachment_changed',
       'E_CTRL_ACCUMULATE': '_on_accumulate',
       'G_ACCUMULATE_START_TIME': '_get_accumulate_start_time',
       'E_CUR_BULLET_NUM_CHG': 'on_bullet_num_change',
       'E_GUN_ATTACK': '_have_gun_attack_start',
       'E_ATTACK_END': '_attack_end',
       'E_AIM_TARGET': '_set_aim_target',
       'E_SHOW_FIRESTREAM_SFX': 'show_firestream_sfx',
       'E_PLAY_GUN_FIRE_SFX': 'play_gun_fire_sfx',
       'E_PLAY_AIM_GUN_FIRE_SFX': 'play_aim_gun_fire_sfx'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanWeaponFire, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._firestream_sfx = [
         None, None, None, None, None]
        self._firestream_sfx_left = [
         None, None, None, None, None]
        self._ignition = None
        self._tail_flamer = None
        self._firestream_visible = False
        self._gun_fire_sfx_id = None
        self._left_gun_fire_sfx_id = None
        self._gun_bullet_sfx_id = None
        self._is_right_gun_fire = False
        self._frozen_sfx_lst = []
        self._accumulate_time = 0
        self._last_aim_target = None
        return

    def _enter_states--- This code section failed: ---

1295       0  LOAD_GLOBAL           0  'common_enter_states'
           3  LOAD_FAST             0  'self'
           6  LOAD_FAST             1  'new_state'
           9  LOAD_CONST            1  'crouch_callback'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'change_fire_animation'
          18  LOAD_CONST            2  'jump_callback'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'change_fire_animation'
          27  CALL_FUNCTION_514   514 
          30  POP_TOP          

1296      31  LOAD_GLOBAL           2  'character_action_utils'
          34  LOAD_ATTR             3  'get_human_blend_type_by_key'
          37  LOAD_ATTR             3  'get_human_blend_type_by_key'
          40  CALL_FUNCTION_2       2 
          43  UNARY_NOT        
          44  STORE_FAST            2  'is_us_single_anim'

1297      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             4  'ev_g_get_state'
          53  LOAD_GLOBAL           5  'status_config'
          56  LOAD_ATTR             6  'ST_SKATE'
          59  CALL_FUNCTION_1       1 
          62  POP_JUMP_IF_TRUE     86  'to 86'
          65  LOAD_FAST             0  'self'
          68  LOAD_ATTR             7  'ev_g_weapon_type'
          71  CALL_FUNCTION_0       0 
          74  LOAD_GLOBAL           8  'animation_const'
          77  LOAD_ATTR             9  'WEAPON_TYPE_SHIELD'
          80  COMPARE_OP            2  '=='
        83_0  COME_FROM                '62'
          83  POP_JUMP_IF_FALSE    95  'to 95'

1298      86  LOAD_GLOBAL          10  'False'
          89  STORE_FAST            2  'is_us_single_anim'
          92  JUMP_FORWARD          0  'to 95'
        95_0  COME_FROM                '92'

1300      95  LOAD_FAST             2  'is_us_single_anim'
          98  POP_JUMP_IF_FALSE   144  'to 144'

1301     101  LOAD_FAST             0  'self'
         104  LOAD_ATTR            11  'is_active'
         107  POP_JUMP_IF_FALSE   144  'to 144'
         110  LOAD_GLOBAL           2  'character_action_utils'
         113  LOAD_ATTR            12  'is_jump'
         116  LOAD_FAST             1  'new_state'
         119  CALL_FUNCTION_1       1 
       122_0  COME_FROM                '107'
         122  POP_JUMP_IF_FALSE   144  'to 144'

1303     125  LOAD_FAST             0  'self'
         128  LOAD_ATTR            13  'send_event'
         131  LOAD_CONST            4  'E_CLEAR_UP_BODY_ANIM'
         134  CALL_FUNCTION_1       1 
         137  POP_TOP          
         138  JUMP_ABSOLUTE       144  'to 144'
         141  JUMP_FORWARD          0  'to 144'
       144_0  COME_FROM                '141'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 40

    def _leave_states--- This code section failed: ---

1306       0  LOAD_GLOBAL           0  'common_leave_states'
           3  LOAD_FAST             0  'self'
           6  LOAD_FAST             1  'leave_state'
           9  LOAD_FAST             2  'new_state'
          12  LOAD_CONST            1  'crouch_callback'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'change_fire_animation'
          21  LOAD_CONST            2  'jump_callback'
          24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             1  'change_fire_animation'
          30  CALL_FUNCTION_515   515 
          33  POP_TOP          

1307      34  LOAD_GLOBAL           2  'character_action_utils'
          37  LOAD_ATTR             3  'get_human_blend_type_by_key'
          40  LOAD_ATTR             3  'get_human_blend_type_by_key'
          43  CALL_FUNCTION_2       2 
          46  UNARY_NOT        
          47  STORE_FAST            3  'is_us_single_anim'

1308      50  LOAD_FAST             0  'self'
          53  LOAD_ATTR             4  'ev_g_get_state'
          56  LOAD_GLOBAL           5  'status_config'
          59  LOAD_ATTR             6  'ST_SKATE'
          62  CALL_FUNCTION_1       1 
          65  POP_JUMP_IF_TRUE     89  'to 89'
          68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             7  'ev_g_weapon_type'
          74  CALL_FUNCTION_0       0 
          77  LOAD_GLOBAL           8  'animation_const'
          80  LOAD_ATTR             9  'WEAPON_TYPE_SHIELD'
          83  COMPARE_OP            2  '=='
        86_0  COME_FROM                '65'
          86  POP_JUMP_IF_FALSE    98  'to 98'

1309      89  LOAD_GLOBAL          10  'False'
          92  STORE_FAST            3  'is_us_single_anim'
          95  JUMP_FORWARD          0  'to 98'
        98_0  COME_FROM                '95'

1311      98  LOAD_FAST             3  'is_us_single_anim'
         101  POP_JUMP_IF_FALSE   160  'to 160'

1312     104  LOAD_FAST             0  'self'
         107  LOAD_ATTR            11  'is_active'
         110  POP_JUMP_IF_FALSE   160  'to 160'
         113  LOAD_GLOBAL           2  'character_action_utils'
         116  LOAD_ATTR            12  'is_jump'
         119  LOAD_FAST             1  'leave_state'
         122  CALL_FUNCTION_1       1 
         125  POP_JUMP_IF_FALSE   160  'to 160'
         128  LOAD_FAST             0  'self'
         131  LOAD_ATTR            13  'ev_g_is_jump'
         134  CALL_FUNCTION_0       0 
         137  UNARY_NOT        
       138_0  COME_FROM                '125'
       138_1  COME_FROM                '110'
         138  POP_JUMP_IF_FALSE   160  'to 160'

1314     141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            14  'play_fire_animation'
         147  LOAD_CONST            4  ''
         150  CALL_FUNCTION_1       1 
         153  POP_TOP          
         154  JUMP_ABSOLUTE       160  'to 160'
         157  JUMP_FORWARD          0  'to 160'
       160_0  COME_FROM                '157'

1316     160  LOAD_FAST             1  'leave_state'
         163  LOAD_FAST             2  'new_state'
         166  COMPARE_OP            3  '!='
         169  POP_JUMP_IF_FALSE   234  'to 234'
         172  LOAD_FAST             1  'leave_state'
         175  LOAD_FAST             0  'self'
         178  LOAD_ATTR            15  'sid'
         181  COMPARE_OP            2  '=='
       184_0  COME_FROM                '169'
         184  POP_JUMP_IF_FALSE   234  'to 234'

1317     187  LOAD_FAST             0  'self'
         190  LOAD_ATTR            16  'send_event'
         193  LOAD_CONST            5  'E_ATTACK_END'
         196  CALL_FUNCTION_1       1 
         199  POP_TOP          

1318     200  LOAD_FAST             0  'self'
         203  LOAD_ATTR            16  'send_event'
         206  LOAD_CONST            6  'E_CALL_SYNC_METHOD'
         209  LOAD_CONST            7  'bcast_evt'
         212  LOAD_GLOBAL          17  'bcast'
         215  LOAD_ATTR            18  'E_ATTACK_END'
         218  LOAD_CONST            8  ''
         221  BUILD_LIST_2          2 
         224  LOAD_GLOBAL          19  'True'
         227  CALL_FUNCTION_4       4 
         230  POP_TOP          
         231  JUMP_FORWARD          0  'to 234'
       234_0  COME_FROM                '231'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 43

    def enter(self, leave_states):
        super(HumanWeaponFire, self).enter(leave_states)
        if self.sd.ref_finish_load_lod_model:
            character_action_utils.set_special_model_transparent_state(self, True)

    def exit(self, enter_states):
        hand_action = self.ev_g_hand_action()
        if hand_action == animation_const.HAND_STATE_NONE:
            self.send_event('E_EXIT_WEAPON_ACTION')
        if self.sd.ref_finish_load_lod_model:
            character_action_utils.set_special_model_transparent_state(self, False)
        super(HumanWeaponFire, self).exit(enter_states)

    def _set_aim_target(self, target):
        if target == self._last_aim_target:
            return
        if self._last_aim_target and self._last_aim_target.is_valid():
            if G_POS_CHANGE_MGR:
                self._last_aim_target.unregist_pos_change(self._follow_aim_target)
            else:
                self._last_aim_target.unregist_event('E_POSITION', self._follow_aim_target)
        self._last_aim_target = target
        if target and target.is_valid():
            if G_POS_CHANGE_MGR:
                target.regist_pos_change(self._follow_aim_target, 0.1)
            else:
                target.regist_event('E_POSITION', self._follow_aim_target)
        self.send_event('E_ROTATE_BODY_BY_Y', 0)

    def _follow_aim_target(self, *arg):
        self.send_event('E_ACTION_ROTATE', 0)

    def get_fire_action_postfix(self):
        action_id = self.ev_g_weapon_action_id()
        if action_id == animation_const.WEAPON_TYPE_FROZEN:
            weapon_obj = self.sd.ref_wp_bar_cur_weapon
            if weapon_obj:
                is_ball_mode = weapon_obj.is_in_multi_mode()
                if is_ball_mode:
                    return ''
            return '_1'
        return ''

    def reset_fire_node_phase(self):
        self.send_event('E_ANIM_PHASE', UP_BODY, 0)
        action_id = self.ev_g_weapon_action_id()
        postfix = self.get_fire_action_postfix()
        action_key = ('fire' + postfix, 'crouch_fire' + postfix)
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, loop=False, do_post=False)

    def get_actual_time(self):
        scale_action_time = 0
        action_id = self.ev_g_weapon_action_id()
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if obj_weapon:
            weapon_id = obj_weapon.get_item_id()
            scale_action_time = confmgr.get('firearm_res_config', str(weapon_id), 'fFireActionDuration', default=0)
        return scale_action_time

    def get_loop_model(self):
        loop = True
        attack_mode = -1
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if obj_weapon:
            attack_mode = obj_weapon.get_effective_value('iMode')
        else:
            print('test--get_loop_model--error--obj_weapon None')
        if attack_mode in (weapon_const.HALF_AUTO_MODE, weapon_const.MANUAL_MODE):
            loop = False
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        if weapon_obj:
            weapon_id = weapon_obj.get_item_id()
            iSingleFireActionInAUTO = confmgr.get('firearm_res_config', str(weapon_id), 'iSingleFireActionInAUTO')
            loop = iSingleFireActionInAUTO == 0
        return loop

    def change_fire_animation(self):
        if not self.is_active:
            return
        if not self.ev_g_get_state(self.sid):
            return
        phase = self.ev_g_anim_phase(UP_BODY)
        self.play_fire_animation(phase)

    def _do_begin_fire--- This code section failed: ---

1428       0  LOAD_GLOBAL           0  'character_action_utils'
           3  LOAD_ATTR             1  'get_human_blend_type_by_key'
           6  LOAD_ATTR             1  'get_human_blend_type_by_key'
           9  CALL_FUNCTION_2       2 
          12  UNARY_NOT        
          13  JUMP_IF_FALSE_OR_POP    25  'to 25'
          16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             2  'ev_g_is_jump'
          22  CALL_FUNCTION_0       0 
        25_0  COME_FROM                '13'
          25  STORE_FAST            1  'is_us_single_anim'

1429      28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             3  'ev_g_get_state'
          34  LOAD_GLOBAL           4  'status_config'
          37  LOAD_ATTR             5  'ST_SKATE'
          40  CALL_FUNCTION_1       1 
          43  POP_JUMP_IF_TRUE     67  'to 67'
          46  LOAD_FAST             0  'self'
          49  LOAD_ATTR             6  'ev_g_weapon_type'
          52  CALL_FUNCTION_0       0 
          55  LOAD_GLOBAL           7  'animation_const'
          58  LOAD_ATTR             8  'WEAPON_TYPE_SHIELD'
          61  COMPARE_OP            2  '=='
        64_0  COME_FROM                '43'
          64  POP_JUMP_IF_FALSE    76  'to 76'

1430      67  LOAD_GLOBAL           9  'False'
          70  STORE_FAST            1  'is_us_single_anim'
          73  JUMP_FORWARD          0  'to 76'
        76_0  COME_FROM                '73'

1432      76  LOAD_FAST             1  'is_us_single_anim'
          79  POP_JUMP_IF_FALSE    99  'to 99'

1433      82  LOAD_FAST             0  'self'
          85  LOAD_ATTR            10  'send_event'
          88  LOAD_CONST            2  'E_CLEAR_UP_BODY_ANIM'
          91  CALL_FUNCTION_1       1 
          94  POP_TOP          

1434      95  LOAD_CONST            0  ''
          98  RETURN_END_IF    
        99_0  COME_FROM                '79'

1436      99  LOAD_FAST             0  'self'
         102  LOAD_ATTR            11  'play_fire_animation'
         105  LOAD_CONST            3  ''
         108  CALL_FUNCTION_1       1 
         111  POP_TOP          

1437     112  LOAD_FAST             0  'self'
         115  LOAD_ATTR            10  'send_event'
         118  LOAD_CONST            4  'E_SET_SMOOTH_SPEED'
         121  LOAD_GLOBAL          12  'UP_BODY'
         124  LOAD_CONST            3  ''
         127  CALL_FUNCTION_3       3 
         130  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9

    def delay_play_gun_sfx(self, *args, **kwargs):
        if not self.ev_g_get_state(self.sid):
            return
        weapon_data = self.sd.ref_wp_bar_cur_weapon
        if weapon_data:
            if weapon_data.get_effective_value('iKind') == weapon_const.WP_SPELL:
                self.show_firestream_sfx()
            else:
                self.play_gun_fire_sfx(*args, **kwargs)

    def play_fire_animation(self, phase):
        scale_action_time = self.get_actual_time()
        action_id = self.ev_g_weapon_action_id()
        loop = self.get_loop_model()
        if action_id == animation_const.WEAPON_TYPE_PULSE:
            self.reset_fire_node_phase()
        use_single = self.ev_g_is_jump()
        postfix = self.get_fire_action_postfix()
        action_key = ('fire' + postfix, 'crouch_fire' + postfix, 'jump_fire' + postfix)
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, blend_time=0, loop=loop, scale_time=scale_action_time, phase=phase, use_single=use_single)

    def _have_gun_attack_start(self, *args, **kwargs):
        self.send_event('E_ACTION_IS_SHOOT', 1)
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_FIRE)
        self.active_self()
        action_id = self.ev_g_weapon_action_id()
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        if weapon_obj:
            weapon_id = weapon_obj.get_item_id()
            iSingleFireActionInAUTO = confmgr.get('firearm_res_config', str(weapon_id), 'iSingleFireActionInAUTO')
            is_loop = iSingleFireActionInAUTO == 0
            if not is_loop:
                self.reset_fire_node_phase()
        if not self.is_active:
            self._do_begin_fire()
            pass_args = args
            pass_kwargs = kwargs
            func = lambda *args: self.delay_play_gun_sfx(*pass_args, **pass_kwargs)
            global_data.game_mgr.register_logic_timer(func, interval=2, times=1)
        else:
            self.delay_play_gun_sfx(*args, **kwargs)

    def _attack_end(self, *args):
        self.hide_firestream_sfx()
        self.disable_self()
        old_hand_action = self.ev_g_hand_action()
        if old_hand_action == animation_const.HAND_STATE_FIRE:
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)

    def _on_accumulate(self, flag, *args):
        self._accumulate_time = time.time() if flag else 0

    def _get_accumulate_start_time(self):
        return self._accumulate_time

    def on_bullet_num_change(self, *args):
        bullet_num = self.ev_g_bullet_num()
        if bullet_num > 0:
            return
        else:
            weapon_obj = self.sd.ref_wp_bar_cur_weapon
            bullet_bind_point = None
            weapon_id = 0
            if weapon_obj:
                weapon_id = weapon_obj.get_item_id()
                weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
                if weapon_res_def:
                    bullet_bind_point = weapon_res_def['cBindPointBullet']
            if not bullet_bind_point:
                return
            gun_model = self.sd.ref_hand_weapon_model
            bullets = model_utils.get_socket_objects(gun_model, bullet_bind_point)
            for one_bullet in bullets:
                gun_model.unbind(one_bullet)
                one_bullet.destroy()

            return

    def on_attachment_changed(self, *args):
        path = self._get_muzzle_sfx_path()
        if not path:
            return
        else:
            if self._gun_fire_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._gun_fire_sfx_id)
                self._gun_fire_sfx_id = None
            if self._left_gun_fire_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._left_gun_fire_sfx_id)
                self._left_gun_fire_sfx_id = None
            return

    def is_load_firestream_sfx(self):
        return None not in self._firestream_sfx

    def play_aim_gun_fire_sfx(self, *args, **kwargs):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return
        else:
            sfx_path = self._get_muzzle_sfx_path()
            if not sfx_path:
                return
            if isinstance(sfx_path, (list, tuple)):
                accumulate_level = kwargs.get('accumulate_level', None)
                if accumulate_level is None:
                    sfx_path = sfx_path[0]
                else:
                    sfx_path = sfx_path[accumulate_level]
            gun_id = str(obj_weapon.get_item_id())
            sfx_bullet = confmgr.get('firearm_res_config', gun_id, 'cAimSfxBullet')
            if sfx_bullet:
                global_data.emgr.cam_aim_model_fire_effect_event.emit(sfx_bullet, RIGHT_BULLET_BIND_POINT)
            scene = world.get_active_scene()
            scale = 1
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            aim_attr = self.ev_g_attachment_attr(ATTACHEMNT_AIM_POS)
            if aim_attr:
                scale = aim_attr['cAttr'].get('fFireFXScale', 1)
            if self.sd.ref_in_aim:
                bind_point = confmgr.get('firearm_res_config', gun_id, 'cAimFirePoint', default=KAIHUO_BIND_POINT)
                global_data.emgr.cam_aim_model_fire_effect_event.emit(sfx_path, bind_point, scale=scale)
                return

            def create_cb(sfx):
                if not self.sd.ref_in_aim:
                    return
                else:
                    matrix = scene.active_camera.rotation_matrix
                    aim_pos_res = global_data.emgr.get_aim_gun_fire_matrix.emit()
                    sfx_pos = None
                    if aim_pos_res and aim_pos_res[0]:
                        sfx_pos = aim_pos_res[0]
                    else:
                        pos = scene.active_camera.position
                        sfx_pos = pos + matrix.forward * 5 - matrix.up * 1
                    sfx.scale = math3d.vector(scale, scale, scale)
                    sfx.rotation_matrix = matrix
                    sfx.position = sfx_pos
                    sfx.frame_rate = 1.0
                    return

            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=create_cb)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_AIM_GUN_FIRE_SFX, (), kwargs], True)
            return

    def play_gun_fire_sfx(self, *args, **kwargs):
        if not self.sd.ref_hand_weapon_model:
            return
        from logic.client.const.camera_const import AIM_MODE, RIGHT_AIM_MODE
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_GUN_FIRE_SFX, (), kwargs], True)
        if global_data.cam_lplayer and self.unit_obj and global_data.cam_lplayer.id == self.unit_obj.id and global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type() == AIM_MODE:
            self.play_aim_gun_fire_sfx(*args, **kwargs)
            return
        self.load_fire_sfx(*args, **kwargs)
        self._is_right_gun_fire = not self._is_right_gun_fire

    def _get_pellets_param(self):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return None
        else:
            pellets_param = confmgr.get('firearm_config', str(obj_weapon.get_item_id()), 'iPellets')
            return pellets_param

    def _get_muzzle_sfx_path(self):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon or not getattr(obj_weapon, 'get_attachment_attr', None):
            return
        else:
            from logic.gcommon.const import ATTACHEMNT_MUZZLE_POS
            attachment_attr = obj_weapon.get_attachment_attr(ATTACHEMNT_MUZZLE_POS)
            if attachment_attr and attachment_attr['cSfx']:
                return attachment_attr['cSfx']
            fashion = obj_weapon.get_fashion()
            fashion_id = fashion.get(FASHION_POS_SUIT, None)
            cSfx = weapon_skin_utils.get_weapon_skin_firearm_res(fashion_id, 'cSfx')
            if cSfx:
                return cSfx
            return self.get_weapon_fire_sfx(obj_weapon.get_item_id())

    def _play_left_weapon_sfx(self, sfx_path, *args, **kwargs):
        if not self.sd.ref_left_hand_weapon_model:
            return
        else:
            if isinstance(sfx_path, (list, tuple)):
                accumulate_level = kwargs.get('accumulate_level', None)
                if accumulate_level is None:
                    sfx_path = sfx_path[0]
                else:
                    sfx_path = sfx_path[accumulate_level]
            if self._left_gun_fire_sfx_id is None:
                if self.sd.ref_left_hand_weapon_model.has_socket(KAIHUO_BIND_POINT):

                    def _left_gun_del_sfx_cb(sfx):
                        self._left_gun_fire_sfx_id = None
                        return

                    self._left_gun_fire_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.sd.ref_left_hand_weapon_model, KAIHUO_BIND_POINT, on_create_func=self._on_create_fire_sfx_func, on_remove_func=_left_gun_del_sfx_cb)
            else:
                global_data.sfx_mgr.restart_sfx_by_id(self._left_gun_fire_sfx_id)
            obj_weapon = self.sd.ref_wp_bar_cur_weapon
            if confmgr.get('firearm_config', str(obj_weapon.get_item_id())).get('iMode') != weapon_const.MANUAL_MODE:
                _play_weapon_bullet_sfx(self, animation_const.WEAPON_POS_LEFT, LEFT_BULLET_BIND_POINT)
            return

    def _play_right_weapon_sfx(self, sfx_path, *args, **kwargs):
        if not self.sd.ref_hand_weapon_model:
            return
        else:
            if isinstance(sfx_path, (list, tuple)):
                accumulate_level = kwargs.get('accumulate_level', None)
                if accumulate_level is None:
                    sfx_path = sfx_path[0]
                else:
                    sfx_path = sfx_path[accumulate_level]
            if self._gun_fire_sfx_id is None:

                def _del_sfx_cb(sfx):
                    self._gun_fire_sfx_id = None
                    return

                self._gun_fire_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.sd.ref_hand_weapon_model, KAIHUO_BIND_POINT, on_create_func=self._on_create_fire_sfx_func, on_remove_func=_del_sfx_cb)
            else:
                global_data.sfx_mgr.restart_sfx_by_id(self._gun_fire_sfx_id)
            obj_weapon = self.sd.ref_wp_bar_cur_weapon
            if confmgr.get('firearm_config', str(obj_weapon.get_item_id())).get('iMode') != weapon_const.MANUAL_MODE:
                _play_weapon_bullet_sfx(self, animation_const.WEAPON_POS_RIGHT, RIGHT_BULLET_BIND_POINT)
            return

    def _on_create_fire_sfx_func(self, sfx, *args):
        if global_data.cam_lplayer:
            sfx_pos = sfx.world_position
            pos = global_data.cam_lplayer.ev_g_position()
            sfx_trans = sfx.transformation
            sfx_trans.rotation = math3d.matrix()
            sfx.transformation = sfx_trans
            if pos and sfx_pos:
                dis = (pos - sfx_pos).length / NEOX_UNIT_SCALE
                if dis <= 20:
                    sf = 1
                elif dis <= 100:
                    sf = 0.05 * dis
                else:
                    sf = 5
                sfx.scale = math3d.vector(sf, sf, sf)

    def load_fire_sfx(self, *args, **kwargs):
        sfx_path = self._get_muzzle_sfx_path()
        if not sfx_path:
            return
        pellets_param = self._get_pellets_param()
        if pellets_param and isinstance(pellets_param, dict):
            interval = pellets_param.get('cd', 0)
            bullets = pellets_param.get('bullets', [])
            times = len(bullets)
            if interval > 0 and times > 0:
                global_data.game_mgr.register_logic_timer(self.play_continuous_fire_sfx, interval, times=times, mode=timer.CLOCK)
        action_id = self.ev_g_weapon_action_id()
        if action_id == animation_const.WEAPON_TYPE_DOUBLE:
            if self._is_right_gun_fire:
                self._play_right_weapon_sfx(sfx_path, *args, **kwargs)
            else:
                self._play_left_weapon_sfx(sfx_path, *args, **kwargs)
        else:
            self._play_right_weapon_sfx(sfx_path, *args, **kwargs)

    def _on_create_fire_continuous_sfx_func(self, sfx, *args):
        action_id = self.ev_g_weapon_action_id()
        if action_id != animation_const.WEAPON_TYPE_PULSE or not self.ev_g_get_state(status_config.ST_SHOOT):
            global_data.sfx_mgr.remove_sfx(sfx)
            return
        sfx.restart()
        self._on_create_fire_sfx_func(sfx)

    def play_continuous_fire_sfx(self, *args):
        action_id = self.ev_g_weapon_action_id()
        if action_id != animation_const.WEAPON_TYPE_PULSE:
            return timer.RELEASE
        if not self.ev_g_get_state(status_config.ST_SHOOT):
            return timer.RELEASE
        sfx_path = self._get_muzzle_sfx_path()
        if not sfx_path:
            return
        global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.sd.ref_hand_weapon_model, 'kaihuo', on_create_func=self._on_create_fire_continuous_sfx_func)
        left_weapon = self.sd.ref_left_hand_weapon_model
        if left_weapon and left_weapon.has_socket('kaihuo'):
            self._left_gun_fire_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, left_weapon, 'kaihuo', on_create_func=self._on_create_fire_continuous_sfx_func)
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return timer.RELEASE
        sfx_bullet = confmgr.get('firearm_res_config', str(obj_weapon.get_item_id()), 'cSfxBullet')
        if not sfx_bullet:
            return timer.RELEASE
        global_data.sfx_mgr.create_sfx_on_model(sfx_bullet, self.sd.ref_hand_weapon_model, 'kaihuo', on_create_func=self._on_create_fire_sfx_func)

    def clear_firestream_sfx(self):
        for idx, sfx in enumerate(self._firestream_sfx):
            if sfx:
                global_data.sfx_mgr.remove_sfx(sfx)
            sfx_left = self._firestream_sfx_left[idx]
            if sfx_left:
                global_data.sfx_mgr.remove_sfx(sfx_left)

        self._firestream_sfx = [
         None, None, None, None, None]
        self._firestream_sfx_left = [None, None, None, None, None]
        if self._ignition:
            global_data.sfx_mgr.remove_sfx(self._ignition)
        self._ignition = None
        if self._tail_flamer:
            global_data.sfx_mgr.remove_sfx(self._tail_flamer)
        self._tail_flamer = None
        self._firestream_visible = False
        self._gun_fire_sfx_id = None
        self._left_gun_fire_sfx_id = None
        return

    def load_firestream_sfx(self, now_weapon):

        def create_cb(user_data, sfx):
            if self.is_valid():
                self.on_add_fire_sfx(user_data, sfx)
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

        weapon_id = now_weapon.get_item_id()
        res_config = confmgr.get('firearm_res_config', str(weapon_id), default={})
        custom_info = res_config.get('cCustomParam')
        custom_info2 = self.ev_g_weapon_attr_get(weapon_id, 'firearm_res_custom', None)
        if custom_info2:
            custom_info = custom_info2
        fashion = now_weapon.get_fashion()
        fashion_id = fashion.get(FASHION_POS_SUIT, None)
        skin_cCustomParam = weapon_skin_utils.get_weapon_skin_firearm_res(fashion_id, 'cCustomParam')
        if skin_cCustomParam:
            custom_info = skin_cCustomParam
        if custom_info:
            has_left_weapon = True if res_config.get('cResLeft', '') else False
            for sfx_path, socket_point, attr_name, idx, is_show in custom_info:
                show = True if is_show else False
                if idx == -1:
                    idx = None
                weapon = self.sd.ref_hand_weapon_model
                if weapon:
                    global_data.sfx_mgr.create_sfx_on_model(sfx_path, weapon, socket_point, on_create_func=Functor(create_cb, (attr_name, idx, show)))
                if has_left_weapon and idx is not None and self.sd.ref_left_hand_weapon_model:
                    attr_name = '_firestream_sfx_left'
                    global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.sd.ref_left_hand_weapon_model, socket_point, on_create_func=Functor(create_cb, (attr_name, idx, show)))

        return

    def on_add_fire_sfx(self, user_data, sfx):
        weapon = self.sd.ref_hand_weapon_model
        attr, index, enable = user_data
        enable = enable and weapon and weapon.visible
        sfx.set_sfx_enable(enable)
        if index is not None:
            sfx_list = getattr(self, attr)
            old_sfx = sfx_list[index]
            if old_sfx:
                global_data.sfx_mgr.remove_sfx(old_sfx)
            getattr(self, attr)[index] = sfx
            if self._firestream_visible:
                sfx.set_sfx_enable(True)
                sfx.restart()
        else:
            old_sfx = getattr(self, attr, None)
            if old_sfx:
                global_data.sfx_mgr.remove_sfx(old_sfx)
            setattr(self, attr, sfx)
        return

    def set_firestream_sfx_scale_z(self, scale_z_list):
        for i, sfx in enumerate(self._firestream_sfx):
            if i >= len(scale_z_list):
                break
            if sfx and sfx.valid:
                scale = sfx.scale
                scale.z = scale_z_list[i]
                sfx.scale = scale
                sfx_left = self._firestream_sfx_left[i]
                if sfx_left and sfx_left.valid:
                    sfx_left.scale = scale

    def get_weapon_fire_sfx(self, weapon_id):
        res_conf = confmgr.get('firearm_res_config', str(weapon_id))
        if not res_conf:
            return ''
        sfx_path = res_conf['cSfx']
        is_ob_player = global_data.cam_lplayer and global_data.cam_lplayer.id == self.unit_obj.id
        if self.ev_g_is_avatar() or is_ob_player:
            if self.ev_g_get_state(status_config.ST_AIM):
                aim_sfx_path = res_conf.get('cOpenAimSfx', '')
                if aim_sfx_path:
                    sfx_path = aim_sfx_path
        return sfx_path

    def show_firestream_sfx(self):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_FIRESTREAM_SFX, ()], True)
        self._firestream_visible = True
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return
        else:
            fashion = obj_weapon.get_fashion()
            fashion_id = fashion.get(FASHION_POS_SUIT, None)
            sfx_path = weapon_skin_utils.get_weapon_skin_firearm_res(fashion_id, 'cSfx')
            if not sfx_path:
                sfx_path = self.get_weapon_fire_sfx(obj_weapon.get_item_id())
            if sfx_path:
                if isinstance(sfx_path, list):
                    for one_sfx_path in sfx_path:
                        global_data.sfx_mgr.create_sfx_on_model(one_sfx_path, self.sd.ref_hand_weapon_model, 'kaihuo')

                else:
                    global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.sd.ref_hand_weapon_model, 'kaihuo')
            if self._tail_flamer and self._tail_flamer.valid:
                self._tail_flamer.set_sfx_enable(True)
                self._tail_flamer.restart()
            for idx, sfx in enumerate(self._firestream_sfx):
                if sfx and sfx.valid:
                    sfx.set_sfx_enable(True)
                    sfx.restart()
                sfx_left = self._firestream_sfx_left[idx]
                if sfx_left and sfx_left.valid:
                    sfx_left.set_sfx_enable(True)
                    sfx_left.restart()

            return

    def hide_firestream_sfx(self):
        self._firestream_visible = False
        if self._tail_flamer and self._tail_flamer.valid:
            self._tail_flamer.set_sfx_enable(False)
        for idx, sfx in enumerate(self._firestream_sfx):
            if sfx and sfx.valid:
                sfx.set_sfx_enable(False)
            sfx_left = self._firestream_sfx_left[idx]
            if sfx_left and sfx_left.valid:
                sfx_left.set_sfx_enable(False)

    def _decide_ignition_visible(self, visible):
        if self._ignition and self._ignition.valid:
            self._ignition.set_sfx_enable(visible)
            if visible:
                self._ignition.restart()

    def _clear_frozen_sfx(self):
        for sfx_id in self._frozen_sfx_lst:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._frozen_sfx_lst = []

    def _on_frozen(self, is_frozen):
        path = 'effect/fx/weapon/bingdongqiang/bdq_ice_04_rw.sfx'
        if is_frozen:
            weapon = self.sd.ref_hand_weapon_model
            if weapon and weapon.has_socket('hand'):
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(path, weapon, 'hand')
                self._frozen_sfx_lst.append(sfx_id)
            left_weapon = self.sd.ref_left_hand_weapon_model
            if left_weapon and left_weapon.has_socket('hand'):
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(path, left_weapon, 'hand')
                self._frozen_sfx_lst.append(sfx_id)
        else:
            self._clear_frozen_sfx()


class HumanReload(StateBase):
    BIND_EVENT = {'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_RELOADING': '_add_bullet',
       'E_NOTIFY_MOVE_STATE_CHANGE': 'change_reload_animation',
       'E_DECIDE_RELOAD_TYPE': 'decide_reload_type',
       'E_CTRL_ROLL': 'on_roll',
       'E_CTRL_RUSH': 'on_roll',
       'E_END_ROLL': 'on_end_roll',
       'E_END_RUSH_EVENT': 'on_end_roll'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanReload, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._reload_type = animation_const.RELOAD_TYPE_ALL
        self._leave_add_bullet_times = 0
        self._reload_time = 0
        self._anim_duration = 0
        self._scale_timer = scale_timer.ScaleTimer(0.033)
        self._reload_times = 0

    def destroy(self):
        super(HumanReload, self).destroy()
        self._scale_timer.destroy()

    def _enter_states(self, new_state):
        common_enter_states(self, new_state, crouch_callback=self.change_reload_animation, jump_callback=self.change_reload_animation)

    def _leave_states(self, leave_state, new_state=None):
        common_leave_states(self, leave_state, new_state, crouch_callback=self.change_reload_animation, jump_callback=self.change_reload_animation)
        if leave_state != new_state and new_state is not None:
            if leave_state == self.sid:
                self.send_event('E_CANCEL_RELOAD')
        return

    def enter(self, leave_states):
        super(HumanReload, self).enter(leave_states)
        self.send_event('E_BEGIN_ADD_BULLET')
        self._decide_add_bullet_clip()

    def exit(self, enter_states):
        elapsed_time = self.elapsed_time
        super(HumanReload, self).exit(enter_states)
        self.send_event('E_END_ADD_BULLET')
        self._scale_timer.unregister('END_ADD_BULLET_EVENT')
        hand_action = self.ev_g_hand_action()
        if hand_action == animation_const.HAND_STATE_ADD_BULLET:
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
            if self.ev_g_get_state(status_config.ST_CROUCH):
                clip_name, _, crouch_data = character_action_utils.get_idle_clip(self, status_config.ST_CROUCH)
                if crouch_data:
                    self.send_event('E_POST_ACTION', crouch_data['anim_name'], LOW_BODY, 1, loop=True)
                    self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=True)
            else:
                self.send_event('E_END_BULLET_RELOAD')

    def on_roll(self, *args):
        roll_reload_speed_factor = self.ev_g_attr_get('fRollReloadSpeedFactor', 0)
        if roll_reload_speed_factor == 0 or not self.ev_g_get_state(self.sid):
            return
        roll_reload_time_scale = 1 + roll_reload_speed_factor
        self._scale_timer.set_time_scale('END_ADD_BULLET_EVENT', roll_reload_time_scale)

    def on_end_roll(self, *args):
        roll_reload_speed_factor = self.ev_g_attr_get('fRollReloadSpeedFactor', 0)
        if roll_reload_speed_factor == 0 or not self.ev_g_get_state(self.sid):
            return
        self._scale_timer.set_time_scale('END_ADD_BULLET_EVENT', 1)

    def _add_bullet(self, *arg):
        if len(arg) < 3:
            self._reload_time = arg[0]
        else:
            self._reload_time = arg[2]
        times = arg[1]
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        self.decide_reload_type(weapon_pos, first_reload=True)
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_ADD_BULLET)
        self._reload_times = times
        if times > 0:
            self._leave_add_bullet_times = times - 1

    def change_reload_animation(self):
        if not self.is_active:
            return
        action_id = self.ev_g_weapon_action_id()
        loop = False
        if self._reload_type == animation_const.RELOAD_TYPE_ONE_NEXT:
            loop = True
        action_key = ('first_reload', 'crouch_first_reload')
        scale_action_time = self._get_add_bullet_time()
        phase = self.sub_sid_timer / self._anim_duration
        use_single = False
        if self.ev_g_is_jump():
            use_single = True
        do_post = True
        if self.ev_g_get_state(status_config.ST_ROLL):
            do_post = False
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, loop=loop, scale_time=scale_action_time, phase=phase, use_single=use_single, do_post=do_post)

    def _decide_add_bullet_clip(self):
        weapon_type_2_action = weapon_action_config.weapon_type_2_action
        action_id = self.ev_g_weapon_action_id()
        action_config = weapon_type_2_action.get(action_id, None)
        loop = False
        if self._reload_type == animation_const.RELOAD_TYPE_ONE_NEXT:
            loop = True
        action_key = ('first_reload', 'crouch_first_reload')
        scale_action_time = self._get_add_bullet_time()
        use_single = False
        if self.ev_g_is_jump():
            use_single = True
        do_post = True
        if self.ev_g_get_state(status_config.ST_ROLL):
            do_post = False
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, loop=loop, scale_time=scale_action_time, phase=0, use_single=use_single, do_post=do_post)
        end_time = scale_action_time
        if not end_time:
            end_time = self.ev_g_get_anim_length(clip_list[-1])
        stage = self._leave_add_bullet_times + 1
        self.sub_state = stage
        self._anim_duration = end_time
        if not self._scale_timer.is_active('END_ADD_BULLET_EVENT') and scale_action_time:
            self._scale_timer.register('END_ADD_BULLET_EVENT', scale_action_time, lambda : self._end_add_bullet(), max_times=self._reload_times)
        elif self._reload_type != weapon_const.RELOAD_ALL:
            self._scale_timer.set_interval('END_ADD_BULLET_EVENT', scale_action_time)
        return

    def _end_add_bullet(self, *args):
        if self.is_active:
            self.send_event('E_END_PUT_ON_BULLET')
        if self._leave_add_bullet_times > 0:
            self._leave_add_bullet_times -= 1
            weapon_pos = self.sd.ref_wp_bar_cur_pos
            self.decide_reload_type(weapon_pos, first_reload=False)
            self._decide_add_bullet_clip()
            return
        self.ev_g_cancel_state(self.sid)
        self.exit(set())

    def _get_add_bullet_time(self):
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        if not weapon_obj:
            print('[error]--_get_add_bullet_time--weapon_obj None')
            return 0
        bullet_num = self.ev_g_bullet_num()
        actual_anim_time = 0
        if weapon_obj.get_effective_value('iReloadType') == weapon_const.RELOAD_ALL:
            actual_anim_time = self._reload_time
        elif bullet_num > 0:
            actual_anim_time = weapon_obj.get_effective_value('fReloadTimeLeft')
        else:
            actual_anim_time = self._reload_time
        weapon_kind = weapon_obj.get_effective_value('iKind')
        speed_factor = self.ev_g_add_attr('weapon_reload_speed_factor_{}'.format(weapon_kind), 0)
        human_speed_common_factor = self.ev_g_add_attr('weapon_reload_speed_factor_human_all')
        return actual_anim_time / (1 + speed_factor + human_speed_common_factor)

    def decide_reload_type(self, weapon_pos, first_reload=False):
        reload_type = animation_const.RELOAD_TYPE_ALL
        if self.ev_g_is_gun_pos(weapon_pos):
            weapon_data = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            if weapon_data and weapon_data.get_effective_value('iReloadType') == weapon_const.RELOAD_ONE:
                if first_reload:
                    reload_type = animation_const.RELOAD_TYPE_ONE_FIRST
                else:
                    reload_type = animation_const.RELOAD_TYPE_ONE_NEXT
        self._set_reload_type(reload_type)

    def _set_reload_type(self, reload_type):
        self._reload_type = reload_type


class HumanWeaponLoad(StateBase):
    BIND_EVENT = {'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_NOTIFY_MOVE_STATE_CHANGE': 'change_gun_load_animation',
       'E_LOADING': '_gun_loading',
       'E_SET_WEAPON_LOAD_TYPE': 'set_weapon_load_type'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanWeaponLoad, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._weapon_load_type = animation_const.WEAPON_LOAD_FROM_IDLE
        self._anim_duration = 0

    def _enter_states(self, new_state):
        common_enter_states(self, new_state, self.change_gun_load_animation)

    def _leave_states(self, leave_state, new_state=None):
        common_leave_states(self, leave_state, new_state, self.change_gun_load_animation)

    def enter(self, leave_states):
        super(HumanWeaponLoad, self).enter(leave_states)
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_LOAD)
        self._do_begin_gun_load()
        if self.status_config.ST_SHOOT in leave_states:
            _play_weapon_bullet_sfx(self, animation_const.WEAPON_POS_RIGHT, RIGHT_BULLET_BIND_POINT, sync=True)
        action_id = self.ev_g_weapon_action_id()
        if action_id == animation_const.WEAPON_TYPE_SNIPER_RIFLE:
            _play_weapon_bullet_sfx(self, animation_const.WEAPON_POS_RIGHT, RIGHT_BULLET_BIND_POINT, sync=True)

    def exit(self, enter_states):
        elapsed_time = self.elapsed_time
        super(HumanWeaponLoad, self).exit(enter_states)
        self._end_load()

    def update(self, dt):
        super(HumanWeaponLoad, self).update(dt)
        if self.elapsed_time >= self._anim_duration:
            self.disable_self()

    def change_gun_load_animation(self):
        if not self.is_active:
            return
        phase = self.ev_g_anim_phase(UP_BODY)
        self.play_gun_load_animation(phase)

    def _do_begin_gun_load(self):
        self.play_gun_load_animation(0)

    def play_gun_load_animation(self, phase):
        action_id = self.ev_g_weapon_action_id()
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        scale_action_time = 0
        weapon_id = 0
        if obj_weapon:
            weapon_id = obj_weapon.get_effective_value('iType', 0)
            scale_action_time = obj_weapon.get_effective_value('fCDTime2', scale_action_time) * (1 - obj_weapon.interval_factor)
        else:
            print('[error]--play_gun_load_animation--obj_weapon None')
        action_key = ('gun_load', 'crouch_gun_load')
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, loop=False, scale_time=scale_action_time, phase=phase)
        end_time = scale_action_time
        if not end_time:
            end_time = self.ev_g_get_anim_length(clip_list[-1])
        self._anim_duration = end_time

    def _gun_loading(self, *arg):
        self.active_self()

    def _end_load(self, *args):
        self.send_event('E_END_LOAD')
        hand_action = self.ev_g_hand_action()
        if hand_action == animation_const.HAND_STATE_LOAD:
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)

    def set_weapon_load_type(self, weapon_load_type):
        self._weapon_load_type = weapon_load_type


class SwitchWeaponMode(StateBase):
    BIND_EVENT = {'E_SWITCHED_WP_MODE': 'switch_gun_mode',
       'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_NOTIFY_MOVE_STATE_CHANGE': 'change_switch_gun_mode_animation'
       }
    SWITCH_SFX = 'effect/fx/robot/bianxingche/bxc_huandan.sfx'

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SwitchWeaponMode, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._anim_duration = 0

    def _enter_states(self, new_state):
        common_enter_states(self, new_state, self.change_switch_gun_mode_animation)

    def _leave_states(self, leave_state, new_state=None):
        common_leave_states(self, leave_state, new_state, self.change_switch_gun_mode_animation)

    def enter(self, leave_states):
        super(SwitchWeaponMode, self).enter(leave_states)
        self._do_begin_switch_gun_mode()

    def exit(self, enter_states):
        elapsed_time = self.elapsed_time
        super(SwitchWeaponMode, self).exit(enter_states)
        self._end_switch_gun_mode()

    def update(self, dt):
        super(SwitchWeaponMode, self).update(dt)
        if self.elapsed_time >= self._anim_duration:
            self.disable_self()

    def change_switch_gun_mode_animation(self):
        if not self.is_active:
            return
        phase = self.ev_g_anim_phase(UP_BODY)
        self.play_switch_gun_mode_animation(phase)

    def _do_begin_switch_gun_mode(self):
        self.play_switch_gun_mode_animation(0)

    def play_switch_gun_mode_animation(self, phase):
        action_id = self.ev_g_weapon_action_id()
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        scale_action_time = 0
        weapon_id = 0
        if obj_weapon:
            weapon_id = obj_weapon.get_effective_value('iType', 0)
            scale_action_time = obj_weapon.get_effective_value('fSwitchModeTime', scale_action_time)
        else:
            print('test--_do_begin_switch_gun_mode--[error]--obj_weapon None')
        action_key = ('switch_gun_mode', 'crouch_switch_gun_mode')
        clip_list = _decide_single_or_blend_clip(self, action_key, action_id, loop=False, scale_time=scale_action_time, phase=phase)
        end_time = scale_action_time
        if not end_time:
            end_time = self.ev_g_get_anim_length(clip_list[-1])
        self._anim_duration = end_time

    def _end_switch_gun_mode(self, *args):
        self.send_event('E_ACTION_END_SWITCH_GUN_MODE')
        hand_action = self.ev_g_hand_action()
        if hand_action == animation_const.HAND_STATE_SWITCH_GUN_MODE:
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)

    def switch_gun_mode(self, *args):
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_SWITCH_GUN_MODE)
        now_weapon = self.sd.ref_wp_bar_cur_weapon
        if now_weapon and now_weapon.get_kind() == weapon_const.WP_SPELL and not self.ev_g_is_load_firestream_sfx():
            self.send_event('E_LOAD_FIRESTREAM_SFX', now_weapon)
        left_weapon = self.sd.ref_left_hand_weapon_model
        if left_weapon and left_weapon.has_socket('fx_xuli_1'):
            global_data.sfx_mgr.create_sfx_on_model(self.SWITCH_SFX, left_weapon, 'fx_xuli_1')
        weapon = self.sd.ref_hand_weapon_model
        if weapon and weapon.has_socket('fx_xuli'):
            global_data.sfx_mgr.create_sfx_on_model(self.SWITCH_SFX, weapon, 'fx_xuli')


class HumanHit(StateBase):
    BIND_EVENT = {'E_HITED': 'be_hited',
       'E_ACTION_HITED_BY_VEHICLE': '_hit_by_vehicle'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HumanHit, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._hited_timer = 0
        self._hit_duration = 0

    def enter(self, leave_states):
        super(HumanHit, self).enter(leave_states)

    def exit(self, enter_states):
        super(HumanHit, self).exit(enter_states)
        self.send_event('E_RESET_ROTATE_WEAPON')

    def is_hit(self):
        return self.ev_g_hand_action() == animation_const.HAND_STATE_HITED

    def _end_hited(self):
        self._hited_timer = 0
        self.disable_self()
        if self.is_hit():
            self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        self.send_event('E_RESET_ROTATE_WEAPON')

    def _hit_by_vehicle(self):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_HITED_BY_VEHICLE, ()], True)
        self.be_hited(False)

    def be_hited(self, is_avart_dont_play=True):
        if self.unit_obj:
            global_data.emgr.battle_people_get_hurt.emit(self.unit_obj.id)
        if is_avart_dont_play:
            if self.ev_g_is_avatar():
                return
        action_id = self.ev_g_weapon_action_id()
        if action_id == animation_const.WEAPON_TYPE_SHIELD:
            return
        if action_id == animation_const.WEAPON_TYPE_SHIELD_RIFLE and self.ev_g_is_shield_opened():
            return
        hand_action = self.ev_g_hand_action()
        if hand_action != animation_const.HAND_STATE_NONE:
            return
        if not self.check_can_active(only_avatar=False):
            return
        self.send_event('E_CHECK_REEQUIP_WEAPON')
        self.active_self()
        clip_list = self.ev_g_weapon_action_list('hit')
        clip_name = clip_list[0]
        self._hit_duration = self.ev_g_get_anim_length(clip_name) * 1.1
        if self._hited_timer:
            global_data.game_mgr.unregister_logic_timer(self._hited_timer)
            self._hited_timer = 0
        interval = self._hit_duration or 0.5
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_HITED)
        self._hited_timer = global_data.game_mgr.register_logic_timer(self._end_hited, interval, times=1, mode=timer.CLOCK)
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=False, blend_time=0.1)
        self.send_event('E_ROTATE_WEAPON')