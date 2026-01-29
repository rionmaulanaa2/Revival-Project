# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CFireSurMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.vscene.parts.gamemode.CNormalMode import CNormalBase

class CFireSurMode(CNormalBase):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)
        self.init_singleton()

    def init_parameters(self):
        self.game_over = False

    def init_mgr(self):
        super(CFireSurMode, self).init_mgr()
        from logic.comsys.battle.Fire.FireSurvivalBattleMgr import FireSurvivalBattleMgr
        FireSurvivalBattleMgr()

    def on_train_loaded(self, *args):
        if not global_data.ui_mgr.get_ui('TrainProgUI'):
            global_data.ui_mgr.show_ui('TrainProgUI', 'logic.comsys.battle.survival')

    def init_singleton(self):
        from logic.comsys.battle.survival.SurvivalBattleData import SurvivalBattleData
        SurvivalBattleData()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_train_loaded': self.on_train_loaded,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'scene_observed_player_setted_event': self.on_enter_observed
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
        else:
            if global_data.ui_mgr.get_ui('FireSurvivalBattleTopCounterUI') is None:
                self.check_show_fire_top_ui()
            if global_data.game_mode.is_neutral_shop_env() and not self.is_in_spectate():
                if global_data.is_pc_mode:
                    from logic.comsys.battle.NeutralShopBattle.BattleAceCoinUIPC import BattleAceCoinUIPC
                    BattleAceCoinUIPC()
                else:
                    from logic.comsys.battle.NeutralShopBattle.BattleAceCoinUI import BattleAceCoinUI
                    BattleAceCoinUI()
            return

    def check_show_fire_top_ui(self):
        if global_data.battle:
            cfg_data = global_data.game_mode.get_cfg_data('play_data')
            fire_extinguishing_count = cfg_data.get('fire_immune_num', 7)
            if global_data.battle.get_fire_num() >= fire_extinguishing_count:
                return
        is_in_spectate = False
        if global_data.player and global_data.player.logic:
            is_in_spectate = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
            if is_in_spectate:
                return
        global_data.ui_mgr.show_ui('FireSurvivalBattleTopCounterUI', 'logic.comsys.battle.Fire')

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('BattleAceCoinUI')
        global_data.ui_mgr.close_ui('TrainProgUI')
        global_data.ui_mgr.close_ui('FireSurvivalBattleTopCounterUI')

    def on_finalize(self):
        super(CFireSurMode, self).on_finalize()
        self.process_event(False)
        self.destroy_ui()
        global_data.fire_sur_battle_mgr.finalize()
        global_data.survival_battle_data.finalize()

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
        global_data.ui_mgr.close_ui('BattleAceCoinUI')