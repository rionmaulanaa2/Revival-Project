# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/FreeflyNonAOICameraController.py
from __future__ import absolute_import
import six
import game
import world
import math3d
from logic.vscene.parts.keyboard.CameraDirectionKeyboardHelper import CameraDirectionKeyboardHelper
from common.framework import Singleton
import time
from .JudgeCameraController import CameraCollisionObject

class FreeflyNonAOICameraController(Singleton):

    def init(self):
        self._camera_direction_helper = CameraDirectionKeyboardHelper()
        self._is_enable = False
        self.update_timer_id = None
        self._cameraCollisionObject = None
        self._is_waiting_for_cam_entity = False
        self._last_disable_time = 0
        global_data.camera_freefly_speed = 2
        from data import hot_key_def
        self.quick_trk_key_list = {hot_key_def.JUDGE_CAMERA_FORWARD: game.VK_W,hot_key_def.JUDGE_CAMERA_BACKWARD: game.VK_S,
           hot_key_def.JUDGE_CAMERA_LEFT: game.VK_A,
           hot_key_def.JUDGE_CAMERA_RIGHT: game.VK_D,
           hot_key_def.JUDGE_CAMERA_UP: game.VK_NUM4,
           hot_key_def.JUDGE_CAMERA_DOWN: game.VK_NUM1
           }
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        self._is_need_col = False
        self._is_need_keyboard_ctrl = False
        return

    def switch_col(self, need_col):
        self._is_need_col = need_col

    def on_finalize(self):
        self.disable(is_destroy=True)
        self.stop_timer()
        self._camera_direction_helper.destroy()
        self._camera_direction_helper = None
        if self._cameraCollisionObject:
            self._cameraCollisionObject.destroy()
            self._cameraCollisionObject = None
        return

    def stop_timer(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = None
        return

    def check_can_enable(self):
        cur_time = time.time()
        if cur_time - self._last_disable_time < 1:
            global_data.game_mgr.show_tip(get_text_by_id(19603))
            return False
        return True

    def enable(self):
        self._camera_direction_helper.reset()
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.register_wheel_event(self.__class__.__name__, self.on_mouse_scroll)
        camera_pos = global_data.game_mgr.scene.active_camera.world_position
        from data.camera_state_const import JUDGE_MODE
        global_data.emgr.switch_camera_state_event.emit(JUDGE_MODE)
        self._is_enable = True
        self._is_waiting_for_cam_entity = False
        if global_data.player and global_data.player.logic:
            tid = global_data.player.logic.ev_g_spectate_target_id()
            if tid:
                global_data.emgr.set_observe_target_id_event.emit(None, True)
            else:
                global_data.emgr.scene_observed_player_setted_for_cam.emit(None, None, False)
        global_data.emgr.switch_cam_state_enable_event.emit(False)
        global_data.emgr.camera_switch_collision_check_event.emit(False)
        global_data.emgr.camera_added_trk_enable.emit(False)
        if self._is_need_col:
            if not self._cameraCollisionObject:
                camera_pos_tuple = [
                 camera_pos.x, camera_pos.y, camera_pos.z]
                self._cameraCollisionObject = CameraCollisionObject({'range': 10,'position': camera_pos_tuple})
        global_data.emgr.enable_target_pos_update_flag_event.emit(True)
        global_data.emgr.enable_special_target_pos_logic_for_judge.emit(True)
        global_data.emgr.set_target_pos_for_special_logic.emit(camera_pos)
        if self._is_need_col:
            if self._cameraCollisionObject:
                self._cameraCollisionObject.set_pos(camera_pos)
                self._cameraCollisionObject.set_col_on()
        from common.framework import Functor
        if global_data.pc_ctrl_mgr and self._is_need_keyboard_ctrl:
            for hotkey_func_name, mapped_key in six.iteritems(self.quick_trk_key_list):
                global_data.pc_ctrl_mgr.process_custom_key_binding(hotkey_func_name, Functor(self.on_quick_key, mapped_key=mapped_key), True)

        return

    def disable(self, is_destroy=False):
        if not self._is_enable:
            return
        else:
            if not is_destroy:
                if not self.check_can_recover_to_cam_player():
                    self._is_waiting_for_cam_entity = True
                    return
            self._is_waiting_for_cam_entity = False
            self._camera_direction_helper.reset()
            if self._is_need_col:
                if self._cameraCollisionObject:
                    self._cameraCollisionObject.move_collision(math3d.vector(0, 0, 0))
            self.stop_timer()
            touch_mgr = global_data.touch_mgr_agent
            touch_mgr.unregister_wheel_event(self.__class__.__name__)
            if global_data.player and global_data.player.logic:
                tid = global_data.player.logic.ev_g_spectate_target_id()
                if tid:
                    global_data.emgr.set_observe_target_id_event.emit(tid)
                else:
                    global_data.emgr.scene_observed_player_setted_for_cam.emit(global_data.player.logic, None, False)
                global_data.emgr.switch_cam_state_enable_event.emit(True)
                global_data.emgr.recover_observe_camera_event.emit()
                global_data.emgr.camera_switch_collision_check_event.emit(True)
                global_data.emgr.camera_added_trk_enable.emit(True)
            if global_data.cam_lplayer:
                global_data.emgr.set_target_pos_for_special_logic.emit(global_data.cam_lplayer.ev_g_position())
            global_data.emgr.enable_special_target_pos_logic_for_judge.emit(False)
            self._is_enable = False
            self._last_disable_time = time.time()
            if self._is_need_col:
                if self._cameraCollisionObject:
                    self._cameraCollisionObject.set_col_off()
            if global_data.pc_ctrl_mgr and self._is_need_keyboard_ctrl:
                for hotkey_func_name, mapped_key in six.iteritems(self.quick_trk_key_list):
                    global_data.pc_ctrl_mgr.process_custom_key_binding(hotkey_func_name, None, False)

            return

    def check_can_recover_to_cam_player(self):
        if global_data.player and global_data.player.logic:
            tid = global_data.player.logic.ev_g_spectate_target_id()
            if tid:
                from mobile.common.EntityManager import EntityManager
                ent = EntityManager.getentity(tid)
                if ent and ent.logic:
                    return True
            else:
                return True
        return False

    def is_enable(self):
        return self._is_enable

    def on_quick_key(self, msg, keycode, mapped_key):
        if msg == game.MSG_KEY_DOWN:
            self.on_quick_key_down(msg, mapped_key)
        else:
            self.on_quick_key_up(msg, mapped_key)

    def on_quick_key_down(self, msg, keycode):
        self._camera_direction_helper.move_key_func(msg, keycode)

    def on_quick_key_up(self, msg, keycode):
        self._camera_direction_helper.move_key_func(msg, keycode)

    def on_update(self):
        if self._is_waiting_for_cam_entity:
            if self.check_can_recover_to_cam_player():
                self.disable()
        if not self._is_enable:
            return
        move_dir = self._camera_direction_helper.get_move_direction()
        if move_dir and move_dir.length > 0.001:
            move_dir.normalize()
            if global_data.camera_freefly_speed:
                speed = global_data.camera_freefly_speed
            else:
                speed = 1.0
            speed_vec = move_dir * global_data.game_mgr.scene.active_camera.world_rotation_matrix * speed * 100
            if self._is_need_col:
                if self._cameraCollisionObject:
                    self._cameraCollisionObject.move_collision(speed_vec)
                    col_pos = self._cameraCollisionObject.get_pos()
                    if col_pos:
                        global_data.emgr.set_target_pos_for_special_logic.emit(col_pos)
            else:
                pos = global_data.game_mgr.scene.active_camera.world_position
                new_pos = pos + speed_vec
                global_data.emgr.set_target_pos_for_special_logic.emit(new_pos)
        elif self._is_need_col:
            if self._cameraCollisionObject:
                self._cameraCollisionObject.move_collision(math3d.vector(0, 0, 0))
                col_pos = self._cameraCollisionObject.get_pos()
                if col_pos:
                    global_data.emgr.set_target_pos_for_special_logic.emit(col_pos)

    def on_mouse_scroll(self, msg, delta, key_state):
        cur_speed = global_data.camera_freefly_speed
        if cur_speed is None:
            global_data.camera_freefly_speed = 2
        global_data.camera_freefly_speed += delta / 100.0
        global_data.camera_freefly_speed = min(max(1, global_data.camera_freefly_speed), 20.0)
        return

    def on_login_reconnect(self):
        if self._is_enable:
            self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)