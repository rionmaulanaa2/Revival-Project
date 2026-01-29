# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/RebateUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
import cc

class RebateUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_new_domestic/i_test_refund_pop'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_close.OnClick': 'close',
       'btn_close.btn_common.OnClick': 'close',
       'btn_refund.btn_common.OnClick': '_on_click_refund'
       }

    def on_init_panel(self):
        self.panel.PlayAnimation('appear')
        text_item = self.panel.lab_content.GetItem(0)
        text_item.lab_content.SetString(607456)
        text_item.lab_content.formatText()
        sz = text_item.lab_content.getTextContentSize()
        old_sz = text_item.getContentSize()
        text_item.setContentSize(cc.Size(old_sz.width, sz.height))
        text_item.RecursionReConfPosition()
        old_inner_size = self.panel.lab_content.GetInnerContentSize()
        self.panel.lab_content.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.lab_content.GetContainer()._refreshItemPos()
        self.panel.lab_content._refreshItemPos()

    def _on_click_refund(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_to_activity
        jump_to_activity('157')
        self.close()