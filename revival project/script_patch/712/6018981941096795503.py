# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ActivityAIConcertCalendarShareCreator.py
from __future__ import absolute_import
from logic.manager_agents.manager_decorators import sync_exec
from common.uisys.uielment.CCSprite import CCSprite
from logic.comsys.share.ActivityCalendarShareCreator import ActivityShareCreator
from logic.comsys.activity.ActivityAIConcert.ActivityAIConcertCalendarMainUI import ActivityAIConcertCalendarBase

class ActivityAIConcertShareCreator(ActivityShareCreator):
    KIND = 'I_SHARE_AI_CONCERT_CALENDAR'
    NODE_TO_HIDE = ['btn_close', 'btn_question', 'nd_dec', 'img_bg', 'bar_bg1', 'img_bg', 'pnl_bg', 'vx_renwu_caijian_01', 'img_name_bg1', 'nd_line']
    NODE_TO_SHOW = ['img_share_all']
    CALENDAR_WIDGET_CLS = ActivityAIConcertCalendarBase

    def __init__(self):
        super(ActivityAIConcertShareCreator, self).__init__(self.KIND, self.CALENDAR_WIDGET_CLS, self.NODE_TO_HIDE, self.NODE_TO_SHOW)

    def create(self, parent=None, init_cb=None, tmpl=None):
        super(ActivityAIConcertShareCreator, self).create(parent, init_cb, tmpl)
        self.panel.vx_renwu_caijian_02.setClippingEnabled(False)
        self.panel.vx_renwu_caijian_03.setClippingEnabled(False)
        i = 1
        while True:
            img_tag_open = getattr(self.panel, 'img_tag_open' + str(i), None)
            if img_tag_open is None:
                break
            for node in img_tag_open._nameless_children:
                if type(node) == CCSprite:
                    node.setVisible(False)

            i += 1

        return

    def destroy(self):
        if self._calendar_widget:
            self._calendar_widget.destroy()
        self._calendar_widget = None
        super(ActivityShareCreator, self).destroy()
        return