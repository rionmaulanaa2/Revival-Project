# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CScavengeMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from common.cfg import confmgr
from logic.gcommon.const import PART_WEAPON_POS_MAIN_DF
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id

class CScavengeMode(CDeathMode):

    def __init__(self, map_id):
        super(CScavengeMode, self).__init__(map_id)
        self.init_singleton()
        self.pick_ui = None
        return

    def init_death_data_mgr(self):
        from logic.comsys.battle.Scavenge.ScavengeData import ScavengeData
        ScavengeData()

    def init_singleton(self):
        from logic.comsys.battle.survival.SurvivalBattleData import SurvivalBattleData
        SurvivalBattleData()

    def on_train_loaded(self, *args):
        if not global_data.ui_mgr.get_ui('TrainProgUI'):
            global_data.ui_mgr.show_ui('TrainProgUI', 'logic.comsys.battle.survival')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'loading_end_event': self.on_loading_end,
           'target_revive_event': self.on_target_revive,
           'settle_stage_event': self.on_settle_stage,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'on_train_loaded': self.on_train_loaded,
           'death_begin_count_down_over': self._create_welcome_ui,
           'show_weapon_picked': self._show_weapon_picked,
           'show_item_refreshed': self._show_item_refreshed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def create_death_ui(self):
        if self.game_over:
            return
        self._show_top_score_ui_after_ready()
        global_data.ui_mgr.show_ui('BattleBuffProgressUI', 'logic.comsys.battle')
        if self.is_need_weapon_ui():
            global_data.ui_mgr.show_ui('DeathWeaponChooseBtn', 'logic.comsys.battle.Death')
        global_data.ui_mgr.show_ui('ScavengeSpItemGuideUI', 'logic.comsys.battle.Scavenge')
        global_data.ui_mgr.show_ui('ScavengeItemLocateUI', 'logic.comsys.battle.Scavenge')
        global_data.ui_mgr.show_ui('ScavengeMiddleBulletWidgetUI', 'logic.comsys.battle.Scavenge')

    def destroy_ui(self):
        super(CScavengeMode, self).destroy_ui()
        global_data.ui_mgr.close_ui('TrainProgUI')
        global_data.ui_mgr.close_ui('ScavengeWeaponRefreshUI')
        global_data.ui_mgr.close_ui('ScavengeSpItemGuideUI')
        global_data.ui_mgr.close_ui('ScavengeItemLocateUI')
        global_data.ui_mgr.close_ui('ScavengeMiddleBulletWidgetUI')
        global_data.ui_mgr.close_ui('ScavengeWelcomeUI')

    def is_need_weapon_ui(self):
        return False

    def _create_welcome_ui(self):
        if not global_data.ui_mgr.get_ui('ScavengeWelcomeUI'):
            global_data.ui_mgr.show_ui('ScavengeWelcomeUI', 'logic.comsys.battle.Scavenge')
        tip_type = battle_const.SCAVENGE_TIP_GAME_START
        text = get_text_by_id(83220)
        message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
        global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)

    def _show_weapon_picked(self, item_id, player_eid):
        if not global_data.player or not global_data.player.logic:
            return
        item_name = confmgr.get('item', str(item_id), 'name_id')
        if global_data.player.logic.ev_g_is_groupmate(player_eid, True):
            tip_type = battle_const.SCAVENGE_TIP_WEAPON_PICKED_BY_GROUPMATE
            text = get_text_by_id(83222).format(get_text_by_id(item_name))
            message = {'i_type': tip_type,'content_txt': text,'in_anim': 'appear','out_anim': 'disappear'}
            global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)
        else:
            tip_type = battle_const.SCAVENGE_TIP_WEAPON_PICKED_BY_ENEMY
            text = get_text_by_id(83223).format(get_text_by_id(item_name))
            message = {'i_type': tip_type,'content_txt': text,'in_anim': 'appear','out_anim': 'disappear'}
            global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)

    def _show_item_refreshed(self, item_id):
        if not global_data.ui_mgr.get_ui('ScavengeWeaponRefreshUI'):
            global_data.ui_mgr.show_ui('ScavengeWeaponRefreshUI', 'logic.comsys.battle.Scavenge')
        global_data.emgr.show_scavenge_item_refreshed_event.emit(item_id)