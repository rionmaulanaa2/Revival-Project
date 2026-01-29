# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ConcertRedPacketSendUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.gutils import mall_utils, task_utils
import common.cfg.confmgr as confmgr
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
import cc
from logic.client.const import mall_const
import logic.gcommon.const as gconst
import logic.gcommon.time_utility as tutil
from logic.comsys.red_packet.ChatRedPacketSendUI import ChatRedPacketSendUI

class ConcertRedPacketSendUI(BasePanel):
    PANEL_CONFIG_NAME = 'chat/red_packet/concert_red_packet_change'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'send_red_packet_succeed': 'on_send_red_packet_succeed'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ConcertRedPacketSendUI, self).on_init_panel()
        from logic.gcommon.common_const.chat_const import CHAT_BATTLE_WORLD
        self._channel_index = CHAT_BATTLE_WORLD
        self.send_red_packet_widget = None
        self.panel.BindMethod('OnClick', self.on_click_btn_close)
        self.init_red_packet()
        return

    def on_finalize_panel(self):
        if self.send_red_packet_widget:
            self.send_red_packet_widget.destroy()
            self.send_red_packet_widget = None
        return

    def on_click_btn_close(self, btn, touch):
        self.close()

    def init_red_packet(self):
        self.send_red_packet_widget = ChatRedPacketSendUI(self.panel.temp_red_packet, self._channel_index)
        self.send_red_packet_widget.update_send_channel(self._channel_index)
        self.send_red_packet_widget.set_show_close_tips(True)
        self.send_red_packet_widget.set_cover_usable(False)

        @self.panel.temp_red_packet.nd_touch.callback()
        def OnClick(*args):
            if self.send_red_packet_widget and self.send_red_packet_widget.get_is_visible():
                self.close()
                return

    def on_send_red_packet_succeed(self):
        self.close()