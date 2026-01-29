# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAtkGun.py
from __future__ import absolute_import
from six.moves import range
import time
import weakref
import logic.gcommon.common_utils.bcast_utils as bcast
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils.weapon_utils import is_fast_aim_and_fire_mode
from .ComBaseWeaponLogic import ComBaseWeaponLogic, GunStatusInf
from logic.gcommon.const import ATK_GUN
from logic.gcommon.common_const import weapon_const
from logic.gcommon.common_const.sync_const import ID_ATTACK_START
from logic.gcommon.common_const.animation_const import WEAPON_TYPE_FROZEN
import logic.gcommon.common_const.animation_const as animation_const
from ...cdata.status_config import ST_HELP, ST_LOAD, ST_SHOOT, ST_RELOAD_LOOP, ST_RELOAD, ST_AIM, ST_RIGHT_AIM, ST_ROLL, ST_RUSH
LEFT_BULLET_NUM = 10000
AUTO_RELOAD_STATE = (
 ST_ROLL, ST_RUSH)

class ComAtkGun(ComBaseWeaponLogic):
    BIND_EVENT = {'E_TRY_RELOAD': '_try_reload',
       'E_SWITCHED': '_on_switched_data',
       'E_TRY_AIM': '_try_aim',
       'E_QUIT_AIM': ('_quit_aim', -10),
       'E_WEAPON_DATA_CHANGED_SUCCESS': '_weapon_data_changed',
       'E_ON_EQUIP_ATTACHMENT': '_attachment_changed',
       'E_ON_TAKE_OFF_ATTACHMENT': '_attachment_changed',
       'E_JUMP': '_on_jump',
       'G_IN_AIM': 'g_is_in_aim',
       'E_DEATH': '_die',
       'E_END_PUT_ON_BULLET': 'put_on_bullet',
       'E_CANCEL_RELOAD': 'cancel_reload',
       'E_RELOADED': '_on_reloaded',
       'E_SUCCESS_AIM': '_switch_to_aim_camera',
       'E_CTRL_ROLL': '_close_auto_mirror',
       'E_FREE_CAMERA_STATE': '_close_auto_mirror',
       'E_ON_ROLL_END': '_on_roll_end',
       'G_IN_RIGHT_AIM': 'g_is_in_right_aim',
       'E_TRY_RIGHT_AIM': '_try_right_aim',
       'E_QUIT_RIGHT_AIM': '_quit_right_aim',
       'E_END_ROLL': '_check_reload',
       'E_END_RUSH_EVENT': '_check_reload',
       'G_IS_CAN_FIRE': '_is_can_fire',
       'G_GET_FIRE_POS': 'get_fire_pos',
       'G_GET_WEAPON_MODEL': 'get_weapon_model',
       'G_IS_AIM_TRANSFERRING': 'get_is_aim_transferring',
       'E_LEAVE_STATE': '_leave_states',
       'E_GUN_MODEL_LOADED': '_on_gun_model_loaded',
       'E_PARACHUTE_STATUS_CHANGED': ('on_parachute_stage_changed', -1),
       'E_WEAPON_MODE_SWITCHED': '_on_weapon_mode_switch',
       'E_REMOTE_FIRE': '_remote_fire',
       'E_AUTO_FIRE_CHECK_COLlISION': 'auto_check_fire_collision',
       'E_IS_KEEP_DOWN_FIRE': 'set_is_keep_down_fire'
       }
    FIRE_POS_COLLISION_INTERVAL = 0.5
    FIRE_POS_COLLISION_DELAY = 0.5

    def __init__(self):
        super(ComAtkGun, self).__init__()
        self.enable = False
        self.gun_status = GunStatusInf()
        self.sd.ref_in_aim = False
        self._lens_in_aim = None
        self._is_auto_mirror = False
        self._timer_id = None
        self._delay_callback = None
        self._reload_num = 0
        self._auxiliary_component_list = []
        self._weapon_model = None
        self._left_weapon_model = None
        self._last_fire_weapon = None
        self._auto_check_timer = None
        self._scn_camera = None
        self.sd.ref_in_right_aim = False
        self._start_aim_transfer_time = 0
        self._aim_transfer_duration = 0.1
        self._start_aim_transfer = False
        self._t_try_stamp = 0
        self._last_reload_begin_time = 0
        self._last_reload_pass_time = 0
        self._gun_model_loaded = True
        self._last_fire_time = time.time()
        self.last_wind_up_time = time.time()
        self.wind_up_timer = None
        self.batch_atk_timer = None
        self.last_dirty_time = time.time()
        self._wait_loading = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAtkGun, self).init_from_dict(unit_obj, bdict)
        self._is_puppet_com = self.is_unit_obj_type('LPuppet')
        if not self._is_puppet_com:
            self.regist_event('E_TRY_FIRE', self._try_fire)

    @property
    def weapon_model(self):
        model = self._weapon_model() if self._weapon_model else None
        if not model or not model.valid:
            weapon_model = self.sd.ref_hand_weapon_model
            if weapon_model and weapon_model.valid:
                model = weapon_model
                self._weapon_model = weakref.ref(weapon_model)
            else:
                self._weapon_model = None
                model = None
        return model

    @property
    def left_weapon_model(self):
        model = self._left_weapon_model() if self._left_weapon_model else None
        if not model or not model.valid:
            weapon_model = self.sd.ref_left_hand_weapon_model
            if weapon_model and weapon_model.valid:
                model = weapon_model
                self._left_weapon_model = weakref.ref(weapon_model)
            else:
                self._left_weapon_model = None
                model = None
        return model

    def on_init_complete(self):
        self.cur_wp = self.sd.ref_wp_bar_cur_weapon
        self.gun_status.set_wp(self.cur_wp)
        if not self._timer_id:
            self._timer_func(1, callback=self._check_reload)

    def on_post_init_complete(self, bdict):
        is_in_aim = self.ev_g_attr_get('aim_state', False)
        if is_in_aim:
            self._try_aim(True)
        is_in_right_aim = self.ev_g_attr_get('right_aim_state', False)
        if is_in_right_aim:
            self._try_right_aim()

    def destroy(self):
        if self.batch_atk_timer:
            global_data.game_mgr.unregister_logic_timer(self.batch_atk_timer)
            self.batch_atk_timer = None
        if not self._is_puppet_com:
            self.unregist_event('E_TRY_FIRE', self._try_fire)
        self.send_event('E_ATK_GUN_DESTROY')
        self.clear_auxiliary_component()
        self.unload_weapon()
        self.clear_timer()
        self.clear_auto_check()
        self._wait_loading = False
        self.gun_status.destroy()
        super(ComAtkGun, self).destroy()
        return

    def on_parachute_stage_changed(self, stage):
        if self.sd.ref_in_aim:
            self.send_event('E_QUIT_AIM')
        if self.ev_g_in_right_aim():
            self.send_event('E_QUIT_RIGHT_AIM')

    def _remote_fire(self):
        kind = self.cur_wp.get_effective_value('iKind')
        firer = self._special_weapon_firer.get(kind, None)
        if firer is None:
            return
        else:
            info = self.ev_g_fire_ray(1)
            if info is None:
                return
            position, direction, aim_direction, original_direction = info
            if direction.is_zero:
                return
            item_no = self.cur_wp.get_item_id()
            ignore_fire_pos = confmgr.get('firearm_config', str(item_no), 'iIgnoreFirePos')
            firer(self.cur_wp, position, direction, aim_direction, None, socket_name='kaihuo', ignore_fire_pos=ignore_fire_pos, original_direction=original_direction)
            return

    def is_record_reload_time(self, new_state):
        if not new_state:
            return False
        if new_state not in AUTO_RELOAD_STATE:
            return False
        if not self.cur_wp:
            return False
        reload_type = self.cur_wp.get_reload_type()
        if reload_type != weapon_const.RELOAD_ALL:
            return False
        return True

    def _leave_states(self, leave_state, new_state=None):
        if leave_state == ST_RELOAD:
            if self.is_record_reload_time(new_state):
                self._last_reload_pass_time = time.time() - self._last_reload_begin_time
                self._last_reload_begin_time = self._t_try_stamp
            else:
                self._last_reload_pass_time = 0
        elif leave_state in AUTO_RELOAD_STATE:
            if self._last_reload_pass_time > 0:
                self._try_reload()
            else:
                self._check_reload()

    def _check_reload(self):
        if self._is_puppet_com:
            return
        if self.cur_wp and self.cur_wp.get_bullet_num() <= 0:
            self._try_reload()

    def _on_attack_end(self, *args):
        self._on_loading()

    def _on_roll_end(self, *args):
        self._on_loading()

    def _switch_to_aim_camera(self, *args):
        self.sd.ref_in_aim = True

    def _close_auto_mirror(self, *args):
        self._is_auto_mirror = False

    def _end_aim_camera_state(self, *args):
        self.sd.ref_in_aim = False
        if self.cur_wp:
            if self.cur_wp.get_bullet_num() <= 0:
                global_data.game_mgr.next_exec(self._try_reload)
            else:
                global_data.game_mgr.next_exec(self._on_loading)

    def load_current(self):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if obj_weapon:
            self.load_weapon(obj_weapon)

    def get_client_dict(self):
        d = {}
        return d

    def _timer_func(self, interval, times=1, callback=None, args=()):
        if self._delay_callback == callback:
            return
        self.clear_timer()
        if callback:
            tm = global_data.game_mgr.get_logic_timer()
            self._timer_id = tm.register(func=callback, args=args, interval=interval, times=times, mode=CLOCK)
            if self._timer_id:
                self._delay_callback = callback

    def clear_timer(self):
        if self._timer_id:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(self._timer_id)
            self._timer_id = None
            self._delay_callback = None
        return

    def clear_auto_check(self):
        if self._auto_check_timer is not None:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(self._auto_check_timer)
            self._scn_camera = None
            self._auto_check_timer = None
        return

    def auto_check(self):
        self.clear_auto_check()
        self._scn_camera = self.scene.active_camera
        tm = global_data.game_mgr.get_logic_timer()
        self._auto_check_timer = tm.register(func=self.auto_check_fire_collision, interval=self.FIRE_POS_COLLISION_INTERVAL, times=-1, mode=CLOCK)

    def unload_weapon(self):
        self.cur_wp = None
        self.enable = False
        self.gun_status.set_wp(None)
        self.gun_status.set_status(weapon_const.FIRE_STATE_NONE)
        if self.sd.ref_in_aim:
            self.send_event('E_QUIT_AIM')
        if self.sd.ref_in_right_aim:
            self.send_event('E_QUIT_RIGHT_AIM')
        self.clear_timer()
        return

    def load_weapon(self, obj_weapon):
        if not obj_weapon:
            self.unload_weapon()
            return
        if obj_weapon.get_atk_mode() != ATK_GUN:
            self.unload_weapon()
            return
        self.cur_wp = obj_weapon

    def set_enbale(self, enable):
        self.enable = enable

    def _reloaded(self, reload_num):
        if self.cur_wp is None:
            self.unload_weapon()
            return
        else:
            t_use = time.time() - self._t_try_stamp if self._t_try_stamp else 0
            self._t_try_stamp = time.time()
            self._last_reload_pass_time = 0
            self.cur_wp.reload(reload_num)
            self.cur_wp.dirty = True
            self.send_event('E_CALL_SYNC_METHOD', 'reloaded', (reload_num, None, t_use), True)
            self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())
            self._delay_callback = None
            self.send_event('E_WEAPON_DATA_CHANGED', self.cur_wp.get_pos())
            return

    def put_on_bullet(self, *args):
        if not self.cur_wp or self._reload_num <= 0:
            return
        if self.cur_wp.get_effective_value('iReloadType') == weapon_const.RELOAD_ONE:
            one_shoot_bullet_num = self.cur_wp.get_one_shoot_bullet_num()
            self._reloaded(one_shoot_bullet_num)
            self._reload_num -= one_shoot_bullet_num
        elif self._reload_num > 0:
            self._reloaded(self._reload_num)
            self._reload_num = 0
        if self._reload_num <= 0:
            global_data.game_mgr.next_exec(self._on_loading)

    def cancel_reload(self, *args):
        self._t_try_stamp = 0
        wp = self.cur_wp
        if not wp:
            return
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())
        if wp.get_effective_value('iReloadType') != weapon_const.RELOAD_ONE:
            return
        self._on_loading()

    def _try_reload(self):
        state, now = self.gun_status.do_status()
        if not self.cur_wp:
            self.cur_wp = self.sd.ref_wp_bar_cur_weapon
            if self.cur_wp is None:
                self.gun_status.set_status(weapon_const.FIRE_STATE_NONE)
                return
            self.gun_status.set_wp(self.cur_wp)
        wp = self.cur_wp
        bullet_type = wp.get_bullet_type()
        left_bullet = self.ev_g_item_count(bullet_type)
        if bullet_type == weapon_const.ITEM_ID_INFINITE_BULLET:
            left_bullet = wp.get_bullet_cap()
        elif bullet_type == weapon_const.ITEM_ID_LIMITED_BULLET:
            left_bullet = wp.get_carry_bullet_num()
            if left_bullet <= 0:
                old_hand_action = self.ev_g_hand_action()
                if old_hand_action == animation_const.HAND_STATE_FIRE:
                    from logic.gutils.item_utils import get_item_name
                    if global_data.cam_lplayer:
                        player = global_data.cam_lplayer
                        player.send_event('E_CTRL_ACCUMULATE', False)
                        player.send_event('E_ATTACK_END')
                        player.send_event('E_QUIT_AIM')
                global_data.emgr.show_carry_bullet_empty.emit()
                return
        elif not left_bullet or left_bullet <= 0:
            from logic.gutils.item_utils import get_item_name
            self.send_event('E_SHOW_MESSAGE', get_text_local_content(18006), itemtype=get_item_name(bullet_type))
            return
        if wp.is_bullet_full():
            return
        else:
            self._is_auto_mirror = False
            if self.sd.ref_in_aim:
                self.send_event('E_QUIT_AIM')
            reload_type = wp.get_reload_type()
            reload_status = ST_RELOAD
            if reload_type == weapon_const.RELOAD_ONE:
                reload_status = ST_RELOAD_LOOP
            if not self.ev_g_status_check_pass(reload_status):
                return
            reload_num = min(left_bullet, wp.get_reload_num())
            reload_time = 0.01
            if reload_type == weapon_const.RELOAD_ONE:
                status = weapon_const.FIRE_STATE_READY
                reload_time += wp.get_effective_value('fReloadTimeEmpty')
            elif wp.is_bullet_empty():
                status = weapon_const.FIRE_STATE_RELOAD_EMPTY
                reload_time += wp.get_effective_value('fReloadTimeEmpty')
            else:
                status = weapon_const.FIRE_STATE_READY
                reload_time += wp.get_effective_value('fReloadTimeLeft')
            self.gun_status.set_status_and_time(status, now)
            self._last_reload_begin_time = time.time()
            self._reload_num = reload_num
            first_reload_time = 0
            if reload_type == weapon_const.RELOAD_ALL:
                times = 1
                reload_time -= self._last_reload_pass_time
                first_reload_time = reload_time
                self._last_reload_begin_time -= self._last_reload_pass_time
            else:
                one_shoot_bullet_num = self.cur_wp.get_one_shoot_bullet_num()
                times = int(reload_num / one_shoot_bullet_num)
                reload_time = wp.get_effective_value('fReloadTimeEmpty') + (times - 1) * wp.get_effective_value('fReloadTimeLeft')
                first_reload_time = wp.get_effective_value('fReloadTimeEmpty') - self._last_reload_pass_time
            self._t_try_stamp = time.time() - self._last_reload_pass_time
            EPSILON_TIME = 0.05
            weapon_kind = wp.get_effective_value('iKind')
            factor = self.ev_g_add_attr('weapon_reload_speed_factor_{}'.format(weapon_kind))
            factor_human_common = self.ev_g_add_attr('weapon_reload_speed_factor_human_all')
            reload_time *= 1.0 / (1 + factor + factor_human_common)
            reload_time = max(reload_time, EPSILON_TIME)
            first_reload_time = max(first_reload_time, EPSILON_TIME)
            need_sync = False if self._last_reload_pass_time > 0 else True
            self._last_reload_pass_time = 0
            if first_reload_time <= EPSILON_TIME:
                self.send_event('E_END_PUT_ON_BULLET')
            else:
                self.ev_g_status_try_trans(reload_status)
                self.send_event('E_RELOADING', reload_time, times, first_reload_time)
                if self.ev_g_is_avatar():
                    need_sync and self.send_event('E_CALL_SYNC_METHOD', 'start_reload', (), True)
                    global_data.emgr.play_game_voice.emit('reload')
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_RELOADING, (reload_time, times, first_reload_time)], True)
            self.send_event('E_STOP_SIM_FIRE')
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ARMOR_ATTACK_END, ()], True)
            return

    def _auto_quit_aim(self):
        pass

    def set_is_keep_down_fire(self, *args):
        if not self._wait_loading:
            return
        self._wait_loading = False
        global_data.game_mgr.next_exec(self._on_loading)

    def _on_loading(self):
        if self.cur_wp is None or self.cur_wp.get_bullet_num() <= 0 or self.cur_wp.get_bolted() >= 1:
            return
        else:
            if self.cur_wp.get_effective_value('iMode') == weapon_const.MANUAL_MODE:
                if self.sd.ref_in_aim:
                    if self.ev_g_is_keep_down_fire():
                        self._wait_loading = True
                        return
                    self.send_event('E_QUIT_AIM')
                    reopen_aim = True
                    if self.ev_g_is_avatar():
                        from logic.gcommon.common_const import ui_operation_const
                        reopen_aim = global_data.player.get_setting_2(ui_operation_const.MANUAL_WEAPON_RE_AUTO_AIM)
                    if reopen_aim:
                        self._is_auto_mirror = True
                        self._timer_func(self.cur_wp.get_effective_value('fCDTime2') * (1 - self.cur_wp.interval_factor) + 0.1, callback=self._auto_mirror, args=None)
                if not self.ev_g_status_try_trans(ST_LOAD):
                    return
                self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_LOADING, time.time())
                self.send_event('E_LOADING')
            self.cur_wp.set_bolted(1)
            return

    def _auto_mirror(self):
        ui = global_data.ui_mgr.get_ui('BagUI')
        if ui and ui.is_appeared():
            self._is_auto_mirror = False
            return
        if self._is_auto_mirror:
            self._is_auto_mirror = False
            if self.ev_g_trans_status(ST_AIM, sync=True):
                self.send_event('E_SUCCESS_AIM')

    def get_fire_pos(self):
        if self.unit_obj is global_data.cam_lplayer and global_data.cam_model:
            trans = global_data.emgr.get_aim_gun_fire_matrix.emit()
            if trans and trans[0]:
                return trans[0]
        weapon_model = self.weapon_model
        action_id = self.ev_g_weapon_action_id()
        if action_id == WEAPON_TYPE_FROZEN and self._last_fire_weapon == self.weapon_model:
            weapon_model = self.left_weapon_model
        self._last_fire_weapon = weapon_model
        if not weapon_model or not weapon_model.valid:
            return
        else:
            import world
            socket_matrix = weapon_model.get_socket_matrix('kaihuo', world.SPACE_TYPE_WORLD)
            if socket_matrix:
                return socket_matrix.translation
            return

    def get_weapon_model(self):
        weapon_model = self.weapon_model
        if not weapon_model or not weapon_model.valid:
            return None
        else:
            return weapon_model

    def get_is_aim_transferring(self):
        return self._start_aim_transfer

    def auto_check_fire_collision(self):
        if self.ev_g_is_move():
            return
        else:
            if not self._scn_camera or not self._scn_camera.valid:
                self.clear_auto_check()
                return
            direction = self._scn_camera.rotation_matrix.forward
            pos = self.check_fire_collision(None, direction)
            if pos:
                self.send_event('E_FIRE_POS_COLLISION', pos, self.FIRE_POS_COLLISION_DELAY, True)
            else:
                self.send_event('E_FIRE_POS_COLLISION', pos, self.FIRE_POS_COLLISION_DELAY, False)
            return

    def _on_gun_model_loaded(self, *args):
        if not self._gun_model_loaded:
            self._try_fire()
        self._gun_model_loaded = True

    def _try_fire(self, accumulate=None):
        if self.cur_wp is None:
            self.unload_weapon()
            self.send_event('E_SHOW_MESSAGE', get_text_local_content(18001))
            return
        else:
            if self.cur_wp.dirty:
                return
            status, now = self.gun_status.do_status()
            if status not in [weapon_const.FIRE_STATE_READY]:
                if status == weapon_const.FIRE_STATE_NONE:
                    self.send_event('E_SHOW_MESSAGE', get_text_local_content(18001))
                if status in (weapon_const.FIRE_STATE_AIM,) and is_fast_aim_and_fire_mode(self.cur_wp):
                    self.send_event('E_QUIT_AIM')
                return
            if not self.ev_g_get_state(ST_HELP):
                if self.weapon_model is None:
                    return
            if self.cur_wp.have_enough_bullet(b_num=1):
                if self.cur_wp.get_bolted() == 0:
                    self._on_loading()
                    return
                if not self.ev_g_status_try_trans(ST_SHOOT):
                    return
                if not self.sd.ref_hand_weapon_model:
                    self._gun_model_loaded = False
                    return
                hold_time = self.cur_wp.get_hold_time()
                if now - self._last_fire_time < hold_time:
                    wind_up_time = 0.0
                else:
                    wind_up_time = self.cur_wp.get_wind_up_time()
                    if self.sd.ref_in_aim or self.ev_g_in_right_aim():
                        wind_up_time = 0.0
                wind_up_interval = now - self.last_wind_up_time
                if wind_up_interval < wind_up_time:
                    wind_up_time -= wind_up_interval
                else:
                    self.last_wind_up_time = now
                    accumulate_level = None
                    if self.cur_wp:
                        accumulate_level = self.cur_wp.get_accumulate_level(accumulate) if self.cur_wp.is_accumulate_gun() else None
                    self.send_event('E_GUN_ATTACK', accumulate_level=accumulate_level)
                    self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_GUN_ATTACK, (), None, True, ID_ATTACK_START, 'E_ATTACK_END'], True)
                if self.wind_up_timer:
                    global_data.game_mgr.unregister_logic_timer(self.wind_up_timer)
                if wind_up_time == 0.0:
                    self.batch_attack(accumulate)
                else:
                    self.wind_up_timer = global_data.game_mgr.register_logic_timer(self.batch_attack, wind_up_time, (accumulate,), times=1, mode=CLOCK)
                return
            self._try_reload()
            return

    def batch_attack(self, accumulate):
        if self.cur_wp is None:
            return
        else:
            pellets = self.cur_wp.get_bullet_pellets()
            if isinstance(pellets, dict):
                if self.batch_atk_timer:
                    global_data.game_mgr.unregister_logic_timer(self.batch_atk_timer)
                bullet_count = len(pellets['bullets'])
                cost_ratio = self.cur_wp.get_cost_ratio()
                if bullet_count > int(self.cur_wp.get_bullet_num() / cost_ratio):
                    bullet_count = int(self.cur_wp.get_bullet_num() / cost_ratio)
                fire_cd = pellets['cd']
                self.batch_atk_timer = global_data.game_mgr.register_logic_timer(self.fire, interval=fire_cd, args=(accumulate,), times=bullet_count - 1, mode=CLOCK)
                self.fire(accumulate)
            else:
                self.fire(accumulate)
            return

    def fire(self, accumulate):
        now = time.time()
        if not self.cur_wp:
            return
        else:
            if now - self._start_aim_transfer_time >= self._aim_transfer_duration:
                self._start_aim_transfer = False
            self.send_event('E_ATTACK_START')
            self._bcast_attack_start()
            self.send_event('E_FIRE')
            self.send_event('E_START_SIM_FIRE')
            if self.cur_wp.get_effective_value('iMode') == weapon_const.MANUAL_MODE:
                self.cur_wp.set_bolted(0)
            self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_CD, now)
            self._last_fire_time = now
            one_shoot_bullet_num = self.cur_wp.get_one_shoot_bullet_num()
            self.cur_wp.cost_bullet(one_shoot_bullet_num)
            self.send_event('E_WEAPON_DATA_CHANGED', self.cur_wp.get_pos())
            self.send_event('E_CUR_BULLET_NUM_CHG', self.cur_wp.get_pos())
            kind = self.cur_wp.get_effective_value('iKind')
            firer = self._special_weapon_firer.get(kind, self.normal_weapon_shoot)
            custom_direction = self.cur_wp.get_custom_direction()
            if custom_direction:
                fire_ray_list = [
                 self.ev_g_fire_ray_by_custom_direction(custom_direction)]
            else:
                fire_ray_list = [ self.ev_g_fire_ray(1) for i in range(one_shoot_bullet_num) ]
            if not fire_ray_list[0]:
                self.ev_g_cancel_state(ST_SHOOT)
                self.send_event('E_ATTACK_END')
                return
            item_no = self.cur_wp.get_item_id()
            ignore_fire_pos = confmgr.get('firearm_config', str(item_no), 'iIgnoreFirePos')
            for index, (position, direction, aim_direction, original_direction) in enumerate(fire_ray_list):
                if isinstance(direction, list):
                    for i, temp_dir in enumerate(direction):
                        firer(self.cur_wp, position, temp_dir, aim_direction, socket_name='kaihuo', ignore_fire_pos=ignore_fire_pos, sub_idx=i, original_direction=original_direction)

                elif accumulate is not None:
                    firer(self.cur_wp, position, direction, aim_direction, energy_cd=accumulate, socket_name='kaihuo', original_direction=original_direction)
                else:
                    firer(self.cur_wp, position, direction, aim_direction, socket_name='kaihuo', ignore_fire_pos=ignore_fire_pos, sub_idx=index, original_direction=original_direction)

            self.clear_timer()
            if self.cur_wp.get_bullet_num() <= 0:
                self._timer_func(self.cur_wp.get_fire_cd() + 0.01, callback=self._try_reload, args=())
            elif self.cur_wp.get_effective_value('iMode') == weapon_const.MANUAL_MODE:
                delay_load_time = self.cur_wp.get_effective_value('fReloadInterval', default=self.cur_wp.get_effective_value('fCDTime'))
                self._timer_func(delay_load_time + 0.01, callback=self._on_loading, args=())
            return

    def _is_can_fire(self):
        if time.time() - self._last_fire_time < self.gun_status.get_fire_cd():
            return False
        opening_aim = global_data.emgr.is_aim_model_opening.emit()
        if opening_aim and opening_aim[0]:
            return False
        status, now = self.gun_status.do_status()
        if self.cur_wp and self.cur_wp.dirty:
            now = time.time()
            if now - self.last_dirty_time < 2.0:
                self.cur_wp.dirty = False
                return False
            self.last_dirty_time = now
        if status == weapon_const.FIRE_STATE_READY:
            return True
        return False

    def _bcast_attack_start(self):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ATTACK_START, (), None, True, ID_ATTACK_START, 'E_ATTACK_END'], True)
        return

    def _switched(self, obj_weapon):
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())
        self.send_event('E_SWITCHED', obj_weapon)

    def _on_switched_data(self, obj_weapon):
        if obj_weapon.get_pos() > 0:
            self.load_weapon(obj_weapon)

    def _weapon_data_changed(self, pos):
        from logic.gcommon.const import PART_WEAPON_POS_NONE
        if not self.cur_wp or self.cur_wp.iPos == PART_WEAPON_POS_NONE:
            return
        else:
            if pos is None or pos == self.cur_wp.iPos:
                self.load_weapon(self.sd.ref_wp_bar_mp_weapons.get(self.cur_wp.iPos))
            if not self.cur_wp or self._is_puppet_com:
                return
            if self.cur_wp.get_bullet_num() <= 0:
                self._try_reload()
            elif self.cur_wp.get_effective_value('iMode') == weapon_const.MANUAL_MODE and self.cur_wp.get_bolted() == 0:
                status, now = self.gun_status.do_status()
                if status in [weapon_const.FIRE_STATE_READY]:
                    self._on_loading()
            if self.sd.ref_in_aim:
                from logic.gcommon.const import ATTACHEMNT_AIM_POS
                lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
                if lens_attachment != self._lens_in_aim:
                    self.send_event('E_QUIT_AIM')
            if self.sd.ref_in_right_aim:
                from logic.gcommon.const import ATTACHEMNT_AIM_POS
                lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
                if lens_attachment is not None:
                    self.send_event('E_QUIT_RIGHT_AIM')
            return

    def _attachment_changed(self, wp_pos, attachment_pos):
        if self.sd.ref_in_aim:
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
            if lens_attachment != self._lens_in_aim:
                self.send_event('E_QUIT_AIM')
        if self.sd.ref_in_right_aim:
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
            if lens_attachment is not None:
                self.send_event('E_QUIT_RIGHT_AIM')
        return

    def _on_jump(self, *args):
        if self.sd.ref_in_aim:
            self.send_event('E_QUIT_AIM')

    def get_gun_auxiliary_component(self, weapon):
        if not weapon:
            return []
        if weapon.get_kind() == weapon_const.WP_SPELL:
            com_list = [
             'ComAtkSpell']
        elif weapon.get_kind() == weapon_const.WP_CONTINUOUS_LASER:
            com_list = [
             'ComAtkContinuousLaser']
        else:
            com_list = [
             'ComRecoilNew']
        return com_list

    def add_auxiliary_component(self, weapon):
        com_list = self.get_gun_auxiliary_component(weapon)
        for com_name in com_list:
            _auxiliary_component = self.unit_obj.add_com(com_name, 'client')
            _auxiliary_component.init_from_dict(self.unit_obj, {})
            _auxiliary_component.set_weapon(weapon)
            self._auxiliary_component_list.append(_auxiliary_component)

    def clear_auxiliary_component(self):
        if self._auxiliary_component_list:
            for auxiliary_component in self._auxiliary_component_list:
                self.unit_obj.del_com(auxiliary_component.__class__.__name__)

        self._auxiliary_component_list = []

    def _on_weapon_mode_switch(self, weapon):
        self.clear_auxiliary_component()
        self.add_auxiliary_component(weapon)

    def install_weapon(self, weapon, is_init, do_not_tell_server=False, is_switch_mode=False):
        self.clear_auxiliary_component()
        self.add_auxiliary_component(weapon)
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_DEPLOY, time.time())
        if self.sd.ref_in_aim:
            self.send_event('E_QUIT_AIM')
        if self.sd.ref_in_right_aim:
            self.send_event('E_QUIT_RIGHT_AIM')
        if weapon.get_effective_value('iMode') != weapon_const.MANUAL_MODE:
            weapon.set_bolted(1)
        if is_init:
            self.gun_status.set_status(weapon_const.FIRE_STATE_READY)
            self.send_event('E_FINISH_SWITCH_GUN', weapon.get_pos())
            self._switched(weapon)
            self.on_init_complete()
        else:
            import common.cfg.confmgr as confmgr
            itvl = weapon.get_effective_value('fTakeTime')
            if not itvl:
                self._switched(weapon)
            else:
                self._timer_func(itvl, callback=self._switched, args=(weapon,))
        if not self._is_puppet_com:
            self.auto_check()
        return True

    def _try_aim(self, serve_sync_back=False):
        if not self.cur_wp:
            self.send_event('E_SHOW_MESSAGE', get_text_local_content(18011))
            return
        else:
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
            if lens_attachment is None:
                return
            status, now = self.gun_status.do_status()
            if status in [weapon_const.FIRE_STATE_RELOAD_EMPTY, weapon_const.FIRE_STATE_RELOAD_LEFT]:
                self.send_event('E_SHOW_MESSAGE', get_text_local_content(18012))
                return
            if status in [weapon_const.FIRE_STATE_AIM, weapon_const.FIRE_STATE_QUIT_AIM]:
                return
            if self.ev_g_is_jump():
                self.send_event('E_SHOW_MESSAGE', get_text_local_content(18013))
                return
            if self.sd.ref_in_aim:
                return
            if not self.ev_g_trans_status(ST_AIM, sync=True):
                return
            self._lens_in_aim = lens_attachment
            self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_AIM, now)
            lens_attr = lens_attachment.get('cAttr', {})
            fAnimTime = lens_attr.get('fAimTime', 0.4)
            if self._delay_callback != self._on_loading:
                self._timer_func(fAnimTime, callback=self._aim_in_transfered, args=(True,))
            self.send_event('E_SUCCESS_AIM')
            self._aim_transfer_duration = fAnimTime
            self._start_aim_transfer_time = time.time()
            self._start_aim_transfer = True
            return

    def _aim_in_transfered(self, auto_fire=False):
        self.clear_timer()
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())
        if self.cur_wp and self.cur_wp.is_accumulate_gun() and auto_fire:
            self.send_event('E_START_AUTO_FIRE')
        self._start_aim_transfer = False

    def _aim_quit_transfered(self):
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())
        self.send_event('E_FINISH_QUIT_AIM')
        if self.cur_wp:
            if self.cur_wp.get_bullet_num() <= 0:
                global_data.game_mgr.next_exec(self._try_reload)
            elif self.cur_wp.get_bolted() < 1:
                global_data.game_mgr.next_exec(self._on_loading)

    def _quit_aim(self):
        if self.cur_wp and self.cur_wp.is_accumulate_gun():
            self.send_event('E_STOP_AUTO_FIRE', force=False, fire=False)
        self._end_aim_camera_state()
        if not self.enable:
            self._lens_in_aim = None
            self._aim_in_transfered()
            return
        else:
            status, now = self.gun_status.do_status()
            if status in [weapon_const.FIRE_STATE_RELOAD_EMPTY, weapon_const.FIRE_STATE_RELOAD_LEFT, weapon_const.FIRE_STATE_AIM, weapon_const.FIRE_STATE_QUIT_AIM]:
                return
            self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_QUIT_AIM, now)
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            fAimQuitTime = -1
            if self.cur_wp:
                lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
                if lens_attachment:
                    lens_attr = lens_attachment.get('cAttr', {})
                    fAimQuitTime = lens_attr.get('fAimQuitTime', 0.4)
            if fAimQuitTime < 0 and self._lens_in_aim is not None:
                lens_attr = self._lens_in_aim.get('cAttr', {})
                fAimQuitTime = lens_attr.get('fAimQuitTime', 0.4)
            else:
                fAimQuitTime = 0.01
            self._lens_in_aim = None
            self._timer_func(fAimQuitTime, callback=self._aim_quit_transfered, args=None)
            return

    def g_is_in_aim(self):
        return self.sd.ref_in_aim

    def _die(self, *args):
        self.unload_weapon()

    def _on_reloaded(self, reload_num, wp_pos, t_use=None):
        if not self._is_puppet_com:
            return
        if not self.cur_wp:
            return
        self.cur_wp.reload(reload_num)
        self.cur_wp.dirty = True
        self.send_event('E_WEAPON_DATA_CHANGED', self.cur_wp.get_pos())
        self.send_event('E_CUR_BULLET_NUM_CHG', self.cur_wp.get_pos())

    def g_is_in_right_aim(self):
        return self.sd.ref_in_right_aim

    def _right_aim_in_transfered(self):
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())

    def _right_aim_quit_transfered(self):
        self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_READY, time.time())
        self.send_event('E_FINISH_QUIT_RIGHT_AIM')
        if self.cur_wp:
            if self.cur_wp.get_bullet_num() <= 0:
                global_data.game_mgr.next_exec(self._try_reload)
            elif self.cur_wp.get_bolted() < 1:
                global_data.game_mgr.next_exec(self._on_loading)

    def _try_right_aim(self):
        if not self.cur_wp:
            self.send_event('E_SHOW_MESSAGE', get_text_local_content(18011))
            return
        else:
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            lens_attachment = self.cur_wp.get_attachment_attr(ATTACHEMNT_AIM_POS)
            if lens_attachment is not None:
                return
            status, now = self.gun_status.do_status()
            if status in [weapon_const.FIRE_STATE_AIM, weapon_const.FIRE_STATE_QUIT_AIM]:
                return
            if status in [weapon_const.FIRE_STATE_RIGHT_AIM, weapon_const.FIRE_STATE_QUIT_RIGHT_AIM]:
                return
            from logic.gutils.item_utils import check_can_right_aim
            if not check_can_right_aim(self.cur_wp.get_item_id()):
                return
            if self.sd.ref_in_aim or self.sd.ref_in_right_aim:
                return
            if not self.ev_g_status_try_trans(ST_RIGHT_AIM):
                return
            fAnimTime = 0.1
            self._timer_func(fAnimTime, callback=self._right_aim_in_transfered, args=None)
            self.sd.ref_in_right_aim = True
            self.send_event('E_SUCCESS_RIGHT_AIM')
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_TRY_RIGHT_AIM, ()], False)
            return

    def _end_right_aim_camera_state(self, *args):
        self.sd.ref_in_right_aim = False
        if self.cur_wp:
            if self.cur_wp.get_bullet_num() <= 0:
                global_data.game_mgr.next_exec(self._try_reload)
            else:
                global_data.game_mgr.next_exec(self._on_loading)

    def _quit_right_aim(self):
        self._end_right_aim_camera_state()
        self.ev_g_cancel_state(ST_RIGHT_AIM)
        if not self.enable:
            self._right_aim_quit_transfered()
            return
        else:
            status, now = self.gun_status.do_status()
            if status in [weapon_const.FIRE_STATE_RELOAD_EMPTY, weapon_const.FIRE_STATE_RELOAD_LEFT,
             weapon_const.FIRE_STATE_AIM, weapon_const.FIRE_STATE_QUIT_AIM,
             weapon_const.FIRE_STATE_RIGHT_AIM, weapon_const.FIRE_STATE_QUIT_RIGHT_AIM]:
                return
            self.gun_status.set_status_and_time(weapon_const.FIRE_STATE_QUIT_RIGHT_AIM, now)
            fAimQuitTime = 0.1
            self._timer_func(fAimQuitTime, callback=self._right_aim_quit_transfered, args=None)
            return

    def get_multi_shape_weapon(self, weapon, weapon_pos, level):
        return None