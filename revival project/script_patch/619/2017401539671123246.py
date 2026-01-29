# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8019.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gutils.screen_effect_utils import create_screen_effect_directly
import traceback
from logic.gcommon.common_const.mecha_const import DEFEND_ON, DEFEND_OFF, SP_MODULE_SLOT
from logic.gcommon.const import SOUND_TYPE_MECHA_FOOTSTEP
from logic.gcommon.common_utils.bcast_utils import E_EXECUTE_MECHA_ACTION_SOUND

class ComMechaEffect8019(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_LOAD_SHIELD_MODEL': 'on_load_shield_model',
       'E_ENTER_DEFEND': 'on_enter_defend',
       'E_EXIT_DEFEND_P': 'on_exit_defend_positive',
       'E_EXIT_DEFEND_N': 'on_exit_defend_negative',
       'E_SC_8019_S': 'on_hp_change',
       'E_8019_SEC_HOLD': 'on_sec_wp_hold',
       'E_8019_SEC_POST': 'on_sec_wp_post',
       'E_8019_SEC_EXIT': 'on_sec_wp_exit',
       'E_8019_SEC_END': 'on_sec_wp_exit',
       'E_NOTIFY_MODULE_CHANGED': 'on_module_changed',
       'E_8019_SEC_FULL': 'on_sec_wp_full'
       })
    S_ENTER = 1
    S_HIGH = 2
    S_LOW = 3
    S_EMPTY = 4
    S_EXIT = 5
    LOOP_STATE = (
     S_ENTER, S_HIGH, S_LOW)
    T_MODEL = 1
    T_SCREEN = 2
    FX_MODEL = {S_ENTER: '30',
       S_HIGH: '31',
       S_LOW: '32',
       S_EMPTY: '33',
       S_EXIT: '34'
       }
    FX_SCREEN = {S_ENTER: '40',
       S_HIGH: '41',
       S_LOW: '42',
       S_EMPTY: '43',
       S_EXIT: '44'
       }
    ATTR_DICT = {S_ENTER: 'enter',
       S_HIGH: 'high',
       S_LOW: 'low'
       }
    SEC_FX = ('50', '51')
    SEC_FULL_SOCKET = 'fx_xuli_buff'
    SEC_FULL_FX = 'effect/fx/mecha/8019/8019_vice_buff.sfx'
    SOUND_PATH = ('m_8019_weapon1_loop', 'm_8019_weapon1_nbloop')

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8019, self).init_from_dict(unit_obj, bdict)
        self.init_param()
        self.init_global_event()

    def init_param(self):
        self.mecha_model = None
        self.state = None
        self.fx_m_enter = None
        self.fx_m_high = None
        self.fx_m_low = None
        self.fx_s_enter = None
        self.fx_s_high = None
        self.fx_s_low = None
        self.player = None
        self.core_module_id = None
        self.fx_sec = None
        self.fx_sec_full = None
        self.hold_sound_name = None
        return

    def init_global_event(self):
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.player = player
        self.on_module_changed()

    def destroy(self):
        self._destroy_fx()
        self.player = None
        global_data.emgr.scene_camera_player_setted_event -= self.on_cam_lplayer_setted
        super(ComMechaEffect8019, self).destroy()
        return

    def on_load_shield_model(self, model, mecha_model):
        self.mecha_model = mecha_model
        state = self.ev_g_handy_shield_state()
        if state == DEFEND_ON:
            self.on_enter_defend()
        if self.ev_g_sec_full_tag():
            self.on_sec_wp_full()

    def on_enter_defend(self):
        self._create_fx(self.T_MODEL, self.S_ENTER)
        self._create_fx(self.T_SCREEN, self.S_ENTER)
        hp_per, hp_tag = self.ev_g_handy_shield_hp_s()
        if hp_per < 0.33:
            self.state = self.S_LOW
            self._create_fx(self.T_MODEL, self.S_LOW)
            self._create_fx(self.T_SCREEN, self.S_LOW)
        elif hp_per < 0.66:
            self.state = self.S_HIGH
            self._create_fx(self.T_MODEL, self.S_HIGH)
            self._create_fx(self.T_SCREEN, self.S_HIGH)
        else:
            self.state = self.S_ENTER

    def on_exit_defend_positive(self):
        self._remove_fx(self.T_MODEL, self.S_ENTER)
        self._remove_fx(self.T_SCREEN, self.S_ENTER)
        self._remove_fx(self.T_MODEL, self.S_LOW)
        self._remove_fx(self.T_SCREEN, self.S_LOW)
        self._remove_fx(self.T_MODEL, self.S_HIGH)
        self._remove_fx(self.T_SCREEN, self.S_HIGH)
        self._create_fx(self.T_MODEL, self.S_EXIT)
        self._create_fx(self.T_SCREEN, self.S_EXIT)
        self.state = self.S_EXIT

    def on_exit_defend_negative(self):
        self._remove_fx(self.T_MODEL, self.S_ENTER)
        self._remove_fx(self.T_SCREEN, self.S_ENTER)
        self._remove_fx(self.T_MODEL, self.S_LOW)
        self._remove_fx(self.T_SCREEN, self.S_LOW)
        self._remove_fx(self.T_MODEL, self.S_HIGH)
        self._remove_fx(self.T_SCREEN, self.S_HIGH)
        self._create_fx(self.T_MODEL, self.S_EMPTY)
        self._create_fx(self.T_SCREEN, self.S_EMPTY)
        self.state = self.S_EMPTY

    def on_hp_change(self, cur_hp, max_hp, hp_tag):
        if self.state in (self.S_EXIT, self.S_EMPTY):
            return
        hp_per = cur_hp * 1.0 / max_hp
        if hp_per < 0.33:
            state = self.S_LOW
        elif hp_per < 0.66:
            state = self.S_HIGH
        else:
            state = self.S_ENTER
        if state != self.state:
            if state == self.S_HIGH:
                self._remove_fx(self.T_MODEL, self.S_LOW)
                self._remove_fx(self.T_SCREEN, self.S_LOW)
                self._create_fx(self.T_MODEL, self.S_HIGH)
                self._create_fx(self.T_SCREEN, self.S_HIGH)
            elif state == self.S_LOW:
                self._remove_fx(self.T_MODEL, self.S_HIGH)
                self._remove_fx(self.T_SCREEN, self.S_HIGH)
                self._create_fx(self.T_MODEL, self.S_LOW)
                self._create_fx(self.T_SCREEN, self.S_LOW)
            else:
                self._remove_fx(self.T_MODEL, self.S_LOW)
                self._remove_fx(self.T_SCREEN, self.S_LOW)
                self._remove_fx(self.T_MODEL, self.S_HIGH)
                self._remove_fx(self.T_SCREEN, self.S_HIGH)
            self.state = state

    def _create_fx(self, c_type, state):
        if c_type == self.T_MODEL:
            fx_type = 'fx_m_' if 1 else 'fx_s_'
            if state in self.LOOP_STATE:
                attr = getattr(self, fx_type + self.ATTR_DICT[state], None)
                if attr:
                    self._remove_fx(fx_type, state)
            if c_type == self.T_MODEL:
                sfx_conf = self.get_readonly_effect_info()[self.FX_MODEL[state]][0]
                sfx_path = sfx_conf.get('final_correspond_path', {})
                socket_list = sfx_conf.get('socket_list', None)
                if socket_list:
                    sfx_socket = socket_list[0] if 1 else 'fx_shd_dunpai'
                    if state in self.LOOP_STATE:
                        return self.mecha_model or None
                    setattr(self, fx_type + self.ATTR_DICT[state], global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.mecha_model(), sfx_socket))
                else:
                    if not self.mecha_model:
                        return
                    global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.mecha_model(), sfx_socket)
            elif c_type == self.T_SCREEN:
                sfx_path = self.get_readonly_effect_info()[self.FX_SCREEN[state]][0]['final_correspond_path']
                return self.ev_g_is_avatar() or None
            if state in self.LOOP_STATE:
                setattr(self, fx_type + self.ATTR_DICT[state], create_screen_effect_directly(sfx_path))
            else:
                create_screen_effect_directly(sfx_path)
        return

    def _remove_fx(self, r_type, state):
        fx_type = 'fx_m_' if r_type == self.T_MODEL else 'fx_s_'
        if state in self.LOOP_STATE:
            attr = getattr(self, fx_type + self.ATTR_DICT[state], None)
            if attr:
                global_data.sfx_mgr.remove_sfx_by_id(attr)
            setattr(self, fx_type + self.ATTR_DICT[state], None)
        return

    def _destroy_fx(self):
        fx_type = 'fx_m_'
        for state in self.LOOP_STATE:
            attr = getattr(self, fx_type + self.ATTR_DICT[state], None)
            if attr:
                global_data.sfx_mgr.remove_sfx_by_id(attr)
            setattr(self, fx_type + self.ATTR_DICT[state], None)

        fx_type = 'fx_s_'
        for state in self.LOOP_STATE:
            attr = getattr(self, fx_type + self.ATTR_DICT[state], None)
            if attr:
                global_data.sfx_mgr.remove_sfx_by_id(attr)
            setattr(self, fx_type + self.ATTR_DICT[state], None)

        self.on_sec_wp_post()
        return

    def on_module_changed(self):
        if self.player:
            module_item = self.player.ev_g_mecha_installed_module(SP_MODULE_SLOT)
            if not module_item:
                self.core_module_id = None
                return
            card_id, _ = module_item
            self.core_module_id = card_id
        return

    def on_sec_wp_hold(self):
        if self.fx_sec:
            global_data.sfx_mgr.remove_sfx_by_id(self.fx_sec)
        if not self.mecha_model:
            return
        sfx_tag = self.SEC_FX[1] if self.core_module_id == 801941 else self.SEC_FX[0]
        sfx_conf = self.get_readonly_effect_info()[sfx_tag][0]
        sfx_path = sfx_conf['final_correspond_path']
        sfx_socket = sfx_conf['socket_list'][0]
        self.fx_sec = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.mecha_model(), sfx_socket)
        sound_path = self.SOUND_PATH[1] if self.core_module_id == 801941 else self.SOUND_PATH[0]
        sound_name = (sound_path, 'nf')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 1, 2, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 1, 2, SOUND_TYPE_MECHA_FOOTSTEP)], True)
        self.hold_sound_name = sound_name

    def on_sec_wp_post(self):
        if self.fx_sec:
            global_data.sfx_mgr.remove_sfx_by_id(self.fx_sec)
            self.fx_sec = None
        if self.fx_sec_full:
            global_data.sfx_mgr.remove_sfx_by_id(self.fx_sec_full)
            self.fx_sec_full = None
        sound_path = self.SOUND_PATH[1] if self.core_module_id == 801941 else self.SOUND_PATH[0]
        sound_name = (sound_path, 'nf')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_EXECUTE_MECHA_ACTION_SOUND, (0, sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)], True)
        if sound_name != self.hold_sound_name:
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, self.hold_sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
             E_EXECUTE_MECHA_ACTION_SOUND, (0, self.hold_sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)], True)
        return

    def on_sec_wp_exit(self):
        if self.fx_sec:
            global_data.sfx_mgr.remove_sfx_by_id(self.fx_sec)
            self.fx_sec = None
        sound_path = self.SOUND_PATH[1] if self.core_module_id == 801941 else self.SOUND_PATH[0]
        sound_name = (sound_path, 'nf')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_EXECUTE_MECHA_ACTION_SOUND, (0, sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)], True)
        if sound_name != self.hold_sound_name:
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 0, self.hold_sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
             E_EXECUTE_MECHA_ACTION_SOUND, (0, self.hold_sound_name, 0, 1, 0, SOUND_TYPE_MECHA_FOOTSTEP)], True)
        return

    def on_sec_wp_full(self):
        if not self.mecha_model:
            return
        if self.fx_sec_full:
            global_data.sfx_mgr.remove_sfx_by_id(self.fx_sec_full)
        self.fx_sec_full = global_data.sfx_mgr.create_sfx_on_model(self.SEC_FULL_FX, self.mecha_model(), self.SEC_FULL_SOCKET)