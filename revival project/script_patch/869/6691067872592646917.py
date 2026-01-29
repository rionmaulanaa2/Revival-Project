# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/FreeflyCameraController.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import game
import world
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.vscene.parts.keyboard.CameraDirectionKeyboardHelper import CameraDirectionKeyboardHelper
from common.framework import Singleton
from logic.gutils.CameraHelper import track_build, cal_horizontal_fov, normalize_angle, get_camera_transform_matrix, rotate_by_center
import logic.vscene.parts.ctrl.GamePyHook as game_hook
import math
import six
SPHERE = 1
SPLINE = 2

class ComSlerp(object):

    def __init__(self):
        self._slerp_target_list = []
        self._cur_view_index = -1
        self._slerp_speed = 1
        self._slerp_type = SPLINE
        self._slerp_rotate_center = None
        self._recorded_cam_info = []
        self._cam_info_cost_time = []
        self.cur_draw_pri_list = []
        self._cur_trk = None
        self._into_modify_index = -1
        self.key_ctrls = []
        self._hot_key_map = {game.VK_NUM_SUB: self.remove_last_track_point,
           game.VK_NUM_ADD: self.insert_track_point,
           game.VK_NUMDOT: self.view_current_tracks,
           game.VK_NUMMUL: self.rotate_view_cam_target_model,
           game.VK_NUMDIV: self.reset,
           game.VK_Y: self.remove_last_track_point,
           game.VK_U: self.insert_track_point,
           game.VK_I: self.view_current_tracks,
           game.VK_O: self.rotate_view_cam_target_model,
           game.VK_P: self.reset
           }
        return

    def get_hotkey_list(self):
        return six_ex.keys(self._hot_key_map)

    def on_hot_key(self, msg, keycode):
        if msg == game.MSG_KEY_DOWN:
            if keycode in self._hot_key_map:
                func = self._hot_key_map[keycode]
                func()

    def destroy(self):
        self.reset()

    def reset(self):
        self._slerp_target_list = []
        self._cur_view_index = -1
        self._slerp_speed = 1
        self._slerp_type = SPLINE
        self._slerp_rotate_center = None
        self._recorded_cam_info = []
        self._cam_info_cost_time = []
        self._cur_trk = None
        self._into_modify_index = -1
        self.remove_points()
        return

    def rotate_view_cam_target_model(self):
        model = global_data.cam_lctarget.ev_g_model()
        if not model:
            global_data.game_mgr.show_tip('\xe6\x89\xbe\xe4\xb8\x8d\xe5\x88\xb0\xe6\xa8\xa1\xe5\x9e\x8b\xef\xbc\x8c\xe8\xaf\xb7\xe7\xa1\xae\xe8\xae\xa4\xe5\xb7\xb2\xe7\xbb\x8f\xe5\x87\xba\xe7\x8e\xb0\xef\xbc\x81')
            return
        t_ls, rotate_center = self.generate_rotate_view_model_time_mat(model, 20)
        self._slerp_type = SPHERE
        self.view_tracks_with_conf(t_ls, self._slerp_speed, SPHERE, rotate_center)

    def generate_rotate_view_cam_target_model_trk(self):
        model = global_data.cam_lctarget.ev_g_model()
        if not model:
            global_data.game_mgr.show_tip('\xe6\x89\xbe\xe4\xb8\x8d\xe5\x88\xb0\xe6\xa8\xa1\xe5\x9e\x8b\xef\xbc\x8c\xe8\xaf\xb7\xe7\xa1\xae\xe8\xae\xa4\xe5\xb7\xb2\xe7\xbb\x8f\xe5\x87\xba\xe7\x8e\xb0\xef\xbc\x81')
            return []
        t_ls, rotate_center = self.generate_rotate_view_model_time_mat(model, 20)
        self._recorded_cam_info = t_ls
        self.update_trk_show()

    def get_trans_by_rot(self, cam, rotate_center, degree):
        rotation_matrix = math3d.matrix.make_rotation_y(math.radians(degree))
        start_trans = cam.world_transformation
        start_pos = start_trans.translation
        p = rotate_by_center(start_pos, rotate_center, rotation_matrix)
        r = cam.world_transformation.rotation * rotation_matrix.rotation
        trans = get_camera_transform_matrix(p, r)
        return trans

    def generate_rotate_view_model_time_mat(self, model, step, rotate_center_bone_or_socket='bip001_head', rotate_offset_y=0):
        trans = self.get_model_socket_or_bone_trans(model, rotate_center_bone_or_socket)
        if trans:
            rotate_center = trans.translation
        else:
            rotate_center = model.world_position
        rotate_center.y += rotate_offset_y
        cam = global_data.game_mgr.scene.active_camera
        fov = cam.fov
        degs = list(range(0, 380, step))
        print('deg', degs)
        t_ls = [ [self.get_trans_by_rot(cam, rotate_center, d), fov] for d in degs ]
        return (
         t_ls, rotate_center)

    def insert_track_point(self):
        if self._into_modify_index < 0:
            cam = global_data.game_mgr.scene.active_camera
            self._recorded_cam_info.append([cam.world_transformation, cam.fov])
            print('new added point ', len(self._recorded_cam_info) - 1, cam.world_position)
            self.update_trk_show()
        else:
            cam = global_data.game_mgr.scene.active_camera
            self._recorded_cam_info[self._into_modify_index] = [cam.world_transformation, cam.fov]
            print('new added point ', len(self._recorded_cam_info) - 1, cam.world_position)
            self.update_trk_show()

    def remove_last_track_point(self):
        if self._recorded_cam_info:
            self._recorded_cam_info.pop(-1)
            print('remain points count ', len(self._recorded_cam_info))
        else:
            print('enmpy points count!')
        self.update_trk_show()

    def clear_track_points(self):
        self._recorded_cam_info = []
        print('clear points')
        self.update_trk_show()

    def setup_track_info(self, speed, slerp_type, rotate_center=None, rotate_center_model=None, rotate_center_bone_or_socket=None):
        self._slerp_speed = speed
        self._slerp_type = slerp_type
        if self._slerp_type == SPHERE:
            if rotate_center_model is None and rotate_center is None:
                global_data.game_mgr.show_tip('\xe4\xbd\xbf\xe7\x94\xa8\xe5\x9c\x86\xe7\x8e\xaf\xe6\x96\xb9\xe5\xbc\x8f\xe7\x8e\xaf\xe7\xbb\x95\xe6\x97\xb6\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe4\xbc\xa0\xe5\x85\xa5\xe7\x8e\xaf\xe7\xbb\x95\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x92\x8c\xe6\x8c\x82\xe7\x82\xb9\xe6\x88\x96\xe8\x80\x85\xe6\x8c\x87\xe5\xae\x9a')
                return
            if rotate_center:
                self._slerp_rotate_center = rotate_center
            else:
                trans = self.get_model_socket_or_bone_trans(rotate_center_model, rotate_center_bone_or_socket)
                if not trans:
                    global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b\xe6\x97\xa0\xe8\xaf\xa5\xe6\x8c\x82\xe7\x82\xb9\xe6\x88\x96\xe8\xaf\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xef\xbc\x81')
                    return
                self._slerp_rotate_center = trans.translation
        return

    def view_current_tracks(self):
        if not self._recorded_cam_info:
            print('empty record cam info, can not preview')
            return
        self.view_tracks_with_conf(self._recorded_cam_info, self._slerp_speed, self._slerp_type)

    def get_intersect_point(self, p0, dir0, p1, dir1):
        y = (p0.y + p1.y) / 2.0
        dir0 = math3d.vector(dir0)
        dir0.y = 0
        dir0.normalize()
        dir1 = math3d.vector(dir1)
        dir1.y = 0
        dir1.normalize()
        eps = 0.0001
        if abs(dir0.x) < eps or abs(dir0.z) < eps or abs(dir1.x) < eps or abs(dir1.z) < eps:
            global_data.game_mgr.show_tip('\xe6\x9c\x89\xe5\x9e\x82\xe7\x9b\xb4\xe8\xa7\x86\xe8\xa7\x92\xe7\x9a\x84\xe5\x9e\x82\xe7\xba\xbf\xef\xbc\x8c\xe6\x9a\x82\xe6\x9c\xaa\xe5\xae\x9e\xe7\x8e\xb0')
            if abs(dir0.x) < eps:
                return p0 + dir0 * 30
        else:
            k0 = dir0.z / dir0.x
            b0 = p0.z - k * p0.x
            k1 = dir1.z / dir1.x
            b0 = p1.z - k * p1.x
            x = (b1 - b0) / (k0 - k1)
            z = k0x + b0
        return math3d.vector(x, y, z)

    def get_model_socket_or_bone_trans(self, model, bone_or_socket):
        if model.has_bone(bone_or_socket):
            _mat = math3d.matrix(model.get_bone_matrix(bone_or_socket, world.SPACE_TYPE_WORLD))
            return _mat
        else:
            if model.has_socket(bone_or_socket):
                _mat = model.get_socket_matrix(bone_or_socket, world.SPACE_TYPE_WORLD)
                return _mat
            return None
            return None

    def view_tracks_with_conf(self, conf, speed, slerp_type, rotate_center=None, rotate_center_model=None, rotate_center_bone_or_socket='bip001_head'):
        if len(conf) <= 0:
            return
        else:
            self._slerp_target_list = conf
            self._cur_view_index = 0
            self._slerp_speed = max(speed, 0.0001)
            self._slerp_type = slerp_type
            if self._slerp_type == SPHERE and not self._slerp_rotate_center:
                if rotate_center_model is None and rotate_center is None:
                    global_data.game_mgr.show_tip('\xe4\xbd\xbf\xe7\x94\xa8\xe5\x9c\x86\xe7\x8e\xaf\xe6\x96\xb9\xe5\xbc\x8f\xe7\x8e\xaf\xe7\xbb\x95\xe6\x97\xb6\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe4\xbc\xa0\xe5\x85\xa5\xe7\x8e\xaf\xe7\xbb\x95\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x92\x8c\xe6\x8c\x82\xe7\x82\xb9\xe6\x88\x96\xe8\x80\x85\xe6\x8c\x87\xe5\xae\x9a')
                    return
                if rotate_center:
                    self._slerp_rotate_center = rotate_center
                else:
                    trans = self.get_model_socket_or_bone_trans(rotate_center_model, rotate_center_bone_or_socket)
                    if not trans:
                        global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b\xe6\x97\xa0\xe8\xaf\xa5\xe6\x8c\x82\xe7\x82\xb9\xe6\x88\x96\xe8\xaf\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xef\xbc\x81')
                        return
                    self._slerp_rotate_center = trans.translation
            else:
                world_transformation, fov = conf[self._cur_view_index]
                cam = global_data.game_mgr.scene.active_camera
                global_data.emgr.camera_set_camera_setting_event.emit(world_transformation, fov)
                self.on_slerp_finish_one_point()
            return

    def on_slerp_finish_one_point(self):
        next_index = self._cur_view_index + 1
        if len(self._slerp_target_list) > next_index:
            pre_trans, pre_fov = self._slerp_target_list[self._cur_view_index]
            pre_world_pos = pre_trans.translation
            world_transformation, fov = self._slerp_target_list[next_index]
            world_pos = world_transformation.translation
            rotation = world_transformation.rotation
            if self._slerp_type == SPLINE:
                cost_t = (world_pos - pre_world_pos).length / self._slerp_speed
            else:
                yaw_diff = normalize_angle(pre_trans.yaw - world_transformation.yaw)
                pitch_diff = normalize_angle(pre_trans.pitch - world_transformation.pitch)
                max_angle = max(abs(yaw_diff), abs(pitch_diff))
                cost_t = max_angle / self._slerp_speed

            def on_slerp_success(*args):
                if not self._cur_trk:
                    self.on_slerp_finish_one_point()
                else:
                    self.draw_points()

            is_sphere = self._slerp_type == SPHERE
            self._cur_view_index = next_index
            rotate_center = self._slerp_rotate_center
            if self._slerp_type == SPLINE:
                if self._cur_trk:
                    cost_t = self._cur_trk.duration / 1000.0
                    end_trans = self._cur_trk.get_transform(self._cur_trk.duration)
                    world_pos = end_trans.translation
                    rotation = end_trans.rotation
                global_data.emgr.camera_set_slerp_target_event.emit(world_pos, rotation, fov, cost_t, on_slerp_success, is_sphere, rotate_center=rotate_center, trk=self._cur_trk)
                self.remove_points()
            else:
                global_data.emgr.camera_set_slerp_target_event.emit(world_pos, rotation, fov, cost_t, on_slerp_success, is_sphere, rotate_center=rotate_center)

    def set_time(self, cost_time_ls):
        self._cam_info_cost_time = cost_time_ls
        self.update_trk_show()

    def modify_point_index(self, index, is_into):
        if is_into:
            self._into_modify_index = index
            if index < len(self._recorded_cam_info):
                trans, fov = self._recorded_cam_info[index]
                global_data.emgr.camera_set_camera_setting_event.emit(trans, fov)
        else:
            self._into_modify_index = None
        return

    def show_info(self):
        print('point details')
        for idx, i in enumerate(self._recorded_cam_info):
            trans, fov = i
            print('index ', idx, trans.translation, trans.yaw, trans.pitch, trans.yaw)

        print('cost time details')
        print(self._cam_info_cost_time)

    def bound_same_height(self):
        fix_height = 0
        new_ls = []
        for idx, i in enumerate(self._recorded_cam_info):
            trans, fov = self._recorded_cam_info[idx]
            if idx == 0:
                fix_height = trans.translation.y
            else:
                trans.translation = math3d.vector(trans.translation.x, fix_height, trans.translation.z)
            new_ls.append([trans, fov])

        self._recorded_cam_info = new_ls
        self.update_trk_show()

    def bound_same_pitch_and_zero_roll(self):
        fix_pitch = 0
        new_ls = []
        for idx, i in enumerate(self._recorded_cam_info):
            trans, fov = self._recorded_cam_info[idx]
            if idx == 0:
                fix_pitch = trans.pitch
            trans.rotation = math3d.matrix.make_rotation_x(fix_pitch) * math3d.matrix.make_rotation_y(trans.yaw)
            new_ls.append([trans, fov])

        self._recorded_cam_info = new_ls
        self.update_trk_show()

    def update_trk_show(self):
        cur_cost_t = -1
        t_mat_list = []
        for idx, info in enumerate(self._recorded_cam_info):
            if idx < len(self._cam_info_cost_time):
                cost_time = self._cam_info_cost_time[idx]
                cur_cost_t = cost_time
                t_mat_list.append([cost_time, info[0]])
            else:
                cost_time = cur_cost_t + 1
                cur_cost_t = cost_time
                t_mat_list.append([cur_cost_t, info[0]])

        if len(self._recorded_cam_info) >= 3:
            duration = round(cur_cost_t * 1000.0 / 33.33333333) * 33.333333333
            self._cur_trk = track_build(t_mat_list, duration)
        self.draw_points()

    def draw_points(self):
        if global_data.disable_draw_camera_point:
            return
        self.remove_points()
        self.cur_draw_pri_list = []
        for idx, info in enumerate(self._recorded_cam_info):
            trans = info[0]
            ret = global_data.emgr.scene_draw_wireframe_event.emit(trans.translation, trans.rotation, alive_time=-1)
            if ret:
                self.cur_draw_pri_list.append(ret[0])

        if self._cur_trk:
            duration = self._cur_trk.duration
            dt = 0
            pts = []
            while dt * 1000 < duration:
                cur_trans = self._cur_trk.get_transform(dt)
                pts.append(cur_trans.translation)
                dt += 0.2

            ret = global_data.emgr.scene_draw_line_event.emit(pts, alive_time=-1)
            if ret:
                self.cur_draw_pri_list.append(ret[0])

    def remove_points(self):
        if self.cur_draw_pri_list:
            for pri in self.cur_draw_pri_list:
                if pri and pri.valid:
                    pri.remove_from_parent()

        self.cur_draw_pri_list = []


class FreeflyCameraController(Singleton):
    ALIAS_NAME = 'freefly_camera_mgr'

    def init(self):
        self._camera_direction_helper = CameraDirectionKeyboardHelper()
        self._is_enable = False
        self.update_timer_id = None
        self._is_binded = False
        self.delta_y_angle = 5.0
        self.delta_x_angle = 2.0
        self._mouse_ctrl = None
        self.old_move_step = math3d.vector(0, 0, 0)
        self.old_fov_step = 0
        self.cur_fov_step = 0
        self.cur_yaw_step = 0
        self.cur_pitch_step = 0
        self.old_yaw_step = 0
        self.old_pitch_step = 0
        self.cur_fov_dir = 0
        self.old_rotate_func = None
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        global_data.emgr.switch_control_target_event += self._on_ctrl_target_changed
        global_data.emgr.on_player_leave_skate += self.on_player_leave_skate
        global_data.emgr.scene_camera_player_setted_event += self.on_player_changed
        self._recorded_cam_info = []
        self._coms = []
        self._com_slerp = ComSlerp()
        self._coms.append(self._com_slerp)
        self._com_keys = []
        for com in self._coms:
            hk_list = com.get_hotkey_list()
            self._com_keys.extend(hk_list)

        return

    def destroy(self):
        self.old_rotate_func = None
        self._camera_direction_helper.destroy()
        self._camera_direction_helper = None
        if self._mouse_ctrl:
            self._mouse_ctrl.disable()
            self._mouse_ctrl.uninstall()
            self._mouse_ctrl.destroy()
            self._mouse_ctrl = None
        for key_ctrl in self.key_ctrls:
            key_ctrl.disable()
            key_ctrl.uninstall()

        self.key_ctrls = []
        return

    def clear_steps(self):
        self.old_move_step = math3d.vector(0, 0, 0)
        self.old_fov_step = 0
        self.old_yaw_step = 0
        self.old_pitch_step = 0
        self.cur_fov_step = 0
        self.cur_yaw_step = 0
        self.cur_pitch_step = 0
        self.old_yaw_step = 0
        self.old_pitch_step = 0
        self.cur_fov_dir = 0

    def enable(self):
        self.quick_trk_key_list = {game.VK_UP: game.VK_W,game.VK_LEFT: game.VK_A,
           game.VK_DOWN: game.VK_S,
           game.VK_RIGHT: game.VK_D,
           game.VK_NUM_1: game.VK_NUM_1,
           game.VK_NUM_4: game.VK_NUM_4
           }
        self.keycode_rotate_map = {game.VK_NUM5: game.VK_DOWN,
           game.VK_NUM8: game.VK_UP,
           game.VK_NUM7: game.VK_LEFT,
           game.VK_NUM9: game.VK_RIGHT
           }
        self.wheel_mock_map = {game.MOUSE_BUTTON_MIDDLE: -1
           }
        self.clear_steps()
        self.init_keyboard_ctrl()
        self._camera_direction_helper.reset()
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.register_wheel_event(self.__class__.__name__, self.on_mouse_scroll)
        from data.camera_state_const import FREE_MODEL, DEBUG_MODE
        global_data.emgr.switch_camera_state_event.emit(DEBUG_MODE)
        self._is_enable = True
        from logic.comsys.control_ui.ShotChecker import ShotChecker
        ShotChecker().do_not_reset_camera_on_fire = True
        global_data.emgr.switch_cam_state_enable_event.emit(False)
        global_data.emgr.camera_switch_collision_check_event.emit(False)
        global_data.emgr.camera_added_trk_enable.emit(False)
        global_data.emgr.camera_on_stop_nearclip.emit()
        import world
        global_data.game_mgr.scene.active_camera.z_range = (10, 10000)

    def disable(self):
        self.recover_keyboard_ctrl()
        self._camera_direction_helper.reset()
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = None
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.unregister_wheel_event(self.__class__.__name__)
        self.unbind()
        global_data.emgr.switch_cam_state_enable_event.emit(True)
        from data.camera_state_const import THIRD_PERSON_MODEL
        global_data.emgr.switch_camera_state_event.emit(THIRD_PERSON_MODEL)
        self._is_enable = False
        from logic.comsys.control_ui.ShotChecker import ShotChecker
        ShotChecker().do_not_reset_camera_on_fire = False
        global_data.emgr.camera_switch_collision_check_event.emit(True)
        global_data.emgr.camera_added_trk_enable.emit(True)
        part_cam = global_data.game_mgr.scene.get_com('PartCamera')
        if part_cam:
            part_cam.cam_manager.refresh_update_timer()
        global_data.emgr.camera_on_start_nearclip.emit()
        return

    def is_enable(self):
        return self._is_enable

    def init_keyboard_ctrl(self):
        partctrl = global_data.game_mgr.scene.get_com('PartCtrl')
        if not partctrl:
            return
        else:
            partctrl.unregister_keys()
            if not self._mouse_ctrl:
                from logic.vscene.parts.mouse.BattleMouse import BattleMouse
                self._mouse_ctrl = BattleMouse()
            self._mouse_ctrl.install()
            self._mouse_ctrl.enable()
            game_hook.add_key_handler(None, six_ex.keys(self.quick_trk_key_list) + six_ex.keys(self.keycode_rotate_map) + self._com_keys, self.on_quick_key)
            if global_data.is_inner_server:
                from logic.vscene.parts.keyboard import MechaKeyboard, CommonKeyboard
                self.key_ctrls = [
                 MechaKeyboard.MechaKeyboard(), CommonKeyboard.CommonKeyboard()]
                for key_ctrl in self.key_ctrls:
                    key_ctrl.install()
                    key_ctrl.enable()

            def rotate_player_camera(ctrl, dx, dy):
                TWO_PI = 2 * math.pi
                if abs(dx) > TWO_PI:
                    dx %= TWO_PI
                if abs(dy) > TWO_PI:
                    dy %= TWO_PI
                self.cur_yaw_step = dx
                self.cur_pitch_step = dy

            self.old_rotate_func = partctrl.rotate_player_camera
            import inspect
            import types
            new_fun = six.create_bound_method(rotate_player_camera, partctrl)
            partctrl.rotate_player_camera = new_fun
            return

    def recover_keyboard_ctrl(self):
        partctrl = global_data.game_mgr.scene.get_com('PartCtrl')
        if not partctrl:
            return
        else:
            import logic.vscene.parts.ctrl.GamePyHook as game_hook
            game_hook.remove_key_handler(None, six_ex.keys(self.quick_trk_key_list) + six_ex.keys(self.keycode_rotate_map) + self._com_keys, self.on_quick_key)
            for key_ctrl in self.key_ctrls:
                key_ctrl.disable()
                key_ctrl.uninstall()

            self.key_ctrls = []
            partctrl.register_keys()
            if self._mouse_ctrl:
                self._mouse_ctrl.disable()
                self._mouse_ctrl.uninstall()
            if self.old_rotate_func:
                partctrl.rotate_player_camera = self.old_rotate_func
                self.old_rotate_func = None
            return

    def on_quick_key(self, msg, keycode):
        if msg == game.MSG_KEY_DOWN:
            self.on_quick_key_down(msg, keycode)
        else:
            self.on_quick_key_up(msg, keycode)

    def on_quick_key_down(self, msg, keycode):
        print('on_quick_key_down', msg, keycode)
        if msg == game.MSG_KEY_DOWN:
            global_data.keys[keycode] = True
        if keycode in self.quick_trk_key_list:
            self.on_key_down(msg, self.quick_trk_key_list[keycode])
        for com in self._coms:
            com.on_hot_key(msg, keycode)

    def on_quick_key_up(self, msg, keycode):
        if msg == game.MSG_KEY_UP:
            global_data.keys[keycode] = False
        if keycode in self.quick_trk_key_list:
            self._camera_direction_helper.move_key_func(msg, self.quick_trk_key_list[keycode])
        for com in self._coms:
            com.on_hot_key(msg, keycode)

    def on_key_down(self, msg, changed_key):
        move_direct = self._camera_direction_helper.move_key_func(msg, changed_key)

    def on_update(self):
        move_dir = self._camera_direction_helper.get_move_direction()
        partcamera = global_data.game_mgr.scene.get_com('PartCamera')
        if not partcamera:
            return
        if move_dir and move_dir.length > 0.001:
            move_dir.normalize()
            cur_target_pos = partcamera.get_target_pos()
            if global_data.camera_freefly_speed:
                speed = global_data.camera_freefly_speed
            else:
                speed = 5.0
            move_step = move_dir * global_data.game_mgr.scene.active_camera.world_rotation_matrix * speed
            new_pos = cur_target_pos + self.old_move_step * 0.5 + move_step * 0.5
            global_data.emgr.set_target_pos_for_special_logic.emit(new_pos)
            self.old_move_dir = move_step
        else:
            self.old_move_dir = math3d.vector(0, 0, 0)
        for keycode in six.iterkeys(self.keycode_rotate_map):
            if global_data.keys.get(keycode):
                self.on_move_camera(self.keycode_rotate_map[keycode])

        if global_data.camera_freefly_fov_speed:
            fov_speed = global_data.camera_freefly_fov_speed
        else:
            fov_speed = 0.3
        has_fov_key_down = False
        cur_fov_step = 0
        for key in six_ex.keys(self.wheel_mock_map):
            if self._mouse_ctrl.get_key_state(key) or game_hook.is_key_down(key):
                has_fov_key_down = True
                cur_fov_step += self.cur_fov_dir * fov_speed

        if has_fov_key_down:
            self.cur_fov_step = cur_fov_step
        else:
            self.cur_fov_dir = 0
        if self.cur_fov_step or self.old_fov_step:
            cur_fov = global_data.game_mgr.scene.active_camera.fov
            cur_fov += (self.cur_fov_step + self.old_fov_step) / 2.0
            self.old_fov_step = self.cur_fov_step
            self.cur_fov_step = 0
            from common.utils.ui_utils import s_designWidth, s_designHeight
            fov = cal_horizontal_fov(cur_fov, s_designWidth, s_designHeight)
            partcamera.cam_manager.set_hoz_fov(fov)
        else:
            self.old_fov_step = 0
            self.cur_fov_step = 0
        if self.cur_yaw_step or self.old_yaw_step or self.cur_pitch_step or self.old_pitch_step:
            partcamera.yaw(self.cur_yaw_step * 0.5 + self.old_yaw_step * 0.5)
            partcamera.pitch((self.cur_pitch_step * 0.5 + self.old_pitch_step * 0.5) * -1)
            self.old_yaw_step = self.cur_yaw_step
            self.old_pitch_step = self.cur_pitch_step
            self.cur_yaw_step = 0
            self.cur_pitch_step = 0

    def on_move_camera(self, keycode):
        scn = global_data.game_mgr.scene
        from data.camera_state_const import FREE_MODEL, AIM_MODE, OBSERVE_FREE_MODE, DEBUG_MODE
        if game.VK_LEFT == keycode or game.VK_RIGHT == keycode:
            DELTA_Y_ANGLE = global_data.debug_camera_delta_y_angle or self.delta_y_angle
            sign = game.VK_LEFT == keycode and -1 or 1
            dx = sign * DELTA_Y_ANGLE * math.pi / 180.0
            com_camera = scn.get_com('PartCamera')
            if com_camera.get_cur_camera_state_type() in (FREE_MODEL, DEBUG_MODE):
                com_camera.yaw(dx)
            else:
                com_camera.yaw(dx)
                player.send_event('E_DELTA_YAW', dx)
        if game.VK_UP == keycode or game.VK_DOWN == keycode:
            DELTA_X_ANGLE = global_data.debug_camera_delta_y_angle or self.delta_x_angle
            sign = game.VK_UP == keycode and -1 or 1
            dx = sign * DELTA_X_ANGLE * math.pi / 180.0
            com_camera = scn.get_com('PartCamera')
            if com_camera.get_cur_camera_state_type() in (FREE_MODEL, DEBUG_MODE):
                com_camera.pitch(dx)
            else:
                com_camera.pitch(dx)
                player.send_event('E_DELTA_PITCH', dx)

    def on_post_update(self):
        active_camera = global_data.game_mgr.scene.active_camera
        parent = active_camera.get_parent()
        if parent:
            skate_model = global_data.cam_lctarget.ev_g_skate_model()
            model = skate_model or global_data.cam_lctarget.ev_g_model()

    def on_mouse_scroll(self, msg, delta, key_state):
        import math
        self.cur_fov_step = delta / 50.0
        self.cur_fov_dir = -1 * math.copysign(1, delta)
        print('on_mouse_scroll', self.cur_fov_step)

    def bind(self, bone_or_socket, bind_type=world.BIND_TYPE_ALL):
        self._bind_info = (
         bone_or_socket, bind_type)
        skate_model = global_data.cam_lctarget.ev_g_skate_model()
        model = skate_model or global_data.cam_lctarget.ev_g_model()
        if not model:
            return
        else:
            cam = global_data.game_mgr.scene.active_camera
            old_world_trans = cam.world_transformation
            scn = world.get_active_scene()
            cam.remove_from_parent()
            res = False
            is_binded = False
            if model.has_bone(bone_or_socket):
                res = model.bind_bone(bone_or_socket, cam, math3d.matrix(), bind_type)
                if res is not None:
                    scn.add_object(cam)
                    scn.active_camera = cam
                else:
                    scn.active_camera = cam
                    bone_mat = math3d.matrix(model.get_bone_matrix(bone_or_socket, world.SPACE_TYPE_WORLD))
                    bone_mat.inverse()
                    cam.transformation = old_world_trans * bone_mat
                    is_binded = True
            if not is_binded and model.has_socket(bone_or_socket):
                res = model.bind(bone_or_socket, cam, bind_type)
                if not res:
                    global_data.game_mgr.show_tip('Camera Bind Failed!!!')
                    scn.add_object(cam)
                    scn.active_camera = cam
                else:
                    scn.active_camera = cam
                    _mat = model.get_socket_matrix(bone_or_socket, world.SPACE_TYPE_WORLD)
                    _mat.inverse()
                    cam.transformation = old_world_trans * _mat
                    is_binded = True
            self._is_binded = is_binded
            if is_binded:
                part_cam = global_data.game_mgr.scene.get_com('PartCamera')
                if part_cam:
                    part_cam.cam_manager.stop_update_timer()
            return

    def unbind(self):
        self._bind_info = None
        import world
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        else:
            old_world_trans = cam.world_transformation
            cam.remove_from_parent()
            scn = world.get_active_scene()
            scn.add_object(cam)
            scn.active_camera = cam
            cam.world_transformation = old_world_trans
            self._is_binded = False
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
            if part_cam:
                part_cam.cam_manager.refresh_update_timer()
            return

    def on_login_reconnect(self):
        if self._is_binded:
            self.unbind()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)

    def _on_ctrl_target_changed(self, *args):
        if self._is_binded:
            self.unbind()

    def on_player_leave_skate(self):
        if self._is_binded:
            self.unbind()

    def on_player_changed(self):
        if not global_data.cam_lctarget or not global_data.cam_lplayer:
            if self._is_binded:
                self.unbind()