# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCamera.py
from __future__ import absolute_import
from __future__ import print_function
import math3d
from . import ScenePart
VIEWER_UPDATE_FRAME = 10
COLL_UPDATE_FRAME = 10
UP_VECTOR = math3d.vector(0, 1, 0)
RIGHT_VECTOR = math3d.vector(1, 0, 0)
YZ_VECTOR = math3d.vector(0, 1, 1)
UPDATE_ACC_DELTA_YAW_LIMIT = 8.0 / 180.0 * 3.1415926
UPDATE_ACC_DELTA_PITCH_LIMIT = 8.0 / 180.0 * 3.1415926
from .camera.SphericalCameraManager import SphericalCameraManager
from .camera.CameraTargetManager import CameraTargetManager
from logic.gcommon.const import NEOX_UNIT_SCALE

class PartCamera(ScenePart.ScenePart):
    ENTER_EVENT = {'on_enter_room_camera_event': 'on_enter_room_camera',
       'on_leave_room_camera_event': 'on_leave_room_camera',
       'on_target_kill_mecha_event': 'on_mecha_killed',
       'get_rotate_center': 'get_rotate_center',
       'try_switch_judge_camera_event': 'switch_judge_camera',
       'set_in_killer_focus_camera_event': 'set_in_killer_focus',
       'enable_camera_kill_mecha': 'enable_camera_kill_mecha'
       }

    def __init__(self, scene, name):
        super(PartCamera, self).__init__(scene, name, True)
        self.coll_update = 0
        self.cam = None
        self.cam_manager = SphericalCameraManager()
        self.cam_target_manager = CameraTargetManager(self.cam_manager)
        self.is_in_killer_focus_camera = False
        self.play_camera_kill_mecha = True
        return

    def on_load(self):
        pass

    def on_enter(self):
        global_data.is_in_judge_camera = False
        self.cam_manager.on_enter()
        self.cam_target_manager.on_enter()
        self.cam = self.cam_manager.cam
        self.register_sub_sys('SysAimPoisonWarning')

    def create_ui(self):
        pass

    def destroy_ui(self):
        if global_data.ui_mgr.get_ui('AimLensUI'):
            global_data.ui_mgr.close_ui('AimLensUI')

    def on_exit(self):
        if global_data.judge_camera_mgr:
            global_data.judge_camera_mgr.finalize()
        global_data.is_in_judge_camera = False
        self.need_update = False
        if self.cam_target_manager:
            self.cam_target_manager.destroy()
            self.cam_target_manager = None
        if self.cam_manager:
            self.cam_manager.on_exit()
            self.cam_manager = None
        self.cam = None
        self.destroy_ui()
        return

    def get_cur_camera_state_type(self):
        if self.cam_manager:
            return self.cam_manager.get_cur_camera_state_type()
        return -1

    def get_cur_camera_magnification_triplet(self):
        if self.cam_manager:
            return self.cam_manager.get_cur_camera_magnification_triplet()
        else:
            return None

    def get_cur_camera_aim_scope_id(self):
        if self.cam_manager:
            return self.cam_manager.get_cur_camera_aim_scope_id()
        return 0

    def get_yaw(self):
        if self.cam_manager:
            return self.cam_manager.get_yaw()
        return 0

    def get_pitch(self):
        if self.cam_manager:
            return self.cam_manager.get_pitch()
        else:
            return 0

    def is_in_cam_slerp(self):
        if self.cam_manager:
            return self.cam_manager.is_in_cam_slerp()
        return False

    def is_out_cam_state_slerp(self, from_state):
        if self.cam_manager:
            return self.cam_manager.is_out_cam_state_slerp(from_state)
        return False

    def get_slerp_cam_states(self):
        if self.cam_manager:
            return self.cam_manager.get_slerp_cam_states()
        else:
            return []

    def is_only_fov_slerp(self):
        if self.cam_manager:
            return self.cam_manager.is_only_fov_slerp()
        return False

    def set_yaw(self, yaw):
        if self.cam_manager:
            self.cam_manager.set_yaw(yaw)

    def set_pitch(self, pitch):
        if self.cam_manager:
            self.cam_manager.set_pitch(pitch)

    def yaw(self, delta):
        if self.cam_manager:
            return self.cam_manager.yaw(delta)

    def pitch(self, delta):
        if self.cam_manager:
            return self.cam_manager.pitch(delta)

    def set_roll(self, value):
        if self.cam_manager:
            return self.cam_manager.set_roll(value)

    def get_is_free_type_camera(self):
        if self.cam_manager:
            return self.cam_manager.get_is_free_type_camera()
        return False

    def switch_cam_state(self, new_cam_type, **kwargs):
        if self.cam_manager:
            self.cam_manager.switch_cam_state(new_cam_type, **kwargs)

    def get_cam_trk_component(self):
        if self.cam_manager:
            return self.cam_manager._added_trk_component

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'on_enter_room_camera_event': self.on_enter_room_camera,
           'on_leave_room_camera_event': self.on_leave_room_camera,
           'on_target_kill_mecha_event': self.on_mecha_killed,
           'get_rotate_center': self.get_rotate_center
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_enter_room_camera(self):
        print('Enter room ...')

    def on_leave_room_camera(self):
        print('Leave room ...')

    @property
    def camera_y_slide_dir(self):
        if self.cam_manager:
            return self.cam_manager.camera_y_slide_dir
        return 1

    def is_free_type_camera(self, camera_type):
        if self.cam_manager:
            return self.cam_manager.is_free_type_camera(camera_type)
        return False

    def get_fov(self):
        return self.cam.fov

    def set_fov(self, fov):
        if self.cam_manager:
            self.cam_manager.cam_state.set_fov(fov)

    def set_pos(self, pos):
        if self.cam_manager:
            self.cam_manager.cam_state.set_pos(pos)

    def get_pos(self):
        return math3d.vector(self.cam.position)

    def get_camera_to_focus_hoz_length(self):
        if not self.cam_manager:
            return None
        else:
            if self.cam_manager.cur_target_pos and self.cam_manager.focus_point:
                rotate_center = self.cam_manager.cur_target_pos + self.cam_manager.focus_point
                dis = self.cam_manager.cam.world_position - rotate_center
                dis.y = 0
                return dis.length
            return None
            return None

    def get_pos_focus_angle(self):
        if not self.cam_manager:
            return None
        else:
            return self.cam_manager.pos_focus_angle

    def on_mecha_killed(self, killer_id, mecha_injured_id, killer_statistics):
        if not global_data.cam_lplayer or not self.play_camera_kill_mecha:
            return
        if global_data.cam_lplayer.id == killer_id:
            global_data.emgr.camera_play_added_trk_event.emit('COMMON_KILL_MECHA')
        elif global_data.cam_lplayer.id == mecha_injured_id:
            global_data.emgr.camera_play_added_trk_event.emit('COMMON_MECHA_DESTROYED')
        else:
            con_target = global_data.cam_lplayer.ev_g_control_target()
            if con_target and con_target.id == mecha_injured_id:
                global_data.emgr.camera_play_added_trk_event.emit('COMMON_MECHA_DESTROYED')

    def get_rotate_center(self):
        if self.cam_manager and self.cam_manager.cur_target_pos and self.cam_manager.focus_point:
            return self.cam_manager.cur_target_pos + self.cam_manager.focus_point
        else:
            return None
            return None

    def get_target_pos(self):
        return self.cam_manager.cur_target_pos

    def get_focus_point_y(self):
        try:
            return self.cam_manager.focus_point.y
        except:
            return 1.0 * NEOX_UNIT_SCALE

    def switch_judge_camera(self, enable, refresh=True, is_force=False):
        if self.is_in_killer_focus_camera:
            return False
        if not global_data.judge_camera_mgr:
            from logic.vscene.parts.camera.JudgeCameraController import JudgeCameraController
            JudgeCameraController()
        if not enable:
            global_data.is_in_judge_camera = enable
            global_data.emgr.switch_judge_camera_event.emit(enable)
            global_data.judge_camera_mgr.disable()
            if refresh:
                global_data.emgr.slerp_into_setupped_camera_event.emit(0)
        elif not global_data.judge_camera_mgr.is_enable():
            if global_data.judge_camera_mgr.check_can_enable() or is_force:
                global_data.is_in_judge_camera = enable
                global_data.emgr.switch_judge_camera_event.emit(enable)
                global_data.judge_camera_mgr.enable()

    def set_in_killer_focus(self, in_kill):
        self.is_in_killer_focus_camera = in_kill

    def enable_camera_kill_mecha(self, flag):
        self.play_camera_kill_mecha = flag