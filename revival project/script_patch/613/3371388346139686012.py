# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbySceneCaptureListenerUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER, UI_TYPE_EFFECT
import time
from common.const import uiconst

class LobbySceneCaptureListenerUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/empty_touch_layer'
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT
    IS_FULLSCREEN = True
    GLOBAL_EVENT = {'ui_close_event': 'on_close_ui'
       }

    def on_init_panel(self, *args, **kwargs):
        self._last_close_ui_time = 0
        self.panel.EnableDoubleClick(True)

        @self.panel.callback()
        def OnDoubleClick(btn, last_pos, cur_pos):
            self.trigger_scene_capture()

    def trigger_scene_capture(self):
        if time.time() - self._last_close_ui_time < 1:
            return
        if not global_data.ui_mgr.get_ui('LobbySceneOnlyUI') and global_data.enable_lobby_scene_only:
            from logic.comsys.share.LobbySceneOnlyUI import LobbySceneOnlyUI
            LobbySceneOnlyUI()

    def on_close_ui(self, dlg_name):
        self._last_close_ui_time = time.time()