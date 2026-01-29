# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/HuntingEndStatisticsUI.py
from __future__ import absolute_import
from logic.gutils.settle_scene_utils import *
from logic.comsys.battle.Death.DeathEndStatisticsUI import DeathStatisticsUI

class HuntingStatisticsUI(DeathStatisticsUI):

    def get_is_pure_mecha(self):
        if not self._is_ob_settle():
            return global_data.player.logic.ev_g_is_pure_mecha()

    def init_settle_score_ui(self):
        super(HuntingStatisticsUI, self).init_settle_score_ui()
        our_item_list = self.panel.temp_data.nd_blue.list_score.GetAllItem()
        other_item_list = self.panel.temp_data.nd_red.list_score.GetAllItem()
        our_group = self.all_infos[0][1]
        other_group = self.all_infos[1][1]
        item_list_infos = [(our_group, our_item_list), (other_group, other_item_list)]
        for groups, items in item_list_infos:
            for idx, item in enumerate(items):
                if idx >= len(groups):
                    item.setVisible(False)
                    continue
                ginfo = groups[idx]
                if ginfo[0] is None:
                    item.setVisible(False)
                    continue
                if ginfo[10] is None:
                    ginfo[10] = (
                     (0, 0), (0, 0), (0, 0))
                item.lab_kill.SetString(str(ginfo[10][0][0]))

        return