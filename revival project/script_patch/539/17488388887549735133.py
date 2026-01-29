# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/SlerpCamera.py
from __future__ import absolute_import
from six.moves import range
import cython
import math3d
from common.utils.time_utils import get_time
from logic.client.const.camera_const import COLL_SLERP
from logic.vscene.parts.camera.CamAimModelComponent import CamAimModelComponent
from .ISlerpCamera import ISlerpCamera
SPHERE = 1
SPLINE = 2

class SlerpCamera(ISlerpCamera):

    def __init__(self, slerp_callback, slerp_end_callback):
        self.cam = None
        self.slerp_move_cost_time = -1.0
        self.slerp_target_pos = None
        self.slerp_end_pos = None
        self.slerp_target_transform = None
        self.slerp_target_rotation = None
        self.is_in_cam_slerp_event = False
        self.is_only_fov_slerp = False
        self.pos_changed_vec_when_slerp = math3d.vector(0, 0, 0)
        self.slerp_type = SPLINE
        self.slerp_rotate_center = None
        self.slerp_level = None
        self.slerp_action_list = []
        self.slerp_passed_time = 0
        self.aim_model_widget = None
        self._slerp_time_action = None
        self._slerp_start_transformation = None
        self._slerp_callback = slerp_callback
        self._slerp_end_callback = slerp_end_callback
        self._camera_slerp_callback = None
        self.slerp_start_fov = 0
        self.slerp_target_fov = 0
        self.cur_slerp_track = None
        return

    def set_camera(self, camera):
        self.cam = camera

    def set_camera_setting(self, transform, fov):
        if self._slerp_callback:
            self._slerp_callback(transform, fov)

    def set_slerp_target(self, tar_pos, tar_rotation, tar_fov, cost_time=0.2, callback=None, is_sphere=False, rotate_center=None, delay=0, slerp_end_pt=None, level=COLL_SLERP, model=None, start_trans=None, start_fov=None, **kwargs):
        if not self.cam:
            return
        else:
            if self.is_in_cam_slerp_event:
                self._end_slerp(False)
            if cost_time > 0:
                tar_rotation = math3d.matrix.make_rotation_x(tar_rotation.pitch) * math3d.matrix.make_rotation_y(tar_rotation.yaw)
                self._camera_slerp_callback = callback
                self.slerp_move_cost_time = cost_time
                self.slerp_passed_time = -delay
                self._slerp_time_action = None
                self.slerp_target_pos = tar_pos
                self.slerp_end_pos = slerp_end_pt
                self.slerp_target_fov = tar_fov
                if not start_fov:
                    self.slerp_start_fov = self.cam.fov if 1 else start_fov
                    self.slerp_target_rotation = math3d.matrix(tar_rotation)
                    self.slerp_rotate_center = rotate_center
                    self.slerp_level = level
                    self._slerp_start_transformation = start_trans
                    end_matrix = self.get_camera_transform_matrix(self.slerp_target_pos, self.slerp_target_rotation)
                    self.slerp_target_transform = end_matrix
                    if is_sphere:
                        self.slerp_type = SPHERE
                    else:
                        self.slerp_type = SPLINE
                    spec_trk = kwargs.get('trk')
                    if spec_trk:
                        self.cur_slerp_track = spec_trk
                    else:
                        self._generate_slerp_track(cost_time)
                    self.is_in_cam_slerp_event = True
                    if (tar_pos - self.cam.position).length < 1 and self.cam.fov != tar_fov:
                        self.is_only_fov_slerp = True
                    else:
                        self.is_only_fov_slerp = False
                    self.pos_changed_vec_when_slerp = math3d.vector(0, 0, 0)
                    axises = [
                     self.slerp_target_transform.rotation.forward, self.slerp_target_transform.rotation.up,
                     self.slerp_target_transform.rotation.right]
                    for ax in axises:
                        if ax.is_zero:
                            self.report_error(tar_pos, tar_rotation)
                            break

                else:
                    end_matrix = self.get_camera_transform_matrix(tar_pos, tar_rotation)
                    self.set_camera_setting(end_matrix, tar_fov)
                    if callback:
                        callback(True)
                    if model and model is global_data.cam_model:
                        return
                self.destroy_aim_model_widget()
                global_data.ui_mgr.close_ui('FightPlasmaWeaponUI')
                if model:
                    wp_gun = global_data.cam_lplayer.share_data.ref_wp_bar_cur_weapon
                    if wp_gun and wp_gun.is_accumulate_gun():
                        magnification_triplet = global_data.ex_scene_mgr_agent.check_settle_scene_active() or kwargs.get('magnification_triplet', None)
                        aim_scope_id = kwargs.get('aim_scope_id', 0)
                        from logic.comsys.battle.FightPlasmaWeaponUI import FightPlasmaWeaponUI
                        FightPlasmaWeaponUI(None, magnification_triplet=magnification_triplet, aim_scope_id=aim_scope_id)
                self.aim_model_widget = CamAimModelComponent(model)
            return

    def update_slerp_target(self, tar_pos, tar_rotation, cost_time=0):
        if self.is_in_cam_slerp_event:
            self.slerp_target_pos = tar_pos
            self.slerp_target_rotation = math3d.matrix(tar_rotation)
            end_matrix = self.get_camera_transform_matrix(self.slerp_target_pos, self.slerp_target_rotation)
            self.slerp_target_transform = end_matrix
            self._slerp_start_transformation = self.cam.world_transformation
            if self.slerp_type == SPHERE and self.slerp_rotate_center:
                self.slerp_rotate_center += self.pos_changed_vec_when_slerp
            self.pos_changed_vec_when_slerp = math3d.vector(0, 0, 0)
            passed_time = self.slerp_passed_time
            if passed_time <= 0:
                remain_time = self.slerp_move_cost_time
            else:
                remain_time = self.slerp_move_cost_time - self.slerp_passed_time
                if remain_time <= 0:
                    return
                passed_percent = min(max(passed_time / self.slerp_move_cost_time, 0.0), 1.0)
                self.slerp_move_cost_time = remain_time + cost_time
                self.slerp_passed_time = 0
                self.slerp_start_fov = self.slerp_start_fov + (self.slerp_target_fov - self.slerp_start_fov) * passed_percent
                new_slerp_action_list = []
                for t in self.slerp_action_list:
                    per, action = t
                    per -= passed_percent
                    new_slerp_action_list.append([per, action])

                self.slerp_action_list = new_slerp_action_list
            self._generate_slerp_track(self.slerp_move_cost_time)
            axises = [
             self.slerp_target_transform.rotation.forward, self.slerp_target_transform.rotation.up,
             self.slerp_target_transform.rotation.right]
            for ax in axises:
                if ax.is_zero:
                    self.report_error(tar_pos, tar_rotation)
                    break

    def set_slerp_remain_time(self, remain_slerp_time):
        if self.is_in_cam_slerp_event:
            passed_time = self.slerp_passed_time
            if passed_time > 0:
                remain_time = self.slerp_move_cost_time - self.slerp_passed_time
                if remain_time <= 0:
                    return
            self.slerp_move_cost_time = remain_slerp_time + self.slerp_passed_time
            self._generate_slerp_track(self.slerp_move_cost_time)

    def get_slerp_remain_time(self):
        if self.is_in_cam_slerp_event:
            passed_time = self.slerp_passed_time
            remain_time = self.slerp_move_cost_time - self.slerp_passed_time
            return remain_time
        else:
            return 0

    def _generate_slerp_track(self, cost_time, start_time=0):
        time_mat_list = []
        start_matrix = math3d.matrix(self._slerp_start_transformation or self.cam.world_transformation if 1 else self._slerp_start_transformation)
        if start_time > 0:
            time_mat_list.append((0, start_matrix))
        time_mat_list.append((start_time, start_matrix))
        end_matrix = self.slerp_target_transform
        if self.slerp_type == SPHERE:
            if (start_matrix.translation - end_matrix.translation).length > 4.0:
                time_mat_list.extend(SlerpCamera._cal_spherical_track_point(start_matrix, end_matrix, self.slerp_rotate_center, 10, duration=cost_time))
        if self.slerp_end_pos:
            time_mat_list.append((cost_time, self.get_camera_transform_matrix(self.slerp_end_pos, self.slerp_target_rotation)))
        else:
            time_mat_list.append((cost_time, end_matrix))
        self.cur_slerp_track = self._build_track(time_mat_list, cost_time)

    def get_camera_transform_matrix(self, pos, rotation, scale=math3d.vector(1, 1, 1)):
        mat = math3d.matrix()
        mat.do_rotation(rotation)
        mat.do_translate(pos)
        mat.do_scale(scale)
        return mat

    def rotate_by_center(self, pos, center, rotation_mat):
        new_pos = (pos - center) * rotation_mat
        return new_pos + center

    @classmethod
    def _cal_spherical_track_point(cls, start_mat, end_mat, rotate_center, fill_pt_nums, duration):
        start_rot = math3d.matrix_to_rotation(start_mat.rotation)
        end_rot = math3d.matrix_to_rotation(end_mat.rotation)
        fill_pts = []
        yaw_start = (start_mat.translation - rotate_center).yaw
        yaw_end = (end_mat.translation - rotate_center).yaw
        pitch_start = (start_mat.translation - rotate_center).pitch
        pitch_end = (end_mat.translation - rotate_center).pitch
        matrix = math3d.matrix.make_rotation_x(pitch_start) * math3d.matrix.make_rotation_y(yaw_start)
        end_matrix = math3d.matrix.make_rotation_x(pitch_end) * math3d.matrix.make_rotation_y(yaw_end)
        start_pos_rot = math3d.matrix_to_rotation(matrix)
        end_pos_rot = math3d.matrix_to_rotation(end_matrix)
        start_length = (start_mat.translation - rotate_center).length
        end_length = (end_mat.translation - rotate_center).length
        for i in range(fill_pt_nums):
            mat = math3d.matrix()
            rot = math3d.rotation(1, 0, 0, 0)
            pos_rot = math3d.rotation(1, 0, 0, 0)
            factor = float(i + 1) / (fill_pt_nums + 1)
            rot.slerp(start_rot, end_rot, factor, True)
            mat.rotation = math3d.rotation_to_matrix(rot)
            pos_rot.slerp(start_pos_rot, end_pos_rot, factor, True)
            length = (end_length - start_length) * factor + start_length
            pos = math3d.rotation_to_matrix(pos_rot).forward * length + rotate_center
            mat.do_translate(pos)
            fill_pts.append((duration * factor, mat))

        return fill_pts

    def _cal_spline_track_point(self, start_mat, end_mat, factor):
        start_rot = math3d.matrix_to_rotation(start_mat.rotation)
        end_rot = math3d.matrix_to_rotation(end_mat.rotation)
        start_pos = start_mat.translation
        end_pos = end_mat.translation
        mat = math3d.matrix()
        rot = math3d.rotation(1, 0, 0, 0)
        rot.slerp(start_rot, end_rot, factor, True)
        pos = math3d.vector(0, 0, 0)
        pos.intrp(start_pos, end_pos, factor)
        mat.rotation = math3d.rotation_to_matrix(rot)
        mat.do_translate(pos)
        return mat

    def _build_track(self, time_mat_list, duration=2.0):
        from logic.gutils.CameraHelper import track_build
        return track_build(time_mat_list, duration)

    def test_spline_speed(self, start_pos, start_rotate, end_pos, end_rotate, cost_time):
        start_mat = self.get_camera_transform_matrix(start_pos, start_rotate)
        end_mat = self.get_camera_transform_matrix(end_pos, end_rotate)
        time_mat_list = [(0, start_mat), [cost_time, end_mat]]
        tra = self._build_track(time_mat_list, cost_time)
        interval = 1.0 / 30
        passed_time = 0.0
        while passed_time < cost_time:
            passed_time += interval
            cur_transform = tra.get_transform(passed_time)

    def _process_slerp_event(self, dt):
        if self.slerp_move_cost_time < 0 or self.cur_slerp_track is None:
            return
        else:
            self.slerp_passed_time += dt
            passed_time = self.slerp_passed_time
            if passed_time <= 0:
                passed_time = 0
            if passed_time > self.slerp_move_cost_time:
                self._end_slerp()
            else:
                get_track_passed_time = passed_time
                if self._slerp_time_action:
                    new_pass_percent = self._slerp_time_action(passed_time / self.slerp_move_cost_time)
                    new_pass_percent = min(1, max(0, new_pass_percent))
                    get_track_passed_time = self.slerp_move_cost_time * new_pass_percent
                factor = get_track_passed_time / float(self.slerp_move_cost_time)
                cur_transform = self.cur_slerp_track.get_transform(get_track_passed_time)
                cur_fov = self.slerp_start_fov + (self.slerp_target_fov - self.slerp_start_fov) * factor
                cur_transform.translation += self.pos_changed_vec_when_slerp
                axises = [
                 cur_transform.rotation.forward, cur_transform.rotation.up,
                 cur_transform.rotation.right]
                for ax in axises:
                    if ax.is_zero:
                        self.report_error(passed_time, self.slerp_move_cost_time)
                        cur_transform = self.cam.world_transformation
                        break

                self.set_camera_setting(cur_transform, cur_fov)
                self.check_slerp_mid_action(float(passed_time) / self.slerp_move_cost_time)
            return

    def _end_slerp(self, with_sync=True, with_callback=True):
        if self.slerp_move_cost_time < 0 or self.cur_slerp_track is None:
            return
        else:
            is_finish = self.slerp_passed_time >= self.slerp_move_cost_time
            self.slerp_move_cost_time = -1.0
            self.slerp_passed_time = 0
            self.cur_slerp_track = None
            self._slerp_time_action = None
            self.slerp_rotate_center = None
            self.slerp_end_pos = None
            self.is_in_cam_slerp_event = False
            self.is_only_fov_slerp = False
            self.slerp_level = None
            self.check_slerp_mid_action(1.0)
            self.slerp_action_list = []
            if with_sync:
                cur_transform = self.slerp_target_transform
                cur_fov = self.slerp_target_fov
                cur_transform.translation += self.pos_changed_vec_when_slerp
                self.set_camera_setting(cur_transform, cur_fov)
            self.pos_changed_vec_when_slerp = math3d.vector(0, 0, 0)
            if with_callback:
                if self._slerp_end_callback:
                    self._slerp_end_callback(is_finish)
                if self._camera_slerp_callback:
                    _camera_slerp_callback = self._camera_slerp_callback
                    self._camera_slerp_callback = None
                    _camera_slerp_callback(is_finish)
            return

    def get_camera_slerp_callback(self):
        return self._camera_slerp_callback

    def replace_camera_slerp_callback(self, cb):
        if not callable(self._camera_slerp_callback):
            return
        self._camera_slerp_callback = cb

    def end_slerp_camera_early(self, with_sync, with_callback=True):
        if self.is_in_cam_slerp_event:
            self._end_slerp(with_sync, with_callback)

    def on_update(self, dt):
        self._process_slerp_event(dt)
        if self.aim_model_widget:
            self.aim_model_widget.on_update(dt)

    def on_target_pos_changed(self, diff_vec):
        if self.is_in_cam_slerp_event:
            self.pos_changed_vec_when_slerp += diff_vec

    def add_slerp_mid_action(self, time_percent, action):
        self.slerp_action_list.append([time_percent, action])

    def check_slerp_mid_action(self, cur_percent):
        remain_slerp_action_list = []
        for task in self.slerp_action_list:
            percent, action = task
            if percent <= cur_percent:
                if action:
                    action()
            else:
                remain_slerp_action_list.append(task)

        self.slerp_action_list = remain_slerp_action_list

    def destroy_aim_model_widget(self):
        if self.aim_model_widget:
            self.aim_model_widget.destroy()
            self.aim_model_widget = None
        return

    def destroy(self):
        self.destroy_aim_model_widget()

    def get_slerp_action(self, type_str, parameters):
        from logic.vscene.parts.camera.SlerpAction import SlerpActionInst
        if SlerpActionInst:
            return SlerpActionInst.generateAction(type_str, parameters)
        else:
            return None

    def set_slerp_action(self, action):
        self._slerp_time_action = action

    def set_slerp_action_str(self, type_str, parameters):
        self.set_slerp_action(self.get_slerp_action(type_str, parameters))

    def get_is_sphere(self):
        return self.slerp_type == SPHERE

    def report_error(self, *args):
        err_msg = 'zero axises new 2222!!!: {}, {}, {}, {}, {}, {}'.format(self.cam.world_rotation_matrix, self.slerp_target_transform, self.slerp_target_rotation, self.slerp_end_pos, self.pos_changed_vec_when_slerp, str(args))
        self._end_slerp(False, False)
        raise ValueError('zero axises new 33333!!!', err_msg)