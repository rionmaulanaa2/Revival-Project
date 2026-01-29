# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8023.py
from __future__ import absolute_import
import six
import world
from .StateBase import StateBase
from .MoveLogic import Walk
from .JumpLogic import JumpUpPure
from .SkillLogic import AccumulateSkill
from .ShootLogic import WeaponFire, Reload
from logic.gcommon.editor import state_exporter
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from common.cfg import confmgr
from logic.gcommon.common_const.mecha_const import MECHA_8023_FORM_SNIPE, MECHA_8023_FORM_PISTOL
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from data.camera_state_const import AIM_MODE, OBSERVE_FREE_MODE
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const.mecha_const import MECHA_8023_STAND, MECHA_8023_RUN, MECHA_8023_DASH, MECHA_8023_MOVE, MECHA_8023_JUMP_1, MECHA_8023_JUMP_2
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.gcommon.const import SOUND_TYPE_MECHA_FOOTSTEP
from logic.gcommon.common_const.ui_operation_const import FAST_AIM_FIRE_8023, NO_CLOSE_AIM_LOAD_8023, AIM_RELOAD_WITHOUT_REOPEN_AIM_8023
from data.camera_state_const import MECHA_8023_DASH, MECHA_8023_SNIPE
from logic.gcommon.common_const.buff_const import BUFF_ID_MECHA_8023_SPEED_UP, BUFF_ID_MECHA_8023_SNIPE_STEALTH, BUFF_ID_MECHA_8023_DASH_STEALTH
from common.utils.timer import CLOCK
from logic.gcommon import time_utility
from logic.gcommon.component.client.com_mecha_effect.ComMechaEffect8023 import EFFECT_TYPE_INVIS, EFFECT_TYPE_DASH

@state_exporter({('anim_duration', 'param'): {'zh_name': '\xe4\xb8\x8a\xe8\x86\x9b\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf'}})
class BoltAction(StateBase):
    STATE_LOAD = 0
    STATE_AIM = 1
    BIND_EVENT = {'E_RELOADING': 'bolt_action_end',
       'E_LOADING': 'on_loading',
       'E_IGNORE_RELOAD_ANIM': 'ignore_anim',
       'E_8023_SWITCH_WEAPON_FORM': 'set_weapon_form',
       'E_ROGUE_WEAPON_INTERVAL_FACTOR': 'on_weapon_interval_factor_changed'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(BoltAction, self).init_from_dict(unit_obj, bdict, sid, info)
        weapon_id = self.custom_param.get('weapon_id', '802302')
        self.load_time = confmgr.get('firearm_config', weapon_id, 'fCDTime2', default=1.0)
        anim_duration = self.custom_param.get('anim_duration', 1.2)
        self.anim_rate = self.load_time / anim_duration
        self.ignore_load_anim = False
        self.weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)

    def ignore_anim(self, ignore):
        self.ignore_load_anim = ignore

    def set_weapon_form(self, weapon_form):
        self.weapon_form = weapon_form

    def on_loading(self):
        if self.weapon_form != MECHA_8023_FORM_SNIPE:
            return
        not self.ignore_load_anim and self.active_self()

    def on_weapon_interval_factor_changed(self, interval_factor):
        self.load_time *= 1 - interval_factor
        weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if weapon:
            weapon.interval_factor = interval_factor

    def enter(self, leave_states):
        super(BoltAction, self).enter(leave_states)
        self.delay_call(self.load_time, self.disable_self)
        self.send_event('E_ANIM_RATE', UP_BODY, self.anim_rate)

    def exit(self, enter_states):
        super(BoltAction, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_CLEAR_UP_BODY_ANIM')


@state_exporter({('open_aim_anim_rate', 'param'): {'zh_name': '\xe5\xbc\x80\xe9\x95\x9c\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe5\xba\xa6'},('close_aim_anim_rate', 'param'): {'zh_name': '\xe5\x85\xb3\xe9\x95\x9c\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe5\xba\xa6'},('exit_aim_time', 'param'): {'zh_name': '\xe5\x85\xb3\xe9\x95\x9c\xe9\x95\x9c\xe5\xa4\xb4\xe5\x88\x87\xe6\x8d\xa2\xe6\x97\xb6\xe9\x97\xb4'},('gravity_factor', 'param'): {'zh_name': '\xe6\xb5\xae\xe7\xa9\xba\xe9\x87\x8d\xe5\x8a\x9b\xe7\xb3\xbb\xe6\x95\xb0','min_val': 0.0,'max_val': 1.0},('speed_factor', 'param'): {'zh_name': '\xe6\xb5\xae\xe7\xa9\xba\xe9\x80\x9f\xe5\xba\xa6\xe7\xb3\xbb\xe6\x95\xb0','min_val': 0.0,'max_val': 1.0},('gravity_mod_time', 'param'): {'zh_name': '\xe6\xb5\xae\xe7\xa9\xba\xe6\x97\xb6\xe9\x95\xbf'},('enable_load_cam_trk', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\x90\xaf\xe6\x8b\x89\xe6\xa0\x93\xe9\x95\x9c\xe5\xa4\xb4\xe9\x9c\x87\xe5\x8a\xa8','param_type': 'bool'}})
class OpenAimCamera8023(StateBase):
    BIND_EVENT = {'E_FIRE': 'on_fire',
       'E_LOADING': 'on_loading',
       'E_RELOADING': 'on_reloading',
       'E_LEAVE_STATE': '_on_leave_state',
       'E_8023_OPEN_AIM': 'enter_aim',
       'E_8023_CLOSE_AIM': 'close_aim',
       'G_AIM_LENS': 'get_aim_lens',
       'E_PLAY_VICTORY_CAMERA': 'on_victory',
       'E_EXIT_FOCUS_CAMERA': 'close_aim',
       'E_ON_CAM_LCTARGET_SET': '_on_cam_lctarget_set',
       'E_ON_SYNC_CAM_STATE_CHANGE': '_on_sync_cam_state_change',
       'E_ON_LOSE_CONNECT': '_on_lose_connect'
       }

    def on_fire(self, *args):
        if self.is_active and self.ev_g_is_avatar():
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_8023_OPEN_AIM_FIRE, ()), True, False, True)

    def _on_leave_state(self, state, *args):
        if state in (MC_LOAD, MC_RELOAD):
            global_data.game_mgr.next_exec(self.try_end_loading)

    def try_end_loading(self):
        if not self.is_active:
            return
        cur_state = self.ev_g_cur_state()
        for ls in (MC_LOAD, MC_RELOAD):
            if ls in cur_state:
                return

        self.on_loading_end()

    def on_loading(self, *args):
        if not self.sd.ref_in_aim:
            return
        self.loading = True
        if self.enable_load_cam_trk:
            self.send_event('E_PLAY_CAMERA_TRK', '8023_SNIPE_LOAD')

    def on_reloading(self, *args):
        self.send_event('E_CLEAR_BLACK_STATE')
        self.on_loading(*args)

    def on_loading_end(self, *args):
        if not self.loading:
            return
        self.loading = False
        if self.enable_load_cam_trk:
            self.send_event('E_CANCEL_CAMERA_TRK', '8023_SNIPE_LOAD')

    def get_aim_lens(self):
        if self.sd.ref_in_aim:
            return self.aim_lens
        else:
            return None

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(OpenAimCamera8023, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.aim_closed = False
        self.loading = False
        self.ignore_btn_up = False
        self._last_cam_state = None
        self.close_callback = []
        self._restore_timer = None
        self._gravity_cache = None
        self.to_replace_anim_info = {(MC_BEAT_BACK, MC_IMMOBILIZE): (
                                         'scope_shake', {}),
           MC_STAND: (
                    'scope_shoot_idle', {}),
           MC_LOAD: (
                   'scope_load', {'only_data': True})
           }
        len_attr_data = confmgr.get('firearm_component', str(self.aim_lens), 'cAttr', default={})
        self.aim_magnitude = len_attr_data.get('iLensMagnitude', 2)
        self.open_aim_time = len_attr_data.get('fAimTime', 0.4)
        self.gravity_mod_end_time = 0
        self.gravity_mod_timer_id = None
        global_data.emgr.camera_switch_to_state_event -= self.set_camera_state
        global_data.emgr.camera_enter_free_observe_event += self.on_camera_enter_free_observe_event
        global_data.emgr.camera_leave_free_observe_event += self.on_camera_leave_free_observe_event
        global_data.emgr.scene_observed_player_setted_event += self.on_scene_observed_player_setted_event
        return

    def set_camera_state(self, state, *args):
        if state not in (AIM_MODE, OBSERVE_FREE_MODE):
            self._last_cam_state = state

    def on_camera_enter_free_observe_event(self):
        if not self.sd.ref_in_open_aim:
            return
        else:
            self.send_event('E_SHOW_MODEL')
            self.sd.ref_in_open_aim = False
            if self._last_cam_state is not None:
                global_data.emgr.switch_observe_camera_state_event.emit(self._last_cam_state)
            return

    def on_camera_leave_free_observe_event(self):
        if self.unit_obj != global_data.cam_lctarget or global_data.player.id and self.sd.ref_driver_id == global_data.player.id:
            return
        if self.is_in_cam_state():
            self.do_restore()

    def is_in_cam_state(self):
        driver_id = self.sd.ref_driver_id
        if not driver_id:
            return False
        from mobile.common.EntityManager import EntityManager
        driver = EntityManager.getentity(driver_id)
        cam_state = driver.logic.ev_g_cam_state()
        return cam_state == AIM_MODE

    def do_restore(self):
        if self.unit_obj != global_data.cam_lctarget or global_data.player.id and self.sd.ref_driver_id == global_data.player.id:
            return
        if not self.is_in_cam_state():
            return
        global_data.emgr.end_slerp_camera_early_event.emit()
        self.enter_aim()

    def on_scene_observed_player_setted_event(self, ltarget):
        if global_data.player.id and self.sd.ref_driver_id == global_data.player.id:
            return
        if not ltarget:
            self.exit(set())
            return
        if self.sd.ref_driver_id != ltarget.id:
            self.exit(set())
            self.send_event('E_OPEN_AIM_CAMERA', False)

    def _on_cam_lctarget_set(self):
        if self.unit_obj != global_data.cam_lctarget:
            return
        if global_data.cam_lplayer and global_data.player and global_data.cam_lplayer.id == global_data.player.id:
            return
        if not self.is_in_cam_state():
            return
        if self._restore_timer:
            return
        self._restore_timer = global_data.game_mgr.register_logic_timer(self.do_restore, 2, times=1)

    def _on_lose_connect(self, *args):
        if self.unit_obj != global_data.cam_lctarget:
            return
        self.exit(set())
        self.send_event('E_OPEN_AIM_CAMERA', False)

    def _on_sync_cam_state_change(self):
        self._on_cam_lctarget_set()

    def read_data_from_custom_param(self):
        from logic.gcommon.common_utils.status_utils import convert_status
        self.aim_lens = self.custom_param.get('aim_lens', 0)
        self.switch_action = self.custom_param.get('switch_action', {})
        self.open_aim_anim = self.custom_param.get('open_aim_anim', None)
        self.open_aim_duration = self.custom_param.get('open_aim_duration', 1.3)
        self.open_aim_anim_rate = self.custom_param.get('open_aim_anim_rate', 1.0)
        self.close_aim_anim = self.custom_param.get('close_aim_anim', None)
        self.close_aim_duration = self.custom_param.get('close_aim_duration', 1.0)
        self.close_aim_anim_rate = self.custom_param.get('close_aim_anim_rate', 2.0)
        self.shoot_anim = self.custom_param.get('shoot_anim', 'scope_shoot')
        self.idle_anim = self.custom_param.get('scope_anim', 'scope_idle')
        self.snipe_idle_anim = self.custom_param.get('snipe_anim', 'snipe_idle')
        self.skill_id = self.custom_param.get('skill_id', None)
        self.close_break_time = self.custom_param.get('close_break_time', self.close_aim_duration)
        self.close_break_states = self.custom_param.get('close_break_states', [MC_JUMP_1, MC_SHOOT])
        self.close_break_states = convert_status(self.close_break_states)
        self.recover_cam_state = self.custom_param.get('recover_cam_state', '20')
        self.exit_aim_time = self.custom_param.get('exit_aim_time', None)
        self.gravity_factor = self.custom_param.get('gravity_factor', 0.5)
        self.speed_factor = self.custom_param.get('speed_factor', 0.5)
        self.gravity_mod_time = self.custom_param.get('gravity_mod_time', 1.0)
        self.enable_load_cam_trk = self.custom_param.get('enable_load_cam_trk', True)
        return

    def on_init_complete(self):
        super(OpenAimCamera8023, self).on_init_complete()
        self.send_event('E_ADD_LOCK_AIM_DIR_CAM_MODE', AIM_MODE)

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        super(OpenAimCamera8023, self).action_btn_down()
        if not self.is_active:
            self.active_self()
            self.ignore_btn_up = True
        return True

    def action_btn_up(self):
        if self.ignore_btn_up:
            self.ignore_btn_up = False
            return
        super(OpenAimCamera8023, self).action_btn_up()
        self.close_aim()
        self.send_event('E_CANCEL_FIRE')

    def enter(self, leave_states):
        self.sound_custom_start()
        super(OpenAimCamera8023, self).enter(leave_states)
        self.enter_aim()
        self.send_event('E_ADD_BLACK_STATE', {MC_JUMP_1})
        self.ev_g_try_exit(MC_JUMP_1)
        if not self.ev_g_on_ground() and self.gravity_factor != 1:
            self._gravity_cache = self.sd.ref_gravity
            self.send_event('E_GRAVITY', self._gravity_cache * self.gravity_factor)
            self.gravity_mod_end_time = time_utility.time() + self.gravity_mod_time + self.open_aim_duration / self.open_aim_anim_rate + self.open_aim_time
            self.gravity_mod_timer_id = global_data.game_mgr.register_logic_timer(self.update_mod_gravity, 0.1, mode=CLOCK)

    def enter_aim(self):
        self.aim_closed = False
        self.sd.ref_in_aim_state = True
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        part = self.get_inout_anim_part()
        self.send_event('E_REPLACE_SHOOT_ANIM', self.shoot_anim)
        self.send_event('E_REPLACE_MOVE_ANIM', {'move_anim': 'scope_move_loop',
           'move_dir_type': 6,
           'start_anim': ('scope_move_start', 0.267),
           'stop_anim': ('scope_move_end', 0.433)
           }, use_new_anim=part == UP_BODY)
        for state, (anim, kwargs) in six.iteritems(self.to_replace_anim_info):
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', state, anim, **kwargs)

        self.send_event('E_ANIM_RATE', part, self.open_aim_anim_rate)
        self.send_event('E_POST_ACTION', self.open_aim_anim, part, 1)
        self.delay_call(self.open_aim_duration / self.open_aim_anim_rate, self.open_aim_camera)
        if self.ev_g_is_avatar():
            self.skill_id and self.send_event('E_DO_SKILL', self.skill_id, True)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_8023_OPEN_AIM, ()), True, False, True)

    def close_aim(self, from_exit=False, close_callback=None):
        if self.aim_closed:
            return
        else:
            self.aim_closed = True
            self.sound_custom_end()
            self.sd.ref_in_open_aim = self.sd.ref_in_aim = False
            self.sd.ref_open_aim_weapon_pos = None
            self.close_aim_camera()
            part = self.get_inout_anim_part()
            self.send_event('E_RESET_SHOOT_ANIM')
            self.send_event('E_REPLACE_MOVE_ANIM', use_new_anim=part == UP_BODY)
            for state in six.iterkeys(self.to_replace_anim_info):
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', state, None, only_data=state == MC_LOAD)

            if from_exit:
                self.close_aim_finish()
            else:
                self.send_event('E_CLEAR_UP_BODY_ANIM')
                self.send_event('E_ANIM_RATE', part, self.close_aim_anim_rate)
                self.send_event('E_POST_ACTION', self.close_aim_anim, part, 1)
                self.delay_call(self.close_aim_duration / self.close_aim_anim_rate, self.close_aim_finish)
                self.delay_call(self.close_break_time, self.close_can_break)
                if callable(close_callback):
                    self.close_callback.append(close_callback)
            if self.ev_g_is_avatar():
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_8023_CLOSE_AIM, ()), True, False, True)
            if self._gravity_cache:
                self.send_event('E_GRAVITY', self._gravity_cache)
                self._gravity_cache = None
            if self.gravity_mod_timer_id:
                global_data.game_mgr.unregister_logic_timer(self.gravity_mod_timer_id)
                self.gravity_mod_timer_id = None
            return

    def update_mod_gravity(self):
        if not self._is_valid:
            return
        else:
            cur_time = time_utility.time()
            if cur_time > self.gravity_mod_end_time:
                self.send_event('E_GRAVITY', self._gravity_cache)
                self._gravity_cache = None
                if self.gravity_mod_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self.gravity_mod_timer_id)
                    self.gravity_mod_timer_id = None
                return
            if self.speed_factor != 1.0:
                cur_dir = self.ev_g_get_walk_direction()
                self.send_event('E_SET_WALK_DIRECTION', cur_dir * self.speed_factor)
                cur_ver_speed = self.ev_g_vertical_speed()
                self.send_event('E_VERTICAL_SPEED', cur_ver_speed * self.speed_factor)
            return

    def open_aim_camera(self):
        if not self.ev_g_is_cam_target():
            return
        self.send_event('E_RECORD_CUR_CAM_AIM_DIR')
        global_data.emgr.switch_to_aim_camera_event.emit(self.aim_magnitude, self.open_aim_time, True, item_id=self.aim_lens)
        self.send_event('E_OPEN_AIM_CAMERA', True)
        self.delay_call(self.open_aim_time, self.open_aim_finish)
        self.send_event('E_HIDE_MODEL')
        if not self.ev_g_is_avatar():
            self.sd.ref_in_open_aim = self.sd.ref_in_aim = True

    def close_aim_camera(self):
        if not self.ev_g_is_cam_target():
            return
        else:
            self.send_event('E_RECORD_CUR_CAM_AIM_DIR')
            self.send_event('E_SHOW_MODEL')
            kwargs = {}
            if self.exit_aim_time is not None:
                kwargs['transfer_time'] = self.exit_aim_time
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', MECHA_8023_SNIPE, **kwargs)
            self.send_event('E_OPEN_AIM_CAMERA', False)
            return

    def open_aim_finish(self):
        if self.aim_closed:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.sd.ref_in_open_aim = self.sd.ref_in_aim = True
        self.sd.ref_open_aim_weapon_pos = PART_WEAPON_POS_MAIN2

    def on_victory(self, *args):
        if self._restore_timer:
            global_data.game_mgr.unregister_logic_timer(self._restore_timer)
            self._restore_timer = None
        self.send_event('E_SHOW_MODEL')
        return

    def close_can_break(self):
        self.send_event('E_ADD_WHITE_STATE', self.close_break_states, self.sid)

    def close_aim_finish(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_SLOW_DOWN', False)
        if self.sd.ref_up_body_anim in (self.open_aim_anim, self.close_aim_anim):
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        for cb in self.close_callback:
            callable(cb) and cb()

        self.close_callback = []
        self.disable_self()
        self.send_event('E_CLOSE_AIM_FINISH')

    def exit(self, enter_states):
        super(OpenAimCamera8023, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        if self._restore_timer:
            global_data.game_mgr.unregister_logic_timer(self._restore_timer)
            self._restore_timer = None
        self.close_aim(from_exit=True)
        self.sd.ref_in_aim_state = self.sd.ref_in_open_aim = self.sd.ref_in_aim = False
        self.close_aim_camera()
        self.skill_id and self.send_event('E_DO_SKILL', self.skill_id, False)
        self.send_event('E_LOAD_GUN', PART_WEAPON_POS_MAIN2)
        self.send_event('E_CLEAR_BLACK_STATE')
        return

    def get_inout_anim_part(self):
        part = LOW_BODY
        cur_state = self.ev_g_cur_state()
        for st in (MC_MOVE, MC_RUN):
            if st in cur_state:
                part = UP_BODY
                break

        return part

    def destroy(self):
        super(OpenAimCamera8023, self).destroy()
        if self.gravity_mod_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.gravity_mod_timer_id)
            self.gravity_mod_timer_id = None
        return


def __set_anim_rate(self):
    self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 1.5) / self.switch_anim_rate
    self.refresh_akimbo_time_l = self.custom_param.get('refresh_akimbo_time_l', 1.0) / self.switch_anim_rate
    self.refresh_akimbo_time_r = self.custom_param.get('refresh_akimbo_time_r', 1.0) / self.switch_anim_rate


@state_exporter({('switch_anim_rate', 'param'): {'param_type': 'float','zh_name': '\xe5\x88\x87\xe6\x9e\xaa\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe7\x8e\x87','post_setter': __set_anim_rate},('switch_min_duration', 'param'): {'param_type': 'float','zh_name': '\xe5\x88\x87\xe6\x9e\xaa\xe6\x9c\x80\xe7\x9f\xad\xe6\x97\xb6\xe9\x95\xbf'}})
class SwitchWeapon8023(StateBase):
    BIND_EVENT = {'E_8023_SWITCH_WEAPON_FORM': 'on_switch_finish',
       'E_MECHA_CONTROL_MAIN_INIT_COMPLETE': 'on_switch_finish',
       'G_WEAPON_FORM': 'get_weapon_form',
       'E_ENABLE_ACC_SWITCH': 'on_enable_acc_switch'
       }
    STATE_INFO = {MECHA_8023_FORM_PISTOL: {'weapon_pos': PART_WEAPON_POS_MAIN1,
                                'action_state': (
                                               (
                                                'action4', MC_SECOND_WEAPON_ATTACK),)
                                },
       MECHA_8023_FORM_SNIPE: {'weapon_pos': PART_WEAPON_POS_MAIN2,
                               'action_state': (
                                              (
                                               'action4', MC_AIM_SHOOT),)
                               }
       }
    STATE_SWITCH_START = 0

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 802352)
        self.switch_anim, self.anim_part, self.anim_dir = self.custom_param.get('switch_anim', ('sniptoaki_start',
                                                                                                'upper',
                                                                                                7))
        self.switch_anim_rate = self.custom_param.get('switch_anim_rate', 1.0)
        self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 1.5) / self.switch_anim_rate
        self.refresh_akimbo_time_l = self.custom_param.get('refresh_akimbo_time_l', 1.0) / self.switch_anim_rate
        self.refresh_akimbo_time_r = self.custom_param.get('refresh_akimbo_time_r', 1.0) / self.switch_anim_rate
        self.switch_min_duration = self.custom_param.get('switch_min_duration', 1.0)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SwitchWeapon8023, self).init_from_dict(unit_obj, bdict, sid, info)
        self.hide_akimbo = 0
        self.can_exit = False
        self.switch_duration_factor = 0.0
        self.weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)
        self.read_data_from_custom_param()
        self.enable_param_changed_by_buff()

    def on_init_complete(self):
        super(SwitchWeapon8023, self).on_init_complete()
        self.on_switch_finish()
        self.send_event('E_REFRESH_AKIMBO_MODEL')

    def action_btn_down(self):
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()
        super(SwitchWeapon8023, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(SwitchWeapon8023, self).enter(leave_states)
        self.can_exit = False
        anim_rate = 1.0 + self.switch_duration_factor
        self.send_event('E_SET_ACTION_FORBIDDEN', 'action7', True)
        self.send_event('E_ANIM_RATE', UP_BODY, self.switch_anim_rate * anim_rate)
        self.send_event('E_POST_ACTION', self.switch_anim, UP_BODY if self.anim_part == 'upper' else LOW_BODY, self.anim_dir)
        show_hand = self.weapon_form != MECHA_8023_FORM_PISTOL
        self.delay_call(self.refresh_akimbo_time_l / anim_rate, lambda : self.send_event('E_REFRESH_AKIMBO_MODEL', side='_l', show_hand=show_hand, need_sync=True))
        self.delay_call(self.refresh_akimbo_time_r / anim_rate, lambda : self.send_event('E_REFRESH_AKIMBO_MODEL', side='_r', show_hand=show_hand, need_sync=True))
        self.delay_call(self.switch_anim_duration / anim_rate, self.try_exit)
        self.delay_call(self.switch_min_duration / anim_rate, lambda : self.send_event('E_DO_SKILL', self.skill_id))
        self.play_sound('m_8023_Weapon2_sniper' if self.weapon_form == MECHA_8023_FORM_PISTOL else 'm_8023_Weapon1_pistol')
        self.send_event('E_START_SWITCH_WEAPON', self.switch_min_duration / anim_rate)
        if global_data.is_local_editor_mode:
            self.delay_call(self.switch_min_duration, lambda : self.send_event('E_8023_SWITCH_WEAPON_FORM', MECHA_8023_FORM_PISTOL if self.weapon_form == MECHA_8023_FORM_SNIPE else MECHA_8023_FORM_SNIPE))

    def try_exit(self):
        if self.can_exit:
            self.disable_self()
        else:
            self.can_exit = True

    def exit(self, enter_states):
        super(SwitchWeapon8023, self).exit(enter_states)
        self.send_event('E_SET_ACTION_FORBIDDEN', 'action7', False)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        if self.sd.ref_up_body_anim == self.last_switch_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_REFRESH_AKIMBO_MODEL')

    def on_switch_finish(self, weapon_form=None):
        if weapon_form is None:
            weapon_form = self.weapon_form
        else:
            self.weapon_form = weapon_form
            if self.ev_g_is_avatar():
                global_data.emgr.on_cancel_reload_event.emit()
        mecha_id = str(self.sd.ref_mecha_id)
        to_switch_id = '{}_{}'.format(mecha_id, weapon_form) if weapon_form else mecha_id
        self.send_event('E_REFRESH_CUR_WEAPON_BULLET', self.STATE_INFO[weapon_form]['weapon_pos'])
        self.send_event('E_REFRESH_STATE_PARAM', to_switch_id, True)
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_RELOAD}, self.sid)
        for action_btn, action_state in self.STATE_INFO[weapon_form]['action_state']:
            self.send_event('E_SWITCH_ACTION', action_btn, action_state)

        self.send_event('E_SWITCH_WEAPON')
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_AIM_SHOOT}, self.sid)
        self.is_active and self.try_exit()
        self.send_event('E_LOAD_GUN', PART_WEAPON_POS_MAIN2)
        return

    def refresh_param_changed(self):
        self.read_data_from_custom_param()

    def refresh_action_param(self, action_param, custom_param):
        super(SwitchWeapon8023, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.last_switch_anim = self.switch_anim
            self.read_data_from_custom_param()

    def get_weapon_form(self):
        return self.weapon_form

    def destroy(self):
        super(SwitchWeapon8023, self).destroy()

    def play_sound(self, event):
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, (event, 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, (event, 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)

    def on_enable_acc_switch(self):
        self.acc_switch_enable = True


@state_exporter({('opacity', 'param'): {'zh_name': '\xe9\x9a\x90\xe8\xba\xab\xe7\x89\xb9\xe6\x95\x88\xe9\x80\x8f\xe6\x98\x8e\xe5\xba\xa6','min_val': 0,'max_val': 1}})
class Invisibility(StateBase):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_all_model_loaded',
       'E_8023_SWITCH_WEAPON_FORM': 'set_weapon_form',
       'E_STEALTH_ON': 'set_sfx_on',
       'E_UPDATE_LOD': 'refresh_refr_model_visible',
       'E_BUFF_ADD_DATA': 'on_add_buff',
       'E_BUFF_DEL_DATA': 'on_del_buff',
       'G_POWERFUL_SNIPE': 'get_powerful_snipe'
       }
    STEALTH_END_EFFECT_ID = '101'
    STEALTH_EFFECT_ID = '102'
    DISTORTION_EFFECT_ID = '103'
    STEALTH_START_EFFECT_ID = '108'
    COST_CD_STATES = {MC_STAND: MECHA_8023_STAND,
       MC_MOVE: MECHA_8023_MOVE,
       MC_RUN: MECHA_8023_RUN,
       MC_DASH: MECHA_8023_DASH,
       MC_JUMP_1: MECHA_8023_JUMP_1,
       MC_JUMP_2: MECHA_8023_JUMP_2
       }
    SNIPE_STEALTH_BREAK_STATES = {
     MC_MOVE, MC_RUN, MC_DASH, MC_SECOND_WEAPON_ATTACK, MC_SHOOT}

    def set_weapon_form(self, weapon_form):
        if self.refr_model:
            self.refr_model.play_animation('snipe_aim' if weapon_form else 'idle')

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 802354)
        self.opacity = self.custom_param.get('opacity', 0.3)
        self.show_refr_lod = self.custom_param.get('show_refr_lod', ('l', 'l1'))

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Invisibility, self).init_from_dict(unit_obj, bdict, sid, info)
        self.cur_weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)
        self.cur_invisible = bdict.get('invisible', False)
        self.stealth_sfx_id = None
        self.distortion_sfx_id = None
        self.screen_sfx_id = None
        self.mec_model = None
        self.refr_model = None
        self.all_model_loaded = False
        self._block_refr = False
        self.snipe_stealth_valid = False
        self.dash_stealth_valid = False
        self.distortion_sfx_path = None
        self.is_sp = 0
        self.enable_param_changed_by_buff()
        self.read_data_from_custom_param()
        return

    def refresh_param_changed(self):
        if self.ev_g_is_avatar() or self.ev_g_is_cam_target():
            self.send_event('E_8023_POWERFUL_SNIPE' if self.is_sp and self.cur_invisible else 'E_8023_POWERFUL_SNIPE_END')

    def get_powerful_snipe(self):
        return self.is_sp and self.cur_invisible

    def on_model_loaded(self, mec_model):
        self.mec_model = mec_model

    def on_all_model_loaded(self, *args):
        self.all_model_loaded = True
        refr_model = self.sd.ref_socket_res_agent.model_res_map.get('distortion', (None, ))
        if refr_model:
            self.refr_model = refr_model[0]
            self.refr_model.inherit_flag &= ~world.INHERIT_VISIBLE
            self.refr_model.set_inherit_parent_shaderctrl(False)
        self.set_weapon_form(self.cur_weapon_form)
        self.set_sfx_on(self.cur_invisible, force=True)
        return None

    def enter(self, leave_states):
        super(Invisibility, self).enter(leave_states)
        self.set_sfx_on(True)

    def update(self, dt):
        super(Invisibility, self).update(dt)
        if not self.snipe_stealth_valid and not self.dash_stealth_valid:
            self.disable_self()

    def exit(self, enter_states):
        super(Invisibility, self).exit(enter_states)
        self.set_sfx_on(False)

    def set_sfx_on(self, on, force=False):
        if not force and self.cur_invisible == on:
            return
        else:
            self.cur_invisible = on
            if not self.all_model_loaded:
                return
            is_avatar = self.ev_g_is_avatar()
            is_cam_target = is_avatar or self.ev_g_is_cam_target()
            if is_cam_target:
                if self.is_sp:
                    self.send_event('E_8023_POWERFUL_SNIPE' if on else 'E_8023_POWERFUL_SNIPE_END')
                self.send_event('E_ENABLE_SFX_SYNC', not on)
                self.send_event('E_BLOCK_LC_EFFECT', on)
            else:
                self.send_event('E_HIDE_ALL_BUFF_SFX', on)
                self.send_event('E_HIDE_ALL_STATE_UI', on)
                self.send_event('E_ENABLE_HP_UI', not on)
                self.send_event('E_BLOCK_FLAG', on)
                self.send_event('E_HIDE_SHIELD_SFX', on)
                self.send_event('E_BLOCK_ANIM_EFFECT', on)
                self.send_event('E_ENABLE_SFX_SYNC', not on)
                if not on and global_data.is_multi_pass_support:
                    self.send_event('E_REFRESH_MODEL')
            self.send_event('E_SHOW_SCREEN_EFFECT', on, EFFECT_TYPE_INVIS)
            if not is_avatar or not self.sd.ref_in_aim:
                self.send_event('E_TRIGGER_STATE_EFFECT', 'stealth_start', self.STEALTH_START_EFFECT_ID if on else self.STEALTH_END_EFFECT_ID)
            self.send_event('E_TRIGGER_STATE_EFFECT', 'stealth', self.STEALTH_EFFECT_ID if on else '')
            self.send_event('E_SET_DAMAGE_EFFECT_VISIBLE', not on)
            self.send_event('E_BLOCK_EFFECT_SFX', on)
            self.send_event('E_HIDE_EFFECT_WHEN_INVISIBLE', on)
            self.send_event('E_DISABLE_TRANSPARENT', on)
            self.mec_model.enable_prez_transparent(on, self.opacity)
            for key in ('akimbo_hand_r', 'akimbo_hand_l', 'akimbo_leg_r', 'akimbo_leg_l'):
                sub_model = self.sd.ref_socket_res_agent.model_res_map.get(key, None)
                if not sub_model or not sub_model[0]:
                    continue
                sub_model[0].enable_prez_transparent(on, self.opacity)

            self.refresh_refr_model_visible()
            if is_cam_target:
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_STEALTH_ON, (on,)), True, False, True)
            return

    def refresh_refr_model_visible(self, lod_level=None):
        if not self.refr_model or not self.refr_model.valid:
            return
        else:
            need_show_refr_model = not self._block_refr and self.ev_g_is_cam_target() or (lod_level or self.ev_g_lod_level()) in self.show_refr_lod
            if self.cur_invisible and need_show_refr_model:
                if not self.distortion_sfx_path:
                    readonly_effect = self.ev_g_mecha_readonly_effect_info()
                    self.distortion_sfx_path = readonly_effect[self.DISTORTION_EFFECT_ID][0]['final_correspond_path']
                self.distortion_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.distortion_sfx_path, self.refr_model, 'fx_root', on_create_func=lambda *args: global_data.game_mgr.next_exec(self.set_refr_model_visible, False))
            else:
                self.refr_model.visible = False
                if self.distortion_sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self.distortion_sfx_id)
                    self.distortion_sfx_id = None
            return

    def set_refr_model_visible(self, visible):
        if self.refr_model and self.refr_model.valid:
            self.refr_model.visible = visible

    def destroy(self):
        super(Invisibility, self).destroy()
        self.refr_model = None
        if self.distortion_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.distortion_sfx_id)
            self.distortion_sfx_id = None
        self.all_model_loaded = False
        self.send_event('E_SHOW_SCREEN_EFFECT', False, EFFECT_TYPE_INVIS)
        return

    def on_add_buff(self, buff_key, buff_id, buff_idx, data, is_init=False):
        if buff_id == BUFF_ID_MECHA_8023_SNIPE_STEALTH:
            self.snipe_stealth_valid = True
        elif buff_id == BUFF_ID_MECHA_8023_DASH_STEALTH:
            self.dash_stealth_valid = True
        else:
            return
        self.refresh_stealth_state()

    def on_del_buff(self, buff_key, buff_id, buff_idx):
        if buff_id == BUFF_ID_MECHA_8023_SNIPE_STEALTH:
            self.snipe_stealth_valid = False
        elif buff_id == BUFF_ID_MECHA_8023_DASH_STEALTH:
            self.dash_stealth_valid = False
        else:
            return
        self.refresh_stealth_state()

    def refresh_stealth_state(self):
        stealth_on = self.snipe_stealth_valid or self.dash_stealth_valid
        if stealth_on:
            self.active_self()
        else:
            self.disable_self()


class Walk8023(Walk):
    BIND_EVENT = Walk.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REPLACE_MOVE_ANIM': 'replace_move_anim',
       'E_8023_SWITCH_WEAPON_FORM': 'on_switch_finish'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Walk8023, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.aim_tag = False
        self.end_sound_tag = False
        self.use_new_anim_after_ap_refresh = False

    def enter(self, leave_states):
        super(Walk8023, self).enter(leave_states)
        if self.aim_tag:
            self.start_sp_move_sound()

    def exit(self, enter_states):
        super(Walk8023, self).exit(enter_states)
        if self.end_sound_tag:
            self.stop_sp_move_sound()

    def update(self, dt):
        super(Walk8023, self).update(dt)
        spd = self.sd.ref_cur_speed
        if spd > 81 or spd < 1:
            if self.aim_tag and self.end_sound_tag:
                self.stop_sp_move_sound()

    def destroy(self):
        super(Walk8023, self).destroy()
        self.play_sound('m_8023_Weapon2_sniper_scope_move_lp', 0, True)

    def replace_move_anim(self, move_anim_info=None, use_new_anim=False):
        if move_anim_info is None:
            self.move_anim = self.custom_param.get('move_anim', None)
            self.move_dir_type = self.custom_param.get('move_dir_type', 6)
            self.move_start_anim, self.start_time = self.custom_param.get('start_anim', (None,
                                                                                         0))
            self.move_stop_anim, self.stop_time = self.custom_param.get('stop_anim', (None,
                                                                                      0))
            self.aim_tag = False
            if self.end_sound_tag:
                self.stop_sp_move_sound()
        else:
            self.move_anim = move_anim_info.get('move_anim', self.move_anim)
            self.move_dir_type = move_anim_info.get('move_dir_type', self.move_dir_type)
            self.move_start_anim, self.start_time = move_anim_info.get('start_anim', (self.move_start_anim, self.start_time))
            self.move_stop_anim, self.stop_time = move_anim_info.get('stop_anim', (self.move_stop_anim, self.stop_time))
            self.aim_tag = True
            if self.is_valid() and not self.end_sound_tag:
                self.start_sp_move_sound()
        self.reset_sub_states_callback()
        if self.move_start_anim or self.move_stop_anim or self.move_anim:
            self.register_substate_callback(self.STATE_START, 0, self.start_cb)
            self.register_substate_callback(self.STATE_MOVE, 0, self.move_cb)
            self.register_substate_callback(self.STATE_STOP, 0, self.stop_cb)
        if use_new_anim:
            self.send_event('E_POST_ACTION', self.move_anim, LOW_BODY, self.move_dir_type, loop=True)
        return

    def on_switch_finish(self, *args):
        if self.is_active:
            self.use_new_anim_after_ap_refresh = True

    def refresh_action_param(self, action_param, custom_param):
        super(Walk8023, self).refresh_action_param(action_param, custom_param)
        if self.use_new_anim_after_ap_refresh:
            self.send_event('E_POST_ACTION', self.move_anim, LOW_BODY, self.move_dir_type, loop=True)
            self.use_new_anim_after_ap_refresh = False

    def start_cb(self):
        self.send_event('E_POST_ACTION', self.move_start_anim, LOW_BODY, 6)
        self.change_state(self.STATE_MOVE)

    def move_cb(self):
        self.send_event('E_POST_ACTION', self.move_anim, LOW_BODY, self.move_dir_type, loop=True)

    def stop_cb(self):
        self.send_event('E_POST_ACTION', self.move_stop_anim, LOW_BODY, 6)
        self.send_event('E_ACTIVE_STATE', self.STAND_STATE)

    def start_sp_move_sound(self):
        self.play_sound('m_8023_Weapon2_sniper_scope_move_start')
        self.play_sound('m_8023_Weapon2_sniper_scope_move_lp', 1, True)
        self.end_sound_tag = True

    def stop_sp_move_sound(self):
        self.play_sound('m_8023_Weapon2_sniper_scope_move_end')
        self.play_sound('m_8023_Weapon2_sniper_scope_move_lp', 0, True)
        self.end_sound_tag = False

    def play_sound(self, event, control_type=1, loop=False):
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', control_type, (event, 'nf'), 0, loop, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_EXECUTE_MECHA_ACTION_SOUND, (control_type, (event, 'nf'), 0, loop, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)


class JumpUp8023(JumpUpPure):
    BIND_EVENT = {'E_ENABLE_REINFORCE_JUMP': 'on_enable_reinforce_jump'
       }

    def action_btn_down(self):
        if self.sd.ref_in_aim:
            return
        return super(JumpUp8023, self).action_btn_down()

    def on_enable_reinforce_jump(self, enable, add_factor=0.0):
        self.extra_jump_speed_scale = 1.0
        if enable:
            self.extra_jump_speed_scale += add_factor


class WeaponFire8023(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_8023_SWITCH_WEAPON_FORM': 'set_weapon_form',
       'E_CANCEL_FIRE': 'cancel_fire',
       'E_CLOSE_AIM_FINISH': 'close_aim_finish'
       })

    @property
    def is_avatar(self):
        if self._is_avatar is None:
            self._is_avatar = self.ev_g_is_avatar()
        return self._is_avatar

    @property
    def fast_aim_shoot(self):
        if self._fast_aim_shoot is None:
            self._fast_aim_shoot = bool(self.is_avatar and global_data.player.get_setting_2(FAST_AIM_FIRE_8023))
        return self._fast_aim_shoot

    @property
    def no_close_aim_load(self):
        if self._no_close_aim_load is None:
            self._no_close_aim_load = bool(self.is_avatar and global_data.player.get_setting_2(NO_CLOSE_AIM_LOAD_8023))
        return self._no_close_aim_load

    @property
    def reload_without_reopen(self):
        if self._reload_without_reopen is None:
            self._reload_without_reopen = bool(self.is_avatar and global_data.player.get_setting_2(AIM_RELOAD_WITHOUT_REOPEN_AIM_8023))
        return self._reload_without_reopen

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8023, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._btn_holding = False
        self._doing_fast_aim_shoot = False
        self._reopen_aim = False
        self._can_fire_end = False
        self.fire_canceled = False
        self.attack_end_after_close_aim = False
        self.cur_weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)
        self.can_close_aim = False
        self._is_avatar = None
        self._fast_aim_shoot = None
        self._no_close_aim_load = None
        self._reload_without_reopen = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_fast_aim_fire_8023': self.update_fast_aim_shoot,
           'update_no_close_aim_load_8023': self.update_no_close_aim_load,
           'update_reload_without_reopen_8023': self.update_reload_without_reopen
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_fast_aim_shoot(self, flag):
        self._fast_aim_shoot = flag

    def update_no_close_aim_load(self, flag):
        self._no_close_aim_load = flag

    def update_reload_without_reopen(self, flag):
        self._reload_without_reopen = flag

    def action_btn_down(self, ignore_reload=False):
        if self.cur_weapon_form == MECHA_8023_FORM_PISTOL:
            super(WeaponFire8023, self).action_btn_down(ignore_reload)
            return
        if self.fire_canceled:
            return
        from logic.comsys.battle.BattleUtils import can_fire
        if not self.sd.ref_is_robot and (ShotChecker().check_camera_can_shot() or not can_fire()) or self.ev_g_reloading() or self.ev_g_weapon_reloading(self.weapon_pos) or not self.ev_g_weapon_loaded(self.weapon_pos):
            return False
        self.is_continue_fire = self.want_to_fire = True
        if not self.check_can_active() or not self.ev_g_is_weapon_enable(self.weapon_pos) or self.ev_g_is_diving():
            self.is_continue_fire = False
            self.can_not_fire_attack()
            return False
        if self._doing_fast_aim_shoot or not self.sd.ref_in_aim_state and self.fast_aim_shoot:
            self._doing_fast_aim_shoot = True
            if MC_AIM_SHOOT not in self.ev_g_cur_state():
                self.send_event('E_ACTIVE_STATE', MC_AIM_SHOOT)
        else:
            if not self.try_weapon_attack_begin():
                self.is_continue_fire = False
                return False
            if self.is_active:
                self.re_enter()
            self.active_self()
            self._can_fire_end = self.no_close_aim_load
            self.send_event('E_SET_AUTO_LOAD', not (self.sd.ref_in_aim_state or self._fast_aim_shoot), PART_WEAPON_POS_MAIN2)
        self.can_close_aim = True
        super(WeaponFire, self).action_btn_down()
        return True

    def action_btn_up(self):
        if self.cur_weapon_form == MECHA_8023_FORM_PISTOL:
            super(WeaponFire8023, self).action_btn_up()
            return
        if self.want_to_fire and self._doing_fast_aim_shoot and not self.fire_canceled and self.check_can_active() and self.try_weapon_attack_begin():
            self.active_self()
            self._can_fire_end = True
        elif not self.no_close_aim_load:
            self.fire_end()
        self.is_continue_fire = self.want_to_fire = False
        super(WeaponFire, self).action_btn_up()
        self.fire_canceled = False
        return True

    def attack_end(self):
        self._doing_fast_aim_shoot = False
        self.send_event('E_SET_AUTO_LOAD', True, PART_WEAPON_POS_MAIN2)
        self.try_weapon_attack_end()

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        super(WeaponFire8023, self).on_fire(f_cdtime, weapon_pos, fired_socket_index)
        if self.cur_weapon_form == MECHA_8023_FORM_SNIPE:
            self.fire_end()

    def fire_end(self):
        if not self._can_fire_end:
            self._can_fire_end = True
            return
        no_close_aim_load = self.no_close_aim_load
        if no_close_aim_load:
            weapon = self.ev_g_wpbar_get_by_pos(self.weapon_pos)
            if weapon and weapon.get_bullet_num() < weapon.get_cost_ratio() and self.reload_without_reopen:
                no_close_aim_load = False
        if no_close_aim_load and not self._doing_fast_aim_shoot:
            self.attack_end()
        elif self.can_close_aim:
            self.send_event('E_8023_CLOSE_AIM')
            self.can_close_aim = False
            if self.sd.ref_in_aim_state:
                self.attack_end_after_close_aim = True
            else:
                self.attack_end()

    def set_weapon_form(self, weapon_form):
        self.cur_weapon_form = weapon_form

    def cancel_fire(self):
        if self.want_to_fire:
            self.fire_canceled = True

    def close_aim_finish(self):
        if self.attack_end_after_close_aim:
            self.attack_end()
            self.attack_end_after_close_aim = False


@state_exporter({('track_extra_speed', 'param'): {'zh_name': '\xe8\xbd\xa8\xe8\xbf\xb9\xe9\xa2\x9d\xe5\xa4\x96\xe9\x80\x9f\xe5\xba\xa6'},('track_extra_g', 'param'): {'zh_name': '\xe8\xbd\xa8\xe8\xbf\xb9\xe9\xa2\x9d\xe5\xa4\x96\xe9\x87\x8d\xe5\x8a\x9b'},('track_extra_up', 'param'): {'zh_name': '\xe8\xbd\xa8\xe8\xbf\xb9\xe9\xa2\x9d\xe5\xa4\x96\xe4\xb8\x8a\xe6\x89\xac\xe8\xa7\x92'}})
class ThrowGrenade8023(AccumulateSkill):
    BIND_EVENT = AccumulateSkill.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SKILL_BUTTON_BOUNDED': 'on_skill_button_bounded'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(ThrowGrenade8023, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.sub_skill_id = self.custom_param.get('sub_skill_id', 802356)
        self.track_extra_speed = self.custom_param.get('track_extra_speed', 0)
        self.track_extra_g = self.custom_param.get('track_extra_g', 0)
        self.track_extra_up = self.custom_param.get('track_extra_up', 0)

    def on_skill_button_bounded(self, skill_id):
        if skill_id != self.skill_id:
            return
        self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)

    def action_btn_down(self):
        if not self.ev_g_can_cast_skill(self.sub_skill_id):
            return
        return super(ThrowGrenade8023, self).action_btn_down()

    def enter(self, leave_states):
        super(ThrowGrenade8023, self).enter(leave_states)
        self.play_sound('m_8023_weapon_grenade_action')
        self.sd.ref_socket_res_agent.set_model_res_visible(False, 'akimbo_hand_r')
        self.sd.ref_socket_res_agent.set_model_res_visible(False, 'akimbo_hand_l')
        self.show_track(True)
        self.send_event('E_SHOW_TOWER_RANGE', self.skill_id)

    def show_track(self, show):
        if not self._show_track:
            return
        if show:
            self.send_event('E_SHOW_ACC_WP_TRACK', self.track_extra_speed, self.track_extra_g, self.track_extra_up)
        else:
            self.send_event('E_STOP_ACC_WP_TRACK')

    def exit(self, enter_states):
        super(ThrowGrenade8023, self).exit(enter_states)
        self.sd.ref_socket_res_agent.set_model_res_visible(True, 'akimbo_hand_r')
        self.sd.ref_socket_res_agent.set_model_res_visible(True, 'akimbo_hand_l')

    def do_skill(self, is_quick_attack=False):
        self.sub_state = self.STATE_POST
        self.show_track(False)
        self.play_sound('m_8023_weapon_grenade_throw')
        if self.up_bone:
            self.send_event('E_POST_EXTERN_ACTION', self.post_anim, True)
        else:
            self.send_event('E_POST_ACTION', self.post_anim, UP_BODY, 1, loop=False, blend_time=0)
            self.replace_stand(self.post_anim, False)
        self.replace_move(None)
        if self.post_forbid_state:
            self.send_event('E_ADD_BLACK_STATE', self.post_forbid_state)
            self.send_event('E_BRAKE')
        import world
        scn = world.get_active_scene()
        camera = scn.active_camera
        self.fire_forward = camera.rotation_matrix.forward
        self.fire_position = camera.position

        def delay_do_skill():
            if not self or not self.is_valid():
                return
            self.send_event('E_DO_SKILL', self.skill_id, 0, self.fire_position, self.fire_forward)
            self.send_event('E_DO_SKILL', self.sub_skill_id)

        global_data.game_mgr.next_exec(delay_do_skill)
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        if self.shoot_aim_ik:
            self.send_event('E_ENABLE_AIM_IK', False)
        self.send_event('E_STOP_TOWER_RANGE', self.skill_id)
        return

    def play_sound(self, event):
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, (event, 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, (event, 'nf'), 0, 0, 1, SOUND_TYPE_MECHA_FOOTSTEP)], True)


class Reload8023(Reload):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8023, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.reload_without_reopen_setting_key = AIM_RELOAD_WITHOUT_REOPEN_AIM_8023
        self.trk_playing = False

    def reload_without_reopen(self):
        if self.reload_without_reopen_setting_key is not None and self.ev_g_is_avatar():
            setting_val = global_data.player.get_setting_2(self.reload_without_reopen_setting_key)
            return bool(setting_val)
        else:
            return False

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.reloaded:
            return False
        if self.ev_g_aim_switching():
            return
        if self.sd.ref_in_aim and self.reload_without_reopen():
            self.send_event('E_8023_CLOSE_AIM', close_callback=lambda : self.send_event('E_TRY_RELOAD', self.weapon_pos))
        else:
            self.send_event('E_TRY_RELOAD', self.weapon_pos)
        super(Reload, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(Reload8023, self).enter(leave_states)
        if self.sd.ref_in_aim:
            self.send_event('E_PLAY_CAMERA_TRK', '8023_SNIPE_RELOAD')
            self.trk_playing = True

    def exit(self, enter_states):
        super(Reload8023, self).exit(enter_states)
        if self.trk_playing:
            self.send_event('E_CANCEL_CAMERA_TRK', '8023_SNIPE_RELOAD')
        self.trk_playing = False


class DashBuff8023(StateBase):
    BIND_EVENT = {'E_BUFF_ADD_DATA': 'on_add_buff',
       'E_BUFF_DEL_DATA': 'on_del_buff',
       'E_8023_SWITCH_WEAPON_FORM': 'set_weapon_form',
       'E_OPEN_AIM_CAMERA': 'on_open_aim_camera'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DashBuff8023, self).init_from_dict(unit_obj, bdict, sid, info)
        self.bind_action_id = bdict.get('bind_action_id', 0)
        self.cur_weapon_form = bdict.get('weapon_form', MECHA_8023_FORM_PISTOL)
        self.skill_id = self.custom_param.get('skill_id', 802354)
        self.cur_in_aim = False
        self.buff_valid = False

    def action_btn_down(self):
        super(DashBuff8023, self).action_btn_down()
        if self.is_active or not self.ev_g_can_cast_skill(self.skill_id):
            return False
        self.send_event('E_DO_SKILL', self.skill_id)

    def enter(self, leave_states):
        super(DashBuff8023, self).enter(leave_states)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        if self.cur_in_aim:
            self.send_event('E_8023_CLOSE_AIM')
            self.send_event('E_CANCEL_FIRE')
        else:
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', MECHA_8023_DASH, transfer_time=0.2)
            self.send_event('E_SHOW_SCREEN_EFFECT', True, EFFECT_TYPE_DASH)

    def update(self, delta_time):
        super(DashBuff8023, self).update(delta_time)
        if not self.buff_valid:
            self.disable_self()

    def exit(self, enter_states):
        super(DashBuff8023, self).exit(enter_states)
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        if not self.cur_in_aim:
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', MECHA_8023_SNIPE, transfer_time=0.2)
        self.send_event('E_SHOW_SCREEN_EFFECT', False, EFFECT_TYPE_DASH)

    def on_add_buff(self, buff_key, buff_id, buff_idx, data, is_init=False):
        if not self.is_active and buff_id == BUFF_ID_MECHA_8023_SPEED_UP:
            self.active_self()
            self.buff_valid = True

    def on_del_buff(self, buff_key, buff_id, buff_idx):
        if self.is_active and buff_id == BUFF_ID_MECHA_8023_SPEED_UP:
            self.disable_self()
            self.buff_valid = False

    def set_weapon_form(self, weapon_form):
        self.cur_weapon_form = weapon_form

    def on_open_aim_camera(self, open):
        self.cur_in_aim = open
        if not self.is_active:
            return
        if not open:
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', MECHA_8023_DASH, transfer_time=0.0)
        self.send_event('E_SHOW_SCREEN_EFFECT', not open, EFFECT_TYPE_DASH)