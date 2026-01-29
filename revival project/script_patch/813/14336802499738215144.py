# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoWindowCtrlUI.py
from __future__ import absolute_import
from __future__ import print_function
from cocosui import ccui
import render
import cc
import game3d
import cclive
from common.uisys.basepanel import BasePanel
from common.uisys.uielment.CCSprite import CCSprite
from common.const.uiconst import LOADING_ZORDER_ABOVE, UI_VKB_CUSTOM
from common.cinematic.VideoPlayer import VideoPlayer
PLATFORM_TIME = {game3d.PLATFORM_ANDROID: 1000.0,
   game3d.PLATFORM_WIN32: 1000000.0,
   game3d.PLATFORM_IOS: 1000.0
   }

class VideoWindowCtrlUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_highlight/video_player_window'
    DLG_ZORDER = LOADING_ZORDER_ABOVE
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def on_init_panel(self, nd_video):
        self.nd_video = nd_video
        self.video_url = None
        self.live_spr = None
        self._ready_cb = None
        self._stop_cb = None
        self._close_cb = None
        self._end_cb = None
        self.is_fullscreen = False
        self._time_scale = PLATFORM_TIME.get(game3d.get_platform(), 1)
        self._duration = 0
        self._update_timer = None
        self._time_str_suffix = ''
        self._is_in_drag = False
        self._is_in_seeking = False
        self._is_play_end = False
        pos = self.panel.nd_video.getPosition()
        self._platform = game3d.get_platform()
        self.init_pos = cc.Vec2(pos.x, pos.y)
        self.init_widget()
        return

    def set_close_cb(self, stop_cb):
        self._stop_cb = stop_cb

    def set_end_cb(self, end_cb):
        self._end_cb = end_cb

    def set_ready_cb(self, ready_cb):
        self._ready_cb = ready_cb

    def init_widget(self):
        self.panel.nd_video.setVisible(False)

        @self.panel.btn_screen.unique_callback()
        def OnClick(btn, touch):
            if self.is_fullscreen:
                self._adjust_panel_window()
            else:
                self._adjust_panel_fullscreen()

        @self.panel.temp_btn_close.btn_back.unique_callback()
        def OnClick(btn, touch):
            if self.is_fullscreen:
                self._adjust_panel_window()
            else:
                self.close()

        self._adjust_panel_window()

    def play_vod(self, url_path):
        self.video_url = url_path
        VideoPlayer().play_vod(url_path, self.video_stop_cb, bg_play=False, custom_video_target=self.video_ready_cb, complete_cb=self.video_end_cb, seek_to_cb=None)
        return

    def video_stop_cb(self, *args):
        if self._stop_cb:
            self._stop_cb()

    def video_ready_cb(self, *args):
        self._init_tex_sprite()
        self.panel.nd_video.setVisible(True)
        self._init_ctrl_ui()
        if self._ready_cb:
            self._ready_cb()

    def video_end_cb(self, *args):
        self.panel.nd_video.setVisible(False)
        if self._end_cb:
            self._end_cb()

    def _init_ctrl_ui(self):
        player = VideoPlayer().get_player()
        if player:
            self.panel.btn_play.SetSelect(True)
            self.panel.nd_ui.setVisible(True)
            self._duration = player.duration / self._time_scale
            minutes = int(self._duration / 60.0)
            seconds = int(self._duration - minutes * 60)
            self._time_str_suffix = '/%02d:%02d' % (minutes, seconds)
            self.panel.lab_time.SetString('00:00' + self._time_str_suffix)
            self._update_timer = global_data.game_mgr.register_logic_timer(self._on_video_timer, 1)

            @self.panel.slider.callback()
            def OnPercentageChanged(ctrl, slider):
                v_player = VideoPlayer().get_player()
                if v_player:
                    if self._is_play_end:
                        self._is_play_end = False
                        VideoPlayer().replay()
                        self.panel.btn_play.SetSelect(True)
                        return
                    seek_time = int(slider.getPercent() / 100.0 * v_player.duration)
                    if global_data.is_inner_server and global_data.crx_test_video:
                        import time
                        print('seek_to', time.time())
                    v_player.seek_to(seek_time)

            block_seek = self._platform == game3d.PLATFORM_ANDROID
            self.panel.slider.setTouchEnabled(not block_seek)
            self.panel.slider.addTouchEventListener(self._on_normal_touch)
            self.panel.slider.setPercent(0)

            @self.panel.btn_play.callback()
            def OnClick(btn, touch):
                if self._is_in_drag:
                    return
                if self._is_in_seeking:
                    return
                v_player = VideoPlayer().get_player()
                if not v_player:
                    return
                if btn.GetSelect():
                    btn.SetSelect(False)
                    v_player.pause()
                else:
                    btn.SetSelect(True)
                    if self._is_play_end:
                        VideoPlayer().replay()
                        self._is_play_end = False
                    else:
                        v_player.resume()

            @self.panel.nd_touch.callback()
            def OnClick(*args):
                if VideoPlayer().get_player():
                    vis = self.panel.nd_ui.isVisible()
                    self.panel.nd_ui.setVisible(not vis)

        else:
            self.panel.nd_ui.setVisible(False)
            self._duration = 0

    def _on_normal_touch(self, widget, event):
        if event == ccui.WIDGET_TOUCHEVENTTYPE_BEGAN:
            v_player = VideoPlayer().get_player()
            if v_player:
                v_player.pause()
                self._is_in_drag = True
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            v_player = VideoPlayer().get_player()
            if v_player:
                btn_play_state = self.panel.btn_play.GetSelect()
                if btn_play_state:
                    v_player.resume()
                self._is_in_drag = False
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_CANCELED:
            self._is_in_drag = False

    def _on_video_timer(self, *args):
        player = VideoPlayer().get_player()
        if player:
            if self._duration == 0.0:
                self._duration = player.duration / self._time_scale
                d_minutes = int(self._duration / 60.0)
                d_seconds = int(self._duration - d_minutes * 60)
                self._time_str_suffix = '/%02d:%02d' % (d_minutes, d_seconds)
            cur_pos = player.current_position / self._time_scale
            minutes = int(cur_pos / 60.0)
            seconds = int(cur_pos - minutes * 60)
            self.panel.lab_time.SetString('%02d:%02d' % (minutes, seconds) + self._time_str_suffix)
            if not self._is_in_drag and not self._is_in_seeking and not self._duration == 0 and not self._is_play_end:
                self.panel.slider.setPercent(float(cur_pos) / float(self._duration) * 100.0)

    def check_can_mouse_scroll(self):
        return False

    def _release_timer(self):
        if self._update_timer:
            global_data.game_mgr.unregister_logic_timer(self._update_timer)
            self._update_timer = None
        return

    def _init_tex_sprite(self):
        provider = VideoPlayer().player.fetch_data_provider()
        render_tex = render.texture('cclive', data_provider=provider)
        spr_cc = CCSprite.CreateWithTexture(cc.Texture2D.createWithITexture(render_tex))
        self.panel.nd_film.AddChild('live_spr', spr_cc)
        spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
        spr_cc.SetPosition('50%', '50%')
        self.live_spr = spr_cc
        self._adjust_spr_scale()
        self._check_spr_shader()

    def _adjust_spr_scale(self):
        full_size = self.panel.nd_film.getContentSize()
        if self.live_spr:
            spr_size = self.live_spr.getContentSize()
            scaleX = min(float(full_size.width / spr_size.width), float(full_size.height / spr_size.height))
            scaleY = scaleX
            if float(abs(full_size.height - full_size.width) / max(full_size.height, full_size.width)) <= 0.26 and spr_size.height - spr_size.width < 0.0:
                scaleY = float(full_size.height / spr_size.height)
                scaleX = float(full_size.width / spr_size.width)
            self.live_spr.setScaleX(scaleX)
            self.live_spr.setScaleY(scaleY)

    def _adjust_panel_fullscreen(self):
        self.is_fullscreen = True
        self.panel.pnl_mask.setVisible(True)
        self.panel.nd_video.setScale(1)
        self.panel.nd_video.setPosition(self.init_pos)

    def _adjust_panel_window(self):
        self.is_fullscreen = False
        self.panel.pnl_mask.setVisible(False)
        max_size = self.nd_video.ConvertToWorldSpacePercentage(100, 100)
        min_size = self.nd_video.ConvertToWorldSpacePercentage(0, 0)
        panel_size = self.panel.getContentSize()
        self.panel.nd_video.setScaleX((max_size.x - min_size.x) / panel_size.width)
        self.panel.nd_video.setScaleY((max_size.y - min_size.y) / panel_size.height)
        pos_s = self.nd_video.ConvertToWorldSpacePercentage(50, 50)
        pos_s = self.panel.convertToNodeSpace(pos_s)
        self.panel.nd_video.setPosition(pos_s)

    def _check_spr_shader(self):
        if not self.live_spr:
            return
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
            from logic.comsys.effect.ui_effect import create_shader
            gl_yuv = create_shader('yuv_texture', 'yuv_texture')
            program_yuv = cc.GLProgramState.getOrCreateWithGLProgram(gl_yuv)
            self.live_spr.setGLProgramState(program_yuv)

    def on_finalize_panel(self):
        if self._close_cb:
            self._close_cb()
        if global_data.video_player.hashed_video_path == self.video_url:
            global_data.video_player.stop_video()
        self._close_cb = None
        self._ready_cb = None
        self._stop_cb = None
        self.video_url = None
        self._release_timer()
        super(VideoWindowCtrlUI, self).on_finalize_panel()
        return