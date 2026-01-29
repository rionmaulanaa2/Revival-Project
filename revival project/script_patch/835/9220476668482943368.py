# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/BunkerCheckHelper.py
from __future__ import absolute_import
import math3d
from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_INCLUDE
from logic.gcommon.const import NEOX_UNIT_SCALE
SW_RIGHT = POSTURE_RIGHT_SIDEWAYS
SW_LEFT = POSTURE_LEFT_SIDEWAYS
SW_UP = POSTURE_UP_SIDEWAYS
HOZ_VECTOR = math3d.vector(1, 0, 1)
FORWARD_DIR = math3d.vector(0, 0, 1)

def get_bunker_shot_world_offset(offset_dir):
    part_cam = global_data.game_mgr.scene.get_com('PartCamera')
    if not part_cam:
        return math3d.vector(0, 0, 0)
    cam = part_cam.cam
    if part_cam.is_in_cam_slerp():
        log_error('\xe5\x9c\xa8\xe9\x95\x9c\xe5\xa4\xb4\xe5\xb9\xb3\xe6\xbb\x91\xe8\xbf\x87\xe7\xa8\x8b\xe4\xb8\xad\xe8\xaf\x95\xe5\x9b\xbe\xe5\x81\x8f\xe7\xa7\xbb\xef\xbc\x8c\xe5\xbd\x93\xe5\x89\x8d\xe7\x9a\x84\xe5\x81\x8f\xe7\xa7\xbb\xe6\x98\xaf\xe5\xad\x98\xe5\x9c\xa8\xe9\x97\xae\xe9\xa2\x98\xe7\x9a\x84\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe7\x9b\xae\xe5\x89\x8d\xe7\x9a\x84\xe6\x9c\x9d\xe5\x90\x91\xe6\x98\xaf\xe4\xb8\x8d\xe5\x87\x86\xe7\xa1\xae\xe7\x9a\x84')
    from common.cfg import confmgr
    conf = confmgr.get('sideways_conf')
    if offset_dir == SW_RIGHT:
        offset_value = conf.get('RIGHT_SIDEWAYS_MOVE_OFFSET', 1) * NEOX_UNIT_SCALE
        dir = cam.world_rotation_matrix.right * HOZ_VECTOR
        dir.normalize()
        offset = dir * offset_value
    elif offset_dir == SW_LEFT:
        offset_value = conf.get('LEFT_SIDEWAYS_MOVE_OFFSET', 1) * NEOX_UNIT_SCALE
        dir = cam.world_rotation_matrix.right * HOZ_VECTOR
        dir.normalize()
        offset = dir * (offset_value * -1)
    else:
        from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND, POSTURE_SQUAT
        from common.cfg import confmgr
        conf = confmgr.get('camera_config', THIRD_PERSON_MODEL, default={})
        stand_focus_vector = conf.get(POSTURE_STAND, {}).get('focus', [0, 0, 0])
        squat_focus_vector = conf.get(POSTURE_SQUAT, {}).get('focus', [0, 0, 0])
        offset = math3d.vector(0, stand_focus_vector[1] - squat_focus_vector[1], 0)
    return offset


class FrameChecker(object):

    def __init__(self):
        self.exec_list = []

    def add(self, func):
        self.exec_list.append(func)

    def insert(self, index, func):
        self.exec_list.insert(index, func)

    def update(self):
        if len(self.exec_list) > 0:
            func = self.exec_list.pop(0)
            if callable(func):
                func()

    def clear(self):
        self.exec_list = []

    def is_empty(self):
        return len(self.exec_list) <= 0

    def destroy(self):
        self.clear()


class DirectionChecker(object):

    def __init__(self):
        self.scene = global_data.game_mgr.scene
        self.cam = self.scene.active_camera

    def destroy(self):
        self.start_socket = None
        self.scene = None
        self.cam = None
        return

    def check_collision(self, start_pos, dir):
        end_pos = start_pos + dir
        scn = self.scene
        coll_res = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, GROUP_CAMERA_INCLUDE, 0)
        return coll_res

    def check_cam_direction_from_camera(self, dist, yaw, pitch, height):
        start_position = self.cam.world_position
        start_position.y = height
        dir = self.rotate_by_axis(FORWARD_DIR, yaw, pitch)
        dir = dir * self.cam.world_transformation.rotation
        coll_res = self.check_collision(start_position, dir * dist)
        return coll_res

    def rotate_by_axis(self, dir, yaw, pitch):
        if pitch and yaw:
            mat = math3d.matrix.make_rotation_x(pitch) * math3d.matrix.make_rotation_y(yaw)
            dir = dir * mat
        elif pitch:
            mat = math3d.matrix.make_rotation_x(pitch)
            dir = dir * mat
        elif yaw:
            mat = math3d.matrix.make_rotation_y(yaw)
            dir = dir * mat
        return dir

    def check_cam_dir_ex(self, start_position, dist, yaw, pitch, is_world_rotate=True, show_debug_line=False):
        if not start_position:
            return (None, None, None, None, None, None)
        else:
            if not is_world_rotate:
                rot_mat = math3d.matrix.make_rotation_y(self.cam.world_transformation.rotation.yaw)
            else:
                rot_mat = math3d.matrix()
            dir = self.rotate_by_axis(FORWARD_DIR, yaw, pitch)
            dir = dir * rot_mat
            if show_debug_line:
                if hasattr(global_data, 'show_sideways_check_line') and global_data.show_sideways_check_line:
                    global_data.emgr.scene_draw_line_event.emit([start_position, start_position + dir * dist])
            coll_res = self.check_collision(start_position, dir * dist)
            return coll_res