# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CSnatchEggMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.comsys.battle import BattleUtils

class CSnatchEggMode(object):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)
        self.init_singleton()

    def init_parameters(self):
        self.game_over = False
        self.is_revive_over = True

    def init_mgr(self):
        pass

    def init_singleton(self):
        from logic.comsys.battle.SnatchEgg.SnatchEggData import SnatchEggData
        SnatchEggData()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'target_revive_event': self.on_target_revive,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'scene_observed_player_setted_event': self.on_enter_observed,
           'battle_loading_finished_event': self.check_show_introduct_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            global_data.death_battle_data.is_ready_state = True
            self.create_snatchegg_ready_ui()
            self.on_player_check_rotate_init()
        elif stage == parachute_utils.STAGE_LAND:
            global_data.death_battle_data.is_ready_state = False
            self.create_snatchegg_ui()
            self.create_egg_ui()
        if global_data.ui_mgr.get_ui('SnatchEggGuideUI') is None:
            if global_data.player:
                guide_ui = global_data.ui_mgr.show_ui('SnatchEggGuideUI', 'logic.comsys.battle.SnatchEgg')
        return

    def check_show_introduct_ui(self):
        showed_intro = global_data.achi_mgr.get_cur_user_archive_data('showed_egg_intro', 0)
        if not showed_intro:
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(None, 48)
            global_data.achi_mgr.set_cur_user_archive_data('showed_egg_intro', 1)
        return

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

    def on_target_revive(self):
        self.is_revive_over = True
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            if global_data.cam_lctarget == global_data.cam_lplayer:
                global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
        global_data.ui_mgr.close_ui('DeathPlayBackUI')

    def init_player_rotation(self):
        if not self.is_in_spectate_or_ob():
            if global_data.player and global_data.player.logic and global_data.death_battle_data.area_id:
                born_data = global_data.game_mode.get_born_data()
                base_center_pos = born_data[global_data.death_battle_data.area_id].get('map_center')
                import math3d
                position = math3d.vector(*base_center_pos)
                self.rotate_to_look_at(global_data.player.logic, position)

    def on_player_check_rotate_init(self):
        self.init_player_rotation()
        if not self.is_revive_over:
            return
        self.is_revive_over = False
        if not self.is_in_spectate_or_ob():
            global_data.player.logic.send_event('E_DEATH_GUIDE_REVIVE')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('SnatchEggTopScoreUI', 'logic.comsys.battle.SnatchEgg')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('SnatchEggTopScoreUI')
        global_data.ui_mgr.show_ui('SnatchEggTopScoreUI', 'logic.comsys.battle.SnatchEgg')

    def create_snatchegg_ready_ui(self):
        self._show_top_score_ui_in_ready()
        revive_time = BattleUtils.get_prepare_left_time()
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
        ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')

        def end_callback():
            global_data.emgr.death_count_down_over.emit()
            global_data.emgr.death_begin_count_down_over.emit()

        ui.on_delay_close(revive_time, end_callback)

    def create_snatchegg_ui(self):
        self._show_top_score_ui_after_ready()
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')

    def is_need_weapon_ui(self):
        if self.is_in_spectate_or_ob():
            return False
        player = global_data.cam_lplayer
        if not player or player.id != global_data.player.id:
            return False
        return True

    def is_in_spectate_or_ob(self):
        if global_data.player and global_data.player.logic:
            from logic.gutils import judge_utils
            if global_data.player.logic.ev_g_is_in_spectate() or judge_utils.is_ob():
                return True
            else:
                return False

        return False

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('GoldenEggThrowUI')
        global_data.ui_mgr.close_ui('EggMarkUI')
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
        global_data.ui_mgr.close_ui('SnatchEggGuideUI')

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.death_battle_data.finalize()

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
        global_data.ui_mgr.show_ui('SnatchEggTopScoreUI', 'logic.comsys.battle.SnatchEgg')
        global_data.ui_mgr.show_ui('EggMarkUI', 'logic.comsys.battle.SnatchEgg')
        global_data.ui_mgr.close_ui('GoldenEggThrowUI')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')

    def create_egg_ui(self):
        if self.game_over:
            return
        self._show_drop_egg_ui()
        self._show_egg_base_ui()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        if not self.is_in_spectate_or_ob():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')

    def _show_drop_egg_ui(self):
        from logic.comsys.battle.SnatchEgg.GoldenEggThrowUI import GoldenEggThrowUI
        GoldenEggThrowUI()

    def _show_egg_base_ui(self):
        global_data.ui_mgr.show_ui('EggMarkUI', 'logic.comsys.battle.SnatchEgg')