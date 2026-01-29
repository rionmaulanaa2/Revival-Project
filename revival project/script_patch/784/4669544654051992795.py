# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillHighSpeedEnergy.py
from __future__ import absolute_import
from .SkillBase import SkillBase

class SkillHighSpeedEnergy(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillHighSpeedEnergy, self).__init__(skill_id, unit_obj, data)
        ext_info = self._data.get('ext_info')
        self._add_energy = ext_info.get('add_energy', 0)
        self._add_skill_id = ext_info.get('add_skill_id', None)
        return

    def on_add(self):
        super(SkillHighSpeedEnergy, self).on_add()

    def on_remove(self):
        super(SkillHighSpeedEnergy, self).on_remove()

    def do_skill(self, *args):
        if not self._add_skill_id:
            return
        self._unit_obj.send_event('E_SKILL_MOD_MP', self._add_skill_id, self._add_energy)