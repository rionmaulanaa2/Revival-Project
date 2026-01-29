# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reconnect_ui/BattleReconnectUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_TYPE_CONFIRM
from common.utils.cocos_utils import ccc4, ccp
from common.const import uiconst

class BattleReconnectUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/reconnect_main'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    ST_CONNECTING = 1
    ST_SELECT_RETURN_TO_BATTLE = 2
    ST_INFORM = 3
    IS_FULLSCREEN = True
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        self.add_blocking_ui_list(['NetworkLagUI'])
        self.hide_main_ui()
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def on_finalize_panel(self):
        self.show_main_ui()
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def show_info_message(self, msg=None, cancel_callback=None, alive_time=-1):
        if msg:
            self.panel.lab_reconnect.SetString(str(msg))
        else:
            self.panel.lab_reconnect.SetString(str(''))
        self.panel.nd_loading.setVisible(True)
        self.panel.nd_reconnect.setVisible(False)
        self.show_connecting()
        if alive_time > 0:
            self.panel.SetTimeOut(alive_time, self.close)

        @self.panel.nd_loading.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self.close()
            if cancel_callback and callable(cancel_callback):
                cancel_callback()

    def show_connecting(self):
        self.panel.lab_reconnect.setVisible(True)
        self.panel.img_loading.setVisible(True)
        self.panel.PlayAnimation('loading')

    def hide_connecting(self):
        self.panel.lab_reconnect.setVisible(False)
        self.panel.img_loading.setVisible(False)
        self.panel.StopAnimation('loading')

    def show_select_message(self, msg=None, sure_callback=None, cancel_callback=None):
        if msg:
            self.panel.nd_reconnect.lab_content.SetString(msg)

        @self.panel.nd_reconnect.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if sure_callback and callable(sure_callback):
                sure_callback()

        @self.panel.nd_reconnect.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if cancel_callback and callable(cancel_callback):
                cancel_callback()

        self.panel.nd_loading.setVisible(False)
        self.panel.nd_reconnect.setVisible(True)
        self.hide_connecting()