# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity7DSign.py
from __future__ import absolute_import
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase

class Activity7DSign(ActivityBase):

    def on_init_panel(self):
        import logic.gcommon.time_utility as tutil
        start_time, reward_status, day_no = global_data.player.get_normal_attend_info()
        start_date = tutil.get_date_str('%Y.%m.%d', start_time)
        finish_date = tutil.get_date_str('%Y.%m.%d', start_time + tutil.ONE_WEEK_SECONDS - 1)
        self.panel.lab_describe.SetString('-'.join((start_date, finish_date)))

        @self.panel.temp_btn_sign.btn_major.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('NormalAttendSignUI', 'logic.comsys.activity')