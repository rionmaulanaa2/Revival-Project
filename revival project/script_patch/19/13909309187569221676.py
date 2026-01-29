# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202401/ActivityBindAnniversaryH5.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate

class ActivityBindAnniversaryH5(ActivityTemplate):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_resp_cswz_jimu_url': self.on_open_url
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        super(ActivityBindAnniversaryH5, self).init_parameters()

    def on_init_panel(self):
        super(ActivityBindAnniversaryH5, self).on_init_panel()
        self.init_btn_jump_h5()

    def init_btn_jump_h5(self):
        btn_go = self.panel.btn_go

        @btn_go.unique_callback()
        def OnClick(btn, touch):
            global_data.player.pull_jimu_url(self._activity_type)

    def on_open_url(self, url):
        if url:
            import game3d
            game3d.open_url(url)