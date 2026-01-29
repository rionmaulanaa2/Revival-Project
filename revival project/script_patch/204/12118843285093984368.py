# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/CommonInputDialog.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
import game3d
import common.utilities
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from common.const import uiconst

class CommonInputDialog(BasePanel):
    PANEL_CONFIG_NAME = 'common/change_name'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kargs):
        self.init_buttons()
        self._send_callback = kargs.get('send_callback', None)
        placeholder = kargs.get('placeholder', '')
        self._real_input_callback = kargs.get('input_callback', None)
        self._max_length = kargs.get('max_length', None)
        self._init_text = kargs.get('init_text', '')
        self._invalid_msg = kargs.get('invalid_msg', get_text_by_id(860192))
        self.panel.panel.lab_title.SetString(kargs.get('title', ''))
        self.panel.lab_desc.SetString(kargs.get('desc_text', ''))
        self.panel.lab_cost.SetString(kargs.get('cost_text'), '')
        self.init_ui(placeholder, self.input_callback, self._max_length)
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self._send_callback = None
        self._real_input_callback = None
        return

    def init_ui(self, placeholder, input_callback, max_length):
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(self.panel.panel.inputbox, placeholder=placeholder, input_callback=input_callback, max_length=self._max_length)
        self._input_box.set_rise_widget(self.panel)
        self._input_box.set_text(self._init_text)

    def init_buttons(self):

        @self.panel.panel.confirm.btn_common_big.callback()
        def OnClick(*args):
            from logic.gcommon.common_utils.text_utils import check_review_words
            flag, text = check_review_words(self._input_box.get_text())
            if not flag:
                global_data.game_mgr.show_tip(self._invalid_msg)
                return
            if self._send_callback:
                if self._send_callback(text):
                    self.close()
            else:
                self.close()

        @self.panel.panel.btn_close.callback()
        def OnClick(*args):
            self.close()

        @self.panel.panel.callback()
        def OnClick(*args):
            self.close()

    def input_callback(self, text):
        if self._real_input_callback:
            self._real_input_callback(text)