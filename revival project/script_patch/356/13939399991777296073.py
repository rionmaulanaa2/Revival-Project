# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CCrownMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from logic.gcommon.cdata.mecha_status_config import MC_SHOOT, MC_AIM_SHOOT
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from logic.gcommon.common_utils import parachute_utils
from logic.comsys.battle.Crown.CrownGuideUI import CrownGuideUI

class CCrownMode(CDeathMode):

    def __init__(self, map_id):
        super(CCrownMode, self).__init__(map_id)
        self.init_crown_ui()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('CrownTopScoreUI')
        global_data.ui_mgr.close_ui('DeathScoreDetailsUI')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('CrownMarkUI')
        global_data.ui_mgr.close_ui('CrownTopCounterUI')
        global_data.ui_mgr.close_ui('CrownGuideUI')
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        global_data.ui_mgr.close_ui('RogueChooseBtnUI')

    def init_death_data_mgr(self):
        from logic.comsys.battle.Crown.CrownBattleData import CrownBattleData
        CrownBattleData()

    def init_crown_ui(self):
        global_data.ui_mgr.close_ui('CrownMarkUI')
        global_data.ui_mgr.show_ui('CrownMarkUI', 'logic.comsys.battle.Crown')
        global_data.ui_mgr.close_ui('CrownTopCounterUI')
        global_data.ui_mgr.show_ui('CrownTopCounterUI', 'logic.comsys.battle.Crown')

    def on_observer_parachute_stage_changed(self, stage):
        super(CCrownMode, self).on_observer_parachute_stage_changed(stage)
        if global_data.ui_mgr.get_ui('CrownTopCounterUI') is None:
            global_data.ui_mgr.show_ui('CrownTopCounterUI', 'logic.comsys.battle.Crown')
        if global_data.ui_mgr.get_ui('CrownMarkUI') is None:
            global_data.ui_mgr.show_ui('CrownMarkUI', 'logic.comsys.battle.Crown')
        if global_data.ui_mgr.get_ui('CrownGuideUI') is None:
            if global_data.player:
                show_crown_guide_name = 'CrownGuideUI' + str(global_data.player.uid)
                show_guide_ui = global_data.achi_mgr.get_cur_user_archive_data(show_crown_guide_name, False)
                if not show_guide_ui:
                    guide_ui = global_data.ui_mgr.show_ui('CrownGuideUI', 'logic.comsys.battle.Crown')
        return

    def _show_top_score_ui_in_ready(self):
        pass

    def _show_top_score_ui_after_ready(self):
        if global_data.ui_mgr.get_ui('CrownTopScoreUI') is None:
            global_data.ui_mgr.show_ui('CrownTopScoreUI', 'logic.comsys.battle.Crown')
        return