# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVETowerWeapon.py
from __future__ import absolute_import
from six.moves import range
from SkillPVEWeapon import SkillPVEWeapon
from common.utils.timer import CLOCK

class SkillPVETowerWeapon(SkillPVEWeapon):

    def remote_do_skill(self, skill_data):
        if not self._weapon_pos:
            return
        fire_cnt = skill_data.get('fire_cnt', 1)
        for i in range(fire_cnt):
            self._unit_obj.ev_g_try_weapon_attack_begin(self._weapon_pos)
            self._unit_obj.ev_g_try_weapon_attack_end(self._weapon_pos)