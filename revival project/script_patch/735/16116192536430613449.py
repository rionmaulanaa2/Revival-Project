# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CTrainMode.py
from __future__ import absolute_import
from logic.comsys.battle import BattleUtils
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle.Train.TrainBattleMgr import TrainBattleData
import math3d

class CTrainMode(CDeathMode):

    def init_parameters(self):
        super(CTrainMode, self).init_parameters()

    def on_target_revive(self):
        super(CTrainMode, self).on_target_revive()

    def process_event(self, is_bind):
        super(CTrainMode, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'battle_loading_finished_event': self.check_show_introduct_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_death_data_mgr(self):
        TrainBattleData()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('DeathBloodBagUI')
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        global_data.ui_mgr.close_ui('TrainRogueChooseBtnUI')
        global_data.ui_mgr.close_ui('TrainTopProgUI')
        global_data.ui_mgr.close_ui('TrainScoreDetailsUI')
        global_data.ui_mgr.close_ui('TrainSkillUI')
        global_data.ui_mgr.close_ui('TrainSkillSelectUI')
        global_data.ui_mgr.close_ui('TrainMarkUI')

    def on_observer_parachute_stage_changed(self, stage):
        super(CTrainMode, self).on_observer_parachute_stage_changed(stage)

    def create_death_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        global_data.ui_mgr.show_ui('DeathBloodBagUI', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('TrainRogueChooseBtnUI', 'logic.comsys.battle.Death')

    def create_death_ready_ui(self):
        revive_time = BattleUtils.get_prepare_left_time()

        def end_callback():
            global_data.emgr.death_count_down_over.emit()
            global_data.emgr.death_begin_count_down_over.emit()

        ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
        ui.on_delay_close(revive_time, end_callback)
        ui.set_start_show_time(5)
        ui.set_count_down_sound('Play_time_countdown')
        ui.set_time_need_ceil(True)
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('TrainRogueChooseBtnUI', 'logic.comsys.battle.Death')
        if not global_data.ui_mgr.get_ui('TrainTopProgUI'):
            global_data.ui_mgr.show_ui('TrainTopProgUI', 'logic.comsys.battle.Train')

    def _show_top_score_ui_after_ready(self):
        if not global_data.ui_mgr.get_ui('TrainSkillUI'):
            global_data.ui_mgr.show_ui('TrainSkillUI', 'logic.comsys.battle.Train')
        if not global_data.ui_mgr.get_ui('TrainMarkUI'):
            global_data.ui_mgr.show_ui('TrainMarkUI', 'logic.comsys.battle.Train')
        if not global_data.ui_mgr.get_ui('TrainTopProgUI'):
            global_data.ui_mgr.show_ui('TrainTopProgUI', 'logic.comsys.battle.Train')
        if not global_data.ui_mgr.get_ui('MechaUI') and not global_data.ui_mgr.get_ui('StateChangeUI'):
            global_data.ui_mgr.show_ui('MechaUI', 'logic.comsys.battle')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('TrainTopProgUI', 'logic.comsys.battle.Train')

    def on_player_check_rotate_init(self):
        if not self.is_revive_over:
            return
        self.is_revive_over = False
        if not self.is_in_spectate_or_ob():
            if global_data.cam_lplayer:
                position = global_data.train_battle_mgr.get_look_at_nearlist_station(global_data.cam_lplayer.ev_g_position())
                position = math3d.vector(*position)
                self.rotate_to_look_at(global_data.cam_lplayer, position)
            global_data.player.logic.send_event('E_DEATH_GUIDE_REVIVE')

    def check_show_introduct_ui(self):
        showed_intro = global_data.achi_mgr.get_cur_user_archive_data('showed_train_intro', 0)
        if not showed_intro:
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(None, 41)
            global_data.achi_mgr.set_cur_user_archive_data('showed_train_intro', 1)
        return