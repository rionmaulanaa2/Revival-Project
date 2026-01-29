# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/HuntingEndStatisticsShareUI.py
from __future__ import absolute_import
import math
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import statistics_const as stat_const
from logic.gutils.role_head_utils import init_role_head, get_role_default_photo, get_mecha_photo
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.const import uiconst
from logic.gutils.end_statics_utils import on_click_player_head
from logic.comsys.battle.Death.DeathEndStatisticsShareUI import DeathStatisticsShareUI

class HuntingStatisticsShareUI(DeathStatisticsShareUI):

    def init_settle_score_ui(self):
        super(HuntingStatisticsShareUI, self).init_settle_score_ui()
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