# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/report/SysReportUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_const.log_const import REPORT_RESULT_OK
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.time_utility as t_util

class SysReportUI(WindowMediumBase):
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'report_window'
    SEND_CD = 5
    MIN_REPORT_LV = 3
    UI_ACTION_EVENT = {'btn_confirm.btn_common.OnClick': 'on_click_confirm_btn'
       }
    GLOBAL_EVENT = {'on_report_result_event': 'on_report_send_ret',
       'on_report_times_change_event': 'on_report_times_change'
       }

    def on_click_confirm_btn(self, *args):
        raise NotImplementedError

    def on_click_close_btn(self, *args):
        self.close()

    def check_user_lv_can_report(self):
        player = global_data.player
        if player and player.get_lv() < self.MIN_REPORT_LV:
            global_data.game_mgr.show_tip(get_text_by_id(80894, {'lv': int(self.MIN_REPORT_LV)}))
            return False
        return True

    def check_send_cd(self):
        if global_data._last_report_send_timestamp:
            cur_time = t_util.get_server_time()
            if cur_time - global_data._last_report_send_timestamp < self.SEND_CD:
                second_later = global_data._last_report_send_timestamp + self.SEND_CD - cur_time + 1
                global_data.game_mgr.show_tip(get_text_by_id(80895, {'time': int(second_later)}))
                return False
        return True

    def on_report_send_ret(self, ret):
        if ret == REPORT_RESULT_OK:
            self.close()

    def on_report_times_change(self, type, times):
        pass