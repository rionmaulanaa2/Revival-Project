# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideIntroStepsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT

class GuideIntroStepsUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/introduction_steps'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kargs):

        @self.panel.callback()
        def OnClick(*args):
            self.close()
            logic = global_data.player.logic if global_data.player else None
            if logic:
                logic.send_event('E_GUIDE_CLOSE_INTRO_STEPS')
            return