# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/ActivitySpringFreeMecha.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate

class ActivitySpringFreeMecha(ActivityTemplate):

    def on_init_panel(self):
        self.set_content()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.set_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_content(self, *args):
        from logic.gutils.advance_utils import set_free_mecha_content
        set_free_mecha_content(self.panel, False)