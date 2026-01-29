# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/art_test_cam_ctrl.py
from __future__ import absolute_import
from .lobby_cam_ctrl import LobbyCamCtrl
import math3d
from common.cfg import confmgr
import math
import world
from logic.gcommon.common_const import collision_const
import collision

class ArtTestCamCtrl(LobbyCamCtrl):

    def get_lobby_cam_info(self, yaw, pitch):
        pos = None
        if global_data.lobby_player:
            pos = global_data.lobby_player.ev_g_foot_position()
        elif global_data.mecha:
            pos = global_data.mecha.ev_g_foot_position()
        if pos is None:
            return
        else:
            scn = world.get_active_scene()
            head_pos = pos + math3d.vector(0, 1, 0) * self._focus_vector[1]
            x_rotate = math3d.matrix.make_rotation_x(pitch)
            y_rotate = math3d.matrix.make_rotation_y(yaw)
            rot_mat = x_rotate * y_rotate
            follow_pos = head_pos + rot_mat.right * self._focus_vector[0]
            camera_pos = -rot_mat.forward * self._camera_distance + follow_pos
            camera_pos = self.collision_check(scn, camera_pos, rot_mat, head_pos)
            target_matrix = math3d.matrix()
            target_matrix.do_rotation(rot_mat)
            target_matrix.do_translate(camera_pos)
            return (
             target_matrix, head_pos)

    def on_update(self, dt, yaw, pitch):
        pos = None
        if global_data.lobby_player:
            pos = global_data.lobby_player.ev_g_foot_position()
        elif global_data.mecha:
            pos = global_data.mecha.ev_g_foot_position()
        if pos is None:
            return
        else:
            import common.utilities
            scn = world.get_active_scene()
            camera = scn.active_camera
            camera_distance = self._camera_distance
            if not self._has_started:
                init_camera_info = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'init_camera')
                rot_mat = math3d.matrix.make_rotation_x(init_camera_info['pitch']) * math3d.matrix.make_rotation_y(init_camera_info['yaw'])
                camera.world_position = math3d.vector(init_camera_info['x'], init_camera_info['y'], init_camera_info['z'])
                camera.world_rotation_matrix = rot_mat
            else:
                head_pos = pos + math3d.vector(0, 1, 0) * self._focus_vector[1]
                if self._cur_trans_lock_time < 0.0:
                    x_rotate = math3d.matrix.make_rotation_x(pitch)
                    y_rotate = math3d.matrix.make_rotation_y(yaw)
                    rot_mat = x_rotate * y_rotate
                else:
                    self._cur_trans_lock_time -= dt
                    percent = abs(self._trans_lock_time - self._cur_trans_lock_time) / self._trans_lock_time
                    percent = math.sin(math.pi * 0.5 * percent)
                    cur_vec = camera.world_position - head_pos
                    camera_distance = common.utilities.lerp(float(cur_vec.length), camera_distance, percent)
                    pi2 = math.pi * 2.0
                    cur_euler = math3d.rotation_to_euler(math3d.matrix_to_rotation(camera.world_rotation_matrix.rotation))
                    nor_cur_euler_y = cur_euler.y % pi2
                    nor_yaw = yaw % pi2
                    lerp_yaw = common.utilities.lerp(nor_cur_euler_y, nor_yaw, percent)
                    rot_mat = math3d.matrix.make_rotation_x(pitch * percent) * math3d.matrix.make_rotation_y(lerp_yaw)
                follow_pos = head_pos + rot_mat.right * self._focus_vector[0]
                camera_pos = -rot_mat.forward * camera_distance + follow_pos
                camera_pos = self.collision_check(scn, camera_pos, rot_mat, head_pos)
                camera.world_position = camera_pos
                camera.world_rotation_matrix = rot_mat
            transform = camera.transformation
            global_data.sound_mgr.set_3d_listener(transform.translation, transform.forward, transform.up)
            return