# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewDeathMatchMapCrimsonUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH
from logic.gcommon.common_utils.battle_utils import is_play_mode_open

class NewDeathMatchMapCrimsonUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202201/open_mine'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5
    NEED_GAUSSIAN_BLUR = False

    def on_init_panel(self, *args):
        super(NewDeathMatchMapCrimsonUI, self).on_init_panel()
        self.panel.btn_go.setVisible(is_play_mode_open(PLAY_TYPE_DEATH))

        @self.panel.btn_go.callback()
        def OnClick(*args):
            self.close()
            jump_to_mode_choose(PLAY_TYPE_DEATH)

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)