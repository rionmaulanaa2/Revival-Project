# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSettleCamera.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import world
from logic.vscene.parts.camera.camera_controller import settle_cam_ctrl

class PartSettleCamera(ScenePart.ScenePart):
    CAM_TRACK_PATH = 'effect/fx/scenes/camera/jie_suan.trk'
    INIT_EVENT = {'start_settle_scene_camera': 'start_camera',
       'resolution_changed': 'on_resolution_changed'
       }

    def __init__(self, scene, name):
        super(PartSettleCamera, self).__init__(scene, name, False)
        self.init_data()
        self.camera_ctrl = settle_cam_ctrl.SettleCamCtrl()

    def init_data(self):
        self._yaw = 0
        self._pitch = 0
        self.can_start_camera = False

    def on_resolution_changed(self):
        cam = self.scene().active_camera
        if not cam:
            return
        win_width = 0
        win_height = 0
        if not global_data.is_pc_mode:
            from common.const import common_const
            win_width, win_height = common_const.WINDOW_WIDTH, common_const.WINDOW_HEIGHT
        else:
            from logic.gutils.pc_resolution_utils import get_window_size
            win_width, win_height = get_window_size()
        cur_ratio = float(win_width) / win_height
        cam.aspect = cur_ratio

    def init_track_data(self):
        self.track = global_data.track_cache.create_track(self.CAM_TRACK_PATH)
        self.track_max_time = self.track.duration / 1000.0
        self.track_last_time = 0
        self.start_trans = math3d.matrix()
        self.track_ended = False
        cam = self.scene().get_preset_camera('camera_jiesuan_01')
        self.end_trans = self.track.get_transform(self.track.duration)
        self.scene().active_camera.position = cam.translation
        self.scene().active_camera.rotation_matrix = cam.rotation

    def on_enter(self):
        self.init_track_data()
        self.on_update(0.0)
        self.need_update = True

    def start_camera(self):
        self.can_start_camera = True

    def on_update(self, dt):
        if dt != 0.0 and not self.can_start_camera:
            return
        if self.camera_ctrl:
            self.track_last_time += dt
            if self.track_last_time < self.track_max_time:
                cur_trans = self.track.get_transform(self.track_last_time * 1000)
                new_trans = cur_trans * self.start_trans
                self.camera_ctrl.set_target_trans(new_trans)
            elif not self.track_ended:
                self.camera_ctrl.set_target_trans(self.end_trans)
                global_data.emgr.finish_settle_scene_camera.emit()
                self.track_ended = True
            if self.scene() is world.get_active_scene():
                self.camera_ctrl.on_update(dt, self._yaw, self._pitch)

    def on_exit(self):
        self.camera_ctrl = None
        return