# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComShield.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.time_utility as t_util
from logic.gcommon.ctypes.FightData import KEY_REAL_DAMAGE
from logic.gcommon.common_const import attr_const

class ComShield(UnitCom):
    BIND_EVENT = {'G_SUB_SHIELD': 'sub_shield',
       'E_ADD_SHIELD': 'add_shield',
       'G_SHIELD': 'get_shield',
       'G_MAX_SHIELD': 'get_max_shield',
       'G_SHIELD_PERCENT': 'get_shield_percent',
       'E_SET_SHIELD': 'set_shield',
       'E_FULL_SHIELD': 'full_shield',
       'E_HEALTH_HP_EMPTY': 'on_hp_empty',
       'E_ON_FIGHT': 'on_fight',
       'E_ENABLE_DAMAGE_2_SHIELD': 'enable_damage_2_shield',
       'E_SET_SHIELD_MAX': 'set_shield_max',
       'G_INI_MAX_SHIELD': '_get_init_max_shield',
       'G_FULL_SHIELD': 'is_shield_full',
       'E_BOND_GIFT_HP_TO_SHIELD_MOD_SHIELD': 'bond_gift_hp_to_shield_mod_shield',
       'E_SYNC_SHIELD': 'sync_shield',
       'E_ENABLE_SHIELD_TICK': 'enable_shield_tick',
       'E_RECOVER_PERCENT_SHIELD': 'recover_percent_shield',
       'E_RECOVER_LOSED_PERCENT_SHIELD': 'recover_losed_percent_shield',
       'G_IS_ENABLE_OVERFULL': 'is_enable_overfull',
       'E_ENABLE_SHIELD_OVERFULL': 'enable_shield_overfull'
       }
    BIND_ATTR_CHANGE = {attr_const.MECHA_ATTR_SHIELD_FACTOR: 'on_add_attr_changed',
       attr_const.MECHA_ATTR_SHIELD_ADD: 'on_add_attr_changed'
       }

    def __init__(self):
        super(ComShield, self).__init__(need_update=False)
        self._init_max_shiled = 0
        self._max_shield = 0
        self._shield_regtime = 0
        self._shield_reginterval = 0
        self._shield_regamount = 0
        self._shield = 0
        self._shield_hurt_time = 0
        self._shield_tick_dt = 0
        self._enable_dmg_2_shield = False
        self._enable_sub = True
        self._init_shield_regtime = 0
        self._init_shield_regamount = 0
        self._is_auto_reg = True
        self._enable_overfull = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComShield, self).init_from_dict(unit_obj, bdict)
        self._init_max_shiled = bdict.get('max_shield', 0)
        if G_IS_SERVER:
            self._init_max_shiled *= self.unit_obj.get_battle().get_common_hp_factor()
        self._max_shield = self._init_max_shiled
        if G_IS_SERVER:
            self.max_shiled = self.ev_g_addition_effect(self._init_max_shiled, factor_attrs=[attr_const.MECHA_ATTR_SHIELD_FACTOR], add_attrs=[attr_const.MECHA_ATTR_SHIELD_ADD])
        self._shield_regtime = bdict.get('shield_regtime', 0)
        self._init_shield_regtime = self._shield_regtime
        self._shield_reginterval = bdict.get('shield_reginterval', 0)
        self._shield_regamount = bdict.get('shield_regamount', 0)
        self._init_shield_regamount = self._shield_regamount
        if G_IS_SERVER:
            self._shield_regamount *= self.unit_obj.get_battle().get_common_hp_factor()
        self._shield = bdict.get('shield', self._max_shield)
        self._dmg_2_shield = bdict.get('damage_2_shield', None)
        if G_IS_SERVER:
            self._is_auto_reg = not self.unit_obj.get_battle().is_pve()
        self._enable_overfull = bdict.get('enable_overfull', False)
        return

    def enable_damage_2_shield(self, enable):
        self._enable_dmg_2_shield = enable

    def get_client_dict(self):
        return {'max_shield': self._max_shield,
           'shield': self._shield
           }

    def get_shield(self):
        return self._shield

    def is_shield_full(self):
        return self._shield == self._max_shield

    def get_max_shield(self):
        return self._max_shield

    def on_hp_empty(self):
        self.need_update = False
        self._shield = self._max_shield

    def get_shield_percent(self):
        return self._shield * 1.0 / self._max_shield

    def _get_init_max_shield(self):
        return self._init_max_shiled

    def tick(self, dt):
        now = t_util.get_time()
        if 0 < now - self._shield_hurt_time < self._shield_regtime:
            return
        self._shield_tick_dt += dt
        if self._shield_tick_dt < self._shield_reginterval:
            return
        self._shield_tick_dt -= self._shield_reginterval
        shield_regamount = self.ev_g_addition_effect(self._shield_regamount, factor_attrs=[attr_const.MECHA_ATTR_SHIELD_RECOVER_FACTOR])
        self.add_shield(shield_regamount)

    def full_shield(self):
        self.add_shield(self._max_shield - self._shield)

    def sub_shield(self, delta, change_by_buff=False):
        if not self._enable_sub:
            return (delta, 0)
        sub_value = 0
        if delta <= 0:
            return (delta, sub_value)
        if not change_by_buff:
            self._shield_hurt_time = t_util.get_time()
            self._shield_tick_dt = 0
        if delta > 0 and self._shield > 0:
            sub_value = min(self._shield, delta)
            delta = max(0, delta - sub_value)
            self.set_shield(self._shield - sub_value)
            if not change_by_buff and self._is_auto_reg:
                self.need_update = True
            self.sync_shield()
        return (
         delta, sub_value)

    def add_shield(self, delta, add_from_dmg=False):
        if delta <= 0:
            return
        shield = self._shield + delta
        if shield >= self._max_shield:
            shield = self._max_shield
            self.need_update = False
        if shield != self._shield:
            self.set_shield(shield)
            self.sync_shield(add_from_dmg)

    def set_shield(self, shield, add_from_dmg=False):
        if G_IS_CLIENT and shield < self._shield:
            self.send_event('E_ON_DEL_SHEILD')
        lst_shield = self._shield
        self._shield = max(0, min(self._max_shield, shield))

    def set_shield_max(self, shiled_max):
        self._max_shield = shiled_max

    def on_add_attr_changed(self, attr, item_id, pre_value, cur_value, source_info):
        if G_IS_SERVER and attr in [attr_const.MECHA_ATTR_SHIELD_FACTOR, attr_const.MECHA_ATTR_SHIELD_ADD]:
            max_shiled = self.ev_g_addition_effect(self._init_max_shiled, factor_attrs=[attr_const.MECHA_ATTR_SHIELD_FACTOR], add_attrs=[attr_const.MECHA_ATTR_SHIELD_ADD])
            self.set_shield_max(max_shiled)
            mod_cur_val = source_info.get('mod_cur_val', True) if isinstance(source_info, dict) else True
            if mod_cur_val:
                if attr == attr_const.MECHA_ATTR_SHIELD_FACTOR:
                    mod_factor = cur_value - pre_value
                    if mod_factor > 0:
                        self.add_shield(self._init_max_shiled * mod_factor)
                    else:
                        self.sub_shield(-self._init_max_shiled * mod_factor)
                elif attr == attr_const.MECHA_ATTR_SHIELD_ADD:
                    mod = cur_value - pre_value
                    if mod > 0:
                        self.add_shield(mod)
                    else:
                        self.sub_shield(-mod)
            elif self._is_auto_reg:
                self.need_update = True
            self.send_event('E_CALL_SYNC_METHOD', 'set_shield_max', (self._max_shield, self._shield, mod_cur_val), False, True, True)

    def sync_shield(self, add_from_dmg=False):
        self.send_event('E_CALL_SYNC_METHOD', 'set_shield', (self._shield, add_from_dmg), False, True, True)

    def enable_shield_tick(self, reset_time=False):
        if self._shield < self._max_shield:
            self.need_update = True
        if reset_time:
            self._shield_hurt_time = t_util.get_time()

    def bond_gift_hp_to_shield_mod_shield(self, change_val):
        if self._max_shield <= 0:
            log_error('ComShield bond_gift_hp_to_shield_mod_shield invalid max_shield=%s, change_val=%s', self._max_shield, change_val)
            return
        ratio = 1.0 * self._shield / self._max_shield
        self.set_shield_max(max(1, self._max_shield + change_val))
        self.set_shield(self._max_shield * ratio)
        self.send_event('E_CALL_SYNC_METHOD', 'set_shield_max', (self._max_shield, self._shield), False, True, True)

    def on_fight(self, ft_dat):
        if not self._enable_dmg_2_shield or self._dmg_2_shield is None:
            return
        else:
            damage = ft_dat.inj_data[KEY_REAL_DAMAGE]
            value = self._dmg_2_shield(damage)
            self.add_shield(value, True)
            return

    def recover_percent_shield(self, ratio, add_from_damage=False):
        delta = self._max_shield * ratio
        if delta > 0:
            self.add_shield(delta, add_from_damage)

    def recover_losed_percent_shield(self, ratio, add_from_damage=False):
        delta = (self._max_shield - self._shield) * ratio
        if delta > 0:
            self.add_shield(delta, add_from_damage)

    def is_enable_overfull(self):
        return self._enable_overfull

    def enable_shield_overfull(self, flag):
        self._enable_overfull = flag