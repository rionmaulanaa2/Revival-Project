# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFairyland/ActivityFairylandQixi.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import template_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class ActivityFairylandQixi(ActivityBase):

    def on_init_panel(self):
        self.panel.nd_middle.nd_upper_text.lab_title_upper01.SetString(609854)
        self.panel.nd_middle.nd_lower_text.lab_title_upper.SetString(609855)
        self.panel.nd_middle.btn_common.btn_common.SetText(601162)

        @self.panel.nd_middle.btn_common.btn_common.unique_callback()
        def OnClick(*args):
            self.on_click_btn_go()

        @self.panel.nd_title.btn_question.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_question(btn)

    def set_show(self, show, is_init=False):
        super(ActivityFairylandQixi, self).set_show(show, is_init)
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(1.2),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))

    def on_click_btn_go(self, *args):
        ui = global_data.ui_mgr.show_ui('TeamHallUI', 'logic.comsys.lobby.TeamHall')
        ui.select_tab(1)

    def on_click_btn_question(self, btn):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(get_text_by_id(609832), get_text_by_id(609856))
        x, y = btn.GetPosition()
        wpos = btn.GetParent().ConvertToWorldSpace(x, y)
        dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
        template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)