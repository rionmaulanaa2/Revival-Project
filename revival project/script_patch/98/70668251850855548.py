# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefinePlanRenameWidget.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id

class SkinDefinePlanRenameWidget(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/change_name'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'

    def on_init_panel(self, *args, **kargs):
        super(SkinDefinePlanRenameWidget, self).on_init_panel()
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(self.panel.panel.inputbox)
        self._input_box.set_rise_widget(self.panel)
        self.panel.lab_cost.setVisible(False)
        self.panel.nd_item.setVisible(False)
        self.panel.panel.lab_title.SetString(get_text_by_id(860204))

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            if not text:
                return

        @self.panel.panel.img_window_bg.btn_close.callback()
        def OnClick(*args):
            self.close()

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return