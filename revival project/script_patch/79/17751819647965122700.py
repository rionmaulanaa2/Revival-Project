# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8033AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN6
from logic.gcommon.common_const.skill_const import SKILL_8033_SCAN

class Mecha8033AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8033'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN6: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.RecordAnimationNodeState('show_tips_blue')
        self.panel.RecordAnimationNodeState('show_sub')
        self.panel.RecordAnimationNodeState('disappear_sub')
        super(Mecha8033AimUI, self).on_init_panel()
        self.energy_percent = 0.01

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_SET_MECAH_MODE', self.set_mecha_mode)
            regist_func('E_ACC_SKILL_BEGIN', self.on_begin_second_weapon)
            regist_func('E_ACC_SKILL_END', self.on_end_second_weapon)
            regist_func('E_TEMP_CHANGE_WEAPON_POS', self.on_change_weapon_pos)
            regist_func('E_ENERGY_CHANGE', self.on_energy_change)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
            self.set_mecha_mode()
            self.mecha.send_event('E_MECHA_VEHICLE_SPREAD')

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SET_MECAH_MODE', self.set_mecha_mode)
            unregist_func('E_ACC_SKILL_BEGIN', self.on_begin_second_weapon)
            unregist_func('E_ACC_SKILL_END', self.on_end_second_weapon)
            unregist_func('E_TEMP_CHANGE_WEAPON_POS', self.on_change_weapon_pos)
            unregist_func('E_ENERGY_CHANGE', self.on_energy_change)
        self.mecha = None
        return

    def on_change_weapon_pos(self, pos):
        self.aim_spread_mgr and self.aim_spread_mgr.set_weapon_pos(pos)

    def set_mecha_mode(self, *args):
        if not (self.mecha and self.mecha.is_valid()):
            return
        if self.mecha.sd.ref_is_car_shape:
            path = 'gui/ui_res_2/battle/mech_attack/mech_8033/img_mech_8033_aim2.png'
            weapon_pos = PART_WEAPON_POS_MAIN6
        else:
            path = 'gui/ui_res_2/battle/mech_attack/mech_8033/img_mech_8033_aim.png'
            weapon_pos = PART_WEAPON_POS_MAIN1
        self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', weapon_pos)
        self.aim_spread_mgr and self.aim_spread_mgr.set_weapon_pos(weapon_pos)
        self.panel.img_ring.SetDisplayFrameByPath('', path)

    def on_begin_second_weapon(self, *args):
        self.panel.StopAnimation('disappear_sub')
        self.panel.RecoverAnimationNodeState('disappear_sub')
        self.panel.PlayAnimation('show_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)

    def on_end_second_weapon(self, *args):
        self.panel.StopAnimation('show_sub')
        self.panel.RecoverAnimationNodeState('show_sub')
        self.panel.PlayAnimation('disappear_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_energy_change(self, key, percent):
        if key == SKILL_8033_SCAN:
            if self.energy_percent == percent:
                return
            self.energy_percent = percent
            if percent >= 1.0:
                self.panel.PlayAnimation('show_tips_blue')
            else:
                self.panel.StopAnimation('show_tips_blue')
                self.panel.RecoverAnimationNodeState('show_tips_blue')