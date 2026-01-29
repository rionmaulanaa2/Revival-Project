# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityDouYu.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr

class ActivityDouYu(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityDouYu, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        btn = self.panel.btn_go

        @btn.unique_callback()
        def OnClick(btn, touch):
            import game3d
            url = 'live.qq.com/api/douyu?type=29&cate_id=1940&cate_name=\xe6\x9c\xba\xe5\x8a\xa8\xe9\x83\xbd\xe5\xb8\x82\xe9\x98\xbf\xe5\xb0\x94\xe6\xb3\x95&is_face=0'
            if game3d.open_url('dydeeplink://' + url):
                return
            game3d.open_url('https://' + url)

        self.panel.PlayAnimation('appear')

    def goto_broadcast(self):
        self.exec_custom_func(0)