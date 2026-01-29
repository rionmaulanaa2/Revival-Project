# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202202/ActivityBackToSchoolTask.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollectNew import ActivityCollectNew
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import activity_utils

class ActivityBackToSchoolTask(ActivityCollectNew):

    def __init__(self, dlg, activity_type):
        super(ActivityBackToSchoolTask, self).__init__(dlg, activity_type)

    def on_init_panel(self):
        super(ActivityBackToSchoolTask, self).on_init_panel()
        self.init_describe()
        start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
        self.panel.lab_time.SetString('{}-{}'.format(start_str, end_str))
        self.panel.act_list_common.setVisible(True)
        self.panel.act_list.setVisible(False)

    def init_describe(self):
        btn_describe = self.panel.btn_see
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        act_name_id = conf.get('iCatalogID', '')

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))