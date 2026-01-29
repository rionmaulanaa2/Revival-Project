# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8003AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, NEOX_UNIT_SCALE
from .MechaBulletWidget import MAIN_WEAPON
from common.cfg import confmgr

class Mecha8003AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8003'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        super(Mecha8003AimUI, self).on_init_panel()
        self.init_auto_aim_widget()
        self.panel.nd_lock.setVisible(False)
        self.panel.nd_lock_fail.setVisible(False)

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def auto_aim_appearance_update_callback(self, target_pos):
        if not self.player:
            return
        if self.cur_navigate_max_distance <= 0:
            self.panel.nd_lock_fail.setVisible(False)
            return
        my_pos = self.player.ev_g_position()
        distance = (target_pos - my_pos).length
        in_range = distance <= self.cur_navigate_max_distance
        self.panel.nd_lock.setVisible(in_range)
        self.panel.nd_lock_fail.setVisible(not in_range)
        distance_text = get_text_by_id(18140, {'distance': int(distance / NEOX_UNIT_SCALE)})
        self.panel.nd_lock.lab_lock_distant.SetString(distance_text)
        self.panel.nd_lock_fail.lab_lock_distant.SetString(distance_text)

    def init_auto_aim_widget(self):
        from .MechaAutoAimWidget import MechaAutoAimWidget
        self.auto_aim_widget = MechaAutoAimWidget(self.panel, target_refreshed_anim_map={'default': 'active_auto'
           }, miss_target_anim='inactive_auto', need_play_lock_sound_map={PART_WEAPON_POS_MAIN2: True
           }, lock_node_map={PART_WEAPON_POS_MAIN1: (
                                 self.panel.nd_lock, self.panel.nd_lock_fail),
           PART_WEAPON_POS_MAIN2: self.panel.nd_lock
           }, reset_node_map={'default': self.panel.nd_sub_no_spread
           }, lock_node_parent_map={'default': self.panel.nd_sub_aim
           }, update_callback=self.auto_aim_appearance_update_callback)

    def on_finalize_panel(self):
        super(Mecha8003AimUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def init_parameters(self):
        self.is_auto_aim = False
        self.main_navigate_max_distance = 0
        self.second_navigate_max_distance = 0
        self.cur_navigate_max_distance = 0
        self.need_play_fire_lock_anim = False
        super(Mecha8003AimUI, self).init_parameters()

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_WEAPON_CHANGED', self.on_weapon_changed)
            unregist_func('E_ACC_SKILL_BEGIN', self.on_second_weapon_begin)
            unregist_func('E_ACC_SKILL_END', self.on_second_weapon_end)
            unregist_func('E_ON_MISSILE_LOCK_TARGET_CHANGE', self.on_missile_lock_target_change)
            unregist_func('E_FIRE', self._on_fire)
        self.mecha = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_erent(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_WEAPON_CHANGED', self.on_weapon_changed)
            regist_func('E_ACC_SKILL_BEGIN', self.on_second_weapon_begin)
            regist_func('E_ACC_SKILL_END', self.on_second_weapon_end)
            regist_func('E_ON_MISSILE_LOCK_TARGET_CHANGE', self.on_missile_lock_target_change)
            regist_func('E_FIRE', self._on_fire)
            main_weapon = mecha.share_data.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN1)
            wp_id = main_weapon.get_item_id()
            self.main_navigate_max_distance = confmgr.get('navigate_config', str(wp_id), 'fNavMaxDistance', default=0) * NEOX_UNIT_SCALE
            self.on_weapon_changed(PART_WEAPON_POS_MAIN2)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)
            lock_target_id = self.mecha.ev_g_get_missile_lock_target()
            if lock_target_id:
                self.on_missile_lock_target_change(lock_target_id)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_weapon_changed(self, weapon_pos):
        if not self.mecha:
            return
        if weapon_pos == PART_WEAPON_POS_MAIN2:
            second_weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN2)
            wp_id = second_weapon.get_item_id()
            self.second_navigate_max_distance = confmgr.get('navigate_config', str(wp_id), 'fNavMaxDistance', default=0) * NEOX_UNIT_SCALE
            if hasattr(second_weapon, 'get_is_navigate_enabled') and second_weapon.get_is_navigate_enabled():
                self.is_auto_aim = True
                return
            self.is_auto_aim = False
            self.mecha.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, PART_WEAPON_POS_MAIN2)
            self.panel.nd_auto_frame.setVisible(False)

    def on_second_weapon_begin(self, *args):
        self.panel.StopAnimation('disappear_javelin')
        self.panel.PlayAnimation('show_javalin')
        if self.is_auto_aim:
            self.mecha.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, PART_WEAPON_POS_MAIN2)
            self.panel.PlayAnimation('show_auto')
            self.auto_aim_widget.refresh_auto_aim_parameters(PART_WEAPON_POS_MAIN2)
            self.cur_navigate_max_distance = self.second_navigate_max_distance
            self.panel.nd_lock_fail.setVisible(False)
            self.panel.nd_lock.lab_lock_distant.SetString('')
            self.panel.nd_lock_fail.lab_lock_distant.SetString('')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)

    def on_second_weapon_end(self, *args):
        self.panel.StopAnimation('show_javalin')
        self.panel.PlayAnimation('disappear_javelin')
        if self.is_auto_aim:
            self.mecha.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, PART_WEAPON_POS_MAIN2)
            self.panel.PlayAnimation('disappear_auto')
            self.auto_aim_widget.update_aim_target(None, PART_WEAPON_POS_MAIN2)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
        return

    def on_missile_lock_target_change(self, target_id):
        target = None
        if target_id:
            from mobile.common.EntityManager import EntityManager
            target = EntityManager.getentity(target_id)
            if target and target.logic:
                target = target.logic
        if target:
            self.cur_navigate_max_distance = self.main_navigate_max_distance
            self.auto_aim_widget.refresh_auto_aim_parameters(PART_WEAPON_POS_MAIN1)
            self.panel.StopAnimation('disappear_javelin')
        self.need_play_fire_lock_anim = bool(target)
        self.auto_aim_widget.update_aim_target(target, PART_WEAPON_POS_MAIN1)
        return

    def _on_fire(self, cd_time, weapon_pos, *args):
        if self.need_play_fire_lock_anim:
            self.panel.PlayAnimation('active_lock')