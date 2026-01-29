# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ChristmasCalendarShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.activity.ActivityChristmas.ActivityChristmasCalendarMainUI import ActivityChristmasCalendarBase
from logic.manager_agents.manager_decorators import sync_exec

class ChristmasCalendarShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_CHRISTMAS_CALENDAR'

    def __init__(self):
        super(ChristmasCalendarShareCreator, self).__init__()

    @async_disable_wrapper
    def create(self, parent=None, init_cb=None, tmpl=None):
        super(ChristmasCalendarShareCreator, self).create(parent, tmpl)
        self.panel.setScale(1.0)
        self._christmas_calendar_widget = AcitivityChristmasCalendarShare(self.panel)
        node_to_hide = [
         self.panel.btn_close, self.panel.btn_question, self.panel.img_light_title, self.panel.img_smoke]
        node_to_show = [self.panel.img_share_all]
        idx = 1
        while 1:
            item = getattr(self.panel, 'caijian_item%d' % idx, None)
            if item is None:
                break
            item.setClippingEnabled(False)
            idx += 1

        for node in node_to_hide:
            node.setVisible(False)

        for node in node_to_show:
            node.setVisible(True)

        if callable(init_cb):
            init_cb()
        return

    def destroy(self):
        if self._christmas_calendar_widget:
            self._christmas_calendar_widget.destroy()
        self._christmas_calendar_widget = None
        super(ChristmasCalendarShareCreator, self).destroy()
        return


class AcitivityChristmasCalendarShare(ActivityChristmasCalendarBase):

    def play_show_animation(self):
        self.panel.img_bg.setVisible(True)