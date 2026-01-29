# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8026AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3
from common.cfg import confmgr
from logic.gcommon.time_utility import get_server_time
SHIELD_PROG_AREA = (62, 88, 26)

class Mecha8026AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8026'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        super(Mecha8026AimUI, self).on_init_panel()

    def init_parameters(self):
        super(Mecha8026AimUI, self).init_parameters()
        self.shield_max_time = None
        self.shield_on = False
        gun_data = confmgr.get('c_gun_data', '802603', 'cCustomParam', default={})
        self.shield_dmg_max = gun_data.get('max_base_power', 1000)
        self.shield_dmg_min = gun_data.get('min_base_power', 100)
        self.shield_timer_id = None
        self.shield_open_ts = None
        self.power_up = False
        self.show_power_prog = False
        return

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr2
        self.aim_spread_mgr = MechaAimSpreadMgr2(self.panel)

    def on_finalize_panel(self):
        super(Mecha8026AimUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_WEAPON_POWERUP', self.on_weapon_powerup)
            regist_func('E_8026_SHIELD_CHANGE', self.on_shield_state_change)
            regist_func('E_8026_SHIELD_AIM', self.on_show_shield_aim)
            regist_func('E_SHILED_ABSORBED_DAMAGE', self.on_shield_hitted)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.is_avatar = mecha.ev_g_is_avatar()
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_WEAPON_POWERUP', self.on_weapon_powerup)
            unregist_func('E_8026_SHIELD_CHANGE', self.on_shield_state_change)
            unregist_func('E_8026_SHIELD_AIM', self.on_show_shield_aim)
            unregist_func('E_SHILED_ABSORBED_DAMAGE', self.on_shield_hitted)
        self.mecha = None
        return

    def on_weapon_powerup(self, percent):
        if self.is_avatar:
            show_progress = 0 < percent < 1
            if show_progress ^ self.show_power_prog:
                self.panel.StopAnimation('spread_fire_show')
                self.panel.StopAnimation('spread_fire_disappear')
                self.show_power_prog = show_progress
                self.panel.PlayAnimation('spread_fire_show' if self.show_power_prog else 'spread_fire_disappear')
        power_up = percent >= 1.0
        if power_up != self.power_up:
            self.panel.nd_spread_2.setVisible(power_up)
            self.power_up = power_up
            icon = 'gui/ui_res_2/battle/mech_main/icon_mech8026_2.png' if power_up else 'gui/ui_res_2/battle/mech_main/icon_mech8026_1.png'
            self.mecha.send_event('E_SET_ACTION_ICON', 'action1', icon)
            self.mecha.send_event('E_SET_ACTION_ICON', 'action2', icon)
            self.mecha.send_event('E_SET_ACTION_ICON', 'action3', icon)
        percent = percent * 22.0 + 52.0
        self.panel.progress_charge.SetPercent(percent)

    def on_shield_state_change(self, shield_on):
        if not self.is_avatar:
            return
        else:
            from common.utils.timer import CLOCK
            shield_on = bool(shield_on)
            if shield_on != self.shield_on:
                self.PlayAnimation('show_sub' if shield_on else 'disappear_sub')
                self.PlayAnimation('show_power' if shield_on else 'disappear_power')
                self.shield_on = shield_on
                self.panel.prog_sub_left.SetPercent(SHIELD_PROG_AREA[1])
                self.panel.lab_power.SetString('0%')
                self.panel.prog_power.SetPercent(0)
                if self.shield_timer_id is None and shield_on:
                    self.shield_open_ts = get_server_time()
                    self.shield_timer_id = global_data.game_mgr.register_logic_timer(self.shield_tick, interval=0.1, times=-1, mode=CLOCK)
                    self.shield_max_time = self.mecha.ev_g_shield_max_time()
                else:
                    global_data.game_mgr.unregister_logic_timer(self.shield_timer_id)
                    self.shield_timer_id = None
            return

    def on_show_shield_aim(self, flag):
        flag = bool(flag)
        if flag:
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN3)
        else:
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
        if self.panel.nd_aim.isVisible() == flag:
            self.PlayAnimation('show_sec' if flag else 'disappear_sec')
            self.panel.nd_aim.setVisible(not flag)
            self.aim_spread_mgr._on_spread()

    def on_shield_hitted(self, absorbed_dmg):
        if absorbed_dmg <= self.shield_dmg_min:
            percent = 0
        elif absorbed_dmg >= self.shield_dmg_max:
            percent = 100
        else:
            percent = (absorbed_dmg - self.shield_dmg_min) / (self.shield_dmg_max - self.shield_dmg_min) * 100
        self.panel.prog_power.SetPercent(percent)
        self.panel.lab_power.SetString('{}%'.format(int(percent)))

    def shield_tick(self):
        cur_shield_time = get_server_time() - self.shield_open_ts
        percent = 1.0 - cur_shield_time / self.shield_max_time
        percent = SHIELD_PROG_AREA[2] * percent + SHIELD_PROG_AREA[0]
        self.panel.prog_sub_left.SetPercent(percent)

    def on_finalize(self):
        super(Mecha8026AimUI, self).on_finalize()
        global_data.game_mgr.unregister_logic_timer(self.shield_timer_id)
        self.shield_timer_id = None
        return