# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaStoryUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class MechaStoryUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mech_display/mech_story'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_window_small'
    UI_ACTION_EVENT = {}

    def on_init_panel(self, text):
        super(MechaStoryUI, self).on_init_panel()
        self.panel.temp_window_small.nd_content.GetItem(0).lab_content.SetString(text)
        self.panel.temp_window_small.lab_title.SetString(38000)

    def on_finalize_panel(self):
        pass

    def on_close(self, *args):
        self.close()