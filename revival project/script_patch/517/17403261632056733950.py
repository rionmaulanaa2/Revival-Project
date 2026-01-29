# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatPigeonInput.py
from __future__ import absolute_import
import common.utilities
import common.const.uiconst
import logic.comsys.common_ui.InputBox as InputBox
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import chat_const
from logic.gutils import chat_utils
MaxLength = 30
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class ChatPigeonInput(WindowSmallBase):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    PANEL_CONFIG_NAME = 'common/speaker'
    TEMPLATE_NODE_NAME = 'temp_pnl'
    UI_ACTION_EVENT = {'btn_verify.btn_common.OnClick': 'on_send'
       }

    def on_init_panel(self, *args, **kargs):
        super(ChatPigeonInput, self).on_init_panel()

        def callback(text):
            length = common.utilities.get_utf8_length(text)
            self.input_limit.setString(get_text_by_id(2131).format(MaxLength - length))

        self._input_box = InputBox.InputBox(self.input_text, max_length=MaxLength, input_callback=callback)
        self._input_box.set_rise_widget(self.panel)
        item_amount = global_data.player.get_item_num_by_no(chat_const.CHAT_PIGEON_COST_ITEM_NO)
        self.remain_num.GetItem(0).txt_price.SetString(str(item_amount))
        self.input_limit.setString(get_text_by_id(2131).format(MaxLength))
        if item_amount <= 0:
            self.btn_verify.btn_common.SetShowEnable(False)

    def on_close(self, *args):
        self.close()

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def on_send(self, *args):

        def _cb():
            self.close()

        chat_utils.send_pigeon_msg(self._input_box, _cb)