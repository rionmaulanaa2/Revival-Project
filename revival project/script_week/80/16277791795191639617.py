# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/GameRuleDescUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import common.utilities

class GameRuleDescUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/game_describe'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kargs):
        self.on_init_btn()
        self.panel.PlayAnimation('appear')

    def on_init_btn(self):

        @self.panel.callback()
        def OnClick(btn, touch):
            self.close()

    def set_show_rule(self, title, rule):
        import cc
        self.panel.lab_title.SetString(title)
        self.panel.list_content.SetInitCount(1)
        text_item = self.panel.list_content.GetItem(0)
        text_item.lab_describe.SetString(rule)
        text_item.lab_describe.formatText()
        sz = text_item.lab_describe.GetTextContentSize()
        sz.height += 20
        old_sz = text_item.getContentSize()
        text_item.setContentSize(cc.Size(old_sz.width, sz.height))
        text_item.RecursionReConfPosition()
        old_inner_size = self.panel.list_content.GetInnerContentSize()
        self.panel.list_content.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.list_content.GetContainer()._refreshItemPos()
        self.panel.list_content._refreshItemPos()

    def set_node_pos(self, wpos, anchor):
        import cc
        from logic.gutils import template_utils
        self.panel.nd_game_describe.setAnchorPoint(anchor)
        template_utils.set_node_position_in_screen(self.panel.nd_game_describe, self.panel, wpos)

    def set_lottery_rule(self, title, rule):
        if isinstance(rule, list):
            content = []
            for line_content in rule:
                if isinstance(line_content, list):
                    text_id, text_args = line_content
                    text_args = {k:get_text_by_id(v) if 1 else v for k, v in six.iteritems(text_args) if isinstance(v, int)}
                    line_content = get_text_by_id(text_id).format(**text_args)
                else:
                    line_content = get_text_by_id(line_content)
                content.append(line_content)

            content = '\n'.join(content)
        elif isinstance(rule, six.string_types):
            content = rule
        else:
            content = get_text_by_id(rule)
        self.set_show_rule(title, content)