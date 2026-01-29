# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/SpringFestivalOpenUI.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from common.cinematic.VideoPlayer import VideoPlayer
from logic.gutils.advance_utils import set_spring_festival_content, create_black_canvas

class SpringFestivalOpenUI(BasePanel):
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = ui_const.UI_VKB_CLOSE
    PANEL_CONFIG_NAME = 'activity/activity_202101/activity_individual_share'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5

    def on_init_panel(self):
        self.init_stage_1()

    def init_stage_1(self):
        create_black_canvas(self.panel, 'canvas')
        VideoPlayer().play_video('video/11_2008.mp4', None, repeat_time=1, complete_cb=self.init_stage_2, can_jump=False)
        return

    def init_stage_2(self):
        VideoPlayer().stop_video()
        self.panel.canvas.setLocalZOrder(-1)
        self.set_content()

    def set_content(self):
        set_spring_festival_content(self.panel.temp_share)

        @self.panel.temp_share.btn_go.btn_major.callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('ActivitySpringFestivalMainUI', 'logic.comsys.activity.SpringFestival')

        @self.panel.btn_close.btn_back.callback()
        def OnClick(*args):
            self.close()