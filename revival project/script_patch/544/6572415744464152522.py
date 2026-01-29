# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewMechaFullScreen.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils, mall_utils, item_utils
from common.cinematic.VideoPlayer import VideoPlayer
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA, get_text_by_id

class NewMechaFullScreen(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_mecha_2/open_mecha_2'
    APPEAR_ANIM = 'appear'
    LOOP_START_TIME = 0.1
    LOOP_ANIM = 'loop'
    LASTING_TIME = 1
    VIDEO_PATH = None

    def on_init_panel(self, *args):
        super(NewMechaFullScreen, self).on_init_panel(*args)
        self.play_loop_anim()
        self.play_video()

    def set_content(self):
        goods_id = '101008023'

        @self.panel.btn_buy.callback()
        def OnClick(btn, touch):
            jump_to_ui_utils.jump_to_mall(goods_id)
            self.close()

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def on_finalize_panel(self):
        super(NewMechaFullScreen, self).on_finalize_panel()
        VideoPlayer().stop_video()

    def play_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return

    def do_hide_panel(self):
        super(NewMechaFullScreen, self).do_hide_panel()
        VideoPlayer().stop_video()

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