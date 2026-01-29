# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/christmas/ChristmasLottery.py
from __future__ import absolute_import
from ..SimpleAdvance import SimpleAdvance
from logic.gutils.jump_to_ui_utils import jump_to_lottery

class ChristmasLottery(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_201912/open_christmas'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def on_click_btn(self, *args):
        pass