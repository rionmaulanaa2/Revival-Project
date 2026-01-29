# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityRedCliff/ActivityPyramidLotteryOpen.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils, mall_utils, item_utils

class ActivityPyramidLotteryOpen(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_activity_2/open_activity_2'
    APPEAR_ANIM = 'appear'
    LOOP_START_TIME = 0.2
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1

    def on_init_panel(self, *args):
        super(ActivityPyramidLotteryOpen, self).on_init_panel(*args)
        if self.LOOP_ANIM:
            self.panel.DelayCall(self.LOOP_START_TIME, self.play_loop_anim)

        @self.panel.btn_go.unique_callback()
        def OnClick(*args):
            jump_to_ui_utils.jump_to_lottery('46')
            self.close()

    def get_close_node(self):
        return (
         self.panel.btn_close,)

    def play_loop_anim(self):
        self.panel.PlayAnimation(self.LOOP_ANIM)