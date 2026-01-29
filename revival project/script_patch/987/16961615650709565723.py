# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/CommonInputUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
import logic.comsys.common_ui.InputBox as InputBox
TEXT_MAX_LEN_JUDGEMENT = 150

class CommonInputUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'setting/i_setting_feedback_details'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'pnl'
    UI_ACTION_EVENT = {'pnl.btn_close.OnClick': 'on_click_close_btn',
       'confirm.btn_common_big.OnClick': 'on_click_commit_btn'
       }

    def on_init_panel(self):
        super(CommonInputUI, self).on_init_panel()
        self.init_ui()

    def init_ui(self):
        panel = self.panel

        def send_cb(*args, **kwargs):
            pass

        def max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        self._input_box = InputBox.InputBox(panel.inputbox, max_length=TEXT_MAX_LEN_JUDGEMENT, max_input_cb=max_input_cb, send_callback=send_cb, detach_after_enter=False)
        self._input_box.set_rise_widget(self.panel)
        self._input_box.enable_input(False)

    def on_finalize_panel(self):
        self.confirm_callback = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def on_click_close_btn(self, *args):
        self.close()

    def on_click_cancel_btn(self, *args):
        self.close()

    def configure_panel(self, confirm_cb, title='', content='', max_length=TEXT_MAX_LEN_JUDGEMENT):
        self.confirm_callback = confirm_cb
        self.pnl.img_window_bg.lab_title.SetString(title)
        self._input_box.set_max_length(max_length)
        self._input_box.set_text(content)
        self._input_box.enable_input(True)

    def on_click_commit_btn(self, *args):
        self.exec_confirm_cb()
        self.close()

    def exec_confirm_cb(self):
        if self.confirm_callback:
            self.confirm_callback(self._input_box.get_text())
        self.confirm_callback = None
        return