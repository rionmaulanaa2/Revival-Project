# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWeaponController.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.const import ATK_FIST, ATK_GUN, ATK_MELEE
from logic.gcommon.const import PART_WEAPON_POS_NONE, PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from logic.gcommon.common_const.weapon_const import WP_GRENADES_GUN, WP_SUMMON_GRENADES_GUN
from ...cdata import status_config as st_const
from common.utils import timer
import time

class ComWeaponController(UnitCom):
    BIND_EVENT = {'E_TRY_SWITCH': '_try_switch',
       'E_LEAVE_STATE': '_end_switch',
       'E_SWITCH_WEAPON_COMPONENT': '_on_switch_weapon_component',
       'E_SWITCH_WEAPON_MODE': '_try_switch_weapon_mode',
       'E_SWITCHING_WP_MODE': '_do_switch_wp_mode'
       }
    COMPONENT_MAP = {ATK_FIST: ('ComAtkHand', ),
       ATK_GUN: ('ComAtkGun', ),
       ATK_MELEE: ('ComAtkMelee', )
       }
    TRACK_WEAPON_COMPONENT_NAME = 'ComAtkThrowTrackGun'
    USE_TRACK_WEAPON_TYPES = {WP_GRENADES_GUN, WP_SUMMON_GRENADES_GUN}

    def __init__(self):
        super(ComWeaponController, self).__init__(False)
        self.last_weapon_entity_id = None
        self.weapon = None
        self.keep_reload = False
        self.keep_time = 0
        self.delay_timer_id = None
        return

    def reset(self):
        self.unload_weapon_component()
        self.load_weapon_component(None, True)
        return

    def _try_switch(self, weapon_pos, switch_status=True, is_init=False):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if weapon and not weapon.check_can_equip():
            if self.unit_obj.__class__.__name__ == 'LAvatar':
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(609340))
            return
        if switch_status:
            if not (self.ev_g_is_parachute_battle_land() or self.ev_g_is_parachute_ready_battle()):
                if weapon_pos:
                    self.send_event('E_CALL_SYNC_METHOD', 'on_wpbar_switch', (weapon_pos,), True, True, True)
                return
            if not self.ev_g_status_try_trans(st_const.ST_SWITCH):
                return
        if not weapon and weapon_pos != PART_WEAPON_POS_NONE:
            weapon_pos = PART_WEAPON_POS_NONE
        if is_init:
            self.switch_component(weapon, True)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'on_wpbar_switch', (weapon_pos,), True, True, True)

    def _try_switch_weapon_mode(self):
        if not (self.ev_g_is_parachute_battle_land() or self.ev_g_is_parachute_ready_battle()):
            return
        if not self.weapon or not self.weapon.is_multi_wp():
            return
        if not self.unit_obj or not self.unit_obj.is_valid():
            return
        if not self.ev_g_status_try_trans(st_const.ST_SWITCH_WP_MODE):
            if self.ev_g_get_state(st_const.ST_SWIM):
                txt = get_text_by_id(19055)
                global_data.emgr.battle_show_message_event.emit(txt)
            return
        enable = False if self.weapon.is_in_multi_mode() else True
        self.send_event('E_CALL_SYNC_METHOD', 'try_switch_wp_mode', (self.weapon.get_pos(), enable), True, True, True)

    def _do_switch_wp_mode(self, pos, enable):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(pos)
        if not self.unit_obj or not self.unit_obj.is_valid():
            return
        if not weapon or not weapon == self.weapon:
            return
        self.unload_weapon_component(reset_wp=False)
        if self.weapon.switch_wp_mode(enable):
            self.send_event('E_SWITCHED_WP_MODE', pos)
            self.load_weapon_component(self.weapon, is_init=False, is_switch_mode=True)

    def _on_switch_weapon_component(self, weapon_pos):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon and weapon_pos != PART_WEAPON_POS_NONE:
            weapon_pos = PART_WEAPON_POS_NONE
        self.switch_component(weapon, False)

    def switch_component(self, weapon, is_init, is_switch_mode=False):
        if self.unit_obj:
            self.unload_weapon_component()
            self.load_weapon_component(weapon, is_init, is_switch_mode)

    def get_weapon_comonent(self, weapon):
        if weapon:
            if weapon.iAtkMode != ATK_GUN:
                component_names = list(self.COMPONENT_MAP[weapon.iAtkMode])
            else:
                kind = weapon.get_kind()
                if kind in self.USE_TRACK_WEAPON_TYPES and weapon.conf('cCustomParam', {}).get('use_track', True):
                    component_names = [
                     self.TRACK_WEAPON_COMPONENT_NAME]
                else:
                    component_names = list(self.COMPONENT_MAP[weapon.iAtkMode])
            conf = weapon.get_config()
            extra_coms = conf.get('arrComponent', [])
            component_names.extend(extra_coms)
        else:
            component_names = list(self.COMPONENT_MAP[ATK_FIST])
        return component_names

    def unload_weapon_component(self, reset_wp=True):
        component_names = self.get_weapon_comonent(self.weapon)
        component_names.reverse()
        for com_name in component_names:
            self.unit_obj.del_com(com_name)

        if reset_wp:
            self.weapon = None
        return

    def load_weapon_component(self, weapon, is_init=False, is_switch_mode=False):
        if not is_switch_mode and self.weapon and self.weapon == weapon:
            log_error('weapon %s load duplicate', self.weapon)
            return
        component_names = self.get_weapon_comonent(weapon)
        if weapon:
            conf = weapon.get_config()
        else:
            conf = {}
        self.weapon = weapon
        for com_name in component_names:
            com_weapon = self.unit_obj.add_com(com_name, 'client')
            com_weapon.init_from_dict(self.unit_obj, conf)
            if hasattr(com_weapon, 'install_weapon'):
                com_weapon.install_weapon(weapon, is_init, is_switch_mode=is_switch_mode)

        for com_name in component_names:
            com_weapon = self.unit_obj.get_com(com_name)
            if com_weapon:
                com_weapon.on_init_complete()

    def _end_switch(self, leave_state, new_state=None):
        if leave_state == st_const.ST_RELOAD and self.weapon:
            self.keep_reload = not self.weapon.dirty
            self.keep_time = time.time() + 1
            self.last_weapon_entity_id = self.weapon.get_entity_id()
        if leave_state not in [st_const.ST_SWITCH, st_const.ST_PARACHUTE, st_const.ST_USE_ITEM, st_const.ST_PICK]:
            return
        self.clear_reload_timer()
        self.delay_timer_id = global_data.game_mgr.register_logic_timer(self.try_reload, interval=0.3, times=1, mode=timer.CLOCK)

    def clear_reload_timer(self):
        if self.delay_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.delay_timer_id)
        self.delay_timer_id = None
        return

    def try_reload(self):
        if not (self and self.is_valid()):
            return
        is_puppet = self.unit_obj.__class__.__name__ == 'LPuppet'
        if self.weapon and self.weapon.__class__.__name__ == 'WpGunClient' and not is_puppet:
            if self.weapon.get_bullet_num() <= 0 or self.weapon.get_entity_id() == self.last_weapon_entity_id and self.keep_reload and time.time() < self.keep_time:
                self.send_event('E_TRY_RELOAD')

    def destroy(self):
        self.unload_weapon_component()
        self.clear_reload_timer()
        super(ComWeaponController, self).destroy()