# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaHpInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import HP_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.common_const.buff_const import BUFF_ID_MECHA_REDUCE_INJURE, BUFF_ID_MECHA_PARALYZE, BUFF_ID_MECAH_MAIN_WEAPON_UNABLE
from mobile.common.EntityManager import EntityManager
from common.utils.timer import CLOCK
from logic.gcommon.common_const.ui_battle_const import MECHA_HP_NORMAL_PERCENT, MECHA_HP_WARNING_PERCENT, HP_TAIL_SLOW_TIME, HP_CURE_SLOW_TIME
from logic.gutils import mecha_utils
ASSOCIATE_UI_LIST = [
 'HpInfoUI']
MIN_DELTA_PER_SEC = 20
from common.const import uiconst
MIN_CHANGE_DANGER_STATE_INTERVAL = 0.1

class MechaHpInfoBaseUI(BasePanel):
    DLG_ZORDER = HP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()

    def on_finalize_panel(self):
        timer_list = [
         'add_hp_timer', 'add_cure_timer', 'shorten_tail_timer', 'delay_change_danger_timer']
        for tname in timer_list:
            inst = getattr(self, tname, None)
            if inst:
                global_data.game_mgr.unregister_logic_timer(inst)
                setattr(self, tname, None)

        self.panel.temp_hp.stopAllActions()
        self.unbind_mecha_event()
        self.show_main_ui()
        self.player = None
        self.mecha = None
        return

    def enter_screen(self):
        super(MechaHpInfoBaseUI, self).enter_screen()
        emgr = global_data.emgr
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_observed_player_setted_event += self.on_player_setted
        self.init_parameters()
        self.init_event()
        self.hide_main_ui(ASSOCIATE_UI_LIST)

    def leave_screen(self):
        super(MechaHpInfoBaseUI, self).leave_screen()
        emgr = global_data.emgr
        emgr.scene_player_setted_event -= self.on_player_setted
        emgr.scene_observed_player_setted_event -= self.on_player_setted
        self.on_finalize_panel()

    def init_parameters(self):
        self.player = None
        self.bind_mecha_id = None
        self.hp_max = 0
        self.hp = 0
        self.shield_max = 0
        self.shield = 0
        self.outer_shield = 0
        self.cure_hp = 0
        self.in_danger = False
        self.unit_width = 0
        self.update_unit_width(mecha_utils.get_mecha_blood_unit_count())
        self.format_hp_max = 0
        self.format_shield_max = 0
        self.format_other_shield_max = 0
        self.format_hp = 0
        self.format_shield = 0
        self.hp_tail = 0
        self.shield_tail = 0
        self.cure_tail = 0
        self.add_hp_timer = None
        self.add_hp_per_tick = 0
        self.add_cure_timer = None
        self.cure_progress = 0
        self.add_cure_per_tick = 0
        self.shorten_tail_timer = None
        self.reduce_hp_per_tick = 0
        self.delay_change_danger_timer = None
        self.spectate_target = None
        if global_data.player and global_data.player.logic:
            self.spectate_target = global_data.player.logic.ev_g_spectate_target()
        if self.spectate_target and self.spectate_target.logic:
            self.on_player_setted(self.spectate_target.logic)
        elif global_data.player:
            self.on_player_setted(global_data.player.logic)
        self.panel.temp_hp.img_light.setVisible(False)
        self.panel.temp_hp.img_state.setVisible(False)
        self.last_change_danger_state_time = 0
        self.pve_fix = global_data.game_mode and global_data.game_mode.is_pve()
        if self.pve_fix:
            self.panel.temp_hp.middle.hp_tail.setVisible(False)
            self.panel.temp_hp.middle.hp_increase.setVisible(False)
        return

    def init_event(self):
        mecha_id = self.player.ev_g_get_bind_mecha()
        if mecha_id:
            mecha = EntityManager.getentity(mecha_id)
            if mecha and mecha.logic:
                mecha = mecha.logic
                self.mecha = mecha
                self.hp_max = mecha.share_data.ref_max_hp
                self.hp = mecha.share_data.ref_hp
                self.shield = mecha.ev_g_shield()
                self.shield_max = mecha.ev_g_max_shield()
                self.outer_shield = mecha.ev_g_outer_shield()
                self.format_hp = self.hp
                self.format_shield = self.shield
                self.other_shield = self.outer_shield
                self.hp_tail = self.hp
                self.cure_tail = self.hp
                self.shield_tail = self.shield
                self.other_shield_tail = self.outer_shield
                self.refresh_all_tail()
                self.check_in_danger(True)
                self.panel.temp_hp.lab_hp.SetString('%.0f' % (self.get_show_bar_value() * global_data.game_mode.get_mode_scale()))
                self.panel.temp_hp.lab_hp_full.SetString('/%.0f' % (self.get_show_bar_max_value() * global_data.game_mode.get_mode_scale()))

    def get_show_bar_value(self):
        return self.format_hp + self.format_shield + self.other_shield

    def get_show_bar_max_value(self):
        return self.hp_max + self.shield_max + self.other_shield

    def on_player_setted(self, player):
        self.player = player
        if not self.player:
            self.leave_screen()

    def on_mecha_setted(self, mecha):
        self.unbind_mecha_event()
        if mecha:
            self.bind_mecha_id = mecha.id
            regist_func = mecha.regist_event
            regist_func('E_HEALTH_HP_CHANGE', self.on_hp_changed)
            regist_func('E_MAX_HP_CHANGED', self.on_max_hp_changed)
            regist_func('E_SET_SHIELD', self.on_shield_changed)
            regist_func('E_SET_SHIELD_MAX', self.on_shield_max_changed)
            regist_func('E_SLOW_CURE_HP_CHANGE', self.on_cure_hp_changed)
            regist_func('E_OUTER_SHIELD_HP_CHANGED', self._on_outer_shield_changed)
            regist_func('E_ON_JOIN_MECHA', self.on_join_mecha)
            self.init_event()
            self.panel.temp_hp.PlayAnimation('appear')

    def unbind_mecha_event(self):
        if self.bind_mecha_id:
            mecha = EntityManager.getentity(self.bind_mecha_id)
            if mecha and mecha.logic:
                unregist_func = mecha.logic.unregist_event
                unregist_func('E_HEALTH_HP_CHANGE', self.on_hp_changed)
                unregist_func('E_MAX_HP_CHANGED', self.on_max_hp_changed)
                unregist_func('E_SET_SHIELD', self.on_shield_changed)
                unregist_func('E_SET_SHIELD_MAX', self.on_shield_max_changed)
                unregist_func('E_SLOW_CURE_HP_CHANGE', self.on_cure_hp_changed)
                unregist_func('E_OUTER_SHIELD_HP_CHANGED', self._on_outer_shield_changed)
                unregist_func('E_ON_JOIN_MECHA', self.on_join_mecha)
            self.bind_mecha_id = None
        return

    def on_join_mecha(self, *args):
        self.init_event()

    def on_shield_changed(self, shield, *args):
        if not self.mecha:
            return
        if shield > self.shield_max:
            return
        self.shield = shield
        self.update_format_shield(shield)
        if self.format_shield < self.shield_tail:
            self.display_reduce_anim()
        else:
            self.update_shield_tail(self.format_shield)

    def on_shield_max_changed(self, max_shield):
        if not self.mecha:
            return
        self.shield_max = max_shield
        self.panel.temp_hp.lab_hp_full.SetString('/%.0f' % (self.get_show_bar_max_value() * global_data.game_mode.get_mode_scale()))
        self.refresh_all_tail()

    def _on_outer_shield_changed(self, outer_shield_hp):
        if not self.mecha:
            return
        self.outer_shield = outer_shield_hp
        self.other_shield = self.outer_shield
        self.panel.temp_hp.lab_hp_full.SetString('/%.0f' % (self.get_show_bar_max_value() * global_data.game_mode.get_mode_scale()))
        if self.other_shield < self.other_shield_tail:
            self.display_reduce_anim()
        else:
            self.update_other_shield_tail(self.other_shield)

    def on_hp_changed(self, hp, mod=0):
        if not self.mecha:
            return
        self.hp = hp
        self.update_cure_tail(self.hp + self.cure_progress)
        if mod < 0:
            if self.hp < self.format_hp:
                self.update_format_hp(self.hp)
            if self.format_hp < self.hp_tail:
                self.display_reduce_anim()
        elif mod > 0 and self.format_hp < hp:
            self.display_add_hp_anim()
        self.check_in_danger()

    def on_cure_hp_changed(self, cure_hp, mod):
        if not self.mecha:
            return
        self.cure_hp = cure_hp
        if mod < 0 and self.cure_progress > self.cure_hp:
            self.cure_progress += mod
            self.update_cure_tail(self.cure_progress + self.hp)
        elif mod > 0 and self.cure_progress < self.cure_hp:
            self.display_add_cure_anim()

    def on_max_hp_changed(self, max_hp, hp, *args):
        if not self.mecha:
            return
        self.hp_max = max_hp
        self.hp = hp
        self.panel.temp_hp.lab_hp_full.SetString('/%.0f' % (self.get_show_bar_max_value() * global_data.game_mode.get_mode_scale()))
        self.refresh_all_tail()
        self.check_in_danger()

    def display_reduce_anim(self):
        shield_delta = self.shield_tail - self.format_shield
        hp_delta = self.hp_tail - self.format_hp
        other_shield_delta = self.other_shield_tail - self.other_shield
        total_delta = hp_delta + shield_delta + other_shield_delta
        self.reduce_hp_per_tick = max(total_delta / (HP_TAIL_SLOW_TIME * 30), MIN_DELTA_PER_SEC)
        self.panel.temp_hp.PlayAnimation('on_change')
        if not self.shorten_tail_timer:
            self.shorten_tail_timer = global_data.game_mgr.register_logic_timer(self.tick_reduce_hp, 0.0333, mode=CLOCK)

    def tick_reduce_hp(self):
        if self.shield_tail > self.format_shield:
            shield_tail = max(self.shield_tail - self.reduce_hp_per_tick, self.format_shield)
            self.update_shield_tail(shield_tail)
        elif self.hp_tail > self.format_hp:
            hp_tail = max(self.hp_tail - self.reduce_hp_per_tick, self.format_hp)
            self.update_hp_tail(hp_tail)
        elif self.other_shield_tail > self.other_shield:
            other_shield_tail = max(self.other_shield_tail - self.reduce_hp_per_tick, self.other_shield)
            self.update_other_shield_tail(other_shield_tail)
        if self.shield_tail <= self.format_shield and self.hp_tail <= self.format_hp and self.other_shield_tail <= self.other_shield:
            self.stop_shorten_tail_timer()

    def stop_shorten_tail_timer(self):
        if self.shorten_tail_timer:
            global_data.game_mgr.unregister_logic_timer(self.shorten_tail_timer)
            self.shorten_tail_timer = None
        return

    def display_add_hp_anim(self):
        self.add_hp_per_tick = max((self.hp - self.format_hp) / (HP_CURE_SLOW_TIME * 30), MIN_DELTA_PER_SEC)
        if not self.add_hp_timer:
            self.add_hp_timer = global_data.game_mgr.register_logic_timer(self.tick_add_hp, interval=0.033, mode=CLOCK)

    def tick_add_hp(self):
        format_hp = min(self.format_hp + self.add_hp_per_tick, self.hp)
        self.update_format_hp(format_hp)
        if self.format_hp > self.hp:
            self.stop_add_hp_timer()

    def stop_add_hp_timer(self):
        if self.add_hp_timer:
            global_data.game_mgr.unregister_logic_timer(self.add_hp_timer)
            self.add_hp_timer = None
        return

    def display_add_cure_anim(self):
        self.add_cure_per_tick = max((self.cure_hp - self.cure_progress) / (HP_CURE_SLOW_TIME * 30), MIN_DELTA_PER_SEC)
        if not self.add_cure_timer:
            self.add_cure_timer = global_data.game_mgr.register_logic_timer(self.tick_add_cure, interval=0.033, mode=CLOCK)

    def tick_add_cure(self):
        self.cure_progress = min(self.cure_progress + self.add_cure_per_tick, self.cure_hp)
        self.update_cure_tail(self.hp + self.cure_progress)
        if self.cure_progress >= self.cure_hp:
            self.stop_add_cure_timer()

    def stop_add_cure_timer(self):
        if self.add_cure_timer:
            global_data.game_mgr.unregister_logic_timer(self.add_cure_timer)
            self.add_cure_timer = None
        return

    def delay_check_change_danger_state(self):
        self.check_in_danger()
        self.delay_change_danger_timer = None
        return

    def check_in_danger(self, force=False):
        in_danger = self.hp < self.hp_max * 0.25
        if not force:
            if self.in_danger ^ in_danger:
                interval = global_data.game_time - self.last_change_danger_state_time
                if interval < MIN_CHANGE_DANGER_STATE_INTERVAL and not self.delay_change_danger_timer:
                    self.delay_change_danger_timer = global_data.game_mgr.register_logic_timer(self.check_in_danger, interval=MIN_CHANGE_DANGER_STATE_INTERVAL - interval, times=1, mode=CLOCK)
                    return
            else:
                return
        self.last_change_danger_state_time = global_data.game_time
        self.in_danger = in_danger
        if in_danger:
            self.panel.temp_hp.PlayAnimation('continue_danger')
            self.panel.temp_hp.img_backgroudn_light.setVisible(False)
            self.panel.temp_hp.hp_progress_dec.SetProgressTexture('gui/ui_res_2/battle/mech_main/hp_mech_danger.png')
            self.panel.temp_hp.hp_progress.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/mech_main/hp_mech_25.png')
            self.panel.temp_hp.img_light.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_main/hp_mech_top_red.png')
            self.panel.temp_hp.lab_hp.SetColor('#SR')
        else:
            self.panel.temp_hp.StopAnimation('continue_danger')
            self.panel.temp_hp.img_state.setVisible(False)
            self.panel.temp_hp.img_backgroudn_light.setVisible(True)
            self.panel.temp_hp.hp_progress_dec.SetProgressTexture('gui/ui_res_2/battle/mech_main/hp_mech_blue_light.png')
            self.panel.temp_hp.hp_progress.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/mech_main/hp_mech_100.png')
            self.panel.temp_hp.img_light.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_main/progress_shield_top.png')
            self.panel.temp_hp.lab_hp.SetColor('#DB')

    def set_progress_params(self, nd, hp, shield, other_shield):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_XBlood', hp)
        programState.setUniformFloat('_YBlood', shield)
        programState.setUniformFloat('_ZBlood', other_shield)

    def set_ratio_params(self, nd, max_hp, max_shield, max_other_shield):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_X', max_hp)
        programState.setUniformFloat('_Y', max_shield)
        programState.setUniformFloat('_Z', max_other_shield)

    def set_unit_params(self, nd, unit, scalar=0.5, gap_unit=None):
        programState = nd.getGLProgramState()
        programState.setUniformFloat('_Xinterval', unit / 2)
        programState.setUniformFloat('_Yinterval', 0)
        programState.setUniformFloat('_Scalar', scalar)
        if gap_unit is not None:
            programState.setUniformFloat('_Emptyinterval', gap_unit)
        return

    def update_unit_width(self, v):
        self.unit_width = v
        self.set_unit_params(self.panel.temp_hp.hp_tail, v)
        self.set_unit_params(self.panel.temp_hp.hp_increase, v)
        self.set_unit_params(self.panel.temp_hp.hp_progress, v)

    def update_format_hp(self, v):
        if v > self.hp_max:
            v = self.hp_max
        if self.format_hp == v:
            return
        self.format_hp = v
        if v > self.hp_tail:
            self.hp_tail = v
        self.refresh_all_tail()

    def update_format_shield(self, v):
        v = min(v, self.shield_max)
        self.format_shield = v
        if v > self.shield_tail:
            self.shield_tail = v
        self.refresh_all_tail()

    def update_hp_tail(self, v):
        if v < self.format_hp:
            v = self.hp_tail
        if self.hp_tail == v:
            return
        self.hp_tail = v
        self.refresh_all_tail()

    def update_cure_tail(self, v):
        if v > self.hp_max:
            v = self.hp_max
        if self.cure_tail == v:
            return
        self.cure_tail = v
        self.refresh_all_tail()

    def update_shield_tail(self, v):
        if v < self.format_shield:
            v = self.format_shield
        if self.shield_tail == v:
            return
        self.shield_tail = v
        self.refresh_all_tail()

    def update_other_shield_tail(self, v):
        if v < self.other_shield:
            v = self.other_shield
        if self.other_shield_tail == v:
            return
        self.other_shield_tail = v
        self.refresh_all_tail()

    def refresh_all_tail(self):
        panel = self.panel
        hp_max = max(self.hp_tail, self.cure_tail)
        shield_max = self.format_shield
        other_shield_max = self.hp_max + self.shield_max + self.other_shield - hp_max - shield_max
        shield_max_for_increase = self.shield_max + self.other_shield
        other_shield_max_for_increase = self.hp_max + self.shield_max + self.other_shield - hp_max - shield_max_for_increase
        if self.format_hp_max != hp_max or self.format_shield_max != shield_max or self.format_other_shield_max != other_shield_max:
            self.format_hp_max = hp_max
            self.format_shield_max = shield_max
            self.format_other_shield_max = other_shield_max
            self.set_ratio_params(panel.temp_hp.hp_progress, hp_max, shield_max, other_shield_max)
            self.set_ratio_params(panel.temp_hp.hp_tail, hp_max, shield_max, other_shield_max)
            self.set_ratio_params(panel.temp_hp.hp_increase, hp_max, shield_max_for_increase, other_shield_max_for_increase)
        self.set_progress_params(panel.temp_hp.hp_progress, self.format_hp, self.format_shield, self.other_shield)
        self.set_progress_params(panel.temp_hp.hp_tail, self.hp_tail, self.shield_tail, self.other_shield_tail)
        self.set_progress_params(panel.temp_hp.hp_increase, self.cure_tail, max(self.shield_tail, self.shield_max) + self.other_shield, 0)
        self.panel.temp_hp.lab_hp.SetString('%.0f' % (self.get_show_bar_value() * global_data.game_mode.get_mode_scale()))
        self.modify_cursor()

    def modify_cursor(self):
        total = float(self.format_hp_max + self.format_shield_max + self.format_other_shield_max) / 100
        if self.other_shield > 0:
            percentage = self.format_hp_max + self.format_shield_max + self.other_shield
        else:
            percentage = self.format_hp_max + self.format_shield if self.format_shield > 0 else self.format_hp
        percentage /= total
        self.panel.temp_hp.hp_progress_dec.setPercentage(0.93 * percentage + 3.5)
        if self.other_shield > 0:
            percentage = self.format_hp_max + self.format_shield_max + self.other_shield
        else:
            percentage = self.format_hp_max + self.format_shield if self.shield_tail >= self.format_shield else self.format_hp
        percentage /= total
        self.panel.temp_hp.img_light.SetPosition('%.2f%%' % percentage, '50%')
        self.panel.temp_hp.img_light.setVisible(1.5 < percentage < 99)

    def test(self):
        a = global_data.ui_mgr.get_ui('MechaHpInfoUI')
        a._on_outer_shield_changed(100)
        a.on_hp_changed(2000)


class MechaHpInfoUI(MechaHpInfoBaseUI):
    PANEL_CONFIG_NAME = 'battle_mech/hp_mech'