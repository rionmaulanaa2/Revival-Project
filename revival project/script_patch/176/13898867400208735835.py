# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoUILogicWidget.py
from __future__ import absolute_import
from __future__ import print_function
import os

class VideoUILogicWidget(object):
    READY_TIMEOUT_TIME = 3

    def __init__(self, *args, **kwargs):
        super(VideoUILogicWidget, self).__init__(*args, **kwargs)
        self._is_preparing = False
        self._fit_scale = None
        return

    def play_video(self, video_path, ui_node=None):
        if not video_path or not os.path.exists(video_path):
            return
        global_data.ui_mgr.close_ui('VideoManualCtrlUI')
        self._is_preparing = True
        from common.cinematic.VideoPlayer import VideoPlayer
        VideoPlayer().play_video(video_path, self._on_stop_cb, {}, 1, self._video_ready_cb, False, 1, self._play_end_cb, self._seek_cb)
        if ui_node and ui_node.isValid():

            def cb(*args):
                self._on_ready_timeout()

            ui_node.SetTimeOut(self.READY_TIMEOUT_TIME, cb)

    def play_vod(self, url, ui_node=None):
        self._is_preparing = True
        global_data.ui_mgr.close_ui('VideoManualCtrlUI')
        from common.cinematic.VideoPlayer import VideoPlayer
        VideoPlayer().play_vod(url, self._on_stop_cb, bg_play=False, custom_video_target=self._video_ready_cb, complete_cb=self._play_end_cb, seek_to_cb=self._seek_cb)
        if ui_node and ui_node.isValid():

            def cb(*args):
                self._on_ready_timeout()

            ui_node.SetTimeOut(self.READY_TIMEOUT_TIME, cb)

    def _on_ready_timeout(self):
        if global_data.is_inner_server:
            print('[VideoUILogicWidget] is preparing:', self._is_preparing)
        if self._is_preparing:
            from common.cinematic.VideoPlayer import VideoPlayer
            VideoPlayer().stop_video(remove_video=False)

    def _on_stop_cb(self, *args):
        self._is_preparing = False
        if global_data.is_inner_server:
            print('[VideoListWidget] _on_stop_cb')
        ui = global_data.ui_mgr.get_ui('VideoManualCtrlUI')
        if ui:
            ui.on_stop_video()

    def _video_ready_cb(self, *args):
        self._is_preparing = False
        if global_data.is_inner_server:
            print('[VideoListWidget] _video_ready_cb')
        from logic.comsys.video.VideoManualCtrlUI import VideoManualCtrlUI
        ui = VideoManualCtrlUI()
        if self._fit_scale is not None:
            ui.change_fit_method(self._fit_scale)
        return

    def _play_end_cb(self, *args):
        self._is_preparing = False
        if global_data.is_inner_server:
            print('[VideoListWidget] _play_end_cb')
        ui = global_data.ui_mgr.get_ui('VideoManualCtrlUI')
        if ui:
            ui.on_play_end()

    def _seek_cb(self, *args):
        ui = global_data.ui_mgr.get_ui('VideoManualCtrlUI')
        if ui:
            ui.on_seek_to(*args)

    def change_fit_method(self, scale):
        self._fit_scale = scale