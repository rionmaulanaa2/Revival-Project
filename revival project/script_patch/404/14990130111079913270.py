# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartArtCheckCamera.py
from __future__ import absolute_import
from .PartLobbyCamera import PartLobbyCamera
import math3d
import math
from common.cfg import confmgr
from logic.vscene.parts.camera.camera_controller import art_test_cam_ctrl, slerp_cam_ctrl
from logic.gutils.CameraHelper import get_adaptive_camera_fov
import math3d
from logic.vscene.parts.camera.SlerpCamera import SlerpCamera

class PartArtCheckCamera(PartLobbyCamera):
    INIT_EVENT = {'on_lobby_player_char_inited': 'on_character_inited',
       'movie_camera_prepare': 'on_movie_camera_prepare',
       'trigger_lobby_player_move': 'on_lobby_player_move',
       'rotation_camera_enable': 'on_rotation_camera_enable',
       'reset_lobby_camera_from_free': 'reset_lobby_camera_from_free',
       'net_reconnect_event': 'on_reconnect',
       'net_login_reconnect_event': 'on_reconnect',
       'resolution_changed': 'on_resolution_changed',
       'update_role_id': 'on_update_role_id',
       'change_camera_focus_and_distance': 'on_change_camera_focus_and_distance'
       }

    def __init__(self, scene, name):
        super(PartArtCheckCamera, self).__init__(scene, name)
        global_data.game_mgr.remove_patch_ui()

    def init_camera_ctrl(self):
        self.camera_ctrl = art_test_cam_ctrl.ArtTestCamCtrl()
        self.camera_ctrl.set_started(True)

    def on_update_role_id(self, role_id, is_mecha=False):
        if is_mecha:
            focus_vector = [
             0, 70]
            camera_distance = 150
        else:
            focus_vector = [
             0, 20]
            camera_distance = 40
        if self.camera_ctrl and hasattr(self.camera_ctrl, 'update_camera_focus_and_distance'):
            self.camera_ctrl.update_camera_focus_and_distance(focus_vector, camera_distance)

    def on_change_camera_focus_and_distance(self, focus, camera_distance):
        if self.camera_ctrl and hasattr(self.camera_ctrl, 'update_camera_focus_and_distance'):
            self.camera_ctrl.update_camera_focus_and_distance(focus, camera_distance)
            global_data.game_mgr.show_tip('\xe6\x9b\xb4\xe6\x8d\xa2\xe7\x9b\xb8\xe6\x9c\xba\xe5\x8f\x82\xe6\x95\xb0\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81')

    def on_touch_slide(self, dx, dy, touches, touch_pos):
        import math3d
        t_pos = math3d.vector2(touch_pos.x, touch_pos.y)
        dx, dy = self.modify_rotate_dist_by_sensitivity(dx, dy, t_pos)
        dx, dy = self.modify_sense_by_dist(dx, dy, t_pos)
        self.rotate_camera(dx, dy)
        if self.camera_ctrl:
            self.camera_ctrl.set_started(True)

    def on_lobby_player_move(self, vec):
        if self.camera_ctrl:
            self.camera_ctrl.set_started(True)

    def rotate_camera(self, dx, dy):
        if self.forbit_rotation_camera_count > 0:
            return
        if not self.camera_ctrl:
            return
        self._yaw = self._yaw + dx * self._delta_yaw_ratio
        self._pitch = min(max(self._pitch_range[0], self._pitch - dy * self._delta_pitch_ratio), self._pitch_range[1])
        global_data.emgr.trigger_lobby_player_set_yaw.emit(self._yaw)

    def reset_lobby_camera_from_free(self):
        rotation_matrix = None
        if global_data.lobby_player:
            rotation_matrix = global_data.lobby_player.ev_g_rotation_matrix()
        elif global_data.mecha:
            rotation_matrix = global_data.mecha.ev_g_rotation_matrix()
        if rotation_matrix is None:
            return
        else:
            yaw = rotation_matrix.yaw
            pitch = rotation_matrix.pitch
            self.update_cam()
            target_cam_info = self.camera_ctrl.get_lobby_cam_info(yaw, pitch)
            if not target_cam_info:
                self._yaw = yaw
                self._pitch = pitch
                self.init_camera_ctrl()
                return
            target_mat, head_pos = target_cam_info
            active_cam = self.scene().active_camera
            slerp_list = SlerpCamera._cal_spherical_track_point(active_cam.world_transformation, target_mat, head_pos, 10, 0.3)

            def slerp_end_callback(*args):
                self._yaw = yaw
                self._pitch = pitch
                self.init_camera_ctrl()
                if global_data.lobby_player:
                    ctrl_dir = global_data.lobby_player.ev_g_ctrl_dir()
                    global_data.lobby_player.send_event('E_CAMERA_SLERP_END')
                    if ctrl_dir and ctrl_dir.length > 0:
                        global_data.lobby_player.send_event('E_MOVE', ctrl_dir)

            self.camera_ctrl = slerp_cam_ctrl.SlerpCameraCtrl()
            cam = self.scene().active_camera
            self.camera_ctrl.set_slerp_list(cam.world_transformation, slerp_list, None, slerp_end_callback)
            return