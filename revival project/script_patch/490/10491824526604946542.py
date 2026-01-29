# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyAnniversaryLiveEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import jump_to_ui_utils
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon.time_utility import get_server_time

class LobbyAnniversaryLiveEntryWidget(LobbyEntryWidgetBase):
    TIMER_TAG = 210820

    def on_init_widget(self):
        super(LobbyAnniversaryLiveEntryWidget, self).on_init_widget()
        self._second_timer = None
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)
        self.panel.PlayAnimation('loop')
        self.start_tick()
        return

    def start_tick(self):
        from common.utils.timer import CLOCK
        left_time = self.get_end_time() - get_server_time() + 1
        if self._second_timer:
            global_data.game_mgr.unregister_logic_timer(self._second_timer)
            self._second_timer = None

        def cb():
            self._second_timer = None
            self.check_close()
            return

        if left_time > 0:
            self._second_timer = global_data.game_mgr.register_logic_timer(cb, interval=left_time, times=1, mode=CLOCK)
        return

    def check_close(self):
        cur_time = get_server_time()
        if cur_time >= self.get_end_time() - 1:
            if self.panel and self.panel.isValid():
                self.panel.setVisible(False)

    def on_finalize_widget(self):
        super(LobbyAnniversaryLiveEntryWidget, self).on_finalize_widget()
        if self._second_timer:
            global_data.game_mgr.unregister_logic_timer(self._second_timer)
            self._second_timer = None
        return

    def on_click_btn(self, *args):

        def enter():
            cur_time = get_server_time()
            start_time = self.get_start_time()
            if cur_time > self.get_end_time():
                global_data.game_mgr.show_tip(get_text_by_id(81796))
                self.panel.setVisible(False)
                return
            if cur_time < start_time:
                return
            from logic.gcommon.common_const import battle_const
            if global_data.player:
                global_data.player.call_server_method('apply_not_ready_match', (battle_const.KIZUNA_AI_CONCERT_TID,))

        cur_time = get_server_time()
        start_time = self.get_start_time()
        if cur_time > start_time:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_by_id(610536), confirm_callback=enter)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(610535))

    def get_start_time(self):
        from common.cfg import confmgr
        time_list = confmgr.get('game_mode/concert/play_data', str('concert_time_conf'), default=[])
        if time_list:
            return time_list[0]
        else:
            return 0

    def get_end_time(self):
        from logic.gcommon.common_const import activity_const as acconst
        from common.cfg import confmgr
        conf = confmgr.get('c_activity_config', str(acconst.ACTIVITY_ANNIVERSARY_LIVE_ENTRY))
        return conf.get('cEndTime', 0)