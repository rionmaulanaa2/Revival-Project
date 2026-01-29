# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaaiMatchTeammate.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
import cc

class ActivityKizunaaiMatchTeammate(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaaiMatchTeammate, self).__init__(dlg, activity_type)

    def on_init_panel(self):
        self.panel.lab_date.SetString(608547)
        self.panel.PlayAnimation('show')
        act0 = cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show'))
        act1 = cc.CallFunc.create(lambda : self.panel.PlayAnimation('btn_loop'))
        self.panel.runAction(cc.Sequence.create([act0, act1]))

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch, *args):
            ui = global_data.ui_mgr.show_ui('TeamHallUI', 'logic.comsys.lobby.TeamHall')
            ui.select_tab(1)

        global_data.player.call_server_method('attend_activity', (self._activity_type,))