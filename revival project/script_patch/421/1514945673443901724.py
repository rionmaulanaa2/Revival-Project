# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CFlag2Mode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.building_const import FLAG_RECOVER_BY_PLANTING
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil

class CFlag2Mode(CDeathMode):
    RECOVER_REASON_TO_UI_TYPE = {FLAG_RECOVER_BY_PLANTING: {'teammate': battle_const.FLAG2_BATTLE_FLAG_PLANTED_SELF_TEAM,
                                  'enemy': battle_const.FLAG2_BATTLE_FLAG_PLANTED_OTHER_TEAM
                                  }
       }

    def __init__(self, map_id):
        super(CFlag2Mode, self).__init__(map_id)
        self.welcome_ui_showed = False

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'loading_end_event': self.on_loading_end,
           'target_revive_event': self.on_target_revive,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'flagsnatch_flag_recover': self.show_flag_recover_hint,
           'flagsnatch_flag_pick_up': self.show_flag_pick_hint,
           'death_begin_count_down_over': self._create_welcome_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('DeathPlayBackUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('DeathBeginCountDown')
        global_data.ui_mgr.close_ui('FFABeginCountDown')
        global_data.ui_mgr.close_ui('DeathWeaponChooseBtn')
        global_data.ui_mgr.close_ui('Flag2TopScoreUI')
        global_data.ui_mgr.close_ui('FlagScoreDetailsUI')
        global_data.ui_mgr.close_ui('DeathAttentionUI')
        global_data.ui_mgr.close_ui('BattleBuffProgressUI')
        global_data.ui_mgr.close_ui('Flag2MarkUI')
        global_data.ui_mgr.close_ui('Flag2ThrowUI')
        global_data.ui_mgr.close_ui('Flag2GuideUI')
        global_data.ui_mgr.close_ui('Flag2PlantProgUI')

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            global_data.death_battle_data.is_ready_state = True
            self.create_death_ready_ui()
            self.create_flag_ui()
            self.on_player_check_rotate_init()
        elif stage == parachute_utils.STAGE_LAND:
            global_data.death_battle_data.is_ready_state = False
            self.create_flag_ui()
            self.on_player_check_rotate_init()
            self.check_lock_time()

    def check_lock_time(self):
        if not global_data.death_battle_data.flag_lock_start_time:
            if global_data.cam_lplayer:
                global_data.death_battle_data.set_flag_lock_start_time(tutil.time(), global_data.cam_lplayer.ev_g_camp_id())

    def create_flag_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        self._show_drop_flag_ui()
        self._show_flag_base_ui()
        self._show_flag2_guide_ui()
        self._show_flag2_plant_prog_ui()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        if not self.is_in_spectate_or_ob():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('Flag2TopScoreUI', 'logic.comsys.battle.Flag2')

    def _show_top_score_ui_after_ready(self):
        if global_data.ui_mgr.get_ui('Flag2TopScoreUI') is None:
            global_data.ui_mgr.show_ui('Flag2TopScoreUI', 'logic.comsys.battle.Flag2')
        return

    def _show_drop_flag_ui(self):
        global_data.ui_mgr.show_ui('Flag2ThrowUI', 'logic.comsys.battle.Flag2')

    def _show_flag_base_ui(self):
        global_data.ui_mgr.show_ui('Flag2MarkUI', 'logic.comsys.battle.Flag2')

    def _show_flag2_guide_ui(self):
        if global_data.ui_mgr.get_ui('Flag2GuideUI') is None:
            global_data.ui_mgr.show_ui('Flag2GuideUI', 'logic.comsys.battle.Flag2')
        return

    def _show_flag2_plant_prog_ui(self):
        if global_data.ui_mgr.get_ui('Flag2PlantProgUI') is None:
            global_data.ui_mgr.show_ui('Flag2PlantProgUI', 'logic.comsys.battle.Flag2')
        return

    def init_death_data_mgr(self):
        from logic.comsys.battle.Flag2.Flag2BattleData import Flag2BattleData
        Flag2BattleData()

    def _create_welcome_ui(self):
        if self.welcome_ui_showed:
            return
        tip_type = battle_const.FLAG2_BATTLE_START_TIP
        text = get_text_by_id(17911)
        message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
        global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)
        self.welcome_ui_showed = True

    def show_flag_recover_hint(self, holder_id, holder_faction, reason):
        ui_types = self.RECOVER_REASON_TO_UI_TYPE.get(reason, None)
        if not ui_types:
            return
        else:
            if reason == FLAG_RECOVER_BY_PLANTING:
                if global_data.battle:
                    picker = global_data.battle.get_entity(holder_id)
                if not picker:
                    return
                name = picker.data.get('char_name', None)
                if not name:
                    return
                if holder_faction == global_data.player.logic.ev_g_group_id():
                    tip_type = ui_types.get('teammate', None)
                    text = get_text_by_id(17907, args=(name,))
                    message = {'i_type': tip_type,'content_txt': text,'in_anim': 'show','out_anim': 'disappear'}
                else:
                    tip_type = ui_types.get('enemy', None)
                    text = get_text_by_id(17910, args=(name,))
                    message = {'i_type': tip_type,'content_txt': text,'in_anim': 'show','out_anim': 'disappear'}
                global_data.emgr.show_battle_main_message.emit(message, battle_const.MAIN_NODE_COMMON_INFO)
            return

    def show_flag_pick_hint(self, picker_id, picker_faction, *args):
        if global_data.battle:
            picker = global_data.battle.get_entity(picker_id)
        if not picker:
            return
        else:
            name = picker.data.get('char_name', None)
            if not name:
                return
            if global_data.player.logic.ev_g_group_id() == picker_faction:
                tip_type = battle_const.FLAG2_BATTLE_FLAG_PICKED_SELF_TEAM
                text = get_text_by_id(17149).format(name)
                message = {'i_type': tip_type,'content_txt': text,'in_anim': 'show','out_anim': 'disappear'}
            else:
                tip_type = battle_const.FLAG2_BATTLE_FLAG_PICKED_OTHER_TEAM
                text = get_text_by_id(17149).format(name)
                message = {'i_type': tip_type,'content_txt': text,'in_anim': 'show','out_anim': 'disappear'}
            global_data.emgr.show_battle_main_message.emit(message, battle_const.MAIN_NODE_COMMON_INFO)
            return