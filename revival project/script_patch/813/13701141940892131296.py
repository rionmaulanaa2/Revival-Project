# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/model_display_cam_ctrl_new.py
from __future__ import absolute_import
from .camctrl_base import CameraCtrl
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
import math3d
import world
from common.cfg import confmgr

class ModelDisplayCamCtrlNew(CameraCtrl):

    def init(self):
        self._model_control_type = None
        self._scene_content_type = None
        scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.DEFAULT_LEFT)
        global_data.emgr.change_model_display_scene_info.emit(scene_data)
        self.on_change_model_display_scene_cam(scene_data.get('cam_key'))
        self.events_binded = False
        self.process_event(True)
        self._last_position = math3d.vector(0, 0, 0)
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        e_conf = {'change_model_display_control_type': self.on_change_model_display_control_type,
           'change_model_display_scene_cam': self.on_change_model_display_scene_cam,
           'change_model_display_scene_cam_pos': self.on_change_model_display_scene_cam_pos,
           'change_model_display_scene_cam_trans': self.on_change_model_display_scene_cam_trans,
           'update_jiemian_scene_content': self.on_update_jiemian_scene_content
           }
        if flag == self.events_binded:
            return
        self.events_binded = flag
        if flag:
            emgr.bind_events(e_conf)
        else:
            emgr.unbind_events(e_conf)

    def on_pause(self, flag):
        self._model_control_type = None
        self.process_event(not flag)
        return

    def on_change_model_display_control_type(self, control_type):
        self._model_control_type = control_type

    def on_update_jiemian_scene_content(self, scene_type, scene_content_type):
        self._scene_content_type = scene_content_type

    def on_change_model_display_scene_cam(self, key, is_slerp=False, update_cam_at_once=False):
        if self._model_control_type is not None:
            return
        else:
            from logic.gutils.lobby_model_display_utils import get_cam_matrix
            cam_hanger = get_cam_matrix(self._scene_content_type, key)
            self.target_rotation = math3d.matrix_to_rotation(cam_hanger.rotation)
            self.target_position = cam_hanger.translation
            self.cam_need_slerp = is_slerp
            if update_cam_at_once:
                if not is_slerp:
                    self._on_update_cam()
            return

    def on_change_model_display_scene_cam_pos(self, pos, is_slerp=False):
        if self._model_control_type is not None:
            return
        else:
            self.target_position = pos
            self.cam_need_slerp = is_slerp
            return

    def on_change_model_display_scene_cam_trans(self, position, rotation, is_slerp=False):
        if self._model_control_type is not None:
            return
        else:
            if rotation:
                self.target_rotation = math3d.matrix_to_rotation(rotation)
            self.target_position = position
            self.cam_need_slerp = is_slerp
            return

    def on_update(self, dt, yaw, pitch):
        self._on_update_cam()

    def _on_update_cam(self):
        scn = world.get_active_scene()
        cam = scn.active_camera
        if self.cam_need_slerp:
            local_rot_mat = cam.rotation_matrix
            local_rot = math3d.matrix_to_rotation(local_rot_mat)
            local_rot.slerp(local_rot, self.target_rotation, 0.1)
            cam.rotation_matrix = math3d.rotation_to_matrix(local_rot)
            local_pos = cam.world_position
            local_pos.intrp(local_pos, self.target_position, 0.1)
            cam.world_position = local_pos
        else:
            cam.rotation_matrix = math3d.rotation_to_matrix(self.target_rotation)
            cam.world_position = self.target_position
        if not (cam.world_position - self._last_position).is_zero:
            self._last_position = cam.world_position
            global_data.emgr.scene_cam_move.emit()