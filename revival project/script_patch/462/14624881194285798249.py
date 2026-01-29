# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoListCtrlUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, BG_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.uielment.CCSprite import CCSprite
import render
import game3d
import cclive
import cc
import six_ex

class VideoListCtrlUI(BasePanel):
    PANEL_CONFIG_NAME = 'login/login_film_new'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *args, **kwargs):
        self._click_cb = None
        self._on_drag_begin_cb = None
        self._on_drag_cb = None
        self._on_drag_end_cb = None
        self.spr_clip_enable = True
        self.enable_touch_close = False
        self.init_widget()
        self.spr_cc_dict = {}
        print('init movie dialog')
        return

    def set_touch_close_enable(self, enable):
        self.enable_touch_close = enable

    def set_spr_clip_enable(self, enable):
        self.spr_clip_enable = enable

    def init_widget(self):
        self._nd_touch_IDs = []
        self._total_drag = 0.0
        self.panel.lab.SetString('')
        self.init_event()

    def set_zorder_bottom(self):
        self.set_template_zorder(BG_ZORDER)

    def show_tex_sprite(self):
        visible = self.spr_cc_dict[0].IsVisible()
        self.spr_cc_dict[0].setVisible(not visible)
        len(self.spr_cc_dict) > 1 and self.spr_cc_dict[1].setVisible(visible)

    def init_tex_sprite(self, video_index):
        from common.cinematic.VideoListPlayer import VideoListPlayer
        player = VideoListPlayer().get_player(video_index)
        provider = player.fetch_data_provider()
        try:
            render_tex = render.texture('cclive', data_provider=provider)
        except ValueError:
            log_error('not support dynamic texutue.')
            return

        rt = cc.Texture2D.createWithITexture(render_tex)
        if len(self.spr_cc_dict) < 2:
            spr_cc = CCSprite.CreateWithTexture(rt)
            self.panel.nd_live.AddChild('live_spr', spr_cc)
            video_index %= 2
            self.spr_cc_dict[video_index] = spr_cc
        else:
            visible = self.spr_cc_dict[0].IsVisible()
            if visible:
                next_show_spr_cc_index = 1
            else:
                next_show_spr_cc_index = 0
            spr_cc = self.spr_cc_dict[next_show_spr_cc_index]
            spr_cc.setTexture(rt)
        spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
        spr_cc.SetPosition('50%', '50%')
        self.adjust_spr_scale(spr_cc)
        self.check_spr_shader(spr_cc)
        spr_cc.setVisible(False)

    def adjust_spr_scale(self, spr):
        spr_size = spr.getContentSize()
        lb_point = self.panel.nd_live.convertToWorldSpace(cc.Vec2(0, 0))
        rt_point = self.panel.nd_live.convertToWorldSpace(cc.Vec2(spr_size.width, spr_size.height))
        w, h = rt_point.x - lb_point.x, rt_point.y - lb_point.y
        design_size = global_data.ui_mgr.design_screen_size
        if self.spr_clip_enable:
            scale = max(design_size.width / w, design_size.height / h)
        else:
            scale = min(design_size.width / w, design_size.height / h)
        spr.setScale(scale)

    def check_spr_shader(self, spr):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
            from logic.comsys.effect.ui_effect import create_shader
            gl_yuv = create_shader('yuv_texture', 'yuv_texture')
            program_yuv = cc.GLProgramState.getOrCreateWithGLProgram(gl_yuv)
            spr.setGLProgramState(program_yuv)

    def init_event(self):
        self.panel.nd_touch.BindMethod('OnClick', self.on_click_video)
        self.panel.nd_touch.BindMethod('OnBegin', self.on_drag_video_begin)
        self.panel.nd_touch.BindMethod('OnDrag', self.on_drag_video)
        self.panel.nd_touch.BindMethod('OnEnd', self.on_drag_video_end)

    def set_interaction_cb(self, click_cb=None, drag_begin_cb=None, drag_cb=None, drag_end_cb=None):
        self._click_cb = click_cb
        self._on_drag_begin_cb = drag_begin_cb
        self._on_drag_cb = drag_cb
        self._on_drag_end_cb = drag_end_cb

    def on_click_video(self, *args):
        if self.enable_touch_close:
            if self._click_cb:
                self._click_cb()
                return
            from common.cinematic.VideoListPlayer import VideoListPlayer
            video = VideoListPlayer().get_cur_video()
            if video:
                video.stop_video()

    def on_drag_video_begin(self, layer, touch):
        if len(self._nd_touch_IDs) > 1:
            return False
        tid = touch.getId()
        if tid not in self._nd_touch_IDs:
            self._nd_touch_IDs.append(tid)
        self._total_drag = 0.0
        if self._on_drag_begin_cb:
            self._on_drag_begin_cb()
        return True

    def on_drag_video(self, layer, touch):
        if not self.enable_touch_close:
            return
        tid = touch.getId()
        if tid not in self._nd_touch_IDs:
            return
        if len(self._nd_touch_IDs) == 1:
            delta_pos = touch.getDelta()
            self._total_drag += abs(touch.getDelta().x) + abs(touch.getDelta().y)
        if self._on_drag_cb:
            self._on_drag_cb(self._total_drag)

    def on_drag_video_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
        if self._on_drag_end_cb:
            self._on_drag_end_cb()

    def on_finalize_panel(self):
        print('videoDialog close')
        super(VideoListCtrlUI, self).on_finalize_panel()

    def set_nd_tips_visible(self, nd_name, visible):
        if not nd_name or not getattr(self, nd_name):
            return
        nd = getattr(self, nd_name)
        nd.setVisible(visible)

    def play_animation(self, anim_name):
        if not anim_name or not self.panel.HasAnimation(anim_name):
            return
        self.panel.PlayAnimation(anim_name)

    def show_dialog(self, txt_id):
        self.panel.lab.setOpacity(0)
        self.panel.lab.SetString(txt_id)
        self.panel.PlayAnimation('show')

    def hide_dialog(self):
        self.panel.lab.SetString('')

    def on_resolution_changed(self):
        if self.panel.nd_live.live_spr:
            for spr_cc in six_ex.values(self.spr_cc_dict):
                if spr_cc and spr_cc.isValid():
                    spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
                    spr_cc.SetPosition('50%', '50%')
                    self.adjust_spr_scale(spr_cc)