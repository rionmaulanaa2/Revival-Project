# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyPayEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const

class LobbyPayEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {}
    ACTIVITY_ID = activity_const.ACTIVITY_FIRST_PAY
    CONTAIN_ACTIVITY = False

    @classmethod
    def check_shown(cls, widget_type):
        activity_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_PAY)
        if not activity_list:
            return False
        contain = False
        for info in activity_list:
            if info.get('activity_type') == cls.ACTIVITY_ID:
                contain = True
                break

        return contain == cls.CONTAIN_ACTIVITY

    def on_init_widget(self):
        super(LobbyPayEntryWidget, self).on_init_widget()

        @self.panel.btn.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('ActivityPayMainUI', 'logic.comsys.activity.ActivityPay')

    def on_finalize_widget(self):
        super(LobbyPayEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(need_red_point)

    def need_show_red_point(self):
        activity_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_PAY)
        count = activity_utils.get_activity_red_point_count_by_activity_list(activity_list)
        return count > 0