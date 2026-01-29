# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/FFAModeUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
from logic.gcommon.common_const.battle_const import PLAY_TYPE_FFA
from logic.gcommon.common_utils.battle_utils import is_play_mode_open

class FFAModeUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_201912/open_ffa_ad'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    NEED_GAUSSIAN_BLUR = True

    def on_init_panel(self, *args):
        super(FFAModeUI, self).on_init_panel()
        self.panel.btn_go.setVisible(is_play_mode_open(PLAY_TYPE_FFA))

        @self.panel.btn_go.callback()
        def OnClick(*args):
            self.close()
            jump_to_mode_choose(PLAY_TYPE_FFA)

    def set_content(self):
        self.panel.lab_workday_1.SetString(81282)
        self.panel.lab_weekend_1.SetString(81283)
        size1 = self.panel.lab_workday_1.getTextContentSize()
        size2 = self.panel.lab_weekend_1.getTextContentSize()
        width = max(size1.width, size2.width) + 10
        x0, _ = self.panel.lab_workday_1.GetPosition()
        _, y1 = self.panel.lab_workday_2.GetPosition()
        _, y2 = self.panel.lab_weekend_2.GetPosition()
        self.panel.lab_workday_2.setPosition(x0 + width, y1)
        self.panel.lab_weekend_2.setPosition(x0 + width, y2)

    def get_close_node(self):
        return (
         self.panel.nd_close, self.panel.temp_btn_close.btn_back)