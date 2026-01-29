# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/OldLobbyGranbelmEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.OldLobbyEntryWidgetBase import OldLobbyEntryWidgetBase
from logic.gutils import activity_utils
import logic.gcommon.common_const.activity_const as activity_const

class OldLobbyGranbelmEntryWidgetBase(OldLobbyEntryWidgetBase):

    def __init__(self, parent_ui, panel):
        ui_config = {'entry_button_name': 'btn_activity_1',
           'ui_name': 'ActivityGranbelmMainUI',
           'ui_path': 'logic.comsys.activity',
           'animation_name': 'granbelm'
           }
        event_conf = {'receive_task_reward_succ_event': self.refresh_red_point,
           'task_prog_changed': self.refresh_red_point
           }
        super(OldLobbyGranbelmEntryWidgetBase, self).__init__(parent_ui, panel, ui_config, event_conf)

    def destroy(self):
        super(OldLobbyGranbelmEntryWidgetBase, self).destroy()

    def get_activity_list(self):
        return activity_utils.get_ordered_activity_list(activity_const.WIDGET_GRANBELM)