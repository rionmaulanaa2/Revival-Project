# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaFuelClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import skill_const
from logic.gcommon.common_const import attr_const

class ComMechaFuelClient(UnitCom):
    BIND_EVENT = {'E_FUEL_DO_SKILL': 'on_fuel_do_skill',
       'E_FUEL_END_SKILL': 'on_fuel_end_skill',
       'E_LOSE_FUEL': 'on_lose_fuel',
       'G_FUEL': 'on_get_fuel',
       'G_MAX_FUEL': 'on_get_max_fuel',
       'E_SET_MAX_FUEL': 'on_set_max_fuel',
       'E_SET_CUR_FUEL': 'on_set_cur_fuel',
       'G_CONSUMING_FUEL': 'on_consuming_fuel',
       'E_ADD_FUEL': 'add_fuel',
       'E_FORBID_FUEL_RECOVER': 'on_forbid_fuel_recover'
       }
    BIND_ATTR_CHANGE = {attr_const.MECHA_ATTR_FUEL_RECOVER_FACTOR: 'on_add_attr_changed',
       attr_const.MECHA_FUEL_REGTIME_DEC_FACTOR: 'on_add_attr_changed'
       }

    def __init__(self):
        super(ComMechaFuelClient, self).__init__(need_update=False)
        self._cur_fuel = [0]
        self.skill_cost_fuel_dict = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaFuelClient, self).init_from_dict(unit_obj, bdict)
        self.cur_fuel = bdict.get('cur_fuel', 0)
        from common.cfg import confmgr
        mecha_id = bdict['mecha_id']
        fuel_conf = confmgr.get('mecha_conf', 'FuelConfig', 'Content', str(mecha_id))
        self.max_fuel = bdict.get('max_fuel') or fuel_conf['max_fuel']
        self.init_fuel_regspeed = fuel_conf['fuel_regspeed']
        self.fuel_regspeed = bdict.get('fuel_regspeed') or self.init_fuel_regspeed
        self.init_fuel_regtime = fuel_conf['regtime']
        self.fuel_regtime = self.get_real_regtime()
        self.cost_rate = 0
        left_regtime = bdict.get('fuel_regtime', 0)
        self.cur_regtime = self.fuel_regtime - left_regtime
        self.forbid_recover = False
        if self.cur_fuel < self.max_fuel:
            self.need_update = True

    def destroy(self):
        super(ComMechaFuelClient, self).destroy()

    @property
    def cur_fuel(self):
        return self._cur_fuel[0]

    @cur_fuel.setter
    def cur_fuel(self, v):
        self._cur_fuel[0] = None
        self._cur_fuel = [v]
        return

    def on_fuel_do_skill(self, skill_id, cost, cost_pre, cost_type):
        if hasattr(global_data, 'no_cd') and global_data.no_cd:
            return
        if cost_type in (skill_const.FUEL_COST_PER_TIMES, skill_const.FUEL_COST_PER_TIMES_INAIR):
            self.cur_fuel -= cost + cost_pre
            self.send_event('E_FUEL_CHANGE', self.cur_fuel / self.max_fuel)
            self.cur_regtime = 0
        else:
            self.cur_fuel -= cost_pre
            self.send_event('E_FUEL_CHANGE', self.cur_fuel / self.max_fuel)
            self.cost_rate += cost
            self.skill_cost_fuel_dict[skill_id] = cost
        self.need_update = True

    def on_fuel_end_skill(self, skill_id, cost, cost_type):
        if cost_type == skill_const.FUEL_COST_PER_SECOND:
            self.cost_rate -= self.skill_cost_fuel_dict.get(skill_id, cost)
            if self.cost_rate < 0.01:
                self.cost_rate = 0

    def on_lose_fuel(self, amount, affect_reg=False):
        self.cur_fuel = max(0, self.cur_fuel - amount)
        if affect_reg:
            self.cur_regtime = 0
        self.send_event('E_FUEL_CHANGE', self.cur_fuel / self.max_fuel)
        self.need_update = True

    def on_get_fuel(self):
        return self.cur_fuel

    def on_get_max_fuel(self):
        return self.max_fuel

    def on_set_max_fuel(self, max_fuel):
        self.max_fuel = max_fuel
        self.need_update = True

    def on_set_cur_fuel(self, cur_fuel):
        self.cur_fuel = cur_fuel
        self.send_event('E_FUEL_CHANGE', self.cur_fuel / self.max_fuel)

    def on_add_attr_changed(self, attr, item_id, pre_value, cur_value, source_info):
        if attr == attr_const.MECHA_ATTR_FUEL_RECOVER_FACTOR:
            self.fuel_regspeed = self.ev_g_addition_effect(self.init_fuel_regspeed, factor_attrs=[attr_const.MECHA_ATTR_FUEL_RECOVER_FACTOR])
        elif attr == attr_const.MECHA_FUEL_REGTIME_DEC_FACTOR:
            self.fuel_regtime = self.get_real_regtime()

    def tick(self, delta):
        if self.cost_rate > 0:
            self.cur_regtime = 0
            last_fuel = self.cur_fuel
            self.cur_fuel -= delta * self.cost_rate
            if self.cur_fuel <= 0:
                if 0 < last_fuel:
                    self.send_event('E_FUEL_EXHAUSTED')
                self.cur_fuel = 0
        else:
            self.cur_regtime += delta
            if not self.forbid_recover and self.cur_regtime > self.fuel_regtime:
                self.cur_fuel += self.fuel_regspeed * delta
                if self.cur_fuel >= self.max_fuel:
                    self.cur_fuel = self.max_fuel
                    self.need_update = False
        self.send_event('E_FUEL_CHANGE', self.cur_fuel / self.max_fuel)

    def on_consuming_fuel(self):
        return self.need_update and self.cost_rate > 0

    def add_fuel(self, delta):
        self.cur_fuel += delta
        if self.cur_fuel >= self.max_fuel:
            self.cur_fuel = self.max_fuel
        self.send_event('E_FUEL_CHANGE', self.cur_fuel / self.max_fuel)

    def on_forbid_fuel_recover(self, forbid):
        self.forbid_recover = forbid

    def get_real_regtime(self):
        return self.ev_g_addition_effect(self.init_fuel_regtime, factor_attrs=[attr_const.MECHA_FUEL_REGTIME_DEC_FACTOR])