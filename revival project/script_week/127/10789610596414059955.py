# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLoopCollectionAccumulate.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityArtCollectionAccumulate import ActivityArtCollectionAccumulate
from common.cfg import confmgr
from logic.gutils import task_utils, loop_lottery_utils

class ActivityLoopCollectionAccumulate(ActivityArtCollectionAccumulate):

    def init_parameters(self):
        super(ActivityLoopCollectionAccumulate, self).init_parameters()
        ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.loop_lottery_id = ui_data.get('loop_lottery_id')
        self.loop_template_id = loop_lottery_utils.get_loop_lottery_template_id(self.loop_lottery_id)

    def get_reward_list(self, reward_id):
        if self.loop_lottery_id and self.loop_template_id:
            return loop_lottery_utils.get_loop_lottery_reward_list(reward_id, self.loop_lottery_id, self.loop_template_id)
        else:
            return []