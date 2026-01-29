# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/report/RoomReportUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_const.log_const import REPORT_REASON_ILLEGAL_ROOM_NAME, REPORT_FROM_TYPE_CUSTOM_ROOM, REPORT_CLASS_ROOM, REPORT_ROOM_DAY_LIMIT, REPORT_ROOM_TIMES
from .SysReportUI import SysReportUI
from logic.gcommon.common_utils.local_text import get_text_by_id

class RoomReportUI(SysReportUI):
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    PANEL_CONFIG_NAME = 'room/i_room_report_window'
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'report_window'

    def on_init_panel(self, *args, **kwargs):
        super(RoomReportUI, self).on_init_panel()
        self.room_id = -1
        self.room_name = ''
        self.init_remain_times()

    def set_room_info(self, room_info):
        self.room_id = room_info.get('room_id', -1)
        self.creator = room_info.get('creator', -1)
        self.room_name = room_info.get('name', '')
        self.panel.lab_player_name.SetString(self.room_name)

    def init_remain_times(self):
        player = global_data.player
        if not player:
            self.panel.lab_remain.setVisible(False)
            return
        self.panel.lab_remain.setVisible(True)
        times = player.get_report_room_times()
        self.panel.lab_remain.SetString(get_text_by_id(606034, (times, REPORT_ROOM_DAY_LIMIT)))

    def on_click_confirm_btn(self, *args):
        report_reasons = [
         REPORT_REASON_ILLEGAL_ROOM_NAME]
        if not self.check_user_lv_can_report():
            return
        report_data = {'reason': report_reasons,
           'name': self.room_name,
           'creator': self.creator
           }
        global_data.player and global_data.player.report_custom_room(REPORT_FROM_TYPE_CUSTOM_ROOM, self.room_id, report_data)
        self.close()

    def on_report_times_change(self, type, times):
        if type != REPORT_ROOM_TIMES:
            return
        if not self.panel or not self.panel.isValid():
            return
        if not self.panel.lab_remain:
            return
        self.panel.lab_remain.SetString(get_text_by_id(606034, (times, REPORT_ROOM_DAY_LIMIT)))