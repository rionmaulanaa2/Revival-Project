# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoManualCtrlUI.py
from __future__ import absolute_import
from __future__ import print_function
import cclive
import render
import game3d
from cocosui import cc, ccui
from common.cinematic.VideoPlayer import VideoPlayer
from common.uisys.basepanel import BasePanel
from common.uisys.uielment.CCSprite import CCSprite
from common.const.uiconst import LOADING_ZORDER_ABOVE, UI_VKB_CUSTOM
PLATFORM_TIME = {game3d.PLATFORM_ANDROID: 1000.0,
   game3d.PLATFORM_WIN32: 1000000.0,
   game3d.PLATFORM_IOS: 1000.0
   }

class VideoManualCtrlUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_highlight/video_player'
    DLG_ZORDER = LOADING_ZORDER_ABOVE
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def close_video(self, *args):
        VideoPlayer().stop_video(False)

    def on_stop_video(self, *args):
        self.close()

    def on_play_end(self, *args):
        self._is_play_end = True
        self.panel.btn_play.SetSelect(False)
        self.panel.nd_ui.img_mask_down.slider.setPercent(100)

    def on_seek_to(self, *args):
        if global_data.is_inner_server and global_data.crx_test_video:
            import time
            print(time.time())
            player = VideoPlayer().get_player()
            if player:
                cur_pos = player.current_position / self._time_scale
        self._is_in_seeking = False

    def on_init_panel(self, *args):
        self._time_scale = PLATFORM_TIME.get(game3d.get_platform(), 1)
        self._duration = 0
        self._update_timer = None
        self._time_str_suffix = ''
        self._is_in_drag = False
        self._is_in_seeking = False
        self._is_play_end = False
        self._platform = game3d.get_platform()
        self.init_widget()
        self.hide_main_ui()
        self._init_ctrl_ui()
        return

    def init_widget(self):
        self.panel.lab_title.SetString('')
        self._init_tex_sprite()
        self._init_ui_event()

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
                self.panel.nd_ui.img_mask_down.slider.setPercent(float(cur_pos) / float(self._duration) * 100.0)

    def check_can_mouse_scroll(self):
        return False

    def ui_vkb_custom_func(self):
        self.close()

    def _init_tex_sprite(self):
        from common.cinematic.VideoPlayer import VideoPlayer
        provider = VideoPlayer().player.fetch_data_provider()
        render_tex = render.texture('cclive', data_provider=provider)
        spr_cc = CCSprite.CreateWithTexture(cc.Texture2D.createWithITexture(render_tex))
        self.panel.nd_film.AddChild('live_spr', spr_cc)
        spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
        spr_cc.SetPosition('50%', '50%')
        self._adjust_spr_scale(spr_cc)
        self._check_spr_shader(spr_cc)

    def change_fit_method(self, scale):
        from common.utils.ui_utils import get_scale
        self.panel.nd_film.setScale(get_scale(scale))

    def _adjust_spr_scale(self, spr):
        full_size = self.panel.nd_film.getContentSize()
        spr_size = spr.getContentSize()
        scale = min(float(full_size.width / spr_size.width), float(full_size.height / spr_size.height))
        spr.setScale(scale)

    def _check_spr_shader(self, spr):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
            from logic.comsys.effect.ui_effect import create_shader
            gl_yuv = create_shader('yuv_texture', 'yuv_texture')
            program_yuv = cc.GLProgramState.getOrCreateWithGLProgram(gl_yuv)
            spr.setGLProgramState(program_yuv)

    def _init_ui_event(self):
        self.panel.temp_btn_close.btn_back.BindMethod('OnClick', self.close_video)

    def _release_timer(self):
        if self._update_timer:
            global_data.game_mgr.unregister_logic_timer(self._update_timer)
            self._update_timer = None
        return

    def on_finalize_panel(self):
        self.close_video()
        self._release_timer()
        self.show_main_ui()
        super(VideoManualCtrlUI, self).on_finalize_panel()