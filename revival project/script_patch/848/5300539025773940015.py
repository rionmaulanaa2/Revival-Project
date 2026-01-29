# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewRoleFullScreen.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils import jump_to_ui_utils
from logic.gutils import advance_utils
from common.cinematic.VideoPlayer import VideoPlayer
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA

class NewRoleFullScreen(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202201/open_yutong'
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = 'loop'
    LASTING_TIME = 0.7
    NEED_GAUSSIAN_BLUR = False
    VIDEO_PATH = None

    def on_init_panel(self, *args):
        cur_lang = get_cur_text_lang()
        self.APPEAR_ANIM = 'show'
        self.LASTING_TIME = self.panel.GetAnimationMaxRunTime(self.APPEAR_ANIM)
        super(NewRoleFullScreen, self).on_init_panel(*args)
        self.process_event(True)
        self.play_video()

    def on_finalize_panel(self):
        self.process_event(False)
        super(NewRoleFullScreen, self).on_finalize_panel()
        VideoPlayer().stop_video()

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)

    def set_content(self):
        from logic.gcommon.common_const import activity_const
        if self.VIDEO_PATH:
            advance_utils.set_new_role(self.panel, activity_const.ACTIVITY_ROLE_26, has_video=True)
        else:
            advance_utils.set_new_role(self.panel, activity_const.ACTIVITY_ROLE_26, has_video=False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.set_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def play_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return

    def do_show_panel(self):
        super(NewRoleFullScreen, self).do_show_panel()
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return