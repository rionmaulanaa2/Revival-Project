# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CFlagMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from logic.gcommon.cdata.mecha_status_config import MC_SHOOT, MC_AIM_SHOOT
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from logic.gcommon.common_utils import parachute_utils

class CFlagMode(CDeathMode):

    def __init__(self, map_id):
        super(CFlagMode, self).__init__(map_id)

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('FlagTopScoreUI')
        global_data.ui_mgr.close_ui('FlagScoreDetailsUI')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        global_data.ui_mgr.close_ui('RogueChooseBtnUI')
        global_data.ui_mgr.close_ui('FlagMarkUI')
        global_data.ui_mgr.close_ui('FlagThrowUI')

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            global_data.death_battle_data.is_ready_state = True
            self.create_death_ready_ui()
            self.on_player_check_rotate_init()
        elif stage == parachute_utils.STAGE_LAND:
            global_data.death_battle_data.is_ready_state = False
            self.create_flag_ui()
            self.on_player_check_rotate_init()

    def create_flag_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        self._show_drop_flag_ui()
        self._show_flag_base_ui()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        if not self.is_in_spectate_or_ob():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('RogueChooseBtnUI', 'logic.comsys.battle.Death')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('FlagTopScoreUI', 'logic.comsys.battle.Flag')

    def _show_top_score_ui_after_ready(self):
        if global_data.ui_mgr.get_ui('FlagTopScoreUI') is None:
            global_data.ui_mgr.show_ui('FlagTopScoreUI', 'logic.comsys.battle.Flag')
        return

    def _show_drop_flag_ui(self):
        global_data.ui_mgr.show_ui('FlagThrowUI', 'logic.comsys.battle.Flag')

    def init_death_data_mgr(self):
        from logic.comsys.battle.Flag.FlagBattleData import FlagBattleData
        FlagBattleData()

    def _show_flag_base_ui(self):
        global_data.ui_mgr.show_ui('FlagMarkUI', 'logic.comsys.battle.Flag')