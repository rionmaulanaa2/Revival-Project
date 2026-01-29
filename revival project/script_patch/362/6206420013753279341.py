# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CArmRaceMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import battle_const

class CArmRaceMode:

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        global_data.armrace_battle_data.finalize()

    def init_parameters(self):
        self.game_over = False

    def init_mgr(self):
        self.init_armrace_data_mgr()

    def init_armrace_data_mgr(self):
        from logic.comsys.battle.ArmRace.ArmRaceBattleData import ArmRaceBattleData
        ArmRaceBattleData()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('ArmRaceScoreUI')
        global_data.ui_mgr.close_ui('ArmRaceScoreDetailsUI')
        global_data.ui_mgr.close_ui('ArmRaceFinishCountDown')
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('ArmRaceBeginCountDown')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_init_mecha_ui': self._hide_mecha_ui,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'settle_stage_event': self.on_settle_stage,
           'target_revive_event': self.recover_death_cam
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _hide_mecha_ui(self):
        global_data.ui_mgr.hide_ui('MechaUI')

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            self.create_armrace_ready_ui()
        elif stage == parachute_utils.STAGE_LAND:
            self.create_armrace_ui()

    def create_armrace_ui(self):
        if self.game_over:
            return
        global_data.ui_mgr.show_ui('ArmRaceScoreUI', 'logic.comsys.battle.ArmRace')
        global_data.ui_mgr.show_ui('ArmRaceWeaponBarSelectUI', 'logic.comsys.battle.ArmRace')
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')

    def create_armrace_ready_ui(self):
        revive_time = BattleUtils.get_prepare_left_time()
        ui = global_data.ui_mgr.show_ui('ArmRaceBeginCountDown', 'logic.comsys.battle.ArmRace')
        ui.on_delay_close(revive_time)
        inst = global_data.ui_mgr.show_ui('ArmRaceStartUI', 'logic.comsys.battle.ArmRace')

    def _on_scene_observed_player_setted(self, ltarget):
        if not ltarget:
            return
        self.recover_death_cam()

    def on_settle_stage(self, *args):
        self.game_over = True
        self.recover_death_cam()

    def on_target_defeated(self, revive_time, killer_id, kill_info):
        if self.game_over:
            return
        reply_data = kill_info.get('reply_data', {})
        ui = global_data.ui_mgr.show_ui('DeathBeginCountDown', 'logic.comsys.battle.Death')
        ui.on_delay_close(revive_time)
        ui = global_data.ui_mgr.show_ui('DeathPlayBackUI', 'logic.comsys.battle.Death')
        ui.set_play_back_info(reply_data)
        ui.set_revive_time(revive_time)
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('S_ATTR_SET', 'death_mode_leave_base_firstly', True)

    def recover_death_cam(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
            global_data.cam_lplayer.send_event('E_CAM_PITCH', 0)
            global_data.emgr.fireEvent('camera_set_pitch_event', 0)
        global_data.ui_mgr.close_ui('DeathPlayBackUI')