# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/PhoneUnBindUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class PhoneUnBindUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/phone_binding_result'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE

    def on_click_close_btn(self, *args):
        self.close()

    def on_init_panel(self, phone=None):
        self.cur_phone = phone

        @self.panel.temp_pnl.btn_close.callback()
        def OnClick(*args):
            self.on_click_close_btn(*args)

        @self.panel.btn_cancel_binding.btn_common.callback()
        def OnClick(*args):
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            cur_phone = self.cur_phone

            def unbind():
                global_data.player.req_unbind(cur_phone)
                self.close()

            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(146).format(self.get_display_number(str(cur_phone))), confirm_callback=unbind)

        if self.cur_phone:
            self.panel.btn_cancel_binding.setVisible(True)
            self.panel.lab_phone_num.SetString(self.get_display_number(str(self.cur_phone)))
        else:
            global_data.player.query_cur_bind()

    def on_get_cur_phone(self, phone):
        self.cur_phone = phone
        if self.cur_phone:
            self.panel.btn_cancel_binding.setVisible(True)
            self.panel.lab_phone_num.SetString(self.get_display_number(str(self.cur_phone)))

    def get_display_number(self, number):
        prefix = number[0:3]
        sufix = number[7:]
        return prefix + '****' + sufix