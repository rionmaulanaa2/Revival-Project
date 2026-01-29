# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmChargeNew.py
from __future__ import absolute_import
from common.cfg import confmgr
from .ActivityProgressTasks import ActivityProgressTasks
CORE_REWARD_ID = 203800006

class ActivityGranbelmChargeNew(ActivityProgressTasks):

    def _custom_init_panel(self):
        super(ActivityGranbelmChargeNew, self)._custom_init_panel()
        from logic.gutils.item_utils import get_lobby_item_name
        self.panel.lab_name.SetString(get_lobby_item_name(CORE_REWARD_ID))

        @self.panel.btn_details.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.item_utils import jump_to_ui_new
            jump_to_ui_new(CORE_REWARD_ID)

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            conf = confmgr.get('c_activity_config', self._activity_type)
            act_name_id = conf['cNameTextID']
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))