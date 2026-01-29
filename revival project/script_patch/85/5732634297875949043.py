# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/CDKeyGiftUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
import re

class CDKeyGiftUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'lobby/redeem_info'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_bg'
    CODE_LEN = 30
    UI_ACTION_EVENT = {'btn_redeem.btn_common.OnClick': 'exchange_cdkey_gift'
       }
    GLOBAL_EVENT = {'textfield_eventtype_attach_with_ime_event': 'on_attach_input'
       }

    def on_init_panel(self, *args, **kwargs):
        super(CDKeyGiftUI, self).on_init_panel()
        self._input_lift_key = InputBox(self.temp_text, placeholder=get_text_by_id(920811))
        self._input_lift_key.set_rise_widget(self.panel)

    def exchange_cdkey_gift(self, *args):
        text = self._input_lift_key.get_text()
        if not text:
            global_data.game_mgr.show_tip(get_text_by_id(920820))
            return
        ret = bool(re.match('[a-zA-Z0-9]+$', text))
        if ret:
            global_data.player.active_cdkey_gift(text)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(920812))

    def on_attach_input(self):
        import game3d
        clipboard_text = game3d.get_clipboard_text()
        if not clipboard_text:
            return
        if len(clipboard_text) > self.CODE_LEN:
            return
        ret = bool(re.match('[a-zA-Z0-9]+$', clipboard_text))
        if ret:
            self._input_lift_key._on_pc_paste_text(clipboard_text)