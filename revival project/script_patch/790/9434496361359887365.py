# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/Charging.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.const import uiconst

class Charging(BasePanel):
    PANEL_CONFIG_NAME = 'charge/charging'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.panel.PlayAnimation('charge')
        global_data.emgr.on_charging_ui_show_event.emit(True)

    def on_finalize_panel(self):
        global_data.emgr.on_charging_ui_show_event.emit(False)