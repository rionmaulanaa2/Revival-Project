# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/SummerCalendar2022ShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.activity.ActivitySummer.ActivitySummerCalendar2022MainUI import ActivitySummerCalendar2022Base

class SummerCalendar2022ShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_SUMMER_CALENDAR_2022'

    def __init__(self, activity_id):
        self.activity_id = activity_id
        super(SummerCalendar2022ShareCreator, self).__init__()

    @async_disable_wrapper
    def create(self, parent=None, init_cb=None, tmpl=None):
        super(SummerCalendar2022ShareCreator, self).create(parent, tmpl)
        self._calendar_widget = ActivitySummerCalendar2022Share(self.panel, activity_type=self.activity_id)
        node_to_hide = ['btn_close', 'nd_share']
        node_to_show = []
        idx = 1
        while 1:
            item = getattr(self.panel, 'caijian_item%d' % idx, None)
            if item is None:
                break
            item.setClippingEnabled(False)
            idx += 1

        if self.panel.nd_head:
            self.panel.nd_head.setClippingEnabled(False)
        for node in node_to_hide:
            if type(node) == str:
                node = getattr(self.panel, node, None)
            node and node.setVisible(False)

        for node in node_to_show:
            if type(node) == str:
                node = getattr(self.panel, node, None)
            node and node.setVisible(True)

        if callable(init_cb):
            init_cb()
        return

    def destroy(self):
        if self._calendar_widget:
            self._calendar_widget.destroy()
        self._calendar_widget = None
        super(SummerCalendar2022ShareCreator, self).destroy()
        return


class ActivitySummerCalendar2022Share(ActivitySummerCalendar2022Base):

    def play_show_animation(self):
        self.panel.temp_head.PlayAnimation('show_head')