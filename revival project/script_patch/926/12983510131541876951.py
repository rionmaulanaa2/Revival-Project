# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaActivateClient.py
from __future__ import absolute_import
import six
from six.moves import range
from ..UnitCom import UnitCom
from logic.gcommon.common_const import mecha_const
import logic.gcommon.const as g_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata import mecha_status_config
from mobile.common.EntityManager import EntityManager
import math3d
import collision
from logic.gcommon.common_const import attr_const
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, GROUP_DEFAULT_VISIBLE
from logic.gutils.client_unit_tag_utils import preregistered_tags

class ComMechaActivateClient(UnitCom):
    BIND_EVENT = {'E_HANDLE_ADD_BUFF': '_handle_buff',
       'E_HANDLE_DEL_BUFF': '_remove_buff',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'G_BALL_STATE': '_get_ball_state',
       'G_BALL_OVERLOAD_STATE': '_get_ball_overload_state',
       'G_BALL_OVERLOAD': '_get_overload',
       'G_OIL_DEBUFF': '_get_oil_debuff',
       'G_FIRE_DEBUFF': '_get_fire_debuff',
       'G_DIZZINESS_DEBUFF': '_get_dizziness_debuff',
       'G_XRAY_RANGE_INFO': 'get_xray_range_info',
       'G_EMP_DEBUFF': '_get_emp_debuff'
       }

    def __init__(self):
        super(ComMechaActivateClient, self).__init__(need_update=False)
        self.ball_state_left_time = 0
        self.ball_state_duration = 30
        self.ball_normal_duration = 20
        self.ball_overload_left_time = 0
        self.ball_overload_duration = 10
        self._oil_debuff = False
        self._fire_debuff = False
        self._dizziness_debuff = False
        self._emp_debuff = False
        self._xray_range_radius = 0
        self._xray_range_total_time = 0
        self._xray_range_start_time = 0
        self.charge_time_factor = 0
        self.rogue_accumulate_factor = 0
        self.rogue_interval_factor = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaActivateClient, self).init_from_dict(unit_obj, bdict)

    def _handle_buff(self, hdl_name, data, left_time, overlying):
        handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
        if handler:
            handler(data, left_time, overlying)
        return

    def _remove_buff(self, hdl_name, buff_key, buff_id, buff_idx):
        handler = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
        if handler:
            handler(buff_key, buff_id, buff_idx)
        return

    def _on_leave_mecha(self, *args):
        self.ball_state_left_time = 0
        self.ball_overload_left_time = 0

    def handle_main_weapon_shot_speed(self, data, *args):
        val = data.get('val', 0)
        if val:
            self.send_event('E_SHOW_SHOT_SPEED_INCREASE_EFFECT', True)

    def del_main_weapon_shot_speed(self, buff_key, buff_id, buff_idx):
        self.send_event('E_SHOW_SHOT_SPEED_INCREASE_EFFECT', False)

    def handle_sub_weapon_missile_num(self, data, *args):
        import copy
        val = data.get('val', 2)
        wp_pos = data.get('wp_pos', g_const.PART_WEAPON_POS_MAIN2)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(wp_pos)
        if weapon:
            conf = weapon.get_config()
            effective_conf = weapon.get_effective_config()
            ori_data = copy.deepcopy(effective_conf.get('iPellets', conf['iPellets']))
            if not ori_data.get('bullets', None):
                log_error('ComMechaActivateClient handle_sub_weapon_missile_num bullets error.')
                return
            for i in range(val / 2):
                ori_data['bullets'].append(2)

            effective_conf['iPellets'] = ori_data
        return

    def del_sub_weapon_missile_num(self, buff_key, buff_id, buff_idx):
        import copy
        from common.cfg import confmgr
        ext_info = confmgr.get('c_buff_data', str(buff_id), 'ExtInfo')
        val = ext_info.get('val', 2)
        wp_pos = ext_info.get('wp_pos', g_const.PART_WEAPON_POS_MAIN2)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(wp_pos)
        if weapon:
            conf = weapon.get_config()
            effective_conf = weapon.get_effective_config()
            ori_data = copy.deepcopy(effective_conf.get('iPellets', conf['iPellets']))
            if not ori_data.get('bullets', None):
                log_error('ComMechaActivateClient del_sub_weapon_missile_num bullets error.')
                return
            for i in range(val / 2):
                ori_data['bullets'].pop()

            effective_conf['iPellets'] = ori_data
        return

    def handle_mod_weapon_pellets_data(self, data, *args):
        pdata = data.get('p_data', None)
        wp_pos_list = data.get('wp_pos', [])
        if not wp_pos_list or not data:
            return
        else:
            for wp_pos in wp_pos_list:
                weapon = self.sd.ref_wp_bar_mp_weapons.get(wp_pos)
                if weapon:
                    effective_conf = weapon.get_effective_config()
                    effective_conf['iPellets'] = pdata
                if isinstance(pdata, int):
                    effective_conf['fShowRatio'] = -pdata
                    lplayer = global_data.cam_lplayer
                    if lplayer:
                        mecha = lplayer.ev_g_ctrl_mecha_obj()
                        if mecha and mecha.logic:
                            mecha.logic.send_event('E_WEAPON_DATA_CHANGED', wp_pos)

            return

    def handle_add_weapon_custom_data(self, data, *args):
        wp_pos_list = data.get('wp_pos', [])
        c_data = data.get('data', {})
        if not wp_pos_list or not c_data:
            return
        for wp_pos in wp_pos_list:
            weapon = self.sd.ref_wp_bar_mp_weapons.get(wp_pos)
            if weapon:
                effective_conf = weapon.get_effective_config()
                effective_conf.setdefault('cCustomParam', {})
                effective_conf['cCustomParam'].update(c_data)

    def handle_breakthrough_8004_tarck_wp(self, data, *args):
        pos = data.get('pos')
        self.send_event('E_ENABLE_BREAKTHROUGH_8004_TRACK_WP', pos)

    def handle_breakthrough_8004_enhance_tarck_wp(self, data, *args):
        self.send_event('E_ENHANCE_BREAKTHROUGH_8004_TRACK_WP')

    def handle_mod_weapon_sd_data(self, data, *args):
        sd_key = data.get('sd_key', None)
        sd_val = data.get('sd_val', None)
        wp_pos = data.get('wp_pos', None)
        if wp_pos is None or sd_key is None or sd_val is None:
            return
        else:
            weapon = self.sd.ref_wp_bar_mp_weapons.get(wp_pos)
            if weapon:
                weapon.set_key_config_value(sd_key, sd_val)
            return

    def handle_mod_add_client_attr(self, data, *args):
        attr = data.get('attr', None)
        if attr is None:
            return
        else:
            mod = data.get('val', 0)
            item_ids = data.get('item_ids', [])
            source_info = data.get('source_info', None)
            if item_ids:
                for item_id in item_ids:
                    self.send_event('E_MOD_ADD_ATTR', attr, mod, item_id, source_info)

            else:
                self.send_event('E_MOD_ADD_ATTR', attr, mod)
            return

    def del_mod_add_client_attr(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        if buff_info:
            attr = buff_info.get('attr', None)
            if not attr:
                return
            val = buff_info.get('val', 0)
            item_ids = buff_info.get('item_ids', [])
            source_info = buff_info.get('source_info', None)
            if isinstance(val, bool):
                mod = not val
            elif isinstance(val, (int, float)):
                mod = -val
            if item_ids:
                for item_id in item_ids:
                    self.send_event('E_MOD_ADD_ATTR', attr, mod, item_id, source_info)

            else:
                self.send_event('E_MOD_ADD_ATTR', attr, mod)
        return

    def handle_move_speed(self, data, *args):
        val = data.get('val', 0.15)
        speed_scale = self.ev_g_speed_scale() or self.ev_g_get_speed_scale()
        if speed_scale is None:
            if self.ev_g_is_avatar():
                raise RuntimeError("handle_move_speed can't get move_speed!", self.sd.ref_mecha_id)
            else:
                return
        self.send_event('E_SET_SPEED_SCALE', speed_scale + val)
        return

    def del_move_speed(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        if buff_info:
            val = buff_info.get('val', 0.15)
            speed_scale = self.ev_g_speed_scale() or self.ev_g_get_speed_scale()
            if speed_scale is None:
                if self.ev_g_is_avatar():
                    raise RuntimeError("del_move_speed can't get move_speed!", self.sd.ref_mecha_id)
                else:
                    return
            self.send_event('E_SET_SPEED_SCALE', speed_scale - val)
        return

    def handle_reload_speed(self, data, *args):
        pass

    def del_reload_speed(self, buff_key, buff_id, buff_idx):
        pass

    def _mod_reload_speed(self, wp_pos_list, val):
        if not val:
            return
        if not isinstance(wp_pos_list, (list, tuple)):
            wp_pos_list = (
             wp_pos_list,)
        for wp_pos in wp_pos_list:
            factor_name = 'reload_speed_factor_pos_%s' % wp_pos
            self.send_event('E_MOD_ADD_ATTR', factor_name, val)

    def handle_sword_core(self, buff_info, left_time, overlying):
        speed_scale = 1 / (1 + buff_info.get('atk_spd_factor', 0))
        scale_states = [mecha_status_config.MC_SWORD_ENERGY, mecha_status_config.MC_CUT_RUSH]
        for sid in scale_states:
            self.send_event('E_STATE_SPEED_SCALE', sid, speed_scale)

        self.send_event('E_BUFF_SPD_ADD_STANDALONE', buff_info['BuffId'], buff_info)
        self.send_event('E_SHOW_SOWRD_CORE_EFFECT', True)
        self.send_event('E_ENABLE_DYNAMIC_SPEED_RATE', False)

    def del_sword_core(self, buff_key, buff_id, buff_idx):
        scale_states = [
         mecha_status_config.MC_SWORD_ENERGY, mecha_status_config.MC_CUT_RUSH]
        for sid in scale_states:
            self.send_event('E_STATE_SPEED_SCALE', sid, 1)

        self.send_event('E_BUFF_SPD_DEL_STANDALONE', buff_id)
        self.send_event('E_SHOW_SOWRD_CORE_EFFECT', False)
        self.send_event('E_ENABLE_DYNAMIC_SPEED_RATE', True)

    def handle_bullet_max_num(self, data, *args):
        change_val = data.get('add_mag_size', 4)
        weapon_pos = data.get('wp_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.send_event('E_CHANGE_WEAPON_BULLET_CAP', weapon_pos, change_val)
        if not data.get('installed_before', True):
            self.send_event('E_RELOAD_WIHTOUT_ACTION', weapon_pos)

    def del_bullet_max_num(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        change_val = buff_info.get('add_mag_size', 4)
        weapon_pos = buff_info.get('wp_pos', g_const.PART_WEAPON_POS_MAIN1)
        self.send_event('E_CHANGE_WEAPON_BULLET_CAP', weapon_pos, -change_val)

    def handle_eject(self, data, *args):
        if self.ev_g_is_avatar():
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_EJECT_PARAM', data['eject_speed'] * NEOX_UNIT_SCALE, data['eject_time'], data['eject_acc'] * NEOX_UNIT_SCALE, data['eject_gravity'] * NEOX_UNIT_SCALE)

    def handle_beat_back(self, data, *args):
        pos = data.get('bomb_position', (0, 0, 0)) or (0, 0, 0)
        self.send_event('E_BEAT_BACK', math3d.vector(*pos), data.get('coe_v', 1), data.get('coe_h', 1), data.get('effect_type', 0))

    def handle_beat_back_self(self, data, *args):
        pos = data.get('bomb_position', (0, 0, 0)) or (0, 0, 0)
        if global_data.mecha and global_data.mecha.logic:
            position = global_data.mecha.logic.ev_g_position() + math3d.vector(0, NEOX_UNIT_SCALE, 0)
            scene = global_data.game_mgr.get_cur_scene()
            result = scene.scene_col.hit_by_ray(position, pos, 0, 65535, GROUP_CAN_SHOOT, collision.INCLUDE_FILTER, True)
            if result[0]:
                for info in result[1]:
                    unit = global_data.emgr.scene_find_unit_event.emit(info[4].cid)[0]
                    if unit is None:
                        return

        self.send_event('E_BEAT_BACK', math3d.vector(*pos), data.get('coe_v', 1), data.get('coe_h', 1), data.get('effect_type', 0))
        return

    def handle_mod_explosive_item_attr(self, data, *args):
        item_ids = data['item_id']
        if isinstance(item_ids, int):
            item_ids = [
             item_ids]
        for attr_name, value in data['attr']:
            for item_id in item_ids:
                self.send_event('E_MOD_ADD_ATTR', attr_name, value, item_id)

    def del_mod_explosive_item_attr(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        item_ids = data['item_id']
        if isinstance(item_ids, int):
            item_ids = [
             item_ids]
        for attr_name, value in data['attr']:
            for item_id in item_ids:
                self.send_event('E_MOD_ADD_ATTR', attr_name, -value, item_id)

    def handle_mod_glide_time(self, data, *args):
        delta = data.get('addition_ratio', 0)
        self.send_event('E_ADD_GLIDE_TIME', delta)

    def del_mod_glide_time(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        delta = data.get('addition_ratio', 0)
        self.send_event('E_ADD_GLIDE_TIME', -delta)

    def handle_mod_init_energy(self, data, *args):
        mod_ratio = data.get('val', 0)
        self.send_event('E_MOD_INIT_ENERY', mod_ratio)

    def del_mod_init_energy(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        mod_ratio = data.get('val', 0)
        self.send_event('E_MOD_INIT_ENERY', -mod_ratio)

    def handle_mod_charge_time(self, data, *args):
        dec_percent = data.get('dec_percent', 0)
        wp_pos = data.get('wp_pos', 1)
        self.charge_time_factor = dec_percent
        self.send_event('E_ACC_ACCUMULATE_CD', dec_percent, wp_pos)

    def del_mod_charge_time(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        wp_pos = data.get('wp_pos', 1)
        self.send_event('E_ACC_ACCUMULATE_CD', -self.charge_time_factor, wp_pos)
        self.charge_time_factor = 0

    def handle_roguegift_8013_accumulate(self, data, *args):
        dec_percent = self.ev_g_add_attr(attr_const.ATTR_ACCUMULATE_GUN_FACTOR) or 0
        self.rogue_accumulate_factor = dec_percent
        self.send_event('E_ROGUE_ACCUMULATE_GUN_FACTOR', dec_percent)

    def del_roguegift_8013_accumulate(self, buff_key, buff_id, buff_idx):
        self.send_event('E_ROGUE_ACCUMULATE_GUN_FACTOR', -self.rogue_accumulate_factor)
        self.rogue_accumulate_factor = 0

    def handle_roguegift_8023_interval(self, data, *args):
        interval_factor = self.ev_g_add_attr(attr_const.ATTR_WEAPON_INTERVAL_FACTOR) or 0
        self.rogue_interval_factor = interval_factor
        self.send_event('E_ROGUE_WEAPON_INTERVAL_FACTOR', interval_factor)

    def del_roguegift_8023_interval(self, buff_key, buff_id, buff_idx):
        interval_factor = self.ev_g_add_attr(attr_const.ATTR_WEAPON_INTERVAL_FACTOR) or 0
        self.send_event('E_ROGUE_WEAPON_INTERVAL_FACTOR', -self.rogue_interval_factor)
        self.rogue_interval_factor = 0

    def handle_roguegift_8026_turn(self, data, *args):
        self.send_event('E_ROGUE_GIFT_8026', True, data.get('camera_sense'))

    def del_roguegift_8026_turn(self, buff_key, buff_id, buff_idx):
        self.send_event('E_ROGUE_GIFT_8026', False, None)
        return

    def _parse_logic_state_param(self, attr):
        pos = attr.find('_')
        if pos == -1 or pos > len(attr):
            return (None, None)
        else:
            state_name = attr[1:pos]
            parameter_name = attr[pos + 1:]
            return (
             state_name, parameter_name)

    def handle_mod_state_param(self, data, left_time, overlying):
        params_dict = data.get('params_dict', {})
        state_parameters = dict()
        for attr, mod_factor in six.iteritems(params_dict):
            old_attr_factor = self.ev_g_attr_get(attr, 0.0)
            now_attr_factor = old_attr_factor + mod_factor
            self.send_event('S_ATTR_SET', attr, now_attr_factor)
            state_name, parameter_name = self._parse_logic_state_param(attr)
            if state_name:
                if state_name not in state_parameters:
                    state_parameters[state_name] = dict()
                state_parameters[state_name][parameter_name] = now_attr_factor

        for state_name, parameters in six.iteritems(state_parameters):
            self.send_event('E_LOGIC_STATE_PARAM_CHANGED_' + state_name, parameters)

    def del_mod_state_param(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        params_dict = data.get('params_dict', {})
        state_parameters = dict()
        for attr, mod_factor in six.iteritems(params_dict):
            old_attr_factor = self.ev_g_attr_get(attr, 0.0)
            now_attr_factor = old_attr_factor - mod_factor
            if now_attr_factor < 0:
                now_attr_factor = 0
            self.send_event('S_ATTR_SET', attr, now_attr_factor)
            state_name, parameter_name = self._parse_logic_state_param(attr)
            if state_name:
                if state_name not in state_parameters:
                    state_parameters[state_name] = dict()
                state_parameters[state_name][parameter_name] = now_attr_factor

        for state_name, parameters in six.iteritems(state_parameters):
            self.send_event('E_LOGIC_STATE_PARAM_CHANGED_' + state_name, parameters)

    def handle_shoot_accuracy(self, data, *args):
        val = data.get('val', 0)
        if not val:
            return
        if 'weapon_id' not in data:
            weapon_pos = data.get('wp', g_const.PART_WEAPON_POS_MAIN1)
            main_weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            weapon_list = (main_weapon.get_item_id(),)
        else:
            weapon_list = data['weapon_id']
            if isinstance(weapon_list, int):
                weapon_list = (
                 weapon_list,)
        for weapon_id in weapon_list:
            self.send_event('E_MOD_ADD_ATTR', attr_const.ATTR_SPREAD_FACTOR, -val, weapon_id)

    def del_shoot_accuracy(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        val = data.get('val', 0)
        if not val:
            return
        if 'weapon_id' not in data:
            weapon_pos = data.get('wp', g_const.PART_WEAPON_POS_MAIN1)
            main_weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            weapon_list = (main_weapon.get_item_id(),)
        else:
            weapon_list = data['weapon_id']
            if isinstance(weapon_list, int):
                weapon_list = (
                 weapon_list,)
        for weapon_id in weapon_list:
            self.send_event('E_MOD_ADD_ATTR', attr_const.ATTR_SPREAD_FACTOR, val, weapon_id)

    dash_module_effect = {'effect/fx/robot/robot_01/robot01_jiasu.sfx': [
                                                    'fx_root']
       }

    def handle_dash_module_effect(self, *args):

        def create_cb(*args):
            self.send_event('E_CREATE_MODEL_EFFECT', **self.dash_module_effect)
            self.unregist_event('E_ANIMATOR_LOADED', create_cb)

        model = self.ev_g_model()
        if model and model.valid:
            create_cb()
        else:
            self.regist_event('E_ANIMATOR_LOADED', create_cb)

    def del_dash_module_effect(self, *args):
        self.send_event('E_REMOVE_MODEL_EFFECT', **self.dash_module_effect)

    def handle_mod_boom_range(self, data, *args):
        val = data.get('dist_factor', 0)
        if val:
            self.send_event('E_MOD_RADIUS_FACTOR', val)

    def del_mod_boom_range(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        val = buff_info.get('dist_factor', 0)
        if val:
            self.send_event('E_MOD_RADIUS_FACTOR', -val)

    def handle_continue_fire_max_num(self, data, *args):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(g_const.PART_WEAPON_POS_MAIN1)
        if weapon:
            effective_conf = weapon.get_effective_config()
            maxSequence = weapon.get_data_by_key('iMaxSequence')
            effective_conf['iMaxSequence'] = maxSequence + data['max_cnt']
            self.send_event('E_CHANGE_NEED_SYNC_CONTINUE_FIRE_CNT', True)

    def del_continue_fire_max_num(self, buff_key, buff_id, buff_idx):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(g_const.PART_WEAPON_POS_MAIN1)
        if weapon:
            buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
            val = buff_info.get('max_cnt', 0)
            effective_conf = weapon.get_effective_config()
            maxSequence = weapon.get_data_by_key('iMaxSequence')
            effective_conf['iMaxSequence'] = maxSequence - val
            self.send_event('E_CHANGE_NEED_SYNC_CONTINUE_FIRE_CNT', False)

    def handle_ball_state(self, data, left_time, *args):
        if left_time is None:
            left_time = 0
        self.ball_state_left_time = left_time
        self.ball_state_duration = data['Duration']
        self.ball_normal_duration = data['normal_state_duration']
        normal_left_time = left_time - (self.ball_state_duration - self.ball_normal_duration)
        self.send_event('E_TRANS_TO_BALL', self.ball_state_duration - self.ball_state_left_time < 1, normal_left_time, self.ball_normal_duration)
        self.send_event('E_DISABLE_MECHA_JUMP_OPACITY')
        if not self.ev_g_is_avatar():
            self.send_event('E_FORBID_ROTATION', True)
        return

    def del_ball_state(self, buff_key, buff_id, buff_idx):
        if hasattr(global_data, 'no_cd') and global_data.no_cd:
            return
        self.send_event('E_TRANS_TO_HUMAN')
        self.send_event('E_RESET_MECHA_JUMP_OPACITY')
        if not self.ev_g_is_avatar():
            self.send_event('E_FORBID_ROTATION', False)

    def _get_ball_state(self):
        return (
         self.ball_state_left_time, self.ball_state_duration, self.ball_normal_duration)

    def handle_mecha_ball_overload_state(self, data, left_time, *args):
        if hasattr(global_data, 'no_cd') and global_data.no_cd:
            return
        self.over_load = True
        self.ball_overload_left_time = left_time
        self.ball_overload_duration = data['Duration']
        self.send_event('E_BALL_OVERLOAD_START', left_time, data['Duration'])

    def del_mecha_ball_overload_state(self, buff_key, buff_id, buff_idx):
        self.over_load = False
        self.send_event('E_BALL_OVERLOAD_STOP')

    def _get_ball_overload_state(self):
        return (
         self.ball_overload_left_time, self.ball_overload_duration)

    def _get_overload(self):
        return self.over_load

    def handle_fire_debuff(self, data, left_time, *args):
        self._fire_debuff = True
        self.send_event('E_FIRE_EFFECT', True, data.get('big_fire', False))

    def del_fire_debuff(self, buff_key, buff_id, buff_idx):
        self._fire_debuff = False
        self.send_event('E_FIRE_EFFECT', False)

    def _get_fire_debuff(self):
        return self._fire_debuff

    def handle_oil_debuff(self, data, left_time, *args):
        self._oil_debuff = True
        self.send_event('E_OIL_EFFECT', True)

    def del_oil_debuff(self, buff_key, buff_id, buff_idx):
        self._oil_debuff = False
        self.send_event('E_OIL_EFFECT', False)

    def _get_oil_debuff(self):
        return self._oil_debuff

    def handle_dizziness(self, data, left_time, *args):
        self._dizziness_debuff = True
        self.send_event('E_ACTIVE_DIZZINESS', True)

    def del_dizziness(self, buff_key, buff_id, buff_idx):
        self._dizziness_debuff = False
        self.send_event('E_ACTIVE_DIZZINESS', False)

    def handle_emp_effect(self, data, left_time, *args):
        self._emp_debuff = True
        self.send_event('E_ACTIVE_EMP', True)

    def del_emp_effect(self, buff_key, buff_id, buff_idx):
        self._emp_debuff = False
        self.send_event('E_ACTIVE_EMP', False)

    def _get_dizziness_debuff(self):
        return self._dizziness_debuff

    def _get_emp_debuff(self):
        return self._emp_debuff

    wild_effect = {'effect/fx/monster/yemu_monster/ym_baofa.sfx': ['fx_baofa']}

    def handle_monster_wild(self, data, left_time, *args):
        self.send_event('E_SET_SPEED_SCALE', data['speed_up'])
        self.send_event('E_MONSTER_WILD_ATTACK_BEGIN', data['animation'])
        self.send_event('E_ACTIVE_STATE', mecha_status_config.MC_SWORD_CORE)
        self.send_event('E_CREATE_MODEL_EFFECT', **self.wild_effect)

    def del_monster_wild(self, buff_key, buff_id, buff_idx):
        self.send_event('E_SET_SPEED_SCALE', 1)
        self.send_event('E_MONSTER_WILD_ATTACK_END')
        self.send_event('E_REMOVE_MODEL_EFFECT', **self.wild_effect)

    def get_xray_range_info(self):
        info = {'radius': self._xray_range_radius,'total_time': self._xray_range_total_time,'start_time': self._xray_range_start_time}
        return info

    def handle_add_range_see_throught(self, data, left_time, *args):
        import time
        control_target = global_data.cam_lctarget
        if control_target.MASK & preregistered_tags.HUMAN_TAG_VALUE:
            driver_id = control_target.id
            cur_entity_id = control_target.ev_g_get_bind_mecha()
        else:
            driver_id = control_target.sd.ref_driver_id
            cur_entity_id = control_target.id
        total_time = 8
        range_radius = data.get('range_radius')
        self._xray_range_radius = range_radius
        self._xray_range_total_time = total_time
        self._xray_range_start_time = time.time() - (total_time - left_time)
        self.send_event('E_RANGE_SEE_THROUGHT_START', left_time, total_time)
        types = [
         'Puppet', 'PuppetRobot', 'Mecha', 'MechaRobot', 'MechaTrans']
        all_entity = {}
        for t in types:
            all_entity.update(EntityManager.get_entities_by_type(t))

        for eid, ent in six.iteritems(all_entity):
            if ent and ent.logic and eid != cur_entity_id and eid != driver_id:
                ent.logic.send_event('E_ADD_RANGE_OUTLINE', range_radius)

    def del_add_range_see_throught(self, buff_key, buff_id, buff_idx):
        driver_id = global_data.cam_lctarget.sd.ref_driver_id
        cur_entity_id = global_data.cam_lctarget.id
        self._xray_range_radius = 0
        self.send_event('E_RANGE_SEE_THROUGHT_STOP')
        types = [
         'Puppet', 'PuppetRobot', 'Mecha', 'MechaRobot', 'MechaTrans']
        all_entity = {}
        for t in types:
            all_entity.update(EntityManager.get_entities_by_type(t))

        for eid, ent in six.iteritems(all_entity):
            if ent and ent.logic and eid != cur_entity_id and eid != driver_id:
                ent.logic.send_event('E_DEL_RANGE_OUTLINE')

    def handle_shoulder_grenade(self, data, left_time, *args):
        self.send_event('E_ENABLE_SHOULDER_GRENADE', True)

    def del_shoulder_grenade(self, data, left_time, *args):
        self.send_event('E_ENABLE_SHOULDER_GRENADE', False)

    def handle_breakthrough_8001_3(self, data, left_time, *args):
        self.send_event('E_ENABLE_BREAKTHROUGH_8001_3', True)

    def del_breakthrough_8001_3(self, data, left_time, *args):
        self.send_event('E_ENABLE_BREAKTHROUGH_8001_3', False)

    def handle_breakthrough_8001_4(self, data, left_time, *args):
        delta_time = data.get('delta_time', 0.5)
        self.send_event('E_ENABLE_BREAKTHROUGH_8001_4', True, delta_time)

    def del_breakthrough_8001_4(self, data, left_time, *args):
        self.send_event('E_ENABLE_BREAKTHROUGH_8001_4', False, 0)

    def handle_breakthrough_8004_all_dir_dash_dmg(self, data, left_time, *args):
        self.send_event('E_ENABLE_ALL_DIR_DASH_DMG', True)

    def del_breakthrough_8004_all_dir_dash_dmg(self, data, left_time, *args):
        self.send_event('E_ENABLE_ALL_DIR_DASH_DMG', False)

    def handle_mod_weapon_conf(self, data, *args):
        if data.get('only_avatar', 1) and not self.ev_g_is_avatar():
            return
        weapon_pos = data.get('wp_pos', 0)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon:
            return
        conf = weapon.get_config()
        effective_conf = weapon.get_effective_config()
        for param_name, ratio in six.iteritems(data.get('ratio_type', {})):
            effective_conf[param_name] = max(weapon.get_data_by_key(param_name) + conf[param_name] * ratio, 0.0001)

        for param_name, value in six.iteritems(data.get('value_type', {})):
            effective_conf[param_name] = max(weapon.get_data_by_key(param_name) + value, 0.0001)

    def del_mod_weapon_conf(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        if data.get('only_avatar', 1) and not self.ev_g_is_avatar():
            return
        weapon_pos = data.get('wp_pos', 0)
        weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon:
            return
        conf = weapon.get_config()
        effective_conf = weapon.get_effective_config()
        for param_name, ratio in six.iteritems(data.get('ratio_type', {})):
            effective_conf[param_name] = max(weapon.get_data_by_key(param_name) - conf[param_name] * ratio, 0.0001)

        for param_name, value in six.iteritems(data.get('value_type', {})):
            effective_conf[param_name] = max(weapon.get_data_by_key(param_name) - value, 0.0001)

    def handle_granbelm_mecha_shield(self, *args):
        pass

    def del_granbelm_mecha_shield(self, *args):
        self.send_event('E_ADD_BUFF_SFX', 471)

    def handle_second_weapon_aim(self, data, *args):
        val = data.get('val', 0)
        if val:
            self.send_event('E_SET_WEAPON_AIM_HELPER_SCALE', 1.0 + val, g_const.PART_WEAPON_POS_MAIN2)

    def handle_add_weapon_aim_dis(self, data, *args):
        val = data.get('val', 0)
        wp_pos = data.get('wp_pos', 2)
        if val:
            self.send_event('E_SET_WEAPON_AIM_HELPER_DISTANCE', 1.0 + val, wp_pos)

    def del_second_weapon_aim(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        val = buff_info['val']
        if val:
            self.send_event('E_SET_WEAPON_AIM_HELPER_SCALE', 1.0, g_const.PART_WEAPON_POS_MAIN2)

    def handle_shoot_move_speed(self, data, *args):
        val = data.get('val', 0)
        if val:
            self.send_event('E_SLOW_DOWN_SPEED_RATE', 'WeaponFire', val)

    def del_shoot_move_speed(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        val = buff_info['val']
        if val:
            self.send_event('E_SLOW_DOWN_SPEED_RATE', 'WeaponFire', -val)

    def handle_status_move_speed(self, data, *args):
        val = data.get('val', 0)
        status = data.get('status', None)
        if val and status:
            self.send_event('E_SLOW_DOWN_SPEED_RATE', status, val)
        return

    def del_status_move_speed(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        val = buff_info['val']
        status = buff_info['status']
        if val:
            self.send_event('E_SLOW_DOWN_SPEED_RATE', status, -val)

    def handle_transform_8011(self, data, left_time, *args):
        self.send_event('E_TRANS_TO_DRAGON', data, left_time)

    def del_transform_8011(self, buff_key, buff_id, buff_idx):
        self.send_event('E_TRANS_TO_DRAGON', None, 0)
        return

    def handle_rush_duration_time_scale(self, data, *args):
        val = data.get('val', 0)
        if val:
            self.send_event('E_SET_RUSH_DURATION_TIME_SCALE', val)

    def del_rush_duration_time_scale(self, buff_key, buff_id, buff_idx):
        buff_info = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        val = buff_info['val']
        if val:
            self.send_event('E_SET_RUSH_DURATION_TIME_SCALE', -val)

    def handle_update_suicide_state(self, data, *args):
        self.send_event('E_UPDATE_SUICIDE_SCREEN_SFX', True)

    def del_update_suicide_state(self, data, *args):
        self.send_event('E_UPDATE_SUICIDE_SCREEN_SFX', False)

    def handle_aim_candidate(self, data, left_time, *args):
        self.send_event('E_AUTO_AIM_BY_OTHERS', True, data['buff_id'], data['creator_id'])

    def del_aim_candidate(self, buff_key, buff_id, buff_idx):
        self.send_event('E_AUTO_AIM_BY_OTHERS', False, buff_id, None)
        return

    def handle_enable_aim_helper(self, data, left_time, *args):
        weapon_pos = data.get('weapon_pos', 0)
        if not weapon_pos:
            return
        if isinstance(weapon_pos, int):
            data['weapon_pos'] = weapon_pos = (
             weapon_pos,)
        aim_cond = {'buff_key': global_data.player.id,'buff_id': data.get('aim_buff_id', 0)}
        aim_target_id = data.get('aim_target')
        for pos in weapon_pos:
            self.send_event('E_SET_AIM_CONDITION', 'buff', aim_cond, pos)
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, pos)
            if aim_target_id:
                self.send_event('E_AIM_TARGET_BY_BUFF', aim_target_id, pos)

    def del_enable_aim_helper(self, buff_key, buff_id, buff_idx):
        data = self.ev_g_get_buff_info(buff_key, buff_id, buff_idx)
        weapon_pos = data.get('weapon_pos', ())
        if isinstance(weapon_pos, int):
            weapon_pos = (
             weapon_pos,)
        for pos in weapon_pos:
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, pos)

    def handle_translation_buff_state(self, data, *args):
        self.send_event('E_UPDATE_TRANSLATION_SCREEN_SFX', True)

    def del_translation_buff_state(self, data, *args):
        self.send_event('E_UPDATE_TRANSLATION_SCREEN_SFX', False)

    def handle_size_up_8026_shield(self, data, *args):
        size_up_factor = data.get('size_up_factor', 0)
        self.send_event('E_SIZE_UP_8026_SHIELD', size_up_factor)

    def del_size_up_8026_shield(self, buff_key, buff_id, buff_idx):
        pass

    def handle_8027_enable_multijump(self, *args):
        self.send_event('E_ENABLE_MULTIJUMP', True)

    def del_8027_enable_multijump(self, *args):
        self.send_event('E_ENABLE_MULTIJUMP', False)

    def handle_main_sec_weapon_use_together_8012(self, *args):
        from logic.gcommon.cdata.mecha_status_config import MC_SHOOT, MC_SECOND_WEAPON_ATTACK
        from logic.gcommon.const import PART_WEAPON_POS_MAIN2
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'sub', MC_SHOOT, {MC_SECOND_WEAPON_ATTACK})
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'sub', MC_SECOND_WEAPON_ATTACK, {MC_SHOOT})
        gun_status = self.ev_g_gun_status_inf(PART_WEAPON_POS_MAIN2)
        if gun_status:
            gun_status.set_socket_list(['fx_kaihuo02'])
        self.send_event('E_MODIFY_EFFECT_INFO', '5', '1', 0, {'socket_list': ['fx_kaihuo02']})

    def del_main_sec_weapon_use_together_8012(self, *args):
        from logic.gcommon.cdata.mecha_status_config import MC_SHOOT, MC_SECOND_WEAPON_ATTACK
        from logic.gcommon.const import PART_WEAPON_POS_MAIN2
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'add', MC_SHOOT, {MC_SECOND_WEAPON_ATTACK})
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'add', MC_SECOND_WEAPON_ATTACK, {MC_SHOOT})
        gun_status = self.ev_g_gun_status_inf(PART_WEAPON_POS_MAIN2)
        if gun_status:
            gun_status.set_socket_list(['fx_kaihuo01'])
        self.send_event('E_MODIFY_EFFECT_INFO', '5', '1', 0, {'socket_list': ['fx_kaihuo01']})

    def handle_8002_pve_init_state(self, *args):
        from logic.gcommon.cdata.mecha_status_config import MC_SWORD_ENERGY, MC_JUMP_1, MC_MOVE, MC_DASH, MC_CUT_RUSH
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'sub', MC_SWORD_ENERGY, {MC_MOVE, MC_JUMP_1})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'sub', MC_MOVE, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'sub', MC_JUMP_1, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'add', MC_DASH, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'sub', MC_DASH, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'add', MC_CUT_RUSH, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'sub', MC_CUT_RUSH, {MC_SWORD_ENERGY})

    def del_8002_pve_init_state(self, *args):
        from logic.gcommon.cdata.mecha_status_config import MC_SWORD_ENERGY, MC_JUMP_1, MC_MOVE, MC_DASH, MC_CUT_RUSH
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'add', MC_SWORD_ENERGY, {MC_MOVE, MC_JUMP_1})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'add', MC_MOVE, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'add', MC_JUMP_1, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'sub', MC_DASH, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'add', MC_DASH, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_cover', 'sub', MC_CUT_RUSH, {MC_SWORD_ENERGY})
        self.send_event('E_MOD_MP_ST', 'mp_st_forbid', 'add', MC_CUT_RUSH, {MC_SWORD_ENERGY})