# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartModelDisplayCamera.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import math
from common.cfg import confmgr
from logic.vscene.parts.camera.camera_controller import lobby_cam_ctrl, model_display_cam_ctrl_new
from logic.gutils.CameraHelper import get_adaptive_camera_fov
import world

class PartModelDisplayCamera(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartModelDisplayCamera, self).__init__(scene, name, False)
        self.init_data()
        self.init_event()
        self.camera_ctrl = model_display_cam_ctrl_new.ModelDisplayCamCtrlNew()

    def get_camera_key(self):
        return '1'

    def init_data(self):
        self._yaw = 0
        self._pitch = 0
        self._delta_yaw_ratio = 1
        self._delta_pitch_ratio = 1
        self._model_cam_flag = None
        self.adjust_touch_pos = None
        self.adjust_touch_time = None
        self.update_camera_data()
        self.init_config_data()
        return

    def update_camera_data(self):
        self._camera_config = confmgr.get('mecha_display', 'LobbyCameraConfig', 'Content')[self.get_camera_key()]
        pitch_range = self._camera_config['pitch']
        self._pitch_range = (math.radians(pitch_range[1]), math.radians(pitch_range[0]))
        adjust_conf = self._camera_config
        self.adjust_touch_interval = adjust_conf['SLIDE_ADJUST_INTERVAL']
        self.adjust_touch_ratio = adjust_conf['MIN_ADJUST_RATIO']
        self.adjust_touch_distance = adjust_conf['SLIDE_ADJUST_DISTANCE']
        self.adjust_pos_move_spd = self.adjust_touch_distance / (self.adjust_touch_interval * 2)

    def init_config_data(self):
        from common.cfg import confmgr
        _screen_sst_conf = confmgr.get('mecha_display', 'SSTConf', 'Content')['lobby_screen']
        self.sst_scr_setting = []
        self.sst_scr_setting.append(_screen_sst_conf.get('base', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('up', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('down', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('left', 1.0))
        self.sst_scr_setting.append(_screen_sst_conf.get('right', 1.0))

    def init_event(self):
        global_data.emgr.resolution_changed += self.on_resolution_changed

    def on_resolution_changed(self):
        scene = self.scene()
        if scene != world.get_active_scene():
            return
        if not scene or not scene.active_camera:
            return
        fov, aspect = get_adaptive_camera_fov(self._camera_config['fov'])
        self.scene().active_camera.aspect = aspect
        self.on_update(0.0)

    def on_character_inited(self):
        self.init_camera()
        self.need_update = True

    def on_enter(self):
        self.on_update(0.0)
        self.need_update = True

    def init_camera(self):
        scene = self.scene()
        if not scene or not scene.active_camera:
            return
        rotation_matrix = global_data.lobby_player.ev_g_rotation_matrix()
        self._yaw = rotation_matrix.yaw
        self._pitch = rotation_matrix.pitch
        fov, aspect = get_adaptive_camera_fov(self._camera_config['fov'])
        self.scene().active_camera.fov = fov
        self.scene().active_camera.aspect = aspect
        self.scene().active_camera.z_range = (1, 18000)
        self.on_update(0.0)

    def on_touch_slide(self, dx, dy, touches, touch_pos):
        t_pos = math3d.vector2(touch_pos.x, touch_pos.y)
        dx, dy = self.modify_rotate_dist_by_sensitivity(dx, dy, t_pos)
        dx, dy = self.modify_sense_by_dist(dx, dy, t_pos)
        self.rotate_camera(dx, dy)
        if self.camera_ctrl is lobby_cam_ctrl.LobbyCamCtrl():
            self.camera_ctrl.set_started(True)
            return

    def rotate_camera(self, dx, dy):
        if self.camera_ctrl is not lobby_cam_ctrl.LobbyCamCtrl():
            return
        self._yaw = self._yaw + dx * self._delta_yaw_ratio
        self._pitch = min(max(self._pitch_range[0], self._pitch - dy * self._delta_pitch_ratio), self._pitch_range[1])
        global_data.emgr.trigger_lobby_player_set_yaw.emit(self._yaw)

    def on_update(self, dt):
        if self.camera_ctrl:
            self.camera_ctrl.on_update(dt, self._yaw, self._pitch)
            self.scene().viewer_position = self.scene().active_camera.world_position

    def on_exit(self):
        self.camera_ctrl = None
        return

    def on_pause(self, flag):
        if self.camera_ctrl:
            self.camera_ctrl.on_pause(flag)

    def modify_rotate_dist_by_sensitivity(self, x_delta, y_delta, pos):
        from logic.gcommon.common_const import ui_operation_const as uoc
        win_w, win_h = global_data.ui_mgr.slide_screen_size.width, global_data.ui_mgr.slide_screen_size.height
        settings = self.sst_scr_setting
        x_scale = settings[uoc.SST_IDX_RIGHT] if pos.x > win_w / 2.0 else settings[uoc.SST_IDX_LEFT]
        x_delta *= settings[uoc.SST_IDX_BASE] * x_scale
        y_scale = settings[uoc.SST_IDX_UP] if pos.y > win_h / 2.0 else settings[uoc.SST_IDX_DOWN]
        y_delta *= settings[uoc.SST_IDX_BASE] * y_scale
        return (
         x_delta, y_delta)

    def modify_sense_by_dist(self, dx, dy, touch_pos):
        from logic.gcommon.time_utility import time
        cnt_time = time()
        win_w, win_h = global_data.ui_mgr.slide_screen_size.width, global_data.ui_mgr.slide_screen_size.height
        ratio = 1.0
        if not self.adjust_touch_pos:
            self.adjust_touch_time = cnt_time
            self.adjust_touch_pos = touch_pos
            ratio = self.adjust_touch_ratio
        else:
            touch_move_vec = self.adjust_touch_pos - touch_pos
            move_length = touch_move_vec.length
            touch_gap = cnt_time - self.adjust_touch_time
            move_distance = touch_gap * self.adjust_pos_move_spd
            if touch_gap >= self.adjust_touch_interval:
                ratio = self.adjust_touch_ratio
            else:
                ratio = move_length / self.adjust_touch_distance
                ratio = max(min(ratio, 1.0), self.adjust_touch_ratio)
            self.adjust_touch_time = cnt_time
            if move_length > 0:
                touch_move_vec.normalize()
            if move_distance >= move_length:
                self.adjust_touch_pos = touch_pos
            elif move_length > self.adjust_touch_distance:
                self.adjust_touch_pos = touch_pos + touch_move_vec * self.adjust_touch_distance
            else:
                self.adjust_touch_pos = self.adjust_touch_pos - touch_move_vec * move_distance
        dx *= ratio / win_w
        dy *= ratio / win_h
        return (
         dx, dy)