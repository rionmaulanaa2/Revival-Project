# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/weapon_atk/AtkProcess.py
from __future__ import absolute_import
from six.moves import range
from common.utils.timer import LOGIC, CLOCK, RELEASE
import time
from logic.gcommon.common_const import weapon_const
from common.cfg import confmgr
from mobile.common.IdManager import IdManager
from logic.gcommon.cdata import mecha_status_config
import world
import math3d
import logic.gcommon.const as g_const
from logic.gcommon import time_utility
import logic.gcommon.common_utils.bcast_utils as bcast
SEQUENCE_MIN_CD = 0.01

class AtkProcess(object):

    def __init__(self, atk_gun_com, weapon_pos, weapon, weapon_status, multi_shape=False, use_main_dir=False):
        self.weapon_pos = weapon_pos
        self.weapon = weapon
        self.weapon_status = weapon_status
        self.atk_gun_com = atk_gun_com
        self._last_sequence_fire_time = None
        self._last_fire_time = time.time() - 999.0
        self.last_wind_up_time = time.time() - 999.0
        self.multi_shape = multi_shape
        self.is_attack_accumulate = False
        self.begin_accumulate_time = time.time()
        self.last_accumulate_duration = 0
        self.wind_up_timer = None
        self.continue_atk_timer = None
        self.batch_atk_timer = None
        self.delay_reload_timer = None
        self.auto_reload_timer = None
        self.check_reload_after_fire = True
        self.fire_index = 0
        self.continue_atk_times = 0
        self.batch_bullet = []
        self.keep_socket_index = False
        self.last_fire_socket_parent_model = None
        self.last_fire_socket_name = ''
        self.last_fire_pos = None
        self.ignore_socket_index_for_fire_appearance = False
        self.is_touch = False
        self.debug_log = True
        self.bullet_auto_recover = None
        self.auto_try_reload_time = 0
        self.gen_id = None
        self.is_continue_sound = False
        self._spell_id = None
        self.weapon_state_info = None
        self.cur_aim_target_index = -1
        self.use_main_dir = use_main_dir
        self.main_position = None
        self.main_direction = None
        self.main_aim_direction = None
        self.specify_pos_dir_getter = None
        self.logic_timer = global_data.game_mgr.get_logic_timer()
        self.init_weapon()
        self.init_events()
        return

    def init_weapon(self):
        if not self.weapon:
            return
        self.check_reload_after_fire = self.weapon.get_check_reload_after_fire()
        self.bullet_auto_recover = self.weapon.get_bullet_recovery_rate()
        last_reload_time = self.weapon.get_last_reloaded_time()
        if self.bullet_auto_recover and last_reload_time:
            bullet_cap = self.weapon.get_bullet_cap()
            bullet_num = self.weapon.get_bullet_num()
            interval_time = self.bullet_auto_recover['time']
            reload_num = self.bullet_auto_recover['num']
            all_time = time_utility.get_server_time() - last_reload_time
            reload_bullet_num = int(all_time / interval_time)
            reload_bullet_num = min(bullet_cap - bullet_num, reload_bullet_num * reload_num)
            if reload_bullet_num:
                self.atk_gun_com.send_event('E_CALL_SYNC_METHOD', 'reloaded', (reload_bullet_num, self.weapon.get_pos(), 0), True)
        self.is_continue_sound = self.weapon.get_key_config_value('iIsContinueSound', default=False)
        socket_select_mode = self.weapon.get_effective_value('iFireSocketSelectMode', default=weapon_const.SWITCH_SOCKET_EACH_BULLET)
        self.keep_socket_index = socket_select_mode == weapon_const.SWITCH_SOCKET_EACH_FIRE
        self.ignore_socket_index_for_fire_appearance = self.weapon.get_effective_value('cCustomParam', default={}).get('ignore_socket_index_for_fire_appearance', False)

    def sync_data_from_other_process(self, old_atk_process):
        if not old_atk_process:
            return
        if old_atk_process.is_touch:
            self.is_touch = old_atk_process.is_touch
        self.is_attack_accumulate = old_atk_process.is_attack_accumulate
        self.last_accumulate_duration = old_atk_process.last_accumulate_duration
        if old_atk_process.is_attack_accumulate:
            self.begin_accumulate_time = old_atk_process.begin_accumulate_time
        self._last_fire_time = old_atk_process._last_fire_time
        self.last_wind_up_time = old_atk_process.last_wind_up_time
        if old_atk_process.weapon_status:
            status, status_time, custom_delay_time = old_atk_process.weapon_status.get_status_and_time()
            self.weapon_status.set_status_and_time(status, status_time, custom_delay_time)
            if old_atk_process.weapon.get_bullet_cap() != 0:
                socket_index = old_atk_process.get_socket_index()
                self.weapon_status.set_socket_index(socket_index)

    def init_events(self):
        if not self.atk_gun_com:
            return
        regist_func = self.atk_gun_com.regist_event
        regist_func('E_BULLET_CAP_NUM_CHG', self.bullet_cap_num_change)
        regist_func('E_WEAPON_BULLET_CHG', self.bullet_reloaded, 20)
        regist_func('E_SET_WEAPON_SPECIFY_POS_DIR_GETTER', self.set_specify_pos_dir_getter)

    def unbind_events(self):
        if not self.atk_gun_com:
            return
        unregist_func = self.atk_gun_com.unregist_event
        unregist_func('E_BULLET_CAP_NUM_CHG', self.bullet_cap_num_change)
        unregist_func('E_WEAPON_BULLET_CHG', self.bullet_reloaded)
        unregist_func('E_SET_WEAPON_SPECIFY_POS_DIR_GETTER', self.set_specify_pos_dir_getter)

    def destroy(self):
        for timer_name in [
         'wind_up_timer',
         'continue_atk_timer',
         'batch_atk_timer',
         'delay_reload_timer',
         'auto_reload_timer']:
            _timer = getattr(self, timer_name)
            if _timer:
                global_data.game_mgr.unregister_logic_timer(_timer)
                setattr(self, timer_name, None)

        self.last_fire_socket_parent_model = None
        self.unbind_events()
        self.atk_gun_com = None
        return

    def touch_begin(self, force_full_power=False, aim_target_index=-1, extra_data={}):
        weapon = self.weapon
        if not weapon:
            return False
        if not extra_data.get('ignore_diving', False) and self.atk_gun_com.ev_g_is_diving():
            return False
        status, now = self.weapon_status.do_status()
        if status not in [weapon_const.FIRE_STATE_READY]:
            return False
        if now - self._last_fire_time < weapon.get_fire_cd():
            return False
        if self.is_touch:
            return False
        self.cur_aim_target_index = aim_target_index
        control_mode = weapon.get_data_by_key('iControl')
        if weapon.is_accumulate_gun():
            self.begin_accumulate_time = 0 if force_full_power else now
            if self.multi_shape:
                self.is_attack_accumulate = True
                if control_mode == weapon_const.CONTROL_MODEL_BEGIN:
                    self.last_accumulate_duration = self.atk_gun_com.get_accumulate_duration(self.weapon_pos)
        self.is_touch = True
        if control_mode != weapon_const.CONTROL_MODEL_BEGIN:
            return True
        self.weapon_status.set_status_and_time(weapon_const.FIRE_STATE_CD, now)
        hold_time = weapon.get_data_by_key('fHoldTime')
        if now - self._last_fire_time < hold_time:
            wind_up_time = 0.0
        else:
            wind_up_time = weapon.get_data_by_key('fWindupTime')
        wind_up_interval = now - self.last_wind_up_time
        if wind_up_interval < wind_up_time:
            wind_up_time -= wind_up_interval
        else:
            self.last_wind_up_time = now
        if wind_up_time == 0.0:
            self.attack_delay()
        else:
            self.atk_gun_com.send_event('E_FIRE_WINDUP')
            self.begin_wind_up_timer(wind_up_time)
        if weapon.get_bullet_cap() != 0 and weapon.get_bullet_num() < weapon.get_cost_ratio():
            return False
        return True

    def check_can_weapon_attack(self):
        weapon = self.weapon
        if not weapon:
            return False
        if self.atk_gun_com.ev_g_is_diving():
            return False
        status, now = self.weapon_status.do_status()
        if status not in [weapon_const.FIRE_STATE_READY]:
            return False
        if weapon.get_bullet_cap() != 0 and weapon.get_bullet_num() < weapon.get_cost_ratio():
            return False
        return True

    def reset_attack(self):
        if self.continue_atk_timer:
            return
        if self.is_touch and self.weapon.get_data_by_key('iMode') == weapon_const.AUTO_MODE:
            self.attack_delay()

    def attack_delay(self):
        self.atk_gun_com.send_event('WEAPON_ATTACK_SUCCESS', self.weapon_pos)
        weapon = self.weapon
        if weapon.get_data_by_key('iMode') == weapon_const.AUTO_MODE and self.is_touch:
            fire_cd = weapon.get_fire_cd()
            if self.continue_atk_timer:
                global_data.game_mgr.unregister_logic_timer(self.continue_atk_timer)
                self.continue_atk_timer = None
            self.continue_atk_times = 0
            if fire_cd:
                self.continue_atk_timer = self.logic_timer.register(None, self.continue_batch_attack, (), interval=fire_cd, times=-1, mode=CLOCK, timedelta=False, strict=True)
        self.batch_attack()
        if weapon.get_data_by_key('iMode') == weapon_const.AUTO_MODE and not self.is_touch:
            self.atk_gun_com.send_and_bcast_event(bcast.E_ATTACK_END, self.weapon_pos)
        return

    def sequence_tick(self):
        weapon = self.weapon
        cd_time = weapon.get_fire_cd()
        sequence_num = self.atk_gun_com.ev_g_sequence_num(self.weapon_pos)
        enable_cd_time = cd_time * 0.8 ** sequence_num
        enable_cd_time = SEQUENCE_MIN_CD if enable_cd_time < SEQUENCE_MIN_CD else enable_cd_time
        now = time.time()
        while now - self._last_sequence_fire_time > enable_cd_time:
            self._last_sequence_fire_time += enable_cd_time
            cd_time = weapon.get_fire_cd()
            sequence_num = self.atk_gun_com.ev_g_sequence_num(self.weapon_pos)
            enable_cd_time = cd_time * 0.8 ** sequence_num
            if enable_cd_time < SEQUENCE_MIN_CD:
                enable_cd_time = SEQUENCE_MIN_CD if 1 else enable_cd_time
                self.batch_attack()

    def touch_end(self, is_cancel=False, weapon_state_info=None):
        self._spell_id = None
        self.weapon_state_info = weapon_state_info
        weapon = self.weapon
        if not weapon:
            return False
        else:
            if is_cancel:
                self.end_wind_up_timer()
            if self.continue_atk_timer:
                global_data.game_mgr.unregister_logic_timer(self.continue_atk_timer)
                self.continue_atk_timer = None
                self.continue_atk_times = 0
            if not self.is_touch:
                return
            self.is_touch = False
            control_mode = weapon.get_data_by_key('iControl')
            if weapon.is_accumulate_gun() and self.multi_shape:
                if control_mode == weapon_const.CONTROL_MODEL_END:
                    self.last_accumulate_duration = self.atk_gun_com.get_accumulate_duration(self.weapon_pos)
            self.atk_gun_com.send_and_bcast_event(bcast.E_STOP_AUTO_FIRE)
            self.atk_gun_com.send_and_bcast_event(bcast.E_ATTACK_END, self.weapon_pos)
            if self.multi_shape:
                self.is_attack_accumulate = False
            weapon_mode = weapon.get_data_by_key('iMode')
            if weapon_mode == weapon_const.MANUAL_MODE and self.atk_gun_com._wait_loading.get(self.weapon_pos, False):
                if weapon.get_bullet_num() < weapon.get_cost_ratio() and self.check_reload_after_fire:
                    self.atk_gun_com.try_reload_new(self.weapon_pos)
                else:
                    self.atk_gun_com.on_loading_new(self.weapon_pos)
                return True
            if not is_cancel and weapon_mode != weapon_const.AUTO_MODE:
                if control_mode != weapon_const.CONTROL_MODEL_END:
                    return True
                status, now = self.weapon_status.do_status()
                if status not in [weapon_const.FIRE_STATE_READY]:
                    return False
                self.weapon_status.set_status_and_time(weapon_const.FIRE_STATE_CD, now)
                hold_time = weapon.get_data_by_key('fHoldTime')
                if now - self._last_fire_time < hold_time:
                    wind_up_time = 0.0
                else:
                    wind_up_time = weapon.get_data_by_key('fWindupTime')
                wind_up_interval = now - self.last_wind_up_time
                if wind_up_interval < wind_up_time:
                    wind_up_time -= wind_up_interval
                else:
                    self.last_wind_up_time = now
                if wind_up_time == 0.0:
                    self.batch_attack()
                else:
                    self.begin_wind_up_timer(wind_up_time)
            return True

    def continue_batch_attack(self):
        self.continue_atk_times += 1
        self.batch_attack()

    def batch_attack(self):
        weapon = self.weapon
        pellets = weapon.get_bullet_pellets()
        self.atk_gun_com.send_event('WEAPON_ATTACK_SUCCESS', self.weapon_pos)
        self.gen_id = IdManager.genid()
        if isinstance(pellets, dict):
            self.stop_batch_attack()
            self.fire_index = 0
            self.batch_bullet = pellets['bullets']
            fire_cd = pellets['cd']
            self.batch_atk_timer = global_data.game_mgr.register_logic_timer(self.batch_attack_tick, interval=fire_cd, times=len(self.batch_bullet) - 1, mode=CLOCK)
            self.batch_attack_tick()
        else:
            self.attack_one()

    def batch_attack_tick(self):
        if self.fire_index >= len(self.batch_bullet):
            return
        self.attack_one(self.batch_bullet[self.fire_index], force_keep_socket_index=self.keep_socket_index)
        self.fire_index += 1

    def is_batch_atk_end(self):
        if self.wind_up_timer:
            return False
        if self.fire_index >= len(self.batch_bullet):
            return True
        return False

    def attack_one(self, pellets=None, force_keep_socket_index=False):
        weapon = self.weapon
        if pellets is None:
            pellets = weapon.get_bullet_pellets()
        if weapon.is_accumulate_gun() and self.multi_shape:
            energy_cd = self.last_accumulate_duration
            weapon_id = weapon.get_accumulate_weapon_id(energy_cd)
            weapon_conf = confmgr.get('firearm_config', str(weapon_id))
            if weapon_conf:
                pellets = weapon_conf.get('iPellets', 1)
        self.last_fire_socket_parent_model = None
        self.last_fire_socket_name = ''
        if weapon.heat_magazine:
            if weapon.heat_magazine.can_shoot():
                weapon.heat_magazine.do_shoot(pellets)
                for idx in range(0, pellets):
                    self.fire(sub_idx=idx, keep_socket_index=force_keep_socket_index or self.keep_socket_index and idx != pellets - 1, weapon_state_info=self.weapon_state_info)

            else:
                self.stop_batch_attack()
                return
        elif weapon.get_bullet_cap() != 0:
            if weapon.get_bullet_num() >= weapon.get_cost_ratio():
                if weapon.get_bolted() == 0:
                    weapon.set_bolted(1)
                    if self.continue_atk_timer:
                        global_data.game_mgr.unregister_logic_timer(self.continue_atk_timer)
                        self.continue_atk_timer = None
                        self.continue_atk_times = 0
                    self.stop_batch_attack()
                    return
                if weapon.get_data_by_key('iMode') == weapon_const.MANUAL_MODE:
                    weapon.set_bolted(0)
                weapon.cost_bullet(pellets)
                for idx in range(0, pellets):
                    self.fire(sub_idx=idx, keep_socket_index=force_keep_socket_index or self.keep_socket_index and idx != pellets - 1, weapon_state_info=self.weapon_state_info)

                pos_list = weapon.get_related_weapon_pos()
                if pos_list:
                    for pos in pos_list:
                        self.atk_gun_com.send_event('E_WEAPON_DATA_CHANGED', pos)

                else:
                    self.atk_gun_com.send_event('E_WEAPON_DATA_CHANGED', weapon.get_pos())
                self.atk_gun_com.send_event('E_WEAPON_DATA_UPDATE_TO_ATTACKING', weapon)
                self.atk_gun_com.send_event('E_CUR_BULLET_NUM_CHG', weapon.get_pos())
                if not self.bullet_auto_recover:
                    if weapon.get_bullet_num() < weapon.get_cost_ratio() and self.check_reload_after_fire:
                        self.delay_reload_timer = global_data.game_mgr.register_logic_timer(self.atk_gun_com.try_reload_new, args=(self.weapon_pos,), interval=weapon.get_fire_cd() + 0.01, times=1, mode=CLOCK)
                    elif weapon.get_data_by_key('iMode') == weapon_const.MANUAL_MODE:
                        self.delay_reload_timer = global_data.game_mgr.register_logic_timer(self.atk_gun_com.on_loading_new, args=(self.weapon_pos,), interval=weapon.get_fire_cd() + 0.01, times=1, mode=CLOCK)
                else:
                    self.auto_try_reload()
            else:
                if not self.bullet_auto_recover:
                    self.check_reload_after_fire and self.atk_gun_com.try_reload_new(self.weapon_pos)
                else:
                    self.auto_try_reload()
                if self.continue_atk_timer:
                    global_data.game_mgr.unregister_logic_timer(self.continue_atk_timer)
                    self.continue_atk_timer = None
                    self.continue_atk_times = 0
                self.stop_batch_attack()
                return
        else:
            fire_offset = self.get_socket_offset()
            if pellets > 1:
                for index in range(pellets):
                    self.fire(fire_offset=fire_offset, sub_idx=index, keep_socket_index=force_keep_socket_index or self.keep_socket_index and index != pellets - 1, weapon_state_info=self.weapon_state_info)

            else:
                self.fire(fire_offset=fire_offset, weapon_state_info=self.weapon_state_info, sub_idx=self.weapon_state_info.get('sub_idx', None) if self.weapon_state_info else None)
        if self.ignore_socket_index_for_fire_appearance:
            self.atk_gun_com.send_event('E_FIRE', weapon.get_fire_cd(), self.weapon_pos, -1)
        else:
            self.atk_gun_com.send_event('E_FIRE', weapon.get_fire_cd(), self.weapon_pos, self.weapon_status.get_fired_socket_index())
        self._last_fire_time = time.time()
        if not self.is_continue_sound:
            self.atk_gun_com.send_and_bcast_event(bcast.E_ATTACK_START, self.weapon_pos)
        else:
            spell_id = IdManager.genid()
            self.atk_gun_com.send_event('E_ATTACK_START', self.weapon_pos)
            self.atk_gun_com.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ATTACK_START, (self.weapon_pos,), None, True, spell_id, 'E_ATTACK_END'], True)
        if hasattr(g_const, 'SWITCH_LOG_SKILL') and g_const.SWITCH_LOG_SKILL and weapon.get_item_id():
            pass
        self.atk_gun_com.send_event('E_FIRE_END', self.weapon_pos)
        return

    def bullet_cap_num_change(self):
        if self.bullet_auto_recover:
            self.auto_try_reload()

    def bullet_reloaded(self, weapon_pos, cur_bullet_cnt):
        if not self.bullet_auto_recover:
            return
        weapon = self.weapon
        interval_time = self.bullet_auto_recover['time']
        now = time.time()
        if not self.auto_try_reload_time:
            self.auto_try_reload_time = now
        pass_time = now - self.auto_try_reload_time
        self.atk_gun_com.send_and_bcast_event(bcast.E_AUTO_RELOADING, weapon_pos, interval_time, pass_time)

    def set_specify_pos_dir_getter(self, weapon_pos, getter):
        if self.weapon_pos != weapon_pos:
            return
        self.specify_pos_dir_getter = getter

    def auto_try_reload(self):
        weapon = self.weapon
        interval_time = self.bullet_auto_recover['time']
        reload_num = self.bullet_auto_recover['num']
        now = time.time()
        if not self.auto_try_reload_time:
            self.auto_try_reload_time = now
        if self.auto_reload_timer:
            return

        def _auto_reload(*args):
            now = time.time()
            if weapon.is_bullet_full():
                global_data.game_mgr.unregister_logic_timer(self.auto_reload_timer)
                self.auto_reload_timer = None
                self.atk_gun_com.send_and_bcast_event(bcast.E_AUTO_RELOADING, weapon.get_pos(), 0)
                self.auto_try_reload_time = 0
                return
            else:
                if now - self.auto_try_reload_time >= interval_time:
                    self.auto_try_reload_time = now
                    self.atk_gun_com.send_event('E_CALL_SYNC_METHOD', 'reloaded', (reload_num, weapon.get_pos(), 0), True)
                return

        self.auto_reload_timer = global_data.game_mgr.register_logic_timer(_auto_reload, interval=0.033, mode=CLOCK)

    def fire(self, fire_offset=None, sub_idx=None, keep_socket_index=False, weapon_state_info=None):
        weapon = self.weapon
        kind = weapon.get_data_by_key('iKind')
        if not self.atk_gun_com._special_weapon_firer:
            return
        else:
            firer = self.atk_gun_com._special_weapon_firer.get(kind, self.atk_gun_com.normal_weapon_shoot)
            item_no = weapon.get_item_id()
            ignore_fire_pos = confmgr.get('firearm_config', str(item_no), 'iIgnoreFirePos')
            if self.use_main_dir and sub_idx != 0:
                if self.main_position and self.main_direction:
                    position, direction, aim_direction = self.main_position, self.main_direction, self.main_aim_direction
                else:
                    fire_ray = self.atk_gun_com.ev_g_mecha_fire_ray(self.weapon_pos, self.cur_aim_target_index, True, ignore_fire_pos)
                    if not fire_ray:
                        return
                    position, direction, aim_direction = fire_ray
            elif self.specify_pos_dir_getter:
                pellets = weapon.get_bullet_pellets()
                position, direction = self.specify_pos_dir_getter(sub_idx, pellets)
                aim_direction = None
            else:
                fire_ray = self.atk_gun_com.ev_g_mecha_fire_ray(self.weapon_pos, self.cur_aim_target_index, True, ignore_fire_pos)
                if not fire_ray:
                    return
                if sub_idx == 0:
                    self.main_position, self.main_direction, self.main_aim_direction = fire_ray
                position, direction, aim_direction = fire_ray
            socket_name, fire_pos = self.get_cur_fire_pos(keep_socket_index)
            not keep_socket_index and self.atk_gun_com.send_event('E_GUN_ATTACK', socket_name, self.weapon_pos)
            if weapon.is_accumulate_gun():
                energy_cd = time.time() - self.begin_accumulate_time
                if self.multi_shape:
                    energy_cd = self.last_accumulate_duration
                auto_param = self.atk_gun_com.ev_g_auto_energy()
                if auto_param:
                    wp_pos, auto_energy_cd = auto_param
                    if wp_pos == self.weapon_pos:
                        energy_cd = auto_energy_cd
            else:
                energy_cd = 0.0
            is_hit_target = firer(weapon, position, direction, aim_direction, fire_pos=fire_pos, energy_cd=energy_cd, gen_id=self.gen_id, sub_idx=sub_idx, ignore_fire_pos=ignore_fire_pos, fire_offset=fire_offset, socket_name=socket_name, weapon_pos=self.weapon_pos, aim_target_index=self.cur_aim_target_index, continue_atk_times=self.continue_atk_times, weapon_state_info=weapon_state_info, fix_pos_dir=bool(self.specify_pos_dir_getter))
            return is_hit_target

    def get_socket_list(self):
        return self.weapon_status.get_socket_list()

    def get_cur_fire_pos(self, keep_socket_index=False):
        if self.last_fire_socket_parent_model:
            model = self.last_fire_socket_parent_model
        else:
            model = self.atk_gun_com.sd.ref_aim_model
            if not model or model and self.atk_gun_com.sd.ref_open_aim_weapon_pos != self.weapon_pos:
                model = self.atk_gun_com.ev_g_model()
            elif self.atk_gun_com.sd.ref_update_aim_model_trans_func:
                self.atk_gun_com.sd.ref_update_aim_model_trans_func()
            self.last_fire_socket_parent_model = model
        if not model:
            return (None, None)
        else:
            socket_name = self.weapon_status.get_socket_name(keep_socket_index, in_aim=self.atk_gun_com.sd.ref_in_aim)
            if self.last_fire_socket_name == socket_name:
                return (socket_name, self.last_fire_pos)
            if socket_name:
                matrix = model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
                if matrix:
                    pos = matrix.translation
                    self.last_fire_socket_name, self.last_fire_pos = socket_name, pos
                    return (
                     socket_name, pos)
            self.last_fire_socket_name, self.last_fire_pos = None, model.world_position + math3d.vector(0.0, 40.0, 0.0)
            return (
             self.last_fire_socket_name, self.last_fire_pos)

    def get_fired_pos(self):
        model = self.atk_gun_com.sd.ref_aim_model
        if not model:
            model = self.atk_gun_com.ev_g_model()
        elif self.atk_gun_com.sd.ref_update_aim_model_trans_func:
            self.atk_gun_com.sd.ref_update_aim_model_trans_func()
        if not model:
            return None
        else:
            socket_name = self.weapon_status.get_fired_socket_name()
            if socket_name:
                matrix = model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
                if matrix:
                    pos = matrix.translation
                    return pos
            return model.world_position + math3d.vector(0.0, 40.0, 0.0)

    def get_weapon_type(self):
        if self.weapon:
            return self.weapon.get_id()

    def get_fired_socket_index(self):
        return self.weapon_status.get_fired_socket_index()

    def set_socket_index(self, socket_index):
        self.weapon_status.set_socket_index(socket_index)

    def get_socket_index(self):
        return self.weapon_status.get_socket_index()

    def get_weapon_fire_cd(self):
        if self.weapon:
            return self.weapon.get_fire_cd()

    def get_socket_offset(self):
        model = self.atk_gun_com.ev_g_model()
        if not model:
            return None
        else:
            socket_name = self.weapon_status.fire_offset_name()
            if not socket_name:
                return None
            if not model.has_socket(socket_name):
                global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xef\xbc\x9a%s' % socket_name)
                return None
            offset = model.get_socket_matrix(socket_name, world.SPACE_TYPE_LOCAL).translation
            return math3d.vector(offset.x, 0, 0)

    def begin_wind_up_timer(self, wind_up_time):

        def wind_up_logic():
            self.wind_up_timer = None
            self.attack_delay()
            return

        self.end_wind_up_timer()
        self.wind_up_timer = global_data.game_mgr.register_logic_timer(wind_up_logic, interval=wind_up_time, times=1, mode=CLOCK)

    def end_wind_up_timer(self):
        if self.wind_up_timer:
            global_data.game_mgr.unregister_logic_timer(self.wind_up_timer)
            self.wind_up_timer = None
        return

    def stop_batch_attack(self):
        if self.batch_atk_timer:
            global_data.game_mgr.unregister_logic_timer(self.batch_atk_timer)
            self.batch_atk_timer = None
        return

    def get_accumulate_begin_time(self):
        return self.begin_accumulate_time

    def get_last_accumulate_duration(self):
        return self.last_accumulate_duration

    def is_attack_accumulate(self):
        return self.is_attack_accumulate

    def refresh_fire_cd(self):
        if self.continue_atk_timer and self.weapon:
            global_data.game_mgr.get_logic_timer().set_interval(self.continue_atk_timer, self.weapon.get_fire_cd())