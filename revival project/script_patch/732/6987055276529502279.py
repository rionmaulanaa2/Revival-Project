# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8028AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
import logic.gcommon.const as g_const
from common.utils.timer import RELEASE
ACCUMULATE_TO_PROGRESS_VALUE_MAP = {-1: 50,
   0: 57,
   1: 62,
   2: 66,
   3: 70,
   4: 73,
   5: 75
   }

class Mecha8028AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8028'
    WEAPON_INFO = {g_const.PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       g_const.PART_WEAPON_POS_MAIN4: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SCALE)

        def get_aim_node():
            if self.is_fairy_shape:
                return self.panel.nd_aim_2.nd_spread
            else:
                return self.panel.nd_aim.nd_spread

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)
        self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN1)

    def on_finalize_panel(self):
        super(Mecha8028AimUI, self).on_finalize_panel()
        if self.accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self.accumulate_timer)
            self.accumulate_timer = None
        return

    def init_parameters(self):
        self.cur_progress = 0
        self.cur_end_progress = 100
        self.accumulate_pre_anim_duration = 0.3
        self.accumulate_interval = 0.2
        self.accumulate_speed = 0.0
        self.accumulate_timer = None
        self.is_fairy_shape = False
        super(Mecha8028AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_PLAY_SWITCH_FAIRY_SHAPE_EFFECT', self.begin_switch_to_fairy)
            regist_func('E_PLAY_SWITCH_RABBIT_SHAPE_EFFECT', self.begin_switch_to_rabbit)
            regist_func('E_SWITCH_MECHA_MODEL', self.on_switch_mecha_model)
            regist_func('E_ACC_SKILL_BEGIN', self.start_acc_weapon)
            regist_func('E_ACC_SKILL_END', self.stop_acc_weapon)
            regist_func('E_PLAY_FAIRY_ACCUMULATE_EFFECT', self.accumulate_progress_changed)
            regist_func('E_SHOW_FAIRY_ACCUMULATE_WEAPON_ENHANCED_UI', self.show_accumulate_weapon_enhanced)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            if not mecha.ev_g_is_using_second_model():
                self.begin_switch_to_fairy()
                self.on_switch_mecha_model(False)
            else:
                self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', g_const.PART_WEAPON_POS_MAIN1)
                self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_PLAY_SWITCH_FAIRY_SHAPE_EFFECT', self.begin_switch_to_fairy)
            unregist_func('E_PLAY_SWITCH_RABBIT_SHAPE_EFFECT', self.begin_switch_to_rabbit)
            unregist_func('E_SWITCH_MECHA_MODEL', self.on_switch_mecha_model)
            unregist_func('E_ACC_SKILL_BEGIN', self.start_acc_weapon)
            unregist_func('E_ACC_SKILL_END', self.stop_acc_weapon)
            unregist_func('E_PLAY_FAIRY_ACCUMULATE_EFFECT', self.accumulate_progress_changed)
            unregist_func('E_SHOW_FAIRY_ACCUMULATE_WEAPON_ENHANCED_UI', self.show_accumulate_weapon_enhanced)
        self.mecha = None
        if self.accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self.accumulate_timer)
            self.accumulate_timer = None
        return

    def begin_switch_to_fairy(self):
        self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN4)
        self.panel.StopAnimation('switch_type_1')
        self.panel.PlayAnimation('switch_type_2')

    def begin_switch_to_rabbit(self):
        self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN1)
        self.panel.StopAnimation('switch_type_2')
        self.panel.PlayAnimation('switch_type_1')

    def on_switch_mecha_model(self, flag):
        if flag:
            self.is_fairy_shape = False
            self.aim_spread_mgr and self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN1)
            self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', g_const.PART_WEAPON_POS_MAIN1)
        else:
            self.is_fairy_shape = True
            self.aim_spread_mgr and self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN4)
            self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', g_const.PART_WEAPON_POS_MAIN4)

    def start_acc_weapon(self, *args):
        if self.mecha.sd.ref_is_fairy_shape:
            self.panel.StopAnimation('disappear_sec_2')
            self.panel.PlayAnimation('show_sec_2')
            self.accumulate_progress_changed(-1)
            self.accumulate_pre_anim_duration = self.mecha.sd.ref_accumulate_pre_anim_duration
            self.accumulate_interval = self.mecha.sd.ref_accumulate_interval
        else:
            self.panel.StopAnimation('disappear_sec')
            self.panel.PlayAnimation('show_sec')

    def stop_acc_weapon(self, *args):
        if self.mecha.sd.ref_is_fairy_shape:
            self.panel.StopAnimation('show_sec_2')
            self.panel.PlayAnimation('disappear_sec_2')
        else:
            self.panel.StopAnimation('show_sec')
            self.panel.PlayAnimation('disappear_sec')
        if self.accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self.accumulate_timer)
            self.accumulate_timer = None
        self.panel.prog.SetPercentage(ACCUMULATE_TO_PROGRESS_VALUE_MAP[-1])
        return

    def interpolate_accumulate_progress(self, dt):
        self.cur_progress += self.accumulate_speed * dt
        reach_end = False
        if self.cur_progress > self.cur_end_progress:
            self.cur_progress = self.cur_end_progress
            reach_end = True
        self.panel.prog.SetPercentage(self.cur_progress)
        if reach_end:
            self.accumulate_timer = None
            return RELEASE
        else:
            return

    def accumulate_progress_changed(self, accumulate_index):
        self.cur_progress = ACCUMULATE_TO_PROGRESS_VALUE_MAP[accumulate_index]
        self.panel.prog.SetPercentage(self.cur_progress)
        if accumulate_index == self.mecha.sd.ref_cur_max_accumulate_index:
            if self.accumulate_timer:
                global_data.game_mgr.unregister_logic_timer(self.accumulate_timer)
                self.accumulate_timer = None
        else:
            if not self.accumulate_timer:
                self.accumulate_timer = global_data.game_mgr.register_logic_timer(self.interpolate_accumulate_progress, interval=1, times=-1, timedelta=True)
            gap = ACCUMULATE_TO_PROGRESS_VALUE_MAP[accumulate_index + 1] - ACCUMULATE_TO_PROGRESS_VALUE_MAP[accumulate_index]
            if accumulate_index == -1:
                self.accumulate_speed = gap / self.accumulate_pre_anim_duration
            else:
                self.accumulate_speed = gap / self.accumulate_interval
            self.cur_end_progress = ACCUMULATE_TO_PROGRESS_VALUE_MAP[accumulate_index + 1]
        return

    def show_accumulate_weapon_enhanced(self, visible):
        self.panel.nd_special.setVisible(bool(visible))