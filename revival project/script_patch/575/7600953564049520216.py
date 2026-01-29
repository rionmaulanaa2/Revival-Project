# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ActivityCalendarShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase

class ActivityShareCreator(ShareTemplateBase):
    KIND = ''
    NODE_TO_HIDE = []
    NODE_TO_SHOW = []
    CALENDAR_WIDGET_CLS = None

    def __init__(self, share_kind, calendar_wdiget_cls=ActivityCalendarBase, node_to_hide=None, node_to_show=None):
        super(ActivityShareCreator, self).__init__()
        self.KIND = share_kind
        self.CALENDAR_WIDGET_CLS = calendar_wdiget_cls
        self.NODE_TO_HIDE = node_to_hide or []
        self.NODE_TO_SHOW = node_to_show or []

    @async_disable_wrapper
    def create(self, parent=None, init_cb=None, tmpl=None):
        super(ActivityShareCreator, self).create(parent, tmpl)
        self._calendar_widget = self.CALENDAR_WIDGET_CLS(self.panel, accept_event=False)
        for node_name in self.NODE_TO_HIDE:
            node = getattr(self.panel, node_name, None)
            node and node.setVisible(False)

        for node_name in self.NODE_TO_SHOW:
            node = getattr(self.panel, node_name, None)
            node and node.setVisible(True)

        idx = 1
        while 1:
            item = getattr(self.panel, 'caijian_item%d' % idx, None)
            if item is None:
                break
            item.setClippingEnabled(False)
            idx += 1

        if callable(init_cb):
            init_cb()
        return

    def destroy(self):
        if self._calendar_widget:
            self._calendar_widget.destroy()
        self._calendar_widget = None
        super(ActivityShareCreator, self).destroy()
        return