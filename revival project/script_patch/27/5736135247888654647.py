# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGunShieldLogic.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import GROUP_DYNAMIC_SHOOTUNIT, GROUP_GRENADE
from logic.gcommon.common_const.weapon_const import GUN_SHIELD_OPEN_CONDITION_ALWAYS, GUN_SHIELD_OPEN_CONDITION_RIGHT_AIM
from logic.gcommon.common_const.animation_const import WEAPON_POS_LEFT
from logic.gcommon.item.item_const import DRESS_POS_SHIELD
from common.utils.timer import CLOCK, RELEASE
from common.cfg import confmgr
from math import pi
import collision
import math3d
import random
STRANGE_DIR_WEAPONS = (10652, 10653, 10654, 10656)

def get_collision_size_vector(weapon_id, width, depth, height):
    if weapon_id in STRANGE_DIR_WEAPONS:
        return math3d.vector(height, depth, width)
    return math3d.vector(depth, width, height)


class ComGunShieldLogic(UnitCom):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'check_add_gun_shield',
       'E_GUN_MODEL_LOADED': 'on_gun_model_loaded',
       'E_CHECK_ADD_GUN_SHIELD': 'check_add_gun_shield',
       'E_CHECK_REMOVE_GUN_SHIELD': 'check_remove_gun_shield',
       'E_ON_JOIN_MECHA': 'check_remove_gun_shield',
       'E_ON_LEAVE_MECHA': 'check_add_gun_shield',
       'G_RANDOM_SHIELD_POS': 'get_random_shield_pos',
       'E_RESUME_HUMAN_COLLISION': 'check_add_gun_shield',
       'G_IS_SHIELD_OPENED': 'check_shield_opened'
       }

    def __init__(self):
        super(ComGunShieldLogic, self).__init__()
        self.process_condition_func_map = {GUN_SHIELD_OPEN_CONDITION_ALWAYS: self._update_shield_opened_state,
           GUN_SHIELD_OPEN_CONDITION_RIGHT_AIM: self._process_condition_right_aim
           }

    def init_from_dict(self, unit_obj, bdict):
        super(ComGunShieldLogic, self).init_from_dict(unit_obj, bdict)
        self.shield_col_map = {}
        self.event_registered_map = {}
        self.shield_active_map = {}
        self.shield_bound_map = {}
        self.cache_custom_conf = {}
        self.cur_shield_col = None
        self.check_open_shield_timer = None
        self.last_shield_duration_percent = 0.0
        self.shield_state_sfx_id = None
        self.sound_mgr = global_data.sound_mgr
        self.shield_sound_id = self.sound_mgr.register_game_obj('gun_shield')
        self.sound_suffix = '_3p'
        self.loop_sound_player_id = None
        return

    def on_init_complete(self):
        if self.ev_g_is_avatar():
            self.sound_suffix = '_1p'

    def _register_check_open_shield_timer(self):
        if not self.check_open_shield_timer:
            self.check_open_shield_timer = global_data.game_mgr.register_logic_timer(self._check_can_open_shield, interval=0.1, times=-1, mode=CLOCK)

    def _unregister_check_open_shield_timer(self):
        if self.check_open_shield_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_open_shield_timer)
            self.check_open_shield_timer = None
        return

    def _remove_shield_state_sfx(self):
        if self.shield_state_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.shield_state_sfx_id)
            self.shield_state_sfx_id = None
        return

    def _clear_all_col(self):
        for weapon_id, conf in six.iteritems(self.cache_custom_conf):
            condition = conf.get('open_condition', GUN_SHIELD_OPEN_CONDITION_ALWAYS)
            self.process_condition_func_map[condition](weapon_id, False)

        self.shield_col_map.clear()
        self.event_registered_map.clear()
        self.shield_active_map.clear()
        self.shield_bound_map.clear()
        self.cache_custom_conf.clear()
        self.cur_shield_col = None
        self._unregister_check_open_shield_timer()
        self._remove_shield_state_sfx()
        if self.sound_mgr:
            if self.loop_sound_player_id is not None:
                self.sound_mgr.stop_playing_id(self.loop_sound_player_id)
                self.loop_sound_player_id = None
                self.need_update = False
            self.sound_mgr.unregister_game_obj(self.shield_sound_id)
            self.sound_mgr = None
        return

    def destroy(self):
        self._clear_all_col()
        self.process_condition_func_map.clear()
        super(ComGunShieldLogic, self).destroy()

    def _arm_shield(self, flag):
        if self.sd.ref_wp_bar_cur_weapon:
            event_name = 'E_WEAPON_SHIELD_GUN_LOAD' if flag else 'E_WEAPON_SHIELD_GUN_UNLOAD'
            self.send_event(event_name, self.sd.ref_wp_bar_cur_weapon.get_pos())

    def _update_shield_opened_state(self, weapon_id, flag):
        if self.shield_active_map[weapon_id] ^ flag:
            self._arm_shield(flag)
            self.shield_active_map[weapon_id] = flag
        if self.shield_bound_map[weapon_id] ^ flag:
            func = self._bind_shield_col if flag else self._unbind_shield_col
            func(weapon_id)

    def _check_can_open_shield(self):
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if cur_weapon and cur_weapon.check_shield_owned() and cur_weapon.check_can_open_shield():
            weapon_id = cur_weapon.get_id()
            self._update_shield_opened_state(weapon_id, True)
            if self.shield_bound_map[weapon_id]:
                self.check_open_shield_timer = None
                return RELEASE
        return

    def on_begin_right_aim(self):
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        weapon_id = cur_weapon.get_id()
        self._update_shield_opened_state(weapon_id, cur_weapon.check_can_open_shield())
        if not self.shield_bound_map[weapon_id]:
            self._register_check_open_shield_timer()
        else:
            armor = self.ev_g_amror_by_pos(DRESS_POS_SHIELD)
            self.on_armor_data_changed(DRESS_POS_SHIELD, armor)

    def on_end_right_aim(self):
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if not cur_weapon:
            return
        weapon_id = cur_weapon.get_id()
        self._update_shield_opened_state(weapon_id, False)
        self._unregister_check_open_shield_timer()

    def on_gun_shield_broken(self):
        self.on_end_right_aim()
        if self.sd.ref_in_right_aim:
            cur_weapon = self.sd.ref_wp_bar_cur_weapon
            weapon_id = cur_weapon.get_id()
            self._update_shield_opened_state(weapon_id, False)
            if not self.shield_bound_map[weapon_id]:
                self._register_check_open_shield_timer()

    def on_armor_data_changed(self, pos, armor):
        if pos == DRESS_POS_SHIELD and armor:
            cur_weapon = self.sd.ref_wp_bar_cur_weapon
            if not cur_weapon:
                return
            weapon_id = cur_weapon.get_id()
            conf = self.cache_custom_conf[weapon_id]
            if 'sfx_conf' not in conf:
                return
            cur_percent = armor.get_duration_percent()
            if cur_percent == 0.0:
                if conf.get('broken_sound'):
                    pos = self.ev_g_position()
                    pos and self.sound_mgr.post_event(conf['broken_sound'] + self.sound_suffix, self.shield_sound_id, pos)
                self.on_gun_shield_broken()
            if cur_percent > self.last_shield_duration_percent:
                self.last_shield_duration_percent = cur_percent + 0.01
                for percent in six.iterkeys(conf['sfx_conf']):
                    if cur_percent <= percent:
                        break
                else:
                    self._remove_shield_state_sfx()

            for percent, sfx_info in six.iteritems(conf['sfx_conf']):
                if cur_percent <= percent < self.last_shield_duration_percent:
                    socket = sfx_info['socket']
                    path = sfx_info['path']
                    is_left = conf.get('is_left')
                    gun_model = self.sd.ref_left_hand_weapon_model if is_left else self.sd.ref_hand_weapon_model
                    self._remove_shield_state_sfx()
                    if gun_model and gun_model.valid:
                        self.shield_state_sfx_id = global_data.sfx_mgr.create_sfx_on_model(path, gun_model, socket)
                        self.last_shield_duration_percent = cur_percent
                    break

    def _process_condition_right_aim(self, weapon_id, flag):
        if self.event_registered_map[weapon_id] ^ flag:
            func = self.regist_event if flag else self.unregist_event
            func('E_SUCCESS_RIGHT_AIM', self.on_begin_right_aim)
            func('E_QUIT_RIGHT_AIM', self.on_end_right_aim)
            func('E_ARMOR_DATA_CHANGED', self.on_armor_data_changed)
            self.event_registered_map[weapon_id] = flag
        if flag and self.sd.ref_in_right_aim:
            self.on_begin_right_aim()
        else:
            self.on_end_right_aim()

    def tick(self, dt):
        pos = self.ev_g_position()
        pos and self.sound_mgr.set_position(self.shield_sound_id, pos)

    def _bind_shield_col(self, weapon_id):
        conf = self.cache_custom_conf[weapon_id]
        is_left = conf.get('is_left')
        if is_left:
            gun_model = self.sd.ref_left_hand_weapon_model if 1 else self.sd.ref_hand_weapon_model
            if gun_model and gun_model.valid:
                shield_col = self.shield_col_map[weapon_id]
                bone_name = conf.get('bind_bone_name', '')
                bone_name or print('({}--cCustomParam)\xe7\xbb\x91\xe5\xae\x9a\xe9\xaa\xa8\xe9\xaa\xbc\xe9\x83\xbd\xe4\xb8\x8d\xe5\xa1\xab\xef\xbc\x8c\xe9\x9a\xbe\xe6\x90\x9e\xe5\x93\xa6'.format(weapon_id))
                return
            if conf.get('open_shield_anim'):
                gun_model.play_animation(conf['open_shield_anim'])
            pos = self.ev_g_position()
            if pos:
                if conf.get('open_sound'):
                    self.sound_mgr.post_event(conf['open_sound'] + self.sound_suffix, self.shield_sound_id, pos)
                if conf.get('loop_sound'):
                    self.loop_sound_player_id = self.sound_mgr.post_event(conf['loop_sound'] + self.sound_suffix, self.shield_sound_id, pos)
                    self.need_update = True
            gun_model.bind_col_obj(shield_col, bone_name)
            self.scene.scene_col.add_object(shield_col)
            global_data.emgr.scene_add_common_shoot_obj.emit(shield_col.cid, self.unit_obj)
            self.send_event('E_NOTIFY_GUN_SHIELD_COL_BOUND', shield_col, True)
            self.shield_bound_map[weapon_id] = True
            self.cur_shield_col = shield_col
            self.sd.ref_raise_shield = True
            if self.ev_g_is_avatar() or self.sd.ref_is_agent:
                self.send_event('E_CALL_SYNC_METHOD', 'load_weapon_shield', (), True)

    def _unbind_shield_col(self, weapon_id):
        shield_col = self.shield_col_map[weapon_id]
        conf = self.cache_custom_conf[weapon_id]
        is_left = conf.get('is_left')
        gun_model = self.sd.ref_left_hand_weapon_model if is_left else self.sd.ref_hand_weapon_model
        if gun_model and gun_model.valid:
            gun_model.unbind_col_obj(shield_col)
            if conf.get('open_shield_anim'):
                gun_model.play_animation(conf['default_anim'])
            if self.loop_sound_player_id is not None:
                self.sound_mgr.stop_playing_id(self.loop_sound_player_id)
                self.loop_sound_player_id = None
                self.need_update = False
            if conf.get('close_sound'):
                cur_weapon = self.sd.ref_wp_bar_cur_weapon
                if cur_weapon and cur_weapon.check_can_open_shield():
                    pos = self.ev_g_position()
                    pos and self.sound_mgr.post_event(conf['close_sound'] + self.sound_suffix, self.shield_sound_id, pos)
        global_data.emgr.scene_remove_common_shoot_obj.emit(shield_col.cid)
        self.scene.scene_col.remove_object(shield_col)
        self.send_event('E_NOTIFY_GUN_SHIELD_COL_BOUND', shield_col, False)
        self.shield_bound_map[weapon_id] = False
        self.cur_shield_col = None
        self.sd.ref_raise_shield = False
        if self.ev_g_is_avatar() or self.sd.ref_is_agent:
            self.send_event('E_CALL_SYNC_METHOD', 'unload_weapon_shield', (), True)
        return

    def _ensure_shield_data_ready(self, cur_weapon, weapon_id):
        if weapon_id not in self.shield_col_map:
            conf = cur_weapon.conf('cCustomParam', {})
            self.cache_custom_conf[weapon_id] = conf
            conf['open_condition'] = cur_weapon.get_effective_value('iShieldOpenCondition')
            sfx_conf = confmgr.get('firearm_res_config', str(weapon_id), 'cCustomParam', default=[{}])[0]
            if sfx_conf:
                self.cache_custom_conf[weapon_id]['sfx_conf'] = {}
                for ratio, sfx_info in six.iteritems(sfx_conf):
                    ratio = float(ratio)
                    self.cache_custom_conf[weapon_id]['sfx_conf'][ratio] = sfx_info

            height = conf.get('col_height', 8.0)
            depth = conf.get('col_depth', 1.0)
            width = conf.get('col_width', 4.0)
            self.shield_col_map[weapon_id] = collision.col_object(collision.BOX, get_collision_size_vector(weapon_id, width, depth, height), GROUP_GRENADE, GROUP_DYNAMIC_SHOOTUNIT, 0)
            self.event_registered_map[weapon_id] = False
            self.shield_active_map[weapon_id] = False
            self.shield_bound_map[weapon_id] = False

    def on_gun_model_loaded(self, gun_model, gun_enable_hand_ik, hand_pos):
        if not self.is_enable():
            return
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if not cur_weapon or not cur_weapon.check_shield_owned():
            return
        weapon_id = cur_weapon.get_id()
        self._ensure_shield_data_ready(cur_weapon, weapon_id)
        conf = self.cache_custom_conf[weapon_id]
        is_left = bool(conf.get('is_left'))
        if is_left ^ (hand_pos == WEAPON_POS_LEFT):
            return
        condition = conf.get('open_condition', GUN_SHIELD_OPEN_CONDITION_ALWAYS)
        self.process_condition_func_map[condition](weapon_id, True)

    def check_add_gun_shield(self, *args, **kwargs):
        if not self.is_enable():
            return
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if not cur_weapon or not cur_weapon.check_shield_owned():
            return
        weapon_id = cur_weapon.get_id()
        self._ensure_shield_data_ready(cur_weapon, weapon_id)
        conf = self.cache_custom_conf[weapon_id]
        condition = conf.get('open_condition', GUN_SHIELD_OPEN_CONDITION_ALWAYS)
        self.process_condition_func_map[condition](weapon_id, True)

    def check_remove_gun_shield(self, *args, **kwargs):
        if not self.is_enable():
            return
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if not cur_weapon or not cur_weapon.check_shield_owned():
            return
        weapon_id = cur_weapon.get_id()
        self._ensure_shield_data_ready(cur_weapon, weapon_id)
        conf = self.cache_custom_conf[weapon_id]
        condition = conf.get('open_condition', GUN_SHIELD_OPEN_CONDITION_ALWAYS)
        self.process_condition_func_map[condition](weapon_id, False)

    def get_random_shield_pos(self):
        if not self.cur_shield_col:
            return None
        else:
            mat = self.cur_shield_col.rotation_matrix
            right = mat.right * random.uniform(0, 3)
            rot = math3d.matrix.make_rotation(mat.up, random.uniform(-pi, pi))
            return self.cur_shield_col.position + right * rot

    def check_shield_opened(self):
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if not cur_weapon:
            return False
        weapon_id = cur_weapon.get_id()
        return self.shield_bound_map.get(weapon_id, False)