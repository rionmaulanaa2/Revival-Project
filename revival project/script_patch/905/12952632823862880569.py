# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8022AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
from .MechaBulletWidget import MAIN_WEAPON

class Mecha8022AimUI(BaseMechaAimUI):
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN3: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

        def get_aim_node():
            if self.is_cannon_shape:
                return self.panel.nd_aim_sec.nd_spread
            else:
                return self.panel.nd_aim.nd_spread

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)
        self.aim_spread_mgr.set_weapon_pos(PART_WEAPON_POS_MAIN1)

    def init_parameters(self):
        super(Mecha8022AimUI, self).init_parameters()
        self.is_shooting = False
        self.is_cannon_shape = False

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_REFRESH_STATE_PARAM', self.enter_cannon_shape)
            regist_func('E_RESET_STATE_PARAM', self.leave_cannon_shape)
            regist_func('E_ACC_SKILL_BEGIN', self._start_acc_weapon)
            regist_func('E_ACC_SKILL_END', self._stop_acc_weapon)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            func = self.enter_cannon_shape if mecha.share_data.ref_is_cannon_shape else (lambda : self.leave_cannon_shape(include_anim=False))
            func()
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_REFRESH_STATE_PARAM', self.enter_cannon_shape)
            unregist_func('E_RESET_STATE_PARAM', self.leave_cannon_shape)
            unregist_func('E_ACC_SKILL_BEGIN', self._start_acc_weapon)
            unregist_func('E_ACC_SKILL_END', self._stop_acc_weapon)
        self.mecha = None
        return

    def enter_cannon_shape(self, *args, **kwargs):
        self.is_cannon_shape = True
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('disappear_sec')
        self.panel.PlayAnimation('show_sec')
        self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', PART_WEAPON_POS_MAIN3)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN3)
        self.aim_spread_mgr._on_spread()

    def leave_cannon_shape(self, include_anim=True, *args, **kwargs):
        self.is_cannon_shape = False
        if include_anim:
            self.panel.StopAnimation('show_sec')
            self.panel.PlayAnimation('disappear_sec')
        self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', PART_WEAPON_POS_MAIN1)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
        self.aim_spread_mgr._on_spread()

    def _start_acc_weapon(self, *args):
        self.panel.StopAnimation('disappear_sub')
        self.panel.PlayAnimation('show_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN2)

    def _stop_acc_weapon(self, *args):
        self.panel.StopAnimation('show_sub')
        self.panel.PlayAnimation('disappear_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)