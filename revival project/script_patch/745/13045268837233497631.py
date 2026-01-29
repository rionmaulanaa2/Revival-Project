# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBannerS5Sakugan.py
from __future__ import absolute_import
from logic.gutils import jump_to_ui_utils
from common.cfg import confmgr
from logic.comsys.activity.SimpleAdvance import SimpleAdvance

class LotteryBannerS5Sakugan(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202111/i_sakugan_open'
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 0
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }
    NEED_GAUSSIAN_BLUR = False

    def on_init_panel(self, *args):
        self.ss_skin = 201802051
        super(LotteryBannerS5Sakugan, self).on_init_panel(*args)

    def on_click_btn(self, *args):
        jump_to_ui_utils.jump_to_lottery('32')

    def get_close_node(self):
        return (
         self.panel.btn_close,)