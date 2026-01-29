# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChristmas/ActivityChristmasCalendar.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from .ActivityChristmasCalendarMainUI import ActivityChristmasCalendarBase

class ActivityChristmasCalendar(ActivityTemplate):

    def on_init_panel(self):
        self.calendar_widget = ActivityChristmasCalendarTabPage(self.panel)

    def on_finalize_panel(self):
        super(ActivityChristmasCalendar, self).on_finalize_panel()
        self.calendar_widget.on_finalize_panel()


class ActivityChristmasCalendarTabPage(ActivityChristmasCalendarBase):
    SHARE_TASK_ID = '1430415'

    def __init__(self, panel):
        super(ActivityChristmasCalendarTabPage, self).__init__(panel)
        self.process_event(True)
        self.refresh_share()

    def play_show_animation(self):
        super(ActivityChristmasCalendarTabPage, self).play_show_animation()
        self.panel.nd_content.setVisible(True)

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
        if global_data.player.has_unreceived_task_reward(self.SHARE_TASK_ID):
            global_data.player.receive_task_reward(self.SHARE_TASK_ID)
        self._refresh_share_btn(global_data.player.has_receive_reward(self.SHARE_TASK_ID))

    def init_panel(self):
        super(ActivityChristmasCalendarTabPage, self).init_panel()
        self.panel.btn_question.setVisible(False)

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI(parent=self.panel)

            def init_cb():
                if share_ui and share_ui.is_valid():
                    share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

                    def share_inform_func():
                        if global_data.player:
                            global_data.player.share_activity('activity_20503')
                            global_data.player.share()
                        self.refresh_share()

                    share_ui.set_share_inform_func(share_inform_func)

            if not getattr(self, '_share_content', None):
                from logic.comsys.share.ChristmasCalendarShareCreator import ChristmasCalendarShareCreator
                self._share_content = ChristmasCalendarShareCreator()
                self._share_content.create(parent=None, init_cb=init_cb)
            else:
                init_cb()
            return

    def jump_from_item(self, idx):
        super(ActivityChristmasCalendarTabPage, self).jump_from_item(idx)
        if idx == 1:
            global_data.ui_mgr.close_ui('ActivityChristmasMainUI')

    def on_finalize_panel(self):
        self.process_event(False)

    def _refresh_share_btn(self, has_shared):
        self.panel.btn_share1.setVisible(not has_shared)
        self.panel.btn_share2.setVisible(has_shared)