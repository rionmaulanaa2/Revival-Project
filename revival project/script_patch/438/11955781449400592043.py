# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraTrkPlayer.py
from __future__ import absolute_import
from six.moves import range
import cython
import world
import time
import math3d
import weakref
import math
import common.utils.timer as timer
from .ICameraTrkPlayer import ILinearPolaHelper, ICameraTrkPlayer
EPSILON = 0.001

class LinearPolaHelper(ILinearPolaHelper):

    def __init__(self, start_t, start_v, end_t, end_v=0):
        self.start_t = start_t
        self.start_v = start_v
        self.end_t = end_t
        self.end_v = end_v
        self.v_range = self.end_v - self.start_v
        self.t_range = self.end_t - self.start_t

    def cal(self, t):
        if not self.t_range:
            return self.end_v
        return (t - self.start_t) / self.t_range * self.v_range


class CameraTrkPlayer(ICameraTrkPlayer):

    def __init__(self):
        self._player_custom_data = None
        self._offset_scale = 1.0
        self._rot_scale = 1.0
        self._skip_time = 0
        self.reset_data()
        self._is_finish = False
        self._finish_callback = None
        self._is_additive = True
        self._is_additive_fov = True
        self._is_left_hand_coordinate_system = False
        self._start_smooth_time = 0
        self._end_smooth_time = 0
        self._end_track = None
        self._end_fov_track = None
        self._cnt_track_time = 0
        self._loop_time = 0
        self._one_time_play_length = 0
        self._add_rot = None
        self._addition_tracks = []
        self._transform_scale = None
        self._is_started = False
        self._track_timer_id = 0
        self._camera_init_position = None
        self._camera_init_rotation = None
        self._track_end_time = 0
        return

    def has_start(self):
        return self._is_started

    def on_exit(self):
        if self._track_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._track_timer_id)
            self._track_timer_id = 0

    def on_track_update_camera(self, *args):
        transform, fov = self.on_track_update()
        translation = transform.translation
        if self._camera_init_position:
            translation = self._camera_init_position + transform.translation
        rotation = transform.rotation
        rotation = math3d.matrix_to_rotation(rotation)
        if self._camera_init_rotation:
            rotation = self._camera_init_rotation * rotation
        kan_rot = math3d.rotation_to_matrix(rotation)
        active_scene = world.get_active_scene()
        camera = active_scene.active_camera
        global_data.emgr.change_model_display_scene_cam_trans.emit(translation, math3d.rotation_to_matrix(rotation), False)
        if self._is_finish:
            return timer.RELEASE

    def auto_play_track(self, track_name, callback, revert=False, time_scale=1.0, is_additive=True, is_left_hand=False, finish_callback=None, update_callback=None):
        if self._track_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._track_timer_id)
            self._track_timer_id = 0
        if is_additive:
            result = global_data.emgr.get_lobby_display_type_event.emit()
            display_type = ''
            if result:
                display_type = result[0]
            active_scene = world.get_active_scene()
            if display_type:
                from logic.gutils import lobby_model_display_utils
                scene_data = lobby_model_display_utils.get_display_scene_data(display_type)
                cam_key = scene_data.get('cam_key')
                cam_hanger = active_scene.get_preset_camera(cam_key)
                self._camera_init_position = cam_hanger.translation
                self._camera_init_rotation = math3d.matrix_to_rotation(cam_hanger.rotation)
            else:
                camera = active_scene.active_camera
                self._camera_init_position = camera.world_position
                self._camera_init_rotation = math3d.matrix_to_rotation(camera.rotation_matrix)
        self.play_track(track_name, callback, revert, time_scale, is_additive, is_left_hand, finish_callback)
        self.on_start()
        self._track_timer_id = global_data.game_mgr.get_logic_timer().register(func=update_callback or self.on_track_update_camera)

    def play_track(self, track_name, callback, revert=False, time_scale=1.0, is_additive=True, is_left_hand=False, finish_callback=None):
        if type(track_name) is str:
            track = global_data.track_cache.create_track_default_none(track_name)
            self._track_file = track_name
        else:
            track = track_name
        if not track:
            log_error('track file %s not exists' % track_name)
            return False
        self._cnt_track = track
        self._is_additive = is_additive
        self._is_left_hand_coordinate_system = is_left_hand
        if self._is_additive:
            self._start_trans = self.get_left_hand_trans(0)
            self._start_inverse_rots = self._start_trans.rotation
            self._start_inverse_rots.inverse()
        if self._is_additive_fov:
            if self._cnt_track.has_fov_info():
                self._start_fov = self._cnt_track.get_fov(0.0)
            self._skip_time = 33.0 / 1000
        self._track_reverse = revert
        self._track_time_scale = time_scale
        self._finish_callback = finish_callback
        if callback:
            self._track_callback = callback
        return True

    def restart(self):
        self.on_start()

    def get_left_hand_trans(self, dt):
        if not self._is_left_hand_coordinate_system:
            cur_trans = self.get_left_hand_from_trk(self._cnt_track.get_transform(dt))
        else:
            cur_trans = self._cnt_track.get_transform(dt)
        return cur_trans

    def get_trk_transformation(self, dt):
        cur_trans = self.get_left_hand_trans(dt)
        if self._is_additive:
            cur_trans.translation -= self._start_trans.translation
            cur_trans.rotation *= self._start_inverse_rots
        if abs(self._offset_scale - 1.0) > EPSILON:
            cur_trans.translation *= self._offset_scale
        if abs(self._rot_scale - 1.0) > EPSILON:
            scale_mul = int(round(abs(self._rot_scale)))
            unit_rot = cur_trans.rotation
            if self._rot_scale < 0:
                unit_rot.transpose()
            unit_trans = math3d.matrix()
            for i in range(scale_mul):
                unit_trans = unit_trans * unit_rot

            cur_trans.rotation = unit_trans.rotation
        if self._add_rot:
            cur_trans.translation *= self._add_rot
        if self._transform_scale:
            cur_trans.rotation *= self._transform_scale
        self.check_addition_track_modify(cur_trans, dt)
        return cur_trans

    def on_start(self):
        self._is_finish = False
        self._is_started = True
        self._track_start_time = time.time() + self._start_smooth_time
        if self._start_smooth_time > 0:
            trans = self.get_trk_transformation(0)
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(None, trans.rotation.pitch, False, self._start_smooth_time)
        end_trans = self.get_trk_transformation(self._cnt_track.duration)
        end_fov = self.get_trk_fov(self._cnt_track.duration)
        if end_trans.translation.length > 0.1 and self._end_smooth_time <= 0:
            pass
        self._one_time_play_length = self._cnt_track.duration / 1000.0 - self._skip_time
        if self._end_smooth_time > 0:
            self._end_track = self._generate_track(end_trans, self._end_smooth_time)
        if not end_fov:
            end_fov = 0
        self._end_fov_track = LinearPolaHelper(0, end_fov, self._end_smooth_time, 0)
        self._track_end_time = self._track_start_time + self._one_time_play_length * (self._loop_time + 1)
        return

    def on_track_update(self):
        import time
        cnt_time = time.time()
        self._cnt_track_time = cnt_time
        return self.get_track(cnt_time)

    def get_trk_fov(self, cnt_time):
        if not self._cnt_track.has_fov_info():
            return None
        else:
            cur_fov = self._cnt_track.get_fov(cnt_time)
            if self._is_additive_fov:
                cur_fov -= self._start_fov
            return cur_fov

    def get_track(self, cnt_time):
        if not self._is_started:
            return (None, None)
        else:
            if cnt_time < self._track_start_time:
                return (None, None)
            if self._track_end_time > cnt_time >= self._track_start_time:
                track_duration = self._cnt_track.duration
                play_time = cnt_time - self._track_start_time
                play_time = play_time % self._one_time_play_length
                time_gap = (play_time + self._skip_time) * 1000 * self._track_time_scale
                cnt_interval = max(0, track_duration - time_gap) if self._track_reverse else min(track_duration, time_gap)
                cur_trk = self.get_trk_transformation(cnt_interval)
                fov = self.get_trk_fov(cnt_interval)
                return (
                 cur_trk, fov)
            if self._track_end_time + self._end_smooth_time > cnt_time:
                dt = (cnt_time - self._track_end_time) * 1000
                query_dt = max(min(dt, self._end_smooth_time * 1000), 0)
                cur_trk = self._end_track.get_transform(query_dt)
                fov = self._end_fov_track.cal(query_dt)
                return (
                 cur_trk, fov)
            self._is_finish = True
            if self._finish_callback:
                self._finish_callback()
            if self._end_track:
                cur_trk = self._end_track.get_transform(self._end_smooth_time * 1000)
                fov = self._end_fov_track.cal(self._end_smooth_time * 1000)
                return (
                 cur_trk, fov)
            end_trans = self.get_trk_transformation(self._cnt_track.duration)
            fov = self.get_trk_fov(self._cnt_track.duration)
            return (
             end_trans, fov)
            return None

    def check_addition_track_modify(self, cur_trans, dt):
        if self._addition_tracks:
            for trk in self._addition_tracks:
                query_dt = max(min(dt, trk.duration), 0)
                added_trk = trk.get_transform(query_dt)
                cur_trans.translation += added_trk.translation
                cur_trans.rotation *= added_trk.rotation

    def get_trk_final_trans(self, check_smooth=False):
        if check_smooth:
            return math3d.matrix()
        else:
            end_trans = self.get_trk_transformation(self._cnt_track.duration)
            return end_trans

    def get_trk_first_trans(self):
        return self.get_trk_transformation(self._skip_time * 1000)

    def reset_data(self):
        self._cnt_track = None
        self._track_timer_id = 0
        self._track_start_time = 0
        self._track_reverse = False
        self._track_callback = None
        self._track_time_scale = 1.0
        self._track_file = None
        self._is_additive = False
        self._start_trans = None
        self._start_inverse_rots = None
        self._start_fov = 0
        self._cnt_track_time = 0
        self._end_track = None
        self._end_fov_track = None
        self._loop_time = 0
        self._start_smooth_time = 0
        return

    def get_left_hand_from_trk(self, trans):
        import math3d
        pos = trans.translation
        rot = trans.rotation
        forward = rot.forward
        forward = forward.cross(-rot.right)
        trans = math3d.matrix.make_orient(forward, rot.forward)
        trans.do_translate(pos)
        return trans

    def set_player_custom_data(self, custom_data):
        self._player_custom_data = custom_data

    def get_player_custom_data(self):
        return self._player_custom_data

    def set_player_scale(self, offset_scale, rot_scale, transform_scale=None):
        self._offset_scale = offset_scale
        self._rot_scale = rot_scale
        self._transform_scale = transform_scale

    def set_add_rot(self, rot):
        if abs(rot - 0) < EPSILON:
            self._add_rot = None
        else:
            self._add_rot = math3d.matrix.make_rotation_y(math.radians(rot))
        return

    def get_player_scale(self):
        return (
         self._offset_scale, self._rot_scale)

    def is_finish(self):
        return self._is_finish

    def on_finish(self):
        self.run_callback()
        self.reset_data()

    def run_callback(self, is_finish=True):
        if self._track_callback:
            self._track_callback(self, is_finish)

    def is_additive(self):
        return self._is_additive

    def get_trk_duration_time(self):
        if self._cnt_track:
            return self._one_time_play_length * (self._loop_time + 1) + self._end_smooth_time
        else:
            return 0

    def get_trk_clean_duration_time(self):
        if self._cnt_track:
            return self._cnt_track.duration / 1000.0 - self._skip_time
        else:
            return 0

    def get_trk_start_smooth_time(self):
        return self._start_smooth_time

    def set_smooth_time(self, start_time, end_time):
        self._start_smooth_time = start_time
        self._end_smooth_time = end_time

    def _generate_track(self, trans, duration=0.3):
        from logic.gutils.CameraHelper import track_build
        track = track_build([(0, trans), (duration * 1000, math3d.matrix())], duration * 1000)
        return track

    def set_loop_time(self, loop_time):
        self._loop_time = loop_time

    def test_show(self):
        trans = [ self.get_trk_transformation(t).translation for t in range(0, int(self._cnt_track.duration), 33) ]

    def add_trk_addition_trans(self, start_time, start_matrix, end_matrix, duration):
        if self._end_smooth_time:
            log_error('addition trans can not coexist with end smooth!!!')
            import traceback
            traceback.print_stack()
            return
        from logic.gutils.CameraHelper import track_build
        time_mat_list = [(start_time, start_matrix), (duration * 1000, end_matrix)]
        if start_time > 0:
            time_mat_list.insert(0, (0, math3d.matrix()))
        track = track_build(time_mat_list, duration * 1000)
        self._addition_tracks.append(track)


class CamPlotPlayer(CameraTrkPlayer):

    def __init__(self):
        super(CamPlotPlayer, self).__init__()

    def on_start(self):
        super(CamPlotPlayer, self).on_start()

    def on_finish(self):
        super(CamPlotPlayer, self).on_finish()