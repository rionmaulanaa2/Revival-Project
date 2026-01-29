# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillHighSpeed.py
from __future__ import absolute_import
from .SkillBase import SkillBase

class SkillHighSpeed(SkillBase):

    def on_add(self):
        super(SkillHighSpeed, self).on_add()
        self._tell_ui_at_once = False

    def on_remove(self):
        super(SkillHighSpeed, self).on_remove()

    def do_skill(self, *args):
        start_pos, end_pos = args
        return (
         [
          start_pos.x, start_pos.y, start_pos.z], [end_pos.x, end_pos.y, end_pos.z])