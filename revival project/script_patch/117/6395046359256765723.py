# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/LoginAnimationUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const import uiconst

class LoginAnimationUI(BasePanel):
    PANEL_CONFIG_NAME = 'login/login_linking'
    IS_FULLSCREEN = True
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kargs):
        self.init_event()
        self.panel.PlayAnimation('login')

    def init_event(self):
        global_data.emgr.on_login_failed_event += self.on_login_fail

    def on_login_fail(self, *args, **kargs):
        global_data.game_mgr.show_tip(get_text_local_content(193))
        global_data.ui_mgr.close_ui('LoginAnimationUI')
        main_login_ui = global_data.ui_mgr.get_ui('MainLoginUI')
        if main_login_ui and not kargs.get('err_code', None):
            main_login_ui.show_server_open_time()
        return

    def on_finalize_panel(self):
        global_data.emgr.on_login_failed_event -= self.on_login_fail