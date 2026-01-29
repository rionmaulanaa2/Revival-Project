# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLoopCollectionCollect.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityArtCollectionCollect import ActivityArtCollectionCollect
from common.cfg import confmgr
from logic.gutils import task_utils, loop_lottery_utils

class ActivityLoopCollectionCollect(ActivityArtCollectionCollect):

    def init_parameters(self):
        self.collect_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default=None)
        ui_data_fix = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.loop_lottery_id = ui_data_fix.get('loop_lottery_id')
        ui_data = loop_lottery_utils.get_loop_lottery_collect_activity_data(self.loop_lottery_id)
        self.loop_template_id = loop_lottery_utils.get_loop_lottery_template_id(self.loop_lottery_id)
        self.ITEM_IMG_CFG = ui_data.get('item_img', {})
        self.template_no = ui_data.get('template', 0)
        self.task_conf = task_utils.get_task_conf_by_id(self.collect_task_id)
        self.prog_rewards = self.task_conf.get('prog_rewards', [])
        self.total_prog = task_utils.get_total_prog(self.collect_task_id)
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        return

    def get_reward_list(self, reward_id):
        if self.loop_lottery_id and self.loop_template_id:
            return loop_lottery_utils.get_loop_lottery_reward_list(reward_id, self.loop_lottery_id, self.loop_template_id)
        else:
            return []