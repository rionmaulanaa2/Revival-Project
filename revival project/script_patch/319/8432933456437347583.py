# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/WindowBigBase.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class WindowBigBase(BasePanel):
    TEMPLATE_NODE_NAME = ''
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE

    def on_init_panel(self, *args, **kwargs):
        self.template_node = None
        self._custom_close_func = None
        nd = getattr(self.panel, self.TEMPLATE_NODE_NAME)
        if nd:
            self.template_node = nd
            self.init_template_node(self.template_node)
        super(WindowBigBase, self).on_init_panel(*args, **kwargs)
        return

    def init_template_node(self, template_nd):

        @template_nd.btn_close.callback()
        def OnClick(btn, touch):
            if callable(self._custom_close_func):
                self._custom_close_func()
            else:
                self.close()

    def set_custom_close_func(self, close_func):
        self._custom_close_func = close_func
        if self._custom_close_func:
            self.UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
            self.ui_vkb_custom_func = self._custom_close_func
        else:
            self.UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
            self.ui_vkb_custom_func = None
        return