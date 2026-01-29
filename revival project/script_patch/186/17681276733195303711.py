# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyNextDayHotSteelEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import jump_to_ui_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id

class LobbyNextDayHotSteelEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {}

    @classmethod
    def check_shown(cls, widget_type):
        if not global_data.player:
            return False
        if global_data.player.get_history_attend_days() > 1:
            return False
        return True

    def on_init_widget(self):
        super(LobbyNextDayHotSteelEntryWidget, self).on_init_widget()
        self.activity_type = '53'

        @self.panel.btn.unique_callback()
        def OnClick(*args):
            jump_to_ui_utils.jump_to_activity(self.activity_type)

    def on_finalize_widget(self):
        super(LobbyNextDayHotSteelEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        pass