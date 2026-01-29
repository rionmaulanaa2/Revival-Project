# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CDeathMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id

class CDeathMode(object):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.death_battle_data.finalize()
        if self.ui_init_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.ui_init_timer_id)
            self.ui_init_timer_id = None
        return

    def init_parameters(self):
        self.game_over = False
        self.is_revive_over = True
        self.ui_init_timer_id = None
        return

    def init_mgr(self):
        self.init_death_data_mgr()

    def init_death_data_mgr(self):
        from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
        DeathBattleData()
        from logic.comsys.battle.Gravity.GravitySurvivalBattleMgr import GravitySurvivalBattleMgr
        GravitySurvivalBattleMgr()

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
        global_data.ui_mgr.close_ui('RogueChooseBtnUI')
        global_data.ui_mgr.close_ui('DeathEnemyBaseUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'loading_end_event': self.on_loading_end,
           'target_revive_event': self.on_target_revive,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

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

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            global_data.death_battle_data.is_ready_state = True
            self.create_death_ready_ui()
            self.on_player_check_rotate_init()
        elif stage == parachute_utils.STAGE_LAND:
            global_data.death_battle_data.is_ready_state = False
            self.create_death_ui()
            self.on_player_check_rotate_init()

    def create_death_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        global_data.ui_mgr.show_ui('DeathBloodBagUI', 'logic.comsys.battle.Death')
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
        if self.is_need_rogue_ui():
            global_data.ui_mgr.show_ui('RogueChooseBtnUI', 'logic.comsys.battle.Death')

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
            global_data.ui_mgr.show_ui('RogueChooseBtnUI', 'logic.comsys.battle.Death')

    def is_need_weapon_ui(self):
        if self.is_in_spectate_or_ob():
            return False
        player = global_data.cam_lplayer
        if not player or player.id != global_data.player.id:
            return False
        return True

    def is_need_rogue_ui(self):
        if self.is_in_spectate_or_ob():
            return False
        player = global_data.cam_lplayer
        if not player or player.id != global_data.player.id:
            return False
        return True

    def on_loading_end(self):
        pass

    def _on_scene_observed_player_setted(self, player):
        self.on_target_revive()

    def on_target_revive(self):
        self.is_revive_over = True
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
        global_data.ui_mgr.close_ui('DeathPlayBackUI')

    def rotate_to_look_at(self, lent, target_pos):
        if not lent:
            return
        lpos = lent.ev_g_position()
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = lent.ev_g_yaw() or 0
                global_data.emgr.fireEvent('camera_set_yaw_event', target_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)
                lent.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def on_player_check_rotate_init(self):
        if not self.is_revive_over:
            return
        self.is_revive_over = False
        if not self.is_in_spectate_or_ob():
            if global_data.player and global_data.player.logic and global_data.death_battle_data.area_id:
                born_data = global_data.game_mode.get_born_data()
                base_center_pos = born_data[global_data.death_battle_data.area_id].get('map_center')
                import math3d
                position = math3d.vector(*base_center_pos)
                self.rotate_to_look_at(global_data.player.logic, position)
            global_data.player.logic.send_event('E_DEATH_GUIDE_REVIVE')

    def on_settle_stage(self, *args):
        self.game_over = True

    def is_in_spectate_or_ob(self):
        if global_data.player and global_data.player.logic:
            from logic.gutils import judge_utils
            if global_data.player.logic.ev_g_is_in_spectate() or judge_utils.is_ob():
                return True
            else:
                return False

        return False

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('DeathTopScoreUI', 'logic.comsys.battle.Death')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('DeathTopScoreUI')
        global_data.ui_mgr.show_ui('DeathTopScoreUI', 'logic.comsys.battle.Death')