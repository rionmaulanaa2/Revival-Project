# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8013AimUI.py
from __future__ import absolute_import
from six.moves import range
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
MAIN_WEAPONS = {
 PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3}

class Mecha8013AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8013'
    WEAPON_INFO = {}
    PVE_WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON}

    def on_init_panel(self):
        super(Mecha8013AimUI, self).on_init_panel()
        self.show_weapon_energy(0, 0)

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def init_parameters(self):
        self.charge_anims = [
         '1_charge', '2_charge']
        self.circle_anims = ['1_charge_circle', '2_charge_circle']
        self.acc_anim_count = len(self.charge_anims)
        self.weapon_energy = 0
        self.need_reset_anim = False
        self.full_anim_played = False
        self._trigger_levels = [0, 1, 2, 3]
        self._last_touch_energy = 0
        self._last_circle_ani_acts = None
        self._last_charge_ani_acts = None
        super(Mecha8013AimUI, self).init_parameters()
        return

    def init_mecha_event(self, flag):
        mecha = self.mecha
        func = mecha.regist_event if flag else mecha.unregist_event
        func('E_FIRE', self.on_fire)
        func('E_ACCUMULATE_DURATION_CHANGED', self.on_energy_changed)
        func('E_SET_SECOND_WEAPON_ATTACK', self.change_to_second_weapon)
        func('E_TRIGGER_FREE_ACCUMULATE', self.on_trigger_free_accumulate)
        func('E_SHOW_TELEPORT_FORBID', self.on_show_teleport_forbid)
        func('E_FORCE_SHOW_FULL_ENERGY', self.show_force_full_energy)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            self.init_mecha_event(True)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.show_weapon_energy(0, 0)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            pass
        if self.mecha and self.mecha.is_valid():
            self.init_mecha_event(False)
        self.mecha = None
        return

    def change_to_second_weapon(self, flag):
        if flag:
            self.panel.StopAnimation('disappear_sub')
            self.panel.PlayAnimation('show_sub')
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)
        else:
            self.panel.StopAnimation('show_sub')
            self.panel.PlayAnimation('disappear_sub')
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_trigger_free_accumulate(self, weapon_pos, val):
        weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon:
            return
        free_acc_max_time = self.mecha.ev_g_free_accumulate_max_time(weapon_pos)
        if free_acc_max_time <= 0.0:
            self.show_weapon_energy(0, 0)

    def on_fire(self, fire_cd, weapon_pos, fired_socket_index):
        if weapon_pos not in MAIN_WEAPONS:
            return
        self.reset_main_weapon_ui()

    def on_energy_changed(self, weapon_pos, cur_energy, touch_energy):
        if weapon_pos not in MAIN_WEAPONS:
            return
        self.show_weapon_energy(cur_energy, touch_energy, weapon_pos)

    def get_circle_scale(self, weapon_pos):
        if global_data.game_mode.is_pve():
            weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
            is_touch_and_free_acc = False
            acc_level = weapon.get_acc_levels()
            if len(acc_level) >= 2 and acc_level[1] > 0:
                acc_interval_ratio = [
                 acc_level[0] / acc_level[1], 1 - acc_level[0] / acc_level[1]]
            else:
                acc_interval_ratio = [
                 0.5, 0.5]
            acc_max_time = float(weapon.get_accumulate_max_time())
            intervals = [acc_max_time * acc_interval_ratio[0], acc_max_time * acc_interval_ratio[1]]
            if acc_max_time <= 0:
                return
            free_acc_max_time = self.mecha.ev_g_free_accumulate_max_time(weapon_pos)
            free_acc_time_intervals = [free_acc_max_time * acc_interval_ratio[0], free_acc_max_time * acc_interval_ratio[1]]
            if self.mecha.ev_g_is_attack_accumulate(weapon_pos):
                if free_acc_max_time > 0:
                    is_touch_and_free_acc = True
                    for idx in range(2):
                        intervals[idx] -= intervals[idx] / free_acc_max_time * acc_interval_ratio[idx]

                circle_scale = [
                 intervals[0], intervals[1], intervals[1], intervals[1]]
            else:
                circle_scale = [
                 free_acc_time_intervals[0], free_acc_time_intervals[1], 0.6, 0.6]
        else:
            weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
            is_touch_and_free_acc = False
            if self.mecha.ev_g_is_attack_accumulate(weapon_pos):
                interval = weapon.get_accumulate_max_time() / 2.0
                free_acc_max_time = self.mecha.ev_g_free_accumulate_max_time(weapon_pos)
                if free_acc_max_time > 0:
                    is_touch_and_free_acc = True
                    interval -= interval / free_acc_max_time * 0.5
                circle_scale = [
                 interval, interval, interval, interval]
            else:
                free_acc_max_time = self.mecha.ev_g_free_accumulate_max_time(weapon_pos)
                interval = free_acc_max_time / 2.0
                circle_scale = [interval, interval, 0.6, 0.6]
        return (
         circle_scale, is_touch_and_free_acc)

    def reset_main_weapon_ui(self):
        if self.need_reset_anim:
            self.need_reset_anim = False
            for i in range(self.acc_anim_count):
                self.panel.StopAnimation(self.circle_anims[i])
                self.panel.StopAnimation(self.charge_anims[i])

            self.panel.PlayAnimation('aim_recover')
            if self.full_anim_played:
                self.panel.PlayAnimation('reset_full')
                self.full_anim_played = False
            self._trigger_levels = [
             0, 1, 2, 3]
            self._last_circle_ani_acts = None
            self._last_charge_ani_acts = None
        return

    def show_force_full_energy(self, show):
        self.panel.nd_aim.nd_no_spread.setVisible(not show)
        self.panel.nd_aim.nd_force_full.setVisible(show)

    def show_weapon_energy(self, cur_energy, touch_energy, weapon_pos=PART_WEAPON_POS_MAIN1):
        if not self.mecha:
            return
        if self.mecha.ev_g_add_attr('force_full_shoot_cnt'):
            self.show_force_full_energy(True)
        else:
            self.show_force_full_energy(False)
        weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon:
            return
        if cur_energy <= 0:
            self.reset_main_weapon_ui()
            return
        if not self.need_reset_anim:
            self.need_reset_anim = True
        max_time = weapon.get_accumulate_max_time()
        cur_level = weapon.get_accumulate_level(cur_energy)
        last_trigger_level = len(weapon.get_acc_levels())
        if cur_energy >= max_time + 0.5:
            trigger_level = last_trigger_level
        else:
            trigger_level = cur_level
        if trigger_level not in self._trigger_levels:
            if self._last_touch_energy == 0 and touch_energy > 0 and self._last_circle_ani_acts and trigger_level < self.acc_anim_count:
                circle_scale, is_touch_and_free_acc = self.get_circle_scale(weapon_pos)
                max_time = self.GetAnimationMaxRunTime(self.circle_anims[trigger_level])
                if max_time > 0:
                    time_scale = max_time / circle_scale[trigger_level]
                    for act in self._last_circle_ani_acts:
                        if act.isValid():
                            act.setSpeed(time_scale)

                if self._last_charge_ani_acts:
                    max_time = self.GetAnimationMaxRunTime(self.charge_anims[trigger_level])
                    if max_time > 0:
                        time_scale = max_time / circle_scale[trigger_level]
                        for act in self._last_charge_ani_acts:
                            if act.isValid():
                                act.setSpeed(time_scale)

            self._last_touch_energy = touch_energy
            return
        self._last_touch_energy = touch_energy
        circle_scale, is_touch_and_free_acc = self.get_circle_scale(weapon_pos)
        if trigger_level < last_trigger_level and trigger_level < self.acc_anim_count:
            if is_touch_and_free_acc:
                for i in range(0, trigger_level):
                    self.panel.StopAnimation(self.circle_anims[i])

            acts = self.panel.PlayAnimation(self.circle_anims[trigger_level], adjust_to_time=circle_scale[trigger_level])
            self._last_circle_ani_acts = acts
        if self._trigger_levels:
            for i in range(0, trigger_level + 1):
                if i in self._trigger_levels:
                    self._trigger_levels.remove(i)
                    if i < self.acc_anim_count:
                        self._last_charge_ani_acts = self.panel.PlayAnimation(self.charge_anims[i], adjust_to_time=circle_scale[trigger_level])

            if len(self._trigger_levels) == 1:
                self.panel.PlayAnimation('change_to_full')
                self.full_anim_played = True

    def on_show_teleport_forbid(self, show):
        self.panel.lab_forbiden.setVisible(show)