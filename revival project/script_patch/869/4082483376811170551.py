# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/MoveKeyboardMgr.py
from __future__ import absolute_import
import game
from logic.client.const import camera_const
from logic.vscene.parts.keyboard.DirectionKeyboardHelper import DirectionKeyboardHelper
import math3d
import math
from logic.client.const.rocker_const import KEEP_RUNNING_ANGLE, RUNNING_ANGLE
from logic.gcommon.cdata import mecha_status_config as mecha_st_const
from logic.gcommon.cdata import status_config as st_const
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.common_const.animation_const import MOVE_STATE_WALK, MOVE_STATE_RUN
import logic.gcommon.common_const.animation_const as animation_const
from common.framework import Singleton
from logic.gutils.hot_key_utils import hot_key_func_to_hot_key, is_down_msg
from data import hot_key_def
import time
from common.utils.timer import CLOCK

class MoveKeyboardMgr(Singleton):
    ALIAS_NAME = 'moveKeyboardMgr'
    DIRECTION_KEYS = [
     game.VK_W, game.VK_S, game.VK_A, game.VK_D]

    def init(self):
        self.direction_keyboard_helper = DirectionKeyboardHelper()
        self._cur_md_dir = None
        self._accelerate_key = game.VK_SHIFT
        run_key = hot_key_func_to_hot_key(hot_key_def.RUN)
        if run_key is not None:
            self._accelerate_key = run_key
        self.move_msg_timer = None
        self.last_move_dir = None
        self._force_run = False
        self._is_run_switch_on = True
        self._run_switch_toggle_key = 10000
        self.last_move_state = animation_const.MOVE_STATE_STAND
        self.check_valid_run_md_dir()
        self._accelerate_key_down_time = 0
        self._press_need_time = 0.2
        self._press_timer_id = None
        return

    def on_finalize(self):
        self.destroy()

    def reset(self):
        if self.direction_keyboard_helper:
            self.direction_keyboard_helper.reset()
        self._cur_md_dir = None
        self.last_move_dir = None
        self.last_move_state = animation_const.MOVE_STATE_STAND
        return

    def destroy(self):
        self.remove_move_timer()
        self.direction_keyboard_helper = None
        if self._press_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._press_timer_id)
            self._press_timer_id = None
        return

    def toggle_move_rocker_lock_shortcut_wrapper(self, keycode, msg):
        if not (global_data.player and global_data.player.logic):
            return
        if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
            self.toggle_move_lock()

    def toggle_move_lock(self):
        if self.is_move_locked():
            self.stop_move_lock()
        else:
            self.start_move_lock()

    def is_move_locked(self):
        return self._force_run

    def start_move_lock(self):
        if self.is_move_locked():
            return
        self.process_input(game.VK_W, game.MSG_KEY_DOWN, skip_claim_shortcut_logic=True)
        self._force_run = True
        self.process_input(self._accelerate_key, game.MSG_KEY_DOWN, skip_claim_shortcut_logic=True)

    def stop_move_lock(self):
        if not self.is_move_locked():
            return
        if not global_data.is_key_down(game.VK_W):
            self.process_input(game.VK_W, game.MSG_KEY_UP, skip_claim_shortcut_logic=True)
        self._force_run = False
        self.process_input(self._accelerate_key, game.MSG_KEY_UP, skip_claim_shortcut_logic=True)

    def _check_need_run(self):
        if (self._force_run or self._is_run_switch_on) and self._cur_md_dir in self.valid_run_index_list:
            return True
        return False

    def _check_need_run_mecha(self, mecha):
        if (self._force_run or self._is_run_switch_on) and (self._cur_md_dir in self.valid_run_index_list or mecha.sd.ref_support_all_direction_run):
            return True
        return False

    def set_run_switch_state(self, on):
        if on is None:
            return
        else:
            self._is_run_switch_on = on
            global_data.emgr.run_switch_state_changed_event.emit(self._is_run_switch_on)
            return

    def get_run_switch_state(self):
        return self._is_run_switch_on

    def start_acc_process_input(self, keycode, msg, skip_claim_shortcut_logic=False):
        if keycode != self._accelerate_key:
            return
        else:

            def press_callback():
                self._press_timer_id = None
                self.set_run_switch_state(True)
                self.process_input(self._run_switch_toggle_key, game.MSG_KEY_DOWN, skip_claim_shortcut_logic)
                return

            if msg == game.MSG_KEY_DOWN:
                self._accelerate_key_down_time = time.time()
                self._press_timer_id = global_data.game_mgr.register_logic_timer(press_callback, interval=self._press_need_time, times=1, mode=CLOCK)
            elif not self._press_timer_id:
                self.process_input(self._run_switch_toggle_key, game.MSG_KEY_DOWN)
            else:
                global_data.game_mgr.unregister_logic_timer(self._press_timer_id)
                self._press_timer_id = None
                self.set_run_switch_state(not self.get_run_switch_state())
                self.process_input(self._run_switch_toggle_key, game.MSG_KEY_DOWN)
            return

    def process_input(self, keycode, msg, skip_claim_shortcut_logic=False):
        if not (global_data.player and global_data.player.logic):
            return
        else:
            player = global_data.player.logic
            if keycode == self._accelerate_key or self._run_switch_toggle_key is not None and keycode == self._run_switch_toggle_key and msg == game.MSG_KEY_DOWN:
                if self._cur_md_dir is not None:
                    from logic.gutils.move_utils import can_move
                    if not can_move():
                        return
                    player.send_event('E_SET_ROCKER_MOVE_DIST', 110)
                    if self.check_move_vehicle(player):
                        return
                    if self.check_move_mecha(player, self._cur_md_dir):
                        return
                    is_in_run, is_in_walk = self._check_walk_or_run(player)
                    if is_in_run or is_in_walk:
                        move_dir = camera_const.DIR_VECS[self._cur_md_dir]
                        if player.__class__.__name__ == 'LAvatar':
                            player.send_event('E_MOVE', move_dir)
                        player.send_event('E_MOVE_ROCK', move_dir, is_in_run)
                return
            if not self.direction_keyboard_helper:
                return
            need_update = self.direction_keyboard_helper.key_handler_hepler(msg, keycode, skip_claim_shortcut_logic)
            if not need_update:
                return
            md = self.direction_keyboard_helper.get_md_dir()
            if md is not None:
                self._cur_md_dir = md
                from common.utils.timer import CLOCK

                def try_send_move_message():
                    from logic.gutils.move_utils import can_move
                    if not can_move():
                        return
                    player.send_event('E_SET_ROCKER_MOVE_DIST', 110)
                    if self.check_move_drone(player, camera_const.DIR_VECS[md]):
                        return
                    if self.check_move_vehicle(player):
                        return
                    if self.check_move_mecha(player, md):
                        return
                    is_in_run, is_in_walk = self._check_walk_or_run(player)
                    move_dir = camera_const.DIR_VECS[md]
                    player.send_event('E_MOVE_ROCK_STATE', True)
                    player.send_event('E_MOVE_ROCK', move_dir, is_in_run)
                    if is_in_run or is_in_walk:
                        if player.__class__.__name__ == 'LAvatar':
                            player.send_event('E_MOVE', move_dir)
                        self.last_move_dir = move_dir

                self.remove_move_timer()
                self.move_msg_timer = global_data.game_mgr.register_logic_timer(lambda : try_send_move_message(), 0.1, times=-1, mode=CLOCK)
                try_send_move_message()
            else:
                player.send_event('E_ROCK_STOP')
                self._cur_md_dir = None
                self.last_move_dir = None
                self.last_move_state = animation_const.MOVE_STATE_STAND
                player.send_event('E_SET_ROCKER_MOVE_DIST', 110)
                self.check_stop_vehicle(player)
                self.check_move_drone(player)
                self.check_move_mecha(player)
                self.remove_move_timer()
            return

    def check_move_vehicle(self, player):
        from logic.gcommon.common_const import mecha_const
        if player.ev_g_get_state(st_const.ST_MECHA_DRIVER):
            ctrl_target = player.ev_g_control_target()
            if ctrl_target and ctrl_target.logic.ev_g_pattern() == mecha_const.MECHA_TYPE_VEHICLE:
                drive_ui = global_data.ui_mgr.get_ui('DriveUI')
                if drive_ui:
                    keycode_list = self.direction_keyboard_helper.get_total_keycodes()
                    for keycode in self.DIRECTION_KEYS:
                        if keycode in keycode_list:
                            drive_ui.on_keyboard_ctrl_change(keycode, game.MSG_KEY_DOWN)
                        else:
                            drive_ui.on_keyboard_ctrl_change(keycode, game.MSG_KEY_UP)

                return True
        return False

    def check_move_drone(self, player, md=None):
        if player:
            ctrl_target = player.ev_g_control_target()
            if ctrl_target and ctrl_target.__class__.__name__ == 'Drone':
                if md:
                    ctrl_target.logic.send_event('E_MOVE', md)
                else:
                    ctrl_target.logic.send_event('E_ROCK_STOP')
                return True
        return False

    def check_move_mecha(self, player, md=None):
        if player:
            ctrl_target = player.ev_g_control_target()
            if ctrl_target and ctrl_target.logic and ctrl_target.logic.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
                if md is not None:
                    ctrl_target.logic.send_event('E_SET_ROCKER_MOVE_DIST', 110)
                    is_in_run, is_in_walk, wanna_run = self._mecha_check_walk_or_run(ctrl_target.logic)
                    move_dir = camera_const.DIR_VECS[md]
                    if is_in_run or is_in_walk:
                        self.last_move_dir = move_dir
                    ctrl_target.logic.send_event('E_MOVE_ROCK', move_dir, wanna_run)
                else:
                    ctrl_target.logic.send_event('E_ROCK_STOP')
                return True
        return False

    def check_stop_vehicle(self, player):
        from logic.gcommon.common_const import mecha_const
        if player.ev_g_get_state(st_const.ST_MECHA_DRIVER):
            ctrl_target = player.ev_g_control_target()
            if not (ctrl_target and ctrl_target.logic):
                return
            ctrl_target.logic.send_event('E_ROCK_STOP')
            if ctrl_target.logic.ev_g_pattern() == mecha_const.MECHA_TYPE_VEHICLE:
                drive_ui = global_data.ui_mgr.get_ui('DriveUI')
                if drive_ui:
                    for keycode in self.DIRECTION_KEYS:
                        drive_ui.on_keyboard_ctrl_change(keycode, game.MSG_KEY_UP)

    def _check_walk_or_run(self, lplayer):
        import game
        if not lplayer:
            return (False, False)
        else:
            is_can_run = lplayer.ev_g_status_check_pass(st_const.ST_RUN) and self._cur_md_dir in self.valid_run_index_list
            is_can_walk = lplayer.ev_g_status_check_pass(st_const.ST_MOVE)
            is_in_run = False
            is_in_walk = False
            if is_can_run or is_can_walk:
                if lplayer.ev_g_parachute_follow_target() is not None:
                    is_can_run = False
                    is_can_walk = False
            if self._check_need_run():
                if is_can_run:
                    is_in_run = True
                elif is_can_walk:
                    is_in_walk = True
                self.last_move_state = MOVE_STATE_RUN
            elif is_can_walk:
                is_in_walk = True
                self.last_move_state = MOVE_STATE_WALK
            return (is_in_run, is_in_walk)

    def _mecha_check_walk_or_run(self, mecha):
        if not mecha:
            return (False, False, False)
        import game
        import logic.gcommon.common_const.robot_animation_const as robot_animation_const
        is_can_run = mecha.ev_g_status_check_pass(mecha_st_const.MC_RUN) and (self._cur_md_dir in self.valid_run_index_list or mecha.sd.ref_all_support_all_direction_run)
        is_can_walk = mecha.ev_g_status_check_pass(mecha_st_const.MC_MOVE)
        is_in_run = False
        is_in_walk = False
        wanna_run = self._check_need_run_mecha(mecha)
        if wanna_run:
            if is_can_run:
                mecha.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_RUN)
                is_in_run = True
            elif is_can_walk:
                mecha.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
                is_in_walk = True
            self.last_move_state = robot_animation_const.MOVE_STATE_RUN
        elif is_can_walk:
            mecha.send_event('E_SET_SPEED_STATUS', robot_animation_const.MOVE_STATE_WALK)
            is_in_walk = True
            self.last_move_state = robot_animation_const.MOVE_STATE_WALK
        return (is_in_run, is_in_walk, wanna_run)

    def check_valid_run_md_dir(self):
        up_vector = (0, 0, 1)
        valid_run_index_list = []
        for d_idx, m_dir in enumerate(camera_const.DIR_VECS):
            angle = math.acos(min(max(m_dir.x * up_vector[0] + m_dir.z * up_vector[2], -1), 1))
            if angle <= RUNNING_ANGLE / 2.0:
                valid_run_index_list.append(d_idx)

        self.valid_run_index_list = valid_run_index_list

    def remove_move_timer(self):
        if self.move_msg_timer:
            tm = global_data.game_mgr.get_logic_timer()
            if self.move_msg_timer:
                tm.unregister(self.move_msg_timer)
            self.move_msg_timer = None
        return