# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySSBannerCopy.py
from __future__ import absolute_import
from .LotterySSBanner import LotterySSBanner

class LotterySSBannerCopy(LotterySSBanner):

    def hide_close_btn(self):
        self.panel.btn_go.setVisible(False)