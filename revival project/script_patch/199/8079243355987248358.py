# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CGranhackSurMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.vscene.parts.gamemode.CNormalMode import CNormalBase

class CGranhackSurMode(CNormalBase):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def init_parameters(self):
        pass

    def init_mgr(self):
        super(CGranhackSurMode, self).init_mgr()
        from logic.comsys.battle.Granbelm.GranbelmSurvivalBattleMgr import GranbelmSurvivalBattleMgr
        GranbelmSurvivalBattleMgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_observer_parachute_stage_changed(self, stage):
        if stage == parachute_utils.STAGE_LAND:
            self.create_gran_sur_ui()

    def create_gran_sur_ui(self):
        global_data.ui_mgr.show_ui('GranhackRuneConfUI', 'logic.comsys.battle.Granbelm')

    def destroy_ui(self):
        close_ui_list = ('GranhackConfUI', 'GranhackListUI')
        for ui in close_ui_list:
            global_data.ui_mgr.close_ui(ui)

    def on_finalize(self):
        super(CGranhackSurMode, self).on_finalize()
        self.process_event(False)
        self.destroy_ui()
        global_data.gran_sur_battle_mgr.finalize()