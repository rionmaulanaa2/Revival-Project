# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8019AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON, MechaBulletWidget
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3
from logic.gcommon.time_utility import time

class Mecha8019AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8019'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }
    PRO_PIC = ('gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_white.png',
               'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_white.png')
    EC_COLOR = ('#SW', '#DB')
    EC_MIN = 40
    EC_MAX = 60
    SC_MIN = 12
    SC_MAX = 38

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def init_bullet_widget(self):
        self.bullet_widget = None
        if global_data.is_pc_mode:
            self.panel.nd_bullet_ob.setVisible(False)
            self.panel.nd_bullet_ob.nd_bullet.setVisible(False)
            self.panel.nd_bullet_ob.nd_bullet.temp_bullet.setVisible(False)
            return
        else:
            self.bullet_widget = MechaBulletWidget(self.panel, self.WEAPON_INFO)
            return

    def on_finalize_panel(self):
        super(Mecha8019AimUI, self).on_finalize_panel()
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.panel.nd_power.progress_power.SetColor('#DQ')
            self.timer_id = None
        return

    def init_parameters(self):
        self.on_rush = False
        self.full_tag = False
        self.hp_tag = False
        self.timer_id = None
        self.last_time = time()
        super(Mecha8019AimUI, self).init_parameters()
        return

    def do_show_panel--- This code section failed: ---

  62       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'nd_aim'
           9  LOAD_ATTR             2  'setVisible'
          12  LOAD_GLOBAL           3  'True'
          15  CALL_FUNCTION_1       1 
          18  POP_TOP          

  63      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             0  'panel'
          25  LOAD_ATTR             4  'nd_bullet_ob'
          28  LOAD_ATTR             2  'setVisible'
          31  LOAD_GLOBAL           3  'True'
          34  CALL_FUNCTION_1       1 
          37  POP_TOP          

  64      38  LOAD_GLOBAL           5  'global_data'
          41  LOAD_ATTR             6  'is_pc_mode'
          44  POP_JUMP_IF_TRUE     69  'to 69'

  65      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             0  'panel'
          53  LOAD_ATTR             4  'nd_bullet_ob'
          56  LOAD_ATTR             2  'setVisible'
          59  LOAD_GLOBAL           3  'True'
          62  CALL_FUNCTION_1       1 
          65  POP_TOP          
          66  JUMP_FORWARD          0  'to 69'
        69_0  COME_FROM                '66'

  66      69  LOAD_GLOBAL           7  'getattr'
          72  LOAD_GLOBAL           1  'nd_aim'
          75  LOAD_CONST            0  ''
          78  CALL_FUNCTION_3       3 
          81  STORE_FAST            1  'aim_spread_mgr'

  67      84  LOAD_FAST             1  'aim_spread_mgr'
          87  JUMP_IF_FALSE_OR_POP    99  'to 99'
          90  LOAD_FAST             1  'aim_spread_mgr'
          93  LOAD_ATTR             9  '_on_spread'
          96  CALL_FUNCTION_0       0 
        99_0  COME_FROM                '87'
          99  POP_TOP          
         100  LOAD_CONST            0  ''
         103  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 78

    def do_hide_panel(self):
        self.panel.nd_aim.setVisible(False)
        self.panel.nd_bullet_ob.setVisible(False)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_BEGIN', self.on_show)
            unregist_func('E_ACC_SKILL_END', self.on_hide)
            unregist_func('E_OX_BEGIN_RUSH', self.on_begin_rush)
            unregist_func('E_OX_END_RUSH', self.on_end_rush)
            unregist_func('E_EC_8019', self.on_energy_change)
            unregist_func('E_EC_8019_S', self.on_energy_change_s)
            unregist_func('E_ENTER_DEFEND', self.on_enter_defend)
            unregist_func('E_EXIT_DEFEND', self.on_exit_defend)
            unregist_func('E_SC_8019', self.on_s_hp_change)
            unregist_func('E_SC_8019_S', self.on_s_hp_change_s)
            unregist_func('E_SC_8019_FULL', self.on_s_hp_change_end)
            unregist_func('E_SHOW_SHIELD_HP_8019', self.on_show_shield_hp)
            unregist_func('E_8019_SWITCH_WEAPON', self.on_switch_weapon)
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
            regist_func('E_EC_8019', self.on_energy_change)
            regist_func('E_EC_8019_S', self.on_energy_change_s)
            regist_func('E_ENTER_DEFEND', self.on_enter_defend)
            regist_func('E_EXIT_DEFEND', self.on_exit_defend)
            regist_func('E_SC_8019', self.on_s_hp_change)
            regist_func('E_SC_8019_S', self.on_s_hp_change_s)
            regist_func('E_SC_8019_FULL', self.on_s_hp_change_end)
            regist_func('E_SHOW_SHIELD_HP_8019', self.on_show_shield_hp)
            regist_func('E_8019_SWITCH_WEAPON', self.on_switch_weapon)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
        state = self.mecha.ev_g_handy_shield_state()
        cur_hp, max_hp, tag = self.mecha.ev_g_handy_shield_hp()
        if state:
            self.on_enter_defend()
            self.on_s_hp_change(cur_hp, max_hp, tag)
        elif abs(cur_hp - max_hp) < 1:
            self.on_exit_defend()
        else:
            self.on_enter_defend()
            self.on_s_hp_change(cur_hp, max_hp, tag)

    def on_show(self, *args):
        self.panel.PlayAnimation('show_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN3)

    def on_hide(self, *args):
        self.panel.PlayAnimation('disappear_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_enter_observe(self, is_observe):
        if is_observe:
            self.panel.nd_bullet_ob.setVisible(False)
            self.panel.nd_bullet_ob.nd_bullet.setVisible(False)
            self.panel.nd_bullet_ob.nd_bullet.temp_bullet.setVisible(False)
        else:
            self.panel.nd_bullet_ob.setVisible(not global_data.is_pc_mode)
            self.panel.nd_bullet_ob.nd_bullet.setVisible(not global_data.is_pc_mode)
            self.panel.nd_bullet_ob.nd_bullet.temp_bullet.setVisible(not global_data.is_pc_mode)

    def on_begin_rush(self, *args):
        self.on_rush = True

        def cb():
            if self and self.is_valid():
                if self.on_rush:
                    self.panel.lab_rush_hint.setVisible(True)

        self.panel.DelayCall(0.5, cb)

    def on_end_rush(self, *args):
        self.on_rush = False
        self.panel.lab_rush_hint.setVisible(False)

    def on_energy_change(self, per):
        percent = self.EC_MIN + (self.EC_MAX - self.EC_MIN) * per
        self.panel.nd_power.progress_power.SetPercentage(percent)
        if per * 100 >= 99 and not self.full_tag:
            self.panel.PlayAnimation('full_power')
            self.full_tag = True
        if per * 100 <= 1:
            self.full_tag = False

    def on_energy_change_s(self, energy):
        pass

    def on_enter_defend(self):
        self.panel.PlayAnimation('show_shield')
        self.panel.PlayAnimation('show_shield_hp')

    def on_exit_defend(self):
        self.panel.PlayAnimation('disappear_shield')

    def on_s_hp_change(self, cur_hp, max_hp, tag):
        per = cur_hp * 1.0 / max_hp
        percent = self.SC_MIN + (self.SC_MAX - self.SC_MIN) * per
        self.panel.nd_shield.nd_sub_left.prog_sub_left.SetPercentage(percent)
        pic = self.PRO_PIC[1] if tag else self.PRO_PIC[0]
        self.panel.nd_shield.nd_sub_left.prog_sub_left.SetProgressTexture(pic)
        self.panel.nd_shield.lab_value.SetString(str(int(cur_hp)) + '/' + str(int(max_hp)))

    def on_s_hp_change_s(self, cur_hp, max_hp, tag):
        self.on_s_hp_change(cur_hp, max_hp, tag)

    def on_s_hp_change_end(self):
        self.panel.PlayAnimation('disappear_shield_hp')

    def on_show_shield_hp(self):
        self.panel.PlayAnimation('show_shield_hp')

    def on_switch_weapon(self, weapon_pos):
        if not self.aim_spread_mgr:
            return
        self.aim_spread_mgr.set_weapon_pos(weapon_pos)