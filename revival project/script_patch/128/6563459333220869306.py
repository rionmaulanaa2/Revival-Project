# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CHuntingMode.py
from __future__ import absolute_import
from __future__ import print_function
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle import BattleUtils
from logic.gcommon.common_utils import parachute_utils
from mobile.common.EntityManager import EntityManager

class CHuntingMode(CDeathMode):

    def __init__(self, map_id):
        super(CHuntingMode, self).__init__(map_id)
        self.init_singleton()
        self._block_ui_record = None
        self._block_hot_key_record = None
        return

    def init_death_data_mgr(self):
        from logic.comsys.battle.Hunting.HuntingBattleData import HuntingBattleData
        HuntingBattleData()

    def init_singleton(self):
        from logic.comsys.battle.survival.SurvivalBattleData import SurvivalBattleData
        SurvivalBattleData()

    def on_finalize(self):
        super(CHuntingMode, self).on_finalize()
        self.set_block_control(True)
        self.clear_current_block()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'loading_end_event': self.on_loading_end,
           'target_revive_event': self.on_target_revive,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'on_observer_global_join_mecha_start': self.on_observer_join_mecha_start,
           'on_observer_global_leave_mecha_start': self.on_observer_leave_mecha_start,
           'on_observer_global_killer_camera': self.on_observer_killer_camera,
           'on_observer_global_join_mecha': self.on_observer_join_mecha,
           'playback_mecha_destroyed': self.on_mecha_destroyed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_observer_join_mecha_start(self, *args, **kwargs):
        group_id = global_data.battle.get_cur_target_group_id()
        if group_id is not None:
            if not global_data.battle.is_mecha_group(group_id):
                return
        self.cam_enable(True)
        self.recover_death_cam()
        return

    def on_observer_leave_mecha_start(self, *args, **kwargs):
        group_id = global_data.battle.get_cur_target_group_id()
        if group_id is not None:
            if not global_data.battle.is_mecha_group(group_id):
                return
        self.cam_enable(False)
        return

    def on_observer_killer_camera(self, *args, **kwargs):
        self.cam_enable(False)

    def on_target_revive(self):
        self.cam_enable(True)
        super(CHuntingMode, self).on_target_revive()

    def on_observer_join_mecha(self, *args, **kargs):
        if global_data.cam_lplayer:
            mecha_entity_id = global_data.cam_lplayer.ev_g_ctrl_mecha()
            mecha_entity = EntityManager.getentity(mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                new_yaw = mecha_entity.logic.ev_g_yaw()
                global_data.emgr.fireEvent('camera_set_yaw_event', new_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)

    def on_mecha_destroyed(self, killer_info, revive_time):
        self.on_target_defeated(revive_time, killer_id=None, kill_info=killer_info)
        return

    def recover_death_cam(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
        global_data.ui_mgr.close_ui('DeathPlayBackUI')

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

    def on_mecha_group_hide_ui(self):
        self.clear_current_block()
        PURE_MECHA_HIDE_UI = ('StateChangeUI', 'StateChangeUIPC', 'MechaUI', 'WeaponBarSelectUI',
                              'PostureControlUI', 'FireRockerUI', 'FightLeftShotUI',
                              'BulletReloadUI', 'HpInfoUI')
        tag = 'hunting_battle_mecha'
        global_data.ui_mgr.add_blocking_ui_list(PURE_MECHA_HIDE_UI, tag)
        self._block_ui_record = (PURE_MECHA_HIDE_UI, tag)
        pc_key_block_list = global_data.game_mode.get_cfg_data('play_data').get('mecha_pc_key_block_list', [])
        if global_data.pc_ctrl_mgr:
            for hotkey_name in pc_key_block_list:
                global_data.pc_ctrl_mgr.block_hotkey(hotkey_name, tag)

            self._block_hot_key_record = (
             pc_key_block_list, tag)

    def on_human_group_hide_ui(self):
        self.clear_current_block()
        PURE_HUMAN_HIDE_UI = ('StateChangeUI', 'StateChangeUIPC', 'MechaUI', 'MechaUIPC',
                              'AttachableDriveUI')
        tag = 'hunting_battle_human'
        global_data.ui_mgr.add_blocking_ui_list(PURE_HUMAN_HIDE_UI, tag)
        self._block_ui_record = (PURE_HUMAN_HIDE_UI, tag)
        pc_key_block_list = global_data.game_mode.get_cfg_data('play_data').get('human_pc_key_block_list', [])
        if global_data.pc_ctrl_mgr:
            for hotkey_name in pc_key_block_list:
                global_data.pc_ctrl_mgr.block_hotkey(hotkey_name, tag)

            self._block_hot_key_record = (
             pc_key_block_list, tag)

    def clear_current_block(self):
        if self._block_ui_record:
            global_data.ui_mgr.remove_blocking_ui_list(self._block_ui_record[0], self._block_ui_record[1])
            self._block_ui_record = None
        if self._block_hot_key_record:
            if global_data.pc_ctrl_mgr:
                for hotkey_name in self._block_hot_key_record[0]:
                    global_data.pc_ctrl_mgr.unblock_hotkey(hotkey_name, self._block_hot_key_record[1])

                self._block_hot_key_record = None
        return

    def on_observer_parachute_stage_changed(self, stage):
        super(CHuntingMode, self).on_observer_parachute_stage_changed(stage)
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            self.set_block_control(False)
        elif stage == parachute_utils.STAGE_LAND:
            self.set_block_control(True)
        group_id = global_data.battle.get_cur_target_group_id()
        print('target group_id ,mecha_group_id', group_id, global_data.battle.mecha_group_id)
        if group_id is not None:
            if not global_data.battle.is_mecha_group(group_id):
                self.on_human_group_hide_ui()
            else:
                self.on_mecha_group_hide_ui()
        return

    def set_block_control(self, vis):
        from data import hot_key_def
        pc_key_block_list = [hot_key_def.MECHA_FIRE,
         hot_key_def.MECHA_SUB,
         hot_key_def.MECHA_RUSH,
         hot_key_def.MECHA_JUMP,
         hot_key_def.MECHA_EXTRA_SKILL,
         hot_key_def.FIRST_SP_MODULE_SKILL,
         hot_key_def.SECOND_SP_MODULE_SKILL,
         hot_key_def.MECHA_SPECIAL_SKILL,
         hot_key_def.MECHA_AIM]
        if global_data.pc_ctrl_mgr:
            for hotkey_name in pc_key_block_list:
                if not vis:
                    global_data.pc_ctrl_mgr.block_hotkey(hotkey_name, 'HUNTING_BLOCK')
                else:
                    global_data.pc_ctrl_mgr.unblock_hotkey(hotkey_name, 'HUNTING_BLOCK')

        READY_HIDE_UI = ('FireRockerUI', 'MechaControlMain', 'MechaControlMainPC')
        tag = 'hunting_battle'
        if not vis:
            global_data.ui_mgr.add_blocking_ui_list(READY_HIDE_UI, tag)
        else:
            global_data.ui_mgr.remove_blocking_ui_list(READY_HIDE_UI, tag)

    def create_death_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')

    def create_death_ready_ui(self):
        revive_time = BattleUtils.get_prepare_left_time()
        self._show_top_score_ui_in_ready()

        def end_callback():
            global_data.emgr.death_count_down_over.emit()

        ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
        ui.on_delay_close(revive_time, end_callback)

    def destroy_ui(self):
        super(CHuntingMode, self).destroy_ui()
        global_data.ui_mgr.close_ui('HuntingLoadingVsUI')
        global_data.ui_mgr.close_ui('EntityHeadMarkUI')

    def _on_scene_observed_player_setted(self, player):
        super(CHuntingMode, self)._on_scene_observed_player_setted(player)
        observe_player = global_data.cam_lplayer
        if observe_player:
            if global_data.battle.is_mecha_group(observe_player.ev_g_group_id()):
                global_data.death_battle_data.update_ui_high_damage_ids(global_data.death_battle_data.high_damage_entity_ids)
            else:
                global_data.death_battle_data.update_ui_high_damage_ids([])