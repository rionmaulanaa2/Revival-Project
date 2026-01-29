# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComHeatEnergyClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.cdata.mecha_status_config import MC_HEAT
from logic.gcommon import time_utility
from common.cfg import confmgr
NOR_HEAT_STATE = 0
MAX_HEAT_STATE = 1

class ComHeatEnergyClient(UnitCom):
    BIND_EVENT = {'E_SET_HEAT': '_set_heat',
       'E_DEATH': 'on_mecha_death',
       'E_HEALTH_HP_EMPTY': 'on_mecha_death',
       'E_ANIMATOR_LOADED': 'on_model_loaded',
       'G_HEAT': '_get_heat',
       'G_IN_MAX_HEAT': 'is_in_max_heat',
       'G_CAN_TRIGGER_HEAT': '_get_can_trigger_heat',
       'G_MAX_HEAT_ENTER_TIME': '_get_max_heat_enter_time',
       'G_ENABLE_TURN_SOUND': 'is_in_max_heat'
       }

    def __init__(self):
        super(ComHeatEnergyClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComHeatEnergyClient, self).init_from_dict(unit_obj, bdict)
        self._cur_heat = bdict.get('cur_heat', 0)
        self._heat_state = bdict.get('heat_state', 0)
        self._max_heat_enter_time = bdict.get('last_max_heat_state_enter_time', None)
        self.max_heat_value = 3000
        self._enter_state_min_heat = 400
        heat_conf = confmgr.get('mecha_conf', 'HeatEnergyConfig', 'Content').get(str(self.sd.ref_mecha_id))
        if heat_conf:
            self.max_heat_value = heat_conf.get('heat_cnt')
            self._enter_state_min_heat = heat_conf.get('enter_state_min_heat', 400)
        return

    def destroy(self):
        super(ComHeatEnergyClient, self).destroy()

    def on_model_loaded(self, *args):
        if self._heat_state == MAX_HEAT_STATE and not self.ev_g_get_state(MC_HEAT):
            self.send_event('E_TRY_IN_MAX_HEAT')

    def _set_heat(self, heat, heat_state):
        if self._heat_state != heat_state:
            if self._heat_state != MAX_HEAT_STATE and heat_state == MAX_HEAT_STATE:
                self.send_event('E_TRY_IN_MAX_HEAT')
            elif self._heat_state == MAX_HEAT_STATE and heat_state != MAX_HEAT_STATE:
                self.send_event('E_TRY_OUT_MAX_HEAT')
        if self._cur_heat <= self._enter_state_min_heat <= heat and self._heat_state != MAX_HEAT_STATE:
            self.send_event('E_ACTIVATE_HEAT', True)
        if self._heat_state == NOR_HEAT_STATE and heat_state == MAX_HEAT_STATE:
            self.send_event('E_ACTIVATE_HEAT', False)
        self._cur_heat = heat
        self._heat_state = heat_state

    def on_mecha_death(self):
        pass

    def _get_heat(self):
        return (
         self._cur_heat, self._heat_state)

    def is_in_max_heat(self):
        return self._heat_state == MAX_HEAT_STATE

    def _get_can_trigger_heat(self):
        return self._cur_heat >= self._enter_state_min_heat and self._heat_state != MAX_HEAT_STATE

    def _get_max_heat_enter_time(self):
        return self._max_heat_enter_time