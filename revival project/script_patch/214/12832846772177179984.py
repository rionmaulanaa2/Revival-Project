# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewSkinOne.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import advance_utils

class ActivityNewSkinOne(ActivityBase):

    def on_init_panel(self):
        self._refresh_content()
        global_data.emgr.player_item_update_event_with_id += self._refresh_content

    def on_finalize_panel(self):
        global_data.emgr.player_item_update_event_with_id -= self._refresh_content

    def _refresh_content(self, *args):
        advance_utils.set_new_skin_one(self.panel)