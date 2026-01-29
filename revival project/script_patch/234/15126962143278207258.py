# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/SphericalCameraManager.py
from __future__ import absolute_import
import cython
import math3d
import world
import logic.client.const.camera_const as camera_const
from data.camera_state_const import *
from logic.client.const.camera_const import POSTURE_STAND
from logic.client.const.camera_const import SWITCH_SLERP, FREE_CAMERA_SLERP_LIST, COLL_SLERP
from logic.gutils.pc_resolution_utils import get_window_size
from logic.gutils.CameraHelper import cal_vertical_fov, get_look_at_pitch
from logic.gutils import character_ctrl_utils
import logic.gcommon.common_const.collision_const as collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
VIEWER_UPDATE_FRAME = 10
COLL_UPDATE_FRAME = 10
UP_VECTOR = math3d.vector(0, 1, 0)
RIGHT_VECTOR = math3d.vector(1, 0, 0)
YZ_VECTOR = math3d.vector(0, 1, 1)
from .SlerpCamera import SlerpCamera
from logic.gutils.CameraHelper import rotate_by_center, cal_horizontal_default_pos, get_reverse_rotation, normalize_angle
from .CameraCollisionChecker import CameraCollisionChecker
from .CamTrkComponent import CamTrkComponent
from .CamAsymptoticFollowCom import CamAsymptoticFollowCom
import math
INV_DEFAULT_CHUNK_SIZE = 1.0 / 832.0
LAST_STOP_CAMERA_UPDATE_TRACE_STR = ''
from math import floor

class SphericalCameraManager(object):

    def __init__(self):
        self.is_in_observe = False
        self.cam = None
        self.viewer_update = 0
        self.coll_update = 0
        self.cam_state = self.new_cam_state(THIRD_PERSON_MODEL)
        self.cam_slerp_method = SlerpCamera(self.set_slerp_camera_setting, self.slerp_end_common_callback)
        self.last_camera_state_setting = None
        self.camera_y_slide_dir = 1
        self.focus_point = None
        self._real_focus_point = None
        self.default_pos = None
        self._real_default_pos = None
        self.__pitch = 0
        self.__yaw = 0
        self.__roll = 0
        self.force_check_distance = 0
        self._acc_delta_yaw = 0
        self._acc_delta_pitch = 0
        self.cur_frame_first_switch_camera_time = 0
        self.cur_frame_first_switch_camera_start_trans = None
        self.cur_player_posture = POSTURE_STAND
        self._target_pos = None
        self._to_visual_focus_length = 0
        self.pos_focus_angle = 0
        self.viewer_dir_offset = math3d.vector(0, 0, 0)
        self.is_enable_collision_check = True
        self._first_world_offset = math3d.vector(0, 0, 0)
        self._ex_world_offset = math3d.vector(0, 0, 0)
        self._default_pos_offset = 0
        self._default_hfov = 0
        self._vfov_offset = 0
        self._cur_fov = 0
        self._cur_magnification_triplet = None
        self._cur_aim_scope_id = 0
        self.init_components()
        self._aim_camera_posture_timer = None
        self.UPDATE_ACC_DELTA_YAW_LIMIT = 8.0 / 180.0 * 3.1415926
        self.UPDATE_ACC_DELTA_PITCH_LIMIT = 8.0 / 180.0 * 3.1415926
        self._is_need_camera_collision_check = True
        self._is_enable_follow_target = True
        self._is_enable_ctrl_viewpos = True
        self._is_dirty = False
        self._track_fov_offset = 0
        self._cam_state_slerp_state = (None, None)
        self._is_destroyed = False
        self._addition_trk_trans = None
        self._real_addition_trk_params = None
        self._need_update_target_pos = False
        self._old_cam_world_rot_mat = None
        self._model_role_id = '11'
        self.cnt_trunk = (-99999, -99999)
        self._refresh_3d_listener_ditry = True
        self.use_special_target_pos = False
        self.use_special_target_pos_for_judge = False
        self.added_trk_enable = True
        self.lock_enable_follow = False
        self.switch_enable = True
        self.cam_ani_enable = True
        self._update_timer_id = -1
        self._render_timer_id = -1
        self._prev_cam_state_slerp_end_cb = None
        self.is_upload_invalid_camera_world_pos = False
        return

    def init_components(self):
        self.cam_coll_checker = CameraCollisionChecker()
        self._added_trk_component = CamTrkComponent()
        self._follow_com = CamAsymptoticFollowCom()

    def destroy_components(self):
        if self.cam_coll_checker:
            self.cam_coll_checker.destroy()
            self.cam_coll_checker = None
        if self._added_trk_component:
            self._added_trk_component.destroy()
            self._added_trk_component = None
        if self._follow_com:
            self._follow_com.destroy()
            self._follow_com = None
        return

    @property
    def _yaw(self):
        return self.__yaw

    @_yaw.setter
    def _yaw(self, val):
        if val is None:
            return
        else:
            if abs(val) > 20000:
                args = [
                 self.__yaw, val]
                if self.cam:
                    args.append(self.cam.world_position)
                    args.append(self.cam.world_transformation)
                if self.cam_state:
                    args.append(self.cam_state.TYPE)
                    args.append(self.cam_state.max_yaw_radian)
                    args.append(self.cam_state.min_yaw_radian)
                self.report_error(args)
                val = normalize_angle(val)
            old_yaw = self.__yaw
            self.__yaw = val
            global_data.cam_data.yaw = val
            self.on_yawed(val - old_yaw)
            global_data.emgr.camera_yaw_changed.emit(self.__yaw)
            return

    @property
    def _pitch(self):
        return self.__pitch

    @property
    def _roll(self):
        return self.__roll

    @_pitch.setter
    def _pitch(self, val):
        old_pitch = self.__pitch
        self.__pitch = val
        global_data.cam_data.pitch = val
        self.on_pitched(val - old_pitch)

    def set_roll(self, roll_value):
        self.__roll = roll_value
        cur_roll = self.cam.rotation_matrix.roll
        delta = roll_value - cur_roll
        self.cam.rotate_z(delta)
        return self.__roll

    @property
    def cur_target_pos(self):
        if not self._target_pos:
            return None
        else:
            return self._world_offset + self._target_pos

    @property
    def _world_offset(self):
        return self._ex_world_offset + self._first_world_offset

    def on_enter(self):
        scn = global_data.game_mgr.scene
        cam = scn.active_camera
        self.cam = cam
        if global_data.is_pc_mode:
            w, h = get_window_size()
            cam.aspect = float(w) / h
        self.cam_slerp_method.set_camera(cam)
        self.process_bind_events(True)
        tm = global_data.game_mgr.get_post_logic_timer()
        self._update_timer_id = tm.register(func=self.check_update, interval=1, timedelta=True)
        _, _, _, _, trunk_size = world.get_active_scene().get_safe_scene_map_uv_parameters()
        self.force_check_distance = trunk_size / 2
        global_data.cam_world_transform = None
        return

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'enable_special_target_pos_logic': self.enable_special_target_pos_logic,
           'enable_special_target_pos_logic_for_judge': self.enable_special_target_pos_logic_for_judge,
           'enable_target_pos_update_flag_event': self.enable_target_pos_update,
           'camera_target_pos_changed_event': self.on_target_pos_changed,
           'set_target_pos_for_special_logic': self.on_set_target_pos_for_special_logic,
           'camera_target_follow_speed_event': self.on_change_target_follow_speed,
           'camera_set_yaw_event': self.set_yaw,
           'camera_set_pitch_event': self.set_pitch,
           'camera_set_hfov_event': self.set_hoz_fov,
           'camera_set_collision_slerp_target_pos_event': self.set_collision_slerp_target_pos,
           'camera_set_slerp_target_event': self.set_slerp_target,
           'camera_set_slerp_target_speed_action_event': self.set_slerp_target_spped_action,
           'camera_set_camera_setting_event': self.set_slerp_camera_setting,
           'modify_camera_parameters_event': self.modify_camera_parameters,
           'set_camera_yaw_pitch_with_slerp_event': self.set_target_angle_with_rotation,
           'set_up_camera_pos_parameters_event': self.set_up_camera_pos_parameters,
           'slerp_into_setupped_camera_event': self.slerp_into_setupped_camera_event,
           'play_camera_animation_event': self.play_camera_animation,
           'play_camera_preset_animation_event': self.play_preset_camera_animation,
           'set_camera_world_offset_event': self.set_camera_offset,
           'accelerate_camera_slerp_event': self.accelerate_camera_slerp_event,
           'switch_camera_state_event': self.switch_cam_state,
           'update_camera_viewer_event': self.update_cam_viewer,
           'tell_update_camera_fov_event': self.actively_update_camera_fov,
           'set_cur_camera_posture_event': self.set_cur_player_posture,
           'camera_play_added_trk_event': self.play_added_trk,
           'camera_cancel_added_trk_event': self.cancel_added_trk,
           'camera_get_added_trk_event': self.get_added_trk,
           'camera_play_plot_trk_event': self.play_plot_trk,
           'camera_additional_transformation_event': self.set_additional_transformation,
           'camera_additional_transformation_end_event': self.set_additional_transformation_end,
           'net_login_reconnect_event': self.on_net_reconnect,
           'net_reconnect_event': self.on_net_reconnect,
           'camera_bind_to_model_socket_event': self.bind_to_model_socket,
           'camera_bind_to_scene_event': self.bind_to_scene,
           'camera_enable_follow_event': self.camera_enable_follow,
           'scene_enable_camera_ctrl_viewpos': self.camera_enable_ctrl_viewpos,
           'get_camera_ctrl_view_pos_enabled': self.get_camera_ctrl_view_pos_enabled,
           'check_camera_vertical_col': self.set_vertical_col_checked,
           'end_slerp_camera_early_event': self.do_end_slerp_camera_early,
           'force_set_last_camera_tarns': self.force_set_last_camera_trans,
           'camera_cancel_all_trk': self.cancel_all_trk,
           'camera_added_trk_enable': self.on_added_trk_enable,
           'camera_lock_enable_follow_event': self.on_lock_enable_follow,
           'switch_cam_state_enable_event': self.switch_cam_state_enable,
           'switch_cam_ani_enable_event': self.switch_cam_ani_enable,
           'resolution_changed': self._on_resolution_changed,
           'camera_switch_collision_check_event': self.set_is_enable_collision_check,
           'camera_refresh_update_event': self.refresh_update_timer,
           'camera_stop_update_event': self.stop_update_camera,
           'app_frame_rate_changed_event': self.on_frame_rate_changed
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def switch_cam_state_enable(self, enable):
        self.switch_enable = enable

    def switch_cam_ani_enable(self, enable):
        self.cam_ani_enable = enable

    def _on_resolution_changed(self):
        if self.cam:
            w, h = get_window_size()
            self.cam.aspect = float(w) / h
        self.actively_update_camera_fov()

    def on_added_trk_enable(self, enable):
        self.added_trk_enable = enable

    def on_lock_enable_follow(self, lock):
        self.lock_enable_follow = lock

    def on_exit(self):
        self.cancel_aim_camera_posture_timer()
        self._prev_cam_state_slerp_end_cb = None
        self.stop_update_timer()
        if self._render_timer_id:
            tm = global_data.game_mgr.get_render_timer()
            tm.unregister(self._render_timer_id)
            self._render_timer_id = -1
        self.process_bind_events(False)
        if self.cam_state:
            self.del_cam_state(self.cam_state)
        self.cam_state = None
        self._is_destroyed = True
        self.cam_slerp_method.destroy()
        self.cam_slerp_method = None
        self.destroy_components()
        return

    def switch_cam_state(self, new_cam_type, **kwargs):
        if not self.switch_enable:
            return
        self.normal_switch_cam_state(new_cam_type, **kwargs)

    def update_cam_viewer(self, *args, **kwargs):
        if not self.cam_state or not self.cam_state.is_valid():
            return
        conf = self.cam_state.get_state_enter_setting()
        if not conf:
            return
        viewer_dir_offset = conf.get('viewer_dir_offset', 0)
        self.viewer_dir_offset = viewer_dir_offset

    def actively_update_camera_fov(self, *args, **kwargs):
        if not self.cam_state or not self.cam_state.is_valid():
            return
        else:
            conf = self.cam_state.get_state_enter_setting()
            if not conf:
                return
            fov = conf.get('fov', None)
            if fov:
                self._default_hfov = fov
                fov = cal_vertical_fov(fov)
            else:
                fov = self.cam.fov
            self._cur_fov = fov
            return

    def new_cam_state(self, new_cam_type, **kwargs):
        return global_data.camera_state_pool.create_camera_state(new_cam_type, self.is_in_observe, self, **kwargs)

    def del_cam_state(self, cam_state):
        global_data.camera_state_pool.destroy_camera_state(cam_state)

    def normal_switch_cam_state(self, new_cam_type, **kwargs):
        if not self._target_pos:
            if self._is_destroyed:
                log_error('SphericalCameraManager has already been destroyed!')
            return
        else:
            import math
            last_camera_setting_conf = self.last_camera_state_setting
            if self.cam_state:
                last_transfer_conf = self.cam_state.get_enter_transfer_setting()
                need_revert_rotate = last_transfer_conf.get('bOutBackRotate', False)
                transfer_out_time = last_transfer_conf.get('fTransferOutTime', 0)
            else:
                need_revert_rotate = False
                transfer_out_time = 0
            new_cam_state = self.new_cam_state(new_cam_type, **kwargs)
            slerp_leave_act_list = []
            if self.cam_state:
                self.last_camera_state_setting = self.cam_state.dump_camera_setting()
                new_cam_state.on_switch_camera_state(self.cam_state)
                slerp_leave_act_list = self.cam_state.get_leave_slerp_mid_action()
                self.del_cam_state(self.cam_state)
            if not new_cam_state.is_enable_player_posture() or not new_cam_state.is_support_posture(self.cur_player_posture):
                self.set_cur_player_posture(POSTURE_STAND)
            modify_offset = None
            if self._real_default_pos != self.default_pos:
                if self._real_default_pos and self.default_pos:
                    modify_offset = self.default_pos - self._real_default_pos
                    if modify_offset.length < 1:
                        modify_offset = None
            old_cam_type = self.cam_state.TYPE
            self.cam_state = new_cam_state
            global_data.cam_data.camera_state_type = new_cam_type
            conf = self.cam_state.get_state_enter_setting()
            pos = conf.get('pos')
            if not conf or not pos:
                log_error('error cam state conf', new_cam_type, self.cur_player_posture)
                raise RuntimeError('Try to Switch to error state', new_cam_type, kwargs, self.cur_player_posture, old_cam_type)
            fov = conf.get('fov', None)
            if fov:
                self._default_hfov = fov
                fov = cal_vertical_fov(fov)
            else:
                fov = self.cam.fov
            focus = conf.get('focus')
            viewer_dir_offset = conf.get('viewer_dir_offset', 0)
            self.viewer_dir_offset = viewer_dir_offset
            transfer_conf = self.cam_state.get_enter_transfer_setting(old_cam_type)
            force_trans_time = kwargs.get('force_trans_time', None)
            regular_transfer_time = transfer_out_time + transfer_conf.get('fTransferInTime', 0.2)
            if force_trans_time is not None:
                transfer_time = force_trans_time if 1 else regular_transfer_time
                delay_time = transfer_conf.get('fDelayTime', 0.0)
                self._cur_magnification_triplet = conf.get('magnification_triplet', None)
                self._cur_aim_scope_id = conf.get('aim_scope_id', 0)
                fFollowSpd = transfer_conf.get('fFollowSpd', None)
                fFollowTransTime = transfer_conf.get('fFollowTransTime', None)
                fFollowRecoverTime = transfer_conf.get('fFollowRecoverTime', 0.2)
                if fFollowSpd is not None and transfer_time > 0 and self._follow_com:
                    self._follow_com.on_change_target_follow_speed(fFollowSpd, transfer_time or fFollowTransTime, fFollowRecoverTime)
            if fFollowSpd is None:
                self.check_newest_target_pos()
            if focus:
                new_focus = math3d.vector(focus[0], focus[1], focus[2]) if 1 else self.focus_point
                target_pos = math3d.vector(*pos)
                default_pos = cal_horizontal_default_pos(target_pos, new_focus)
                old_focus = self.focus_point
                old_default_pos = self.default_pos
                self.update_real_camera_config(default_pos, new_focus)
                modify_offset or self.update_camera_config(default_pos, new_focus)
            else:
                new_def = default_pos + modify_offset
                new_focus_with_modify = math3d.vector(new_focus)
                new_focus_with_modify.y += modify_offset.y
                self.update_camera_config(new_def, new_focus_with_modify)
            self._default_pos_offset = 0
            self._cur_fov = fov
            rotation_matrix, is_sphere = self.get_enter_rotation_setting(target_pos, new_focus, transfer_conf, last_camera_setting_conf, need_revert_rotate)
            axises = [
             rotation_matrix.forward, rotation_matrix.up,
             rotation_matrix.right]
            for ax in axises:
                if ax.is_zero:
                    self.report_error(self.cam_state.TYPE, target_pos, new_focus, transfer_conf, last_camera_setting_conf, need_revert_rotate, rotation_matrix, self._pitch, self._yaw, is_sphere)
                    break

            self.cam_state.on_before_enter()
            self.cam_state.on_get_enter_parameters()
            focus_point = self.focus_point or math3d.vector(0, 0, 0)
            cur_target_pos = self.cur_target_pos or math3d.vector(0, 0, 0)
            rotate_center = cur_target_pos + focus_point
            new_pos = self.get_slerp_target_pos(rotation_matrix, rotate_center)
            max_pitch, min_pitch = conf.get('pitch', (None, None))
            yaw_range = conf.get('yaw', 0.0)
            if max_pitch is not None and min_pitch is not None:
                self.cam_state.max_pitch_radian = math.radians(max_pitch)
                self.cam_state.min_pitch_radian = math.radians(min_pitch)
            if yaw_range:
                self.cam_state.yaw_range = math.radians(yaw_range)
            start_trans = None
            if kwargs.get('force_inherit_cam_transformation', False) and old_focus:
                if self.cur_frame_first_switch_camera_time == global_data.game_time:
                    start_trans = self.cur_frame_first_switch_camera_start_trans
                else:
                    old_rotation_matrix = math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw)
                    old_rotate_center = cur_target_pos + old_focus
                    old_pos = self.get_slerp_target_pos(old_rotation_matrix, old_rotate_center, default_pos=old_default_pos)
                    start_trans = math3d.matrix()
                    start_trans.do_rotation(old_rotation_matrix)
                    start_trans.do_translate(old_pos)
                    self.cur_frame_first_switch_camera_time = global_data.game_time
                    self.cur_frame_first_switch_camera_start_trans = start_trans
            self._pitch = rotation_matrix.pitch
            self._yaw = rotation_matrix.yaw
            if self.is_free_type_camera(self.cam_state.TYPE):
                transfer_time = camera_const.FREE_TYPE_IN_TIME
            elif self.is_free_type_camera(old_cam_type):
                transfer_time = camera_const.FREE_TYPE_OUT_TIME
            is_finish_switch = False
            self._cam_state_slerp_state = (
             old_cam_type, new_cam_type)

            def on_slerp_success(is_finish):
                self.cam_state.enter()
                if is_finish:
                    self._pitch = self.cam.world_rotation_matrix.pitch
                    self._yaw = self.cam.world_rotation_matrix.yaw
                is_finish_switch = True
                self._cam_state_slerp_state = (None, None)
                global_data.emgr.camera_switch_to_state_event.emit(new_cam_type, old_cam_type, is_finish_switch)
                return None

            if self.is_in_cam_slerp():
                self.cam_slerp_method.end_slerp_camera_early(False, False)
            self.set_slerp_target(new_pos, rotation_matrix, self._cur_fov, cost_time=transfer_time, callback=on_slerp_success, is_sphere=is_sphere, rotate_center=rotate_center, delay=delay_time, level=SWITCH_SLERP, model=conf.get('cModel', None), start_trans=start_trans, magnification_triplet=self._cur_magnification_triplet, aim_scope_id=self._cur_aim_scope_id)
            speedActionConf = transfer_conf.get('cSpeedAction', [])
            if speedActionConf:
                self.cam_slerp_method.set_slerp_action_str(speedActionConf[0], speedActionConf[1])
            global_data.emgr.camera_switch_to_state_event.emit(new_cam_type, old_cam_type, is_finish_switch)
            if transfer_time > 0:
                for leave_act in slerp_leave_act_list:
                    percent, callback = leave_act
                    self.cam_slerp_method.add_slerp_mid_action(percent, callback)

            else:
                for percent, callback in slerp_leave_act_list:
                    if callable(callback):
                        callback()

            return

    def refresh_yaw_range(self):
        self.cam_state.refresh_real_yaw_range()

    def get_enter_rotation_setting(self, target_pos, new_focus, transfer_conf, last_camera_setting_conf, need_revert_rotate):
        from logic.gutils.CameraHelper import cal_vertical_fov, get_look_at_pitch, get_look_at_yaw
        enter_same_rotate = transfer_conf.get('bInKeepRotate', camera_const.KEEP_PRE_ROTATE)
        look_at_pos = transfer_conf.get('look_at_pos', None)
        if look_at_pos:
            cur_target_pos = self.cur_target_pos or math3d.vector(0, 0, 0)
            look_at_dir = look_at_pos - (self.default_pos + cur_target_pos)
            if look_at_dir.length > 1:
                look_at_pich = look_at_dir.pitch
                look_at_yaw = look_at_dir.yaw
                look_at_mat = math3d.matrix.make_rotation_x(look_at_pich) * math3d.matrix.make_rotation_y(look_at_yaw)
                return (
                 look_at_mat, False)
        if enter_same_rotate == camera_const.KEEP_PRE_ROTATE:
            if need_revert_rotate:
                last_trans = last_camera_setting_conf['trans']
                rotation_matrix = last_trans.rotation
                is_sphere = True
            else:
                rotation_matrix = math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw)
                is_sphere = False
        elif enter_same_rotate == camera_const.KEEP_PRE_ROTATE_ONLY_YAW:
            if need_revert_rotate:
                last_trans = last_camera_setting_conf['trans']
                rotation_matrix = last_trans.rotation
                self._yaw = rotation_matrix.yaw
                is_sphere = True
            else:
                is_sphere = False
            new_pitch = get_look_at_pitch(new_focus, target_pos)
            rotation_matrix = math3d.matrix.make_rotation_x(new_pitch) * math3d.matrix.make_rotation_y(self._yaw)
        else:
            new_yaw = get_look_at_yaw(new_focus, target_pos) + self._yaw
            new_pitch = get_look_at_pitch(new_focus, target_pos)
            is_sphere = True
            rotation_matrix = math3d.matrix.make_rotation_x(new_pitch) * math3d.matrix.make_rotation_y(new_yaw)
        if not is_sphere:
            cur_yaw = self.cam.world_rotation_matrix.yaw
            nor_yaw = normalize_angle(cur_yaw - self._yaw)
            if abs(nor_yaw) > math.pi * 0.25:
                is_sphere = True
        if rotation_matrix.roll > 0.01:
            rotation_matrix = math3d.matrix.make_rotation_x(rotation_matrix.pitch) * math3d.matrix.make_rotation_y(rotation_matrix.yaw)
        return (rotation_matrix, is_sphere)

    def update_camera_config(self, default_pos, focus_pos):
        self.default_pos = default_pos
        self.focus_point = focus_pos
        self._to_visual_focus_length = ((self.default_pos - self.focus_point) * YZ_VECTOR).length
        if self.default_pos.x < self._to_visual_focus_length:
            if self._to_visual_focus_length > 0 and abs(self.default_pos.x) < self._to_visual_focus_length:
                self.pos_focus_angle = math.asin(self.default_pos.x / self._to_visual_focus_length)
            else:
                self.pos_focus_angle = 0
        else:
            self.pos_focus_angle = 0
        self.cam_coll_checker.update_camera_config(default_pos, focus_pos, self.cam)

    def update_real_camera_config(self, default_pos, focus_point):
        self._real_default_pos = math3d.vector(default_pos)
        self._real_focus_point = math3d.vector(focus_point)

    def check_update(self, dt):
        real_dt = global_data.post_logic_real_dt
        self.on_update(real_dt)
        self._check_collision_tick()
        if global_data.sunshine_uniman:
            global_data.sunshine_uniman.update(dt)

    def on_update(self, dt):
        self._record_old_camera_transformation()
        self._on_update_camera_pos(dt)
        self._refresh_3d_listener()
        if self.cam_slerp_method and self.cam_slerp_method.aim_model_widget:
            self.cam_slerp_method.aim_model_widget.on_update(dt)
        if self._cur_fov:
            self.cam.fov = self._cur_fov
        if self.is_in_cam_slerp():
            self._is_need_camera_collision_check = True
            self.cam_slerp_method.on_update(dt)
        else:
            if self.coll_update == 0:
                self._is_need_camera_collision_check = True
                self.coll_update = COLL_UPDATE_FRAME
            self.coll_update -= 1
        if self._added_trk_component:
            self._added_trk_component.on_track_update()
        if self._is_enable_ctrl_viewpos:
            viewer_position_offset = self.cam.world_rotation_matrix.forward * self.viewer_dir_offset
            if not global_data.feature_mgr.is_support_open_aim_in_house():
                hit_point_list = []
                group = -1
                mask = collision_const.TERRAIN_GROUP | collision_const.WOOD_GROUP | collision_const.STONE_GROUP
                chect_begin = self.cam.world_position - self.cam.world_rotation_matrix.forward * 0.1 * NEOX_UNIT_SCALE
                check_end = chect_begin + viewer_position_offset
                is_hit = character_ctrl_utils.hit_by_scene_collision(chect_begin, check_end, group, mask, is_multi_select=False, hit_point_list=hit_point_list)
                if is_hit and hit_point_list:
                    old_viewer_position_offset = math3d.vector(viewer_position_offset)
                    viewer_position_offset = hit_point_list[0] - chect_begin
            target_exist = bool(self.cur_target_pos)
            if target_exist and not math.isnan(self.cur_target_pos.x) and not math.isinf(self.cur_target_pos.x):
                if global_data.feature_mgr.is_support_open_aim_in_house():
                    new_viewer_pos = self.cur_target_pos + viewer_position_offset
                else:
                    new_viewer_pos = self.cur_target_pos
                trunk_pos = [0, 0]
                x = new_viewer_pos.x
                z = new_viewer_pos.z
                trunk_pos[0] = int(floor(x * INV_DEFAULT_CHUNK_SIZE + 0.5))
                trunk_pos[1] = int(floor(z * INV_DEFAULT_CHUNK_SIZE + 0.5))
                if trunk_pos[0] != self.cnt_trunk[0] or trunk_pos[1] != self.cnt_trunk[1]:
                    self.viewer_update = 0
                    self.cnt_trunk = trunk_pos
                if self.viewer_update <= 0:
                    self.viewer_update = VIEWER_UPDATE_FRAME
                    scn = global_data.game_mgr.scene
                    if global_data.feature_mgr.is_support_open_aim_in_house():
                        scn.set_lod_offset(viewer_position_offset)
                    else:
                        scn.set_lod_offset(-viewer_position_offset)
                    scn.viewer_position = new_viewer_pos
        self.viewer_update -= 1

    def _check_collision(self):
        if not self.is_enable_collision_check:
            return
        else:
            self._is_need_camera_collision_check = False
            if self.cam_state.TYPE not in {AIM_MODE, FIRST_PERSON_MODEL, DEAD_MODEL}:
                world_offset = self.get_checkable_world_offset(self._world_offset)
                if self._real_addition_trk_params:
                    old_add_rot, _, _ = self._real_addition_trk_params
                    reverse_old_add_rot = get_reverse_rotation(old_add_rot)
                    cam_rot = math3d.matrix_to_rotation(self.cam.world_rotation_matrix)
                    org_rot = cam_rot * reverse_old_add_rot
                    org_mat = math3d.rotation_to_matrix(org_rot)
                else:
                    org_mat = None
                self.cam_coll_checker.check_collision(self.cam, self.cur_target_pos, self.cam_state.get_need_collision_recover(), world_offset, org_mat)
            return

    def get_collision_point_with_record(self, cur_target_pos, camera_pos, camera_rotate_matrix, world_offset):
        if not self.is_enable_collision_check:
            return (None, None)
        else:
            self._is_need_camera_collision_check = False
            world_offset = self.get_checkable_world_offset(world_offset)
            return self.cam_coll_checker.get_collision_point_with_record(cur_target_pos, camera_pos, camera_rotate_matrix, world_offset)

    def pitch(self, delta):
        delta *= self.camera_y_slide_dir
        original_pitch = self.cam_state._pitch
        self.cam_state.pitch(delta)
        self.check_camera_transformation_matrix_is_valid()
        return (self.cam_state._pitch - original_pitch) / self.camera_y_slide_dir

    def on_pitched(self, delta):
        if delta == 0:
            return
        self._acc_delta_pitch += delta
        self._is_need_camera_collision_check = True
        if abs(self._acc_delta_pitch) > self.UPDATE_ACC_DELTA_PITCH_LIMIT:
            self._acc_delta_pitch = 0
            self._refresh_3d_listener_ditry = True
        if self.is_in_cam_slerp():
            self._update_slerp_target()
        if global_data.cam_lplayer and global_data.player and global_data.cam_lplayer.id == global_data.player.id and global_data.player.logic:
            if not global_data.player.logic.ev_g_death():
                global_data.player.logic.send_event('E_ACTION_SYNC_CAM_PITCH', delta)

    def yaw(self, radians_delta):
        original_yaw = self.cam_state._yaw
        self.cam_state.yaw(radians_delta)
        self.check_camera_transformation_matrix_is_valid()
        return self.cam_state._yaw - original_yaw

    def on_yawed(self, radians_delta):
        if radians_delta == 0:
            return
        self._is_need_camera_collision_check = True
        self._acc_delta_yaw += radians_delta
        if abs(self._acc_delta_yaw) > self.UPDATE_ACC_DELTA_YAW_LIMIT:
            self._acc_delta_yaw = 0
            self._refresh_3d_listener_ditry = True
        if self.is_in_cam_slerp():
            self._update_slerp_target()
        if global_data.cam_lplayer and global_data.player and global_data.cam_lplayer.id == global_data.player.id and global_data.player.logic:
            if not global_data.player.logic.ev_g_death():
                global_data.player.logic.send_event('E_ACTION_SYNC_CAM_YAW', radians_delta)

    def _update_slerp_target(self, cost_time=0):
        if math.isnan(self._pitch) or math.isinf(self._pitch):
            self.report_error(self.cam_state.TYPE, self.default_pos, self.focus_point, self.cur_target_pos, self._pitch, self._yaw)
            self.__pitch = 0
        if math.isnan(self._yaw) or math.isinf(self._yaw):
            self.report_error(self.cam_state.TYPE, self.default_pos, self.focus_point, self.cur_target_pos, self._pitch, self._yaw)
            self.__yaw = 0
        mat = math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw)
        new_pos = self.get_slerp_target_pos(mat, self.cur_target_pos + self.focus_point)
        self.cam_slerp_method.update_slerp_target(new_pos, mat, cost_time)

    def set_yaw(self, yaw):
        self._yaw = yaw
        self.check_refresh_yaw_and_pitch()

    def set_pitch(self, pitch):
        self._pitch = pitch
        self.check_refresh_yaw_and_pitch()

    def set_yaw_and_pitch(self, yaw, pitch):
        self._pitch = pitch
        self._yaw = yaw
        self.check_refresh_yaw_and_pitch()

    def get_pitch(self):
        return self._pitch

    def get_yaw(self):
        return self._yaw

    def refresh_yaw_pitch(self):
        x_rotate = math3d.matrix.make_rotation_x(self._pitch)
        y_rotate = math3d.matrix.make_rotation_y(self._yaw)
        if self.is_in_cam_slerp():
            _yaw = self._yaw
            _pitch = self._pitch
            self.cam_slerp_method.end_slerp_camera_early(True, True)
            self._yaw = _yaw
            self._pitch = _pitch
        if self.cam:
            rot_mat = x_rotate * y_rotate
            if self.cur_target_pos and self.focus_point:
                new_pos = self.get_slerp_target_pos(rot_mat, self.focus_point + self.cur_target_pos)
                trans = self.cam_slerp_method.get_camera_transform_matrix(new_pos, rot_mat)
                self.cam_slerp_method.set_camera_setting(trans, self._cur_fov)
            else:
                self.cam.world_rotation_matrix = rot_mat
                self._refresh_3d_listener_ditry = True
            if self._addition_trk_trans:
                self.set_additional_transformation(*self._addition_trk_trans)

    def get_cur_camera_state_type(self):
        return self.cam_state.TYPE

    def get_cur_camera_magnification_triplet(self):
        return self._cur_magnification_triplet

    def get_cur_camera_aim_scope_id(self):
        return self._cur_aim_scope_id

    def get_fov(self):
        return self.cam.fov

    def set_show_fov(self, fov):
        self.cam.fov = fov
        if self.cam_coll_checker:
            self.cam_coll_checker.update_camera_fov(self.cam)

    def set_pos(self, pos):
        self.cam.position = pos

    def get_pos(self):
        return math3d.vector(self.cam.position)

    def on_switch_player_posture(self, to_state, need_transfer=True):
        if self.cur_player_posture == to_state:
            return
        else:
            if not self.cur_target_pos:
                return
            if to_state is None:
                return
            if not self.cam_state or not self.cam_state.is_valid():
                return
            import math
            cam_state_type = self.cam_state.get_real_camera_type()
            self.set_cur_player_posture(to_state)
            new_conf = self.cam_state.get_state_enter_setting()
            if not new_conf:
                return
            new_focus = new_conf.get('focus')
            focus_point = math3d.vector(new_focus[0], new_focus[1], new_focus[2])
            transfer_time = new_conf.get('fInnerTransfer', 0.2) if need_transfer else 0
            delay_time = new_conf.get('fInnerDelay', 0)
            new_def_pos = new_conf.get('pos')
            new_def_pos = cal_horizontal_default_pos(math3d.vector(*new_def_pos), focus_point)
            max_pitch, min_pitch = new_conf.get('pitch')
            self.cam_state.max_pitch_radian = math.radians(max_pitch)
            self.cam_state.min_pitch_radian = math.radians(min_pitch)
            max_pitch_radian = self.cam_state.get_real_max_pitch_radian()
            min_pitch_radian = self.cam_state.get_real_min_pitch_radian()
            rotation_matrix = self.limit_rotate_angle_helper(max_pitch_radian, min_pitch_radian)
            fov = self._cur_fov
            self._pitch = rotation_matrix.pitch
            self._yaw = rotation_matrix.yaw
            self.update_camera_config(new_def_pos, focus_point)
            self.update_real_camera_config(new_def_pos, focus_point)
            if self._default_pos_offset:
                self.modify_default_pos_dist(self._default_pos_offset, False, is_additive=False)
            new_pos = self.get_slerp_target_pos(rotation_matrix, self.cur_target_pos + self.focus_point, self.default_pos)

            def on_switch_callback(*args):
                self._pitch = self.cam.world_rotation_matrix.pitch
                self._yaw = self.cam.world_rotation_matrix.yaw

            if self.cam_state and self.cam_state.TYPE == AIM_MODE:
                self.start_aim_camera_posture_slerp(transfer_time)
            else:
                self.set_slerp_target(math3d.vector(new_pos), rotation_matrix, fov, cost_time=transfer_time, callback=on_switch_callback, delay=delay_time, level=SWITCH_SLERP, model=global_data.cam_model)
            return

    def start_aim_camera_posture_slerp(self, slerp_time=1):

        def check_update_aim_pos():
            if not self.cam_state or not self.cam_state.is_valid() or self.cam_state.TYPE != AIM_MODE:
                self.cancel_aim_camera_posture_timer()
                return
            new_conf = self.cam_state.get_state_enter_setting()
            new_focus = new_conf.get('focus')
            focus_point = math3d.vector(new_focus[0], new_focus[1], new_focus[2])
            new_def_pos = new_conf.get('pos')
            new_def_pos = cal_horizontal_default_pos(math3d.vector(*new_def_pos), focus_point)
            self.update_camera_config(new_def_pos, focus_point)
            self.update_real_camera_config(new_def_pos, focus_point)
            if self._default_pos_offset:
                self.modify_default_pos_dist(self._default_pos_offset, False, is_additive=False)
            new_pos = self.cur_target_pos + self.focus_point
            self.cam.world_position = new_pos

        self.cancel_aim_camera_posture_timer()
        from common.utils.timer import LOGIC
        INTERVAL = 0.03
        tmr = global_data.game_mgr.get_logic_timer()
        self._aim_camera_posture_timer = tmr.register(func=check_update_aim_pos, times=int(slerp_time / INTERVAL), mode=LOGIC, interval=INTERVAL)

    def cancel_aim_camera_posture_timer(self):
        if self._aim_camera_posture_timer is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._aim_camera_posture_timer)
            self._aim_camera_posture_timer = None
        return

    def limit_rotate_angle_helper(self, max_pitch, min_pitch):
        new_pitch = min(max(self._pitch, min_pitch), max_pitch)
        self._pitch = new_pitch
        return math3d.matrix.make_rotation_x(new_pitch) * math3d.matrix.make_rotation_y(self._yaw)

    def set_cur_player_posture(self, posture):
        self.cur_player_posture = posture
        global_data.emgr.switch_camera_posture_event.emit(posture)

    def set_cur_player_role_id(self, role_id):
        self._model_role_id = role_id

    def init_target_pos(self, world_pos, need_immediately):
        self._need_update_target_pos = True
        if self._follow_com:
            self._follow_com.init_target_pos(world_pos)
        if not self._target_pos or need_immediately:
            self._target_pos = world_pos

    def on_target_pos_changed(self, world_pos):
        if self._follow_com and not (self.use_special_target_pos or self.use_special_target_pos_for_judge):
            self._follow_com.update_follow_target_pos(world_pos)

    def on_set_target_pos_for_special_logic(self, world_pos):
        if self._follow_com and (self.use_special_target_pos or self.use_special_target_pos_for_judge):
            self._follow_com.update_follow_target_pos(world_pos)

    def _on_update_camera_pos(self, delta_time):
        if self._need_update_target_pos:
            if self._target_pos:
                diff_vec = None
                if self._follow_com:
                    diff_vec = self._follow_com.get_asymptotic_follow_pos(self._target_pos, delta_time, self.cam)
                return diff_vec or None
            self._target_pos += diff_vec
            if not self.is_upload_invalid_camera_world_pos:
                if math.isnan(self._target_pos.x) or math.isinf(self._target_pos.x):
                    self.is_upload_invalid_camera_world_pos = True
                    if self._follow_com:
                        follow_target_pos = self._follow_com.get_follow_target_pos() if 1 else None
                        raise ValueError('invalid camera pos', str(self._target_pos), str(diff_vec), str(follow_target_pos))
                if self.is_in_cam_slerp():
                    self.cam_slerp_method.on_target_pos_changed(diff_vec)
                else:
                    self.cam.world_position += diff_vec
                self.cam_state.target_pos_changed(self._target_pos)
                self._is_need_camera_collision_check = True
                self._refresh_3d_listener_ditry = True
            else:
                self._target_pos = self._follow_com.get_follow_target_pos() if self._follow_com else None
        return

    def _refresh_3d_listener(self):
        if self._refresh_3d_listener_ditry and self.cam:
            transform = self.cam.transformation
            global_data.sound_mgr.set_3d_listener(transform.translation, transform.forward, transform.up)
            self._refresh_3d_listener_ditry = False

    def modify_default_pos_dist(self, dist_offset, is_temporary=False, is_additive=False):
        if is_additive:
            dist_offset += self._default_pos_offset
        pos_dir_vec = self._real_default_pos - self.focus_point
        cur_length = pos_dir_vec.length
        new_length = cur_length + dist_offset
        pos_dir_vec.normalize()
        default_pos = pos_dir_vec * new_length + self.focus_point
        if not is_temporary:
            self._default_pos_offset = dist_offset
            self.update_camera_config(default_pos, self.focus_point)
        return default_pos

    def modify_camera_parameters(self, camera_param_offset, pos_offset, fov_offset):
        if not self._real_default_pos:
            return
        else:
            if camera_param_offset is not None:
                new_focus = math3d.vector(self._real_focus_point)
                new_focus.y += camera_param_offset.y
                new_def = math3d.vector(camera_param_offset + self._real_default_pos)
                default_pos = cal_horizontal_default_pos(new_def, new_focus)
                self.update_camera_config(default_pos, new_focus)
            if pos_offset is not None:
                self._ex_world_offset = pos_offset
            old_remain_time = self.cam_slerp_method.get_slerp_remain_time()
            if old_remain_time > 1 / 30.0:
                old_remain_time -= 1 / 30.0

            def end_callback(*args):
                pass

            self._play_camera_parameters_ani(self.default_pos, self._cur_fov, old_remain_time, end_callback, is_sphere=self.cam_slerp_method.get_is_sphere(), delay=0)
            return

    def _play_camera_parameters_ani(self, default_pos, fov, cost_time, _end_callback=None, is_sphere=False, delay=0):
        mat = math3d.matrix.make_rotation_z(self.__roll) * (math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw))
        new_pos = self.get_slerp_target_pos(mat, self.cur_target_pos + self.focus_point, default_pos)
        if callable(_end_callback):
            if not self._prev_cam_state_slerp_end_cb:
                self._prev_cam_state_slerp_end_cb = None
            if not self._prev_cam_state_slerp_end_cb:
                if self.in_slerp_between_cam_states():
                    prev_cam_state_slerp_end_cb = self.cam_slerp_method.get_camera_slerp_callback()
                    if callable(prev_cam_state_slerp_end_cb):
                        self.cam_slerp_method.replace_camera_slerp_callback(None)
                        self._prev_cam_state_slerp_end_cb = prev_cam_state_slerp_end_cb

            def wrapper(is_finish):
                if callable(self._prev_cam_state_slerp_end_cb):
                    cb = self._prev_cam_state_slerp_end_cb
                    self._prev_cam_state_slerp_end_cb = None
                    cb(is_finish)
                if is_finish:
                    self._pitch = self.cam.world_rotation_matrix.pitch
                    self._yaw = self.cam.world_rotation_matrix.yaw
                _end_callback(is_finish)
                return

            end_callback = wrapper
        else:
            end_callback = None
            self._prev_cam_state_slerp_end_cb = None
        if is_sphere:
            rotate_center = self.focus_point + self.cur_target_pos
            self.set_slerp_target(new_pos, mat, fov, cost_time, callback=end_callback, is_sphere=is_sphere, rotate_center=rotate_center, delay=delay)
        else:
            self.set_slerp_target(new_pos, mat, fov, cost_time, callback=end_callback, delay=delay)
        return

    def set_yaw_with_duration(self, to_yaw, need_slerp=False, cost_time=0.3):
        self.set_target_angle_with_rotation(to_yaw, self._pitch, need_slerp, cost_time)

    def set_pitch_with_duration(self, to_pitch, need_slerp=False, cost_time=0.3):
        self.set_target_angle_with_rotation(self._yaw, to_pitch, need_slerp, cost_time)

    def set_target_angle_with_rotation(self, to_yaw, to_pitch, need_slerp=False, cost_time=0.3):
        input_yaw = to_yaw
        input_pitch = to_pitch
        if to_yaw is None:
            to_yaw = self._yaw
        if to_pitch is None:
            to_pitch = self._pitch

        def on_slerp_success(is_finish):
            if is_finish:
                self._pitch = self.cam.world_rotation_matrix.pitch
                self._yaw = self.cam.world_rotation_matrix.yaw

        if math.isnan(to_pitch) or math.isinf(to_pitch):
            self.report_error(self.cam_state.TYPE, self.focus_point, self.cur_target_pos, to_pitch, to_yaw)
            to_pitch = 0
        if math.isnan(to_yaw) or math.isinf(to_yaw):
            self.report_error(self.cam_state.TYPE, self.focus_point, self.cur_target_pos, to_pitch, to_yaw)
            to_yaw = 0
        if not self.focus_point or not self.cur_target_pos:
            self._yaw = to_yaw
            max_pitch_radian = self.cam_state.get_real_max_pitch_radian()
            min_pitch_radian = self.cam_state.get_real_min_pitch_radian()
            to_pitch = min(max(to_pitch, min_pitch_radian), max_pitch_radian)
            self._pitch = to_pitch
            return
        else:
            rotate_center = self.focus_point + self.cur_target_pos
            if math.isnan(to_pitch) or math.isinf(to_pitch):
                self.report_error(self.cam_state.TYPE, self.focus_point, self.cur_target_pos, to_pitch, to_yaw)
                to_pitch = 0
            if math.isnan(to_yaw) or math.isinf(to_yaw):
                self.report_error(self.cam_state.TYPE, self.focus_point, self.cur_target_pos, to_pitch, to_yaw)
                to_yaw = 0
            max_pitch_radian = self.cam_state.get_real_max_pitch_radian()
            min_pitch_radian = self.cam_state.get_real_min_pitch_radian()
            to_pitch = min(max(to_pitch, min_pitch_radian), max_pitch_radian)
            rot_mat = math3d.matrix.make_rotation_x(to_pitch) * math3d.matrix.make_rotation_y(to_yaw)
            new_pos = self.get_slerp_target_pos(rot_mat, rotate_center)
            axises = [
             rot_mat.rotation.forward, rot_mat.rotation.up,
             rot_mat.rotation.right]
            for ax in axises:
                if ax.is_zero:
                    self.report_error(rot_mat, new_pos, self.cam_state.TYPE, input_yaw, input_pitch, to_yaw, to_pitch, self._yaw, self._pitch, self.focus_point, self.cur_target_pos, max_pitch_radian, min_pitch_radian)
                    return

            self._yaw = to_yaw
            self._pitch = to_pitch
            if not need_slerp or cost_time <= 0.05:
                if not self.is_in_cam_slerp():
                    self.refresh_yaw_pitch()
                else:
                    self._update_slerp_target(cost_time=cost_time)
            elif cost_time > 0.05:
                if not self.is_in_cam_slerp():
                    self.set_slerp_target(new_pos, rot_mat, self._cur_fov, cost_time=cost_time, callback=on_slerp_success, is_sphere=True, rotate_center=rotate_center, delay=0, level=SWITCH_SLERP)
                else:
                    self._update_slerp_target(cost_time=cost_time)
            return

    def get_slerp_target_pos(self, rot_mat, rotate_center, default_pos=None):
        cur_default_pos = default_pos and default_pos if 1 else self.default_pos
        new_pos = rotate_by_center(cur_default_pos + self.cur_target_pos, rotate_center, rot_mat)
        coll_pos, ratio = self.get_collision_point_with_record(self.cur_target_pos, new_pos, rot_mat, self._world_offset)
        new_pos = coll_pos if coll_pos else new_pos
        return new_pos

    def is_in_cam_slerp(self):
        return self.cam_slerp_method.is_in_cam_slerp_event

    def is_out_cam_state_slerp(self, from_state):
        return self._cam_state_slerp_state[0] == from_state

    def get_slerp_cam_states(self):
        return self._cam_state_slerp_state

    def in_slerp_between_cam_states(self):
        return self._cam_state_slerp_state and self._cam_state_slerp_state[0] and self._cam_state_slerp_state[1]

    def is_only_fov_slerp(self):
        return self.cam_slerp_method.is_only_fov_slerp

    def is_free_type_camera(self, camera_type):
        return camera_type in camera_const.FREE_CAMERA_TYPE

    def get_is_free_type_camera(self):
        return self.is_free_type_camera(self.cam_state.TYPE)

    def set_camera_offset(self, offset, immediately=True):
        old_offset = self._world_offset
        self._first_world_offset = offset
        self._is_need_camera_collision_check = True
        if immediately:
            offset_diff = self._world_offset - old_offset
            if self.is_in_cam_slerp():
                self.cam_slerp_method.on_target_pos_changed(offset_diff)
            else:
                self.cam.world_position += offset_diff

    def set_camera_trk_fov_offset(self, fov_offset):
        if self._track_fov_offset == fov_offset:
            return
        self._track_fov_offset = fov_offset
        new_fov = self.cam.fov + fov_offset
        self.cam.fov = new_fov

    def play_camera_animation(self, forward_offset, abs_offset, abs_fov_offset, cost_time, end_callback, is_temporary=False, is_additive=True):
        if not self.cam_ani_enable:
            return
        else:
            if not self.focus_point or not self.cur_target_pos:
                return
            if forward_offset is not None:
                new_default_pos = self.modify_default_pos_dist(forward_offset, is_temporary=is_temporary, is_additive=is_additive)
            else:
                new_default_pos = self.default_pos
            if abs_fov_offset is not None:
                from logic.gutils.CameraHelper import cal_vertical_fov
                new_fov = cal_vertical_fov(self._default_hfov + abs_fov_offset)
                self._vfov_offset = new_fov - cal_vertical_fov(self._default_hfov)
            else:
                new_fov = self._cur_fov
            self._cur_fov = new_fov
            self._play_camera_parameters_ani(new_default_pos, new_fov, cost_time, end_callback)
            return

    def slerp_into_setupped_camera_event(self, cost_time, is_slerp=False, delay=0):
        if not self.focus_point or not self.cur_target_pos:
            return
        else:
            self._play_camera_parameters_ani(self.default_pos, self._cur_fov, cost_time, None, is_sphere=is_slerp, delay=delay)
            return

    def set_up_camera_pos_parameters(self, forward_offset, abs_offset=None, fov_offset=None):
        if not self.focus_point or not self.cur_target_pos:
            return
        else:
            if forward_offset is not None:
                self.modify_default_pos_dist(forward_offset, is_temporary=False, is_additive=True)
            from logic.gutils.CameraHelper import cal_vertical_fov
            if fov_offset is not None:
                new_fov = cal_vertical_fov(self._default_hfov + fov_offset)
                self._vfov_offset = new_fov - cal_vertical_fov(self._default_hfov)
                self._cur_fov = new_fov
            else:
                self._vfov_offset = 0
                self._cur_fov = cal_vertical_fov(self._default_hfov)
            return

    def play_preset_camera_animation(self, clip_name):
        from .CameraAnimation import CameraAnimationClip
        clip = CameraAnimationClip(clip_name)
        clip.Play()

    def accelerate_camera_slerp_event(self, new_remain_time):
        old_remain_time = self.cam_slerp_method.get_slerp_remain_time()
        if new_remain_time < old_remain_time:
            self.cam_slerp_method.set_slerp_remain_time(new_remain_time)

    def set_collision_slerp_target_pos(self, target_pos, cost_time):
        if not self.is_in_cam_slerp() or self.cam_slerp_method.slerp_level == COLL_SLERP:
            if cost_time <= 0:
                self.cam.world_position = target_pos
            else:
                mat = math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw)
                self.set_slerp_target(target_pos, mat, self._cur_fov, cost_time=cost_time)
        else:
            if cost_time <= 0:
                self.cam.world_position = target_pos
            self._update_slerp_target()

    def on_before_switch_cam_player(self):
        if self.cam_state:
            self.cam_state.on_before_switch_cam_player()

    def play_added_trk(self, trk_tag, callback=None, custom_data=None, is_custom_trk_instance=False):
        if not self.added_trk_enable:
            return
        if not self._added_trk_component:
            return

        def real_end_callback():
            if callable(callback):
                callback()

        if not is_custom_trk_instance:
            self._added_trk_component.play_preset_trk_animation(trk_tag, real_end_callback, custom_data)
        else:
            self._added_trk_component.play_outer_track(trk_tag, real_end_callback, custom_data)

    def cancel_added_trk(self, trk_tag, run_callback=False, cancel_failed_cb=None):
        if self._added_trk_component:
            self._added_trk_component.cancel_trk_animation(trk_tag, run_callback, cancel_failed_cb)

    def cancel_all_trk(self):
        if self._added_trk_component:
            self._added_trk_component.clear_all_track()
        global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, False)

    def get_added_trk(self, trk_tag):
        if self._added_trk_component:
            return self._added_trk_component.get_animation_tag_trk(trk_tag)

    def play_plot_trk(self, trk_tag, end_callback, custom_data=None):
        self.on_begin_plot()

        def real_end_callback():
            self.clear_plot_effect()
            if end_callback and callable(end_callback):
                end_callback()

        if self._added_trk_component:
            self._added_trk_component.play_preset_trk_animation(trk_tag, real_end_callback)

    def on_begin_plot(self):
        self.is_enable_collision_check = False

    def clear_plot_effect(self):
        self.is_enable_collision_check = True

    def set_additional_transformation(self, trans, fov=None, is_absolute=False, immediately=True):
        if self._is_destroyed:
            return
        else:
            if not is_absolute:
                if fov is not None:
                    self.set_camera_trk_fov_offset(fov)
                add_rot = math3d.matrix_to_rotation(trans.rotation)
                if not self.is_in_cam_slerp():
                    cur_rot = math3d.matrix.make_rotation_z(self.__roll) * (math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw))
                    base_rot = math3d.matrix_to_rotation(cur_rot)
                    offset = base_rot.rotate_vector(trans.translation)
                    self.set_camera_offset(offset, immediately)
                else:
                    if self._real_addition_trk_params:
                        old_add_rot, _, _ = self._real_addition_trk_params
                    else:
                        old_add_rot = math3d.rotation(0, 0, 0, 1)
                    reverse_old_add_rot = get_reverse_rotation(old_add_rot)
                    cam_rot = math3d.matrix_to_rotation(self.cam.world_rotation_matrix)
                    org_rot = cam_rot * reverse_old_add_rot
                    base_rot = org_rot
                    offset = org_rot.rotate_vector(trans.translation)
                    self.set_camera_offset(offset, immediately)
                self._real_addition_trk_params = [add_rot, offset, fov]
                if immediately:
                    ret_rot = base_rot * add_rot
                    ret_mat = math3d.rotation_to_matrix(ret_rot)
                    self.cam.world_rotation_matrix = ret_mat
                    global_data.emgr.camera_trans_change.emit(trans)
                else:
                    self._is_dirty = True
                    self.set_camera_offset(offset, immediately)
                self._addition_trk_trans = [
                 trans, fov, is_absolute, immediately]
            else:
                self.set_camera_transformation(trans)
            self.check_camera_transformation_matrix_is_valid()
            return

    def set_additional_transformation_end(self):
        self._addition_trk_trans = None
        self._real_addition_trk_params = None
        return

    def set_camera_transformation(self, trans):
        self.cam.transformation = trans

    def _check_collision_tick(self):
        if self._is_need_camera_collision_check:
            self._check_collision()

    def set_hoz_fov(self, fov, change_cam=False):
        if fov is None:
            fov = self._default_hfov
        from logic.gutils.CameraHelper import cal_vertical_fov
        new_fov = cal_vertical_fov(fov)
        self._vfov_offset = 0
        self._cur_fov = new_fov
        if change_cam:
            self.cam.fov = self._cur_fov
        return

    def on_net_reconnect(self, *args):
        tm = global_data.game_mgr.get_post_logic_timer()
        tm.unregister(self._update_timer_id)
        camera_hosting = global_data.emgr.is_launch_boost_updating_camera.emit()
        if camera_hosting:
            camera_hosting = camera_hosting[0]
        if not camera_hosting:
            self._update_timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self.check_update, interval=1, timedelta=True)

    def stop_update_timer(self):
        global LAST_STOP_CAMERA_UPDATE_TRACE_STR
        tm = global_data.game_mgr.get_post_logic_timer()
        if self._update_timer_id > 0:
            tm.unregister(self._update_timer_id)
            self._update_timer_id = -1
            import traceback
            LAST_STOP_CAMERA_UPDATE_TRACE_STR = traceback.format_stack()

    def refresh_update_timer(self):
        tm = global_data.game_mgr.get_post_logic_timer()
        if self._update_timer_id > 0:
            tm.unregister(self._update_timer_id)
        self._update_timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self.check_update, interval=1, timedelta=True)
        self._need_update_target_pos = True

    def bind_to_model_socket(self, model, socket):
        if model and model.valid:
            old_world_pos = self.cam.world_position
            scn = world.get_active_scene()
            self.cam.remove_from_parent()
            res = model.bind(socket, self.cam)
            if not res:
                log_error('Camera Bind Failed!!!')
            scn.active_camera = self.cam
            self.cam.world_position = old_world_pos
        else:
            log_error('Bind_to_model_socket:Invalid Model!!!!')

    def bind_to_scene(self):
        if self.cam.valid:
            if not self.cam.get_parent():
                return
            old_world_trans = self.cam.world_transformation
            self.cam.remove_from_parent()
            scn = world.get_active_scene()
            scn.add_object(self.cam)
            scn.active_camera = self.cam
            self.cam.world_transformation = old_world_trans
        else:
            log_error('need create new camera!')

    def camera_enable_ctrl_viewpos(self, is_enable):
        self._is_enable_ctrl_viewpos = is_enable

    def get_camera_ctrl_view_pos_enabled(self):
        if self._update_timer_id == -1:
            return (self._is_enable_ctrl_viewpos, '\n' + str(LAST_STOP_CAMERA_UPDATE_TRACE_STR) + '\n')
        else:
            return (
             self._is_enable_ctrl_viewpos, True, self._world_offset, self.viewer_dir_offset)

    def camera_enable_follow(self, is_enable):
        if self.lock_enable_follow:
            return
        if self._follow_com:
            if not is_enable:
                self._follow_com.on_change_target_follow_speed(0)
            elif self._follow_com.get_follow_target_speed() <= 0:
                self._follow_com.recover_to_default_speed(0)

    def check_newest_target_pos(self):
        if self._follow_com:
            self._target_pos = self._follow_com.get_follow_target_pos()

    def get_checkable_world_offset(self, world_offset):
        THRES = 5
        if world_offset and world_offset.length > THRES:
            return world_offset
        return world_offset

    def check_refresh_yaw_and_pitch(self):
        self.refresh_yaw_pitch()

    def set_vertical_col_checked(self, checked):
        if self.cam_coll_checker:
            self.cam_coll_checker.check_vertical_col = checked

    def do_end_slerp_camera_early(self, with_sync=True, do_callback=True):
        if self.is_in_cam_slerp():
            self.cam_slerp_method.end_slerp_camera_early(with_sync, do_callback)

    def on_change_target_follow_speed(self, is_enable, new_speed, last_time=10, recover_time=0.2, mode=None, extra_info=None):
        if self._follow_com:
            if is_enable:
                self._follow_com.on_change_target_follow_speed(new_speed, last_time, recover_time, mode, extra_info)
            else:
                self._follow_com.recover_to_default_speed(recover_time)

    def force_set_last_camera_trans(self, trans):
        self.last_camera_state_setting['trans'] = trans
        player = global_data.player
        if player and player.logic:
            ctrl_target = player.logic.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                ctrl_target.logic.send_event('E_CAM_YAW', trans.yaw)
                ctrl_target.logic.send_event('E_CAM_PITCH', trans.pitch)

    def _record_old_camera_transformation(self):
        self._old_cam_world_rot_mat = self.cam.world_rotation_matrix
        global_data.cam_world_transform = self.cam.world_transformation
        global_data.cam_state_type = self.get_cur_camera_state_type()

    def check_camera_transformation_matrix_is_valid(self):
        mat = self.cam.world_rotation_matrix
        if mat.forward.is_zero or mat.up.is_zero or mat.right.is_zero:
            raise ValueError('zero axises!!!', mat, self._old_cam_world_rot_mat)

    def set_slerp_target(self, tar_pos, tar_rotation, tar_fov=None, cost_time=0.2, callback=None, is_sphere=False, rotate_center=None, delay=0, slerp_end_pt=None, level=COLL_SLERP, model=None, start_trans=None, **kwargs):
        if not tar_fov:
            tar_fov = self._cur_fov
        self.cam_slerp_method.set_slerp_target(tar_pos, tar_rotation, tar_fov, cost_time, callback, is_sphere, rotate_center, delay, slerp_end_pt, level, model, start_trans, None, **kwargs)
        return

    def set_slerp_target_spped_action(self, type_str, type_parameter):
        if self.cam_slerp_method and self.is_in_cam_slerp():
            self.cam_slerp_method.set_slerp_action_str(type_str, type_parameter)

    def set_slerp_camera_setting(self, transform, fov):
        self.cam.transformation = transform
        if fov:
            self.set_show_fov(fov)
        global_data.sound_mgr.set_3d_listener(transform.translation, transform.forward, transform.up)
        self.check_camera_transformation_matrix_is_valid()

    def slerp_end_common_callback(self, is_finsih):
        pass

    def on_switch_cam_lplayer(self, role_id):
        self.set_cur_player_role_id(role_id)
        self.set_additional_transformation(math3d.matrix(), 0)
        if self._added_trk_component:
            self._added_trk_component.clear_all_track()
        self._follow_com.recover_to_default_speed(0)
        self._need_update_target_pos = False
        self._ex_world_offset = math3d.vector(0, 0, 0)
        self.__roll = 0

    def out_pos(self, pos):
        if pos:
            return '<%.2f, %.2f, %.2f>' % (pos.x, pos.y, pos.z)
        else:
            return str(None)

    def get_state_enter_setting(self, camera_state=None):
        camera_state = self.cam_state if camera_state is None else camera_state
        if camera_state and camera_state.is_valid():
            camera_conf = camera_state.get_state_enter_setting()
            return camera_conf
        else:
            return {}
            return

    def report_error(self, *args):
        raise ValueError('This should not happened', str(args))

    def enable_special_target_pos_logic(self, enable):
        self.use_special_target_pos = enable

    def enable_special_target_pos_logic_for_judge(self, enable):
        self.use_special_target_pos_for_judge = enable

    def enable_target_pos_update(self, enable):
        self._need_update_target_pos = enable

    def get_default_hfov(self):
        return self._default_hfov

    def get_default_cam_focus(self):
        return self._real_focus_point

    def get_default_cam_pos(self):
        return self._real_default_pos

    def set_is_enable_collision_check(self, val):
        self.is_enable_collision_check = val

    def stop_update_camera(self):
        self.stop_update_timer()

    def add_log_to_log_panel(self, txt):
        from logic.comsys.test.LogPanelUI import LogPanelUI
        LogPanelUI().add_log(txt, True)

    def on_frame_rate_changed(self):
        if self._follow_com:
            self._follow_com.on_frame_rate_changed()