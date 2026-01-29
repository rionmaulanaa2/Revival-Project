# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillBase.py
from __future__ import absolute_import
import six
import cython
from .ISkillBase import ISkillBase
from logic.gcommon import time_utility as tutil
import copy
from logic.gcommon.common_const.skill_const import MP_COST_PER_TIMES, MP_COST_PER_SECOND, FUEL_COST_PER_TIMES_INAIR
from logic.gcommon.common_const.skill_const import MP_SYNC_STAGE_BEGIN_DO_SKILL, MP_SYNC_STAGE_END_DO_SKILL, MP_SYNC_STAGE_BEGIN_RECOVER
from logic.gcommon.common_const.skill_const import ATTR_DMG_FACTOR, ATTR_BUFF_EXTRA_DURATION
from common.cfg import confmgr
from logic.gcommon.common_const import water_const
from logic.gcommon.common_const import attr_const

class SkillBase(ISkillBase):

    def __init__(self, skill_id, unit_obj, data):
        self.__mp = [
         0]
        self._skill_id = skill_id
        self._data = copy.deepcopy(data)
        self._skill_hit = data.get('hit', 0)
        self._unit_obj = unit_obj
        self._last_hit = 0
        self._left_count = 0
        self._max_mp = data.get('max_mp', 0)
        self._mp = data.get('mp', self._max_mp)
        self._cost_mp = data.get('cost_mp', 0)
        self._cost_mp_pre = data.get('cost_mp_pre', 0)
        self._inc_mp = data.get('inc_mp', 0)
        self._init_inc_mp = data.get('init_inc_mp', self._inc_mp)
        self._category = data.get('category', 6)
        self._cost_mp_type = data.get('cost_mp_type', 1)
        self._auto_recover = data.get('auto_recover', False)
        self._is_reconnect_skill = data.get('is_reconnect_skill', False)
        self._mp_stage = 0
        self._cost_fuel = data.get('cost_fuel', 0)
        self._cost_fuel_pre = data.get('cost_fuel_pre', 0)
        self._cost_fuel_type = data.get('cost_fuel_type', MP_COST_PER_TIMES)
        self._tell_ui_at_once = True
        self._cd_type = data.get('cd_type', None)
        self._tick_interval = 0.1 if data.get('cd_type', 0) == 0 else 0.06
        self._delta = 0
        self._max_fuel = data.get('max_fuel', 0)
        self.need_tick = self._mp < self._max_mp
        self._last_cast_time = data.get('last_cast_time', 0)
        self._mp_attr = {ATTR_DMG_FACTOR: 1,
           ATTR_BUFF_EXTRA_DURATION: 0
           }
        self._module_card_id = data.get('module_card_id', 0)
        self._disabled_by_module_card = False
        self.is_move_skill = data.get('is_move_skill', -1)
        return

    def destroy(self):
        self._data = None
        self._unit_obj = None
        return

    @property
    def _mp(self):
        return self.__mp[0]

    @_mp.setter
    def _mp(self, v):
        self.__mp[0] = None
        self.__mp = [v]
        return

    def on_add_attr_changed(self, attr, pre_value, cur_value):
        if not self._max_mp:
            return
        old_inc_mp = self._inc_mp
        recover_factor_name = 'skill_{}_recover_factor'.format(self._category)
        recover_factor_specific = self._unit_obj.ev_g_add_attr(recover_factor_name)
        recover_factor_common = self._unit_obj.ev_g_add_attr(attr_const.ATTR_SKILL_RECOVER_FACTOR, self._skill_id)
        temp_recover_factor = 0
        if self._mp_stage == MP_SYNC_STAGE_BEGIN_RECOVER:
            temp_recover_factor_name = 'tmp_skill_{}_recover_factor'.format(self._category)
            temp_recover_factor = self._unit_obj.ev_g_add_attr(temp_recover_factor_name)
        total_factor = recover_factor_specific + recover_factor_common + temp_recover_factor
        skill_cd_add = self._unit_obj.ev_g_add_attr(attr_const.ATTR_SKILL_CD_ADD, self._skill_id)
        cd_factor = 1 + total_factor + self._init_inc_mp * skill_cd_add * 1.0 / self._max_mp
        if cd_factor < 0.3:
            if not (global_data.battle and global_data.battle._is_customed_battle):
                log_error('[Skill %s-%s-%s]skill cd factor is invalid, recover_factor_specific=%s, recover_factor_common=%s, skill_cd_add=%s', self._unit_obj.__class__.__name__, self._unit_obj.id, self._skill_id, recover_factor_specific, recover_factor_common, skill_cd_add)
                cd_factor = 0.3
            elif cd_factor <= 0.16:
                cd_factor = 0.16
        self._inc_mp = self._init_inc_mp / cd_factor
        if self._inc_mp != old_inc_mp:
            self._unit_obj.send_event('E_UPDATE_SKILL_ATTR', self._skill_id)

    def update_skill(self, data, trigger_update_event=True):
        if not data:
            return
        for key, value in six.iteritems(data):
            attr_key = '_%s' % key
            if hasattr(self, attr_key):
                setattr(self, attr_key, value)
            elif 'ext_info' in self._data and key in self._data['ext_info']:
                self._data['ext_info'][key] = value

        if trigger_update_event:
            self._unit_obj.send_event('E_UPDATE_SKILL_ATTR', self._skill_id)
        self.need_tick = self._mp < self._max_mp

    def mod_skill(self, data, trigger_update_event=True):
        if not data:
            return
        for key, value in six.iteritems(data):
            attr_key = '_%s' % key
            if hasattr(self, attr_key):
                setattr(self, attr_key, getattr(self, attr_key) + value)
            elif 'ext_info' in self._data and key in self._data['ext_info']:
                self._data['ext_info'][key] += value

        if trigger_update_event:
            self._unit_obj.send_event('E_UPDATE_SKILL_ATTR', self._skill_id)
        self.need_tick = self._mp < self._max_mp

    def get_skill_data(self, keys):
        if not keys:
            return
        else:
            skill_data_copy = {}
            for key in keys:
                attr_key = '_%s' % key
                if hasattr(self, attr_key):
                    skill_data_copy[key] = getattr(self, attr_key, None)
                elif 'ext_info' in self._data and key in self._data['ext_info']:
                    skill_data_copy[key] = self._data['ext_info'][key]

            return skill_data_copy

    def on_add(self):
        if self._mp < self._max_mp:
            self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
        else:
            self._mp_stage = 0

    def on_remove(self):
        pass

    def check_cost_energy(self):
        return True

    def on_check_cast_skill(self):
        if not self.can_do_skill_in_water():
            return False
        if self.is_move_skill and self._unit_obj.ev_g_is_move_skill_disabled():
            return False
        if self._cost_mp_type == MP_COST_PER_SECOND:
            if self._mp < self._cost_mp_pre:
                return False
        elif self._mp < self._cost_mp + self._cost_mp_pre:
            return False
        cost_fuel_in_air = self._cost_fuel_type == FUEL_COST_PER_TIMES_INAIR and not self._unit_obj.ev_g_on_ground()
        should_cost = self._cost_fuel_type != FUEL_COST_PER_TIMES_INAIR or cost_fuel_in_air
        cost_fuel = max(0, self.get_cost_fuel() * (1 - self._unit_obj.ev_g_add_attr('skill_{}_fuel_cost_factor'.format(self._category)) - self._unit_obj.ev_g_add_attr('skill_fuel_cost_factor', self._skill_id)))
        cost_fuel_pre = max(0, self.get_cost_fuel_pre() * (1 - self._unit_obj.ev_g_add_attr('skill_{}_fuel_cost_factor'.format(self._category)) - self._unit_obj.ev_g_add_attr('skill_fuel_cost_factor', self._skill_id)))
        if should_cost and cost_fuel > 0:
            need_fuel = cost_fuel + cost_fuel_pre if self._cost_fuel_type == 1 else cost_fuel_pre
            if self.has_spec_fuel():
                now_fuel = self._unit_obj.ev_g_skill_fuel(self._skill_id)
            else:
                now_fuel = self._unit_obj.ev_g_fuel()
            if not now_fuel or now_fuel < need_fuel:
                global_data.emgr.mecha_skill_lack_fuel_event.emit()
                return False
        return True

    def check_skill(self):
        if hasattr(global_data, 'no_cd') and global_data.no_cd:
            return True
        if self._cost_mp == 0:
            return True
        if self._cost_mp_type == MP_COST_PER_SECOND:
            if self._mp > self._cost_mp_pre:
                self._mp_stage = MP_SYNC_STAGE_BEGIN_DO_SKILL
                self._mp -= self._cost_mp_pre
                if self._tell_ui_at_once:
                    self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)
                self.need_tick = True
                return True
        else:
            if self._cost_mp_type == MP_COST_PER_TIMES:
                if self._cost_mp + self._cost_mp_pre > 0 and self._mp < self._cost_mp + self._cost_mp_pre:
                    return False
                self._mp -= self._cost_mp + self._cost_mp_pre
                self.need_tick = True
                if self._auto_recover:
                    self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
                else:
                    self._mp_stage = MP_SYNC_STAGE_BEGIN_DO_SKILL
                if self._tell_ui_at_once:
                    self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)
                return True
            return False

    def set_mp(self, mp):
        self._mp = min(mp, self._max_mp)

    def get_mp(self):
        return self._mp

    def get_max_mp(self):
        return self._max_mp

    def do_skill(self, *args):
        pass

    def remote_do_skill(self, *args):
        pass

    def end_skill(self, *args):
        if self._auto_recover:
            self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
        else:
            self._mp_stage = MP_SYNC_STAGE_END_DO_SKILL

    def begin_recover_mp(self, *args):
        if self._mp < self._max_mp:
            self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
            self.need_tick = True

    def on_temp_remove(self):
        pass

    def on_recover(self):
        pass

    def on_interrupt(self):
        pass

    def cal_dmg(self, entity, info):
        return 0

    def mod_attr(self, key, mod):
        if key not in self._mp_attr:
            return
        self._mp_attr[key] += mod

    def get_attr_by_key(self, key, default=None):
        return self._mp_attr.get(key, default)

    def hit_on_target(self):
        pass

    def set_tick_interval(self, interval):
        self._tick_interval = interval

    def tick(self, delta):
        self._delta += delta
        if self._delta < self._tick_interval:
            return
        delta = self._delta
        self._delta = 0
        if self._mp_stage == MP_SYNC_STAGE_BEGIN_DO_SKILL:
            if self._cost_mp_type == MP_COST_PER_SECOND:
                if self._mp > 0:
                    self._mp -= delta * self._cost_mp
                    if self._mp < 0:
                        self._mp = 0
                    self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)
                else:
                    self._unit_obj.send_event('E_ENERGY_EXHAUSTED', self._skill_id)
                    if self._auto_recover:
                        self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
                    else:
                        self._mp_stage = 0
        elif self._mp_stage == MP_SYNC_STAGE_BEGIN_RECOVER:
            self._mp += delta * self._inc_mp
            if self._mp > self._max_mp:
                self._mp = self._max_mp
                self._mp_stage = 0
                self.need_tick = False
                self._unit_obj.send_event('E_ENERGY_FULL', self._skill_id)
            self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)

    def get_cost_fuel(self):
        return self._cost_fuel

    def get_cost_fuel_pre(self):
        return self._cost_fuel_pre

    def get_cost_fuel_type(self):
        return self._cost_fuel_type

    def can_do_skill_in_water(self, *args):
        cur_conf = confmgr.get('skill_conf', str(self._skill_id))
        if cur_conf.get('ignore_water', None) is None:
            if self._unit_obj.ev_g_is_water_depth_over(water_const.H_WATER_MECHA_DIVING) and self._unit_obj.ev_g_water_height() >= self._unit_obj.ev_g_position().y:
                return False
        return True

    def mod_left_cnt(self, delta_times):
        pass

    def set_left_cnt(self, cnt):
        pass

    def mod_mp(self, mod):
        self._mp += mod
        if self._mp > self._max_mp:
            self._mp = self._max_mp
        elif self._mp < 0:
            self._mp = 0

    def has_spec_fuel(self):
        return self._max_fuel > 0

    def reset_skill_cd(self):
        self.set_mp(self._max_mp)
        self.begin_recover_mp()

    def get_module_card_id(self):
        return self._module_card_id

    def disable_by_module_card(self, disable):
        self._disabled_by_module_card = disable

    def is_disabled_by_module_card(self):
        return self._module_card_id > 0 and self._disabled_by_module_card

    def useless_function(self):
        pass