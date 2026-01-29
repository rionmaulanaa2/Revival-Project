# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reconnect_ui/LobbyReconnectUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import DISCONNECT_ZORDER, UI_TYPE_CONFIRM
from common.utils.cocos_utils import ccc4, ccp
from common.const import uiconst

class LobbyReconnectUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/reconnect_main_2'
    DLG_ZORDER = DISCONNECT_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    UI_ACTION_EVENT = {'nd_confirm.temp_btn_2.btn_common_big.OnClick': 'on_confirm_dialog',
       'nd_message.btn_close.OnClick': 'on_close_dialog'
       }

    def on_init_panel(self):
        self.playing_waiting = False
        self.add_blocking_ui_list(['NetworkLagUI'])
        self._custom_close_callback = None
        self.panel.nd_message.setVisible(False)
        self.panel.nd_select.setVisible(False)
        self.panel.nd_confirm.setVisible(False)
        return

    def on_finalize_panel(self):
        pass

    def do_hide_panel(self):
        super(LobbyReconnectUI, self).do_hide_panel()
        self.show_main_ui()

    def do_show_panel(self):
        super(LobbyReconnectUI, self).do_show_panel()

    def on_confirm_dialog(self, btn, touch):
        self.close()

    def play_waiting_animation(self):
        if not self.playing_waiting:
            self.panel.PlayAnimation('waiting')
            self.playing_waiting = True

    def show_info_message(self, msg=None, alive_time=-1, sure_callback=None, cancel_callback=None):
        if msg:
            self.panel.nd_message.text.SetString(str(msg))
        self.play_waiting_animation()

        @self.panel.nd_message.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if sure_callback and callable(sure_callback):
                sure_callback()

        @self.panel.nd_message.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if cancel_callback and callable(cancel_callback):
                cancel_callback()

        self.panel.nd_message.setVisible(True)
        self.panel.nd_select.setVisible(False)
        self.panel.nd_confirm.setVisible(False)
        if alive_time > 0:
            self.panel.nd_message.btn_close.setVisible(True)
            self.panel.nd_message.temp_btn_1.setVisible(False)
            self.panel.nd_message.temp_btn_2.setVisible(False)
            self.panel.SetTimeOut(alive_time, self.close)
        else:
            self.panel.nd_message.btn_close.setVisible(False)
            self.panel.nd_message.temp_btn_1.setVisible(False)
            self.panel.nd_message.temp_btn_2.setVisible(True)

    def show_confirm_message(self, msg=None):
        if msg:
            self.panel.nd_confirm.text.SetString(msg)
        self.panel.nd_message.setVisible(False)
        self.panel.nd_select.setVisible(False)
        self.panel.nd_confirm.setVisible(True)

    def show_select_message(self, msg=None, sure_callback=None, cancel_callback=None):
        if msg:
            self.panel.nd_select.text.SetString(msg)

        @self.panel.nd_select.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if sure_callback and callable(sure_callback):
                sure_callback()

        @self.panel.nd_select.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if cancel_callback and callable(cancel_callback):
                cancel_callback()

        self.panel.nd_message.setVisible(False)
        self.panel.nd_select.setVisible(True)
        self.panel.nd_confirm.setVisible(False)

    def set_custom_close_callback(self, callback):
        self._custom_close_callback = callback

    def on_close_dialog(self, *args):
        if self._custom_close_callback:
            self._custom_close_callback()
        else:
            self.hide()