# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/lucky_house_cam_ctrl.py
from __future__ import absolute_import
from .camctrl_base import CameraCtrl
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
import math3d
import world

class LuckyHouseCamCtrl(CameraCtrl):

    def init(self):
        scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.LUCKY_HOUSE)
        self.on_change_lucky_house_scene_cam(scene_data.get('cam_key'))
        self.events_binded = False
        self.process_event(True)

    def process_event(self, flag):
        emgr = global_data.emgr
        e_conf = {'change_lucky_house_scene_cam': self.on_change_lucky_house_scene_cam
           }
        if flag == self.events_binded:
            return
        self.events_binded = flag
        if flag:
            emgr.bind_events(e_conf)
        else:
            emgr.unbind_events(e_conf)

    def on_pause(self, flag):
        self.process_event(not flag)

    def on_change_lucky_house_scene_cam(self, key, is_slerp=False):
        scene = global_data.game_mgr.scene
        cam_hanger = scene.get_preset_camera(key)
        self.target_rotation = math3d.matrix_to_rotation(cam_hanger.rotation)
        self.target_position = cam_hanger.translation
        self.cam_need_slerp = is_slerp

    def on_update(self, dt, yaw, pitch):
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