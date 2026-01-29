# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComHumanStateData.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import mecha_const
from ....cdata.status_config import *
from common.utils.timer import CLOCK
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.cdata import speed_physic_arg
from common.cfg import confmgr
from logic.gutils import character_action_utils

class ComHumanStateData(UnitCom):
    BIND_EVENT = {'E_CHARACTER_ATTR': '_change_character_attr',
       'E_JUMP_STAGE': 'set_jump_stage',
       'G_JUMP_STAGE': 'get_jump_stage',
       'G_IS_MULTIPLE_JUMP': 'is_multiple_jump',
       'E_FIXED_POS_JUMP': 'set_fixed_pos_jump',
       'G_FIXED_POS_JUMP': 'get_fixed_pos_jump',
       'G_ACTION_IS_JUMP': 'action_is_jump',
       'E_MOVE_STATE': 'set_move_state',
       'G_MOVE_STATE': 'get_move_state',
       'G_IS_MOVE': 'is_move',
       'E_KEEP_SHOOT_TIME': 'set_keep_shoot_time',
       'G_KEEP_SHOOT_TIME': 'get_keep_shoot_time',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': 'leave_states',
       'E_SET_WEAPON_TYPE': 'set_weapon_type',
       'G_WEAPON_TYPE': 'get_weapon_type',
       'G_WEAPON_ACTION_ID': '_get_weapon_action_id',
       'E_ACTION_IS_SHOOT': 'set_is_shoot',
       'G_ACTION_IS_SHOOT': 'get_is_shoot',
       'G_MAX_JUMP_AIR_SPEED': 'get_max_jump_air_speed',
       'E_MAX_JUMP_AIR_SPEED': 'set_max_jump_air_speed',
       'G_IS_KEEP_DOWN_FIRE': 'get_is_keep_down_fire',
       'E_IS_KEEP_DOWN_FIRE': 'set_is_keep_down_fire'
       }
    DEFAULT_DELAY_KEEP_SHOOT_TIME = 1
    KEEP_SHOOT_STATE = (ST_SHOOT, ST_AIM)

    def __init__(self):
        super(ComHumanStateData, self).__init__()
        self._jump_stage = 0
        self._is_fixed_pos_jump = False
        self._move_action = animation_const.MOVE_STATE_STAND
        self._keep_shoot_time = 0
        self._weapon_type = animation_const.WEAPON_TYPE_EMPTY_HAND
        self._is_shoot = 0
        self._max_jump_air_speed = 0
        self._is_keep_down_fire = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanStateData, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_left_hand_weapon_model = None
        self.sd.ref_hand_weapon_model = None
        return

    def on_init_complete(self):
        super(ComHumanStateData, self).on_init_complete()

    def destroy(self):
        super(ComHumanStateData, self).destroy()

    def _change_character_attr(self, name, *arg):
        if name == 'animator_info':
            print(('test--ComHumanStateData--_weapon_type =', self._weapon_type, '--is_shoot =', self._is_shoot, '--jump_stage =', self._jump_stage))

    def enter_states(self, new_state):
        if new_state in character_action_utils.JUMP_STATE:
            if self.ev_g_is_avatar() and self.get_is_shoot():
                self.set_is_shoot(0)
                self.set_keep_shoot_time(0)

    def leave_states(self, leave_state, new_state=None):
        if leave_state in self.KEEP_SHOOT_STATE:
            self.update_keep_shoot_time()
        if leave_state in character_action_utils.HUMAN_SLOW_DOWN_STATE:
            self.set_is_shoot(0)

    def update_keep_shoot_time(self, *arg):
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        delay_time = 0.0
        if weapon_obj:
            weapon_id = weapon_obj.get_item_id()
            delay_time = confmgr.get('firearm_res_config', str(weapon_id), 'fAimActionDuration')
        if self.ev_g_get_state(ST_SKATE_MOVE):
            delay_time = speed_physic_arg.skate_move_fire_keep_time
        if delay_time <= 0.0:
            delay_time = self.DEFAULT_DELAY_KEEP_SHOOT_TIME
        self._keep_shoot_time = delay_time

    def set_is_keep_down_fire(self, is_keep_down_fire):
        self._is_keep_down_fire = is_keep_down_fire

    def get_is_keep_down_fire(self):
        return self._is_keep_down_fire

    def set_jump_stage(self, stage):
        self._jump_stage = stage

    def get_jump_stage(self):
        return self._jump_stage

    def set_fixed_pos_jump(self, is_fixed):
        self._is_fixed_pos_jump = is_fixed

    def get_fixed_pos_jump(self):
        return self._is_fixed_pos_jump

    def is_multiple_jump(self):
        if self.ev_g_is_jump():
            if self._jump_stage > 1:
                return True
        return False

    def action_is_jump(self):
        current_posture_state = self.ev_g_anim_state()
        return current_posture_state == animation_const.STATE_JUMP

    def set_move_state(self, move_action):
        if self._move_action == move_action:
            return
        self._move_action = move_action
        self.send_event('E_CALL_SYNC_METHOD', 'sync_move_state', (move_action,), False)
        self.send_event('E_SET_HAND_IK')
        self.send_event('E_NOTIFY_MOVE_STATE_CHANGE')
        self.send_event('E_SET_FOOT_IK')

    def get_move_state(self):
        return self._move_action

    def is_move(self):
        return self._move_action == animation_const.MOVE_STATE_WALK or self._move_action == animation_const.MOVE_STATE_RUN or self.ev_g_get_state(ST_MECHA_BOARDING)

    def set_keep_shoot_time(self, shoot_time):
        self._keep_shoot_time = shoot_time

    def get_keep_shoot_time(self):
        return self._keep_shoot_time

    def get_weapon_type(self):
        return self._get_weapon_action_id()

    def set_weapon_type(self, weapon_type):
        self._weapon_type = weapon_type
        self.send_event('E_ON_CHANGE_WEAPON')

    def _get_weapon_action_id(self):
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        action_id = animation_const.WEAPON_TYPE_EMPTY_HAND
        if weapon_obj:
            weapon_id = weapon_obj.get_item_id()
            action_id = confmgr.get('firearm_res_config', str(weapon_id), 'iActionType')
        return action_id

    def get_is_shoot(self):
        return self._is_shoot

    def set_is_shoot(self, is_shoot):
        if not is_shoot and (self.ev_g_is_in_slow_down_state() or self._keep_shoot_time > 0):
            return
        if self._is_shoot == is_shoot:
            return
        self._is_shoot = is_shoot
        self.send_event('E_SET_BIND_OBJ_IS_SHOOT', is_shoot)
        self.send_event('E_CHANGE_SHOOT_STATE')
        self.send_event('E_CHANGE_SPEED')

    def get_is_shoot(self):
        return self._is_shoot

    def get_max_jump_air_speed(self):
        return self._max_jump_air_speed

    def set_max_jump_air_speed(self, speed):
        self._max_jump_air_speed = speed