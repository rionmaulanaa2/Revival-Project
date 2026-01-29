# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideForceUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER
from common.const import uiconst

class GuideForceUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_force_ui'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        self._touch_area_list = []
        self.panel.BindMethod('OnBegin', self.on_check_guide)

    def on_finalize_panel(self):
        self._touch_area_list = []

    def set_touch_area_list(self, nd_list):
        self._touch_area_list = nd_list

    def on_check_guide(self, btn, touch):
        if not self._touch_area_list:
            return False
        pos = touch.getLocation()
        for nd in self._touch_area_list:
            if nd.isValid():
                if nd.IsPointIn(pos):
                    return False

        return True