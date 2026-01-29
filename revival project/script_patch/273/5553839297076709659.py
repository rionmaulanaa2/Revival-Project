# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCameraSimple.py
from __future__ import absolute_import
import math3d
from . import ScenePart
from .camera.SphericalCameraManager import SphericalCameraManager

class PartCameraSimple(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartCameraSimple, self).__init__(scene, name, True)
        self._bind_unit = None
        self._cam_dirty = False
        self._cam_mat = math3d.matrix()
        self._pitch = 0
        self.cam_manager = SphericalCameraManager()
        return

    def on_load(self):
        self.process_bind_events(True)
        self.cam_manager.on_enter()

    def on_exit(self):
        self._bind_unit = None
        self.process_bind_events(False)
        if self.cam_manager:
            self.cam_manager.on_exit()
            self.cam_manager = None
        return

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'scene_camera_player_setted_event': self.on_bind
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_bind(self, unit):
        self._bind_unit = unit
        self._cam_dirty = True
        if self._bind_unit:
            self.update_target_pos()
            from data.camera_state_const import MELEE_MECHA_MODE
            from logic.client.const.camera_const import POSTURE_STAND
            global_data.emgr.set_cur_camera_posture_event.emit(POSTURE_STAND)
            self.cam_manager.switch_cam_state(MELEE_MECHA_MODE)
            from logic.comsys.debug.CameraTestUI import CameraTestUI
            CameraTestUI()
            com = self._bind_unit.add_com('ComStateTrkCamSimple', 'client.com_camera')
            com.init_from_dict(self._bind_unit, {})
            com.on_init_complete()

    def get_cam_mat(self):
        if self._cam_dirty and self._bind_unit:
            model = self._bind_unit.ev_g_model()
            height = model.bounding_box_w.y
            ofs_z = math3d.matrix.make_translation(0, 0, -model.bounding_radius_w * 2)
            rot_pitch = math3d.matrix.make_rotation_x(self._pitch)
            ofs_y = math3d.matrix.make_translation(0, height / 2, 0)
            self._cam_mat = ofs_z * rot_pitch * ofs_y
            self._cam_dirty = False
        return self._cam_mat

    def on_update(self, dt):
        if self._bind_unit:
            self.update_target_pos()

    def update_target_pos(self):
        if self._bind_unit:
            model = self._bind_unit.ev_g_model()
            target_pos = model.world_position
            if target_pos:
                self.cam_manager.on_target_pos_changed(model.world_position)

    def get_cur_camera_state_type(self):
        return self.cam_manager.get_cur_camera_state_type()

    def get_cur_camera_magnification_triplet(self):
        return self.cam_manager.get_cur_camera_magnification_triplet()

    def get_cur_camera_aim_scope_id(self):
        return self.cam_manager.get_cur_camera_aim_scope_id()

    def yaw(self, delta):
        return self.cam_manager.yaw(delta)

    def pitch(self, delta):
        return self.cam_manager.pitch(delta)