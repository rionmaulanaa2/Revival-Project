# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/mode/SpringFestivalModeUI.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
from logic.gcommon.common_utils.battle_utils import is_play_mode_open

class SpringFestivalModeUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202101/open_spring_mode'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def set_content(self):

        @self.panel.callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_mode_choose_by_battle_tid
            jump_to_mode_choose_by_battle_tid('6')