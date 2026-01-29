# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanFullScreenBg.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER
from common.const import uiconst

class ClanFullScreenBg(BasePanel):
    PANEL_CONFIG_NAME = 'crew/bg_full_screen_crew'
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True

    def on_init_panel(self, *args, **kwargs):
        pass