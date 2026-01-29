# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaShowtimeIntroUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel

class KizunaShowtimeIntroUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/ai_introduce'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {}
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(KizunaShowtimeIntroUI, self).on_init_panel()
        self.hide_main_ui()
        self.panel.nd_intro_2.setVisible(False)
        self.panel.nd_intro_1.setVisible(True)
        self.panel.BindMethod('OnClick', self.on_click_bg)
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(0.7, lambda : self.panel.PlayAnimation('loop'))

    def on_finalize_panel(self):
        super(KizunaShowtimeIntroUI, self).on_finalize_panel()
        self.show_main_ui()

    def on_click_bg(self, btn, touch):
        ani_list = [
         'show', 'show_02', 'show_03']
        for ani in ani_list:
            if self.panel.IsPlayingAnimation(ani):
                return

        if self.panel.nd_intro_3.isVisible():
            self.close()
        elif self.panel.nd_intro_1.isVisible():
            self.panel.nd_intro_2.setVisible(True)
            self.panel.nd_intro_1.setVisible(False)
            self.panel.PlayAnimation('show_02')
        elif self.panel.nd_intro_2.isVisible():
            self.panel.nd_intro_3.setVisible(True)
            self.panel.nd_intro_2.setVisible(False)
            self.panel.nd_intro_1.setVisible(False)
            self.panel.PlayAnimation('show_03')

    def set_close_countdown(self, t):
        self.panel.SetTimeOut(t, lambda : self.close())