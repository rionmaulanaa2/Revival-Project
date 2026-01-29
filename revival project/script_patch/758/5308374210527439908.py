# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraCollisionChecker.py
from __future__ import absolute_import
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_CAMERA_INCLUDE
from logic.gutils.CameraHelper import is_posture_inherit_camera_type, rotate_by_center
from data.c_camera_const import CAMERA_COLL_RECOVER_SPEED
import math3d
import math
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
import device_compatibility
YZ_VECTOR = math3d.vector(0, 1, 1)
OFFSET_FOCUS_RAY_START = math3d.vector(0, 1 * NEOX_UNIT_SCALE, 0)
OFFSET_FOCUS_SHIFT_DOWN = math3d.vector(0, -2.0, 0)

class CameraCollisionChecker(object):

    def __init__(self):
        self.is_enable_collision_check = True
        self.focus_point = None
        self.default_pos = None
        self._to_visual_focus_length = 0
        self.last_collision = False
        self.check_vertical_col = True
        self._static_cols = []
        self._default_dist = 1.0
        self._long_z_near_half = 1.0
        self._v_fov = 0
        self._sweep_col = None
        return

    def destroy(self):
        self._sweep_col = None
        self._static_cols = []
        return

    def set_enable_collision_check(self, enable):
        self.is_enable_collision_check = enable

    def update_camera_config(self, default_pos, focus_point, cam):
        self.default_pos = default_pos
        self.focus_point = focus_point
        self._to_visual_focus_length = ((self.default_pos - self.focus_point) * YZ_VECTOR).length
        self.update_camera_fov(cam)

    def update_camera_fov(self, cam):
        unit_height = math.tan(math.radians(cam.fov / 2)) * 2.0
        unit_width = cam.aspect * unit_height
        self.half_h = unit_height / 2
        self.half_w = unit_width / 2
        self.init_static_test(cam)

    def init_static_test(self, cam):
        if abs(self._v_fov - cam.fov) < 5:
            return
        cal_fov = cam.fov
        self._v_fov = cal_fov
        default_dist = self._default_dist
        unit_height = default_dist * math.tan(math.radians(cal_fov / 2)) * 2.0
        unit_width = cam.aspect * unit_height
        half_h = unit_height / 2
        half_w = unit_width / 2
        self._long_z_near_half = max(half_w, half_h)
        d = default_dist
        import game3d
        if device_compatibility.IS_DX:
            self._size_factor = 4
        else:
            self._size_factor = 2.2
        self._sweep_size = math3d.vector(half_w * d * self._size_factor, d / 2.0 * self._size_factor, half_h * d * self._size_factor)
        col = collision.col_object(collision.BOX, self._sweep_size)
        self._sweep_col = col
        if device_compatibility.IS_DX:
            self._static_size_factor = 3
        else:
            self._static_size_factor = 2
        scale = self._static_size_factor
        self._static_cols = []
        col = collision.col_object(collision.BOX, math3d.vector(half_w * d * scale, d / 2.0 * scale, half_h * d * scale))
        self._static_cols.append(col)

    def test_rebuild_static_test(self):
        self.init_static_test(global_data.game_mgr.scene.active_camera)

    def check_collision(self, cam, cur_target_pos, need_collision_recover, cam_offset=None, org_mat=None):
        if not self.is_enable_collision_check:
            return
        if not cur_target_pos or not self.focus_point:
            return
        if self.focus_point.length < 0.001:
            return
        start_pos = self.focus_point + cur_target_pos
        if cam_offset:
            offset = cam_offset if 1 else math3d.vector(0, 0, 0)
            mat = org_mat or cam.world_rotation_matrix if 1 else org_mat
            end_pos = rotate_by_center(self.default_pos + cur_target_pos, start_pos, mat)
            coll_pos, ratio = self.get_collision_point(cur_target_pos, end_pos, mat, cam_offset)

            def set_coll_point_immediately--- This code section failed: ---

 113       0  LOAD_FAST             0  'to_coll_pos'
           3  POP_JUMP_IF_FALSE    28  'to 28'

 114       6  LOAD_GLOBAL           0  'global_data'
           9  LOAD_ATTR             1  'emgr'
          12  LOAD_ATTR             2  'camera_set_collision_slerp_target_pos_event'
          15  LOAD_ATTR             3  'emit'
          18  LOAD_ATTR             1  'emgr'
          21  CALL_FUNCTION_2       2 
          24  POP_TOP          
          25  JUMP_FORWARD          0  'to 28'
        28_0  COME_FROM                '25'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21

            if coll_pos:
                start_pos = math3d.vector(start_pos) - offset
                cur_ratio = (cam.world_position - start_pos).length / (end_pos - start_pos).length
                self.last_collision = True
                need_collision_recover or set_coll_point_immediately(coll_pos)
                return
            if ratio - cur_ratio <= 0.03:
                set_coll_point_immediately(coll_pos)
            elif ratio - cur_ratio > 0.03:
                cost_time = (coll_pos - cam.world_position).length / CAMERA_COLL_RECOVER_SPEED
                if cost_time > 0.05:
                    global_data.emgr.camera_set_collision_slerp_target_pos_event.emit(coll_pos, cost_time)
                else:
                    set_coll_point_immediately(coll_pos)
        elif self.last_collision:
            self.last_collision = False
            if not need_collision_recover:
                set_coll_point_immediately(end_pos)
            else:
                cost_time = (end_pos - cam.world_position).length / CAMERA_COLL_RECOVER_SPEED
                global_data.emgr.camera_set_collision_slerp_target_pos_event.emit(end_pos, cost_time)
        else:
            self.last_collision = False

    def get_collision_point_with_record(self, cur_target_pos, camera_pos, camera_rotate_matrix, cam_offset):
        coll_pos, ratio = self.get_collision_point(cur_target_pos, camera_pos, camera_rotate_matrix, cam_offset)
        if coll_pos:
            self.last_collision = True
        else:
            self.last_collision = False
        return (coll_pos, ratio)

    def get_collision_point(self, cur_target_pos, camera_pos, camera_rotate_matrix, cam_offset):
        scn = global_data.game_mgr.scene
        if not cur_target_pos or not self.focus_point:
            return (None, None)
        else:
            start_pos = self.focus_point + cur_target_pos
            org_start_pos = math3d.vector(start_pos)
            if cam_offset and cam_offset.length > 1:
                cam_offset_hor = math3d.vector(cam_offset)
                cam_offset_hor.y = 0
                start_pos -= cam_offset_hor
                cam_offset_ver = math3d.vector(cam_offset)
                cam_offset_ver.x = 0
                cam_offset_ver.z = 0
                res = self.coll_check_offset_helper(scn, start_pos, cam_offset_ver, OFFSET_FOCUS_SHIFT_DOWN.length)
                if res:
                    start_pos = res if 1 else start_pos
                    hit_f, point_f, normal_f, fraction_f, color_f, obj_f = scn.scene_col.hit_by_ray(org_start_pos - cam_offset, start_pos, 0, GROUP_CAMERA_INCLUDE, -1, collision.INCLUDE_FILTER)
                    if hit_f:
                        cam_offset_cp = math3d.vector(cam_offset)
                        offset = min(cam_offset_cp.length * 0.5, 5)
                        if cam_offset_cp.length > 1:
                            cam_offset_cp.normalize()
                            start_pos = point_f - cam_offset_cp * offset
                    end_pos = camera_pos
                if self.check_vertical_col:
                    skip_vertical_check = cam_offset and cam_offset.length > 1 and cam_offset.y < 0 or self.focus_point.y <= abs(OFFSET_FOCUS_SHIFT_DOWN.y)
                    offset = skip_vertical_check or math3d.vector(0, self.focus_point.y / 2.0, 0)
                    hit, point, normal, fraction, color, obj = scn.scene_col.hit_by_ray(cur_target_pos + offset, cur_target_pos + self.focus_point - OFFSET_FOCUS_SHIFT_DOWN, 0, GROUP_CAMERA_INCLUDE, -1, collision.INCLUDE_FILTER)
                    if hit:
                        start_pos = point + OFFSET_FOCUS_SHIFT_DOWN
            end_pos = camera_pos
            if (end_pos - start_pos).length <= 1e-05:
                return (None, None)
            pos_end_pos = end_pos
            pos_coll_pos = math3d.vector(end_pos)
            pos_ratio = 1
            org_offset = cam_offset if cam_offset else math3d.vector(0, 0, 0)
            if global_data.camera_collision_use_ray:
                pos_res = scn.scene_col.hit_by_ray(start_pos, pos_end_pos, 0, GROUP_CAMERA_INCLUDE, -1, collision.INCLUDE_FILTER)
                check_end_pos = pos_end_pos
            else:
                col_obj = self._sweep_col
                col_obj.rotation_matrix = camera_rotate_matrix
                col_obj.position = start_pos
                if cam_offset and scn.scene_col.static_test(col_obj):
                    end_2_start_vec = pos_end_pos - start_pos
                    if not end_2_start_vec.is_zero:
                        end_2_start_vec.normalize()
                    start_pos = start_pos + end_2_start_vec * self._long_z_near_half * 2
                end_2_start_vec_dir = pos_end_pos - start_pos
                if not end_2_start_vec_dir.is_zero:
                    end_2_start_vec_dir.normalize()
                check_end_pos = pos_end_pos + end_2_start_vec_dir * self._sweep_size.y
                pos_res = scn.scene_col.sweep_test(col_obj, start_pos, check_end_pos, GROUP_CAMERA_INCLUDE, GROUP_CAMERA_INCLUDE, 0, collision.INCLUDE_FILTER)
            if pos_res[0]:
                if global_data.camera_collision_use_ray:
                    pos_coll_pos = math3d.vector(pos_res[1])
                else:
                    fraction = pos_res[3]
                    fraction = max(0, fraction)
                    pos_coll_pos = start_pos + (check_end_pos - start_pos) * fraction
                pos_diff = org_start_pos - org_offset - pos_coll_pos
                all_len = (end_pos - org_start_pos + org_offset).length
                if all_len > 1e-05:
                    pos_ratio = pos_diff.length / all_len
            if pos_res[0]:
                return (pos_coll_pos, pos_ratio)
            test_pos = self.get_static_test_result(scn, camera_rotate_matrix, end_pos, start_pos)
            if test_pos:
                pos_diff2 = org_start_pos - org_offset - test_pos
                all_len = (end_pos - org_start_pos + org_offset).length
                if all_len > 1e-05:
                    pos_ratio2 = pos_diff2.length / all_len
                else:
                    pos_ratio2 = 1
                return (test_pos, pos_ratio2)
            return (None, None)
            return None

    def get_static_test_result(self, scn, camera_rotate_matrix, camera_pos, start_pos):
        rot_mat = camera_rotate_matrix
        view_dir = start_pos - camera_pos
        if not view_dir.is_zero:
            view_dir.normalize()
        for col_obj in self._static_cols:
            col_obj.rotation_matrix = rot_mat
            col_obj.position = camera_pos
            if scn.scene_col.static_test(col_obj):
                return camera_pos + view_dir * self._static_size_factor

        return None

    def set_vertical_checker(self, use):
        self.check_vertical_col = use

    def coll_check_offset_helper(self, scn, start_pos, offset_vec, min_offset_length=0):
        hit_f, point_f, normal_f, fraction_f, color_f, obj_f = scn.scene_col.hit_by_ray(start_pos - offset_vec, start_pos, 0, GROUP_CAMERA_INCLUDE, -1, collision.INCLUDE_FILTER)
        if hit_f:
            offset = min(offset_vec.length * 0.5, 3)
            if min_offset_length > 0 and offset_vec.y > 0:
                offset = max(offset, min_offset_length)
            if not offset_vec.is_zero:
                offset_vec.normalize()
                return point_f - offset_vec * offset
        return None

    def out_pos(self, pos):
        if pos:
            return '<%.2f, %.2f, %.2f>' % (pos.x, pos.y, pos.z)
        else:
            return str(None)