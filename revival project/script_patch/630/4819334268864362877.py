# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillTrioFirepower.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from logic.gcommon.common_const.skill_const import MP_SYNC_STAGE_BEGIN_RECOVER

class SkillTrioFirepower(SkillCd):

    def on_add(self):
        need_recover = self._unit_obj.ev_g_reconnect_skill_need_recover()
        if self._mp < self._max_mp and need_recover:
            self._mp_stage = MP_SYNC_STAGE_BEGIN_RECOVER
        else:
            self._mp_stage = 0
        self._tell_ui_at_once = False