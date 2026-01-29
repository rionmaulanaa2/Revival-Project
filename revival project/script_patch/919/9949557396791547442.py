# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyAlphaPlanEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const

class LobbyAlphaPlanEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {}

    def on_init_widget(self):
        super(LobbyAlphaPlanEntryWidget, self).on_init_widget()

        @self.panel.btn.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('AlphaPlanMainUI', 'logic.comsys.activity.NewAlphaPlan')

    def on_finalize_widget(self):
        super(LobbyAlphaPlanEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(need_red_point)

    def need_show_red_point(self):
        from common.utils.redpoint_check_func import check_lobby_red_point
        if not check_lobby_red_point():
            return False
        activity_list = self.get_activity_list()
        count = activity_utils.get_activity_red_point_count_by_activity_list(activity_list)
        return count > 0