# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/KothEndStatisticsUI.py
from __future__ import absolute_import
import math
import functools
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.end_statics_utils import init_koth_end_person_statistics_new, init_koth_end_teammate_statistics_new
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class KothEndStatisticsUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_statistics_koth_team'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_next.btn_common.OnClick': '_on_click_btn_exit'
       }

    def on_init_panel(self, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, finished_cb=None):
        ui = global_data.ui_mgr.show_ui('KothEndFullScreenBg', 'logic.comsys.battle.Settle')
        ui.img_right.setVisible(True)
        self.finished_cb = finished_cb
        self._init_teammate(teaminfo, achievement)
        self._init_statistics(teammate_num, group_num, settle_dict, achievement)
        self._play_animation()
        self.init_event()

    def _init_teammate(self, teaminfo, achievement):
        groupmate_info = global_data.player.logic.ev_g_teammate_infos()
        init_koth_end_teammate_statistics_new(self.panel, groupmate_info, teaminfo, achievement)

    def _init_statistics(self, teammate_num, group_num, settle_dict, achievement):
        init_koth_end_person_statistics_new(self.panel, teammate_num, group_num, settle_dict, achievement)
        self.panel.nd_best_team.setVisible(settle_dict.get('is_best_group', False))

    def _play_animation(self):
        self.panel.PlayAnimation('appear')

    def _on_click_btn_exit(self, *args):
        self.close()
        self.finished_cb and self.finished_cb()

    def init_event(self):
        pass

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('KothEndFullScreenBg')