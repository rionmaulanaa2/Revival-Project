# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/fixed_point_cam_ctrl.py
from __future__ import absolute_import
from .camctrl_base import CameraCtrl
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
import math3d
import world

class FixedPointCamCtrl(CameraCtrl):

    def init(self):
        self.cam_need_slerp = True

    def set_target_trans(self, trans):
        self.target_rotation = trans.rotation
        self.target_position = trans.translation
        scn = world.get_active_scene()
        cam = scn.active_camera
        cam.world_position = self.target_position
        cam.rotation_matrix = self.target_rotation

    def on_update(self, dt, yaw, pitch):
        scn = world.get_active_scene()
        cam = scn.active_camera
        x_rotate = math3d.matrix.make_rotation_x(pitch)
        y_rotate = math3d.matrix.make_rotation_y(yaw)
        rot_mat = x_rotate * y_rotate
        cam.world_position = self.target_position
        cam.world_rotation_matrix = rot_mat