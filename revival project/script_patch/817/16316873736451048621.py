# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/AutoDissolveDescUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from cocosui import cc, ccui, ccs
import common.const.uiconst

class AutoDissolveDescUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/i_common_describe'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    BORDER_INDENT = 24
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'nd_bg.OnBegin': '_hide_item_desc_info'
       }

    def on_init_panel(self, *args, **kwargs):
        self.hide()

    def _hide_item_desc_info(self, *args):
        self.hide()

    def ui_vkb_custom_func(self):
        self._hide_item_desc_info()

    def init_dissolve_desc(self, text, wpos):
        self.panel.SetStringWithAdapt(text, min_size=(240, 0))
        size = self.panel.getTextContentSize()
        pos = self.panel.getParent().convertToNodeSpace(wpos)
        self.panel.setPosition(wpos.x - size.width, wpos.y + size.height)
        self.show()