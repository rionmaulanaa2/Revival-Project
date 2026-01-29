# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/SimpleChat.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import math
import time
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils import text_utils
RICHTEXT_CONTENT_EDGE = 10
RICHTEXT_BOTTOM_TRIANGLE_WIDTH = 13
from logic.gcommon.common_utils.local_text import get_text_by_id, get_server_text
from logic.comsys.chat.MainChat import check_show_msg
from logic.gcommon.common_const import ui_operation_const as uoc

class SimpleChat(object):
    MIN_SEND_TIME = 5

    def __init__(self, channel, panel, rise_panel):
        self._message_data = global_data.message_data
        self.main_panel = rise_panel
        self.panel = panel
        self._channel_index = channel
        self._my_uid = global_data.player.uid
        self._last_send_time = time.time()
        self._player_info_manager = PlayerInfoManager()
        self._chat_emote_ui = None
        self._sview_data_index = 0
        self._cur_msg_data = []
        self._lv_chat = self.panel.lv_chat
        self._lv_chat.DeleteAllSubItem()
        self.reload_all_template_format()
        self.init_channel()
        self.init_touch()
        self.init_input()
        if self.main_panel:
            self.save_nd_chat_pos_y = self.main_panel.GetPosition()[1]
        else:
            self.save_nd_chat_pos_y = 0
        global_data.emgr.chat_add_channel_msg += self.on_add_channel_msg
        return

    def init_channel(self):
        self.refresh_channel_show()

    def refresh_channel_show(self, data_list=None):
        self._lv_chat.DeleteAllSubItem()
        self._lv_chat.setVisible(True)
        self._cur_msg_data = list(self._message_data.get_channel_msg(self._channel_index)) if data_list is None else data_list
        data_count = len(self._cur_msg_data)
        sview_height = self._lv_chat.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = self._cur_msg_data[data_count - index - 1]
            chat_pnl = self.add_msg(data, False)
            if chat_pnl is None:
                del self._cur_msg_data[data_count - index - 1]
                data_count -= 1
                continue
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._lv_chat._container._refreshItemPos()
        self._lv_chat._refreshItemPos()
        self._lv_chat.ScrollToBottom()
        self._sview_data_index = len(self._cur_msg_data) - 1
        return

    def init_touch(self):
        self._is_check_sview = False

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self._lv_chat.SetTimeOut(0.021, self.check_sview)

        self._lv_chat.addEventListener(scroll_callback)

    def init_input(self):
        panel = self.panel
        input_box = panel.input_box

        def max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        def send_cb(*args, **kwargs):
            panel.btn_send.btn_common.OnClick(None)
            return

        self._input_box = InputBox.InputBox(input_box, max_input_cb=max_input_cb, send_callback=send_cb, detach_after_enter=False)
        self._input_box.set_rise_widget(self.main_panel)
        if panel.btn_emote:

            @panel.btn_emote.callback()
            def OnClick(*args):
                ui = global_data.ui_mgr.show_ui('ChatEmote', 'logic.comsys.chat')
                self._chat_emote_ui = ui
                ui.set_input_box(self._input_box, panel.btn_send.btn_common)
                ui.set_close_callback(self.panel_recover)
                panel_bot_pos = self.panel.img_bg.ConvertToWorldSpacePercentage(100, 100)
                height_offset = ui.get_bg_height() - panel_bot_pos.y + 5
                if height_offset < 0:
                    height_offset = 0
                self.panel_up_move(height_offset)

        @panel.btn_send.btn_common.callback()
        def OnClick(*args, **kargs):
            do_not_check_msg = kargs.get('do_not_check_msg')
            msg = do_not_check_msg or self._input_box.get_text()
            if msg == '':
                global_data.player.notify_client_message((get_text_by_id(11055),))
                return
            cur_time = time.time()
            if cur_time - self._last_send_time < 0.5:
                return
            if global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
                global_data.player.notify_client_message((get_text_by_id(11063).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
                return
            if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
                return
            pass_time = cur_time - self._last_send_time
            if pass_time < self.MIN_SEND_TIME:
                global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(self.MIN_SEND_TIME - pass_time)))}))
                return
            self._last_send_time = cur_time
            self.send_msg(self._channel_index, msg, do_not_check_msg, from_input_box=True)

    def send_msg(self, channel, msg, do_not_check_msg=False, from_input_box=False):
        if msg == '':
            global_data.player.notify_client_message((get_text_by_id(11055),))
            return
        if channel == chat_const.CHAT_WORLD and global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
            global_data.player.notify_client_message((get_text_by_id(11063).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
            return
        if do_not_check_msg:
            check_code = 0
            check_result = text_utils.CHECK_WORDS_PASS
        else:
            check_code, check_result, msg = text_utils.check_review_words_chat(msg)
            if check_result == text_utils.CHECK_WORDS_NO_PASS:
                global_data.player.notify_client_message((get_text_by_id(11009),))
                global_data.player.sa_log_forbidden_msg(channel, msg, check_code)
                return
        if from_input_box:
            self._input_box.set_text('')
        if check_result == text_utils.CHECK_WORDS_PASS:
            global_data.player.send_msg(channel, msg, code=check_code)
        elif check_result == text_utils.CHECK_WORDS_ONLY_SELF:
            self._message_data.add_only_self_msg(channel, msg)
            global_data.player.sa_log_forbidden_msg(channel, msg, check_code)
        self.on_send_success(msg)

    def on_send_success(self, msg):
        pass

    def on_add_channel_msg(self, index_move, channel, data):
        if self._channel_index == channel:
            self.add_msg(data)
            self._lv_chat._container._refreshItemPos()
            self._lv_chat._refreshItemPos()
            self._lv_chat.jumpToBottom()
            self._sview_data_index += index_move

    def add_msg(self, data, is_back_item=True, index=-1, is_new=False):
        pass

    def get_max_line_width(self, line_widths):
        max_width = None
        for width in line_widths:
            if not max_width:
                max_width = width
            elif max_width < width:
                max_width = width

        return max_width

    def reload_all_template_format(self):
        self.release_template_format()
        self.load_template_format()

    def load_template_format(self):
        pass

    def release_template_format(self):
        pass

    def check_sview(self):
        msg_count = len(self._cur_msg_data)
        self._sview_data_index = self._lv_chat.AutoAddAndRemoveItem_chat(self._sview_data_index, self._cur_msg_data, msg_count, self.add_msg, 300, 400)
        self._is_check_sview = False

    def panel_up_move(self, height):
        if self.main_panel:
            x, _ = self.main_panel.GetPosition()
            self.main_panel.SetPosition(x, self.save_nd_chat_pos_y + height)

    def panel_recover(self):
        if self.main_panel:
            x, _ = self.main_panel.GetPosition()
            self.main_panel.SetPosition(x, self.save_nd_chat_pos_y)
        self._chat_emote_ui = None
        return

    def hide_inputbox(self):
        if self._input_box:
            self._input_box.hide()

    def destroy(self):
        if self._chat_emote_ui:
            global_data.ui_mgr.close_ui('ChatEmote')
            self._chat_emote_ui = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self._lv_chat.DeleteAllSubItem()
        global_data.emgr.chat_add_channel_msg -= self.on_add_channel_msg
        self.release_template_format()
        return