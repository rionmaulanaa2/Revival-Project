# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/FastSurvivalModeUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance

class FastSurvivalModeUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/bg_quick_start'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.1

    def get_close_node(self):
        return (
         self.panel.nd_touch,)

    def set_content(self):
        self.panel.lab_workday_1.SetString(81282)
        self.panel.lab_weekend_1.SetString(81283)
        size1 = self.panel.lab_workday_1.getTextContentSize()
        size2 = self.panel.lab_weekend_1.getTextContentSize()
        width = max(size1.width, size2.width) + 10
        x0, _ = self.panel.lab_workday_1.GetPosition()
        _, y1 = self.panel.lab_workday_2.GetPosition()
        _, y2 = self.panel.lab_weekend_2.GetPosition()
        self.panel.lab_workday_2.setPosition(x0 + width, y1)
        self.panel.lab_weekend_2.setPosition(x0 + width, y2)