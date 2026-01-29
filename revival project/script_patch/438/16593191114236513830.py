# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8026.py
from __future__ import absolute_import
import world
import math3d
from common.cfg import confmgr
from logic.gcommon import editor
from logic.gcommon.const import NEOX_UNIT_SCALE
from .StateBase import StateBase
from .ShootLogic import WeaponFire, Reload
from .MoveLogic import Walk
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3, PART_WEAPON_POS_MAIN4
from common.utils.timer import LOGIC
from logic.gcommon.time_utility import get_server_time
from logic.vscene.parts import PartCtrl
from logic.gcommon.common_const import attr_const
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.common_const.ui_operation_const import DRAG_DASH_BTN_8026

@editor.state_exporter({('powerup_post_cd', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x8a\x9b\xe5\x87\xbb\xe5\x90\x8e\xe6\x91\x87\xe6\x97\xb6\xe9\x95\xbf','param_type': 'float'},('max_energy', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x8a\x9b\xe5\x87\xbb\xe8\x93\x84\xe5\x8a\x9b\xe6\x97\xb6\xe9\x95\xbf'}})
class WeaponFire8026(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SET_ENERGY_FULL': 'set_energy_full',
       'E_WEAPON_BULLET_CHG': 'on_reloaded',
       'E_ATTACK_START': ('on_fire_end', 99),
       'E_DO_SKILL': 'on_do_skill'
       })

    def read_data_from_custom_param(self):
        super(WeaponFire8026, self).read_data_from_custom_param()
        self.powerup_anim = self.custom_param.get('powerup_anim', 'powerup_shoot')
        self.all_shoot_anim.add(self.powerup_anim)
        self.powerup_post_cd = self.custom_param.get('powerup_post_cd', 0.3)
        self.max_energy = self.custom_param.get('max_energy', 3)
        self._last_states = None
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8026, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.cur_energy = 0
        self.is_powerup = False
        self._last_tick_ts = get_server_time()
        if self.ev_g_is_avatar():
            self.charge_timer = global_data.game_mgr.register_logic_timer(self.charge_tick, interval=1, times=-1, mode=LOGIC)
        else:
            self.charge_timer = None
        self.fire_cd = -1
        self.is_sp = False
        self.continue_fire_count = 0
        self.max_continue_fire = 4
        self.enable_param_changed_by_buff()
        self.is_breakthrough_5_1_sp = False
        return

    def on_post_init_complete(self, *args):
        super(WeaponFire8026, self).on_post_init_complete(*args)
        self.set_energy(self.cur_energy)

    def action_btn_down(self, ignore_reload=False):
        super(WeaponFire8026, self).action_btn_down(ignore_reload)

    def action_btn_up(self):
        super(WeaponFire8026, self).action_btn_up()
        self.continue_fire_count = 0

    def try_weapon_attack_begin(self):
        if self.fire_cd > 0:
            return False
        self.weapon_pos = PART_WEAPON_POS_MAIN2 if self.is_powerup else PART_WEAPON_POS_MAIN1
        self.shoot_anim = self.powerup_anim if self.is_powerup else self._nl_shoot_anim
        return self.ev_g_try_bind_weapon_attack_begin(0)

    def try_weapon_attack_end(self, is_cancel=False):
        return self.ev_g_try_bind_weapon_attack_end(0)

    def charge_tick(self):
        cur_time = get_server_time()
        dt = cur_time - self._last_tick_ts
        self._last_tick_ts = cur_time
        cur_states = self.ev_g_cur_state()
        no_charge_states = {MC_DASH, MC_DEFEND, MC_SECOND_WEAPON_ATTACK}
        and_states = cur_states & no_charge_states
        if and_states and cur_states != self._last_states:
            self.set_energy(0)
        elif not self.is_powerup and not self.ev_g_reloading() and not self.want_to_fire:
            self.set_energy(self.cur_energy + dt)
        if self.fire_cd > 0:
            self.fire_cd -= dt
        self._last_states = cur_states

    def set_energy_full(self):
        self.set_energy(self.max_energy)

    def set_energy(self, energy):
        if energy == self.cur_energy:
            return
        self.cur_energy = energy
        is_powerup = self.cur_energy >= self.max_energy
        if is_powerup != self.is_powerup:
            self.is_powerup = is_powerup
            new_weapon_pos = PART_WEAPON_POS_MAIN2 if self.is_powerup else PART_WEAPON_POS_MAIN1
            self.send_event('E_SWITCH_BIND_WEAPON', 0, new_weapon_pos)
        self.send_event('E_WEAPON_POWERUP', energy / self.max_energy)

    def on_fire_end(self, weapon_pos):
        self.set_energy(0)
        if weapon_pos == PART_WEAPON_POS_MAIN2:
            self.fire_cd = self.powerup_post_cd
            self.continue_fire_count = 0
        elif self.is_sp:
            self.continue_fire_count += 1
            if self.continue_fire_count >= self.max_continue_fire:
                self.set_energy_full()

    def destroy(self):
        super(WeaponFire8026, self).destroy()
        global_data.game_mgr.unregister_logic_timer(self.charge_timer)
        self.charge_timer = None
        return

    def on_reloaded(self, *args):
        if self.is_sp:
            self.set_energy_full()

    def on_do_skill(self, *args):
        if self.is_breakthrough_5_1_sp:
            self.set_energy_full()


class Reload8026(Reload):

    def on_reloading_bullet(self, time, times, weapon_pos):
        if weapon_pos not in (PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2):
            return
        self.reload_time = time
        if not self.ignore_anim:
            self.active_self()


@editor.state_exporter({('shield_start_len', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x9b\xbe\xe6\x8a\xac\xe6\x89\x8b\xe6\x97\xb6\xe9\x95\xbf',
                                   'getter': lambda self: self.shield_start_anim_len * self.shield_start_anim_rate,
                                   'setter': --- This code section failed: ---

 156       0  LOAD_GLOBAL           0  'setattr'
           3  LOAD_GLOBAL           1  'shield_start_anim_len'
           6  LOAD_FAST             1  'value'
           9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             1  'shield_start_anim_len'
          15  BINARY_DIVIDE    
          16  CALL_FUNCTION_3       3 
          19  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_3' instruction at offset 16
,'param_type': 'float'
                                   },
   ('shield_end_break', 'param'): {'zh_name': '\xe6\x94\xb6\xe7\x9b\xbe\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x95\xbf'},('shield_col_size', 'param'): {'zh_name': '\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\xe5\xb0\xba\xe5\xaf\xb8',
                                  'post_setter': lambda self: self.refresh_col(),'structure': [{'zh_name': '\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe5\x8e\x9a\xe5\xba\xa6','type': 'float'}]},
   ('shield_col_offset', 'param'): {'zh_name': '\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\xe5\x81\x8f\xe7\xa7\xbb',
                                    'post_setter': lambda self: self.refresh_col(),'structure': [{'zh_name': '\xe5\x89\x8d\xe5\x90\x8e','type': 'float'}, {'zh_name': '\xe4\xb8\x8a\xe4\xb8\x8b','type': 'float'}]}
   })
class Shield8026(StateBase):
    ST_START = 0
    ST_OPENED = 1
    ST_END = 2
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_8026_SHIELD_CHANGE': 'on_shield_state_change',
       'E_SHILED_ABSORBED_DAMAGE': 'on_shield_hitted',
       'E_UPDATE_SHIELD_MAX_TIME': 'update_shield_max_time',
       'G_SHIELD_MAX_TIME': 'get_shield_max_time',
       'TRY_STOP_WEAPON_ATTACK': 'end_btn_down',
       'E_ENTER_STATE': 'enter_states',
       'E_SIZE_UP_8026_SHIELD': 'size_up_8026_shield'
       }

    def on_shield_hitted(self, *args):
        self.end_custom_sound('hitted')
        self.start_custom_sound('hitted')

    def update_shield_max_time(self, shield_max_time):
        self.shield_max_time = shield_max_time

    def get_shield_max_time(self):
        return self.shield_max_time

    def enter_states(self, *args):
        if not self.check_can_active():
            self.send_event('E_DO_SKILL', self.shield_skill_id, False, False)
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Shield8026, self).init_from_dict(unit_obj, bdict, sid, info)
        self.skill_id = self.custom_param.get('skill_id', 802656)
        self.shield_skill_id = self.custom_param.get('shield_skill_id', 802651)
        self.shield_start_anim = self.custom_param.get('shield_start_anim', 'shield_start')
        self.shield_start_anim_len = self.custom_param.get('shield_start_anim_len', 0.6)
        self.shield_start_anim_rate = self.custom_param.get('shield_start_anim_rate', 1.0)
        self.shield_loop_anim = self.custom_param.get('shield_loop_anim', 'shield_loop')
        self.shield_end_anim = self.custom_param.get('shield_end_anim', 'shield_end')
        self.shield_end_anim_len = self.custom_param.get('shield_end_anim_len', 0.8)
        self.shield_end_break = self.custom_param.get('shield_end_break', 0.5)
        self.interrupt_states = {MC_SHOOT, MC_DASH}
        self.shield_col_size = self.custom_param.get('shield_col_size', [4, 4, 0.5])
        self.shield_col_offset = self.custom_param.get('shield_col_offset', [0, 0])
        self.shield_max_time = 0.0
        self.skill_end = False
        self.shield_closed = False
        self.ignore_btn_down = False
        self.mecha_model = None
        from logic.gcommon.common_const.ui_operation_const import SHIELD_TRIGGER_PRESS_8026
        self._close_on_release_key = SHIELD_TRIGGER_PRESS_8026
        self._register_sub_state_callbacks()
        return

    def close_on_release(self):
        if self._close_on_release_key is not None and self.ev_g_is_avatar():
            setting_val = global_data.player.get_setting_2(self._close_on_release_key)
            return bool(setting_val)
        else:
            return False

    def _on_model_loaded(self, model):
        import weakref
        self.mecha_model = weakref.ref(model)
        self.refresh_col()

    def refresh_col(self):
        self.send_event('E_ON_LOAD_SHIELD_MODEL', None, self.mecha_model, size=self.shield_col_size, socket_name='fx_hudun', offset=self.shield_col_offset)
        return

    def size_up_8026_shield(self, size_up_factor):
        self.send_event('E_SET_SHIELD_SIZE_RATIO', size_up_factor)
        self.refresh_col()
        col_size = self.shield_col_size
        x, y, z = col_size
        x *= 1 + size_up_factor
        y *= 1 + size_up_factor
        z *= 1 + size_up_factor
        col_size = [x, y, z]
        self.send_event('E_ON_LOAD_SHIELD_MODEL', None, self.mecha_model, size=col_size, socket_name='fx_hudun', offset=self.shield_col_offset)
        return

    def _register_sub_state_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.ST_START, 0.0, self.on_shield_start)
        self.register_substate_callback(self.ST_START, self.shield_start_anim_len * self.shield_start_anim_rate, lambda : setattr(self, 'sub_state', self.ST_OPENED))
        self.register_substate_callback(self.ST_OPENED, 0.0, self.on_shield_opened)
        self.register_substate_callback(self.ST_END, 0.0, self.on_shield_end)
        self.register_substate_callback(self.ST_END, self.shield_end_break, self.on_shield_end_break)
        self.register_substate_callback(self.ST_END, self.shield_end_anim_len, self.disable_self)

    def action_btn_down(self):
        if self.ignore_btn_down:
            return
        if not self.close_on_release() and self.is_active:
            self.close_shield(False)
        else:
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
        if not self.is_active:
            self.active_self()
        super(Shield8026, self).action_btn_down()
        self.ignore_btn_down = True
        return True

    def action_btn_up(self):
        super(Shield8026, self).action_btn_up()
        if self.is_active and not self.shield_closed and self.close_on_release():
            self.close_shield(False)
        self.ignore_btn_down = False

    def end_btn_down(self, *args):
        self.close_shield(True)

    def on_shield_state_change(self, state):
        self.send_event('E_ADD_HS_COL' if state else 'E_REMOVE_HS_COL')

    def enter(self, leave_states):
        super(Shield8026, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.shield_skill_id, True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.send_event('E_SLOW_DOWN', True, state='Shield8026')
        self.send_event('E_8026_SHIELD_AIM', True)
        self.skill_end = True
        self.shield_closed = False
        self.off_sound_played = False
        self.sub_state = self.ST_START
        self.sound_drive.run_start()
        global_data.emgr.camera_leave_free_observe_event.emit()
        self.send_event('E_ENABLE_FREE_CAMERA', False)
        if self.ev_g_is_avatar():
            self.sd.ref_raise_shield = True
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.end_btn_down)
        return

    def update(self, dt):
        super(Shield8026, self).update(dt)
        if not self.shield_closed and self.elapsed_time >= self.shield_max_time:
            self.close_shield(False)

    def exit(self, enter_states):
        super(Shield8026, self).exit(enter_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        if self.sd.ref_up_body_anim in (self.shield_start_anim, self.shield_loop_anim, self.shield_end_anim):
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.send_event('E_DO_SKILL', self.shield_skill_id, False, not self.skill_end)
        if self.skill_end:
            self.end_custom_sound('off')
            self.start_custom_sound('off')
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
            self.send_event('E_8026_SHIELD_AIM', False)
            self.send_event('E_SET_ENERGY_FULL')
        self.send_event('E_SLOW_DOWN', False, state='Shield8026')
        self.send_event('E_REPLACE_MOVE_ANIM')
        self.send_event('E_ENABLE_FREE_CAMERA', True)
        self.sound_drive.run_end()
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
            self.sd.ref_raise_shield = False
        return

    def close_shield(self, skill_end):
        self.skill_end = skill_end
        if skill_end:
            self.sub_state = self.ST_END
        else:
            self.send_event('E_ACTIVE_STATE', MC_SECOND_WEAPON_ATTACK)
        self.shield_closed = True

    def on_shield_start(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.shield_start_anim_rate)
        cur_state = self.ev_g_cur_state()
        if cur_state is None:
            cur_state = set()
        and_state = {
         MC_STAND} & cur_state
        if len(and_state):
            self.send_event('E_POST_ACTION', self.shield_start_anim, LOW_BODY, 1)
        self.send_event('E_POST_ACTION', self.shield_start_anim, UP_BODY, 7)
        return

    def on_shield_opened(self):
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.shield_loop_anim)
        self.send_event('E_POST_ACTION', self.shield_loop_anim, UP_BODY, 7)
        self.send_event('E_REPLACE_MOVE_ANIM', {'move_anim': self.shield_loop_anim,'move_dir_type': 6}, use_new_anim=True)

    def on_shield_end(self):
        cur_state = self.ev_g_cur_state()
        if cur_state is None:
            cur_state = set()
        and_state = {
         MC_STAND} & cur_state
        if len(and_state):
            self.send_event('E_POST_ACTION', self.shield_end_anim, LOW_BODY, 1)
        self.send_event('E_POST_ACTION', self.shield_end_anim, UP_BODY, 7)
        self.send_event('E_DO_SKILL', self.shield_skill_id, False, False)
        return

    def on_shield_end_break(self):
        self.send_event('E_ADD_WHITE_STATE', self.interrupt_states, self.sid)


@editor.state_exporter({('fire_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe6\x97\xb6\xe9\x97\xb4'},('break_time', 'param'): {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'},('anim_rate', 'param'): {'zh_name': '\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe7\x8e\x87'},('anim_len', 'param'): {'zh_name': '\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf'}})
class ShieldShoot(StateBase):
    BIND_EVENT = {'E_SHILED_ABSORBED_DAMAGE': 'on_shield_hitted'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ShieldShoot, self).init_from_dict(unit_obj, bdict, sid, info)
        self.skill_id = self.custom_param.get('skill_id', 802656)
        self.anim_name = self.custom_param.get('anim_name', 'shield_fire')
        self.anim_len = self.custom_param.get('anim_len', 1.2)
        self.anim_rate = self.custom_param.get('anim_rate', 1.0)
        self.fire_time = self.custom_param.get('fire_time', 1.0)
        self.break_time = self.custom_param.get('break_time', 2.0)
        self.weapon_pos = self.custom_param.get('weapon_pos', PART_WEAPON_POS_MAIN3)
        self.break_states = {MC_SHOOT, MC_DASH}
        gun_data = confmgr.get('c_gun_data', '802603', 'cCustomParam', default={})
        self.shield_dmg_max = gun_data.get('max_base_power', 1000)
        self.absorb_full = False
        self.can_break = False

    def enter(self, leave_states):
        super(ShieldShoot, self).enter(leave_states)
        self.can_break = False
        cur_state = self.ev_g_cur_state()
        if cur_state is None:
            cur_state = set()
        and_state = {
         MC_STAND} & cur_state
        if len(and_state):
            self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, 1)
            self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, UP_BODY, 1)
        self.send_event('E_ANIM_RATE', UP_BODY, self.anim_rate)
        self.delay_call(self.fire_time / self.anim_rate, self.on_fire)
        self.delay_call(self.break_time / self.anim_rate, self.on_can_break)
        self.delay_call(self.anim_len / self.anim_rate, self.disable_self)
        return

    def on_fire(self):
        self.weapon_pos = PART_WEAPON_POS_MAIN4 if self.absorb_full else PART_WEAPON_POS_MAIN3
        return self.ev_g_try_weapon_attack_begin(self.weapon_pos)

    def on_can_break(self):
        self.send_event('E_ADD_WHITE_STATE', self.break_states, self.sid)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)
        self.absorb_full = False
        self.can_break = True

    def check_transitions(self):
        super(ShieldShoot, self).check_transitions()
        if not self.can_break:
            return
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            return self.status_config.MC_MOVE

    def exit(self, enter_states):
        super(ShieldShoot, self).exit(enter_states)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        if self.sd.ref_up_body_anim == self.anim_name:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        if self.sd.ref_low_body_anim == self.anim_name:
            self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_8026_SHIELD_AIM', False)
        self.send_event('E_SET_ENERGY_FULL')

    def on_shield_hitted(self, absorbed_dmg):
        if absorbed_dmg >= self.shield_dmg_max:
            self.absorb_full = True


def _param_postsetter(self):
    self.acc_speed = self.max_rush_speed / (self.pre_anim_duration - self.start_acc_time)
    self.brake_speed = self.max_rush_speed / self.end_brake_time
    self._register_sub_state_callbacks()


@editor.state_exporter({('max_rush_speed', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6','post_setter': _param_postsetter},('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': _param_postsetter},('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': _param_postsetter},('start_acc_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x97\xb4',
                                 'explain': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe5\x8a\xa0\xe9\x80\x9f\xe5\x88\xb0\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6',
                                 'post_setter': _param_postsetter
                                 },
   ('max_rush_duration', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x97\xb4','post_setter': _param_postsetter},('hit_anim_duration', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': _param_postsetter},('hit_anim_rate', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': _param_postsetter},('break_hit_time', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9',
                                 'explain': '\xe7\x9b\xae\xe5\x89\x8d\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe7\x8a\xb6\xe6\x80\x81\xe6\x9c\x89\xef\xbc\x9a\xe7\xa7\xbb\xe5\x8a\xa8\xef\xbc\x8c\xe8\xb7\xb3\xe8\xb7\x83\xef\xbc\x8c\xe8\x90\xbd\xe5\x9c\xb0\xef\xbc\x8c\xe5\xb0\x84\xe5\x87\xbb',
                                 'post_setter': _param_postsetter
                                 },
   ('attack_skill_time', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe4\xbc\xa4\xe5\xae\xb3\xe8\xa7\xa6\xe5\x8f\x91\xe6\x97\xb6\xe9\x97\xb4'},('miss_anim_duration', 'param'): {'zh_name': '\xe6\x9c\xaa\xe5\x91\xbd\xe4\xb8\xad\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf','post_setter': _param_postsetter},('miss_anim_rate', 'param'): {'zh_name': '\xe6\x9c\xaa\xe5\x91\xbd\xe4\xb8\xad\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': _param_postsetter},('end_brake_time', 'param'): {'zh_name': '\xe6\x9c\xaa\xe5\x91\xbd\xe4\xb8\xad\xe5\x87\x8f\xe9\x80\x9f\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4',
                                 'explain': '\xe8\xbf\x9b\xe5\x85\xa5\xe6\x9c\xaa\xe5\x91\xbd\xe4\xb8\xad\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8e\xe4\xbc\x9a\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x8f\xe9\x80\x9f',
                                 'post_setter': _param_postsetter
                                 },
   ('dash_stepheight', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6(m)','min_val': 1.0,'max_val': 3.5},('air_dash_brake_time', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x86\xb2\xe5\x88\xba\xe7\xbb\x93\xe6\x9d\x9f\xe5\x90\x8ex\xe7\xa7\x92\xe5\x86\x85\xe5\x87\x8f\xe9\x80\x9f\xe5\x88\xb0\xe9\x9d\x99\xe6\xad\xa2','param_type': 'float'},('rush_col_size', 'param'): {'zh_name': '\xe9\x87\x8d\xe8\xa3\x85\xe6\x97\xb6\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\xe5\xa4\xa7\xe5\xb0\x8f',
                                'param_type': 'list','structure': [{'zh_name': '\xe5\xae\xbd','type': 'float'}, {'zh_name': '\xe9\xab\x98','type': 'float'}, {'zh_name': '\xe9\x95\xbf','type': 'float'}],'post_setter': lambda self: self.send_event('E_SET_RUSH_COL_SIZE', self.rush_col_size)
                                },
   ('attack_dist', 'meter'): {'zh_name': '\xe5\xa4\x84\xe5\x86\xb3\xe6\x97\xb6\xe5\x8f\x8c\xe6\x96\xb9\xe8\xb7\x9d\xe7\xa6\xbb\xef\xbc\x88\xe7\xb1\xb3\xef\xbc\x89','param_type': 'float'}})
class Dash8026(StateBase):
    BIND_EVENT = {'E_RUSH_HIT_TARGET': 'on_hit_target',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_ENTER_STATE': 'enter_states',
       'E_ROGUE_GIFT_8026': 'on_get_rogue_gift_8026'
       }
    STATE_PRE = 0
    STATE_RUSH = 1
    STATE_HIT = 2
    STATE_MISS = 3
    IS_AUTO_OX_RUSH_COL_CHECK = True

    def read_data_from_custom_param(self):
        self.tick_interval = self.custom_param.get('tick_interval', 0.1)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.hit_skill_id = self.custom_param.get('hit_skill_id', 802654)
        self.attack_skill_id = self.custom_param.get('attack_skill_id', 802655)
        self.max_rush_speed = self.custom_param.get('max_rush_speed', 40) * NEOX_UNIT_SCALE
        self.min_elevation_speed_ratio = self.custom_param.get('min_elevation_speed_ratio', 1.0)
        self.pre_anim = self.custom_param.get('pre_anim', 'thrust_f_01')
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.833)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.start_acc_time = self.custom_param.get('start_acc_time', 0.767)
        self.acc_speed = self.max_rush_speed / (self.pre_anim_duration - self.start_acc_time)
        self.rush_anim = self.custom_param.get('rush_anim', 'thrust_f_02')
        self.max_rush_duration = self.custom_param.get('max_rush_duration', 2.5)
        self.hit_anim = self.custom_param.get('hit_anim', 'shockwave_03')
        self.hit_anim_duration = self.custom_param.get('hit_anim_duration', 1.6)
        self.hit_anim_rate = self.custom_param.get('hit_anim_rate', 1.0)
        self.break_hit_time = self.custom_param.get('break_hit_time', 2.3)
        self.attack_skill_time = self.custom_param.get('attack_skill_time', 1.1)
        self.miss_anim = self.custom_param.get('miss_anim', 'thrust_f_miss')
        self.miss_anim_duration = self.custom_param.get('miss_anim_duration', 0.66)
        self.miss_anim_rate = self.custom_param.get('miss_anim_rate', 1.0)
        self.end_brake_time = self.custom_param.get('end_brake_time', 0.434)
        self.brake_speed = self.max_rush_speed / self.end_brake_time
        self.dash_stepheight = self.custom_param.get('dash_stepheight', 2 * NEOX_UNIT_SCALE)
        self.air_dash_brake_time = self.custom_param.get('air_dash_brake_time', 0.0)
        self.rush_col_size = self.custom_param.get('rush_col_size', [2.5, 3, 2.5])
        self.attack_dist = self.custom_param.get('attack_dist', 1.5 * NEOX_UNIT_SCALE)
        self._register_sub_state_callbacks()
        return

    def on_post_init_complete(self, bidct):
        super(Dash8026, self).on_post_init_complete(bidct)
        self.send_event('E_SET_RUSH_COL_SIZE', self.rush_col_size)

    def _register_sub_state_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0.0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.start_acc_time / self.pre_anim_rate, self.on_start_acc)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration / self.pre_anim_rate, self.on_end_pre)
        self.register_substate_callback(self.STATE_RUSH, 0.0, self.on_begin_rush)
        self.register_substate_callback(self.STATE_RUSH, self.max_rush_duration, self.on_end_rush)
        self.register_substate_callback(self.STATE_HIT, 0.0, self.on_begin_hit)
        self.register_substate_callback(self.STATE_HIT, self.attack_skill_time / self.hit_anim_rate, self.do_attack_skill)
        self.register_substate_callback(self.STATE_HIT, self.break_hit_time / self.hit_anim_rate, self.on_add_hit_white_state)
        self.register_substate_callback(self.STATE_HIT, self.hit_anim_duration / self.hit_anim_rate, self.on_end_hit)
        self.register_substate_callback(self.STATE_MISS, 0.0, self.on_begin_miss)
        self.register_substate_callback(self.STATE_MISS, self.end_brake_time / self.miss_anim_rate, self.on_end_miss_brake)
        self.register_substate_callback(self.STATE_MISS, self.miss_anim_duration / self.miss_anim_rate, self.on_end_miss)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Dash8026, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.need_trigger_btn_up_when_action_forbidden = False
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.is_accelerating = False
        self.is_braking = False
        self.rush_direction = None
        self.cur_speed = 0.0
        self.rush_finished = False
        self.continual_on_ground = False
        self.target_hitted = False
        self.water_time_scale = 1.0
        self.post_brake_timer = None
        self.hit_target = None
        self.btn_down = False
        self.can_cast = False
        self.showing_cancel_ui = False
        self.is_moving = False
        self.event_registered = False
        self.can_turn = False
        self.camera_sense = 0
        if global_data.game_mode.is_pve():
            self.target_tags = preregistered_tags.MONSTER_TAG_VALUE
        else:
            self.target_tags = preregistered_tags.MECHA_TAG_VALUE
        return

    def destroy(self):
        if self.event_registered:
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        PartCtrl.enable_clamp_cam_rotation(False)
        super(Dash8026, self).destroy()
        return

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar() and not self.event_registered:
            self.regist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = True

    def on_leave_mecha_start(self):
        if self.ev_g_is_avatar() and self.event_registered:
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False

    def action_btn_down(self):
        if self.btn_down:
            return
        else:
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
            self.btn_down = True
            self.can_cast = True
            if self.ev_g_is_avatar():
                from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                MechaCancelUI(None, self.end_btn_down, True)
                self.showing_cancel_ui = True
            super(Dash8026, self).action_btn_down()
            return

    def action_btn_up(self):
        self.btn_down = False
        if not self.can_cast:
            return
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        if self.ev_g_is_avatar() and self.showing_cancel_ui:
            global_data.ui_mgr.close_ui('MechaCancelUI')
            self.showing_cancel_ui = False
        super(Dash8026, self).action_btn_up()
        self.sound_custom_start()
        return True

    def end_btn_down(self):
        self.can_cast = False
        if self.ev_g_is_avatar() and self.showing_cancel_ui:
            global_data.ui_mgr.close_ui('MechaCancelUI')
            self.showing_cancel_ui = False

    def enter_states(self, *args):
        if self.is_active:
            return
        if not self.check_can_active():
            self.end_btn_down()

    def enter(self, leave_states):
        super(Dash8026, self).enter(leave_states)
        self.init_parameters()
        self.air_walk_direction_setter.reset()
        self.start_rush()

    def trigger_rush_skill(self):
        self.send_event('E_DO_SKILL', self.skill_id)

    def start_rush(self):
        global_data.emgr.enable_camera_kill_mecha.emit(False)
        self.send_event('E_STEP_HEIGHT', self.dash_stepheight)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.trigger_rush_skill()
        self.sound_drive.run_start()
        self.send_event('E_GRAVITY', 0)
        self._start_pre()
        if self.can_turn and self.camera_sense:
            PartCtrl.enable_clamp_cam_rotation(True, 0.01 * self.camera_sense * (1.0 + self.ev_g_add_attr(attr_const.MECHA_MAX_BODY_TURN_SPEED_FACTOR)))

    def _start_pre(self):
        if self.sd.ref_on_ground:
            self.sub_state = self.STATE_PRE
        else:
            self.on_start_acc()
            self.on_end_pre()

    def init_parameters(self):
        self.is_accelerating = False
        self.is_braking = False
        self.rush_direction = None
        self.rush_finished = False
        self.continual_on_ground = True
        self.cur_speed = 0.0
        self.can_break_by_move = False
        self.target_hitted = False
        self.model_forward_locked = False
        self.is_moving = False
        return

    def on_begin_pre(self):
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def on_start_acc(self, *args):
        effect = global_data.emgr.show_screen_effect.emit('MeleeRushEffect', {})
        if effect:
            effect = effect[0]
            effect and effect.show()
        if self.IS_AUTO_OX_RUSH_COL_CHECK:
            self.send_event('E_OX_BEGIN_RUSH')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.is_accelerating = True
        self.is_moving = True

    def on_end_pre(self):
        self.sub_state = self.STATE_RUSH
        self.is_accelerating = False
        self.cur_speed = self.max_rush_speed

    def on_begin_rush(self):
        import collision
        from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, WATER_GROUP, WATER_MASK
        self.is_moving = True
        if not self.can_turn or not self.camera_sense:
            self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        group = GROUP_CHARACTER_INCLUDE & ~WATER_GROUP
        mask = GROUP_CHARACTER_INCLUDE & ~WATER_MASK
        scn = world.get_active_scene()
        camera = scn.active_camera
        ori_forward = camera.rotation_matrix.forward
        start_pos = camera.position + ori_forward * 3 * NEOX_UNIT_SCALE
        end_pos = start_pos + ori_forward * self.max_rush_speed * self.max_rush_duration
        result = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
        if result[0]:
            end_pos = result[1]
        mecha_pos = self.ev_g_position()
        y_offset = camera.position.y - mecha_pos.y
        end_pos += math3d.vector(0, -y_offset, 0)
        self.rush_direction = end_pos - mecha_pos
        self.rush_direction.normalize()
        self.cur_speed = self.max_rush_speed
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_POST_ACTION', self.rush_anim, LOW_BODY, 1, loop=True)
        self.send_event('E_FORWARD', self.rush_direction, True)

    def on_end_rush(self):
        if self.sd.ref_on_ground:
            self.sub_state = self.STATE_MISS
        else:
            self.rush_finished = True
        PartCtrl.enable_clamp_cam_rotation(False)

    def on_begin_hit(self):
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.hit_anim_rate)
        self.send_event('E_POST_ACTION', self.hit_anim, LOW_BODY, 1)
        self.sound_drive.run_end()
        self.rush_direction = None
        return

    def on_add_hit_white_state(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_JUMP_1, MC_JUMP_2}, self.sid)
        if self.sd.ref_on_ground:
            self.send_event('E_RESET_GRAVITY')
            self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT}, self.sid)
            self.can_break_by_move = True
        else:
            self.send_event('E_FALL')

    def on_end_hit(self):
        self.rush_finished = True
        PartCtrl.enable_clamp_cam_rotation(False)

    def on_begin_miss(self):
        cam_mtx = global_data.game_mgr.scene.active_camera.rotation_matrix
        self.sd.ref_logic_trans.yaw_target = cam_mtx.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.miss_anim_rate)
        self.send_event('E_POST_ACTION', self.miss_anim, LOW_BODY, 1)
        self.end_custom_sound('end')
        self.start_custom_sound('end')
        self.is_braking = True

    def on_end_miss_brake(self):
        self.is_moving = False
        self.is_braking = False
        self.rush_direction = None
        self.cur_speed = 0.0
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_ACTION_SYNC_STOP')
        self.sound_drive.run_end()
        self.send_event('E_CLEAR_SPEED')
        self.on_add_hit_white_state()
        return

    def on_end_miss(self):
        self.sound_drive.run_end()
        self.rush_finished = True
        PartCtrl.enable_clamp_cam_rotation(False)

    def update_dash_param(self, scale):
        time_scale = self.water_time_scale / scale
        self.send_event('E_ANIM_RATE', LOW_BODY, scale if scale < 1 else 1)
        self.max_rush_speed /= time_scale
        self.water_time_scale = scale

    def update(self, dt):
        super(Dash8026, self).update(dt)
        if self.is_accelerating:
            self.cur_speed += self.acc_speed * dt
            if self.cur_speed > self.max_rush_speed:
                self.cur_speed = self.max_rush_speed
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.sub_state == self.STATE_RUSH:
            if self.is_moving and self.can_turn and self.camera_sense:
                scn = world.get_active_scene()
                speed_scale = self.ev_g_speedup_skill_scale() or 1.0
                self.update_dash_param(speed_scale)
                if self.ev_g_is_agent():
                    cam_forward = self.ev_g_forward()
                    cam_pitch = self.ev_g_cam_pitch()
                    if not cam_forward.y:
                        up = math3d.vector(0, 1, 0)
                        right = cam_forward.cross(up) * -1
                        right.normalize()
                        mat = math3d.matrix.make_rotation(right, -cam_pitch)
                        cam_forward = cam_forward * mat
                else:
                    cam_forward = scn.active_camera.rotation_matrix.forward
                    cam_pitch = scn.active_camera.rotation_matrix.pitch
                if cam_pitch < 0.0 and not self.ev_g_is_agent():
                    if cam_pitch < -1.3:
                        speed_ratio = self.min_elevation_speed_ratio
                    else:
                        speed_ratio = 1.0 - cam_pitch / -1.3 * (1.0 - self.min_elevation_speed_ratio)
                else:
                    speed_ratio = 1.0
                walk_direction = self.get_walk_direction(cam_forward) * speed_ratio
                self.air_walk_direction_setter.execute(walk_direction)
                if not self.ev_g_on_ground():
                    self.continual_on_ground = False
                if self.continual_on_ground and cam_forward.y < 0:
                    cam_forward.y = 0
                    cam_forward.normalize()
                self.send_event('E_FORWARD', cam_forward, True)
            elif self.rush_direction is not None:
                walk_direction = self.get_walk_direction(self.rush_direction)
                self.air_walk_direction_setter.execute(walk_direction)
        return

    def check_transitions(self):
        if self.can_break_by_move or self.rush_finished:
            if not self.ev_g_on_ground():
                self.disable_self()
                return MC_JUMP_2
            rocker_dir = self.sd.ref_rocker_dir
            self.disable_self()
            if rocker_dir and not rocker_dir.is_zero:
                return MC_MOVE
            return MC_STAND

    def on_get_rogue_gift_8026(self, can_turn, camera_sense):
        self.can_turn = can_turn
        self.camera_sense = camera_sense if camera_sense else 0

    def get_walk_direction(self, cam_forward, cur_ratio=1.0):
        return cam_forward * (self.cur_speed * cur_ratio)

    def exit(self, enter_states):
        super(Dash8026, self).exit(enter_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        global_data.emgr.enable_camera_yaw.emit(True)
        global_data.emgr.destroy_screen_effect.emit('MeleeRushEffect')
        PartCtrl.enable_clamp_cam_rotation(False)
        if not self.sd.ref_on_ground and self.air_dash_brake_time:
            self.send_event('E_CLEAR_SPEED_INTRP', self.air_dash_brake_time)
        else:
            self.send_event('E_CLEAR_SPEED')
        if self.IS_AUTO_OX_RUSH_COL_CHECK:
            self.send_event('E_OX_END_RUSH')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_SET_ENERGY_FULL')
        global_data.emgr.enable_camera_kill_mecha.emit(True)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        cam_mtx = global_data.game_mgr.scene.active_camera.rotation_matrix
        self.sd.ref_logic_trans.yaw_target = cam_mtx.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        if self.target_hitted:
            self.send_event('E_DO_SKILL', self.hit_skill_id, None, None)
        return

    def on_hit_target(self, target):
        if not (target and target.MASK & self.target_tags):
            return
        if self.sub_state == self.STATE_HIT:
            return
        if self.target_hitted:
            return
        target_pos = target.ev_g_position()
        position = self.ev_g_position()
        if not target_pos or not position:
            return
        direction = target_pos - position
        forward = self.rush_direction if self.rush_direction else self.ev_g_forward()
        if math3d.vector.dot(direction, forward) < 0.0:
            return
        direction.normalize()
        position = (position.x, position.y, position.z)
        self.send_event('E_DO_SKILL', self.hit_skill_id, target.id, position)
        self.sd.ref_logic_trans.yaw_target = direction.yaw
        super(Dash8026, self).sound_custom_end()
        self.end_custom_sound('hit1')
        self.start_custom_sound('hit1')
        self.target_hitted = target
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)
        if self.IS_AUTO_OX_RUSH_COL_CHECK:
            self.send_event('E_OX_END_RUSH')
        self.sub_state = self.STATE_HIT

    def do_attack_skill(self):
        position = self.ev_g_position()
        position = (position.x, position.y, position.z)
        self.send_event('E_DO_SKILL', self.attack_skill_id, self.target_hitted.id, position)
        self.end_custom_sound('hit2')
        self.start_custom_sound('hit2')

    def on_cam_rotate(self, *args):
        if self.is_active and self.is_moving and self.can_turn and self.camera_sense and self.sub_state == self.STATE_RUSH:
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            cam_forward = scn.active_camera.rotation_matrix.forward
            walk_direction = cam_forward * self.cur_speed
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)


class Walk8026(Walk):
    BIND_EVENT = Walk.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REPLACE_MOVE_ANIM': 'replace_move_anim'
       })

    def start_cb(self):
        self.send_event('E_POST_ACTION', self.move_start_anim, LOW_BODY, 6)
        self.change_state(self.STATE_MOVE)

    def move_cb(self):
        self.send_event('E_POST_ACTION', self.move_anim, LOW_BODY, self.move_dir_type, loop=True)

    def stop_cb(self):
        self.send_event('E_POST_ACTION', self.move_stop_anim, LOW_BODY, 6)
        self.send_event('E_ACTIVE_STATE', self.STAND_STATE)

    def replace_move_anim(self, move_anim_info=None, use_new_anim=False):
        if move_anim_info is None:
            self.move_anim = self.custom_param.get('move_anim', None)
            self.move_dir_type = self.custom_param.get('move_dir_type', 6)
            self.move_start_anim, self.start_time = self.custom_param.get('start_anim', (None,
                                                                                         0))
            self.move_stop_anim, self.stop_time = self.custom_param.get('stop_anim', (None,
                                                                                      0))
        else:
            self.move_anim = move_anim_info.get('move_anim', self.move_anim)
            self.move_dir_type = move_anim_info.get('move_dir_type', self.move_dir_type)
            self.move_start_anim, self.start_time = move_anim_info.get('start_anim', (None,
                                                                                      0))
            self.move_stop_anim, self.stop_time = move_anim_info.get('stop_anim', (None,
                                                                                   0))
        self.reset_sub_states_callback()
        if self.move_start_anim or self.move_stop_anim or self.move_anim:
            if self.move_start_anim:
                self.register_substate_callback(self.STATE_START, 0, self.start_cb)
            self.register_substate_callback(self.STATE_MOVE, 0, self.move_cb)
            if self.move_stop_anim:
                self.register_substate_callback(self.STATE_STOP, 0, self.stop_cb)
        if use_new_anim and self.is_active:
            self.send_event('E_POST_ACTION', self.move_anim, LOW_BODY, self.move_dir_type, loop=True)
        return