# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaJetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import LEFT_CONTROL_ZORDER
from common.const import uiconst

class MechaJetUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_jet'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.panel.setLocalZOrder(LEFT_CONTROL_ZORDER)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.unbind_posture_ui_event(self.player)
        self.player = None
        return

    def init_parameters(self):
        self.player = None
        self.last_val_percent = 100
        self.dis_appear_anim = None
        emgr = global_data.emgr
        if global_data.player:
            self.on_player_setted(global_data.player.logic)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)
        return

    def init_event(self):
        self.panel.setVisible(False)
        mecha = global_data.mecha
        if mecha and mecha.logic:
            mecha = mecha.logic
            self.last_val_percent = mecha.ev_g_jet_energy_percent()
            if self.last_val_percent is not None:
                self.on_energy_change(self.last_val_percent)
        return

    def on_player_setted(self, player):
        self.unbind_posture_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_posture_ui_event(self.player)

    def on_mecha_setted(self, mecha):
        if mecha:
            regist_func = mecha.regist_event
            regist_func('E_MECHA_JET_ENERGY', self.on_energy_change)
            self.init_event()

    def bind_posture_ui_event(self, target):
        if target:
            pass

    def unbind_posture_ui_event(self, target):
        if target and target.is_valid():
            mecha = global_data.mecha
            if mecha and mecha.logic:
                unregist_func = mecha.logic.unregist_event
                unregist_func('E_MECHA_JET_ENERGY', self.on_energy_change)

    def on_energy_change(self, percent):
        if self.last_val_percent < percent == 100:
            self.disappear()
        elif self.last_val_percent == 100 > percent:
            self.appear()
        self.panel.prog_jet.setPercentage(percent)
        self.last_val_percent = percent

    def appear(self):
        self.panel.StopAnimation('appear')
        self.panel.StopAnimation('disappear')
        if self.dis_appear_anim:
            self.panel.stopAction(self.dis_appear_anim)
        self.panel.PlayAnimation('appear')
        self.panel.setVisible(True)

    def disappear(self):
        time = self.panel.GetAnimationMaxRunTime('disappear')

        def finished():
            if self and self.is_valid():
                self.panel.setVisible(False)

        self.panel.StopAnimation('appear')
        self.panel.StopAnimation('disappear')
        self.dis_appear_anim = self.panel.SetTimeOut(time, finished)
        self.panel.PlayAnimation('disappear')