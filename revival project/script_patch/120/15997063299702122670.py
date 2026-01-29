# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8018SubUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.common_const import mecha_const
from common.utils.timer import RELEASE
import logic.gcommon.const as g_const
from common.const import uiconst
MAX_SUB_WEAPON_PERCENT = 88
MIN_SUB_WEAPON_PERCENT = 62
SUB_WEAPON_PERCENT_GAP = MAX_SUB_WEAPON_PERCENT - MIN_SUB_WEAPON_PERCENT
MAX_RUSH_PERCENT = 75
MIN_RUSH_PERCENT = 62
RUSH_PERCENT_GAP = MAX_RUSH_PERCENT - MIN_RUSH_PERCENT
PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_mech_8018_rush.png',
 'gui/ui_res_2/battle/mech_attack/progress_mech_8018_rush_red.png']

class Mecha8018SubUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8018_2'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        self.clear_sub_weapon_timer()
        self.clear_rush_timer()
        return

    def disappear(self):
        self.close()

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self._target = None
        self.core_module_id = None
        self.sub_show_state = 0
        self.cur_sub_state = 0
        self.sub_weapon_max_duration = 1.0
        self.sub_weapon_duration = 0.0
        self.sub_weapon_timer = None
        self.rush_max_duration = 1.0
        self.rush_duration = 0.0
        self.rush_timer = None
        self.progress_pic = 0
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        self.on_camera_switch_to_state(global_data.cam_data.camera_state_type)
        self._on_module_changed()

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_START_SEQUENCESHOOT_8018', self.start_sequence_shoot)
            regist_func('E_START_RUSH_8018', self.start_rush)
            regist_func('E_SEQUENCE_SHOOT_8018_HOLD', self.show_hold)
            regist_func('E_NOTIFY_MODULE_CHANGED', self._on_module_changed)
            state, max_stage, left_time, max_duration = self.mecha.ev_g_sequence_shoot_8018_state() or (None,
                                                                                                        None,
                                                                                                        None,
                                                                                                        None)
            if state:
                self.cur_sub_state = state
                self.start_sequence_shoot(state, max_stage, left_time, max_duration)
            state, max_stage, left_time, max_duration = self.mecha.ev_g_rush_8018_state() or (None,
                                                                                              None,
                                                                                              None,
                                                                                              None)
            if state:
                self.start_rush(state, max_stage, left_time, max_duration)
        return None

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_START_SEQUENCESHOOT_8018', self.start_sequence_shoot)
            unregist_func('E_START_RUSH_8018', self.start_rush)
            unregist_func('E_SEQUENCE_SHOOT_8018_HOLD', self.show_hold)
            unregist_func('E_NOTIFY_MODULE_CHANGED', self._on_module_changed)
        self.mecha = None
        return

    def _on_module_changed(self):
        if self.player:
            module_item = self.player.ev_g_mecha_installed_module(mecha_const.SP_MODULE_SLOT)
            if not module_item:
                if self.core_module_id:
                    self.core_module_id = None
                    self.show_sub_ani(self.sub_show_state)
                return
            card_id, _ = module_item
            if card_id != self.core_module_id and self.sub_show_state:
                self.core_module_id = card_id
                self.show_sub_ani(self.sub_show_state)
            else:
                self.core_module_id = card_id
        return

    def reset_aim_ui(self):
        self.panel.PlayAnimation('disappear_sub_aim')
        self.sub_show_state = 0

    def show_sub_ani(self, show_state):
        self.sub_show_state = show_state
        if self.core_module_id == 801842:
            ani_name = 'show_sp_sub_%d' % (2 if show_state == 3 else 1)
        else:
            ani_name = 'show_sub_%d' % show_state
        self.panel.PlayAnimation(ani_name)

    def show_hold(self, state):
        if state == 1:
            self.show_sub_ani(state)

    def clear_sub_weapon_timer(self):
        if self.sub_weapon_timer:
            global_data.game_mgr.unregister_logic_timer(self.sub_weapon_timer)
        self.sub_weapon_timer = None
        return

    def start_sequence_shoot(self, state, max_stage, left_duration, max_duration):
        if left_duration <= 0:
            return
        self.cur_sub_state = state
        self.panel.lab_num_sub.SetString(str(max_stage - state))
        if state < 3:
            self.show_sub_ani(self.cur_sub_state + 1)
        elif state == 3:
            self.panel.prog_sub_left.stopAllActions()
            self.panel.PlayAnimation('disappear_sub')
            self.clear_sub_weapon_timer()
            self.cur_sub_state = 0
            self.sub_show_state = 0
            return
        self.panel.PlayAnimation('show_sub')
        self.sub_weapon_max_duration = max_duration
        self.sub_weapon_duration = left_duration
        self.clear_sub_weapon_timer()
        self.sub_weapon_timer = global_data.game_mgr.register_logic_timer(self.update_sub_weapon, interval=1, times=-1, timedelta=True)
        cur_percent = MIN_SUB_WEAPON_PERCENT + SUB_WEAPON_PERCENT_GAP * float(left_duration) / max_duration
        self.panel.prog_sub_left.SetPercentage(cur_percent)

    def update_sub_weapon(self, dt):
        if not (self.panel and self.panel.isValid()):
            return RELEASE
        self.sub_weapon_duration -= dt
        if self.sub_weapon_duration < 0.0:
            self.sub_weapon_duration = 0.0
        cur_percent = MIN_SUB_WEAPON_PERCENT + SUB_WEAPON_PERCENT_GAP * float(self.sub_weapon_duration) / self.sub_weapon_max_duration
        self.panel.prog_sub_left.SetPercentage(cur_percent)
        if self.sub_weapon_duration == 0.0:
            self.panel.PlayAnimation('disappear_sub')
            self.cur_sub_state = 0
            self.sub_show_state = 0
            return RELEASE

    def clear_rush_timer(self):
        if self.rush_timer:
            global_data.game_mgr.unregister_logic_timer(self.rush_timer)
        self.rush_timer = None
        return

    def start_rush(self, state, max_stage, left_duration, max_duration):
        if left_duration <= 0:
            return
        if state == 2:
            if self.panel:
                self.panel.prog_power.stopAllActions()
                self.panel.PlayAnimation('disappear_rush')
                self.clear_rush_timer()
            return
        self.panel.PlayAnimation('show_rush')
        self.rush_max_duration = max_duration
        self.rush_duration = left_duration
        self.clear_rush_timer()
        self.rush_timer = global_data.game_mgr.register_logic_timer(self.update_rush, interval=1, times=-1, timedelta=True)
        cur_percent = MIN_RUSH_PERCENT + RUSH_PERCENT_GAP * float(left_duration) / max_duration
        self.panel.prog_power.SetPercentage(cur_percent)
        self.refesh_rush_progress_show(cur_percent)

    def refesh_rush_progress_show(self, cur_percent):
        progress_pic = 1 if cur_percent <= MIN_RUSH_PERCENT + RUSH_PERCENT_GAP * 0.3 else 0
        if progress_pic != self.progress_pic:
            self.progress_pic = progress_pic
            self.panel.prog_power.SetProgressTexture(PROGRESS_PIC[progress_pic])

    def update_rush(self, dt):
        if not (self.panel and self.panel.isValid()):
            return RELEASE
        self.rush_duration -= dt
        if self.rush_duration < 0.0:
            self.rush_duration = 0.0
        cur_percent = MIN_RUSH_PERCENT + RUSH_PERCENT_GAP * float(self.rush_duration) / self.rush_max_duration
        self.panel.prog_power.SetPercentage(cur_percent)
        self.refesh_rush_progress_show(cur_percent)
        if self.rush_duration == 0.0:
            self.panel.PlayAnimation('disappear_rush')
            return RELEASE

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')