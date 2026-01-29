# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerCalendar.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from .ActivitySummerCalendarMainUI import ActivitySummerCalendarBase

class ActivitySummerCalendar(ActivityTemplate):
    PANEL_CONFIG_NAME = 'activity/activity_202107/calendar/i_activity_summer_calendar'

    def on_init_panel(self):
        self.calendar_widget = ActivitySummerCalendarTabPage(self.panel)

    def on_finalize_panel(self):
        super(ActivitySummerCalendar, self).on_finalize_panel()
        self.calendar_widget.on_finalize_panel()


class ActivitySummerCalendarTabPage(ActivitySummerCalendarBase):
    VIDEO_PATH = 'video/activity_calendar_bg.mp4'
    SHARE_TASK_ID = '1430038'

    def __init__(self, panel):
        super(ActivitySummerCalendarTabPage, self).__init__(panel)
        self.process_event(True)
        self.refresh_share()

    def play_show_animation(self):
        self.panel.img_bg_02.setVisible(False)
        global_data.video_player.play_video(self.VIDEO_PATH, None, {}, 0, None, True, video_ready_cb=self.on_video_ready, disable_sound_mgr=False)
        super(ActivitySummerCalendarTabPage, self).play_show_animation()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.refresh_share
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_share(self, *args):
        reward_recv = global_data.player.has_receive_reward(self.SHARE_TASK_ID)
        self.panel.lab_share.SetString(603013 if reward_recv else 609717)
        if global_data.player.has_unreceived_task_reward(self.SHARE_TASK_ID):
            global_data.player.receive_task_reward(self.SHARE_TASK_ID)

    def init_panel(self):
        super(ActivitySummerCalendarTabPage, self).init_panel()
        if global_data.is_pc_mode:
            self.panel.nd_share.setVisible(False)
            return

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI(parent=self.panel)

            def init_cb():
                if share_ui and share_ui.is_valid():
                    share_ui.set_share_content_raw(self._share_content.get_show_render_texture(), need_scale=True, share_content=self._share_content)
                    share_ui.set_save_content(self._share_content.get_save_render_texture())

                    def share_inform_func():
                        if global_data.player:
                            global_data.player.share_activity('activity_10521')
                            global_data.player.share()
                        self.refresh_share()

                    share_ui.set_share_inform_func(share_inform_func)

            if not getattr(self, '_share_content', None):
                from logic.comsys.share.SummerCalendarShareCreator import SummerCalendarShareCreator
                self._share_content = SummerCalendarShareCreator()
                self._share_content.create(parent=None, init_cb=init_cb)
            else:
                init_cb()
            return

    def on_video_ready(self):
        self.panel.SetTimeOut(0.1, lambda : self.panel.img_bg.setVisible(False))

    def jump_from_item(self, idx):
        super(ActivitySummerCalendarTabPage, self).jump_from_item(idx)
        if idx == 1:
            global_data.ui_mgr.close_ui('ActivitySummerMainUI')

    def on_finalize_panel(self):
        self.process_event(False)
        if global_data.video_player.video_name == self.VIDEO_PATH:
            global_data.video_player.stop_video()