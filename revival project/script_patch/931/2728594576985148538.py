# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/CountdownWidget.py
from __future__ import absolute_import
from .ActivityWidgetBase import ActivityWidgetBase
from logic.gcommon.time_utility import get_readable_time, get_simply_time

class CountdownWidget(ActivityWidgetBase):

    def on_init_panel(self):
        self._timer = 0
        self.tick()
        self.register_timer()

    def on_finalize_panel(self):
        self.unregister_timer()
        super(CountdownWidget, self).on_finalize_panel()

    def tick(self):
        if not self.panel or self.panel.IsDestroyed():
            self.unregister_timer()
            return
        from logic.gutils.activity_utils import get_left_time
        from logic.gcommon.cdata.loop_activity_data import get_loop_activity_left_time, is_loop_activity
        if is_loop_activity(self.activity_id):
            left_time = get_loop_activity_left_time(self.activity_id)
        else:
            left_time = get_left_time(self.activity_id)
        text = get_readable_time(left_time)
        if self.extra_conf.get('completion', 0):
            text = get_text_by_id(607014).format(text)
        elif self.extra_conf.get('txt_id', 0):
            text = get_text_by_id(self.extra_conf['txt_id']).format(text)
        elif self.extra_conf.get('txt_cb'):
            txt_cb = self.extra_conf.get('txt_cb')
            text = txt_cb(left_time)
        self.panel.SetString(text)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.tick, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0