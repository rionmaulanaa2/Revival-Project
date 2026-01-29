# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CCrystalMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from common.utils.timer import CLOCK

class CCrystalMode(CDeathMode):

    def init_parameters(self):
        super(CCrystalMode, self).init_parameters()

    def on_finalize(self):
        super(CCrystalMode, self).on_finalize()

    def destroy_ui(self):
        super(CCrystalMode, self).destroy_ui()

    def init_death_data_mgr(self):
        from logic.comsys.battle.Crystal.CrystalBattleData import CrystalBattleData
        CrystalBattleData()

    def create_death_ready_ui(self):
        self._create_crystal_hint_ui()
        super(CCrystalMode, self).create_death_ready_ui()

    def create_death_ui(self):
        super(CCrystalMode, self).create_death_ui()
        self._create_crystal_hint_ui()

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('CrystalTopScoreUI')
        global_data.ui_mgr.show_ui('CrystalTopScoreUI', 'logic.comsys.battle.Crystal')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('CrystalTopScoreUI', 'logic.comsys.battle.Crystal')

    def _create_crystal_hint_ui(self):
        global_data.ui_mgr.show_ui('CrystalBattleHintUI', 'logic.comsys.battle.Crystal')

    def clear_close_mark_ui_timer(self):
        if self.close_mark_ui_timer:
            global_data.game_mgr.unregister_logic_timer(self.close_mark_ui_timer)
            self.close_mark_ui_timer = None
        return