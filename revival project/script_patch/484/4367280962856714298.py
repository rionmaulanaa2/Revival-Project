# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/CreditAdvanceUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance

class CreditAdvanceUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_201911/open_honor'
    APPEAR_ANIM = 'in'
    LASTING_TIME = 0.5

    def set_content(self, open=True):

        @self.panel.btn_go.callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_player_info
            jump_to_player_info(3)