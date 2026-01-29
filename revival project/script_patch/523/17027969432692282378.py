# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity51Bicycle.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import activity_utils

class Activity51Bicycle(ActivityCollect):

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.panel.PlayAnimation('show')
        animation_time = self.panel.GetAnimationMaxRunTime('show')

        def finished_show():
            self.panel.PlayAnimation('loop')

        self.panel.SetTimeOut(animation_time, finished_show)
        self.show_list()

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))