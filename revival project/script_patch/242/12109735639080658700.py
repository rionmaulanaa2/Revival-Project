# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVEWeapon.py
from __future__ import absolute_import
from .SkillBase import SkillBase
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gcommon import time_utility as tutil

class SkillPVEWeapon(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVEWeapon, self).__init__(skill_id, unit_obj, data)
        self._weapon_id = data.get('weapon_id')
        self._weapon_pos = data.get('weapon_pos')
        ext_info = confmgr.get('skill_conf', str(self._skill_id), 'ext_info', default={})
        self.fire_socket_follow_wp_pos = ext_info.get('fire_socket_follow_wp_pos', None)
        self.fire_cd = ext_info.get('fire_cd', 0)
        self.timer_id = None
        self.last_fire_end_ts = 0
        return

    def update_skill(self, data, trigger_update_event=True):
        super(SkillPVEWeapon, self).update_skill(data, trigger_update_event)

    def remote_do_skill(self, skill_data):
        if self.fire_cd > 0 and self.fire_cd >= tutil.time() - self.last_fire_end_ts:
            return
        gun_status_inf = self._unit_obj.ev_g_gun_status_inf(self._skill_id)
        if not gun_status_inf:
            return
        if self.fire_socket_follow_wp_pos:
            follow_status_inf = self._unit_obj.ev_g_gun_status_inf(self.fire_socket_follow_wp_pos)
            if follow_status_inf:
                gun_status_inf.set_socket_list([follow_status_inf.get_fired_socket_name()])
        duration = skill_data.get('duration', 0)
        if not self._weapon_pos:
            return
        self.destroy_timer()
        if not self._unit_obj.ev_g_try_weapon_attack_begin(self._weapon_pos):
            return
        if duration:
            self.timer_id = global_data.game_mgr.register_logic_timer(func=self.skill_end, times=1, mode=CLOCK, interval=duration)
        else:
            self.skill_end()

    def skill_end(self):
        self.destroy_timer()
        self._unit_obj.ev_g_try_weapon_attack_end(self._weapon_pos)
        if self.fire_cd > 0:
            self.last_fire_end_ts = tutil.time()

    def destroy_timer(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return

    def destroy(self):
        super(SkillPVEWeapon, self).destroy()
        self.destroy_timer()