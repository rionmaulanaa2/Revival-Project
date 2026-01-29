# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/TeamQuickChat.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import time
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
from logic.gcommon import const
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.comsys.common_ui.InputBox as InputBox
import common.utilities
import logic.gcommon.const
from common.utils.path import get_neox_dir
from patch.patch_path import get_download_target_path
import math
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gutils import role_head_utils
from common.platform import channel_const
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils import text_utils
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
team_chat_edite_res_path = 'gui/ui_res_2/common/icon/icon_tick.png'
team_chat_common_res_path = 'gui/ui_res_2/battle/icon/icon_fight_setting.png'
MAX_ITEM_COUNT = 7

class TeamQuickChat(object):

    def __init__(self, main_panel):
        self.main_panel = main_panel
        self.panel = main_panel.panel
        self._is_edited_mode = False
        self.team_chat_quick_temp = global_data.uisystem.load_template('chat/i_chat_quick_list_add')
        nd_chat_quick = self.panel.nd_chat_quick
        nd_chat_quick.btn_setting.EnableCustomState(True)

        @nd_chat_quick.btn_setting.callback()
        def OnClick(*args):
            self._is_edited_mode = not self._is_edited_mode
            if self._is_edited_mode:
                nd_chat_quick.btn_setting.SetSelect(True)
            else:
                nd_chat_quick.btn_setting.SetSelect(False)
            self.refresh_all_team()

        self.refresh_all_team()

    def refresh_all_team(self):
        list_chat_quick = self.panel.nd_chat_quick.list_chat_quick
        list_chat_quick.DeleteAllSubItem()
        quick_chats = global_data.message_data.get_seting_inf('team_quick_chat')
        if self._is_edited_mode and len(quick_chats) < MAX_ITEM_COUNT:
            panel = list_chat_quick.AddItem(self.team_chat_quick_temp, bRefresh=True)
            self.add_new_chat_quick_item(panel)
        for msg in quick_chats:
            panel = list_chat_quick.AddTemplateItem()
            self.add_team_chat_quick_item(panel, msg)

        for index in range(MAX_ITEM_COUNT - len(quick_chats)):
            panel = list_chat_quick.AddTemplateItem()
            panel.btn_chat.SetText('')
            panel.btn_delete.setVisible(False)

    def add_team_chat_quick_item(self, panel, msg):
        panel.btn_chat.SetText(msg)

        @panel.btn_chat.callback()
        def OnClick(*args):
            if not self._is_edited_mode:
                self.main_panel.send_msg(chat_const.CHAT_TEAM, msg)
                self.main_panel.chat_close()
                self.main_panel.refresh_team_quick_chat()
                self.main_panel.refresh_base_panel_touch_status()
                self.panel.nd_chat_quick.setVisible(False)

        panel.btn_delete.setVisible(self._is_edited_mode)

        @panel.btn_delete.callback()
        def OnClick(*args):
            if self._is_edited_mode:

                def click_unfollow():
                    quick_chats = global_data.message_data.get_seting_inf('team_quick_chat')
                    quick_chats.remove(msg)
                    global_data.message_data.set_seting_inf('team_quick_chat', quick_chats)
                    self.refresh_all_team()

                SecondConfirmDlg2().confirm(content=get_text_by_id(81355), confirm_callback=click_unfollow)

    def add_new_chat_quick_item(self, panel):

        @panel.btn_chat_add.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('ChatEditedInput', 'logic.comsys.chat')
            ui.set_callback(self.edite_input_callback)

    def edite_input_callback(self, msg):
        check_code, check_result, msg = text_utils.check_review_words_chat(msg)
        if check_result == text_utils.CHECK_WORDS_NO_PASS:
            global_data.player.notify_client_message((get_text_by_id(10045),))
            return
        quick_chats = global_data.message_data.get_seting_inf('team_quick_chat')
        quick_chats.append(msg)
        global_data.message_data.set_seting_inf('team_quick_chat', quick_chats)
        self.refresh_all_team()

    def set_visible(self, visible):
        self.panel.nd_chat_quick.setVisible(visible)

    def is_visible(self):
        return self.panel.nd_chat_quick.isVisible()

    def is_edited_mode(self):
        return self._is_edited_mode