# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/DanmuButtonWidget.py
from __future__ import absolute_import
import game3d
from logic.comsys.chat.DanmuChatWidget import DanmuChatWidget

class DanmuButtonWidget(object):
    DANMU_PATHS = {True: 'gui/ui_res_2/battle/icon/icon_danmu_open.png',
       False: 'gui/ui_res_2/battle/icon/icon_danmu_close.png'
       }

    def __init__(self, nd, send_group_message_either=False):
        self.panel = nd
        self.init_click_event()
        self.set_danmu_state(True)
        self.process_event(True)
        self.danmu_widget = DanmuChatWidget()
        self.danmu_widget.init(self.panel)
        self.danmu_widget.set_send_group_message_either(send_group_message_either)

    def process_event(self, is_bind):
        event_infos = {}
        if is_bind:
            global_data.emgr.bind_events(event_infos)
        else:
            global_data.emgr.unbind_events(event_infos)

    def destroy(self):
        self.process_event(False)
        self.panel = None
        if self.danmu_widget:
            self.danmu_widget.destroy()
            self.danmu_widget = None
        return

    def set_danmu_state(self, is_enable):
        self._enable_danmu = is_enable
        self.on_danmu_switch_state_changed(self._enable_danmu)
        dlg = global_data.ui_mgr.show_ui('DanmuLinesUI', 'logic.comsys.observe_ui')
        dlg.enable_danmu(self._enable_danmu)
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_SET_BS_STATE', self._enable_danmu)

    def init_click_event(self):

        @self.panel.btn_danmu.callback()
        def OnClick(btn, touch):
            self._enable_danmu = not self._enable_danmu
            self.set_danmu_state(self._enable_danmu)

        @self.panel.btn_send.callback()
        def OnClick(btn, touch):
            if self.danmu_widget:
                self.danmu_widget.on_danmu_input_chat_ui()

    def on_danmu_switch_state_changed(self, is_enable):
        path = self.DANMU_PATHS[is_enable]
        self.panel.img_danmu.SetDisplayFrameByPath('', path)