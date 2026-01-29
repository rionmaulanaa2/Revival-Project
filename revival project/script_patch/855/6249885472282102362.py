# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8035LockedUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from logic.gcommon.const import PART_WEAPON_POS_MAIN2
from logic.gcommon.common_const.skill_const import SKILL_8035_DASH

class Mecha8035LockedUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8035_2'
    WEAPON_INFO = {}

    def on_init_panel(self, *args, **kwargs):
        super(Mecha8035LockedUI, self).on_init_panel()
        self.init_auto_aim_widget()

    def init_parameters(self):
        super(Mecha8035LockedUI, self).init_parameters()
        self.is_locking_target = False
        self.can_fly_to_locked_target = False
        self.doing_lock_appearance = False

    def init_aim_spread_mgr(self):
        pass

    def init_bullet_widget(self):
        pass

    @staticmethod
    def get_target_pos_func(target):
        return target.ev_g_position()

    def init_auto_aim_widget(self):
        from .MechaAutoAimWidget import MechaAutoAimWidget
        self.auto_aim_widget = MechaAutoAimWidget(self.panel, auto_aim_fov_map={PART_WEAPON_POS_MAIN2: 84
           }, get_target_pos_func=self.get_target_pos_func)

    def on_finalize_panel(self):
        super(Mecha8035LockedUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ACC_SKILL_BEGIN', self.on_acc_skill_begin)
            regist_func('E_ACC_SKILL_END', self.on_acc_skill_end)
            regist_func('E_LOCKED_FAN_CHANGED', self.on_locked_fan_changed)
            regist_func('E_ENERGY_FULL', self.on_skill_energy_full)
            regist_func('E_DO_DASH_SKILL', self.on_do_dash_skill)
            if self.auto_aim_widget:
                self.auto_aim_widget.on_mecha_set(mecha)
                self.auto_aim_widget.refresh_auto_aim_parameters(PART_WEAPON_POS_MAIN2)
                self.auto_aim_widget.refresh_auto_aim_range_appearance(PART_WEAPON_POS_MAIN2, set_size_directly=True, size_offset=80)
            self.can_fly_to_locked_target = mecha.ev_g_can_cast_skill(SKILL_8035_DASH)
            if mecha.sd.ref_cur_locked_fan_unit:
                self.on_locked_fan_changed(mecha.sd.ref_cur_locked_fan_unit)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_BEGIN', self.on_acc_skill_begin)
            unregist_func('E_ACC_SKILL_END', self.on_acc_skill_end)
            unregist_func('E_LOCKED_FAN_CHANGED', self.on_locked_fan_changed)
            unregist_func('E_ENERGY_FULL', self.on_skill_energy_full)
            unregist_func('E_DO_DASH_SKILL', self.on_do_dash_skill)
        self.mecha = None
        return

    def on_acc_skill_begin(self, *args):
        self.panel.StopAnimation('disappear_sub_weapon')
        self.panel.PlayAnimation('show_sub_weapon')

    def on_acc_skill_end(self, *args):
        self.panel.StopAnimation('show_sub_weapon')
        self.panel.PlayAnimation('disappear_sub_weapon')

    def _do_lock_appearance(self, flag):
        if flag:
            if self.doing_lock_appearance ^ flag:
                self.auto_aim_widget.show()
            self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_cur_locked_fan_unit, PART_WEAPON_POS_MAIN2)
        elif self.doing_lock_appearance ^ flag:
            self.auto_aim_widget.hide()
            self.auto_aim_widget.update_aim_target(None, PART_WEAPON_POS_MAIN2)
        self.doing_lock_appearance = flag
        return

    def on_locked_fan_changed(self, target):
        self.is_locking_target = bool(target)
        self._do_lock_appearance(self.is_locking_target and self.can_fly_to_locked_target)

    def on_skill_energy_full(self, skill_id):
        if skill_id != SKILL_8035_DASH:
            return
        self.can_fly_to_locked_target = True
        self._do_lock_appearance(self.is_locking_target)

    def on_do_dash_skill(self):
        if not global_data.no_cd:
            self.can_fly_to_locked_target = False
        self._do_lock_appearance(False)