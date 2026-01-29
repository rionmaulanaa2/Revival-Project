# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/HeatMagazineServer.py
from __future__ import absolute_import
from logic.gcommon import time_utility
from logic.gcommon.common_const import weapon_const
from logic.gcommon.common_const.weapon_const import STATE_NONE, STATE_SHOOT, STATE_NORMAL_DEC, STATE_FORCE_DEC, BAN_SHOOT_STATE, HEAT_DEC_STATE
from logic.gcommon.common_const.attr_const import ATTR_RELOAD_SPEED_FACTOR, ATR_HEAT_DEC_FACTOR

class HeatMagazine(object):

    def __init__(self, unit_com, magazine_id, info):
        self._unit_com = unit_com
        self._magazine_id = magazine_id
        self._state = STATE_NONE
        self._state_start_time = 0
        self._cur_heat = 0
        self._mag_conf_id = 1
        self._mag_info = info
        self._inc_heat = info.get('IncHeat', {1: [0, 8]})[self._mag_conf_id]
        self._max_heat = info.get('MaxHeat', 1)
        self._dissipate_time = info.get('DissipateTime', 0)
        self._normal_dec_heat = info.get('NormalDecHeat', 0)
        self._reload_dec_heat = info.get('ReloadDecHeat', 0)
        self.normal_dec_heat_imp = self._normal_dec_heat
        self.reload_dec_heat_imp = self._reload_dec_heat
        self.dissipate_time = self._dissipate_time

    def destroy(self):
        self._unit_com = None
        return

    def get_client_dict(self):
        d = {'magazine_id': self._magazine_id,
           'cur_heat': self._cur_heat,
           'inc_heat': self._mag_info.get('IncHeat'),
           'max_heat': self._max_heat,
           'state': self._state,
           'dissipate_time': self._dissipate_time,
           'normal_dec_heat': self._normal_dec_heat,
           'reload_dec_heat': self._reload_dec_heat,
           'mag_conf_id': self._mag_conf_id
           }
        return d

    def get_throw_dict(self):
        d = {'cur_heat': self._cur_heat,
           'throw_time': time_utility.get_time()
           }
        return d

    def recover_from_data(self, data):
        cur_heat = data.get('cur_heat', 0)
        dt = time_utility.get_time() - data.get('throw_time', 0)
        self._cur_heat = max(0, cur_heat - dt * self._reload_dec_heat)

    def tick(self, dt):
        if self._state == STATE_NONE:
            return
        if self._state == STATE_SHOOT:
            if time_utility.get_time() > self._state_start_time + self.dissipate_time:
                self.set_state(STATE_NORMAL_DEC)
        elif self._state == STATE_NORMAL_DEC:
            self._cur_heat -= self.normal_dec_heat_imp * dt
            if self._cur_heat <= 0:
                self._cur_heat = 0
                self.set_state(STATE_NONE)
        elif self._state & BAN_SHOOT_STATE:
            self._cur_heat -= self.reload_dec_heat_imp * dt
            if self._cur_heat <= 0:
                self._cur_heat = 0
                self.set_state(STATE_NONE)

    def get_inc_heat(self):
        inc_heat = 1
        for h, inc in self._inc_heat:
            if self._cur_heat >= h:
                inc_heat = inc
            else:
                break

        return inc_heat

    def do_shoot(self):
        self.set_state(STATE_SHOOT)
        self._cur_heat = min(self._max_heat, self._cur_heat + self.get_inc_heat())
        self._state_start_time = time_utility.get_time()
        return True

    def reduce_heat(self, mod):
        if mod <= 0:
            return
        self._cur_heat = max(self._cur_heat - mod, 0)

    def on_sync_state(self, state, heat, timestamp):
        if state not in weapon_const.ALL_HEAT_STATE_SET:
            return
        self.set_state(state)
        self._cur_heat = min(max(heat, 0), self._max_heat)
        self._state_start_time = timestamp

    def set_state(self, state, sync=True):
        if self._state == state:
            return
        self._state = state
        if state & HEAT_DEC_STATE:
            self.update_dec_param()

    def update_dec_param(self):
        if self._unit_com:
            factor = self._unit_com.ev_g_add_attr(ATTR_RELOAD_SPEED_FACTOR, self._magazine_id) or 0
            normal_factor = self._unit_com.ev_g_add_attr(ATR_HEAT_DEC_FACTOR, self._magazine_id) or 0
            self.dissipate_time = self._dissipate_time * (1 - normal_factor)
            self.normal_dec_heat_imp = self._normal_dec_heat * (1 + normal_factor + factor)
            self.reload_dec_heat_imp = self._reload_dec_heat * (1 + factor)

    def mod_magzine_conf(self, conf_id):
        self._mag_conf_id = conf_id
        self._inc_heat = self._mag_info.get('IncHeat', {1: [0, 8]})[self._mag_conf_id]