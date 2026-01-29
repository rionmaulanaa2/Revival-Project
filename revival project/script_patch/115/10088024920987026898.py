# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NoAdvanceUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from common.const import uiconst

class NoAdvanceUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/close_tips'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'panel.btn_close.OnClick': 'on_click_btn'
       }

    def on_init_panel(self, *args):
        self._is_hide = False
        if global_data.player:
            _, self._is_hide = global_data.player.get_hide_advance_data()
        self.panel.btn_close.SetSelect(self._is_hide)

    def on_click_btn(self, *args):
        self._is_hide = not self._is_hide
        self.panel.btn_close.SetSelect(self._is_hide)
        if global_data.player:
            global_data.player.set_hide_advance(self._is_hide)

    def on_finalize_panel(self):
        pass