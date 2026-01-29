# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/slerp_cam_ctrl.py
from __future__ import absolute_import
from .camctrl_base import CameraCtrl
from time import time
import math3d
import world

class SlerpCameraCtrl(CameraCtrl):

    def init(self):
        self.duration = 0
        self.start_time = 0
        self.slerp_list = []
        self.end_callback = None
        return

    def update_position(self, ratio):
        if self.start_translation is None or self.end_translation is None:
            return
        else:
            return self.start_translation + (self.end_translation - self.start_translation) * ratio

    def set_slerp_info(self, start_transform, end_transform, duration, fov=None):
        self.duration = duration
        self.start_time = time()
        self.start_translation = start_transform.translation
        self.end_translation = end_transform.translation
        self.start_rotation = math3d.matrix_to_rotation(start_transform.rotation)
        self.end_rotation = math3d.matrix_to_rotation(end_transform.rotation)
        self.start_fov = world.get_active_scene().active_camera.fov
        self.end_fov = fov if fov else self.start_fov

    def set_slerp_list(self, start_transform, slerp_list, fov=None, end_callback=None):
        if not slerp_list:
            return
        self.slerp_list = slerp_list
        self.start_time = time()
        self.start_translation = start_transform.translation
        self.start_rotation = math3d.matrix_to_rotation(start_transform.rotation)
        self.start_fov = world.get_active_scene().active_camera.fov
        self.end_fov = fov if fov else self.start_fov
        self.end_callback = end_callback

    def update_rotation(self, ratio):
        if self.start_rotation is None or self.end_rotation is None:
            return
        else:
            cnt_rotation = math3d.rotation(0, 0, 0, 0)
            cnt_rotation.slerp(self.start_rotation, self.end_rotation, ratio)
            return math3d.rotation_to_matrix(cnt_rotation)

    def update_fov(self, ratio):
        return self.start_fov + (self.end_fov - self.start_fov) * ratio

    def on_update(self, dt, yaw, pitch):
        if self.slerp_list:
            cur_duration = time() - self.start_time
            delete_list = []
            self.end_translation = None
            self.end_rotation = None
            target_duration = None
            last_duration = 0
            for idx, slerp_info in enumerate(self.slerp_list):
                duration, target_matrix = slerp_info
                if cur_duration > duration:
                    delete_list.append(slerp_info)
                else:
                    self.end_translation = target_matrix.translation
                    self.end_rotation = math3d.matrix_to_rotation(target_matrix.rotation)
                    target_duration = duration
                    if idx == 0:
                        last_duration = 0
                    else:
                        self.start_translation = self.slerp_list[idx - 1][1].translation
                        self.start_rotation = math3d.matrix_to_rotation(self.slerp_list[idx - 1][1].rotation)
                        last_duration = self.slerp_list[idx - 1][0]
                    break

            for del_info in delete_list:
                self.slerp_list.remove(del_info)

            if target_duration:
                ratio = float(cur_duration - last_duration) / (target_duration - last_duration)
                ratio = max(0, min(1.0, ratio))
                matrix = math3d.matrix()
                matrix.translation = self.update_position(ratio)
                matrix.rotation = self.update_rotation(ratio)
                camera = world.get_active_scene().active_camera
                camera.world_transformation = matrix
                camera.fov = self.update_fov(ratio)
            if not self.slerp_list:
                if self.end_callback and callable(self.end_callback):
                    self.end_callback()
        else:
            if self.duration == 0:
                ratio = 1.0
            else:
                ratio = (time() - self.start_time) * 1.0 / self.duration
            ratio = max(0, min(1.0, ratio))
            active_scene = world.get_active_scene()
            if not active_scene:
                return
            camera = active_scene.active_camera
            matrix = math3d.matrix()
            translation = self.update_position(ratio)
            if translation:
                matrix.translation = translation
            rotation = self.update_rotation(ratio)
            if rotation:
                matrix.rotation = rotation
            camera.world_transformation = matrix
            camera.fov = self.update_fov(ratio)
        return