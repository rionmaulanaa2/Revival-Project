# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/BondAdvance.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils

class BondAdvance(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202004/bond'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    NEED_GAUSSIAN_BLUR = False
    UI_ACTION_EVENT = {'panel.btn_go.OnClick': 'on_click_go'
       }

    def set_content(self):
        pass

    def get_close_node(self):
        return (
         self.panel.nd_close, self.panel.temp_btn_close.btn_back)

    def on_click_go(self, *args):
        jump_to_ui_utils.try_jump_to_bond(global_data.player.get_role())