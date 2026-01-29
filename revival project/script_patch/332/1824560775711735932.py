# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CADCrystalMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from common.utils.timer import CLOCK
from logic.gcommon.common_const.battle_const import ROUND_STATUS_INTERVAL

class CADCrystalMode(CDeathMode):

    def init_death_data_mgr(self):
        from logic.comsys.battle.ADCrystal.ADCrystalBattleData import ADCrystalBattleData
        ADCrystalBattleData()

    def process_event(self, is_bind):
        super(CADCrystalMode, self).process_event(is_bind)
        if is_bind:
            global_data.emgr.battle_loading_finished_event += self.check_show_introduct_ui
            global_data.emgr.force_check_player_forward_event += self.force_check_player_forward
        else:
            global_data.emgr.battle_loading_finished_event -= self.check_show_introduct_ui
            global_data.emgr.force_check_player_forward_event -= self.force_check_player_forward

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('ADCrystalTopScoreUI', 'logic.comsys.battle.ADCrystal')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('ADCrystalTopScoreUI')
        global_data.ui_mgr.show_ui('ADCrystalTopScoreUI', 'logic.comsys.battle.ADCrystal')

    def check_show_introduct_ui(self):
        showed_intro = global_data.achi_mgr.get_cur_user_archive_data('showed_adcrystal_intro', 0)
        if not showed_intro:
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(None, 37)
            global_data.achi_mgr.set_cur_user_archive_data('showed_adcrystal_intro', 1)
        return

    def force_check_player_forward(self):
        if not self.is_in_spectate_or_ob():
            if global_data.player and global_data.player.logic:
                born_data = global_data.game_mode.get_born_data()
                base_center_pos = born_data[global_data.death_battle_data.area_id].get('map_center')
                import math3d
                position = math3d.vector(*base_center_pos)
                self.rotate_to_look_at(global_data.player.logic, position)

    def on_observer_parachute_stage_changed(self, stage):
        super(CADCrystalMode, self).on_observer_parachute_stage_changed(stage)
        battle = global_data.battle
        if not battle:
            return
        battle.show_interval_count_down()
        if battle.get_round_status() == ROUND_STATUS_INTERVAL:
            global_data.cam_lplayer and global_data.cam_lplayer.send_event('S_ATTR_SET', 'death_mode_leave_base_firstly', True)
        battle.exit_interval_view()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('DeathTopScoreUI')
        global_data.ui_mgr.close_ui('DeathScoreDetailsUI')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('DeathBloodBagUI')
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        global_data.ui_mgr.close_ui('ADCrystalRogueChooseBtnUI')
        global_data.ui_mgr.close_ui('DeathEnemyBaseUI')

    def create_death_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        global_data.ui_mgr.show_ui('DeathBloodBagUI', 'logic.comsys.battle.Death')
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('ADCrystalRogueChooseBtnUI', 'logic.comsys.battle.Death')

    def create_death_ready_ui(self):
        revive_time = BattleUtils.get_prepare_left_time()
        self._show_top_score_ui_in_ready()

        def end_callback():
            global_data.emgr.death_count_down_over.emit()
            global_data.emgr.death_begin_count_down_over.emit()

        ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
        ui.on_delay_close(revive_time, end_callback)
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
            global_data.ui_mgr.show_ui('DeathChooseWeaponUI', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('ADCrystalRogueChooseBtnUI', 'logic.comsys.battle.Death')