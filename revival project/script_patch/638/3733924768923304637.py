# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/SpringFestivalCalendarShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.activity.Activity202201.ActivitySpringFestivalCalendarMainUI import ActivitySpringFestivalCalendarBase
from logic.manager_agents.manager_decorators import sync_exec

class SpringFestivalCalendarShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_SPRING_FESTIVAL_CALENDAR_2022'

    def __init__(self):
        super(SpringFestivalCalendarShareCreator, self).__init__()

    @async_disable_wrapper
    def create(self, parent=None, init_cb=None, tmpl=None):
        super(SpringFestivalCalendarShareCreator, self).create(parent, tmpl)
        self.panel.setScale(1.0)
        self._christmas_calendar_widget = AcitivitySpringFestivalCalendarShare(self.panel)
        node_to_hide = [
         self.panel.btn_question]
        node_to_show = []
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

        self.hide_all_player_head_nodes()
        if callable(init_cb):
            init_cb()
        return

    def destroy(self):
        if self._christmas_calendar_widget:
            self._christmas_calendar_widget.destroy()
        self._christmas_calendar_widget = None
        super(SpringFestivalCalendarShareCreator, self).destroy()
        return


class AcitivitySpringFestivalCalendarShare(ActivitySpringFestivalCalendarBase):

    def play_show_animation(self):
        self.panel.img_bg.setVisible(True)


class ActivitySpringFestivalFreeMecha(ShareTemplateBase):

    def create(self, parent=None, tmpl=None):
        super(ActivitySpringFestivalFreeMecha, self).create(parent, 'activity/activity_202201/spring_mecha_free/spring_mecha_free_share')
        from logic.gutils.advance_utils import set_free_mecha_content
        set_free_mecha_content(self.panel)