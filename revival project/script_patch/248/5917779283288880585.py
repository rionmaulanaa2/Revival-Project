# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaNingNingAimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2

class MechaNingNingAimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8001'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def init_parameters(self):
        self.is_shooting = False
        self._start_second_fire = False
        super(MechaNingNingAimUI, self).init_parameters()

    def weapon_attack(self, weapon_pos):
        if weapon_pos == PART_WEAPON_POS_MAIN2:
            self.panel.PlayAnimation('missile_using')
            self._start_second_fire = True

    def on_fire(self, cd_time, weapon_pos, *args):
        if weapon_pos == PART_WEAPON_POS_MAIN2:
            if self._start_second_fire:
                self._start_second_fire = False
            self.panel.SetTimeOut(cd_time + 0.04, lambda : self.panel.PlayAnimation('missile_disappear'), 181127)

    def set_recover_show(self, show):
        self.panel.nd_missile.nd_missile_left.prog_using.SetPercentage(100)
        self.panel.nd_missile.nd_missile_left.prog_cd.SetPercentage(0)
        self.panel.nd_missile.nd_missile_left.prog_using.setVisible(not show)
        self.panel.nd_missile.nd_missile_left.prog_cd.setVisible(show)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_FIRE', self.on_fire)
            regist_func('WEAPON_ATTACK_SUCCESS', self.weapon_attack)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_FIRE', self.on_fire)
            unregist_func('WEAPON_ATTACK_SUCCESS', self.weapon_attack)
        self.mecha = None
        return

    def on_reload_bullet(self, reload_time, times, *args):
        self.show_reload_ui(False)
        self.panel.DelayCall(reload_time, lambda : self.show_reload_ui(True))

    def show_reload_ui(self, flag):
        self.panel.nd_aim.setVisible(flag)