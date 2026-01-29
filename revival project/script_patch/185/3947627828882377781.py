# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8026.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
POWER_UP_EFFECT = '99'
SHIELD_ON_EFFECT = '100'

class ComMechaEffect8026(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_WEAPON_POWERUP': 'on_weapon_power_up',
       'E_8026_SHIELD_CHANGE': 'on_shield_state_change'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8026, self).init_from_dict(unit_obj, bdict)
        self.shield_on = None
        return

    def on_weapon_power_up(self, percent):
        if POWER_UP_EFFECT not in self._dynamic_effect_conf:
            return
        power_up = percent >= 1.0
        self.on_trigger_state_effect('power_up', POWER_UP_EFFECT if power_up else '', socket_index=0, need_sync=True)

    def on_shield_state_change(self, flag):
        if flag != self.shield_on:
            self.shield_on = flag
            self.on_trigger_state_effect('shield_on', SHIELD_ON_EFFECT if flag else '', socket_index=0, need_sync=True)