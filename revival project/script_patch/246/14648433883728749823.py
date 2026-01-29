# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/FairylandCalendarShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.activity.ActivityFairyland.ActivityFairylandCalendarMainUI import ActivityFairylandCalendarBase
from logic.manager_agents.manager_decorators import sync_exec
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA

class FairylandCalendarShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_FAIRYLAND_CALENDAR'

    def __init__(self):
        super(FairylandCalendarShareCreator, self).__init__()

    @async_disable_wrapper
    def create(self, parent=None, init_cb=None, tmpl=None):
        super(FairylandCalendarShareCreator, self).create(parent, tmpl)
        self._fairyland_calendar_widget = AcitivityFairylandCalendarShare(self.panel)
        cur_lang = get_cur_text_lang()
        if cur_lang == LANG_EN:
            self.panel.nd_title.setScale(0.85)
        node_to_hide = [
         self.panel.btn_close]
        idx = 1
        while 1:
            item = getattr(self.panel, 'caijian_item%d' % idx, None)
            if item is None:
                break
            item.setClippingEnabled(False)
            idx += 1

        for node in node_to_hide:
            node.setVisible(False)

        if callable(init_cb):
            init_cb()
        return

    def destroy(self):
        if self._fairyland_calendar_widget:
            self._fairyland_calendar_widget.destroy()
        self._fairyland_calendar_widget = None
        super(FairylandCalendarShareCreator, self).destroy()
        return


class AcitivityFairylandCalendarShare(ActivityFairylandCalendarBase):

    def play_show_animation(self):
        pass