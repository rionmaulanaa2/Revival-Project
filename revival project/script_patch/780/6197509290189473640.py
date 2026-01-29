# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/CommonCountdownWidget.py
from __future__ import absolute_import
from logic.gcommon.time_utility import get_readable_time

class CommonCountdownWidget(object):

    def __init__(self, panel, activity_type):
        self.panel = panel
        self.price_widget = None
        self._activity_type = activity_type
        self.on_init_panel()
        return

    def on_init_panel(self):
        self._timer = 0
        self.tick()
        self.register_timer()

    def on_finalize_panel(self):
        self.unregister_timer()
        self.panel = None
        return

    def tick(self):
        if not self.panel and self.panel.isValid():
            self.unregister_timer()
            return
        from logic.gutils.activity_utils import get_left_time
        left_time = get_left_time(self._activity_type)
        text = get_readable_time(left_time)
        self.panel.left_time.SetString(text)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.tick, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def refresh_panel(self):
        pass