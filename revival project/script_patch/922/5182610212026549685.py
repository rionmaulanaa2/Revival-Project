# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyYueKaEntryWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon import time_utility as tutil

class LobbyYueKaEntryWidget(BaseUIWidget):
    DELAY_SHOW_TAG = 31415926
    LAST_READ_MARK_KEY = 'last_read_yueka_lobby_tips_time'

    def __init__(self, panel_cls, panel):
        super(LobbyYueKaEntryWidget, self).__init__(panel_cls, panel)
        self._init_data()
        self._init_view()
        self.process_event(True)
        self._init_ui_events()

    def destroy(self):
        self._stop_check_tips_timer()
        self.process_event(False)
        super(LobbyYueKaEntryWidget, self).destroy()

    def _init_data(self):
        self._check_tips_timer_id = None
        return

    def _init_view(self):
        self.panel.RecordAnimationNodeState('month_show')
        self.panel.RecordAnimationNodeState('month_loop')
        self._start_check_tips_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_month_card_info': self._on_update_month_card_info
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_ui_events(self):

        @self.panel.btn_month_card.callback()
        def OnClick(b, t):
            if self._is_shown():
                self._mark_read_renew_tips()
            self.on_entry_btn_click(b, t)

    def _is_shown(self):
        return self.panel.nd_month_tips.isVisible()

    def _show(self):
        self.panel.nd_month_tips.setVisible(True)
        self._play_show_anim()

    def _hide(self):
        self.panel.nd_month_tips.setVisible(False)
        self._stop_show_anim()

    def on_lobby_ui_hide(self):
        pass

    def _get_day_no(self, now=None):
        if now is None:
            now = tutil.get_server_time()
        return tutil.get_rela_day_no(now, tutil.CYCLE_DATA_REFRESH_TYPE_2)

    def _mark_read_renew_tips(self):
        cur_day_no = self._get_day_no()
        global_data.achi_mgr.set_cur_user_archive_data(self.LAST_READ_MARK_KEY, cur_day_no)
        self._tips_checker()

    def on_entry_btn_click(self, btn, touch):
        from logic.gcommon.common_const.activity_const import ACTIVITY_YUEKA_NEW
        from logic.comsys.charge_ui.ChargeUINew import ChargeUINew
        ui = global_data.ui_mgr.get_ui('ChargeUINew')
        if not ui:
            ui = ChargeUINew(None, ACTIVITY_YUEKA_NEW)
        ui.switch_to_activity_page(ACTIVITY_YUEKA_NEW)
        return

    def _stop_show_anim(self):
        self.panel.StopAnimation('month_show')
        self.panel.StopAnimation('month_loop')

    def _play_show_anim(self):
        self._stop_show_anim()
        self.panel.RecoverAnimationNodeState('month_show')
        self.panel.RecoverAnimationNodeState('month_loop')
        self.panel.PlayAnimation('month_show')
        delay = self.panel.GetAnimationMaxRunTime('month_show')

        def cb():
            self.panel.PlayAnimation('month_loop')

        self.panel.btn_month_card.DelayCallWithTag(delay, cb, self.DELAY_SHOW_TAG)

    def _update_day_text(self, remaining_time):
        lab_node = self.panel.lab_month_tips
        text_id = 607243
        from logic.gcommon.common_utils.local_text import get_text_by_id
        format_text = get_text_by_id(text_id)
        day_text = self._get_day_text(remaining_time)
        text = format_text.format(day_text)
        lab_node.SetString(text)

    def _get_day_text(self, delta_time):
        day, hour, minute, second = tutil.get_day_hour_minute_second(delta_time)
        if day > 0:
            return str(day)
        else:
            return '<1'

    def _should_show(self):
        cur_day_no = self._get_day_no()
        last_read_day_no = global_data.achi_mgr.get_cur_user_archive_data(self.LAST_READ_MARK_KEY, default=0)
        if last_read_day_no == cur_day_no:
            return (False, 0.0)
        else:
            remaining_time = max(0.0, global_data.player.get_yueka_time() - tutil.get_server_time()) if global_data.player else 0.0
            remaining_day = float(remaining_time) / tutil.ONE_DAY_SECONDS
            day_delimiter = 10
            if 0 < remaining_day < day_delimiter:
                return (True, remaining_time)
            return (
             False, 0.0)

    def _start_check_tips_timer(self):
        self._stop_check_tips_timer()
        if self._check_tips_timer_id:
            return
        from common.utils.timer import CLOCK
        interval = tutil.ONE_MINUTE_SECONDS
        self._check_tips_timer_id = global_data.game_mgr.register_logic_timer(func=self._tips_checker, times=-1, mode=CLOCK, interval=interval)
        self._tips_checker()

    def _stop_check_tips_timer(self):
        if self._check_tips_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._check_tips_timer_id)
        self._check_tips_timer_id = None
        return

    def _tips_checker(self):
        show, remaining_time = self._should_show()
        if show:
            if not self._is_shown():
                self._show()
            self._update_day_text(remaining_time)
        else:
            self._hide()

    def _on_update_month_card_info(self, *args):
        self._tips_checker()