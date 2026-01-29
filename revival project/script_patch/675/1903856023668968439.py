# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8034AimUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from common.utils.timer import CLOCK
from logic.gcommon import time_utility as tutils

class Mecha8034AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8034'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }
    MECHA_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self):
        super(Mecha8034AimUI, self).on_init_panel()
        self.panel.nd_sub_aim.setVisible(False)
        self.sub_shown = False

    def init_parameters(self):
        super(Mecha8034AimUI, self).init_parameters()
        self.fuel_level_reset_time = None
        self.fuel_level_reset_ts = None
        self.fuel_level_reset_timer_id = None
        return

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)
        self.aim_spread_mgr.set_weapon_pos(PART_WEAPON_POS_MAIN1)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_POISON_JUMP_FUEL_LEVEL', self.on_poison_jump_fuel_level_changed)
            regist_func('E_SHOW_SEC_WP_ACC', self.show_sec_weapon_acc)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_POISON_JUMP_FUEL_LEVEL', self.on_poison_jump_fuel_level_changed)
            unregist_func('E_SHOW_SEC_WP_ACC', self.show_sec_weapon_acc)
        self.mecha = None
        return

    def on_poison_jump_fuel_level_changed(self, fuel_level, reset_time=None, reset_ts=None):
        show_sub = fuel_level > 0
        if self.panel.nd_sub.isVisible() ^ show_sub:
            self.panel.PlayAnimation('show_sub' if show_sub else 'disappear_sub')
        if show_sub:
            self.fuel_level_reset_time = reset_time
            self.fuel_level_reset_ts = reset_ts or tutils.time() + reset_time
            if not self.fuel_level_reset_timer_id:
                self.fuel_level_reset_timer_id = global_data.game_mgr.register_logic_timer(self.update_fuel_level_reset_prog, interval=0.1, times=-1, mode=CLOCK)
        else:
            global_data.game_mgr.unregister_logic_timer(self.fuel_level_reset_timer_id)
            self.fuel_level_reset_timer_id = None
        self.update_fuel_level_reset_prog()
        return

    def update_fuel_level_reset_prog(self):
        prog = max((self.fuel_level_reset_ts - tutils.time()) * 100.0 / self.fuel_level_reset_time, 0)
        self.panel.prog_sub_left.setPercentage(int(prog))

    def _play_sub_weapon_anim(self, show):
        if show:
            self.panel.StopAnimation('disappear_sub_weapon')
            self.panel.PlayAnimation('show_sub_weapon')
        else:
            self.panel.StopAnimation('show_sub_weapon')
            self.panel.PlayAnimation('disappear_sub_weapon')

    def show_sec_weapon_acc(self, show):
        if self.sub_shown ^ show:
            self.sub_shown = show
            self._play_sub_weapon_anim(show)

    def on_finalize_panel(self):
        super(Mecha8034AimUI, self).on_finalize_panel()
        global_data.game_mgr.unregister_logic_timer(self.fuel_level_reset_timer_id)
        self.fuel_level_reset_timer_id = None
        return