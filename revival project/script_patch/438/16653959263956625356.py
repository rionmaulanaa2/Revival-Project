# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CNormalMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id

class CNormalBase(object):

    def on_finalize(self):
        global_data.gravity_sur_battle_mgr and global_data.gravity_sur_battle_mgr.finalize()

    def init_mgr(self):
        from logic.comsys.battle.Gravity.GravitySurvivalBattleMgr import GravitySurvivalBattleMgr
        GravitySurvivalBattleMgr()


class CNormalMode(CNormalBase):

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.process_event(True)
        self.init_mgr()

    def on_train_loaded(self, *args):
        if not global_data.ui_mgr.get_ui('TrainProgUI'):
            global_data.ui_mgr.show_ui('TrainProgUI', 'logic.comsys.battle.survival')

    def on_finalize(self):
        super(CNormalMode, self).on_finalize()
        self.process_event(False)
        self.destroy_ui()
        global_data.survival_battle_data.finalize()

    def init_parameters(self):
        self.game_over = False

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('BattleAceCoinUI')
        global_data.ui_mgr.close_ui('TrainProgUI')

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

    def init_mgr(self):
        super(CNormalMode, self).init_mgr()
        from logic.comsys.battle.survival.SurvivalBattleData import SurvivalBattleData
        SurvivalBattleData()

    def on_observer_parachute_stage_changed(self, stage):
        if stage == parachute_utils.STAGE_LAND:
            self.create_mode_specified_ui()

    def create_mode_specified_ui(self):
        if self.game_over:
            return
        if global_data.game_mode.is_neutral_shop_env() and not self.is_in_spectate():
            if global_data.is_pc_mode:
                from logic.comsys.battle.NeutralShopBattle.BattleAceCoinUIPC import BattleAceCoinUIPC
                BattleAceCoinUIPC()
            else:
                from logic.comsys.battle.NeutralShopBattle.BattleAceCoinUI import BattleAceCoinUI
                BattleAceCoinUI()

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