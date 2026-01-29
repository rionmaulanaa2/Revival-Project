# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_TYPE_MESSAGE
from common.utils.cocos_utils import ccp, CCSizeZero
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_const import battle_const as bconst
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.common_const import battle_const
from logic.gcommon import const
import world
import cc
import time
from logic.comsys.lobby.LobbyMainCommonInfo import LobbyMainCommonInfo
from logic.client.const import tips_const

class BaseMessageQueue(object):

    def __init__(self, panel, node_message):
        self._message_queue = []
        self._can_show_message = True
        self._node_message = node_message
        self.panel = panel

    def destroy(self):
        self.panel = None
        self._node_message = {}
        self._message_queue = []
        return

    def show_message(self, message, message_type):
        if message_type not in self._node_message:
            return
        self._message_queue.append((message, message_type))
        self._show_next_message()

    def finish_message_show(self):
        self._can_show_message = True
        self._show_next_message()

    def _show_next_message(self):
        if not self._can_show_message:
            return
        if len(self._message_queue) > 0:
            msg = self._message_queue.pop(0)
            text, message_type = msg
            self._can_show_message = False
            battle_info_message = self._node_message[message_type]
            ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
            if not ui:
                ui = battle_info_message(self.panel, self.finish_message_show)
            ui.add_message(text)

    def is_last_message(self):
        return len(self._message_queue) <= 0


from common.const import uiconst

class LobbyInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/lobby_feedback'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {}
    MAIN_NODE_MESSAGE = {}
    UP_NODE_MESAAGE = {}
    MED_NODE_MESSAGE = {}
    DOWN_NODE_MESSAGE = {tips_const.LOBBY_MAIN_COMMON_INFO: LobbyMainCommonInfo
       }
    GLOBAL_EVENT = {'lobby_tips_down_message_event': 'add_bottom_message'
       }

    def on_init_panel(self):
        self.init_parameters()

    def init_parameters(self):
        self._bottom_message_queue = BaseMessageQueue(self.panel, self.DOWN_NODE_MESSAGE)

    def on_finalize_panel(self):
        pass

    def init_event(self):
        self.init_parameters()

    def get_text_with_checking(self, raw_msg_id):
        if raw_msg_id:
            return get_text_by_id(int(raw_msg_id))
        else:
            return ''

    def add_bottom_message(self, message, message_type):
        self._bottom_message_queue.show_message(message, message_type)