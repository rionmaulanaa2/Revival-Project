# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComLobbyChatUI.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.comsys.battle.TeammateWidget.LobbyChatHeadUI import LobbyChatHeadUI

class ComLobbyChatUI(UnitCom):
    BIND_EVENT = {'E_SHOW_CHAT_MESSAGE': 'on_show_chat_message',
       'E_EMOJI': 'on_emoji'
       }

    def __init__(self):
        super(ComLobbyChatUI, self).__init__()
        self.init_ui_data()

    def init_ui_data(self):
        self._chat_ui = None
        return

    def on_show_chat_message(self, msg):
        LobbyChatHeadUI.cls_show_chat_msg(self.unit_obj, msg)

    def destroy(self):
        LobbyChatHeadUI.destroy_ui(self.unit_obj)
        super(ComLobbyChatUI, self).destroy()

    def on_emoji(self, *args):
        LobbyChatHeadUI.cls_hide_chat_msg(self.unit_obj)