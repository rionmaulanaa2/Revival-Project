# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillShockWave8021.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
from .SkillBase import SkillBase
from common.cfg import confmgr

class SkillShockWave8021(SkillBase):

    def do_skill(self, wave_hit_target, start_pos):
        return (
         wave_hit_target, start_pos)