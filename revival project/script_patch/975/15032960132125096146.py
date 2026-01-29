# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/lobby_cam_ctrl.py
from __future__ import absolute_import
from .camctrl_base import CameraCtrl
import math3d
from common.cfg import confmgr
import math
import world
from logic.gcommon.common_const import collision_const
import collision
import common.utilities

class LobbyCamCtrl(CameraCtrl):

    def init(self):
        super(LobbyCamCtrl, self).init()
        self._camera_config = confmgr.get('mecha_display', 'LobbyCameraConfig', 'Content')['1']
        self._focus_vector = self._camera_config['focus']['other']
        self._camera_distance = self._camera_config['distance']['other']
        self._init_camera_yaw = 2.0
        self._has_started = False
        self._trans_lock_time = 1.0
        self._cur_trans_lock_time = -1
        self.init_col_test()

    def update_camera_focus_and_distance(self, focus_vector, camera_distance):
        self._focus_vector = focus_vector
        self._camera_distance = camera_distance

    def on_finalize(self):
        self._sweep_col = None
        return

    def init_col_test(self):
        default_dist = 1.0
        fov = 60
        import game3d
        import device_compatibility
        orig_width, orig_height, _, _, _ = game3d.get_window_size()
        unit_height = default_dist * math.tan(math.radians(fov / 2)) * 2.0
        unit_width = float(orig_width) / orig_height * unit_height
        half_h = unit_height / 2
        half_w = unit_width / 2
        d = default_dist
        if device_compatibility.IS_DX:
            _size_factor = 1.8
        else:
            _size_factor = 1.3
        col = collision.col_object(collision.BOX, math3d.vector(half_w * d * _size_factor, half_h * d * _size_factor, d / 2.0 * _size_factor))
        self._sweep_col = col

    def set_started(self, flag):
        old_flag = self._has_started
        self._has_started = flag
        if not old_flag:
            self._cur_trans_lock_time = self._trans_lock_time

    def get_lobby_cam_info(self, yaw, pitch):
        lobby_player = global_data.lobby_player
        if not lobby_player:
            return
        char_ctrl = lobby_player.share_data.ref_character
        if not char_ctrl:
            return
        return self.get_cam_info_by_pos(char_ctrl.position, yaw, pitch)

    def get_cam_info_by_pos(self, pos, yaw, pitch):
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
        lobby_player = global_data.lobby_player
        if not lobby_player:
            return
        char_ctrl = lobby_player.share_data.ref_character
        if not char_ctrl:
            return
        self.on_update_by_pos(dt, char_ctrl.position, yaw, pitch)

    def on_update_by_pos(self, dt, pos, yaw, pitch):
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

    def collision_check(self, scn, camera_pos, rot_mat, head_pos):
        collision_direction = head_pos - camera_pos
        dist = collision_direction.length
        if dist < 0.01:
            return camera_pos
        else:
            if not collision_direction.is_zero:
                collision_direction.normalize()
            col_obj = self._sweep_col
            col_obj.position = camera_pos
            col_obj.rotation_matrix = rot_mat
            res = scn.scene_col.sweep_test(col_obj, head_pos, camera_pos, collision_const.GROUP_CAMERA_INCLUDE, collision_const.GROUP_CAMERA_INCLUDE, 0, collision.INCLUDE_FILTER)
            MIN_DISTANCE = 7
            if res[0]:
                fraction = res[3]
                pos_coll_pos = head_pos
                if dist > 0:
                    fraction = max(0, fraction)
                    vec = (camera_pos - head_pos) * fraction
                    if vec.length < MIN_DISTANCE:
                        vec = collision_direction * MIN_DISTANCE * -1
                    pos_coll_pos = head_pos + vec
                return pos_coll_pos
            return camera_pos