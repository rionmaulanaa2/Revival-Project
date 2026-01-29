# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/DescribeWidget.py
from __future__ import absolute_import
import cc
from .Widget import Widget
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gcommon.common_utils.local_text import get_text_by_id

class DescribeWidget(Widget):

    def on_init_panel(self):
        super(DescribeWidget, self).on_init_panel()
        conf = confmgr.get('c_activity_config', self._activity_type)
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_describe
        if btn_describe:
            if not conf.get('cRuleTextID', ''):
                btn_describe.setVisible(False)
            else:

                @btn_describe.unique_callback()
                def OnClick(btn, touch):
                    dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                    rule_text = self.get_rule_text()
                    dlg.set_show_rule(get_text_by_id(int(conf.get('cNameTextID', '607171'))), rule_text)
                    x, y = btn_describe.GetPosition()
                    wpos = btn_describe.GetParent().ConvertToWorldSpace(x, y)
                    dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.5, 1.0))
                    template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def get_rule_text(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        return get_text_by_id(conf.get('cRuleTextID', ''))