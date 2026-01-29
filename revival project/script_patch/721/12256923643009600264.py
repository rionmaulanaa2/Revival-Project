# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/GameDescCenterUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import common.utilities

class GameDescCenterUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/game_describe_big'
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
        self.panel.lab_title.SetString(title)
        self.panel.list_content.SetInitCount(1)
        text_item = self.panel.list_content.GetItem(0)
        text_item.lab_describe.SetString(rule)
        text_item.lab_describe.formatText()
        sz = text_item.lab_describe.getTextContentSize()
        sz.height += 20
        text_item.setContentSize(sz)
        text_item.RecursionReConfPosition()
        self.panel.list_content.SetInnerContentSize(sz.width, sz.height)
        self.panel.list_content.GetContainer()._refreshItemPos()
        self.panel.list_content._refreshItemPos()