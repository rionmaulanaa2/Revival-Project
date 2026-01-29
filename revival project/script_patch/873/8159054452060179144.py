# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/FirstChargeResetAdvanceUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils.jump_to_ui_utils import jump_to_charge
from logic.gcommon.time_utility import get_server_time
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import activity_const

class FirstChargeResetAdvanceUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202201/bg_open_first_charge'
    APPEAR_ANIM = 'show'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn_go',
       'btn_question.OnClick': 'on_click_btn_question'
       }

    def on_init_panel(self, *args):
        self._activity_type = activity_const.ACTIVITY_CHRISTMAS_RESTART
        super(FirstChargeResetAdvanceUI, self).on_init_panel()

    def set_content(self):
        super(FirstChargeResetAdvanceUI, self).set_content()
        self.panel.lab_desc.SetString(610328)

    def on_click_btn_go(self, *args):
        self.close()
        jump_to_charge(0)

    def on_click_btn_question(self, *args):
        activity_conf = confmgr.get('c_activity_config', self._activity_type)
        dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(get_text_by_id(activity_conf['cNameTextID']), get_text_by_id(activity_conf['cRuleTextID']))

    def get_close_node(self):
        return (
         self.panel.btn_close,)