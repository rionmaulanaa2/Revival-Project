# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyVeteranEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import jump_to_ui_utils
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const

class LobbyVeteranEntryWidget(LobbyEntryWidgetBase):

    @classmethod
    def check_shown(cls, widget_type):
        if not global_data.player:
            return
        return global_data.player.can_return_steam_server()

    def on_init_widget(self):
        super(LobbyVeteranEntryWidget, self).on_init_widget()
        self.panel.btn_return.BindMethod('OnClick', self.on_click_btn)

    def on_click_btn(self, *args):
        global_data.ui_mgr.show_ui('PCVeteranUI', 'logic.comsys.veteran')

    def refresh_red_point(self):
        pass

    def need_show_red_point(self):
        return False