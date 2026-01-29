# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyAlphaAdvanceEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase

class LobbyAlphaAdvanceEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {}

    @classmethod
    def check_shown(cls, widget_type):
        return global_data.player.is_old_alpha_plan_enabled() and not global_data.player.has_set_hide_newbiepass_ui()

    def on_init_widget(self):
        super(LobbyAlphaAdvanceEntryWidget, self).on_init_widget()
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)

    def on_finalize_widget(self):
        super(LobbyAlphaAdvanceEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        pass

    def on_click_btn(self, *args):
        from logic.gcommon.common_const.task_const import TASK_TYPE_ASSESS
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def show_ui():
            ui = global_data.ui_mgr.get_ui('NewbiePassUI')
            if not ui:
                ui = global_data.ui_mgr.show_ui('NewbiePassUI', 'logic.comsys.battle_pass')
            ui.show()

        player = global_data.player
        setting = player.get_hide_newbiepass_ui_setting()
        if not setting and player.has_received_all_newbiepass_reward():

            def confirm_hide_ui():
                player.write_hide_newbiepass_ui_setting(1)
                self.parent.refresh_widget_list()
                task_ui = global_data.ui_mgr.get_ui('TaskMainUI')
                if task_ui:
                    task_ui.close_task(TASK_TYPE_ASSESS)

            SecondConfirmDlg2().confirm(content=608066, confirm_callback=confirm_hide_ui, cancel_callback=show_ui)
        else:
            show_ui()