# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8031AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
import logic.gcommon.const as g_const
from common.cfg import confmgr
from common.utils.timer import RELEASE
import cc

class Mecha8031AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8031'
    WEAPON_INFO = {g_const.PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       g_const.PART_WEAPON_POS_MAIN2: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

        def get_aim_node():
            return self.panel.nd_aim.nd_spread

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)
        self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN1)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_TRANS_TO_REAPER', self.on_trans_to_reaper, 99)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_TRANS_TO_REAPER', self.on_trans_to_reaper)
        self.mecha = None
        return

    def on_trans_to_reaper(self, left_time, beacon_eid=None):
        if left_time > 0:
            self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN2)
        else:
            self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN1)
        self.aim_spread_mgr._on_spread()