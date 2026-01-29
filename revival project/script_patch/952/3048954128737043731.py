# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/scene_background/LuckyHouse.py
from __future__ import absolute_import
from .BackgroundUI import BackgroundUI

class LuckyHouse(BackgroundUI):
    PANEL_CONFIG_NAME = 'mall/bg_mall_exclusive'

    def on_init_panel(self):
        pass

    def on_finalize_panel(self):
        pass

    def on_appear(self):
        self.panel.PlayAnimation('show', force_resume=True)
        global_data.scene_background.start_render(5)