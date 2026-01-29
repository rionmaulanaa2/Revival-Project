# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPhotonTower.py
from __future__ import absolute_import
import math3d
from .SkillCd import SkillCd

class SkillPhotonTower(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPhotonTower, self).__init__(skill_id, unit_obj, data)

    def do_skill(self, *args):
        if self._unit_obj and self._unit_obj.is_valid():
            target, pos, rot = self._unit_obj.ev_g_attack_info()
            target_ids = [target.id]
            rot = math3d.matrix_to_rotation(rot)
            self._unit_obj.send_event('E_SHOW_PHOTON_GUIDE_EFFECT')
            start_pos = self._unit_obj.ev_g_position()
            return (
             target_ids, (start_pos.x, start_pos.y, start_pos.z), (rot.x, rot.y, rot.z, rot.w))

    def on_add(self):
        super(SkillPhotonTower, self).on_add()
        if self._unit_obj:
            self._unit_obj.send_event('E_ADD_SKILL_SUCCESS', self._skill_id)
            if self._mp >= 0 and self._max_mp > 0:
                self._unit_obj.send_event('E_ENERGY_CHANGE', self._skill_id, self._mp * 1.0 / self._max_mp)

    def on_remove(self):
        super(SkillPhotonTower, self).on_remove()
        if self._unit_obj:
            self._unit_obj.send_event('E_DEL_SKILL', self._skill_id)