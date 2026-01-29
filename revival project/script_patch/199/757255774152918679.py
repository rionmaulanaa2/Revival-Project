# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/GrowthFundWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const.activity_const import ACTIVITY_GROWTH_FUND
from logic.comsys.activity.ActivityGrowthFund import ActivityGrowthFund
from logic.comsys.activity.ActivityGrowthFundNew import ActivityGrowthFundNew

class GrowthFundWidget(object):

    def on_init_panel(self, panel, parent_ui_cls_name='ChargeUINew'):
        self.panel = panel
        self.panel.SetPosition('40%', '50%')
        self._parent_ui_cls_name = parent_ui_cls_name
        cls = ActivityGrowthFund
        self.activity_growth_fund = cls(panel, ACTIVITY_GROWTH_FUND)
        self.activity_growth_fund.on_init_panel()

    def on_finalize_panel(self):
        self.activity_growth_fund.on_finalize_panel()

    def set_show(self, show):
        if self.panel:
            self.panel.setVisible(show)