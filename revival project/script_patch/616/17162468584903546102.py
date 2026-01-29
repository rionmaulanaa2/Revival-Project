# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/RankBeginUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class RankBeginUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_point/fight_point_begin'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.set_data(0)

    def on_finalize_panel(self):
        self.panel.nd_point.StopTimerAction()

    def init_parameters(self):
        pass

    def init_event(self):
        pass

    def set_data(self, group_points):
        self.panel.lab_point.SetString(str(group_points))