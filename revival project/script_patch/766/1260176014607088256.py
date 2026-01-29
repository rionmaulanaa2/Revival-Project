# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoWrapper.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, BG_ZORDER
from common.const import uiconst
from common.cinematic.VideoPlayer import VideoPlayer
import time

class VideoWrapper(BasePanel):
    PANEL_CONFIG_NAME = 'common/video_curtain'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    CAN_JUMP = False
    AUTO_CLOSE = True
    CLIP = False
    UI_ACTION_EVENT = {'nd_close.OnClick': 'on_click'
       }

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        self._close_t = time.time() + 30

    def on_finalize_panel(self):
        self.show_main_ui()
        VideoPlayer().stop_video()

    def play_video(self, video_tag):
        self.panel.nd_bg.setVisible(True)
        video_ready_cb = lambda *args: self.on_video_ready()
        complete_cb = lambda *args: self.on_video_complete()
        video_path = 'video/%s.mp4' % video_tag
        import C_file
        if not C_file.find_res_file(video_path, ''):
            self.close()
            return
        VideoPlayer().play_video(video_path, self.on_video_complete, repeat_time=1, bg_play=True, video_ready_cb=video_ready_cb, complete_cb=complete_cb, can_jump=self.CAN_JUMP, clip_enable=self.CLIP, skip_time=5, skip_callback=complete_cb)
        day = global_data.player.get_setting(video_tag, -1)
        from logic.gcommon import time_utility as tutil
        today = int(tutil.get_date_str('%Y%m%d'))
        if day != today:
            global_data.player.write_setting(video_tag, today)
            global_data.player.save_settings_to_file()

    def on_video_ready(self):
        self.panel.nd_bg.setVisible(False)

    def on_video_complete(self):
        if self.AUTO_CLOSE:
            self.close()
        self._close_t = 0

    def on_click(self, *args):
        if time.time() < self._close_t:
            return
        self.close()