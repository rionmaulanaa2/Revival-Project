# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CFFAMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.EntityManager import EntityManager

class CFFAMode:

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.ffa_battle_data.finalize()

    def init_parameters(self):
        self.game_over = False

    def init_mgr(self):
        self.init_ffa_data_mgr()

    def init_ffa_data_mgr(self):
        from logic.comsys.battle.ffa.FFABattleData import FFABattleData
        FFABattleData()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('FFAScoreUI')
        global_data.ui_mgr.close_ui('FFAScoreDetailsUI')
        global_data.ui_mgr.close_ui('FFAFinishCountDown')
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_observer_global_join_mecha_start': self.on_observer_join_mecha_start,
           'on_observer_global_join_mecha': self.on_observer_join_mecha,
           'on_observer_global_leave_mecha_start': self.on_observer_leave_mecha_start,
           'on_observer_global_killer_camera': self.on_observer_killer_camera,
           'ffa_mecha_destroyed': self.on_mecha_destroyed,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'settle_stage_event': self.on_settle_stage
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            self.create_ffa_ready_ui()
        elif stage == parachute_utils.STAGE_LAND:
            self.create_ffa_ui()

    def create_ffa_ui(self):
        if self.game_over:
            return
        global_data.ui_mgr.show_ui('FFAScoreUI', 'logic.comsys.battle.ffa')
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        if global_data.battle:
            global_data.battle.init_rechoose_mecha_ui()

    def create_ffa_ready_ui(self):
        revive_time = BattleUtils.get_prepare_left_time()
        ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
        ui.on_delay_close(revive_time)

    def _on_scene_observed_player_setted(self, ltarget):
        if not ltarget:
            return
        self.recover_death_cam()

    def on_settle_stage(self, *args):
        self.game_over = True
        self.recover_death_cam()

    def on_observer_join_mecha_start(self, *args, **kargs):
        self.cam_enable(True)
        self.recover_death_cam()

    def on_observer_join_mecha(self, *args, **kargs):
        if global_data.cam_lplayer:
            mecha_entity_id = global_data.cam_lplayer.ev_g_ctrl_mecha()
            mecha_entity = EntityManager.getentity(mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                new_yaw = mecha_entity.logic.ev_g_yaw()
                global_data.emgr.fireEvent('camera_set_yaw_event', new_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)

    def on_observer_leave_mecha_start(self, *args, **kwargs):
        self.cam_enable(False)

    def on_observer_killer_camera(self, *args, **kwargs):
        self.cam_enable(False)

    def on_mecha_destroyed(self, killer_info, revive_time):
        if self.game_over:
            return
        reply_data = killer_info.get('reply_data', {})
        ui = global_data.ui_mgr.show_ui('DeathBeginCountDown', 'logic.comsys.battle.Death')
        ui.on_delay_close(revive_time)
        ui = global_data.ui_mgr.show_ui('MechaDeathPlayBackUI', 'logic.comsys.battle.MechaDeath')
        ui.set_play_back_info(reply_data)

    def recover_death_cam(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    def cam_enable(self, is_enable):
        if is_enable:
            global_data.emgr.camera_lock_enable_follow_event.emit(False)
            global_data.emgr.camera_enable_follow_event.emit(True)
        else:
            global_data.emgr.camera_lock_enable_follow_event.emit(False)
            global_data.emgr.camera_enable_follow_event.emit(False)
            global_data.emgr.camera_lock_enable_follow_event.emit(True)
        global_data.emgr.camera_added_trk_enable.emit(is_enable)
        global_data.emgr.switch_cam_state_enable_event.emit(is_enable)