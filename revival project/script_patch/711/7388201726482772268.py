# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/ScriptErrorUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const import uiconst

class ScriptErrorUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/script_error_ui'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_event()

    def init_event(self):

        @self.btn_error.callback()
        def OnClick(*args):
            self.create_error()

        @self.btn_error_next.callback()
        def OnClick(self):
            raise Exception('click error')

    def on_btn_error_next_clicked(self, *args):
        import game3d
        game3d.delay_exec(1, self.create_error)