# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8007AimUI.py
from __future__ import absolute_import
from six.moves import range
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON, SUB_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_red.png',
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_white.png']

class Mecha8007AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8007'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN2: SUB_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def init_parameters(self):
        self.is_shooting = False
        self.is_open = False
        self.visible_progress = None
        self.last_val_percent = 100
        self.timer_id = None
        self.default_energy = 0
        self.energy_weapon = None
        self.max_energy = 2
        self.max_level = 5
        self.reloading = False
        self.energy_lv = 0
        super(Mecha8007AimUI, self).init_parameters()
        return

    def init_event(self):
        if not self.mecha:
            return
        weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if weapon:
            self.max_energy = weapon.get_accumulate_max_time()
            self.max_level = 5
            self.energy_weapon = weapon

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_OPEN_AIM_CAMERA', self.on_open_aim_camera)
            regist_func('E_OPEN_AIM_CAMERA_ON_FIRE', self.on_fire)
            regist_func('E_RELOADING', self.on_reloading)
            regist_func('E_WEAPON_BULLET_CHG', self.on_reloaded)
            regist_func('E_OPEN_AIM_RELOADED', self.on_reloaded)
            regist_func('E_SHOW_TELEPORT_FORBID', self.on_show_teleport_forbid)
            regist_func('E_GUN_ATTACK', self.on_gun_attack)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.init_event()
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_OPEN_AIM_CAMERA', self.on_open_aim_camera)
            unregist_func('E_OPEN_AIM_CAMERA_ON_FIRE', self.on_fire)
            unregist_func('E_RELOADING', self.on_reloading)
            unregist_func('E_WEAPON_BULLET_CHG', self.on_reloaded)
            unregist_func('E_OPEN_AIM_RELOADED', self.on_reloaded)
            unregist_func('E_SHOW_TELEPORT_FORBID', self.on_show_teleport_forbid)
            unregist_func('E_GUN_ATTACK', self.on_gun_attack)
        self.mecha = None
        return

    def on_open_aim_camera(self, is_open):
        self.is_open = is_open
        if is_open:
            self.panel.StopAnimation('disappear_sniper')
            self.panel.PlayAnimation('show_sniper')
            self.charge_weapon_energy()
            self.player.send_event('E_CLOSE_MECHA_UI')
        else:
            self.panel.StopAnimation('show_sniper')
            self.panel.PlayAnimation('disappear_sniper')
            self.player.send_event('E_SHOW_MECHA_UI')
            self.panel.nd_sniper.StopTimerAction()
        hide_list = ['FightStateUI', 'FightBagUI', 'StateChangeUI', 'BattleRightTopUI', 'BattleFightCapacity', 'BattleFightMeow']
        for ui_name in hide_list:
            if ui_name != self._panelName:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui:
                    if is_open:
                        ui.add_hide_count(self.__class__.__name__)
                        self._hide_set.add(ui_name)
                    else:
                        ui.add_show_count(self.__class__.__name__)
                        if ui_name in self._hide_set:
                            self._hide_set.remove(ui_name)

        self.panel.nd_sniper.setVisible(is_open)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2 if is_open else PART_WEAPON_POS_MAIN1)

    def charge_weapon_energy(self):
        MIN_PERCENTAGE = 43.5
        MAX_PERCENTAGE = 56.5
        one_bullet_progress = MAX_PERCENTAGE - MIN_PERCENTAGE
        weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if not weapon:
            return
        self.max_energy = weapon.get_accumulate_max_time() or 2.5
        _, self.default_energy = self.mecha.ev_g_auto_energy()
        interval_time = self.max_energy - self.default_energy
        interval = 100 / self.max_level

        def refresh_time(p_time):
            ori_percent = (p_time + self.default_energy) / self.max_energy
            percent = int(ori_percent * 100)
            cur_energy_lv = int(percent / interval)
            for i in range(self.max_level):
                lv = i + 1
                node = getattr(self.panel, 'power%s' % lv)
                if lv > cur_energy_lv:
                    node and node.setVisible(False)
                else:
                    node and node.setVisible(True)

            if cur_energy_lv and cur_energy_lv != self.energy_lv:
                self.panel.PlayAnimation('power%s' % cur_energy_lv)
            self.panel.lab_power.setString(str(percent) + '%')
            self.energy_lv = cur_energy_lv

        def refresh_time_finish():
            self.panel.lab_power.setString('100%')
            self.panel.PlayAnimation('power5')
            self.energy_lv = self.max_level

        if interval_time <= 0:
            refresh_time_finish()
        else:
            refresh_time(0)
        self.panel.nd_sniper.StopTimerAction()
        weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
        if weapon.get_bullet_num() <= 0 or self.reloading:
            return refresh_time(0)
        self.panel.nd_sniper.TimerAction(refresh_time, interval_time, callback=refresh_time_finish)

    def on_fire(self):
        if not self.is_open:
            return
        self.panel.PlayAnimation('sub_fire')
        self.charge_weapon_energy()

    def on_reloaded(self, *args):
        self.reloading = False
        if not self.is_open:
            return
        self.charge_weapon_energy()

    def on_reloading(self, *args):
        self.reloading = True

    def on_show_teleport_forbid(self, show):
        self.panel.lab_forbiden.setVisible(show)
        normal_color = '#SW'
        if self.aim_spread_mgr:
            normal_color = self.aim_spread_mgr.get_aim_normal_color()
        self.panel.aim_right.SetColor('#SR' if show else normal_color)
        self.panel.aim_left.SetColor('#SR' if show else normal_color)
        self.panel.img_aim.SetColor('#SR' if show else normal_color)

    def on_gun_attack(self, socket_name, weapon_pos):
        if weapon_pos == PART_WEAPON_POS_MAIN1 or weapon_pos == PART_WEAPON_POS_MAIN3:
            self.panel.PlayAnimation('shot')