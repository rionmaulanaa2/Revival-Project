# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomPasswordUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.comsys.common_ui.InputBox as InputBox

class RoomPasswordUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'room/room_password'
    TEMPLATE_NODE_NAME = 'temp_panel'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_confirm.btn_common_big.OnClick': 'on_click_confirm_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        super(RoomPasswordUI, self).on_init_panel()
        need_pwd = kwargs.get('need_pwd')
        max_word = kwargs.get('max_word', 20)
        place_holder = kwargs.get('place_holder', get_text_by_id(2138))
        self._input_box = InputBox.InputBox(self.panel.temp_input, max_length=max_word, placeholder=place_holder)
        self._input_box.setPasswordEnabled(need_pwd)
        self._input_box.set_rise_widget(self.panel)
        self.confirm_callback = kwargs.get('confirm_cb', None)
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def on_click_confirm_btn(self, *args):
        if self.confirm_callback and callable(self.confirm_callback):
            self.confirm_callback(self._input_box.get_text())
        self.close()