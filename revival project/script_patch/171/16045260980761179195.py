# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWinterCupCompetition.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import jump_to_ui_utils
from logic.client.const import mall_const
from logic.gutils import mall_utils
import logic.gcommon.const as gconst
from logic.gutils import template_utils

class ActivityWinterCupCompetition(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWinterCupCompetition, self).__init__(dlg, activity_type)
        self.init_mall_info()

    def on_finalize_panel(self):
        super(ActivityWinterCupCompetition, self).on_finalize_panel()

    def on_init_panel(self):
        super(ActivityWinterCupCompetition, self).on_init_panel()

    def init_mall_info(self):
        btn = self.panel.btn_go

        @btn.callback()
        def OnClick(_layer, _touch):
            from logic.gcommon.common_const import liveshow_const as live_sc
            from logic.comsys.live.LiveMainUI import LiveMainUI
            live_main = LiveMainUI()
            live_main.change_tab_force(live_sc.HUYA_LIVE)