# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8025AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from logic.gcommon.common_const.weapon_const import BAN_SHOOT_STATE
HEAT_WEAPON_ID = 802501
NORMAL_BG_PIC_PATH = 'gui/ui_res_2/battle/mech_attack/mech_8025/bg_mech_8025_prog_normal.png'
NORMAL_PROG_PIC_PATH = 'gui/ui_res_2/battle/mech_attack/mech_8025/prog_mech_8025_1.png'
HEAT_PROG_PIC_PATH = 'gui/ui_res_2/battle/mech_attack/mech_8025/prog_mech_8025_2.png'
OVERHEAT_BG_PIC_PATH = 'gui/ui_res_2/battle/mech_attack/mech_8025/bg_mech_8025_prog_hot.png'
OVERHEAT_PROG_PIC_PATH = 'gui/ui_res_2/battle/mech_attack/mech_8025/prog_mech_8025_3.png'
HEAT_PERCENT = 50

class Mecha8025AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8025'
    WEAPON_INFO = {}

    def init_parameters(self):
        self.second_aim_show = False
        self.is_overheat = False
        self.is_heat = False
        super(Mecha8025AimUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr2
        self.aim_spread_mgr = MechaAimSpreadMgr2(self.panel)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            regist_func('E_HEAT_MAGAZINE_CHANGED', self.on_heat_magazine_changed)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
            self.on_heat_magazine_changed()

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            unregist_func('E_HEAT_MAGAZINE_CHANGED', self.on_heat_magazine_changed)
        self.mecha = None
        return

    def enable_weapon_aim_helper(self, enabled, weapon_pos):
        self.second_aim_show = enabled
        if enabled:
            self.panel.PlayAnimation('show_sub')
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)
        else:
            self.panel.PlayAnimation('disappear_sub')
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_heat_magazine_changed(self):
        if self.mecha.sd.ref_heat_magazine:
            heat_magazine = self.mecha.sd.ref_heat_magazine.get(HEAT_WEAPON_ID)
            percent = heat_magazine.cur_heat_percent
            nd_hot = self.panel.nd_hot
            is_overheat = heat_magazine._state & BAN_SHOOT_STATE
            if self.is_overheat ^ is_overheat:
                if is_overheat:
                    nd_hot.bg.SetDisplayFrameByPath('', OVERHEAT_BG_PIC_PATH)
                    nd_hot.bg.prog.SetProgressTexture(OVERHEAT_PROG_PIC_PATH)
                else:
                    nd_hot.bg.SetDisplayFrameByPath('', NORMAL_BG_PIC_PATH)
                    nd_hot.bg.prog.SetProgressTexture(NORMAL_PROG_PIC_PATH)
                self.is_overheat = is_overheat
            is_heat = percent > 0.5
            if self.is_heat ^ is_heat and not self.is_overheat:
                if is_heat:
                    nd_hot.bg.prog.SetProgressTexture(HEAT_PROG_PIC_PATH)
                else:
                    nd_hot.bg.prog.SetProgressTexture(NORMAL_PROG_PIC_PATH)
                self.is_heat = is_heat
            nd_hot.bg.prog.SetPercent(59 + 32 * percent)

    def on_enter_observe(self, is_observe):
        self.panel.nd_hot.setVisible(not is_observe)