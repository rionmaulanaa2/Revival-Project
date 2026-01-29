# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbyCamera.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import math
from common.cfg import confmgr
from logic.vscene.parts.camera.camera_controller import lobby_cam_ctrl, slerp_cam_ctrl
from logic.gutils.CameraHelper import get_adaptive_camera_fov
import math3d
import world
from logic.vscene.parts.camera.SlerpCamera import SlerpCamera

class PartLobbyCamera(ScenePart.ScenePart):
    INIT_EVENT = {'on_lobby_player_char_inited': 'on_character_inited',
       'movie_camera_prepare': 'on_movie_camera_prepare',
       'rotate_fixed_point_camera_event': 'rotate_fixed_point_camera',
       'set_fixed_point_camera_event': 'set_fixed_point_camera',
       'trigger_lobby_player_move': 'on_lobby_player_move',
       'rotation_camera_enable': 'on_rotation_camera_enable',
       'reset_lobby_camera_from_free': 'reset_lobby_camera_from_free',
       'net_reconnect_event': 'on_reconnect',
       'net_login_reconnect_event': 'on_reconnect',
       'resolution_changed': 'on_resolution_changed',
       'update_role_id': 'on_update_role_id',
       'modify_lobby_camera_display_parameter': 'modify_camera_display_parameter'
       }

    def __init__(self, scene, name):
        super(PartLobbyCamera, self).__init__(scene, name, False)
        self.init_data()
        self.camera_ctrl = None
        self.pause_flag = False
        self.init_camera_ctrl()
        self.post_timer = global_data.game_mgr.get_post_logic_timer().register(func=self.post_rotate_camera, interval=1, strict=True)
        return

    def on_reconnect(self):
        self._release_timer()
        self.post_timer = global_data.game_mgr.get_post_logic_timer().register(func=self.post_rotate_camera, interval=1, strict=True)

    def _release_timer(self):
        if self.post_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.post_timer)
            self.post_timer = None
        return

    def init_camera_ctrl(self):
        self.camera_ctrl = lobby_cam_ctrl.LobbyCamCtrl()
        self.on_update_role_id()
        self.camera_ctrl.set_started(True)

    def init_data(self):
        self._yaw = 0
        self._pitch = 0
        self._delta_yaw_ratio = 1
        self._delta_pitch_ratio = 1
        self._camera_config = confmgr.get('mecha_display', 'LobbyCameraConfig', 'Content')['1']
        pitch_range = self._camera_config['pitch']
        self._pitch_range = (math.radians(pitch_range[1]), math.radians(pitch_range[0]))
        self._model_cam_flag = None
        self.adjust_touch_pos = None
        self.adjust_touch_time = None
        adjust_conf = self._camera_config
        self.adjust_touch_interval = adjust_conf['SLIDE_ADJUST_INTERVAL']
        self.adjust_touch_ratio = adjust_conf['MIN_ADJUST_RATIO']
        self.adjust_touch_distance = adjust_conf['SLIDE_ADJUST_DISTANCE']
        self.adjust_pos_move_spd = self.adjust_touch_distance / (self.adjust_touch_interval * 2)
        self.init_config_data()
        self.forbit_rotation_camera_count = 0
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

    def on_rotation_camera_enable(self, flag):
        if flag:
            self.forbit_rotation_camera_count -= 1
        else:
            self.forbit_rotation_camera_count += 1

    def on_character_inited(self):
        self.init_camera()

    def init_camera(self):
        scene = self.scene()
        if not scene or not scene.active_camera:
            return
        rotation_matrix = global_data.lobby_player.ev_g_rotation_matrix()
        self._yaw = rotation_matrix.yaw
        self._pitch = rotation_matrix.pitch
        self.update_cam()
        self.on_update(0.0)

    def on_touch_slide(self, dx, dy, touches, touch_pos):
        import math3d
        t_pos = math3d.vector2(touch_pos.x, touch_pos.y)
        dx, dy = self.modify_rotate_dist_by_sensitivity(dx, dy, t_pos)
        dx, dy = self.modify_sense_by_dist(dx, dy, t_pos)
        self.rotate_camera(dx, dy)
        if self.camera_ctrl is lobby_cam_ctrl.LobbyCamCtrl():
            self.camera_ctrl.set_started(True)
            return

    def on_lobby_player_move(self, vec):
        if self.camera_ctrl is lobby_cam_ctrl.LobbyCamCtrl():
            self.camera_ctrl.set_started(True)
            return

    def rotate_camera(self, dx, dy):
        if self.forbit_rotation_camera_count > 0:
            return
        if self.camera_ctrl is not lobby_cam_ctrl.LobbyCamCtrl():
            return
        self._yaw = self._yaw + dx * self._delta_yaw_ratio
        self._pitch = min(max(self._pitch_range[0], self._pitch - dy * self._delta_pitch_ratio), self._pitch_range[1])
        global_data.emgr.trigger_lobby_player_set_yaw.emit(self._yaw)

    def post_rotate_camera(self):
        if self.camera_ctrl and not self.pause_flag:
            dt = global_data.post_logic_real_dt or 0.03
            self.camera_ctrl.on_update(dt, self._yaw, self._pitch)

    def on_resolution_changed(self):
        self.update_cam()

    def update_cam(self):
        if global_data.is_pc_mode:
            vfov = self._camera_config['fov']
            from logic.gutils.pc_resolution_utils import get_window_size
            w, h = get_window_size()
            aspect = float(w) / h
        else:
            vfov, aspect = get_adaptive_camera_fov(self._camera_config['fov'])
        self.scene().active_camera.fov = vfov
        self.scene().active_camera.aspect = aspect
        self.scene().active_camera.z_range = (1, 18000)

    def reset_lobby_camera_from_free(self):
        rotation_matrix = global_data.lobby_player.ev_g_rotation_matrix()
        yaw = rotation_matrix.yaw
        pitch = rotation_matrix.pitch
        self.update_cam()
        target_cam_info = lobby_cam_ctrl.LobbyCamCtrl().get_lobby_cam_info(yaw, pitch)
        if not target_cam_info:
            self._yaw = yaw
            self._pitch = pitch
            self.init_camera_ctrl()
            return
        else:
            target_mat, head_pos = target_cam_info
            active_cam = self.scene().active_camera
            slerp_list = SlerpCamera._cal_spherical_track_point(active_cam.world_transformation, target_mat, head_pos, 10, 0.3)

            def slerp_end_callback(*args):
                self._yaw = yaw
                self._pitch = pitch
                self.init_camera_ctrl()
                if global_data.lobby_player:
                    ctrl_dir = global_data.lobby_player.ev_g_ctrl_dir()
                    global_data.lobby_player.send_event('E_CAMERA_SLERP_END')
                    if ctrl_dir and ctrl_dir.length > 0:
                        global_data.lobby_player.send_event('E_MOVE', ctrl_dir)

            self.camera_ctrl = slerp_cam_ctrl.SlerpCameraCtrl()
            cam = self.scene().active_camera
            self.camera_ctrl.set_slerp_list(cam.world_transformation, slerp_list, None, slerp_end_callback)
            return

    def on_pause(self, flag):
        self.pause_flag = flag
        if flag and global_data.lobby_player:
            model = global_data.lobby_player.ev_g_model()
            if model:
                global_data.lobby_model_rotation = model.world_rotation_matrix
        if self.post_timer:
            global_data.game_mgr.get_post_logic_timer().set_pause(self.post_timer, flag)

    def on_exit(self):
        tm = global_data.game_mgr.get_post_logic_timer()
        tm.unregister(self.post_timer)
        self.camera_ctrl = None
        global_data.lobby_model_rotation = None
        global_data.emgr.on_lobby_player_char_inited -= self.on_character_inited
        global_data.emgr.movie_camera_prepare -= self.on_movie_camera_prepare
        global_data.emgr.trigger_lobby_player_move -= (self.on_lobby_player_move,)
        global_data.emgr.rotation_camera_enable -= (self.on_rotation_camera_enable,)
        global_data.emgr.reset_lobby_camera_from_free -= self.reset_lobby_camera_from_free
        return

    def on_movie_camera_prepare(self, parameter, *args):
        target_matrix = math3d.matrix()
        pos = parameter['position']
        rot = [ math.radians(i) for i in parameter['rotation'] ]
        target_matrix.translation = math3d.vector(*pos)
        target_matrix.rotation = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
        self.camera_ctrl = slerp_cam_ctrl.SlerpCameraCtrl()
        camera = self.scene().active_camera
        self.camera_ctrl.set_slerp_info(camera.world_transformation, target_matrix, parameter['duration'], parameter.get('fov', None))
        return

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

    def on_update_role_id(self, _=None):
        if global_data.player:
            role_id = global_data.player.get_role()
            camera_config = confmgr.get('mecha_display', 'LobbyCameraConfig', 'Content')['1']
            focus_vector = camera_config['focus'].get(str(role_id), camera_config['focus'].get('other', [5, 22]))
            camera_distance = camera_config['distance'].get(str(role_id), camera_config['distance'].get('other', 19))
            if self.camera_ctrl and hasattr(self.camera_ctrl, 'update_camera_focus_and_distance'):
                self.camera_ctrl.update_camera_focus_and_distance(focus_vector, camera_distance)

    def set_fixed_point_camera(self, parameter):
        from logic.vscene.parts.camera.camera_controller import fixed_point_cam_ctrl
        target_matrix = math3d.matrix()
        pos = parameter['position']
        rot = [ math.radians(i) for i in parameter['rotation'] ]
        target_matrix.translation = math3d.vector(*pos)
        target_matrix.rotation = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
        self.camera_ctrl = fixed_point_cam_ctrl.FixedPointCamCtrl()
        self.camera_ctrl.set_target_trans(target_matrix)
        self._yaw = target_matrix.rotation.yaw
        self._pitch = target_matrix.rotation.pitch

    def rotate_fixed_point_camera(self, dx, dy):
        from logic.vscene.parts.camera.camera_controller import fixed_point_cam_ctrl
        if self.forbit_rotation_camera_count > 0:
            return
        if self.camera_ctrl is not fixed_point_cam_ctrl.FixedPointCamCtrl():
            return
        self._yaw = self._yaw + dx * self._delta_yaw_ratio
        self._pitch = min(max(self._pitch_range[0], self._pitch - dy * self._delta_pitch_ratio), self._pitch_range[1])

    def modify_camera_display_parameter(self, focus_vector, camera_distance, fov=None):
        if self.camera_ctrl and hasattr(self.camera_ctrl, 'update_camera_focus_and_distance'):
            self.camera_ctrl.update_camera_focus_and_distance(focus_vector, camera_distance)
            if fov is not None:
                scn = world.get_active_scene()
                camera = scn.active_camera
                camera.fov = fov
        return