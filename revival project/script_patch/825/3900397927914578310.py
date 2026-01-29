# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/CertificateMainUIBg.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const

class CertificateMainUIBg(BasePanel):
    PANEL_CONFIG_NAME = 'guide/bg_guide_main'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = ui_const.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args):
        self.panel.PlayAnimation('show')