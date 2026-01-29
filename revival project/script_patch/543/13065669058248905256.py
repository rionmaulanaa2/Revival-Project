# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8015AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from mobile.common.EntityManager import EntityManager
from common.utils.timer import CLOCK

class Mecha8015AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8015'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SCALE)

    def init_parameters(self):
        self._target = None
        self.enhance_weapon_timer_id = None
        super(Mecha8015AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ACC_SKILL_BEGIN', self.on_second_weapon_begin)
            regist_func('E_ACC_SKILL_END', self.on_second_weapon_end)
            regist_func('E_MECHA_AIM_TARGET', self._aim_target)
            regist_func('E_SET_WEAPON_AIM_HELPER_SCALE', self.refresh_second_weapon_aim_scale, 99)
            regist_func('E_CHANGE_ENHANCE_WEAPON_FIRE_8015', self._on_change_enhance_weapon_fire)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.refresh_second_weapon_aim_scale()
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_BEGIN', self.on_second_weapon_begin)
            unregist_func('E_ACC_SKILL_END', self.on_second_weapon_end)
            unregist_func('E_MECHA_AIM_TARGET', self._aim_target)
            unregist_func('E_SET_WEAPON_AIM_HELPER_SCALE', self.refresh_second_weapon_aim_scale)
            unregist_func('E_CHANGE_ENHANCE_WEAPON_FIRE_8015', self._on_change_enhance_weapon_fire)
        self.mecha = None
        return

    def on_second_weapon_begin(self, *args):
        self.panel.StopAnimation('disappear_sub')
        self.panel.PlayAnimation('show_sub')
        self.mecha.send_event('E_ENABLE_HIT_BY_RAY_IN_ADVANCE', True, PART_WEAPON_POS_MAIN2)
        self.mecha.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, PART_WEAPON_POS_MAIN2)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)

    def on_second_weapon_end(self, *args):
        self.panel.StopAnimation('show_sub')
        self.panel.PlayAnimation('disappear_sub')
        self.mecha.send_event('E_ENABLE_HIT_BY_RAY_IN_ADVANCE', False, PART_WEAPON_POS_MAIN2)
        self.mecha.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, PART_WEAPON_POS_MAIN2)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def _aim_target(self, target, *args, **kwargs):
        if type(target) is str:
            unit = EntityManager.getentity(target)
            if not (unit and unit.logic):
                return
            target = unit.logic
        if target == self._target:
            return
        self._target = target
        pic_path = 'gui/ui_res_2/battle/mech_attack/mech_8015_sub_hit_4.png' if target else 'gui/ui_res_2/battle/mech_attack/mech_8015_sub_hit_1.png'
        self.panel.img_sub_aim_1.SetDisplayFrameByPath('', pic_path)

    def refresh_second_weapon_aim_scale(self, *args):
        if self.mecha:
            cur_scale = self.mecha.share_data.ref_aim_helper_scale.get(PART_WEAPON_POS_MAIN2, 1.0)
            self.panel.nd_sub_no_spread.setScale(cur_scale)

    def clear_delay_timer(self):
        if self.enhance_weapon_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.enhance_weapon_timer_id)
        self.enhance_weapon_timer_id = None
        return

    def _on_change_enhance_weapon_fire(self, is_switch):
        self.clear_delay_timer()
        self.enhance_weapon_timer_id = global_data.game_mgr.register_logic_timer(lambda : self.panel.nd_sp.setVisible(bool(is_switch)), interval=0.5, times=1, mode=CLOCK)

    def on_finalize_panel(self):
        super(Mecha8015AimUI, self).on_finalize_panel()
        self.clear_delay_timer()