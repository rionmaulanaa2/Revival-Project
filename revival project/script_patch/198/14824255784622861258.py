# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComHandyShieldCore.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import weakref
from logic.gcommon.time_utility import time
from logic.gcommon.common_const.mecha_const import HANDY_SHIELD_BONE, HANDY_SHIELD_SOCKET, DEFEND_ON, DEFEND_OFF, HANDY_SHIELD_MAX_HP
from logic.gcommon.common_const.skill_const import SKILL_LIGHT_CAKE

class ComHandyShieldCore(UnitCom):
    BIND_EVENT = {'E_ON_LOAD_SHIELD_MODEL': 'on_load_shield_model',
       'E_ON_LOAD_SHIELD_COL': 'on_load_shield_col',
       'E_ENTER_DEFEND': 'on_enter_defend',
       'E_EXIT_DEFEND': 'on_exit_defend',
       'E_HANDY_SHIELD_HP': 'on_change_hp',
       'G_HANDY_SHIELD_HP': 'get_cur_hp',
       'G_HANDY_SHIELD_HP_S': 'get_cur_hp_s',
       'G_HANDY_SHIELD_STATE': 'get_cur_state',
       'G_CHECK_ENTER_DEFEND': 'on_check_enter_defend',
       'E_LIGHT_CAKE_ENERGY_CHANGE': 'on_energy_change',
       'E_MAX_SHIELD_HP_CHANGE': 'on_change_max_hp',
       'G_SEC_FULL_TAG': 'get_sec_wp_full_tag'
       }

    def __init__(self):
        super(ComHandyShieldCore, self).__init__()
        self.need_update = True

    def init_from_dict(self, unit_obj, bdict):
        super(ComHandyShieldCore, self).init_from_dict(unit_obj, bdict)
        self._defend_state = DEFEND_OFF
        self.defend_state = bdict.get('defend_state', DEFEND_OFF)
        self.max_shield_hp = bdict.get('max_shield_hp', 1)
        self.min_enter_hp = bdict.get('defend_min_shield_hp', 0.5)
        self.cur_shield_hp = bdict.get('cur_shield_hp', 0)
        self.recover_speed = bdict.get('shield_hp_recover_spd', 0.1)
        self.rest_time = bdict.get('hp_rest_time', 1)
        self.next_recover_timestamp = bdict.get('next_hp_recover_timestamp', 0)
        if self.defend_state == DEFEND_OFF:
            self.need_update = True
        else:
            self.need_update = False
        self.init_params()
        self.send_event('E_TRY_SWITCH_DEFEND', self.defend_state)
        self.last_shield_hp = self.cur_shield_hp

    @property
    def defend_state(self):
        return self._defend_state

    @defend_state.setter
    def defend_state(self, v):
        self._defend_state = v
        self.sd.ref_raise_shield = v == DEFEND_ON

    def init_params(self):
        self.mecha_model = None
        self.col = None
        self.cid = None
        self.cur_t = 0
        self.skill_obj = None
        return

    def on_load_shield_model(self, model, mecha_model):
        self.mecha_model = mecha_model

    def on_load_shield_col(self, model, col):
        self.col = col

    def on_enter_defend(self):
        self.send_event('E_ADD_HS_COL', self.col)
        self.defend_state = DEFEND_ON
        self.send_event('E_SC_8019', self.cur_shield_hp, self.max_shield_hp, self.cur_shield_hp < self.min_enter_hp)
        self.need_update = False

    def on_exit_defend(self):
        self.send_event('E_REMOVE_HS_COL')
        self.defend_state = DEFEND_OFF
        self.cur_t = time()
        self.next_recover_timestamp = self.cur_t + self.rest_time
        self.need_update = True

    def on_change_hp(self, hp):
        self.last_shield_hp = self.cur_shield_hp
        self.cur_shield_hp = hp
        self.send_event('E_SC_8019_S', self.cur_shield_hp, self.max_shield_hp, self.cur_shield_hp < self.min_enter_hp)
        gap = abs(self.last_shield_hp - self.cur_shield_hp)
        if gap > 1000:
            gap = 1000
        rtpc_val = gap / 10
        global_data.sound_mgr.set_rtpc_ex('shd_hit', rtpc_val)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, ('m_8019_shd_hit', 'nf'), 0, 0, 0, 0)

    def tick(self, dt):
        if self.cur_t > self.next_recover_timestamp:
            self.cur_shield_hp += self.recover_speed * dt
            if self.cur_shield_hp >= self.max_shield_hp:
                self.cur_shield_hp = self.max_shield_hp
                self.need_update = False
                self.send_event('E_SC_8019_FULL')
        else:
            self.cur_t += dt
        self.send_event('E_SC_8019', self.cur_shield_hp, self.max_shield_hp, self.cur_shield_hp < self.min_enter_hp)

    def get_cur_hp(self):
        return (
         self.cur_shield_hp, self.max_shield_hp, self.cur_shield_hp < self.min_enter_hp)

    def get_cur_hp_s(self):
        return (
         self.cur_shield_hp * 1.0 / self.max_shield_hp, self.cur_shield_hp < self.min_enter_hp)

    def get_cur_state(self):
        return self.defend_state

    def on_check_enter_defend(self):
        return self.cur_shield_hp >= self.min_enter_hp

    def on_energy_change(self, energy):
        if not self.skill_obj:
            self.skill_obj = self.ev_g_skill(SKILL_LIGHT_CAKE)
        self.skill_obj.change_energy(energy)

    def on_change_max_hp(self, hp):
        self.max_shield_hp = hp
        self.send_event('E_SC_8019', self.cur_shield_hp, self.max_shield_hp, self.cur_shield_hp < self.min_enter_hp)
        if self.defend_state == DEFEND_OFF:
            self.need_update = True
            self.send_event('E_SHOW_SHIELD_HP_8019')
        else:
            self.need_update = False

    def get_sec_wp_full_tag(self):
        if not self.skill_obj:
            self.skill_obj = self.ev_g_skill(SKILL_LIGHT_CAKE)
        return self.skill_obj.get_full_tag()

    def destroy(self):
        self.init_params()
        super(ComHandyShieldCore, self).destroy()