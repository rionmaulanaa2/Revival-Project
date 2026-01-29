# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8012AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gcommon.common_const import skill_const
from common.utils.timer import RELEASE
MIN_FLAMETHROWER_PERCENT = 52
MAX_FLAMETHROWER_PERCENT = 72
FLAMETHROWER_NORMAL_STATE = 0
FLAMETHROWER_EMPTY_STATE = 1
FLAMETHROWER_ENERGY_PIC_PREFIX = 'gui/ui_res_2/battle/mech_attack/'
FLAMETHROWER_ENERGY_PIC = {FLAMETHROWER_NORMAL_STATE: (
                             FLAMETHROWER_ENERGY_PIC_PREFIX + 'progress_8012_norm.png', FLAMETHROWER_ENERGY_PIC_PREFIX + 'pnl_8012_norm_bar.png', None),
   FLAMETHROWER_EMPTY_STATE: (
                            FLAMETHROWER_ENERGY_PIC_PREFIX + 'progress_8012_ban.png', FLAMETHROWER_ENERGY_PIC_PREFIX + 'pnl_8012_low_bar.png', 'spread_flash')
   }

class Mecha8012AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8012'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def on_init_panel(self):
        super(Mecha8012AimUI, self).on_init_panel()
        self.panel.lab_warning.SetStringWithAdapt(get_text_local_content(81104))
        self.panel.RecordAnimationNodeState('spread_flash')

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def on_finalize_panel(self):
        super(Mecha8012AimUI, self).on_finalize_panel()
        self._release_flamethrower_energy_state_timer()

    def init_parameters(self):
        self.over_loading = False
        self.playing_dash_pre = False
        self.last_val_percent = 100
        self.showing_ball_fuel = False
        self.is_ball_state = False
        self.need_resume_show_fuel = False
        self.showing_flamethrower_energy = False
        self.flamethrower_energy_state_timer = None
        self.cur_flamethrower_energy_state = FLAMETHROWER_NORMAL_STATE
        super(Mecha8012AimUI, self).init_parameters()
        return

    def init_event(self):
        left, full = self.mecha.ev_g_ball_overload_state()
        if left > 0:
            self.on_overload_start(left, full)
        else:
            left, full, normal = self.mecha.ev_g_ball_state()
            left = left - (full - normal)
            if left > 0:
                self.on_trans_to_ball(False, left, full)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_BALL_OVERLOAD_START', self.on_overload_start)
            regist_func('E_BALL_OVERLOAD_STOP', self.on_overload_stop)
            regist_func('E_SHOW_DASH_PRE_PROGRESS', self.on_show_dash_pre_progress)
            regist_func('E_SKILL_FUEL_CHANGE', self.on_skill_fuel_changed)
            regist_func('E_TRANS_TO_BALL', self.on_trans_to_ball)
            regist_func('E_TRANS_TO_HUMAN', self.on_trans_to_human)
            regist_func('E_CONTINUOUSLY_SHOOT', self.on_continuously_shoot)
            regist_func('E_ENERGY_CHANGE', self.on_skill_energy_changed)
            self.init_event()
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_BALL_OVERLOAD_START', self.on_overload_start)
            unregist_func('E_BALL_OVERLOAD_STOP', self.on_overload_stop)
            unregist_func('E_SHOW_DASH_PRE_PROGRESS', self.on_show_dash_pre_progress)
            unregist_func('E_SKILL_FUEL_CHANGE', self.on_skill_fuel_changed)
            unregist_func('E_TRANS_TO_BALL', self.on_trans_to_ball)
            unregist_func('E_TRANS_TO_HUMAN', self.on_trans_to_human)
            unregist_func('E_CONTINUOUSLY_SHOOT', self.on_continuously_shoot)
            unregist_func('E_ENERGY_CHANGE', self.on_skill_energy_changed)
        self.mecha = None
        return

    def on_trans_to_ball(self, first_trans, left_time, full_time):
        self.is_ball_state = True
        self.stop_update_front_sight_extra_info()

    def on_trans_to_human(self):
        self.is_ball_state = False
        self.panel.nd_aim.setVisible(True)
        self.panel.nd_aim.setOpacity(255)
        self.panel.nd_aim.setScale(1.0)
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def start_roll_count_down(self, left_time, full_time):

        def count_down(pass_time):
            percent = (left_time - pass_time) / full_time * 100
            percent = percent if percent > 0 else 0
            MIN_PERCENT = 47
            MAX_PERCENT = 59
            self.panel.progress_roll1.setPercentage(MIN_PERCENT + (MAX_PERCENT - MIN_PERCENT) * (percent * 1.0 / 100))
            self.panel.progress_roll2.setPercentage(MIN_PERCENT + (MAX_PERCENT - MIN_PERCENT) * (percent * 1.0 / 100))

        self.panel.nd_sp.StopTimerAction()
        self.panel.nd_sp.TimerAction(count_down, left_time, None, interval=0.05)
        return

    def on_overload_start(self, left_time, full_time):
        self.over_loading = False
        self.start_danger_count_down(left_time, full_time)
        self.panel.nd_sp.StopTimerAction()
        self.panel.nd_sp.setVisible(False)

        def delay_start():
            if self.is_valid() and self.mecha and self.mecha.is_valid() and self.mecha.ev_g_ball_overload():
                self.over_loading = True
                self.panel.PlayAnimation('show_danger')

        self.panel.nd_roll_danger.DelayCall(0.06, delay_start)

        def delay_show():
            if self.is_valid() and self.mecha and self.mecha.is_valid() and self.mecha.ev_g_ball_overload():
                self.panel.PlayAnimation('danger')

        self.panel.DelayCall(0.15, delay_show)

    def on_overload_stop(self):
        self.panel.StopAnimation('danger')
        if self.over_loading:
            self.panel.PlayAnimation('dissappear_danger')
        self.panel.nd_roll_danger.StopTimerAction()

        def delay_show_fuel():
            self.panel.StopAnimation('dissappear_danger')
            self.need_resume_show_fuel = self.showing_ball_fuel

        self.panel.DelayCall(self.panel.GetAnimationMaxRunTime('dissappear_danger'), delay_show_fuel)

    def start_danger_count_down(self, left_time, full_time):

        def count_down(pass_time):
            percent = (left_time - pass_time) / full_time * 100
            percent = percent if percent > 0 else 0
            percent = 100.0 - percent
            MIN_PERCENT = 62
            MAX_PERCENT = 88
            self.panel.nd_roll_danger.prog_jet.SetPercent(MIN_PERCENT + (MAX_PERCENT - MIN_PERCENT) * (percent / 100))

        self.panel.nd_roll_danger.StopTimerAction()
        self.panel.nd_roll_danger.TimerAction(count_down, left_time, None, interval=0.05)
        return

    def on_show_dash_pre_progress(self, show, pre_time=0):
        if show == self.playing_dash_pre:
            return
        else:
            if show:

                def count_down(pass_time):
                    percent = pass_time / pre_time * 100
                    self.panel.nd_sp2.progress1.setPercentage(percent)
                    self.panel.nd_sp2.progress2.setPercentage(percent)

                self.panel.nd_sp2.TimerAction(count_down, pre_time, None, interval=0.05)
                self.panel.PlayAnimation('show_sp2')
            else:
                self.panel.PlayAnimation('disappear_sp2')
            self.playing_dash_pre = show
            return

    def on_skill_fuel_changed(self, skill_id, percent):
        if skill_id != skill_const.SKILL_DASH_8012:
            return
        percent = int(percent * 100)
        if not self.showing_ball_fuel:
            if self.last_val_percent == 100 > percent:
                self.panel.StopAnimation('disappear_sp')
                self.panel.PlayAnimation('show_sp')
                self.showing_ball_fuel = True
        elif self.last_val_percent <= percent == 100:
            self.showing_ball_fuel = False
            self.panel.StopAnimation('show_sp')
            self.panel.PlayAnimation('disappear_sp')
        elif self.need_resume_show_fuel:
            self.panel.nd_sp.setVisible(True)
            self.panel.nd_sp.setOpacity(255)
            self.panel.nd_roll.setOpacity(255)
            self.panel.nd_roll.prog_jet.setOpacity(255)
            self.need_resume_show_fuel = False
        MIN_PERCENT = 62
        MAX_PERCENT = 88
        self.panel.nd_roll.prog_jet.SetPercent(MIN_PERCENT + (MAX_PERCENT - MIN_PERCENT) * (percent * 1.0 / 100))
        self.last_val_percent = percent

    def _release_flamethrower_energy_state_timer(self):
        if self.flamethrower_energy_state_timer:
            global_data.game_mgr.unregister_logic_timer(self.flamethrower_energy_state_timer)
            self.flamethrower_energy_state_timer = None
        return

    def _update_flamethrower_energy_state(self):
        if not self.panel or not self.panel.isValid() or not self.mecha:
            return RELEASE
        else:
            if not self.mecha.ev_g_can_cast_skill(801257) or not self.mecha.ev_g_can_continuously_shoot():
                new_state = FLAMETHROWER_EMPTY_STATE
            else:
                new_state = FLAMETHROWER_NORMAL_STATE
            if new_state != self.cur_flamethrower_energy_state:
                self.cur_flamethrower_energy_state = new_state
                prog_pic, panel_pic, anim_name = FLAMETHROWER_ENERGY_PIC[new_state]
                self.panel.progress_charge.SetProgressTexture(prog_pic)
                self.panel.pnl_progress_bar.SetDisplayFrameByPath('', panel_pic)
                if anim_name is None:
                    self.panel.StopAnimation('spread_flash')
                    self.panel.RecoverAnimationNodeState('spread_flash')
                else:
                    self.panel.PlayAnimation('spread_flash')
            return

    def _show_flamethrower_energy(self, flag):
        self.showing_flamethrower_energy = flag
        self.panel.nd_spread_fire.setVisible(flag)
        self.panel.nd_spread.setVisible(not flag)
        hide_anim_name = 'spread_fire_disappear' if flag else 'spread_fire_show'
        show_anim_name = 'spread_fire_show' if flag else 'spread_fire_disappear'
        self.panel.StopAnimation(hide_anim_name)
        self.panel.PlayAnimation(show_anim_name)

    def on_continuously_shoot(self, flag):
        if flag and not self.showing_flamethrower_energy:
            self._release_flamethrower_energy_state_timer()
            self._show_flamethrower_energy(flag)
            self.flamethrower_energy_state_timer = global_data.game_mgr.register_logic_timer(self._update_flamethrower_energy_state, interval=1, times=-1)
        elif self.showing_flamethrower_energy:
            if self.panel.progress_charge.getPercentage() == MAX_FLAMETHROWER_PERCENT:
                self._release_flamethrower_energy_state_timer()
                self._show_flamethrower_energy(flag)
        if flag:
            self.stop_update_front_sight_extra_info()
        else:
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_flamethrower_energy_changed(self, energy_rate):
        self.panel.progress_charge.SetPercent(MIN_FLAMETHROWER_PERCENT + energy_rate * (MAX_FLAMETHROWER_PERCENT - MIN_FLAMETHROWER_PERCENT))
        if energy_rate >= 1.0:
            self._show_flamethrower_energy(False)

    def on_ball_dash_energy_changed(self, energy_rate):
        nd_energy = self.panel.nd_sp2_cd
        if energy_rate < 1.0 and not self.is_ball_state:
            if not nd_energy.isVisible():
                nd_energy.setVisible(True)
                nd_energy.setOpacity(255)
                nd_energy.nd_useless.setVisible(True)
                nd_energy.lab_cd_time.setVisible(True)
            nd_energy.nd_useless.progress_cd.SetPercent(100 * (1.0 - energy_rate))
            recover_rate = self.mecha.ev_g_energy_recover(skill_const.SKILL_BALL_DASH)
            left_time_str = '{:.1f}'.format((1.0 - energy_rate) / recover_rate)
            nd_energy.lab_cd_time.SetString(left_time_str)
        elif energy_rate == 1.0 and nd_energy.isVisible():
            if self.panel.IsPlayingAnimation('enable'):
                return
            nd_energy.lab_cd_time.setVisible(False)
            self.panel.PlayAnimation('enable')
            self.panel.DelayCall(self.panel.GetAnimationMaxRunTime('enable'), lambda : self.panel.nd_sp2_cd.setVisible(False))
        else:
            nd_energy.setVisible(False)

    def on_skill_energy_changed(self, skill_id, energy_rate):
        if skill_id == skill_const.SKILL_FLAMETHROWER:
            self.on_flamethrower_energy_changed(energy_rate)
        elif skill_id == skill_const.SKILL_BALL_DASH:
            self.on_ball_dash_energy_changed(energy_rate)