# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Improvise/ImproviseRoundPrompUI.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.timer import CLOCK

class ImproviseRoundPrompUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_3v3/3v3_jushu'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self._round = 1
        self._theme_text_id = None
        self._last_time = None
        self._delay_close_timer_id = None
        self._refresh_view()
        self.panel.PlayAnimation('show')
        anim_time = self.panel.GetAnimationMaxRunTime('show')
        self._set_last_time(anim_time)
        return

    def on_finalize_panel(self):
        self._safe_cancel_delay_close_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update(self, round_num, theme_text_id):
        self._round = round_num
        self._theme_text_id = theme_text_id
        self._refresh_view()

    def set_early_begin(self, early):
        self.panel.nd_time.setVisible(early)

    def _refresh_view(self):
        self.panel.lab_round_num.SetString(str(self._round))
        theme_text = get_text_by_id(self._theme_text_id) if self._theme_text_id is not None else ''
        self.panel.lab_zhuti.SetString(theme_text)
        return

    def _set_last_time(self, last_time):
        last_time = max(last_time, 0)
        self._last_time = last_time
        if self._last_time == 0:
            self.close()
            return
        self._safe_cancel_delay_close_timer()

        def func():
            self.close()

        self._delay_close_timer_id = global_data.game_mgr.register_logic_timer(func, interval=self._last_time, times=1, mode=CLOCK)

    def _safe_cancel_delay_close_timer(self):
        if self._delay_close_timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._delay_close_timer_id)
        self._delay_close_timer_id = None
        return