# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/advertising/TemplateActivity2.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class TemplateActivity2(SimpleAdvance):
    PANEL_CONFIG_NAME = ''
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1
    ACTIVITY_ID = None
    ACTIVITY_TIME = None

    def set_content(self):
        if self.panel.lab_time:
            self.panel.lab_time.SetString(get_text_by_id(611565).format(time=self.ACTIVITY_TIME))

        @self.panel.nd_content.btn_go.callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            jump_to_ui_utils.jump_to_activity(self.ACTIVITY_ID)

    def get_close_node(self):
        return (
         self.panel.nd_content.btn_close,)