# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTrkCamera.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import weakref
import time
import math
import math3d
import world
import logic.vscene.parts.camera.SlerpAction as slerpaction
DEFAULT_FORWARD = math3d.vector(0, 0, 1)
DEFAULT_UP = math3d.vector(0, 1, 0)
SLERP_LINEAR = 0
SLERP_EASE_IN = 1
SLERP_EASE_OUT = 2
SLERP_EASE_IN_OUT = 3

class PartTrkCamera(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartTrkCamera, self).__init__(scene, name)

    def reset_data(self):
        self._cnt_track = None
        self._track_timer_id = 0
        self._track_start_time = 0
        self._track_reverse = False
        self._track_callback = None
        self._track_time_scale = 1.0
        self._left_hand_coordinate = True
        self._MODES = [
         slerpaction.linear,
         slerpaction.easein,
         slerpaction.easeout,
         slerpaction.easeinout]
        self._mode_arg = None
        self._mode_func = self._MODES[SLERP_LINEAR]
        self._fix_forward = None
        self._fix_up = None
        self._is_add_model = False
        self._init_camera_rotation = None
        self._init_camera_position = None
        self._is_reset_model_display_camera = False
        self._first_frame_trk_transform = None
        return

    def on_pre_load(self):
        self._camera = weakref.ref(self.scene().active_camera)
        self.reset_data()
        self.init_event()

    def init_cam_trk_edit_ui(self):
        from logic.comsys.debug.CamTrkEditorUI import CamTrkEditorUI
        CamTrkEditorUI()

    def init_event(self):
        event_mgr = global_data.emgr
        event_mgr.play_camera_trk_event += self.play_track
        print('init_event', event_mgr.play_camera_trk_event)

    def _slerp_mode(self, mode, mode_arg):
        if mode > 0 and mode < len(self._MODES):
            self._mode_func = self._MODES[mode]
            self._mode_arg = mode_arg

    def play_track(self, track_name, callback=None, revert=False, time_scale=1.0, mode=SLERP_LINEAR, mode_arg=2.0, fix_forward=None, fix_up=None, left_hand_coordinate=True, is_add_model=False, is_reset_model_display_camera=False, src_scene=None):
        if src_scene is not None:
            play_scene = src_scene if 1 else world.get_active_scene()
            if self.scene() != play_scene:
                return
            self._slerp_mode(mode, mode_arg)
            self._is_add_model = is_add_model
            self._init_camera_rotation = self.camera.world_rotation_matrix
            self._init_camera_position = self.camera.world_position
            self._is_reset_model_display_camera = is_reset_model_display_camera
            self._fix_forward = fix_forward
            self._fix_up = fix_up
            self._left_hand_coordinate = left_hand_coordinate
            if self._track_timer_id:
                global_data.game_mgr.get_post_logic_timer().unregister(self._track_timer_id)
                self._track_timer_id = 0
            self._cnt_track = global_data.track_cache.create_track(track_name)
            self._cnt_track or log_error('track file %s not exists' % track_name)
            return False
        else:
            self._first_frame_trk_transform = self.get_left_hand_from_trk(self._cnt_track.get_transform(0))
            self._first_frame_trk_transform.rotation.inverse()
            self._track_start_time = time.time()
            self._track_reverse = revert
            self._track_time_scale = time_scale
            if callback:
                self._track_callback = callback
            self._track_timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self.on_track_update)
            return True

    def get_trk_fov(self, cnt_time):
        if not self._cnt_track.has_fov_info():
            return None
        else:
            cur_fov = self._cnt_track.get_fov(cnt_time)
            return cur_fov

    def get_left_hand_from_trk(self, trans):
        pos = trans.translation
        rot = trans.rotation
        forward = rot.forward
        forward = forward.cross(-rot.right)
        trans = math3d.matrix.make_orient(forward, rot.forward)
        trans.do_translate(pos)
        return trans

    def update_camera(self, dt):
        if self._left_hand_coordinate:
            pos = self._cnt_track.get_position(dt)
            rot = self._cnt_track.get_rotation(dt)
            forward = rot.forward if self._fix_forward is None else self._fix_forward
            up = rot.up if self._fix_up is None else self._fix_up
            if math.isnan(forward.x):
                forward = DEFAULT_FORWARD
            if math.isnan(up.x):
                up = DEFAULT_UP
            self.camera.set_placement(pos, forward, up)
        else:
            transform = self.get_left_hand_from_trk(self._cnt_track.get_transform(dt))
            if self._is_add_model:
                transform.translation -= self._first_frame_trk_transform.translation
                transform.rotation *= self._first_frame_trk_transform.rotation
                self.camera.world_rotation_matrix = self._init_camera_rotation * transform.rotation
                base_rot = math3d.matrix_to_rotation(self._init_camera_rotation)
                offset = base_rot.rotate_vector(transform.translation)
                self.camera.world_position = self._init_camera_position + offset
            else:
                self.camera.world_rotation_matrix = transform.rotation
                self.camera.world_position = transform.translation
        if self._is_reset_model_display_camera:
            global_data.emgr.change_model_display_scene_cam_trans.emit(self.camera.world_position, self.camera.rotation_matrix, False)
        fov = self.get_trk_fov(dt)
        if fov is not None:
            self.camera.fov = fov
        self.scene().viewer_position = self.camera.world_position
        return

    def on_track_update(self):
        from common.utils.timer import RELEASE
        cnt_time = time.time()
        track_duration = self._cnt_track.duration
        time_gap = (cnt_time - self._track_start_time) * 1000 * self._track_time_scale
        cnt_interval = min(track_duration, time_gap)
        cnt_interval = self._mode_func(cnt_interval / track_duration, self._mode_arg) * track_duration
        if self._track_reverse:
            cnt_interval = track_duration - cnt_interval
        self.update_camera(cnt_interval)
        if time_gap >= track_duration:
            cb = self._track_callback
            self.reset_data()
            if cb:
                cb()
            self._track_timer_id = 0
            return RELEASE

    @property
    def camera(self):
        return self._camera()

    def on_exit(self):
        if self._track_timer_id:
            global_data.game_mgr.get_post_logic_timer().unregister(self._track_timer_id)
            self._track_timer_id = 0