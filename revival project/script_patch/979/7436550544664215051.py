# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ScreenSnapShotLoadingBgUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER, UI_TYPE_EFFECT
from logic.comsys.common_ui.SceneSnapShotUI import RenderFrame
from common.const import uiconst

class ScreenSnapShotLoadingBgUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/empty_no_scale'
    IS_FULLSCREEN = True
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self):
        sz = self.panel.getContentSize()
        self.render_frame = RenderFrame(sz.width * self.panel.getScaleX(), sz.height * self.panel.getScaleY())
        self.callback = None
        self._context = None
        return

    def on_finalize_panel(self):
        if self.render_frame:
            self.render_frame.destroy()
            self.render_frame = None
        if self.callback:
            self.callback()
        return

    def set_context(self, context):
        self._context = context

    def get_context(self):
        return self._context

    def take_scene_snapshot(self, callback=None, exception_uis=[]):
        self.callback = callback
        if self.render_frame:

            def finish_callback():
                callback and callback()
                self.callback = None
                return

            self.render_frame.set_render_frame_output(self.panel, None, finish_callback)
            self.render_frame.set_exception_uis(exception_uis)
            self.render_frame.init_render_frame()
        return