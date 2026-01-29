# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202212/ActivityKizunaFreeCD.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import jump_to_ui_utils

class ActivityKizunaFreeCD(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaFreeCD, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.activity_conf = conf

    def on_init_panel(self):
        self.init_btn_goto()
        self.init_describe()

    def on_finalize_panel(self):
        pass

    def init_describe(self):

        @self.panel.lab_title.nd_auto_fit.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

    def init_btn_goto(self):

        @self.panel.btn_setting.unique_callback()
        def OnClick(btn, touch):
            jump_to_ui_utils.jump_to_switch_lobby_music(0)