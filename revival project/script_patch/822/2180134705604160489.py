# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySeason.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.advance_utils import set_season_small, set_reward_item

class ActivitySeason(ActivityBase):

    def on_init_panel(self):
        global_data.emgr.season_pass_open_type += self._update_season
        set_season_small(self.panel)
        set_reward_item(self.panel)

    def _update_season(self, *args):
        set_season_small(self.panel)

    def on_finalize_panel(self):
        global_data.emgr.season_pass_open_type -= self._update_season