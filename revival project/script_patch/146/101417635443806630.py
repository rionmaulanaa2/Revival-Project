# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/home_message_board/MessageLeftUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.common_utils import text_utils
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import homeland_utils
from logic.gcommon.common_const import homeland_const
import time
import json

class MessageLeftUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/open_home_system_inputbox'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'panel.btn_close.OnClick': 'on_click_btn_close',
       'panel.temp_btn_1.btn_common.OnClick': 'on_click_btn_send'
       }
    SEND_CD = 5.0
    LEFT = 1
    REPLY = 2
    WRITE_INTRO = 3

    def on_init_panel(self):
        self.is_landlord = global_data.message_board_mgr.is_landlord()
        self.message_type = self.LEFT
        self.bid = None
        self.last_send_time = 0
        self.init_input_box()
        player = global_data.player
        if player:
            uid = player.get_visit_uid() or player.uid
            if self.is_landlord:
                self.panel.lab_title.SetString(get_text_by_id(611529).format(name=player.get_name()))
            else:
                role_data = global_data.message_data.get_player_inf(1, int(uid))
                if role_data:
                    char_name = role_data['char_name']
                    self.panel.lab_title.SetString(get_text_by_id(611529).format(name=char_name))
        return

    def init_input_box(self):
        self.input_box = InputBox(self.panel.temp_inputbox, send_callback=self.on_edit_box_send_callback, input_callback=self.on_edit_box_changed_callback)
        self.input_box.set_enable_pop_up_keyboard(False)

    def set_message_data(self, msg_type, bid=None):
        self.message_type = msg_type
        self.bid = bid

    def on_click_btn_close(self, *args):
        self.close()

    def on_click_btn_send(self, *args):
        self.on_edit_box_send_callback()

    def on_edit_box_send_callback(self, *args):
        msg = self.input_box.get_text()
        if not msg:
            return
        else:
            cur_time = time.time()
            delta_time = cur_time - self.last_send_time
            if delta_time < self.SEND_CD:
                global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': int(self.SEND_CD - delta_time)}))
                return
            self.last_send_time = cur_time
            check_code, flag, msg = text_utils.check_review_words_chat(msg)
            if flag != text_utils.CHECK_WORDS_PASS:
                global_data.player.notify_client_message((get_text_by_id(11009),))
                return
            if self.message_type == self.LEFT:
                homeland_utils.left_message(msg)
            elif self.message_type == self.REPLY and self.bid is not None:
                homeland_utils.reply_message(self.bid, msg)
                global_data.message_board_mgr.reply_message(self.bid, msg)
            elif self.message_type == self.WRITE_INTRO:
                homeland_utils.write_intro(msg)
                global_data.message_board_mgr.set_intro(msg)
            self.input_box.set_text('')
            self.close()
            return

    def on_edit_box_changed_callback(self, text):
        if text.endswith('\n') or text.endswith('\r'):
            text = text.rstrip('\n')
            text = text.rstrip('\r')
            self.input_box.set_text(text)
            self.input_box.detachWithIME()