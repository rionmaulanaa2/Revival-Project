# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/scene_background/BackgroundUI.py
from __future__ import absolute_import
import game3d
import cc

class BackgroundUI(object):
    PANEL_CONFIG_NAME = 'not exist'

    def __init__(self):
        self._load_panel()
        self.on_init_panel()

    def _load_panel(self):
        import device_compatibility
        self.panel = panel = global_data.uisystem.load_template_create(self.PANEL_CONFIG_NAME)
        panel.retain()
        size = panel.getContentSize()
        design_size = global_data.ui_mgr.design_screen_size
        x_scale = design_size.width / size.width
        y_scale = design_size.height / size.height
        panel.setAnchorPoint(cc.Vec2(0, 0))
        if device_compatibility.IS_DX:
            panel.setScaleX(x_scale)
            panel.setScaleY(y_scale)
            panel.SetPosition(0, 0)
        else:
            panel.setScaleX(x_scale)
            panel.setScaleY(-y_scale)
            panel.SetPosition(0, size.height * y_scale)

    def get(self):
        return self.panel.get()

    def visit(self):
        self.panel.visit()

    def isValid(self):
        return self.panel.isValid()

    def destroy(self):
        self.on_finalize_panel()
        self.panel.Destroy()
        self.panel = None
        return

    def on_init_panel(self):
        pass

    def on_finalize_panel(self):
        pass