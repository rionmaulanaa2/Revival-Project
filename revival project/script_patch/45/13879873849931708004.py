# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SchoolFullScreen.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance

class SchoolFullScreen(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/bg_school'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'panel.btn_go.OnClick': 'on_click_btn'
       }

    def on_init_panel(self, *args):
        self._lottery_ui = None
        super(SchoolFullScreen, self).on_init_panel(*args)
        return

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def set_content(self):
        self.panel.lab_desc.SetString(81284)

    def on_click_btn(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_to_lottery
        jump_to_lottery('8', 208200111)

    def show_from_lottery(self, ui_name):
        self.panel.PlayAnimation(self.APPEAR_ANIM)
        self.panel.btn_go.setVisible(False)
        if ui_name:
            self.add_show_count(ui_name)
            self._lottery_ui = ui_name
            ui = global_data.ui_mgr.get_ui(ui_name)
            ui and ui.add_hide_count(self.__class__.__name__)

    def close(self):
        self.panel.StopAnimation(self.APPEAR_ANIM)
        if self._lottery_ui:
            self.add_hide_count(self._lottery_ui)
            ui = global_data.ui_mgr.get_ui(self._lottery_ui)
            ui and ui.add_show_count(self.__class__.__name__)
            self._lottery_ui = None
            self.panel.btn_go.setVisible(True)
        else:
            super(SchoolFullScreen, self).close()
        return