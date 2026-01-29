# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ActivityAnnivCalendarShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ActivityCalendarShareCreator import ActivityShareCreator
from logic.comsys.activity.ActivityAnnivCalendar import ActivityAnnivCalendarBase
from logic.gutils.activity_utils import get_activity_open_time

class ActivityAnnivShareCreator(ActivityShareCreator):
    KIND = 'I_SHARE_ANNIV_CALENDAR'
    NODE_TO_HIDE = ['temp_btn_close', 'btn_share_img', 'lab_share', 'lab_share_first', 'btn_question']
    NODE_TO_SHOW = []
    CALENDAR_WIDGET_CLS = ActivityAnnivCalendarBase

    def __init__(self):
        super(ActivityAnnivShareCreator, self).__init__(self.KIND, self.CALENDAR_WIDGET_CLS, self.NODE_TO_HIDE, self.NODE_TO_SHOW)