# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/advertising/TemplateSkin1.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class TemplateSkin1(SimpleAdvance):
    PANEL_CONFIG_NAME = ''
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1
    JUMP_FUNC = ''
    JUMP_ARGS = []

    def set_content(self):

        @self.panel.btn_go.callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            if self.JUMP_FUNC:
                func = getattr(jump_to_ui_utils, self.JUMP_FUNC)
                if func:
                    func(*self.JUMP_ARGS)

    def get_close_node(self):
        if self.panel.temp_btn_close:
            return (self.panel.temp_btn_close.btn_back,)
        else:
            return (
             self.panel.btn_close,)