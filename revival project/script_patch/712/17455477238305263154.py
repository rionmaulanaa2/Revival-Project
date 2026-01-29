# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CGVGMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
from logic.client.const import game_mode_const

class CGVGMode:

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.gvg_battle_data.finalize()

    def init_parameters(self):
        self.game_over = False

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('GVGTopScoreUI')
        global_data.ui_mgr.close_ui('GVGTopScoreJudgeUI')
        global_data.ui_mgr.close_ui('GVGScoreDetailsUI')
        global_data.ui_mgr.close_ui('GVGScoreMsgUI')

    def init_mgr(self):
        self.init_gvg_data_mgr()

    def init_gvg_data_mgr(self):
        from logic.comsys.battle.gvg.GVGBattleData import GVGBattleData
        GVGBattleData()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'on_observer_global_join_mecha': self.on_observer_join_mecha,
           'on_player_global_leave_mecha': self.on_player_leave_mecha,
           'on_observer_global_join_mecha_start': self.on_observer_join_mecha_start,
           'on_observer_global_leave_mecha_start': self.on_observer_leave_mecha_start,
           'on_observer_global_killer_camera': self.on_observer_killer_camera,
           'loading_end_event': self.on_loading_end,
           'gvg_mecha_destroyed': self.on_mecha_destroyed,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self.update_observed,
           'battle_change_prepare_timestamp': self.change_prepare_timestamp
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_duel_begin_tips(self):
        if global_data.battle:
            global_data.battle.show_round_begin_tip()

    def count_close_cb(self):
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            self.show_duel_begin_tips()

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            self.create_gvg_ready_ui()
        elif stage == parachute_utils.STAGE_LAND:
            self.create_gvg_ui()

    def change_prepare_timestamp(self):
        revive_time = self.get_count_down_time()
        if revive_time < 0 and global_data.is_judge_ob:
            return
        ui = global_data.ui_mgr.get_ui('FFABeginCountDown')
        ui and ui.on_delay_close(revive_time, self.count_close_cb)

    def get_count_down_time(self):
        diff = 0
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            if global_data.battle:
                diff = global_data.battle.ui_start_diff_time
            return BattleUtils.get_prepare_left_time() + diff
        else:
            return BattleUtils.get_prepare_left_time()

    def create_gvg_ready_ui(self):
        revive_time = self.get_count_down_time()

        def show_count_down():
            ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                ui.set_context('DUEL')
                ui.on_delay_close(revive_time, self.count_close_cb)
            else:
                ui.set_context('GVG')
                ui.on_delay_close(revive_time, self.count_close_cb)

        if not global_data.is_judge_ob:
            if revive_time >= 0:
                show_count_down()
        elif revive_time >= 0:
            ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                ui.set_context('DUEL')
                ui.on_delay_close(revive_time, self.count_close_cb)
            else:
                ui.set_context('GVG')
                ui.on_delay_close(revive_time, self.count_close_cb)
        if not global_data.is_judge_ob:
            ui = global_data.ui_mgr.show_ui('GVGTopScoreUI', 'logic.comsys.battle.gvg')
            ui and ui.show_count_down(False)
        else:
            ui = global_data.ui_mgr.show_ui('GVGTopScoreJudgeUI', 'logic.comsys.battle.gvg')
            ui and ui.show_count_down(False)

    def create_gvg_ui(self):
        if self.game_over:
            return
        if not global_data.is_judge_ob:
            ui = global_data.ui_mgr.show_ui('GVGTopScoreUI', 'logic.comsys.battle.gvg')
            ui and ui.show_count_down(True)
        else:
            ui = global_data.ui_mgr.show_ui('GVGTopScoreJudgeUI', 'logic.comsys.battle.gvg')
            ui and ui.show_count_down(True)
        global_data.ui_mgr.show_ui('GVGScoreMsgUI', 'logic.comsys.battle.gvg')

    def on_observer_join_mecha(self, *args, **kargs):
        if global_data.cam_lplayer:
            mecha_entity_id = global_data.cam_lplayer.ev_g_ctrl_mecha()
            mecha_entity = EntityManager.getentity(mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                new_yaw = mecha_entity.logic.ev_g_yaw()
                global_data.emgr.fireEvent('camera_set_yaw_event', new_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)

    def update_observed(self, ltarget):
        if not ltarget:
            return
        self.cam_enable(True)
        if global_data.is_judge_ob:
            if global_data.cam_lplayer:
                self.on_observer_parachute_stage_changed(global_data.cam_lplayer.ev_g_parachute_stage())

    def cam_enable(self, enable):
        if enable:
            global_data.emgr.camera_lock_enable_follow_event.emit(False)
            global_data.emgr.camera_enable_follow_event.emit(True)
        else:
            global_data.emgr.camera_lock_enable_follow_event.emit(False)
            global_data.emgr.camera_enable_follow_event.emit(False)
            global_data.emgr.camera_lock_enable_follow_event.emit(True)
        global_data.emgr.camera_added_trk_enable.emit(enable)
        global_data.emgr.switch_cam_state_enable_event.emit(enable)

    def on_player_leave_mecha(self, *args, **kargs):
        if global_data.gvg_battle_data:
            global_data.gvg_battle_data.player_req_spectate()

    def on_observer_join_mecha_start(self, *args, **kargs):
        self.cam_enable(True)
        self.recover_death_cam()

    def on_observer_leave_mecha_start(self, *args, **kargs):
        self.cam_enable(False)

    def on_observer_killer_camera(self, *args, **kargs):
        self.cam_enable(False)

    def on_loading_end(self):
        pass

    def recover_death_cam(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
        global_data.ui_mgr.close_ui('DeathPlayBackUI')

    def on_settle_stage(self, *args, **kargs):
        self.game_over = True
        self.recover_death_cam()

    def on_mecha_destroyed(self, soul_id, mecha_idx, killer_info, mecha_revice_ts):
        if self.game_over:
            return
        if global_data.cam_lplayer and global_data.cam_lplayer.id == soul_id:
            if global_data.gvg_battle_data.somebody_is_over(soul_id):
                self.recover_death_cam()
                return
            reply_data = killer_info.get('reply_data', {})
            mecha_id = self.get_mecha_choose_dict().get(soul_id, {}).get(mecha_idx + 1)
            killer_info = reply_data.get('killer_info', {})
            if killer_info:
                killer_info['destroyed_mecha_id'] = mecha_id
            ui = global_data.ui_mgr.show_ui('DeathBeginCountDown', 'logic.comsys.battle.Death')
            revive_time = self.get_revive_time(mecha_revice_ts)
            ui.on_delay_close(revive_time)
            ui = global_data.ui_mgr.show_ui('DeathPlayBackUI', 'logic.comsys.battle.Death')
            ui.set_revive_time(revive_time)
            ui.set_play_back_info(reply_data)

    def get_mecha_choose_dict(self):
        return global_data.battle.mecha_choose_dict or {}

    def get_revive_time(self, mecha_revice_ts):
        revive_time = mecha_revice_ts - time_utility.time()
        return revive_time