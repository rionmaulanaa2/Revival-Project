# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/ActivityAIConcertCalendar.py
from __future__ import absolute_import
from logic.comsys.share.ActivityAIConcertCalendarShareCreator import ActivityAIConcertShareCreator
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.comsys.activity.ActivityAIConcert.ActivityAIConcertCalendarMainUI import ActivityAIConcertCalendarBase

class ActivityAIConcertCalendar(ActivityTemplate):

    def on_init_panel(self):
        self.calendar_widget = ActivityAIConcertCalendarPage(self.panel)

    def on_finalize_panel(self):
        super(ActivityAIConcertCalendar, self).on_finalize_panel()
        self.calendar_widget.on_finalize_panel()


class ActivityAIConcertCalendarPage(ActivityAIConcertCalendarBase):
    SHARE_CREATOR = ActivityAIConcertShareCreator
    SHARE_NEED_BLACK_BG = False

    def __init__(self, panel, jump_cb=None, play_animation=True):
        self.SHARE_ARGS = {}
        super(ActivityAIConcertCalendarPage, self).__init__(panel, jump_cb, play_animation)

    def _refresh_share_btn(self, has_shared):
        self.panel.btn_share1.setVisible(not has_shared)
        self.panel.btn_share2.setVisible(has_shared)