# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8035AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1

class Mecha8035AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8035'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('show_bullet')
        super(Mecha8035AimUI, self).on_init_panel()

    def init_parameters(self):
        super(Mecha8035AimUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def disappear(self):
        self.panel.PlayAnimation('disappear_bullet')
        super(Mecha8035AimUI, self).disappear()

    def on_finalize_panel(self):
        super(Mecha8035AimUI, self).on_finalize_panel()

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ACC_SKILL_BEGIN', self.on_acc_skill_begin)
            regist_func('E_ACC_SKILL_END', self.on_acc_skill_end)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_BEGIN', self.on_acc_skill_begin)
            unregist_func('E_ACC_SKILL_END', self.on_acc_skill_end)
        self.mecha = None
        return

    def on_acc_skill_begin(self, *args):
        self.panel.StopAnimation('disappear_sub_weapon')
        self.panel.PlayAnimation('show_sub_weapon')

    def on_acc_skill_end(self, *args):
        self.panel.StopAnimation('show_sub_weapon')
        self.panel.PlayAnimation('disappear_sub_weapon')