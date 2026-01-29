# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8037AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from common.utils.timer import RELEASE
UNDER_GROUND_PROGRESS_MIN_PERCENT = 62
UNDER_GROUND_PROGRESS_MAX_PERCENT = 88
UNDER_GROUND_PROGRESS_GAP = UNDER_GROUND_PROGRESS_MAX_PERCENT - UNDER_GROUND_PROGRESS_MIN_PERCENT

class Mecha8037AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8037'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self):
        super(Mecha8037AimUI, self).on_init_panel()
        self.panel.lab_forbiden.SetString(557)

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def _unregister_under_ground_timer(self):
        if self.under_ground_timer:
            global_data.game_mgr.unregister_logic_timer(self.under_ground_timer)
            self.under_ground_timer = None
        return

    def _unregister_danger_timer(self):
        if self.danger_timer:
            global_data.game_mgr.unregister_logic_timer(self.danger_timer)
            self.danger_timer = None
        return

    def on_finalize_panel(self):
        self._unregister_under_ground_timer()
        self._unregister_danger_timer()
        super(Mecha8037AimUI, self).on_finalize_panel()

    def init_parameters(self):
        self.start_under_ground_count_down_time = 0.0
        self.max_under_ground_duration = 2.0
        self.under_ground_timer = None
        self.showing_under_ground = False
        self.start_danger_count_down_time = 0.0
        self.max_danger_duration = 2.0
        self.danger_timer = None
        self.showing_danger = False
        super(Mecha8037AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_SHOW_UNDER_GROUND_COUNT_DOWN', self.show_under_ground_count_down)
            regist_func('E_SHOW_DANGER_COUNT_DOWN', self.show_danger_count_down)
            regist_func('E_DO_UNDER_GROUND_UI_APPEARANCE', self.do_under_ground_ui_appearance)
            regist_func('E_ACC_SKILL_BEGIN', self.on_sec_weapon_begin)
            regist_func('E_ACC_SKILL_END', self.on_sec_weapon_end)
            regist_func('E_SHOW_FORBID_SUMMON_WALL_TAG', self.show_forbid_summon_wall_tag)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_SHOW_UNDER_GROUND_COUNT_DOWN', self.show_under_ground_count_down)
            unregist_func('E_SHOW_DANGER_COUNT_DOWN', self.show_danger_count_down)
            unregist_func('E_DO_UNDER_GROUND_UI_APPEARANCE', self.do_under_ground_ui_appearance)
            unregist_func('E_ACC_SKILL_BEGIN', self.on_sec_weapon_begin)
            unregist_func('E_ACC_SKILL_END', self.on_sec_weapon_end)
            unregist_func('E_SHOW_FORBID_SUMMON_WALL_TAG', self.show_forbid_summon_wall_tag)
        self.mecha = None
        return

    def update_under_ground_count_down_progress(self):
        cur_time = global_data.game_time
        percent = (cur_time - self.start_under_ground_count_down_time) / self.max_under_ground_duration
        if percent > 1.0:
            percent = 1.0
        self.panel.nd_roll.prog_jet.SetPercent(UNDER_GROUND_PROGRESS_MIN_PERCENT + UNDER_GROUND_PROGRESS_GAP * (1.0 - percent))
        if percent >= 1.0:
            self.under_ground_timer = None
            return RELEASE
        else:
            return

    def show_under_ground_count_down(self, flag, start_count_down_time=0, duration=2.0):
        if flag:
            self.start_under_ground_count_down_time = start_count_down_time
            self.max_under_ground_duration = duration
            if self.under_ground_timer is None:
                self.under_ground_timer = global_data.game_mgr.register_logic_timer(self.update_under_ground_count_down_progress, interval=1, times=-1)
            if not self.showing_under_ground:
                self.panel.StopAnimation('disappear_sp')
                self.panel.PlayAnimation('show_sp')
        elif self.showing_under_ground:
            self.panel.StopAnimation('show_sp')
            self.panel.PlayAnimation('disappear_sp')
            self._unregister_under_ground_timer()
        self.showing_under_ground = flag
        return

    def update_danger_count_down_progress(self):
        cur_time = global_data.game_time
        percent = (cur_time - self.start_danger_count_down_time) / self.max_danger_duration
        if percent > 1.0:
            percent = 1.0
        self.panel.nd_roll_danger.prog_jet.SetPercent(UNDER_GROUND_PROGRESS_MIN_PERCENT + UNDER_GROUND_PROGRESS_GAP * percent)
        if percent >= 1.0:
            self.danger_timer = None
            return RELEASE
        else:
            return

    def show_danger_count_down(self, flag, start_count_down_time=0, duration=2.0):
        if flag:
            self.start_danger_count_down_time = start_count_down_time
            self.max_danger_duration = duration
            if self.danger_timer is None:
                self.danger_timer = global_data.game_mgr.register_logic_timer(self.update_danger_count_down_progress, interval=1, times=-1)
            if not self.showing_danger:
                self.StopAnimation('dissappear_danger')
                self.PlayAnimation('danger')
                self.PlayAnimation('show_danger')
        elif self.showing_danger:
            self.StopAnimation('danger')
            self.StopAnimation('show_danger')
            self.PlayAnimation('dissappear_danger')
            self._unregister_danger_timer()
        self.showing_danger = flag
        return

    def do_under_ground_ui_appearance(self, flag):
        if flag:
            self.stop_update_front_sight_extra_info()
        else:
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_sec_weapon_begin(self, *args):
        self.panel.StopAnimation('disappear_sub')
        self.panel.PlayAnimation('show_sub')

    def on_sec_weapon_end(self, *args):
        self.panel.StopAnimation('show_sub')
        self.panel.PlayAnimation('disappear_sub')

    def show_forbid_summon_wall_tag(self, flag):
        self.panel.lab_forbiden.setVisible(flag)