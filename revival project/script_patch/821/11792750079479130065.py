# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/WeaponAction.py
from __future__ import absolute_import
from __future__ import print_function
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.cdata import status_config
import logic.gcommon.const as const
from common.cfg import confmgr

class WeaponAction(object):
    TYPE = animation_const.HAND_STATE_NONE

    def __init__(self, weapon_id, weapon_pos, unit_com, *args, **kwargs):
        self._weapon_id = weapon_id
        self._weapon_pos = weapon_pos
        self._cancel_state_on_exit = True
        self.unit_com = unit_com
        self._weapon_data = unit_com.ev_g_wpbar_get_by_pos(weapon_pos)

    def __hash__(self):
        return self.TYPE

    def __eq__(self, other):
        return self.TYPE == other.TYPE

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '[weapon_id= %d, weapon_pos=%d, address=%s, type=%s]' % (self.weapon_id, self.weapon_pos, id(self), type(self))

    @property
    def weapon_id(self):
        return self._weapon_id

    @property
    def weapon_pos(self):
        return self._weapon_pos

    @property
    def weapon_data(self):
        return self._weapon_data

    def is_start_after_model_loaded(self):
        return False

    def set_up_animator_param(self):
        pass

    def enter(self, **kwargs):
        pass

    def on_exit(self):
        pass

    def exit(self, cancel_state=True):
        self._cancel_state_on_exit = cancel_state
        self.on_exit()
        self.unit_com = None
        return


class GetNewGunAction(WeaponAction):
    TYPE = animation_const.HAND_STATE_GET_NEW_GUN

    def is_start_after_model_loaded(self):
        return True

    def set_up_animator_param(self):
        super(GetNewGunAction, self).set_up_animator_param()
        self.unit_com.send_event('E_HAND_ACTION', self.TYPE)
        if self.unit_com.ev_g_is_gun_pos(self._weapon_pos):
            action_id = confmgr.get('firearm_res_config', str(self._weapon_id), 'iActionType')
            if action_id is None:
                print('[error] read weapon_id = ', self._weapon_id, ' from firearm_res_config fail')
                action_id = animation_const.WEAPON_TYPE_NORMAL
            self.unit_com.send_event('E_SET_WEAPON_TYPE', action_id)
        elif self._weapon_pos > const.PART_WEAPON_POS_NONE:
            self.unit_com.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_NORMAL)
        else:
            self.unit_com.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_EMPTY_HAND)
        return

    def enter(self, **kwargs):
        super(GetNewGunAction, self).enter(**kwargs)
        self.unit_com.ev_g_status_try_trans(status_config.ST_SWITCH)
        self.unit_com.send_event('E_CLEAR_FIRESTREAM_SFX')

    def on_exit(self):
        super(GetNewGunAction, self).on_exit()
        self.unit_com.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        self.unit_com.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        self.unit_com.send_event('E_DECIDE_RELOAD_TYPE', self._weapon_pos, True)
        gun_model = self.unit_com.sd.ref_hand_weapon_model
        if self._cancel_state_on_exit:
            self.unit_com.ev_g_cancel_state(status_config.ST_SWITCH)
        if not gun_model or not self.unit_com:
            return
        bind_point = 'gun'
        is_fix_pos, equip_pos = self.unit_com.ev_g_is_fix_equip_pos(self._weapon_pos)
        if not is_fix_pos:
            model = self.unit_com.ev_g_model()
            if model:
                model.unbind(gun_model)
                model.bind(bind_point, gun_model)


class ImmediatePutOffWeaponAction(WeaponAction):
    TYPE = animation_const.HAND_STATE_NONE
    GUN_ACTION_LIST = (
     animation_const.HAND_STATE_GET_NEW_GUN, animation_const.HAND_STATE_ADD_BULLET,
     animation_const.HAND_STATE_FIRE,
     animation_const.HAND_STATE_PREPARE_THROW_BOMB, animation_const.HAND_STATE_READY_FOR_THROW_BOMB,
     animation_const.HAND_STATE_THROW_BOMB, animation_const.HAND_STATE_LOAD)

    def enter(self, **kwargs):
        import logic.gcommon.const as const
        super(ImmediatePutOffWeaponAction, self).enter(**kwargs)
        self.unit_com.send_event('E_DECIDE_RELOAD_TYPE', const.PART_WEAPON_POS_NONE, True)
        self.unit_com.ev_g_cancel_state(status_config.ST_SWITCH)
        self.unit_com.send_event('E_SET_WEAPON_TYPE', animation_const.WEAPON_TYPE_EMPTY_HAND)
        self.unit_com._unbind_all_weapon()
        hand_action = self.unit_com.ev_g_hand_action()
        if hand_action in self.GUN_ACTION_LIST:
            self.unit_com.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)


all_weapon_action = {animation_const.HAND_STATE_GET_NEW_GUN: GetNewGunAction
   }

def get_weapon_action--- This code section failed: ---

 138       0  LOAD_GLOBAL           0  'all_weapon_action'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  MAKE_FUNCTION_0       0 
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'weapon_action'

 139      18  LOAD_FAST             1  'weapon_action'
          21  POP_JUMP_IF_TRUE     39  'to 39'

 140      24  LOAD_GLOBAL           2  'Exception'
          27  LOAD_CONST            2  'Error weapon action!'
          30  CALL_FUNCTION_1       1 
          33  RAISE_VARARGS_1       1 
          36  JUMP_FORWARD          0  'to 39'
        39_0  COME_FROM                '36'

 142      39  LOAD_FAST             1  'weapon_action'
          42  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `MAKE_FUNCTION_0' instruction at offset 9