# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8029AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
from common.utils.cocos_utils import neox_pos_to_cocos
from mobile.common.EntityManager import EntityManager
from common.utils import timer
from logic.gcommon.common_const.mecha_const import MECHA_8029_FORM_SCOUT, MECHA_8029_FORM_HUNT
import world
import cc
STATE_TO_WEAPON_POS_MAP = {MECHA_8029_FORM_SCOUT: PART_WEAPON_POS_MAIN1,
   MECHA_8029_FORM_HUNT: PART_WEAPON_POS_MAIN3
   }
AIM_POST_FIX = {MECHA_8029_FORM_HUNT: '_2',
   MECHA_8029_FORM_SCOUT: '_1'
   }
AIM_SWITCH_ANI = {MECHA_8029_FORM_SCOUT: 'switch_type_1',
   MECHA_8029_FORM_HUNT: 'switch_type_2'
   }

class Mecha8029AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8029'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN3: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('show_bullet')
        super(Mecha8029AimUI, self).on_init_panel()

    def init_parameters(self):
        self._state = MECHA_8029_FORM_SCOUT
        super(Mecha8029AimUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

        def get_aim_node():
            node = getattr(self.panel, 'nd_type%s' % AIM_POST_FIX[self._state], None)
            if node and node.isVisible():
                return node.nd_aim.nd_spead
            else:
                return

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)

    def disappear(self):
        self.panel.PlayAnimation('disappear_bullet')
        super(Mecha8029AimUI, self).disappear()

    def on_finalize_panel(self):
        super(Mecha8029AimUI, self).on_finalize_panel()

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_SHOW_ACC_WP_TRACK', self.hide_aim_ui)
            regist_func('E_STOP_ACC_WP_TRACK', self.show_aim_ui)
            regist_func('E_SWITCH_WEAPON', self.on_switch_weapon)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self._cache_target = self.mecha.sd.ref_aim_target
            self._state = self.mecha.sd.ref_cur_state
            self.on_switch_weapon(self._state)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SHOW_ACC_WP_TRACK', self.hide_aim_ui)
            unregist_func('E_STOP_ACC_WP_TRACK', self.show_aim_ui)
            unregist_func('E_SWITCH_WEAPON', self.on_switch_weapon)
        self.mecha = None
        return

    def show_aim_ui(self):
        if self.panel and self.panel.nd_aim:
            self.panel.nd_aim.setVisible(True)

    def hide_aim_ui(self):
        if self.panel and self.panel.nd_aim:
            self.panel.nd_aim.setVisible(False)

    def on_switch_weapon(self, new_state):
        if self.aim_spread_mgr:
            self.aim_spread_mgr.set_weapon_pos(STATE_TO_WEAPON_POS_MAP[new_state])
        if self.mecha:
            self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', STATE_TO_WEAPON_POS_MAP[new_state])
        self.start_update_front_sight_extra_info(STATE_TO_WEAPON_POS_MAP[new_state])
        self._state = new_state
        self.panel.PlayAnimation(AIM_SWITCH_ANI[self._state])