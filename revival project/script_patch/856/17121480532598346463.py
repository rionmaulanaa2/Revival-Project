# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleTransitionUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils.judge_utils import get_player_group_id
import math
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id

class BattleTransitionUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_crystal/end_crystal2_round_1'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, delay_disappear_time=5.0, delay_close_time=5.5, **kwargs):
        self.init_score_widget()
        self.panel.PlayAnimation('appear')
        self.panel.DelayCall(delay_disappear_time, self.do_disappear)
        self.panel.DelayCall(delay_close_time, self.close)

    def init_score_widget(self):
        pass

    def do_disappear(self):
        if self.panel and self.panel.isValid():
            self.panel.PlayAnimation('disappear')

    def close(self, *args):
        if not self or not self.panel or not self.panel.isValid():
            return
        super(BattleTransitionUI, self).close()