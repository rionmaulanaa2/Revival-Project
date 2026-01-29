# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/Widget.py


class Widget(object):

    def __init__(self, panel, activity_type):
        self.panel = panel
        self._activity_type = activity_type
        self.on_init_panel()

    def on_init_panel(self):
        pass

    def on_finalize_panel(self):
        self.panel = None
        return

    def refresh_panel(self):
        pass