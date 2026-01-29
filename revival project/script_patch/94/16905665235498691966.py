# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillShield8026.py
from __future__ import absolute_import
from .SkillBase import SkillBase

class SkillShield8026(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillShield8026, self).__init__(skill_id, unit_obj, data)
        self.max_shield_duration = data.get('ext_info', {}).get('max_shield_duration', 10.0)

    def update_skill(self, data, trigger_update_event=True):
        super(SkillShield8026, self).update_skill(data, trigger_update_event)
        if 'max_shield_duration' in data:
            self.max_shield_duration = data['max_shield_duration']
        add_shield_duration_factor = data.get('add_shield_duration_factor', 0.0)
        self._unit_obj.send_event('E_UPDATE_SHIELD_MAX_TIME', self.max_shield_duration * (1.0 + add_shield_duration_factor))

    def do_skill(self, *args):
        return args