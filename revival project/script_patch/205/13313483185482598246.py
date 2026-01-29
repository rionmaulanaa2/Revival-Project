# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoCtrlUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, BG_ZORDER
from common.uisys.uielment.CCSprite import CCSprite
import cclive
import render
from cocosui import cc
import game3d
from common.const import uiconst

class VideoCtrlUI(BasePanel):
    PANEL_CONFIG_NAME = 'login/login_film'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *args, **kwargs):
        self.enable_touch_close = True
        self.spr_clip_enable = kwargs.get('clip_enable', True)
        self.init_widget()
        print('init movie dialog')

    def set_touch_close_enable(self, enable):
        self.enable_touch_close = enable

    def init_widget(self):
        self.panel.lab.SetString('')
        self.init_tex_sprite()
        self.init_event()

    def set_zorder_bottom(self):
        self.set_template_zorder(BG_ZORDER)

    def init_tex_sprite(self):
        from common.cinematic.VideoPlayer import VideoPlayer
        provider = VideoPlayer().player.fetch_data_provider()
        try:
            render_tex = render.texture('cclive', data_provider=provider)
        except ValueError:
            log_error('not support dynamic texutue.')
            return

        spr_cc = CCSprite.CreateWithTexture(cc.Texture2D.createWithITexture(render_tex))
        print('video data size')
        print(render_tex.dimension)
        print(render_tex.size)
        self.panel.nd_live.AddChild('live_spr', spr_cc)
        spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
        spr_cc.SetPosition('50%', '50%')
        self.adjust_spr_scale(spr_cc)
        self.check_spr_shader(spr_cc)

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

    def on_click_video(self, *args):
        if self.enable_touch_close:
            from common.cinematic.VideoPlayer import VideoPlayer
            VideoPlayer().stop_video()

    def on_finalize_panel(self):
        print('videoDialog close')
        super(VideoCtrlUI, self).on_finalize_panel()

    def show_dialog(self, txt_id):
        self.panel.lab.setOpacity(0)
        self.panel.lab.SetString(txt_id)
        self.panel.PlayAnimation('show')

    def hide_dialog(self):
        self.panel.lab.SetString('')

    def on_resolution_changed(self):
        if self.panel.nd_live.live_spr:
            spr_cc = self.panel.nd_live.live_spr
            spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
            spr_cc.SetPosition('50%', '50%')
            self.adjust_spr_scale(spr_cc)