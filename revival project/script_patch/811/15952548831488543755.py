# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonEmptyUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.const import uiconst

class CommonEmptyUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/empty_no_scale'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    CAN_JUMP = False
    AUTO_CLOSE = True
    CLIP = False

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.show_main_ui()