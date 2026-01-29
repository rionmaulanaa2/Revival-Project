# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/OldLobbyAnnivEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.OldLobbyEntryWidgetBase import OldLobbyEntryWidgetBase
from logic.gutils import activity_utils
import logic.gcommon.common_const.activity_const as activity_const
import cc

class OldLobbyAnnivEntryWidgetBase(OldLobbyEntryWidgetBase):

    def __init__(self, parent_ui, panel):
        ui_config = {'entry_button_name': 'btn_activity_1',
           'ui_name': 'ActivityAnnivMainUI',
           'ui_path': 'logic.comsys.activity',
           'animation_name': ''
           }
        event_conf = {'receive_task_reward_succ_event': self.refresh_red_point,
           'task_prog_changed': self.refresh_red_point
           }
        super(OldLobbyAnnivEntryWidgetBase, self).__init__(parent_ui, panel, ui_config, event_conf)
        self.display_flag_anim()

    def destroy(self):
        super(OldLobbyAnnivEntryWidgetBase, self).destroy()

    def get_activity_list(self):
        return activity_utils.get_ordered_activity_list(activity_const.WIDGET_ANNIV)

    def _refresh_widget(self):
        entry_button_name = self.ui_config.get('entry_button_name')
        entry_btn = getattr(self.panel, entry_button_name) if entry_button_name else None
        if not entry_btn:
            return
        else:
            if not self.is_activity_open():
                entry_btn.setVisible(False)
                return
            animation_name = self.ui_config.get('animation_name')
            if animation_name:
                self.panel.PlayAnimation(animation_name)
            self.panel.PlayAnimation('activity_loop')
            self.panel.PlayAnimation('flag_loop')
            entry_btn.setVisible(True)

            @entry_btn.callback()
            def OnClick(b, t):
                self.on_entry_btn_click(b, t)
                if self.panel:
                    self.panel.PlayAnimation('flag_disappear')

            return

    def display_flag_anim(self):
        if not self.panel:
            return
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.show_flag_node()),
         cc.DelayTime.create(5),
         cc.CallFunc.create(lambda : self.hide_flag_node())]))

    def show_flag_node(self):
        if self.panel:
            self.panel.PlayAnimation('flag_show')

    def hide_flag_node(self):
        if self.panel:
            self.panel.PlayAnimation('flag_disappear')