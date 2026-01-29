# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8024AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
from common.utils.cocos_utils import neox_pos_to_cocos
from mobile.common.EntityManager import EntityManager
from common.utils import timer
import world
import cc

class Mecha8024AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8017'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('show_bullet')
        super(Mecha8024AimUI, self).on_init_panel()

    def init_parameters(self):
        self._target = None
        self._cache_target = None
        self.check_timer = None
        self.is_in_second_weapon_aim = False
        self.main_weapon_enhanced = False
        super(Mecha8024AimUI, self).init_parameters()
        return

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def disappear(self):
        self.panel.PlayAnimation('disappear_bullet')
        super(Mecha8024AimUI, self).disappear()

    def on_finalize_panel(self):
        super(Mecha8024AimUI, self).on_finalize_panel()
        self._target = None
        self._cache_target = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_SHOW_ACC_WP_TRACK', self.hide_aim_ui)
            regist_func('E_STOP_ACC_WP_TRACK', self.show_aim_ui)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self._cache_target = self.mecha.sd.ref_aim_target
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SHOW_ACC_WP_TRACK', self.hide_aim_ui)
            unregist_func('E_STOP_ACC_WP_TRACK', self.show_aim_ui)
        self.mecha = None
        return

    def show_aim_ui(self):
        if self.panel and self.panel.nd_aim:
            self.panel.nd_aim.setVisible(True)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def hide_aim_ui(self):
        if self.panel and self.panel.nd_aim:
            self.panel.nd_aim.setVisible(False)
        self.stop_update_front_sight_extra_info()