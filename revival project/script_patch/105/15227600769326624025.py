# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySmallSecondConfirmWidget.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel

class LotterySmallSecondConfirmWidget(BasePanel):
    PANEL_CONFIG_NAME = 'common/bg_second_confirm_small'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, title_text_id=None, content_text_id=None, confirm_text_id=None, cancel_text_id=None, confirm_callback=None, cancel_callback=None, *args, **kwargs):
        if title_text_id:
            self.panel.lab_title.SetString(title_text_id)
        if content_text_id:
            self.panel.lab_content.SetString(content_text_id)
        if confirm_text_id:
            self.panel.temp_btn_2.btn_common_big.SetText(confirm_text_id)
        if cancel_text_id:
            self.panel.temp_btn_1.btn_common_big.SetText(cancel_text_id)

        @self.panel.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(*args):
            if confirm_callback:
                confirm_callback()
            self.close()

        @self.panel.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(*args):
            if cancel_callback:
                cancel_callback()
            self.close()

        @self.panel.btn_close.unique_callback()
        def OnClick(*args):
            self.close()