# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaWaterWarningUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
import logic.gcommon.time_utility as t_util
from logic.gcommon.common_const.mecha_const import MECHA_WATER_BROKEN_TIME as DIVING_TIME_OUT
from logic.gutils import mecha_utils
from common.const import uiconst

class MechaWaterWarningUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_water_warning'
    DLG_ZORDER = UI_TYPE_MESSAGE - 1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}
    HIDE_UI_LIST = mecha_utils.MECHA_FRONT_UI_LIST

    def on_init_panel(self):
        self.panel.setLocalZOrder(self.DLG_ZORDER)
        self.init_parameters()
        self.init_event()
        self.panel.PlayAnimation('show_warning')
        self.set_progress(100)
        self.start_timer()

    def do_hide_main_ui(self):
        self.hide_main_ui(self.HIDE_UI_LIST)

    def do_show_panel(self):
        super(MechaWaterWarningUI, self).do_show_panel()
        self.hide_main_ui(self.HIDE_UI_LIST)

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        self.last_lv = None
        self.show_main_ui()
        return

    def init_parameters(self):
        self.player = None
        self.last_lv = None
        self._timer = None
        self._t_start = 0
        if global_data.player:
            self.on_player_setted(global_data.player.logic)
        return

    def init_event(self):
        mecha = global_data.mecha
        if mecha and mecha.logic:
            mecha = mecha.logic
            self.mecha = mecha
            self.on_mecha_setted(mecha)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_ui_event(self.player)

    def on_mecha_setted(self, mecha):
        if mecha:
            regist_func = mecha.regist_event
            regist_func('E_ON_LEAVE_MECHA_START', self.on_start_leave_mecha)

    def bind_ui_event(self, target):
        if target:
            regist_func = target.regist_event

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
            mecha = global_data.mecha
            if mecha and mecha.logic:
                unregist_func = mecha.logic.unregist_event
                unregist_func('E_ON_LEAVE_MECHA_START', self.on_start_leave_mecha)

    def set_progress(self, pg):
        self.panel.nd_pro.pro.setPercentage(int(pg))

    def start_timer(self):
        self.stop_timer()
        self._t_start = t_util.time()
        self._timer = global_data.game_mgr.register_logic_timer(self.on_timer_tick, interval=0.1)

    def stop_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)

    def on_timer_tick(self):
        if not self.is_valid():
            return
        t_diff = t_util.time() - self._t_start
        percent = max(0, DIVING_TIME_OUT - t_diff) / DIVING_TIME_OUT * 100.0
        self.set_progress(percent)
        if t_diff > DIVING_TIME_OUT:
            self.on_time_out()

    def on_time_out(self):
        self.stop_timer()
        self.close()

    def on_start_leave_mecha(self, *args):
        self.close()