# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/COccupyMode.py
from __future__ import absolute_import
from logic.comsys.battle import BattleUtils
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode

class COccupyMode(CDeathMode):

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.death_battle_data.finalize()

    def init_mgr(self):
        self.init_occupy_data_mgr()

    def init_occupy_data_mgr(self):
        from logic.comsys.battle.Occupy.OccupyData import OccupyData
        OccupyData()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('OccupyBattleUI')
        global_data.ui_mgr.close_ui('OccupyScoreDetailsUI')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('OccupyProgressUI')
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        global_data.ui_mgr.close_ui('RogueChooseBtnUI')

    def create_death_ui(self):
        super(COccupyMode, self).create_death_ui()
        if self.game_over:
            return
        global_data.ui_mgr.show_ui('OccupyProgressUI', 'logic.comsys.battle.Occupy')

    def create_death_ready_ui(self):
        super(COccupyMode, self).create_death_ready_ui()
        revive_time = BattleUtils.get_prepare_left_time()
        if revive_time > 0:
            from logic.gcommon.common_const.battle_const import UP_NODE_COMMON_RIKO_TIPS
            message_data = {'content_txt': get_text_by_id(8219),'delay_time': 10,'template_scale': [1, 1]}
            global_data.emgr.battle_event_message.emit(message_data, message_type=UP_NODE_COMMON_RIKO_TIPS)

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('OccupyBattleUI', 'logic.comsys.battle.Occupy')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('OccupyBattleUI')
        global_data.ui_mgr.show_ui('OccupyBattleUI', 'logic.comsys.battle.Occupy')