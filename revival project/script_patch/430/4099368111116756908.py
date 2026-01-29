# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/MeowExchangeMall.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils

class MeowExchangeMall(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/activity_202108/i_activity_miaomiao'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = False

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def on_click_btn(self, *args):
        from logic.client.const.mall_const import MEOW_ID, NONE_ID
        jump_to_ui_utils.jump_to_mall(i_types=(MEOW_ID, NONE_ID))
        self.close()