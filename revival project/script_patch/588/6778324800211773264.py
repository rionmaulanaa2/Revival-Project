# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityBroadcastSmallUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance

class ActivityBroadcastSmallUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/game_live_small'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5

    def set_content(self):
        btn = self.panel.temp_banner.btn_for_details

        @btn.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import activity_utils
            activity_utils.goto_broadcast()