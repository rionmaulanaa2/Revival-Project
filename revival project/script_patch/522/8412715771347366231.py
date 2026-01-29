# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVEMechaSummon.py
from __future__ import absolute_import
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from SkillBase import SkillBase

class SkillPVEMechaSummon(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVEMechaSummon, self).__init__(skill_id, unit_obj, data)
        self._weapon_id = None
        self._weapon_pos = None
        self.timer_id = None
        return

    def update_skill(self, data, trigger_update_event=True):
        super(SkillPVEMechaSummon, self).update_skill(data, trigger_update_event)

    def remote_do_skill(self, *args):
        forward = self._unit_obj.ev_g_forward()
        spawn_dist_range = [2 * NEOX_UNIT_SCALE, 6 * NEOX_UNIT_SCALE]
        sweep_dist = spawn_dist_range[1] + NEOX_UNIT_SCALE
        sweep_result = self._unit_obj.ev_g_sweep_test(forward * sweep_dist)
        if sweep_result[0]:
            dist = sweep_result[3] * sweep_dist
            dist = min(max(dist, spawn_dist_range[0]), spawn_dist_range[1])
        else:
            dist = spawn_dist_range[1]
        pos = self._unit_obj.ev_g_position() + forward * dist
        self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'do_skill', (
         self._skill_id, ([pos.x, pos.y + 50, pos.z], [forward.x, forward.y, forward.z])))

    def skill_end(self):
        self.destroy_timer()
        self._unit_obj.ev_g_try_weapon_attack_end(self._weapon_pos)

    def destroy_timer(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return

    def destroy(self):
        self.destroy_timer()