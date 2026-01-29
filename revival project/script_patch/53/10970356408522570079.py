# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillMultiJump.py
from __future__ import absolute_import
from .SkillCd import SkillCd

class SkillMultiJump(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillMultiJump, self).__init__(skill_id, unit_obj, data)
        self._add_jump_stage = data.get('add_jump_stage', 0)

    def on_add(self):
        pass

    def update_skill(self, data, trigger_update_event=True):
        if not data:
            return
        pre_stage = self._add_jump_stage
        super(SkillMultiJump, self).update_skill(data, trigger_update_event)
        if self._add_jump_stage != pre_stage and 'add_jump_stage' in data:
            self._unit_obj.send_event('E_ADD_JUMP_MAX_STAGE', self._add_jump_stage - pre_stage)

    def on_remove(self):
        self._unit_obj.send_event('E_ADD_JUMP_MAX_STAGE', -self._add_jump_stage)
        self._add_jump_stage = 0
        super(SkillMultiJump, self).on_remove()