# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewMechaSkinAd.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils, mall_utils, item_utils

class NewMechaSkinAd(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_mecha_1/open_mecha_1'
    APPEAR_ANIM = 'appear'
    LOOP_START_TIME = 0.1
    LOOP_ANIM = ''
    LASTING_TIME = 1

    def on_init_panel(self, *args):
        super(NewMechaSkinAd, self).on_init_panel(*args)
        if self.LOOP_ANIM:
            self.panel.DelayCall(self.LOOP_START_TIME, self.play_loop_anim)

    def set_content(self):

        @self.panel.btn_buy.callback()
        def OnClick(btn, touch):
            jump_to_ui_utils.jump_to_lottery('42', 201800251)

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def on_finalize_panel(self):
        super(NewMechaSkinAd, self).on_finalize_panel()

    def play_loop_anim(self):
        if self.LOOP_ANIM:
            self.panel.PlayAnimation(self.LOOP_ANIM)