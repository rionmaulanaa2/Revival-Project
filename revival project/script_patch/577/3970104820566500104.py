# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewSeasonUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
import logic.gutils.season_utils as season_utils
from common.const import uiconst
import time
from logic.gutils.advance_utils import create_black_canvas

class NewSeasonUI(BasePanel):
    PANEL_CONFIG_NAME = 'season/season_fg'
    VIDEO_PATH = 'video/season_logo.mp4'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_close.OnClick': 'try_close'
       }
    UI_OPEN_SOUND = 'season_logo'

    def on_init_panel(self, *args):
        self._open_ts = time.time()
        self.hide_main_ui()
        from logic.gutils.battle_pass_utils import get_now_season
        now_season = get_now_season()
        self.panel.lab_title.SetString(get_text_by_id(83588).format(now_season))
        create_black_canvas(self.panel, 'canvas')
        from common.cinematic.VideoPlayer import VideoPlayer
        video_ready_cb = lambda *args: self.on_video_ready()
        complete_cb = lambda *args: self.on_video_complete()
        VideoPlayer().play_video(self.VIDEO_PATH, video_ready_cb, repeat_time=1, bg_play=True, complete_cb=complete_cb, can_jump=False, video_ready_cb=video_ready_cb)
        self._loading_video = True

    def on_video_ready(self):
        self.panel.canvas.setVisible(False)
        self._loading_video = False
        self.panel.SetTimeOut(1.5, lambda : self.panel.PlayAnimation('show') and 0)
        self.panel.SetTimeOut(5.0, lambda : self.panel.PlayAnimation('loop') and 0)

    def on_video_complete(self):
        pass

    def on_finalize_panel(self):
        from common.cinematic.VideoPlayer import VideoPlayer
        VideoPlayer().stop_video()
        self.show_main_ui()

    def try_close(self, *args):
        if time.time() - self._open_ts < 2 and not self._loading_video:
            return
        self.close()