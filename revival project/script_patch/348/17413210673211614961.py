# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/season/FightEndFullScreenBg.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.const import uiconst

class FightEndFullScreenBg(BasePanel):
    PANEL_CONFIG_NAME = 'rank/bg_tier_up'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('in')
        self.hide_main_ui(exceptions=('FightEndUI', ))

    def on_finalize_panel(self):
        self.show_main_ui()