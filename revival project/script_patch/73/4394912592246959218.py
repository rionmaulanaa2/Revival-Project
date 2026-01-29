# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/scene_background/GetMechaModelDisplay.py
from __future__ import absolute_import
from .BackgroundUI import BackgroundUI

class GetMechaModelDisplay(BackgroundUI):
    PANEL_CONFIG_NAME = 'mall/get_model_display_new02'

    def _ontest_get_mecha(self, shit=False):
        self.panel.img_mecha_display.setVisible(shit)

    def on_init_panel(self):
        self.panel.nd_star.setVisible(False)
        global_data.scene_background.start_render(-1)
        global_data.emgr.test_get_mecha += self._ontest_get_mecha

    def on_finalize_panel(self):
        global_data.scene_background.stop_render()
        global_data.emgr.test_get_mecha -= self._ontest_get_mecha

    def on_appear(self):
        pass