# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityBindTT.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityBindTT(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityBindTT, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        pass

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        self.refresh_btn()
        self.panel.PlayAnimation('appear')

    def refresh_btn(self, *args):
        btn = self.panel.nd_content.temp_btn.btn_common_big
        btn.SetEnable(True)
        btn.SetText(81331)

        @btn.callback()
        def OnClick(*args):
            import game3d
            game3d.open_url('https://cdn.i52tt.com/web/frontend-web-activity-nsh-game-book-2310/index.html')

        global_data.emgr.refresh_activity_redpoint.emit()