# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHealthMecha.py
from ..share.ComHealth import ComHealth

class ComHealthMecha(ComHealth):
    BIND_EVENT = ComHealth.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SET_SLOW_CURE_HP': 'set_slow_cure_hp',
       'G_SLOW_CURE_HP': 'get_slow_cure_hp'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComHealthMecha, self).init_from_dict(unit_obj, bdict)

    def set_hp(self, hp):
        hp = min(max(0, hp), self._max_hp)
        if hp == self._hp:
            return
        mod = hp - self._hp
        self._hp = hp
        self.sd.ref_hp = hp
        self.send_event('E_HEALTH_HP_CHANGE', self._hp, mod)
        if self._hp <= 0:
            self.send_event('E_DEATH')
            global_data.emgr.mecha_crashed_event.emit(self.unit_obj.id)