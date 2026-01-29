# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/CullingTestUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from cocosui import cc
from common.const import uiconst
from common.const.uiconst import TOP_ZORDER

class CullingTestUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/culling'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_event()
        self.init_culling_event()

    def init_event(self):
        pass

    def init_culling_event(self):

        @self.panel.ck_culling_enable.callback()
        def OnChecked(btn, check, index):
            global_data.game_mgr.scene.set_enable_cgi_visiblility_culling(check)

        @self.panel.ck_culling_debug.callback()
        def OnChecked(btn, check, index):
            global_data.emgr.scene_add_zhujue_event.emit(check)

        @self.panel.ck_culling_visibility1.callback()
        def OnChecked(btn, check, index):
            global_data.game_mgr.scene.set_debug_visibility(check)

        @self.panel.ck_culling_visibility2.callback()
        def OnChecked(btn, check, index):
            global_data.game_mgr.scene.set_debug_visibility2(check)