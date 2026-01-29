# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPVESettleCamera.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import world
from math import radians
from logic.vscene.parts.camera.camera_controller import model_display_cam_ctrl_new
from common.cfg import confmgr
from logic.gutils.CameraHelper import get_adaptive_camera_fov

class PartPVESettleCamera(ScenePart.ScenePart):
    INIT_EVENT = {'start_settle_scene_camera': 'start_camera',
       'resolution_changed': 'on_resolution_changed'
       }

    def __init__(self, scene, name):
        super(PartPVESettleCamera, self).__init__(scene, name, False)
        self.init_data()
        self.camera_ctrl = model_display_cam_ctrl_new.ModelDisplayCamCtrlNew()

    def init_data(self):
        self._yaw = 0
        self._pitch = 0
        self._delta_yaw_ratio = 1
        self._delta_pitch_ratio = 1
        self._camera_config = confmgr.get('mecha_display', 'LobbyCameraConfig', 'Content')['1']
        pitch_range = self._camera_config['pitch']
        self._pitch_range = (radians(pitch_range[1]), radians(pitch_range[0]))
        self._model_cam_flag = None
        self.adjust_touch_pos = None
        self.adjust_touch_time = None
        adjust_conf = self._camera_config
        self.adjust_touch_interval = adjust_conf['SLIDE_ADJUST_INTERVAL']
        self.adjust_touch_ratio = adjust_conf['MIN_ADJUST_RATIO']
        self.adjust_touch_distance = adjust_conf['SLIDE_ADJUST_DISTANCE']
        self.adjust_pos_move_spd = self.adjust_touch_distance / (self.adjust_touch_interval * 2)
        self.init_config_data()
        return

    def init_config_data(self):
        from common.cfg import confmgr
        _screen_sst_conf = confmgr.get('mecha_display', 'SSTConf', 'Content')['lobby_screen']
        self.sst_scr_setting = []
        self.sst_scr_setting.append(_screen_sst_conf.get('base', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('up', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('down', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('left', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('right', 1.0))

    def on_resolution_changed(self):
        scene = self.scene()
        if scene != world.get_active_scene():
            return
        if not scene or not scene.active_camera:
            return
        fov, aspect = get_adaptive_camera_fov(self._camera_config['fov'])
        self.scene().active_camera.aspect = aspect
        self.on_update(0.0)

    def start_camera(self):
        self.on_update(0.0)
        self.on_pause(False)

    def on_enter(self):
        self.on_update(0.0)
        self.need_update = True
        global_data.emgr.finish_settle_scene_camera.emit()

    def on_update(self, dt):
        if self.camera_ctrl:
            self.camera_ctrl.on_update(dt, self._yaw, self._pitch)
            self.scene().viewer_position = self.scene().active_camera.world_position

    def on_exit(self):
        self.need_update = False
        self.camera_ctrl = None
        return

    def on_pause(self, flag):
        if self.camera_ctrl:
            self.camera_ctrl.on_pause(flag)
        self.need_update = False