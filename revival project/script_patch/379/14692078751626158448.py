# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/HeatMagazineClient.py
from __future__ import absolute_import
from logic.gcommon import time_utility
from common.cfg import confmgr
from logic.gcommon.common_const.weapon_const import STATE_NONE, STATE_SHOOT, STATE_NORMAL_DEC, STATE_FORCE_DEC, BAN_SHOOT_STATE, HEAT_DEC_STATE, STATE_FORCE_DEC_OVERLOAD
from logic.gcommon.common_const.attr_const import ATTR_RELOAD_SPEED_FACTOR, ATR_HEAT_DEC_FACTOR

class HeatMagazine(object):
    tick_dummy = lambda *args: True
    HANDLER_MAP = {STATE_NONE: 'tick_dummy',
       STATE_SHOOT: 'tick_shoot',
       STATE_NORMAL_DEC: 'tick_normal_dec',
       STATE_FORCE_DEC: 'tick_reload_dec',
       STATE_FORCE_DEC_OVERLOAD: 'tick_reload_dec'
       }

    def __init__(self, unit_com, magazine_key, info):
        self._unit_com = unit_com
        self._magazine_key = magazine_key
        self._magazine_id = info.get('magazine_id', 0)
        self._state = -1
        self._state_trans_time = 0
        self._cur_heat = info.get('cur_heat', 0)
        self._mag_conf_id = 1
        self._mag_info = info
        self._inc_heat = info.get('inc_heat', {1: [0, 8]})[self._mag_conf_id]
        self._max_heat = info.get('max_heat', 0)
        self._dissipate_time = info.get('dissipate_time', 0)
        self._normal_dec_heat = info.get('normal_dec_heat', 0)
        self._reload_dec_heat = info.get('reload_dec_heat', 0)
        conf = confmgr.get('gun_heat', str(self._magazine_id), default={})
        self._shoot_args = conf.get('ShootArgs', {}).get(str(self._mag_conf_id), [])
        self._cur_shoot_level = 0
        self._cur_shoot_args = {}
        self.normal_dec_heat_imp = self._normal_dec_heat
        self.reload_dec_heat_imp = self._reload_dec_heat
        self.dissipate_time = self._dissipate_time
        self.server_state = info.get('state', STATE_NONE)

    def on_init_complete(self):
        self.set_state(self.server_state)

    def destroy(self):
        self.tick = None
        self._unit_com = None
        self._mag_info = None
        return

    def can_shoot(self):
        if not self._unit_com:
            return False
        if self._state & BAN_SHOOT_STATE:
            return False
        return True

    def get_inc_heat(self):
        inc_heat = 1
        for h, inc in self._inc_heat:
            if self._cur_heat >= h:
                inc_heat = inc
            else:
                break

        return inc_heat

    def do_shoot(self, num):
        if not self._unit_com:
            return
        self.cur_heat += self.get_inc_heat() * num
        if self.cur_heat >= self._max_heat:
            self.set_state(STATE_FORCE_DEC_OVERLOAD)
        else:
            self.set_state(STATE_SHOOT)
            self._state_trans_time = time_utility.get_time() + self.dissipate_time
        self._unit_com.start_tick()

    def reduce_heat(self, mod):
        self.cur_heat = max(self.cur_heat - mod, 0)

    @property
    def cur_heat(self):
        return self._cur_heat

    @cur_heat.setter
    def cur_heat(self, v):
        self._cur_heat = v
        for level, args in self._shoot_args:
            if v >= level:
                break
        else:
            level = 0
            args = {}

        if level != self._cur_shoot_level:
            self._cur_shoot_level = level
            self._cur_shoot_args = args
            self._unit_com.notify_heat_level_changed(self._magazine_key, level)

    @property
    def cur_heat_percent(self):
        return float(self._cur_heat) / self._max_heat

    def set_state(self, state, sync=True):
        if self._state == state:
            return
        self._state = state
        if state & HEAT_DEC_STATE:
            self.update_dec_param()
        self._unit_com.notify_heat_state_changed(self._magazine_key, state)
        handle_name = HeatMagazine.HANDLER_MAP[state]
        self.tick = getattr(self, handle_name)
        if sync:
            self._unit_com.send_event('E_CALL_SYNC_METHOD', 'upload_heat_magazine_info', (self._magazine_key, state, self.cur_heat, time_utility.get_server_time_battle()))

    def tick_shoot(self, dt):
        if time_utility.get_time() >= self._state_trans_time:
            self.set_state(STATE_NORMAL_DEC)

    def tick_normal_dec(self, dt):
        self.cur_heat -= self.normal_dec_heat_imp * dt
        if self.cur_heat <= 0:
            self.cur_heat = 0
            self.set_state(STATE_NONE)

    def tick_reload_dec(self, dt):
        self.cur_heat -= self.reload_dec_heat_imp * dt
        if self.cur_heat <= 0:
            self.cur_heat = 0
            self.set_state(STATE_NONE)

    def get_fire_cd_ratio(self):
        return self._cur_shoot_args.get('speed', 0)

    def get_fire_spread_ratio(self):
        return self._cur_shoot_args.get('spread', 0)

    def refresh(self, info):
        pass

    def update_dec_param(self):
        if self._unit_com:
            factor = self._unit_com.ev_g_add_attr(ATTR_RELOAD_SPEED_FACTOR, self._magazine_id) or 0
            normal_factor = self._unit_com.ev_g_add_attr(ATR_HEAT_DEC_FACTOR, self._magazine_id) or 0
            self.dissipate_time = self._dissipate_time * (1 - normal_factor)
            self.normal_dec_heat_imp = self._normal_dec_heat * (1 + normal_factor + factor)
            self.reload_dec_heat_imp = self._reload_dec_heat * (1 + factor)

    def update_sec_heart(self):
        pass

    def get_dissipation_duration(self):
        return float(self._cur_heat) / self.reload_dec_heat_imp

    def mod_magzine_conf(self, conf_id):
        self._mag_conf_id = conf_id
        self._inc_heat = self._mag_info['inc_heat'][self._mag_conf_id]
        conf = confmgr.get('gun_heat', str(self._magazine_id), default={})
        self._shoot_args = conf.get('ShootArgs', {}).get(str(self._mag_conf_id), [])