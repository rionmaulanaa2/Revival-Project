# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillSlash8014.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
from .SkillBase import SkillBase
from common.cfg import confmgr

class SkillSlash8014(SkillBase):

    def do_skill(self, *args):
        stage, ignore_water = args
        self._last_cast_time = tutil.get_time()
        return (
         stage,)