# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComHealth.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.time_utility as t_util
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import attr_const

class ComHealth(UnitCom):
    BIND_EVENT = {'G_HP': 'get_hp',
       'G_MAX_HP': 'get_max_hp',
       'G_FULL_HP': 'is_full_hp',
       'G_HEALTH_GET_INIT_MAX_HP': 'get_init_max_hp',
       'S_HP': 'set_hp',
       'G_HEALTH_PERCENT': 'get_hp_percent',
       'E_FULLHP': 'full_hp',
       'E_SECKILL': 'empty_hp',
       'G_DAMAGE': 'sub_hp',
       'E_CURE': 'do_cure',
       'E_SET_MAX_HP': 'set_max_hp',
       'E_RECOVER_LOSE_HP': 'recover_lose_hp',
       'E_RECOVER_HP_BY_PERCENTAGE': 'recover_hp_by_percentage',
       'E_PRE_HP_CHANGE_CHECK_SWITCH': 'pre_hp_change_check_handler'
       }
    BIND_ATTR_CHANGE = {attr_const.ATTR_MAX_HP_ADD: 'on_add_attr_changed',
       attr_const.ATTR_MAX_HP_FACTOR: 'on_add_attr_changed'
       }

    def __init__(self):
        super(ComHealth, self).__init__(need_update=False)
        self._max_hp = 0
        self._hp = 0
        self.sd.ref_max_hp = 0
        self.sd.ref_hp = 0
        self._slow_cure_hp_sum = 0
        self._slow_cure_hp = {}
        self._max_hp_factor = 0
        self.pre_hp_change_check = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComHealth, self).init_from_dict(unit_obj, bdict)
        self._max_hp = int(bdict.get('max_hp', 100))
        self._hp = int(bdict.get('hp', self._max_hp))
        self.sd.ref_max_hp = self._max_hp
        self.sd.ref_hp = self._hp
        self._init_max_hp = int(bdict.get('init_max_hp', self._max_hp))
        self._slow_cure_hp_sum = int(bdict.get('cure_hp', self._slow_cure_hp_sum))
        unit_obj.send_event('E_HEALTH_HP_INIT', self._hp, self._max_hp)
        self.send_event('E_HEALTH_INIT')

    def on_post_init_complete(self, bdict):
        if G_IS_SERVER:
            max_hp = self._max_hp * self.unit_obj.get_battle().get_common_hp_factor()
            self.set_max_hp(max_hp)
            self._init_max_hp = self._max_hp

    def on_add_attr_changed(self, attr, item_id, pre_value, cur_value, source_info):
        if G_IS_SERVER:
            max_hp = self._init_max_hp * (1 + self.ev_g_add_attr(attr_const.ATTR_MAX_HP_FACTOR))
            max_hp += self.ev_g_add_attr(attr_const.ATTR_MAX_HP_ADD) * self.unit_obj.get_battle().get_common_hp_factor()
            mod_val = int(max_hp - self._max_hp)
            mod_cur_val = source_info.get('mod_cur_val', None) if isinstance(source_info, dict) else None
            if mod_cur_val is not None:
                if mod_val > 0:
                    self.add_max_hp(mod_val, addhp=mod_cur_val)
                else:
                    self.sub_max_hp(-mod_val, subhp=mod_cur_val)
            elif mod_val > 0:
                self.add_max_hp(mod_val)
            else:
                self.sub_max_hp(-mod_val, subhp=True)
        return

    def destroy(self):
        super(ComHealth, self).destroy()

    def get_client_dict(self):
        cdict = {}
        cdict['max_hp'] = self._max_hp
        cdict['hp'] = self._hp
        cdict['init_max_hp'] = self._init_max_hp
        if self._slow_cure_hp_sum > 0:
            cdict['cure_hp'] = self._slow_cure_hp_sum
        return cdict

    def is_full_hp(self):
        return self._hp >= self._max_hp

    def get_hp(self):
        return self._hp

    def get_max_hp(self):
        return self._max_hp

    def get_init_max_hp(self):
        return self._init_max_hp

    def set_max_hp(self, val, change_hp=None):
        delta = val - self._max_hp
        if change_hp is not None:
            if delta > 0:
                self.add_max_hp(delta, change_hp)
            elif delta < 0:
                self.sub_max_hp(-delta, change_hp)
        elif delta > 0:
            self.add_max_hp(delta)
        elif delta < 0:
            self.sub_max_hp(-delta)
        return

    def add_max_hp(self, val, addhp=True, event_notify=True):
        self._max_hp += val
        self.sd.ref_max_hp = self._max_hp
        if event_notify:
            self.send_event('E_MAX_HP_CHANGED', self._max_hp, self._hp, addhp)
        if addhp:
            self.add_hp(val)

    def sub_max_hp(self, val, subhp=False, event_notify=True):
        if val >= self._max_hp:
            return
        self._max_hp -= val
        self.sd.ref_max_hp = self._max_hp
        if event_notify:
            self.send_event('E_MAX_HP_CHANGED', self._max_hp, self._hp, subhp)
        if self._hp > self._max_hp:
            self.sub_hp(self._hp - self._max_hp)

    def _mod_max_hp_factor(self, val, change_hp=False, source_info=None):
        self._max_hp_factor += val
        if self._max_hp_factor <= -1:
            log_error('_mod_max_hp_factor error! val = %s, _max_hp_factor = %s, _max_hp = %s', val, self._max_hp_factor, self._max_hp)
        mod_val = int(self._init_max_hp * (1 + self._max_hp_factor) - self._max_hp)
        if mod_val > 0:
            self.add_max_hp(mod_val, change_hp)
        else:
            self.sub_max_hp(-mod_val, change_hp)

    def recover_lose_hp(self, percent):
        lose_hp = self._max_hp - self._hp
        delta = lose_hp * percent / 100.0
        self.do_cure(delta, i_type=battle_const.CURE_TYPE_REAL_VALUE)

    def recover_hp_by_percentage(self, percent):
        delta = self._max_hp * percent
        self.do_cure(delta, i_type=battle_const.CURE_TYPE_REAL_VALUE)

    def do_cure(self, delta, i_limit=0, i_type=battle_const.CURE_TYPE_NORMAL):
        pre_hp = self._hp
        if i_type not in battle_const.NO_COMMON_FACTOR_CURE_LIST:
            delta *= self.unit_obj.get_battle().get_common_hp_factor()
        mecha_driver = self.unit_obj.get_battle().get_entity(self.ev_g_driver())
        add_factor = self.ev_g_add_attr(attr_const.ATTR_CURE_FACTOR)
        if mecha_driver and mecha_driver.logic and i_type != battle_const.CURE_TYPE_ATTACK:
            add_factor += mecha_driver.logic.ev_g_add_attr(attr_const.MECHA_ATTR_CURE_ITEM_ADD_FACTOR, 0)
        delta *= 1 + add_factor
        self.add_hp(delta, i_limit, i_type)
        cure_hp = self._hp - pre_hp
        self.send_event('E_ON_CURE', cure_hp, i_type, delta - cure_hp)

    def do_slow_cure(self, delta, source_type, buff_id, cover=False):
        delta *= self.unit_obj.get_battle().get_common_hp_factor()
        mecha_driver = self.unit_obj.get_battle().get_entity(self.ev_g_driver())
        add_factor = self.ev_g_add_attr(attr_const.ATTR_CURE_FACTOR)
        if mecha_driver and mecha_driver.logic:
            add_factor += mecha_driver.logic.ev_g_add_attr(attr_const.MECHA_ATTR_CURE_ITEM_ADD_FACTOR, 0)
        delta *= 1 + add_factor
        self._slow_cure_hp_sum += delta
        if self._slow_cure_hp_sum < -0.01:
            self.logger.error('[ComHealth] _slow_cure_hp: %f', self._slow_cure_hp_sum)
            return
        if source_type not in self._slow_cure_hp:
            self._slow_cure_hp[source_type] = {}
        if buff_id not in self._slow_cure_hp[source_type]:
            self._slow_cure_hp[source_type][buff_id] = 0
        if cover and delta >= 0:
            self._slow_cure_hp_sum -= self._slow_cure_hp[source_type][buff_id]
            self._slow_cure_hp[source_type][buff_id] = delta
        else:
            self._slow_cure_hp[source_type][buff_id] += delta
        self.send_event('E_CALL_SYNC_METHOD', 'on_slow_cure_hp_change', (self._slow_cure_hp_sum,), False, True, False)

    def set_slow_cure_hp(self, cure_hp):
        cure_hp = max(0, cure_hp)
        if cure_hp == self._slow_cure_hp_sum:
            return
        mod = cure_hp - self._slow_cure_hp_sum
        self._slow_cure_hp_sum = cure_hp
        self.send_event('E_SLOW_CURE_HP_CHANGE', self._slow_cure_hp_sum, mod)

    def get_slow_cure_hp(self):
        return self._slow_cure_hp

    def add_hp(self, delta, i_limit=0, i_type=0):
        if delta <= 0:
            return
        if i_limit:
            if i_limit <= self._hp:
                return
            if i_limit < self._hp + delta:
                delta = i_limit - self._hp
        self.mod_hp(delta)

    def sub_hp(self, delta, i_type=0):
        if delta <= 0:
            return 0
        _pre = self._hp
        if G_IS_SERVER:
            if delta >= _pre:
                effect_data = {'damage': delta}
                self.send_event('E_EFFECT_EVENT', 'EVENT_FATAL_DMG', effect_data)
            if self.ev_g_invincible():
                return
        self.mod_hp(-delta)
        return _pre - self._hp

    def empty_hp(self):
        self.set_hp(0)

    def mod_hp(self, mod):
        self.set_hp(self._hp + mod)

    def full_hp(self):
        self.set_hp(self._max_hp)

    def set_hp(self, hp, force_set=False):
        hp = min(max(0, hp), self._max_hp)
        if hp == self._hp and not force_set:
            return
        mod = hp - self._hp
        self._hp = hp
        self.sd.ref_hp = hp
        if self.pre_hp_change_check:
            pre_check_hp = self._hp
            self.send_event('E_PRE_HEALTH_HP_CHANGE', hp)
            mod = self._hp - pre_check_hp
            self.sd.ref_hp = self._hp
        self.send_event('E_HEALTH_HP_CHANGE', self._hp, mod)
        if self._hp <= 0:
            self.send_event('E_HEALTH_HP_EMPTY')

    def get_hp_percent(self):
        return self._hp * 1.0 / self._max_hp

    def pre_hp_change_check_handler(self, do_check):
        if do_check:
            self.pre_hp_change_check = True
        else:
            self.pre_hp_change_check = False