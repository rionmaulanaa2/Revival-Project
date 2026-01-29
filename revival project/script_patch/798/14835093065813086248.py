# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/GooseBearHappyPush/GooseBearEndStatisticsShareUI.py
from __future__ import absolute_import
from logic.comsys.battle.Death.DeathEndStatisticsShareUI import DeathStatisticsShareUI

class GooseBearEndStatisticsShareUI(DeathStatisticsShareUI):
    PANEL_CONFIG_NAME = 'battle_tdm2/role_battle_record_tdm'

    def on_init_panel(self, _settle_dict, my_group_list, other_group_list, my_uid, game_info=None):
        super(GooseBearEndStatisticsShareUI, self).on_init_panel(_settle_dict, my_group_list, other_group_list, my_uid, game_info)
        self.panel.temp_details.lab_blue_title_2.SetString(5072)
        self.panel.temp_details.lab_blue_title_3.SetString(17368)
        self.panel.temp_details.lab_red_title_2.SetString(5072)
        self.panel.temp_details.lab_red_title_3.SetString(17368)