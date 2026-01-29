# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/HumanFireKeyboardMgr.py
from __future__ import absolute_import
from common.framework import Singleton

class HumanFireKeyboardMgr(Singleton):
    ALIAS_NAME = 'human_fire_keyboard_mgr'

    def init(self):
        self._fire_started = False
        self._check_fire_timer_id = None
        self._can_non_auto_shoot = False
        self._prev_auto_mode = None
        return

    def reset(self):
        self._stop_shot()

    def on_finalize(self):
        self._safe_remove_check_fire_timer()

    def _get_lplayer(self):
        if not global_data.player or not global_data.player.logic:
            return None
        else:
            return global_data.player.logic

    def process_input(self, _, msg):
        lplayer = self._get_lplayer()
        if not lplayer:
            self._safe_remove_check_fire_timer()
            return
        from logic.gutils.hot_key_utils import is_down_msg
        if is_down_msg(msg):
            from logic.comsys.battle.BattleUtils import can_fire
            if can_fire():
                is_mecha_trans = lplayer.ev_g_in_mecha('MechaTrans')
                is_mecha = lplayer.ev_g_in_mecha('Mecha')
                is_human = not (is_mecha or is_mecha_trans)
                if is_human:
                    self._can_non_auto_shoot = True
                    self._safe_remove_check_fire_timer()
                    from common.utils.timer import CLOCK, RELEASE

                    def timer_func():
                        from logic.gutils.hot_key_utils import is_hotkey_down
                        from data import hot_key_def
                        if not is_hotkey_down(hot_key_def.HUMAN_FIRE):
                            self._stop_shot()
                            return RELEASE
                        from logic.comsys.battle.BattleUtils import can_fire
                        if not can_fire():
                            self._stop_shot()
                            return RELEASE
                        self._try_start_shot()

                    self._check_fire_timer_id = global_data.game_mgr.register_logic_timer(timer_func, 0.1, times=-1, mode=CLOCK)
                    timer_func()
        else:
            self._stop_shot()

    def _try_start_shot(self):
        lplayer = self._get_lplayer()
        if not lplayer:
            return
        if self._check_camera_can_shot(lplayer):
            return
        cur_weapon_pos = lplayer.share_data.ref_wp_bar_cur_pos
        lplayer.send_event('E_IS_KEEP_DOWN_FIRE', True)
        from logic.gcommon.const import MAIN_WEAPON_LIST
        if cur_weapon_pos in MAIN_WEAPON_LIST:
            from logic.gcommon.cdata import status_config
            if lplayer.ev_g_status_check_pass(status_config.ST_SHOOT) and lplayer.ev_g_is_can_fire():
                auto_mode = lplayer.ev_g_is_weapon_in_auto_mode()
                auto_mode_changed = self._prev_auto_mode != auto_mode
                if auto_mode_changed:
                    from logic.gcommon.common_const import weapon_const
                    if auto_mode != weapon_const.AUTO_MODE:
                        self._can_non_auto_shoot = True
                if global_data.is_allow_sideways:
                    lplayer.send_event('E_START_FIRE_ROCKER')
                elif auto_mode:
                    if not lplayer.ev_g_is_auto_fire():
                        lplayer.send_event('E_START_AUTO_FIRE', right_mode=True)
                    self._fire_started = True
                elif self._can_non_auto_shoot:
                    lplayer.send_event('E_START_AUTO_FIRE', right_mode=True)
                    self._fire_started = True
                    self._can_non_auto_shoot = False
                self._prev_auto_mode = auto_mode

    def stop_shot(self):
        return self._stop_shot()

    def _stop_shot(self):
        self._safe_remove_check_fire_timer()
        if not self._fire_started:
            return
        self._fire_started = False
        lplayer = self._get_lplayer()
        if not lplayer:
            return
        lplayer.send_event('E_IS_KEEP_DOWN_FIRE', False)
        from logic.gcommon import const
        cur_weapon_pos = lplayer.share_data.ref_wp_bar_cur_pos
        from logic.gcommon.const import MAIN_WEAPON_LIST
        if cur_weapon_pos in MAIN_WEAPON_LIST:
            if global_data.is_allow_sideways:
                lplayer.send_event('E_END_FIRE_ROCKER')
            else:
                lplayer.send_event('E_STOP_AUTO_FIRE', right_mode=True)

    def _check_camera_can_shot(self, lplayer):
        from logic.comsys.control_ui.ShotChecker import ShotChecker
        return ShotChecker().check_camera_can_shot(lplayer)

    def _safe_remove_check_fire_timer(self):
        if self._check_fire_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._check_fire_timer_id)
        self._check_fire_timer_id = None
        return