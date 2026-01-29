# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/report/ClanReportUI.py
from __future__ import absolute_import
from logic.gcommon.common_const.log_const import REPORT_REASON_ILLEGAL_CLAN_NAME, REPORT_REASON_ILLEGAL_CLAN_INTRO, REPORT_FROM_TYPE_CLAN, REPORT_CLASS_CLAN, REPORT_CLAN_DAY_LIMIT, REPORT_CLAN_TIMES
from logic.gutils.new_template_utils import MultiChooseWidget
from .SysReportUI import SysReportUI
from logic.gcommon.common_utils.local_text import get_text_by_id

class ClanReportUI(SysReportUI):
    PANEL_CONFIG_NAME = 'crew/i_crew_report'
    TEMPLATE_NODE_NAME = 'report_window'
    SEND_CD = 1

    def on_init_panel(self, *args, **kwargs):
        super(ClanReportUI, self).on_init_panel()
        self.clan_id = -1
        self.clan_name = ''
        self.clan_intro = ''
        self.init_remain_times()
        self.init_report_reasons()
        self.set_custom_close_func(self.on_click_close_btn)

    def init_remain_times(self):
        player = global_data.player
        if not player:
            self.panel.lab_remain.setVisible(False)
            return
        self.panel.lab_remain.setVisible(True)
        times = player.get_report_clan_times()
        self.panel.lab_remain.SetString(get_text_by_id(606034, (times, REPORT_CLAN_DAY_LIMIT)))

    def init_report_reasons(self):
        name_container = self.panel.nd_player.report_container
        name_container.SetInitCount(1)
        name_items = name_container.GetAllItem()
        self.name_widget = MultiChooseWidget()
        self.name_widget.init(self.panel, name_items, [])
        self.name_widget.SetCallbacks(None, None)
        intro_container = self.panel.nd_announce.report_container
        intro_container.SetInitCount(1)
        intro_items = intro_container.GetAllItem()
        self.intro_widget = MultiChooseWidget()
        self.intro_widget.init(self.panel, intro_items, [])
        return

    def set_clan_info(self, clan_info):
        self.clan_id = clan_info.get('clan_id')
        self.panel.nd_player.lab_player_name.SetString(clan_info.get('clan_name', ''))
        self.panel.nd_announce.lab_player_name.SetString(clan_info.get('clan_intro', ''))

    def on_click_confirm_btn(self, *args):
        report_reasons = []
        if self.name_widget.GetSelects():
            report_reasons.append(REPORT_REASON_ILLEGAL_CLAN_NAME)
        if self.intro_widget.GetSelects():
            report_reasons.append(REPORT_REASON_ILLEGAL_CLAN_INTRO)
        if not report_reasons:
            return
        if not self.check_user_lv_can_report():
            return
        report_data = {'reason': report_reasons}
        global_data.player and global_data.player.report_clan(REPORT_FROM_TYPE_CLAN, self.clan_id, report_data)
        self.close()

    def on_report_times_change(self, type, times):
        if type != REPORT_CLAN_TIMES:
            return
        if not self.panel or not self.panel.isValid():
            return
        if not self.panel.lab_remain:
            return
        self.panel.lab_remain.SetString(get_text_by_id(606034, (times, REPORT_CLAN_DAY_LIMIT)))