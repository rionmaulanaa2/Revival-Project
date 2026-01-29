# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonBeginBackgroundUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_0, UI_VKB_CLOSE
import cc

class SeasonBeginBackgroundUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/new_season_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('appear')))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('appear')))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        self.panel.runAction(cc.Sequence.create(action_list))