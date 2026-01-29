# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8030AimUI.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from common.utils.timer import CLOCK
from logic.gcommon.time_utility import get_server_time
from common.utilities import clamp
from logic.gcommon.common_const.mecha_const import MODULE_ATTACK_SLOT
from logic.gcommon.component.client.ComMechaAimHelper import AIM_TARGET_TOO_FAR, AIM_TARGET_VALID
from logic.gcommon.common_const.buff_const import BUFF_ID_8030_AIM_SELF
ATTACK_CARD_2_ID = 803012

class Mecha8030AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8030'
    GLOBAL_EVENT = {'battle_add_mecha_buff': 'on_add_buff'
       }
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('show_bullet')
        self.events = {'E_ENABLE_WEAPON_AIM_HELPER': self.enable_main_weapon_aim,
           'E_SHOW_JUMP_CHARGE': self.show_jump_charge,
           'E_NOTIFY_MODULE_CHANGED': self.on_module_changed,
           'E_SHOW_SEC_AIM': self.show_sec_aim,
           'E_SHOW_CHARGE_FAIL': self.show_charge_fail_anim
           }
        super(Mecha8030AimUI, self).on_init_panel()
        self.init_auto_aim_widget()
        self.on_module_changed()

    def init_parameters(self):
        super(Mecha8030AimUI, self).init_parameters()
        self.main_weapon_aim_helper_enabled = False
        self.prog_jump_charge_showed = False
        self.jump_charge_start_ts = None
        self.max_jump_charge = 0
        self.jump_charge_timer = None
        self.show_sp_lock = False
        self.sec_aim_showed = False
        self.aim_timer = None
        self.aim_remain_time = 0.0
        self.aim_duration = 0.0
        self.panel.RecordAnimationNodeState('prog_flicker')
        return

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, spread_type=MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def init_auto_aim_widget(self):
        from .MechaAutoAimWidget8030 import MechaAutoAimWidget8030
        self.auto_aim_widget = MechaAutoAimWidget8030(self.panel, lock_node_map={PART_WEAPON_POS_MAIN1: (self.panel.nd_lock, self.panel.nd_lock_fail, self.panel.nd_aim_sp)}, update_callback=self.auto_aim_appearance_update_callback)

    def disappear(self):
        self.panel.PlayAnimation('disappear_bullet')
        super(Mecha8030AimUI, self).disappear()

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            for event, func in six.iteritems(self.events):
                regist_func(event, func)

            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)
            main_weapon = mecha.share_data.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN1)
            weapon_conf = main_weapon.get_config()
            self.main_navigate_max_distance = weapon_conf.get('fAutoAimDistance', 0.0) * NEOX_UNIT_SCALE

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            for event, func in six.iteritems(self.events):
                unregist_func(event, func)

        self.mecha = None
        return

    def show_aim_ui(self, show):
        if not self.panel:
            return
        self.panel.nd_aim and self.panel.nd_aim.setVisible(show)
        self.panel.auto and self.panel.auto.setVisible(show and self.auto_aim_widget.panel_showed)

    def add_show_count(self, key='_default', count=1, is_check=True):
        if key == 'BulletReloadProgressUI':
            self.show_aim_ui(True)
        else:
            super(Mecha8030AimUI, self).add_show_count(key, count, is_check)

    def add_hide_count(self, key='_default', count=1, no_same_key=True, is_check=True):
        if key == 'BulletReloadProgressUI':
            self.show_aim_ui(False)
        else:
            super(Mecha8030AimUI, self).add_hide_count(key, count, no_same_key, is_check)

    def enable_main_weapon_aim(self, enabled, weapon_pos, **kwargs):
        if enabled == self.main_weapon_aim_helper_enabled:
            return
        else:
            self.main_weapon_aim_helper_enabled = enabled
            if enabled and self.auto_aim_widget.refresh_auto_aim_range_appearance(weapon_pos):
                self.auto_aim_widget.show()
                self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
                self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_target, weapon_pos)
            else:
                self.auto_aim_widget.hide()
                self.auto_aim_widget.update_aim_target(None, weapon_pos)
            return

    def show_jump_charge(self, show, start_ts=None, max_charge=None):
        if show:
            self.show_charge_fail_anim(False)
            self.jump_charge_start_ts = start_ts
            self.max_jump_charge = max_charge
            if not self.jump_charge_timer:
                self.jump_charge_timer = global_data.game_mgr.register_logic_timer(self.update_jump_charge, interval=0.1, times=-1, mode=CLOCK)
            self.update_jump_charge()
        else:
            self.destroy_jump_charge_timer()
        if show ^ self.prog_jump_charge_showed:
            self.panel.PlayAnimation('show_sp2' if show else 'disappear_sp2')
            self.prog_jump_charge_showed = show

    def update_jump_charge(self, *args):
        if not self.prog_jump_charge_showed:
            return
        charge_time = clamp(get_server_time() - self.jump_charge_start_ts, 0, self.max_jump_charge)
        percent = 100.0 * charge_time / self.max_jump_charge
        self.panel.prog_jump_charge.SetPercent(percent)

    def destroy_jump_charge_timer(self):
        if self.jump_charge_timer:
            global_data.game_mgr.unregister_logic_timer(self.jump_charge_timer)
            self.jump_charge_timer = None
        return

    def on_finalize_panel(self):
        super(Mecha8030AimUI, self).on_finalize_panel()
        self.destroy_jump_charge_timer()
        self.destroy_aim_timer()
        self.destroy_widget('auto_aim_widget')

    def on_module_changed(self):
        if not self.player:
            return
        show_sp_lock = False
        module_info = self.player.ev_g_mecha_installed_module(MODULE_ATTACK_SLOT)
        if module_info:
            show_sp_lock = module_info[0] == ATTACK_CARD_2_ID
        if self.show_sp_lock ^ show_sp_lock:
            self.show_sp_lock = show_sp_lock
            self.panel.nd_aim_sp.setVisible(self.auto_aim_widget.panel_showed and show_sp_lock)

    def show_sec_aim(self, show):
        if show:
            self.panel.nd_sub_aim.setVisible(True)
            self.panel.nd_aim.setVisible(False)
            self.aim_spread_mgr._on_spread()
        if show ^ self.sec_aim_showed:
            self.sec_aim_showed = show
            self.panel.StopAnimation('missile_using')
            self.panel.StopAnimation('missile_disappear')
            self.panel.PlayAnimation('missile_using' if show else 'missile_disappear')

    def auto_aim_appearance_update_callback(self, target_pos, valid):
        if not self.player:
            return
        my_pos = self.player.ev_g_position()
        distance = (target_pos - my_pos).length
        is_valid = valid == AIM_TARGET_VALID
        self.panel.nd_lock.setVisible(is_valid)
        self.panel.nd_lock_fail.setVisible(not is_valid)
        distance_text = get_text_by_id(18140, {'distance': int(distance / NEOX_UNIT_SCALE)})
        show_distant = valid == AIM_TARGET_TOO_FAR
        self.panel.nd_lock.lab_lock_distant.setVisible(show_distant)
        self.panel.nd_lock_fail.lab_lock_distant.setVisible(show_distant)
        if show_distant:
            self.panel.nd_lock.lab_lock_distant.SetString(distance_text)
            self.panel.nd_lock_fail.lab_lock_distant.SetString(distance_text)
        self.panel.nd_aim_sp.setVisible(self.show_sp_lock)

    def on_add_buff(self, buff_id, left_time, add_time, duration, data):
        if buff_id != BUFF_ID_8030_AIM_SELF:
            return
        if duration > 0 and left_time > 0:
            self.aim_remain_time = left_time
            self.aim_duration = duration
            if not self.aim_timer:
                self.aim_timer = global_data.game_mgr.register_logic_timer(self.update_aim_time, interval=0.05, times=-1, mode=CLOCK, timedelta=True)
                self.update_aim_time(0.0)

    def update_aim_time(self, dt):
        self.aim_remain_time -= dt
        if self.aim_remain_time <= 0.0:
            self.aim_remain_time = 0.0
            self.destroy_aim_timer()
        prog = int(self.aim_remain_time * 100.0 / self.aim_duration)
        self.panel.center.bar_prog.prog_aim.SetPercentage(prog)

    def destroy_aim_timer(self):
        if self.aim_timer:
            global_data.game_mgr.unregister_logic_timer(self.aim_timer)
            self.aim_timer = None
        return

    def show_charge_fail_anim(self, show):
        self.panel.nd_jump_charge.SetOpacity(255)
        self.panel.nd_jump_charge.setVisible(show)
        self.panel.prog_jump_charge.setVisible(not show)
        self.panel.prog_jump_charge_2.setVisible(show)
        if show:
            self.panel.bar_progress.SetOpacity(255)
            self.panel.prog_jump_charge_2.SetOpacity(255)
            self.panel.PlayAnimation('prog_flicker')
        else:
            self.panel.StopAnimation('prog_flicker')