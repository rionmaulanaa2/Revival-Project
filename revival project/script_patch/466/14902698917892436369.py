# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CMutiOccupyMode.py
from __future__ import absolute_import
from logic.comsys.battle import BattleUtils
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle.MutiOccupy.MutiOccupyData import MutiOccupyData
from logic.comsys.battle.MutiOccupy.MutiOccupySfxMgr import MutiOccupySfxMgr

class CMutiOccupyMode(CDeathMode):

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        self.occupy_data_mgr.destroy()
        self.occupy_data_mgr = None
        global_data.death_battle_data.finalize()
        return

    def init_mgr(self):
        self.init_occupy_data_mgr()
        self.init_occupy_sfx_mgr()

    def init_occupy_data_mgr(self):
        MutiOccupyData()

    def init_occupy_sfx_mgr(self):
        self.occupy_data_mgr = MutiOccupySfxMgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'loading_end_event': self.on_loading_end,
           'target_revive_event': self.on_target_revive,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'scene_pick_obj_event': self.pick_up_paradrop_weapon,
           'battle_loading_finished_event': self.check_show_introduct_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('MutiOccupyDeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('DeathTopScoreUI')
        global_data.ui_mgr.close_ui('MutiOccupyScoreDetailsUI')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('MutiOccupyMarkUI')
        global_data.ui_mgr.close_ui('MutiOccupySkillUI')
        global_data.ui_mgr.close_ui('MutiOccupyBattleUI')
        global_data.ui_mgr.close_ui('MutiOccupyBornChooseUI')

    def create_death_ui(self):
        super(CMutiOccupyMode, self).create_death_ui()
        if self.game_over:
            return
        global_data.ui_mgr.show_ui('MutiOccupyMarkUI', 'logic.comsys.battle.MutiOccupy')
        global_data.ui_mgr.show_ui('MutiOccupySkillUI', 'logic.comsys.battle.MutiOccupy')
        global_data.emgr.update_occupy_point_state.emit()
        global_data.emgr.player_enable_auto_pick_event.emit(False)

    def create_death_ready_ui(self):
        super(CMutiOccupyMode, self).create_death_ready_ui()
        revive_time = BattleUtils.get_prepare_left_time()
        global_data.emgr.update_occupy_point_state.emit()

    def check_show_introduct_ui(self):
        showed_intro = global_data.achi_mgr.get_cur_user_archive_data('showed_mutioccupy_intro', 0)
        if not showed_intro:
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(None, 40)
            global_data.achi_mgr.set_cur_user_archive_data('showed_mutioccupy_intro', 1)
        return

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('MutiOccupyBattleUI', 'logic.comsys.battle.MutiOccupy')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('MutiOccupyBattleUI')
        global_data.ui_mgr.show_ui('MutiOccupyBattleUI', 'logic.comsys.battle.MutiOccupy')

    def on_target_revive(self):
        self.is_revive_over = True
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
        global_data.ui_mgr.close_ui('MutiOccupyDeathPlayBackUI')
        global_data.ui_mgr.close_ui('MutiOccupyBornChooseUI')

    def on_target_defeated(self, revive_time, killer_id, kill_info):
        if self.game_over:
            return
        global_data.ui_mgr.close_ui('MutiOccupySkillUI')
        reply_data = kill_info.get('reply_data', {})
        ui = global_data.ui_mgr.show_ui('DeathBeginCountDown', 'logic.comsys.battle.Death')
        ui.on_delay_close(revive_time)
        ui = global_data.ui_mgr.show_ui('MutiOccupyDeathPlayBackUI', 'logic.comsys.battle.MutiOccupy')
        ui.set_revive_time(revive_time)
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('S_ATTR_SET', 'death_mode_leave_base_firstly', True)
        if global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate():
            return
        global_data.ui_mgr.show_ui('MutiOccupyBornChooseUI', 'logic.comsys.battle.MutiOccupy')

    def pick_up_paradrop_weapon(self, item_no=None, package_part=None, put_pos=-1, house_entity_id=None, parent_entity_id=None):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            weapons = global_data.player.logic.ev_g_all_weapons()
            first_weapon = weapons.get(1, None)
            if first_weapon:
                item_id = first_weapon.get('item_id', 10654)
                weapon_list = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
                global_data.emgr.battle_show_message_event.emit(get_text_local_content(17466))
            return