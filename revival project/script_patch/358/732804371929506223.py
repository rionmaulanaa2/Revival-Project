# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseModeChooseWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.common_const.battle_const import DEFAULT_EXERCISE_TID, DEFAULT_EXERCISE_PRIVATE_TID

class ExerciseModeChooseWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {}
        super(ExerciseModeChooseWidget, self).__init__(parent, panel)
        self._mode = DEFAULT_EXERCISE_TID
        self.on_init_panel()

    def on_init_panel(self):
        self.init_ui_events()
        self.init_default_choice()

    def init_ui_events(self):

        @self.panel.nd_window.img_window_bg.btn_close.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.destroy()

        @self.panel.btn_tips.unique_callback()
        def OnClick(*args):
            self.on_click_show_tips(*args)

        @self.panel.nd_choose.temp_1.btn.unique_callback()
        def OnClick(*args):
            self.panel.nd_choose.temp_1.btn.bar.choose.setVisible(True)
            self.panel.nd_choose.temp_2.btn.bar.choose.setVisible(False)
            self._mode = DEFAULT_EXERCISE_TID

        @self.panel.nd_choose.temp_2.btn.unique_callback()
        def OnClick(*args):
            self.panel.nd_choose.temp_1.btn.bar.choose.setVisible(False)
            self.panel.nd_choose.temp_2.btn.bar.choose.setVisible(True)
            self._mode = DEFAULT_EXERCISE_PRIVATE_TID

        @self.panel.btn_confirm.btn_common_big.unique_callback()
        def OnClick(*args):
            self.on_click_confirm(*args)

    def init_default_choice(self):
        self.panel.nd_choose.temp_1.btn.bar.choose.setVisible(self._mode == DEFAULT_EXERCISE_TID)
        self.panel.nd_choose.temp_2.btn.bar.choose.setVisible(self._mode == DEFAULT_EXERCISE_PRIVATE_TID)

    def on_click_confirm(self, *args):
        if self._mode in (DEFAULT_EXERCISE_TID, DEFAULT_EXERCISE_PRIVATE_TID):
            global_data.player.get_ready(True, self._mode, True)

    def on_click_show_tips(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(5098, 5097)
        dlg.panel.SetPosition('80%', '50%')

    def destroy(self):
        self.panel.Destroy()
        super(ExerciseModeChooseWidget, self).destroy()