# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CHumanDeathMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from logic.gcommon.cdata.mecha_status_config import MC_SHOOT, MC_AIM_SHOOT
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock

class CHumanDeathMode(CDeathMode):

    def __init__(self, map_id):
        super(CHumanDeathMode, self).__init__(map_id)
        self.init_singleton()

    def init_death_data_mgr(self):
        from logic.comsys.battle.Death.HumanDeathBattleData import HumanDeathBattleData
        HumanDeathBattleData()

    def init_singleton(self):
        from logic.comsys.battle.survival.SurvivalBattleData import SurvivalBattleData
        SurvivalBattleData()

    def on_train_loaded(self, *args):
        if not global_data.ui_mgr.get_ui('TrainProgUI'):
            global_data.ui_mgr.show_ui('TrainProgUI', 'logic.comsys.battle.survival')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'loading_end_event': self.on_loading_end,
           'target_revive_event': self.on_target_revive,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'on_train_loaded': self.on_train_loaded
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy_ui(self):
        super(CHumanDeathMode, self).destroy_ui()
        global_data.ui_mgr.close_ui('TrainProgUI')