# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Recruitment/RecruitmentSurvivalBattleMgr.py
from __future__ import absolute_import
from common.framework import Singleton

class RecruitmentSurvivalBattleMgr(Singleton):
    ALIAS_NAME = 'recruitment_survival_battle_mgr'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        pass

    def on_finalize(self):
        self.init_parameters()