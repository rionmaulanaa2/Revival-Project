# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8032AimUI.py
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON, SUB_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN4
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
import time
AIM_NODE_SUFFIX = {'normal': '',
   'enhance': '_2'
   }

class Mecha8032AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8032'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       PART_WEAPON_POS_MAIN4: MAIN_WEAPON
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.PlayAnimation('show_bullet')
        self.panel.nd_prog.setVisible(False)
        self.panel.nd_aim.setVisible(True)
        self.panel.nd_aim_2.setVisible(False)
        super(Mecha8032AimUI, self).on_init_panel()

    def init_parameters(self):
        self._target = None
        self._cache_target = None
        self.check_timer = None
        self.is_in_second_weapon_aim = False
        self.main_weapon_enhanced = False
        self.cur_state = 'normal'
        self._prog_timer = None
        self._prog_left_time = 0.0
        self._prog_duration = 0.0
        self._prog_start_time = 0.0
        super(Mecha8032AimUI, self).init_parameters()
        return

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

        def get_aim_node():
            node = getattr(self.panel, 'nd_aim%s' % AIM_NODE_SUFFIX[self.cur_state], None)
            if node and node.isVisible():
                return node.nd_spread
            else:
                return

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)

    def disappear(self):
        self.panel.PlayAnimation('disappear_bullet')
        super(Mecha8032AimUI, self).disappear()

    def on_finalize_panel(self):
        if self._prog_timer:
            global_data.game_mgr.unregister_logic_timer(self._prog_timer)
        super(Mecha8032AimUI, self).on_finalize_panel()
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
            regist_func('E_ENABLE_THROUGH_SHIELD', self.on_enable_through_shield)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self._cache_target = self.mecha.sd.ref_aim_target
            self.on_enable_through_shield(False)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SHOW_ACC_WP_TRACK', self.hide_aim_ui)
            unregist_func('E_STOP_ACC_WP_TRACK', self.show_aim_ui)
            unregist_func('E_ENABLE_THROUGH_SHIELD', self.on_enable_through_shield)
        self.mecha = None
        return

    def show_aim_ui(self):
        if self.panel and self.panel.nd_aim:
            if self.cur_state == 'normal':
                self.panel.nd_aim.setVisible(True)
            else:
                self.panel.nd_aim_2.setVisible(True)
        self.panel.nd_sub_weapon.setVisible(False)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def hide_aim_ui(self):
        if self.panel and self.panel.nd_aim:
            self.panel.nd_aim.setVisible(False)
            self.panel.nd_aim_2.setVisible(False)
        self.panel.nd_sub_weapon.setVisible(True)
        self.stop_update_front_sight_extra_info()

    def _update_progress(self):
        cur_time = time.time() - self._prog_start_time
        if cur_time > self._prog_left_time:
            self.panel.nd_prog.setVisible(False)
            return
        self.panel.prog.SetPercentage((1.0 - cur_time / self._prog_duration) * 100)

    def on_enable_through_shield(self, enable, left_time=0.0, duration=0.0):
        if enable:
            if self._prog_timer:
                global_data.game_mgr.unregister_logic_timer(self._prog_timer)
            self.cur_state = 'enhance'
            self._prog_left_time = left_time
            self._prog_duration = duration
            self._prog_start_time = time.time()
            self.panel.nd_prog.setVisible(True)
            self.panel.nd_aim.setVisible(False)
            self.panel.nd_aim_2.setVisible(True)
            if self.aim_spread_mgr:
                self.aim_spread_mgr.set_weapon_pos(PART_WEAPON_POS_MAIN4)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN4)
            self._prog_timer = global_data.game_mgr.register_logic_timer(self._update_progress, interval=0.1, times=-1, mode=2)
        else:
            self.cur_state = 'normal'
            if self._prog_timer:
                global_data.game_mgr.unregister_logic_timer(self._prog_timer)
            if self.aim_spread_mgr:
                self.aim_spread_mgr.set_weapon_pos(PART_WEAPON_POS_MAIN1)
            self.panel.nd_aim.setVisible(True)
            self.panel.nd_aim_2.setVisible(False)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
            self.panel.nd_prog.setVisible(False)