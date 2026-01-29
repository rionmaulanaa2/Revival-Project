# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/LobbyCommonBgUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER
from common.const import uiconst

class LobbyCommonBgUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/window_common_bg'
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True

    def on_init_panel(self, **kwargs):
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        self.init_event()

    def on_finalize_panel(self):
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def init_event(self):
        pass