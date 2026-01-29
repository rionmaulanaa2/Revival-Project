# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaSkillFuelClient.py
from __future__ import absolute_import
import six
import six_ex
from ..UnitCom import UnitCom
import logic.gcommon.time_utility as t_util
from logic.gcommon.common_const.skill_const import FUEL_COST_PER_TIMES, FUEL_COST_PER_SECOND, FUEL_COST_PER_TIMES_INAIR
from common.cfg import confmgr

class ComMechaSkillFuelClient(UnitCom):
    BIND_EVENT = {'E_SPEC_FUEL_DO_SKILL': 'on_fuel_do_skill',
       'E_SPEC_FUEL_END_SKILL': 'on_fuel_end_skill',
       'E_SET_SKILL_MAX_FUEL': 'on_set_skill_max_fuel',
       'E_SET_SKILL_CUR_FUEL': 'on_set_skill_cur_fuel',
       'E_ON_SKILL_ADDED': 'on_skill_added',
       'G_SKILL_FUEL': 'get_skill_fuel',
       'G_SKILL_MAX_FUEL': 'get_skill_max_fuel',
       'G_SKILL_FUEL_PERCENT': 'get_skill_percent',
       'E_ON_LEAVE_MECHA': 'on_recover_skill_fuel',
       'E_SYNC_SKILL_FUEL_CHANGE': 'on_sync_skill_fuel_change'
       }

    def __init__(self):
        super(ComMechaSkillFuelClient, self).__init__(need_update=True)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaSkillFuelClient, self).init_from_dict(unit_obj, bdict)
        self._cur_fuel = bdict.get('cur_fuel_dict', {})
        mecha_id = bdict['mecha_id']
        self.coomon_fuel_config = confmgr.get('mecha_conf', 'FuelConfig', 'Content', str(mecha_id))
        self._max_fuel = bdict.get('max_fuel_dict', {})
        self._regspeed = {}
        self._regtime = {}
        self._init_max_fuel = {}
        for skill_id in six.iterkeys(self._cur_fuel):
            conf = confmgr.get('skill_conf', str(skill_id))
            self._init_max_fuel[skill_id] = conf.get('max_fuel', 0)
            self._regtime[skill_id] = conf.get('fuel_regtime', 0)
            self._regspeed[skill_id] = conf.get('fuel_regspeed', 0)

        self._next_regtime = bdict.get('next_regtime_dict', {})
        self._durative_cost = bdict.get('durative_cost', {})
        self.need_update = True

    def destroy(self):
        super(ComMechaSkillFuelClient, self).destroy()

    def on_skill_added(self, skill_id):
        conf = confmgr.get('skill_conf', str(skill_id))
        if conf.get('max_fuel') and skill_id not in self._cur_fuel:
            self._init_max_fuel[skill_id] = conf.get('max_fuel', 0)
            self._max_fuel[skill_id] = self._init_max_fuel[skill_id]
            self._regtime[skill_id] = conf.get('fuel_regtime', 0)
            self._regspeed[skill_id] = conf.get('fuel_regspeed', 0)

    def get_skill_fuel(self, skill_id):
        return self._cur_fuel.get(skill_id, 0)

    def on_fuel_do_skill(self, skill_id, cost_cnt, cost_pre, cost_type):
        if hasattr(global_data, 'no_cd') and global_data.no_cd:
            return
        if skill_id not in self._cur_fuel:
            return
        if cost_type in (FUEL_COST_PER_TIMES, FUEL_COST_PER_TIMES_INAIR):
            if self._cur_fuel[skill_id] < cost_cnt:
                return False
            self._reduce_fuel(skill_id, cost_cnt)
            self._next_regtime[skill_id] = t_util.time() + self._regtime[skill_id]
        else:
            if self._cur_fuel[skill_id] < cost_pre:
                return False
            self._reduce_fuel(skill_id, cost_pre)
            self._durative_cost[skill_id] = cost_cnt
        self.need_update = True

    def on_fuel_end_skill(self, skill_id, *args):
        if skill_id in self._durative_cost:
            del self._durative_cost[skill_id]
            self._next_regtime[skill_id] = t_util.time() + self._regtime[skill_id]

    def on_set_skill_max_fuel(self, skill_id, max_fuel):
        if skill_id in self._max_fuel:
            self._max_fuel[skill_id] = max_fuel

    def on_set_skill_cur_fuel(self, skill_id, cur_fuel):
        if skill_id in self._cur_fuel:
            self._cur_fuel[skill_id] = cur_fuel
            self.send_event('E_SKILL_FUEL_CHANGE', skill_id, self._cur_fuel[skill_id] / self._max_fuel[skill_id])
        self.need_update = True

    def get_skill_percent(self, skill_id):
        if skill_id in self._cur_fuel and skill_id in self._max_fuel:
            return self._cur_fuel[skill_id] / self._max_fuel[skill_id]
        return 0.0

    def get_skill_max_fuel(self, skill_id):
        return self._max_fuel.get(skill_id)

    def tick(self, dt):
        need_update = False
        for skill_id in six.iterkeys(self._cur_fuel):
            if skill_id in six_ex.keys(self._durative_cost):
                last_fuel = self._cur_fuel[skill_id]
                self._reduce_fuel(skill_id, self._durative_cost[skill_id] * dt)
                if self._cur_fuel[skill_id] <= 0:
                    self._cur_fuel[skill_id] = 0
                    self._next_regtime[skill_id] = t_util.time() + self._regtime[skill_id]
                    if last_fuel > 0:
                        self.send_event('E_SKILL_FUEL_EXHAUSTED', skill_id)
                need_update = True
            else:
                if self._cur_fuel[skill_id] == self._max_fuel[skill_id] or t_util.time() < self._next_regtime.get(skill_id, 0):
                    return
                self._cur_fuel[skill_id] += self._regspeed[skill_id] * dt
                self._cur_fuel[skill_id] = min(self._cur_fuel[skill_id], self._max_fuel[skill_id])
                need_update = True
            self.send_event('E_SKILL_FUEL_CHANGE', skill_id, self._cur_fuel[skill_id] / self._max_fuel[skill_id])

        self.need_update = need_update

    def on_recover_skill_fuel(self):
        self._durative_cost = {}
        self.need_update = True

    def _reduce_fuel(self, skill_id, delta):
        if delta <= 0:
            return
        if delta > self._cur_fuel[skill_id]:
            self._cur_fuel[skill_id] = 0
        else:
            self._cur_fuel[skill_id] -= delta

    def on_sync_skill_fuel_change(self, skill_id, new_fuel):
        self._cur_fuel.setdefault(skill_id, 0)
        self._max_fuel.setdefault(skill_id, 0)
        pre_fuel = self._cur_fuel[skill_id]
        self._cur_fuel[skill_id] = min(new_fuel, self._max_fuel[skill_id])
        real_delta = self._cur_fuel[skill_id] - pre_fuel
        if real_delta != 0:
            self.send_event('E_SKILL_FUEL_CHANGE', skill_id, self._cur_fuel[skill_id] / self._max_fuel[skill_id])