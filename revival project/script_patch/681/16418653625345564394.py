# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8010AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.common_const.mecha_const import STATE_HUMANOID, STATE_LEVITATE, STATE_INJECT
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3, PART_WEAPON_POS_MAIN4
STATE_TO_WEAPON_POS_MAP = {STATE_HUMANOID: PART_WEAPON_POS_MAIN1,
   STATE_LEVITATE: PART_WEAPON_POS_MAIN2,
   STATE_INJECT: PART_WEAPON_POS_MAIN3
   }
MAIN_WEAPON_POS_SET = frozenset([PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3])

class Mecha8010AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8010'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        super(Mecha8010AimUI, self).on_init_panel()
        self.init_auto_aim_widget()

    def init_parameters(self):
        self.main_aim_show = False
        self.second_aim_show = False
        super(Mecha8010AimUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr2
        self.aim_spread_mgr = MechaAimSpreadMgr2(self.panel)

    def init_auto_aim_widget(self):
        from .MechaAutoAimWidget import MechaAutoAimWidget
        self.auto_aim_widget = MechaAutoAimWidget(self.panel, auto_aim_fov_map={PART_WEAPON_POS_MAIN3: 120.0
           }, target_refreshed_anim_map={PART_WEAPON_POS_MAIN4: 'auto_sub_lock'
           }, need_play_lock_sound_map={PART_WEAPON_POS_MAIN4: True
           }, lock_node_map={PART_WEAPON_POS_MAIN4: self.panel.nd_sub_aim_lock
           }, reset_node_map={PART_WEAPON_POS_MAIN4: self.panel.img_aim1
           }, lock_node_parent_map={PART_WEAPON_POS_MAIN4: self.panel.nd_sub_aim
           })

    def on_finalize_panel(self):
        super(Mecha8010AimUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            regist_func('E_ACC_SKILL_BEGIN', self.on_second_weapon_begin, -1)
            regist_func('E_ACC_SKILL_END', self.on_second_weapon_end, -1)
            regist_func('E_SET_FLIGHT_STATE', self._set_flight_state)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            unregist_func('E_ACC_SKILL_BEGIN', self.on_second_weapon_begin)
            unregist_func('E_ACC_SKILL_END', self.on_second_weapon_end)
            unregist_func('E_SET_FLIGHT_STATE', self._set_flight_state)
        self.mecha = None
        return

    def enable_weapon_aim_helper(self, enabled, weapon_pos, **kwargs):
        if weapon_pos in MAIN_WEAPON_POS_SET:
            self._enable_main_weapon_aim_helper(enabled, weapon_pos)
        else:
            self._enable_second_weapon_aim_helper(enabled, weapon_pos)

    def _enable_main_weapon_aim_helper(self, enabled, weapon_pos):
        self.main_aim_show = enabled
        if enabled and not self.second_aim_show and self.auto_aim_widget.refresh_auto_aim_range_appearance(weapon_pos):
            self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
            self.auto_aim_widget.show()
            self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_target, weapon_pos)
        else:
            self.auto_aim_widget.hide()
            self.auto_aim_widget.update_aim_target(None, weapon_pos)
        return

    def _enable_second_weapon_aim_helper(self, enabled, weapon_pos):
        if enabled:
            self.panel.PlayAnimation('show_sub_auto')
            self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
            self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_target, weapon_pos)
        else:
            self.panel.PlayAnimation('disappear_sub_auto')
            self.auto_aim_widget.hide()
            self.auto_aim_widget.update_aim_target(None, weapon_pos)
        return

    def on_second_weapon_begin(self, *args):
        self.second_aim_show = True
        if self.panel.IsPlayingAnimation('disappear_sub'):
            self.panel.StopAnimation('disappear_sub')
        self.panel.PlayAnimation('show_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN4)

    def on_second_weapon_end(self, *args):
        self.second_aim_show = False
        if self.panel.IsPlayingAnimation('show_sub'):
            self.panel.StopAnimation('show_sub')
        self.panel.PlayAnimation('disappear_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def _set_flight_state(self, state, *args):
        self.aim_spread_mgr and self.aim_spread_mgr.set_weapon_pos(STATE_TO_WEAPON_POS_MAP[state])
        self.start_update_front_sight_extra_info(STATE_TO_WEAPON_POS_MAP[state])