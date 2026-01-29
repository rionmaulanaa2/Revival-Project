# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPoisonJump.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from common.utils.timer import CLOCK
import logic.gcommon.time_utility as tutils

class SkillPoisonJump(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPoisonJump, self).__init__(skill_id, unit_obj, data)
        self._cost_fuel_by_level = data.get('cost_fuel_by_level', None)
        self._fuel_level_reset_time = data.get('fuel_level_reset_time', 15)
        self.fuel_level = data.get('fuel_level', 0)
        self.fuel_level_reset_timer_id = None
        reset_ts = None
        if self.fuel_level > 0:
            reset_ts = data.get('fuel_level_reset_ts', None)
            if reset_ts:
                self.fuel_level_reset_timer_id = global_data.game_mgr.register_logic_timer(self.reset_fuel_level, interval=reset_ts - tutils.time(), times=1, mode=CLOCK)
        self._unit_obj.send_event('E_POISON_JUMP_FUEL_LEVEL', self.fuel_level, reset_time=self._fuel_level_reset_time, reset_ts=reset_ts)
        return

    def get_cost_fuel(self):
        if self._cost_fuel_by_level:
            if self.fuel_level < len(self._cost_fuel_by_level):
                return self._cost_fuel_by_level[self.fuel_level]
            else:
                return self._cost_fuel_by_level[-1]

        else:
            return self._cost_fuel

    def do_skill(self, *args):
        super(SkillPoisonJump, self).do_skill()
        self.fuel_level += 1
        if self.fuel_level_reset_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.fuel_level_reset_timer_id)
        self.fuel_level_reset_timer_id = global_data.game_mgr.register_logic_timer(self.reset_fuel_level, interval=self._fuel_level_reset_time, times=1, mode=CLOCK)
        if self._unit_obj:
            self._unit_obj.send_event('E_POISON_JUMP_FUEL_LEVEL', self.fuel_level, reset_time=self._fuel_level_reset_time)

    def reset_fuel_level(self):
        if self.fuel_level_reset_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.fuel_level_reset_timer_id)
            self.fuel_level_reset_timer_id = None
        self.fuel_level = 0
        if self._unit_obj:
            self._unit_obj.send_event('E_POISON_JUMP_FUEL_LEVEL', self.fuel_level)
        return