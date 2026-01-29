# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChristmas/ActivityChristmasFirstCharge.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.jump_to_ui_utils import jump_to_charge
from logic.gcommon.time_utility import get_server_time
from common.cfg import confmgr

class ActivityChristmasFirstCharge(ActivityBase):

    def on_init_panel(self):

        @self.panel.btn_go.callback()
        def OnClick(btn, touch):
            jump_to_charge(0)

        self.panel.PlayAnimation('show')
        activity_conf = confmgr.get('c_activity_config', self._activity_type)
        ui_data = activity_conf['cUiData']
        self.panel.lab_desc.SetString(ui_data['pre_text'] if get_server_time() < ui_data['restart_ts'] else ui_data['after_text'])

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(activity_conf['cNameTextID']), get_text_by_id(activity_conf['cRuleTextID']))