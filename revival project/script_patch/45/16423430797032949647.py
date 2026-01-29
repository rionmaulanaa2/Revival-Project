# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/Calendar/CalendarModeIntroUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from common.const import uiconst
import datetime
import cc
from common.framework import Functor
from logic.gcommon.common_const.activity_const import ACTIVITY_TIME_NOTICE_DATE_KEY
from logic.gcommon.common_const.activity_const import ACTIVITY_ID_2, ACTIVITY_ID_3
from logic.gcommon.common_const.activity_const import ACTIVITY_STATUS_END, ACTIVITY_STATUS_UNSTART, ACTIVITY_STATUS_GOING
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gcommon.time_utility import UTC

class CalendarModeIntroUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/mode_calendar_mode_introduce'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_close.btn_back.OnClick': 'on_click_close'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self):
        self.battle_type = None
        self.mode_id = None
        return

    def on_finalize_panel(self):
        pass

    def init_intro_panel(self, mode_id, battle_type):
        self.mode_id = mode_id
        self.battle_type = battle_type
        conf = confmgr.get('c_battle_mode_show_config', str(mode_id))
        tip_confs = conf.get('cPlayTips', [])
        if not tip_confs:
            return
        from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
        ui = PlayIntroduceUI(self.panel.nd_mode_introduce, *tip_confs)
        ui.set_panel_custom_by_other_panel()
        self.init_button_status()

    def init_button_status(self):
        archive_data = global_data.achi_mgr.get_general_archive_data()
        mode_dict = archive_data.get_field(ACTIVITY_TIME_NOTICE_DATE_KEY, {})

        def on_click_reserve(panel, battle_type, is_going, *args):
            if not is_going:
                panel.lab_tips.SetString(get_text_by_id(19851))
                panel.temp_btn_1.btn_common_big.SetEnable(False)
                panel.temp_btn_1.btn_common_big.SetText(get_text_by_id(19852))
                archive_data = global_data.achi_mgr.get_general_archive_data()
                mode_dict = archive_data.get_field(ACTIVITY_TIME_NOTICE_DATE_KEY, {})
                mode_dict[battle_type] = True
                archive_data.set_field(ACTIVITY_TIME_NOTICE_DATE_KEY, mode_dict)
                global_data.emgr.reserve_activity_changed.emit()
            else:
                global_data.ui_mgr.close_ui('CalendarModeIntroUI')
                global_data.ui_mgr.close_ui('CalendarModeTipsUI')
                global_data.ui_mgr.close_ui('CalendarUI')
                global_data.ui_mgr.close_ui('PlayIntroduceUI')

        ac_list2 = confmgr.get('battle_opentime_config', ACTIVITY_ID_2)
        ac_list3 = confmgr.get('battle_opentime_config', ACTIVITY_ID_3)
        ac_list = []
        ac_list.extend(ac_list2)
        ac_list.extend(ac_list3)
        ac_status_list = []
        now = datetime.datetime.fromtimestamp(tutil.time())
        now = datetime.datetime(year=now.year, month=now.month, day=now.day, tzinfo=UTC(8))
        for ac in ac_list:
            if ac['battle_type'] == self.battle_type:
                st_date = datetime.datetime(tzinfo=UTC(8), *[ int(x) for x in ac['start_date'] ])
                ed_date = datetime.datetime(tzinfo=UTC(8), *[ int(x) for x in ac['end_date'] ])
                status = self.get_activity_status(st_date, ed_date, now)
                ac_status_list.append(status)

        final_status = None
        has_going = False
        has_unstart = False
        for status in ac_status_list:
            if status == ACTIVITY_STATUS_GOING:
                has_going = True
            elif status == ACTIVITY_STATUS_UNSTART:
                has_unstart = True

        if has_going:
            final_status = ACTIVITY_STATUS_GOING
        else:
            final_status = ACTIVITY_STATUS_UNSTART
        if final_status == ACTIVITY_STATUS_GOING:
            self.panel.lab_tips.SetString(get_text_by_id(19849))
            self.panel.temp_btn_1.btn_common_big.SetText(get_text_by_id(19850))
            self.panel.temp_btn_1.btn_common_big.OnClick = Functor(on_click_reserve, self.panel, self.battle_type, True)
        elif mode_dict.get(self.battle_type, None):
            self.panel.lab_tips.SetString(get_text_by_id(19851))
            self.panel.temp_btn_1.btn_common_big.SetEnable(False)
            self.panel.temp_btn_1.btn_common_big.SetText(get_text_by_id(19852))
        else:
            self.panel.lab_tips.SetString(get_text_by_id(19853))
            self.panel.temp_btn_1.btn_common_big.SetText(get_text_by_id(19854))
            self.panel.temp_btn_1.btn_common_big.OnClick = Functor(on_click_reserve, self.panel, self.battle_type, False)
        return

    def get_activity_status(self, ac_start, ac_end, now):
        if now > ac_end:
            return ACTIVITY_STATUS_END
        else:
            if now < ac_start:
                return ACTIVITY_STATUS_UNSTART
            return ACTIVITY_STATUS_GOING

    def on_click_close(self, *args):
        global_data.ui_mgr.close_ui('PlayIntroduceUI')
        self.close()