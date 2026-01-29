# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/advertising/TemplateMecha1.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils
from common.cinematic.VideoPlayer import VideoPlayer

class TemplateMecha1(SimpleAdvance):
    PANEL_CONFIG_NAME = ''
    APPEAR_ANIM = 'appear'
    LOOP_START_TIME = 0.1
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1
    VIDEO_PATH = None
    GOODS_ID = None
    SKIN_ID = None

    def on_init_panel(self, *args):
        super(TemplateMecha1, self).on_init_panel(*args)
        self.play_loop_anim()
        self.play_video()
        if self.SKIN_ID:
            from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
            img_path = get_lobby_item_pic_by_item_no(self.SKIN_ID)
            self.panel.temp_skin.item.SetDisplayFrameByPath('', img_path)

    def set_content(self):

        @self.panel.btn_buy.callback()
        def OnClick(btn, touch):
            jump_to_ui_utils.jump_to_mall(str(self.GOODS_ID))

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def on_finalize_panel(self):
        self.stop_video()
        super(TemplateMecha1, self).on_finalize_panel()

    def play_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return

    def stop_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().stop_video()

    def do_hide_panel(self):
        self.stop_video()
        super(TemplateMecha1, self).do_hide_panel()

    def play_loop_anim(self):
        self.panel.PlayAnimation(self.LOOP_ANIM)

    def on_anim_finish(self):
        close_node = self.get_close_node()
        for nd in close_node:

            @nd.callback()
            def OnClick(*args):
                if callable(self._close_btn_cb):
                    self._close_btn_cb()
                else:
                    self.close()