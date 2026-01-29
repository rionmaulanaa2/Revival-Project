# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CAssaultMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id

class CAssaultMode(CDeathMode):

    def __init__(self, map_id):
        super(CAssaultMode, self).__init__(map_id)
        self.show_rules = False
        global_data.emgr.show_hang_up_event += self.on_show_hang_up

    def on_finalize(self):
        super(CAssaultMode, self).on_finalize()
        global_data.emgr.show_hang_up_event -= self.on_show_hang_up

    def destroy_ui(self):
        super(CAssaultMode, self).destroy_ui()
        global_data.ui_mgr.close_ui('AssaultRankUI')
        global_data.ui_mgr.close_ui('AssaultRoomCloseTipsUI')
        global_data.ui_mgr.close_ui('NormalConfirmUI2')

    def on_loading_end(self):
        super(CAssaultMode, self).on_loading_end()
        global_data.battle and global_data.battle.show_battle_start_tips()
        if global_data.player and global_data.player.logic:
            global_data.battle and global_data.battle.call_soul_method('on_loading_succeed', (global_data.player.logic.id,))

    def create_death_ui(self):
        super(CAssaultMode, self).create_death_ui()
        if global_data.battle and global_data.battle.is_settle:
            return
        global_data.ui_mgr.show_ui('AssaultRoomCloseTipsUI', 'logic.comsys.battle.Assault')
        ui = global_data.ui_mgr.show_ui('AssaultRankUI', 'logic.comsys.battle.Assault')
        if global_data.battle and global_data.cam_lplayer and not self.show_rules:
            ui.show_rule_info()
            self.show_rules = True
        else:
            ui.show_rank_info()

    def create_death_ready_ui(self):
        if global_data.battle and global_data.battle.is_settle:
            return
        revive_time = BattleUtils.get_prepare_left_time()
        self._show_top_score_ui_in_ready()
        ui = global_data.ui_mgr.show_ui('AssaultRankUI', 'logic.comsys.battle.Assault')
        ui.show_rule_info()

        def end_callback():
            global_data.emgr.death_count_down_over.emit()
            global_data.emgr.death_begin_count_down_over.emit()

        ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
        ui.on_delay_close(revive_time, end_callback)
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
            global_data.ui_mgr.show_ui('DeathChooseWeaponUI', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('RogueChooseBtnUI', 'logic.comsys.battle.Death')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('AssaultTopScoreUI', 'logic.comsys.battle.Assault')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('AssaultTopScoreUI')
        global_data.ui_mgr.show_ui('AssaultTopScoreUI', 'logic.comsys.battle.Assault')

    def on_show_hang_up(self):
        if self.game_over:
            global_data.ui_mgr.close_ui('NormalConfirmUI2')
            return
        NormalConfirmUI2(content=get_text_by_id(18367))