# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8005AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from common.utils.timer import CLOCK
from .MechaBulletWidget import MAIN_WEAPON, SP_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3

class Mecha8005AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8005'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN3: SP_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def on_finalize_panel(self):
        self.stop_update_front_sight_extra_info()
        self.revert_to_defalut_bullet_type()
        super(Mecha8005AimUI, self).on_finalize_panel()

    def init_parameters(self):
        self.is_shape_shift = False
        self.check_explode_instant_timer = None
        self.is_avatar = False
        super(Mecha8005AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            self.is_avatar = mecha.ev_g_is_avatar()
            regist_func = mecha.regist_event
            regist_func('E_SHAPESHIFT', self.on_shape_shift)
            regist_func('E_ACC_SKILL_BEGIN', self._start_second_attack)
            regist_func('E_ACC_SKILL_END', self._stop_second_attack)
            regist_func('E_SHOW_DASH_HINT', self.on_show_dash_hint)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            mecha_ctrl_main_ui = global_data.ui_mgr.get_ui('MechaControlMain')
            if mecha_ctrl_main_ui and mecha_ctrl_main_ui.mecha and mecha_ctrl_main_ui.mecha != mecha:
                mecha_ctrl_main_ui.on_mecha_setted(mecha)
            if mecha:
                self.on_shape_shift(bool(mecha.ev_g_shape_shift()))

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SHAPESHIFT', self.on_shape_shift)
            unregist_func('E_ACC_SKILL_BEGIN', self._start_second_attack)
            unregist_func('E_ACC_SKILL_END', self._stop_second_attack)
            unregist_func('E_SHOW_DASH_HINT', self.on_show_dash_hint)
        self.mecha = None
        return

    def on_shape_shift(self, shape_shift):
        self.is_shape_shift = shape_shift
        self.panel.setVisible(True)
        bullet_widget = None
        if global_data.is_pc_mode:
            mecha_ctrl_main_ui = global_data.ui_mgr.get_ui('MechaControlMain')
            if mecha_ctrl_main_ui:
                bullet_widget = mecha_ctrl_main_ui.get_bullet_widget()
        else:
            bullet_widget = self.bullet_widget
        if shape_shift:
            if self.is_avatar:
                bullet_widget and bullet_widget.weapon_data_changed(PART_WEAPON_POS_MAIN3)
                if global_data.is_pc_mode:
                    bullet_widget and bullet_widget.switch_bullet_widget(shape_shift)
                self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN3)
            self.panel.PlayAnimation('show_gun_mode')
        else:
            if self.is_avatar:
                bullet_widget and bullet_widget.weapon_data_changed(PART_WEAPON_POS_MAIN1)
                if global_data.is_pc_mode:
                    bullet_widget and bullet_widget.switch_bullet_widget(shape_shift)
                self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
            self.panel.PlayAnimation('disappear_gun_mode')
        return

    def _start_second_attack(self, *args):
        self.panel.StopAnimation('disappear_sub')
        self.panel.PlayAnimation('show_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)

    def _stop_second_attack(self, *args):
        self.panel.StopAnimation('show_sub')
        self.panel.PlayAnimation('disappear_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def revert_to_defalut_bullet_type(self):
        if not global_data.is_pc_mode:
            return
        mecha_ctrl_main_ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if mecha_ctrl_main_ui and self.is_avatar:
            bullet_widget = mecha_ctrl_main_ui.get_bullet_widget()
            bullet_widget and bullet_widget.switch_bullet_widget(False)

    def on_show_dash_hint(self, flag):
        self.panel.lab_rush_hint.setVisible(flag)