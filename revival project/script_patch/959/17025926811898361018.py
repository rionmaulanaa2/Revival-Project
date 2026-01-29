# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/BlankTouchUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_MSG_ZORDER
from common.const import uiconst

class BlankTouchUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/blank_touch'
    DLG_ZORDER = TOP_MSG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'touch_layer.OnClick': 'on_click_touch_layer'
       }

    def on_init_panel(self):
        self._callback = None
        return

    def set_touch_callback(self, callback):
        self._callback = callback

    def on_click_touch_layer(self, btn, touch):
        if self._callback:
            self._callback(btn, touch)

    def on_finalize_panel(self):
        self._callback = None
        return