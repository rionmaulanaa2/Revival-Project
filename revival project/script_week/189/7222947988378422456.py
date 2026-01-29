# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/ArtCollectionActivityEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.OldLobbyEntryWidgetBase import OldLobbyEntryWidgetBase
from logic.gutils import activity_utils, loop_lottery_utils
from logic.gcommon import time_utility as tutil

class ArtCollectionActivityEntryWidget(OldLobbyEntryWidgetBase):

    def __init__(self, parent_ui, panel, activity_type, ui_name, ui_path, entry_button_name='btn_activity', lottery_id=None):
        ui_config = {'entry_button_name': entry_button_name,
           'ui_name': ui_name,
           'ui_path': ui_path
           }
        event_conf = {'receive_task_reward_succ_event': self.refresh_red_point,
           'task_prog_changed': self.refresh_red_point,
           'message_update_global_reward_receive': self.refresh_red_point,
           'receive_task_prog_reward_succ_event': self.refresh_red_point,
           'message_update_global_stat': self.refresh_red_point,
           'refresh_activity_list': self.on_refresh_activity
           }
        self.activity_type = activity_type
        self.lottery_id = lottery_id
        super(ArtCollectionActivityEntryWidget, self).__init__(parent_ui, panel, ui_config, event_conf)

    def destroy(self):
        super(ArtCollectionActivityEntryWidget, self).destroy()

    def get_activity_list(self):
        return activity_utils.get_ordered_activity_list(self.activity_type)

    def is_activity_open(self):
        if self.lottery_id and loop_lottery_utils.is_loop_lottery(self.lottery_id):
            goods_open_info, shop_open_info = loop_lottery_utils.get_loop_lottery_open_info(self.lottery_id)
            left_time = goods_open_info[2] - tutil.time() if goods_open_info else 0
            if left_time < 0.1:
                return False
            else:
                return True

        else:
            return super(ArtCollectionActivityEntryWidget, self).is_activity_open()