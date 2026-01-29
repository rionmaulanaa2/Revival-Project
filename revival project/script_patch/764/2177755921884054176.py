# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartModelDisplayFollowCamera.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import math
from common.cfg import confmgr
from logic.vscene.parts.camera.camera_controller import lobby_cam_ctrl, model_display_cam_ctrl_new, lobby_circle_cam_ctrl
from logic.gutils.CameraHelper import get_adaptive_camera_fov
import world
from logic.vscene.parts.camera.camera_controller.lobby_circle_cam_ctrl import LobbyCircleCamCtrl
from logic.vscene.parts.PartModelDisplayCamera import PartModelDisplayCamera

class PartModelDisplayFollowCamera(PartModelDisplayCamera):
    ENTER_EVENT = dict(PartModelDisplayCamera.ENTER_EVENT)
    ENTER_EVENT.update({'update_display_camera_target_position': 'on_update_camera_target_position',
       'update_display_camera_parameter': 'on_update_camera_target_parameter'
       })

    def __init__(self, scene, name):
        super(PartModelDisplayCamera, self).__init__(scene, name, False)
        self._camera_key = 'item_books'
        self.init_data()
        self.init_event()
        self.camera_ctrl = LobbyCircleCamCtrl()
        self.need_update_distance_dx = 0
        self.need_update_distance_dy = 0
        self.cur_speed = 0.08

    def get_camera_key(self):
        return self._camera_key

    def on_touch_slide(self, dx, dy, touches, touch_pos):
        t_pos = math3d.vector2(touch_pos.x, touch_pos.y)
        dx, dy = self.modify_rotate_dist_by_sensitivity(dx, dy, t_pos)
        dx, dy = self.modify_sense_by_dist(dx, dy, t_pos)
        self.need_update_distance_dx += dx
        self.need_update_distance_dy += dy
        if self.camera_ctrl is lobby_cam_ctrl.LobbyCamCtrl():
            self.camera_ctrl.set_started(True)
            return

    def on_update(self, dt):
        super(PartModelDisplayFollowCamera, self).on_update(dt)
        if abs(self.need_update_distance_dx) > 0.001 or abs(self.need_update_distance_dy) > 0.001:
            dx = self.need_update_distance_dx * self.cur_speed
            dy = self.need_update_distance_dy * self.cur_speed
            self.need_update_distance_dx -= dx
            self.need_update_distance_dy -= dy
            self.rotate_camera(dx, dy)

    def rotate_camera(self, dx, dy):
        if self.camera_ctrl is lobby_circle_cam_ctrl.LobbyCircleCamCtrl():
            self._yaw = self._yaw + dx * self._delta_yaw_ratio
            self._pitch = min(max(self._pitch_range[0], self._pitch - dy * self._delta_pitch_ratio), self._pitch_range[1])
            return

    def on_update_camera_target_position(self, dt, target_pos):
        if self.camera_ctrl:
            self.camera_ctrl.set_target_pos(target_pos)
            if target_pos:
                self.camera_ctrl.on_update_by_trigger(dt, self._yaw, self._pitch)

    def on_update_camera_target_parameter(self, config_key, yaw, pitch, height_offset, camera_distance_offset=0):
        self._camera_key = config_key
        self.update_camera_data()
        role_id = global_data.player.get_role() if global_data.player else 'other'
        camera_config = self._camera_config
        focus_vector = camera_config['focus'].get(str(role_id), camera_config['focus'].get('other', [2, 20]))
        camera_distance = camera_config['distance'].get(str(role_id), camera_config['distance'].get('other', 10))
        focus_vector = list(focus_vector)
        old_height = focus_vector[1]
        focus_vector[1] += height_offset
        camera_distance += camera_distance_offset
        if self.camera_ctrl:
            self.camera_ctrl.update_camera_focus_and_distance(focus_vector, camera_distance)
        self._yaw = yaw
        self._pitch = pitch