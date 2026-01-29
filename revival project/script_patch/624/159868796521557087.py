# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8013SubUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import AIM_ZORDER
from common.utils.timer import LOGIC, RELEASE
import logic.gcommon.const as g_const
from common.const import uiconst
MAX_ENERGY_PERCENT = 60
MIN_ENERGY_PERCENT = 50
ENERGY_PERCENT_GAP = MAX_ENERGY_PERCENT - MIN_ENERGY_PERCENT

class Mecha8013SubUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8013_sub'
    DLG_ZORDER = AIM_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_events()
        self.panel.nd_sp.setVisible(False)

    def init_parameters(self):
        self.player = None
        self.mecha = None
        return

    def init_events(self):
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {}
        emgr.bind_events(econf)

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_ui_event(self.player)

    def init_mecha_event(self, flag):
        mecha = self.mecha
        func = None
        if flag:
            func = mecha.regist_event
        else:
            func = mecha.unregist_event
        func('E_RANGE_SEE_THROUGHT_START', self.on_see_throught_start)
        func('E_RANGE_SEE_THROUGHT_STOP', self.on_see_throught_stop)
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            self.init_mecha_event(True)

    def bind_ui_event(self, target):
        pass

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            pass
        if self.mecha and self.mecha.is_valid():
            self.init_mecha_event(False)
        self.mecha = None
        return

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        return

    def on_see_throught_start(self, left_time, total_time):
        from common import utilities
        cur_percent = utilities.safe_percent(left_time, total_time)
        cur_percent = MIN_ENERGY_PERCENT + ENERGY_PERCENT_GAP * cur_percent / 100
        self.panel.progress_heat1.SetPercent(cur_percent)
        self.panel.progress_heat2.SetPercent(cur_percent)

        def count_down(pass_time):
            percent = utilities.safe_percent(left_time - pass_time, total_time)
            percent = MIN_ENERGY_PERCENT + ENERGY_PERCENT_GAP * percent / 100
            self.panel.progress_heat1.SetPercent(percent)
            self.panel.progress_heat2.SetPercent(percent)

        self.panel.nd_sp.StopTimerAction()
        self.panel.nd_sp.TimerAction(count_down, left_time, None, interval=0.05)
        self.panel.nd_sp.setVisible(True)
        return

    def on_see_throught_stop(self):
        self.panel.nd_sp.setVisible(False)