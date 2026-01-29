# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBannerS6Preview.py
from __future__ import absolute_import
from .LotteryBannerS6 import LotteryBannerS6

class LotteryBannerS6Preview(LotteryBannerS6):

    def set_content(self):
        super(LotteryBannerS6Preview, self).set_content()
        self.panel.btn_go.SetText(610617)

    def on_click_btn(self, *args):
        pass