# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CGulagSurMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.comsys.battle.Gulag.GulagSurvivalBattleMgr import GulagSurvivalBattleMgr
from logic.vscene.parts.gamemode.CNormalMode import CNormalBase

class CGulagSurMode(CNormalBase):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def init_parameters(self):
        self.game_over = False
        self.revive_game_id = None
        self.revive_game_opponent_eid = None
        self.revive_game_queue_timestamp = 0
        return

    def init_mgr(self):
        super(CGulagSurMode, self).init_mgr()
        GulagSurvivalBattleMgr.finalize()
        GulagSurvivalBattleMgr()

    def on_train_loaded(self, *args):
        if not global_data.ui_mgr.get_ui('TrainProgUI'):
            global_data.ui_mgr.show_ui('TrainProgUI', 'logic.comsys.battle.survival')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_train_loaded': self.on_train_loaded,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'scene_observed_player_setted_event': self.on_enter_observed,
           'target_revive_event': self.on_target_revive
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_observer_parachute_stage_changed(self, stage):
        if stage == parachute_utils.STAGE_LAND:
            self.create_mode_specified_ui()

    def create_mode_specified_ui(self):
        if self.game_over:
            return
        global_data.ui_mgr.show_ui('GulagInfoUI', 'logic.comsys.battle.Gulag')
        if global_data.player:
            show_gulag_tip_name = 'GulagRuleTip' + str(global_data.player.uid)
            rule_tip_shown = global_data.achi_mgr.get_cur_user_archive_data(show_gulag_tip_name, False)
            if not rule_tip_shown:
                global_data.emgr.show_human_tips.emit(17981, 5)
                global_data.achi_mgr.set_cur_user_archive_data(show_gulag_tip_name, True)

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('GulagInfoUI')

    def on_finalize(self):
        super(CGulagSurMode, self).on_finalize()
        self.process_event(False)
        self.destroy_ui()
        global_data.gulag_sur_battle_mgr.finalize()

    def on_settle_stage(self, *args):
        self.game_over = True

    def is_in_spectate(self):
        if global_data.player and global_data.player.logic:
            if global_data.player.logic.ev_g_is_in_spectate():
                return True
            else:
                return False

        return False

    def on_enter_observed(self, spec_target):
        self.on_target_revive()

    def on_target_revive(self, *args):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')