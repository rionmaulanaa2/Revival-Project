# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ScreenTouchEffectUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_MSG_ZORDER
from common.const import uiconst

class ScreenTouchEffectUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/screen_touch_effect'
    DLG_ZORDER = TOP_MSG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'touch_layer.OnBegin': 'on_update_touch_time',
       'touch_layer.OnDrag': 'on_update_touch_time',
       'touch_layer.OnClick': 'on_click_touch_layer'
       }

    def on_init_panel(self):
        self.panel.touch_layer.set_sound_enable(False)
        self._last_click_time = time.time()

    def on_update_touch_time(self, *args):
        self._last_click_time = time.time()

    def on_click_touch_layer(self, btn, touch):
        self.on_update_touch_time()
        wpos = touch.getLocation()
        lpos = self.panel.touch_effect.getParent().convertToNodeSpace(wpos)
        self.panel.touch_effect.setPosition(lpos)
        self.show_touch_effect()

    def show_touch_effect(self):
        self.panel.touch_effect.PlayAnimation('cilck')
        self.panel.touch_effect.liz_touch.resetSystem()