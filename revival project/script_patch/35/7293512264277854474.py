# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillSecWeapon8019.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from logic.gcommon.time_utility import time
from logic.gcommon.common_utils.bcast_utils import E_8019_SEC_FULL

class SkillSecWeapon8019(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillSecWeapon8019, self).__init__(skill_id, unit_obj, data)
        self._max_energy = 0
        self._init_energy = None
        self._recover_spd = 1
        self._cur_energy = None
        self._recover_interval = None
        self._next_recover_time = None
        self.cur_t = None
        self.timer_id = None
        self.full_tag = False
        return

    def update_skill(self, data, trigger_update_event=True):
        super(SkillSecWeapon8019, self).update_skill(data, trigger_update_event)
        self.time_dur = self._max_energy * 1.5 / self._recover_spd + 5.0

    def on_add(self):
        super(SkillSecWeapon8019, self).on_add()
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
        self.cur_t = time()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.update, interval=0.1, times=self.time_dur * 10, mode=2, timedelta=True)

    def tick(self, dt):
        super(SkillSecWeapon8019, self).tick(dt)

    def update(self, dt):
        if self.cur_t > self._next_recover_time:
            self._cur_energy += self._recover_spd * dt
            if self._cur_energy >= self._max_energy:
                self._cur_energy = self._max_energy
                if not self.full_tag:
                    self._unit_obj.send_event('E_8019_SEC_FULL')
                    self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_8019_SEC_FULL, ()], True)
                    self.full_tag = True
        else:
            self.cur_t += dt
        self._unit_obj.send_event('E_EC_8019', self._cur_energy * 1.0 / self._max_energy)

    def change_energy(self, energy):
        self._cur_energy = energy
        self._unit_obj.send_event('E_EC_8019_S', energy)
        if energy == 0:
            self.cur_t = time()
            self._next_recover_time = self.cur_t + self._recover_interval
            if self.timer_id:
                global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = global_data.game_mgr.register_logic_timer(self.update, interval=0.1, times=self.time_dur * 10, mode=2, timedelta=True)
            self.full_tag = False
        if abs(self._max_energy - energy) < 1:
            if not self.full_tag:
                self._unit_obj.send_event('E_8019_SEC_FULL')
                self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_8019_SEC_FULL, ()], True)
                self.full_tag = True

    def get_full_tag(self):
        return self.full_tag

    def destroy(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        super(SkillSecWeapon8019, self).destroy()
        return