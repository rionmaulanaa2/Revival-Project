# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/advertising/TemplateRole1.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils import advance_utils
from common.cinematic.VideoPlayer import VideoPlayer

class TemplateRole1(SimpleAdvance):
    PANEL_CONFIG_NAME = ''
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 0.7
    NEED_GAUSSIAN_BLUR = False
    ACTIVITY_ID = None
    VIDEO_PATH = None

    def on_init_panel(self, *args):
        self.LASTING_TIME = self.panel.GetAnimationMaxRunTime(self.APPEAR_ANIM)
        super(TemplateRole1, self).on_init_panel(*args)
        self.process_event(True)
        self.play_video()

    def on_finalize_panel(self):
        self.process_event(False)
        self.stop_video()
        super(TemplateRole1, self).on_finalize_panel()

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def set_content(self):
        advance_utils.set_new_role(self.panel, self.ACTIVITY_ID, has_video=True if self.VIDEO_PATH else False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.set_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def do_show_panel(self):
        super(TemplateRole1, self).do_show_panel()
        self.play_video()

    def play_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return

    def stop_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().stop_video()