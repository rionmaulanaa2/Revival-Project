# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityXiaoheihe.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityXiaoheihe(ActivityBase):

    def on_init_panel(self):

        @self.panel.temp_btn_get.btn_major.unique_callback()
        def OnClick(*args):
            self.on_click_goto()

    def on_click_goto(self, *args):
        import game3d
        game3d.open_url('https://api.xiaoheihe.cn/v3/bbs/app/api/web/share?link_id=55851492')