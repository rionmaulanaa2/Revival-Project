# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CRecruitmentSurMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CNormalMode import CNormalBase

class CRecruitmentSurMode(CNormalBase):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def init_parameters(self):
        pass

    def init_mgr(self):
        super(CRecruitmentSurMode, self).init_mgr()
        from logic.comsys.battle.Recruitment.RecruitmentSurvivalBattleMgr import RecruitmentSurvivalBattleMgr
        RecruitmentSurvivalBattleMgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy_ui(self):
        pass

    def on_finalize(self):
        super(CRecruitmentSurMode, self).on_finalize()
        self.process_event(False)
        self.destroy_ui()
        global_data.recruitment_survival_battle_mgr.finalize()