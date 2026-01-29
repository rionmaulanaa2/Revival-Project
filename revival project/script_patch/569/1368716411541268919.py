# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8017AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2

class Mecha8017AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8017'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('show_bullet')
        super(Mecha8017AimUI, self).on_init_panel()
        self.init_auto_aim_widget()

    def init_parameters(self):
        self.second_weapon_on = False
        self.main_weapon_aim_helper_enabled = False
        self.main_weapon_enhanced = False
        super(Mecha8017AimUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def init_auto_aim_widget(self):
        from .MechaAutoAimWidget import MechaAutoAimWidget
        self.auto_aim_widget = MechaAutoAimWidget(self.panel)

    def disappear(self):
        self.panel.PlayAnimation('disappear_bullet')
        super(Mecha8017AimUI, self).disappear()

    def on_finalize_panel(self):
        super(Mecha8017AimUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ACC_SKILL_BEGIN', self.on_begin_second_weapon)
            regist_func('E_ACC_SKILL_END', self.on_end_second_weapon)
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_main_weapon_aim)
            regist_func('E_ENHANCE_MAIN_WEAPON', self.on_enhance_main_weapon)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_BEGIN', self.on_begin_second_weapon)
            unregist_func('E_ACC_SKILL_END', self.on_end_second_weapon)
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_main_weapon_aim)
            unregist_func('E_ENHANCE_MAIN_WEAPON', self.on_enhance_main_weapon)
        self.mecha = None
        return

    def on_begin_second_weapon(self, *args):
        self.second_weapon_on = True
        self.panel.PlayAnimation('show_sub_weapon')
        self.panel.PlayAnimation('disappear_bullet')
        if self.main_weapon_enhanced:
            self.panel.StopAnimation('show_sp')
            self.panel.PlayAnimation('disappear_sp')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)

    def on_end_second_weapon(self, *args):
        self.second_weapon_on = False
        self.panel.StopAnimation('show_sub_weapon')
        self.panel.PlayAnimation('disappear_sub_weapon')
        if self.main_weapon_enhanced:
            self.panel.PlayAnimation('show_sp')
        else:
            self.panel.StopAnimation('disappear_bullet')
            self.panel.PlayAnimation('show_bullet')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def enable_main_weapon_aim(self, enabled, weapon_pos, **kwargs):
        if enabled ^ self.main_weapon_aim_helper_enabled:
            self.main_weapon_aim_helper_enabled = enabled
            if enabled and self.auto_aim_widget.refresh_auto_aim_range_appearance(weapon_pos):
                self.auto_aim_widget.show()
                self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
                self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_target, weapon_pos)
            else:
                self.auto_aim_widget.hide()
                self.auto_aim_widget.update_aim_target(None, weapon_pos)
        return

    def on_enhance_main_weapon(self, flag):
        self.main_weapon_enhanced = flag
        if flag:
            if not self.second_weapon_on:
                self.panel.StopAnimation('disappear_sp')
                self.panel.PlayAnimation('show_sp')
        elif not self.second_weapon_on:
            self.panel.StopAnimation('show_sp')
            self.panel.PlayAnimation('disappear_sp')
            self.panel.StopAnimation('disappear_bullet')
            self.panel.PlayAnimation('show_bullet')