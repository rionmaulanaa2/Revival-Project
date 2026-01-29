# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillMecha12Bump.py
from __future__ import absolute_import
from .SkillBase import SkillBase

class SkillMecha12Bump(SkillBase):

    def on_add(self):
        pass

    def on_remove(self):
        pass

    def do_skill(self, target_id, start_pos, speed, energy, timestamp):
        if start_pos:
            start_pos = (
             start_pos.x, start_pos.y, start_pos.z)
        return (target_id, start_pos, speed, energy, timestamp)