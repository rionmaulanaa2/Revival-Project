# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHeatMagazine.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.gcommon.ctypes.HeatMagazineClient import HeatMagazine
from logic.gcommon.common_const.weapon_const import STATE_NONE, STATE_SHOOT, STATE_NORMAL_DEC, STATE_FORCE_DEC, BAN_SHOOT_STATE
from logic.gcommon.common_const import attr_const

class ComHeatMagazine(UnitCom):
    BIND_EVENT = {'G_ADD_HEAT_MAGAZINE': '_add_heat_magazine',
       'G_HEAT_MAGAZINE': '_get_heat_magazine',
       'E_REFRESH_HEAT_MAGAZINE': '_refresh_heat_magazine',
       'E_FORCE_EXECUTE_HEAT_DISSIPATION': 'force_execute_heat_dissipation',
       'E_DEC_MAGAZINE_HEAT': '_reduce_heat',
       'E_MOD_MAGZINE_CONF': '_mod_magzine_conf'
       }
    BIND_ATTR_CHANGE = {attr_const.ATR_HEAT_DEC_FACTOR: 'on_dec_factor_changed'
       }

    def __init__(self):
        super(ComHeatMagazine, self).__init__(need_update=True)
        self._heat_magazine = {}
        self.sd.ref_heat_magazine = self._heat_magazine
        self.is_force_dec = False

    def destroy(self):
        for mag in six.itervalues(self._heat_magazine):
            mag.destroy()

        self._heat_magazine = None
        self.sd.ref_heat_magazine = None
        super(ComHeatMagazine, self).destroy()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHeatMagazine, self).init_from_dict(unit_obj, bdict)
        for mag_key, mag_info in six.iteritems(bdict.get('heat_magazine', {})):
            self._add_heat_magazine(mag_key, mag_info, True)

    def _add_heat_magazine(self, mag_key, mag_info, is_init=False):
        if mag_key not in self._heat_magazine:
            self._heat_magazine[mag_key] = HeatMagazine(self, mag_key, mag_info)
            self._heat_magazine[mag_key].on_init_complete()
        if not is_init:
            self.start_tick()

    def _get_heat_magazine(self, key):
        return self._heat_magazine.get(key)

    def tick(self, dt):
        stop_tick = True
        for mag in six.itervalues(self._heat_magazine):
            stop_tick = stop_tick and mag.tick(dt)

        if stop_tick:
            self.need_update = False
        self.send_event('E_HEAT_MAGAZINE_CHANGED')

    def start_tick(self):
        if not self._need_update:
            self.need_update = True
        self.send_event('E_HEAT_MAGAZINE_CHANGED')

    def _refresh_heat_magazine(self, info):
        magazine_key = info.get('magazine_key')
        mag = self._heat_magazine.get(magazine_key)
        if mag:
            mag.refresh(info)

    def notify_heat_state_changed(self, key, state):
        is_force_dec = state & BAN_SHOOT_STATE
        if self.is_force_dec ^ is_force_dec:
            if is_force_dec:
                dissipation_duration = self._heat_magazine[key].get_dissipation_duration()
                self.send_event('E_BEGIN_FORCE_HEAT_DISSIPATION', key, dissipation_duration)
            else:
                self.send_event('E_END_FORCE_HEAT_DISSIPATION', key)
            self.is_force_dec = is_force_dec

    def notify_heat_level_changed(self, key, level):
        self.send_event('E_HEAT_LEVEL_CHANGED', key, level)

    def force_execute_heat_dissipation(self, key):
        if self._heat_magazine[key]._cur_heat <= 0.0:
            return
        self._heat_magazine[key].set_state(STATE_FORCE_DEC)

    def _reduce_heat(self, magazine_key, mod):
        mag = self._heat_magazine.get(magazine_key)
        if mag:
            mag.reduce_heat(mod)

    def on_dec_factor_changed(self, *args):
        for mag in six.itervalues(self._heat_magazine):
            mag.update_dec_param()

    def _mod_magzine_conf(self, mag_key, conf_id):
        mag = self._heat_magazine.get(mag_key)
        if not mag:
            return
        mag.mod_magzine_conf(conf_id)