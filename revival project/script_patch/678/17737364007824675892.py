# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComHealthHuman.py
from __future__ import absolute_import
from .ComHealth import ComHealth
import logic.gcommon.time_utility as t_util
from logic.gcommon.common_const import attr_const

class ComHealthHuman(ComHealth):
    BIND_EVENT = ComHealth.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HEALTH_HP_CHANGE': 'sync_hp',
       'E_HEALTH_HP_EMPTY': 'on_hp_empty',
       'E_ON_SAVED': ('on_saved', 99),
       'E_REVIVE': ('on_revive', 99),
       'E_MAX_HP_CHANGED': 'sync_max_hp',
       'E_POST_START_SPECTATE': '_on_post_start_spectate',
       'E_SLOW_CURE': 'do_slow_cure',
       'E_SET_SLOW_CURE_HP': 'set_slow_cure_hp',
       'G_SLOW_CURE_HP': 'get_slow_cure_hp',
       'E_ENABLE_HEAL': '_enable_heal',
       'E_DISABLE_HEAL': '_disable_heal'
       })

    def __init__(self):
        super(ComHealthHuman, self).__init__()
        self._hurt_time = 0
        self._heal_dt = 0
        self._heal_time = 0
        self._heal_interval = 0
        self._heal_hp = 0
        self._heal_valid = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComHealthHuman, self).init_from_dict(unit_obj, bdict)
        self._heal_valid = bdict.get('heal_valid', False)
        if self._heal_valid:
            self._heal_hp = bdict.get('heal_hp', 0)
            self._heal_time = bdict.get('heal_time', 0)
            self._heal_interval = bdict.get('heal_interval', 0)

    def on_init_complete(self):
        self._heal_hp = self.ev_g_addition_effect(self._heal_hp, factor_attrs=[attr_const.HUMAN_ATTR_HEAL_HP_FACTOR])
        self._heal_time = self.ev_g_addition_effect(self._heal_time, factor_attrs=[attr_const.HUMAN_ATTR_HEAL_TIME_FACTOR])

    def sync_hp(self, hp, mod):
        self.send_event('E_CALL_SYNC_METHOD', 'on_hp_change', (hp,), False, True, True)

    def empty_hp(self):
        super(ComHealthHuman, self).empty_hp()
        self.send_event('T_DEFEATED')

    def add_hp(self, delta, i_limit=0, i_type=0):
        super(ComHealthHuman, self).add_hp(delta, i_limit, i_type)
        if self._hp <= 0 or self._hp >= self._max_hp:
            self.send_event('E_DISABLE_HEAL')

    def sub_hp(self, delta, i_type=0):
        ret = super(ComHealthHuman, self).sub_hp(delta, i_type)
        if delta > 0:
            self.send_event('E_ENABLE_HEAL')
        return ret

    def on_hp_empty(self):
        self.send_event('E_DISABLE_HEAL')

    def sync_max_hp(self, max_hp, hp, change_hp=True):
        if G_IS_SERVER:
            self.send_event('E_CALL_SYNC_METHOD', 'set_max_hp', (max_hp, hp), False, True)

    def _enable_heal(self):
        if self._heal_valid and self._hp < self._max_hp and self.unit_obj.is_alive():
            self._hurt_time = t_util.get_time()
            self.need_update = True

    def _disable_heal(self):
        if self._heal_valid:
            if self._hp <= 0 or self._hp >= self._max_hp:
                self.need_update = False

    def tick(self, dt):
        now = t_util.get_time()
        if now - self._hurt_time >= self._heal_time:
            self._heal_dt += dt
            if self._heal_dt >= self._heal_interval:
                self._heal_dt -= self._heal_interval
                self.add_hp(self._heal_hp)

    def on_saved(self):
        if self._hp > 0:
            return
        self.set_hp(30)
        self.send_event('E_ENABLE_HEAL')

    def on_revive(self, *args):
        self.set_hp(self._max_hp)
        self.send_event('E_ENABLE_HEAL')

    def _on_post_start_spectate(self, from_id):
        self.send_event('E_CALL_SYNC_SPECIFIC', 'on_hp_change', (self._hp,), False, (from_id,))