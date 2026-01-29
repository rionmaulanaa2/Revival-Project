# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8004AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.component.client.com_mecha_appearance.ComHeatEnergyClient import MAX_HEAT_STATE
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3
PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_red.png',
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_white.png']

class Mecha8004AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8004'
    MAX_HEAT = 3000
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def init_parameters(self):
        self.last_heat_state = 0
        self.move_type_walk = False
        self.on_rush = False
        self.listen_skill_id = None
        self.panel.btn_test.setVisible(False)
        super(Mecha8004AimUI, self).init_parameters()
        return

    def init_event(self):
        behavior = self.mecha.ev_g_behavior_config()
        self.listen_skill_id = behavior[mecha_status_config.MC_JUMP_1]['custom_param']['skill_id']

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_BEGIN', self.on_show)
            unregist_func('E_ACC_SKILL_END', self.on_hide)
            unregist_func('E_OX_BEGIN_RUSH', self.on_begin_rush)
            unregist_func('E_OX_END_RUSH', self.on_end_rush)
            unregist_func('E_FIRE', self.on_fire)
            unregist_func('E_SET_HEAT', self.on_heat_change)
        self.mecha = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ACC_SKILL_BEGIN', self.on_show)
            regist_func('E_ACC_SKILL_END', self.on_hide)
            regist_func('E_OX_BEGIN_RUSH', self.on_begin_rush)
            regist_func('E_OX_END_RUSH', self.on_end_rush)
            regist_func('E_FIRE', self.on_fire)
            regist_func('E_SET_HEAT', self.on_heat_change)
            self.init_event()
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_heat_change(self, heat, heat_state):
        state_index = 1 if heat_state == MAX_HEAT_STATE else 0
        if self.last_heat_state != heat_state:
            ani_name = [
             'disappear_frenzy', 'show_frenzy']
            self.panel.PlayAnimation(ani_name[state_index])
        self.last_heat_state = heat_state

    def on_fire(self, cd_time, weapon_pos, *args):
        if weapon_pos == PART_WEAPON_POS_MAIN1:
            self.panel.PlayAnimation('aim_spread')

    def on_show(self, *args):
        self.panel.PlayAnimation('show_hotweave')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN3)

    def on_hide(self, *args):
        self.panel.PlayAnimation('dissappear_hotweave')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_begin_rush(self, *args):
        self.on_rush = True

        def cb():
            if self and self.is_valid():
                if self.on_rush:
                    self.panel.lab_rush_hint.setVisible(True)

        self.panel.DelayCall(0.9, cb)

    def on_end_rush(self, *args):
        self.on_rush = False
        self.panel.lab_rush_hint.setVisible(False)