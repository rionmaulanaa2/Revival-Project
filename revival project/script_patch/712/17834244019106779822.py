# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatBlessingPigeon.py
from __future__ import absolute_import
import common.utilities
import common.const.uiconst
from common.const.property_const import U_ID, U_LV, CLAN_ID, C_NAME
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils import task_utils
from common.uisys.basepanel import BasePanel
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import chat_const
from logic.gutils import chat_utils
from logic.gcommon.common_utils import text_utils
MaxLength = 30
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class ChatBlessingPigeon(WindowSmallBase):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    PANEL_CONFIG_NAME = 'common/speaker'
    TEMPLATE_NODE_NAME = 'temp_pnl'
    UI_ACTION_EVENT = {'btn_verify.btn_common.OnClick': 'on_send'
       }

    def on_init_panel(self, *args, **kargs):
        super(ChatBlessingPigeon, self).on_init_panel()

        def callback(text):
            length = common.utilities.get_utf8_length(text)
            self.input_limit.setString(get_text_by_id(2131).format(MaxLength - length))

        self._input_box = InputBox.InputBox(self.input_text, max_length=MaxLength, input_callback=callback)
        self._input_box.set_rise_widget(self.panel)
        self.input_limit.setString(get_text_by_id(2131).format(MaxLength))
        self.panel.remain_num.setVisible(False)
        self.panel.temp_pnl.lab_title.setString(get_text_by_id(633752))
        self._blessing_ui = None
        self._message_data = None
        self.init_box_message()
        return

    def init_box_message(self):
        input_msg = ArchiveManager().get_cur_user_archive_data('blessing_msg') or get_text_by_id(633753)
        self._input_box.set_text(input_msg)
        length = common.utilities.get_utf8_length(input_msg)
        self.input_limit.setString(get_text_by_id(2131).format(MaxLength - length))

    def set_extra_info(self, message_data, blessing_ui):
        self._blessing_ui = blessing_ui
        self._message_data = message_data

    def on_close(self, *args):
        self.close()

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return

    def on_send(self, *args):
        task_id = '1301521'
        task_conf = task_utils.get_task_conf_by_id(task_id)
        prog_rewards_list = task_conf.get('prog_rewards', [])
        task_prog = global_data.player.get_task_prog(task_id)
        max_prog = prog_rewards_list[-1][0]
        msg = self._input_box.get_text()
        if len(msg) == 0:
            global_data.player.notify_client_message((get_text_by_id(11055),))
            return
        check_code, check_result, msg = text_utils.check_review_words_chat(msg)
        if check_result == text_utils.CHECK_WORDS_NO_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg, check_code, self._message_data[U_ID], self._message_data[U_LV])
            self._input_box.set_text(get_text_by_id(633753))
            return

        def dummyfunc(*args):
            pass

        blessed = self._message_data.get('blessed', False)
        global_data.message_data.recv_to_friend_msg(self._message_data[U_ID], self._message_data[C_NAME], msg, self._message_data[U_LV], extra={})
        if not blessed:
            if self._blessing_ui and self._blessing_ui.icon_got:
                self._blessing_ui.icon_got.setVisible(True)
            self._message_data['blessed'] = True
            extra = {}
            extra['reward_key'] = self._message_data.get('extra', {}).get('reward_key')
            if task_prog == max_prog:
                global_data.player.req_friend_msg(self._message_data[U_ID], self._message_data[U_LV], self._message_data.get(CLAN_ID, -1), msg, extra=extra)
                global_data.game_mgr.show_tip(get_text_by_id(633750))
            else:
                global_data.player.req_blessing_msg(self._message_data[U_ID], self._message_data[U_LV], self._message_data.get(CLAN_ID, -1), msg, extra=extra)
                global_data.game_mgr.show_tip(get_text_by_id(633751))
        else:
            extra = {}
            global_data.player.req_friend_msg(self._message_data[U_ID], self._message_data[U_LV], self._message_data.get(CLAN_ID, -1), msg, extra=extra)
            global_data.game_mgr.show_tip(get_text_by_id(633751))
        if self._blessing_ui and self._blessing_ui.lab_blessing:
            self._blessing_ui.lab_blessing.SetCallback(dummyfunc)
        ArchiveManager().set_cur_user_archive_data('blessing_msg', msg)
        self.close()