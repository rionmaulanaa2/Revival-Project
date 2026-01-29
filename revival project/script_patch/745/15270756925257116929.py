# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraComponents.py
from __future__ import absolute_import
from six.moves import zip
import math3d
import math
from common.framework import Singleton
from data.c_camera_const import CAMERA_COLL_RECOVER_SPEED, CAMERA_IN_ROOM_SPEED
from logic.client.const.camera_const import FOLLOW_SYNC_TARGET, FOLLOW_SYNC_CAM, FOLLOW_SYNC_NONE
from data.camera_state_const import *
from .CameraAnimation import CameraAnimationClip
from common.cfg import confmgr
from .ObserveCameraStates import get_camera_state_sync_type

class CameraComData(Singleton):

    def regist_para(self, var_name, var_val):
        if hasattr(self, var_name):
            return
        setattr(self, var_name, var_val)


camera_com_data = CameraComData()
COLL_UPDATE_FRAME = 10
UP_VECTOR = math3d.vector(0, 1, 0)
RIGHT_VECTOR = math3d.vector(1, 0, 0)
YZ_VECTOR = math3d.vector(0, 1, 1)

class CamCom(object):
    REGIST = True

    def __init__(self, cam_state):
        self.cam_state = cam_state
        self.on_init()

    def on_init(self):
        pass

    def cache(self):
        self.cam_state and self.on_cam_destroy()
        self.cam_state = None
        return

    def reuse(self, cam_state):
        self.cam_state = cam_state
        self.on_init()

    def enter(self):
        self.on_enter()

    def on_enter(self):
        pass

    def destroy(self):
        self.cam_state and self.on_cam_destroy()
        self.cam_state = None
        return

    def on_cam_destroy(self):
        pass

    def on_target_pos_changed(self, wpos):
        pass

    def regist_global_parameter(self, var_name, var_val):
        camera_com_data.regist_para(var_name, var_val)

    def on_get_enter_parameters(self):
        pass


class RoomOffsetCameraCom(CamCom):

    def on_init(self):
        self.last_check_camera_time = 0
        self._is_in_room = False

    @property
    def is_in_room(self):
        return self._is_in_room

    @is_in_room.setter
    def is_in_room(self, val):
        self._is_in_room = val
        self.cam_state.set_cam_state_data('is_in_room', val)

    def on_cam_destroy(self):
        self.is_in_room = False

    def on_get_enter_parameters(self):
        self.check_in_is_room(self.cam_state.cur_target_pos, is_init=True)

    def on_target_pos_changed(self, wpos):
        self.check_in_is_room(self.cam_state.cur_target_pos)

    def check_in_is_room(self, world_pos, is_init=False):
        from logic.gutils.CameraHelper import check_in_room
        import time
        cur_time = time.time()
        if cur_time - self.last_check_camera_time < 0.3:
            return
        self.last_check_camera_time = cur_time
        scn = global_data.game_mgr.scene
        is_in_room = check_in_room(world_pos, scn)
        if self.is_in_room != is_in_room:
            if is_in_room:
                self.modification_if_enter_room_area(is_init)
            else:
                self.modification_if_leave_room_area(is_init)

    def modification_if_enter_room_area(self, is_init=False):
        from data.c_camera_const import CAMERA_ROOM_OFFSET
        if self.cam_state.TYPE in [THIRD_PERSON_MODEL, FREE_MODEL, THIRD_PERSON_SPEED_UP_MODE]:
            self.is_in_room = True
            global_data.emgr.on_enter_room_camera_event.emit()
            cost_time = float(abs(CAMERA_ROOM_OFFSET)) / CAMERA_IN_ROOM_SPEED
            global_data.emgr.set_up_camera_pos_parameters_event.emit(CAMERA_ROOM_OFFSET)
            if not is_init:
                global_data.emgr.slerp_into_setupped_camera_event.emit(cost_time)

    def modification_if_leave_room_area(self, is_init=False):
        from data.c_camera_const import CAMERA_ROOM_OFFSET
        if self.cam_state.TYPE in [THIRD_PERSON_MODEL, FREE_MODEL, THIRD_PERSON_SPEED_UP_MODE] and self.is_in_room:
            self.is_in_room = False
            global_data.emgr.on_leave_room_camera_event.emit()
            cost_time = float(abs(CAMERA_ROOM_OFFSET)) / CAMERA_COLL_RECOVER_SPEED
            global_data.emgr.set_up_camera_pos_parameters_event.emit(-CAMERA_ROOM_OFFSET)
            if not is_init:
                global_data.emgr.slerp_into_setupped_camera_event.emit(cost_time)


class SkateOffsetCameraCom(CamCom):
    ENTER_ANI_NAME = 'start_skate_move'
    LEAVE_ANI_NAME = 'stop_skate_move'

    def on_init(self):
        self.is_in_skating = False
        self.init_event()

    def init_event(self):
        self.process_bind_events(True)

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'player_enter_skate_move_camera': self.enter_skate_move,
           'player_leave_skate_move_camera': self.leave_skate_move
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_cam_destroy(self):
        self.is_in_skating = False
        self.process_bind_events(False)

    def on_get_enter_parameters(self):
        if self.check_is_in_skate():
            clip = CameraAnimationClip(self.ENTER_ANI_NAME)
            clip.SetupCameraParameters()

    def check_is_in_skate(self):
        if not global_data.cam_lplayer:
            return False
        else:
            return global_data.cam_lplayer.ev_g_is_in_skate_move_cam()

    def enter_skate_move(self):
        clip = CameraAnimationClip(self.ENTER_ANI_NAME)
        clip.Play()

    def leave_skate_move(self):
        clip = CameraAnimationClip(self.LEAVE_ANI_NAME)
        clip.Play()


class ParachuteAssistCam(CamCom):
    MOVE_ANI_NAME = 'parachute_move_start'
    STOP_ANI_NAME = 'parachute_move_end'

    def on_init(self):
        self.is_in_moving = False
        self.init_event()

    def init_event(self):
        self.process_bind_events(True)

    def check_is_in_parachute_move(self):
        if not global_data.cam_lplayer:
            return False
        else:
            return global_data.cam_lplayer.ev_g_is_in_parachute_move_cam()

    def on_get_enter_parameters(self):
        self.is_in_moving = self.check_is_in_parachute_move()
        if self.is_in_moving:
            self.on_free_frop_move()

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'player_enter_free_drop_move_camera': self.on_free_frop_move,
           'player_leave_free_drop_move_camera': self.on_free_drop_move_stop
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_cam_destroy(self):
        self.process_bind_events(False)

    def on_free_frop_move(self):
        self.is_in_moving = True
        clip = CameraAnimationClip(self.MOVE_ANI_NAME)
        clip.Play()

    def on_free_drop_move_stop(self):
        self.is_in_moving = False
        from .CameraAnimation import CameraAnimationClip
        clip = CameraAnimationClip(self.STOP_ANI_NAME)
        clip.Play()


class BiStateAniCam(CamCom):
    BI_EVENT_LIST = []
    BI_CLIP_LIST = []
    CHECK_ENTER_STATE_EVENT_NAME = ''
    ENTER_INDEX = 0
    LEAVE_INDEX = 1

    def on_init(self):
        self.is_in_state = False
        self.init_event()

    def on_cam_destroy(self):
        self.process_bind_events(False)

    def init_event(self):
        self.process_bind_events(True)

    def is_control_target_state(self):
        return False

    def check_is_in_state(self):
        if not global_data.cam_lplayer:
            return False
        else:
            if self.is_control_target_state():
                return global_data.cam_lplayer.get_value(self.CHECK_ENTER_STATE_EVENT_NAME)
            control_target = global_data.cam_lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                return control_target.logic.get_value(self.CHECK_ENTER_STATE_EVENT_NAME)
            return False

    def on_get_enter_parameters(self):
        if self.check_is_in_state() and self.check_can_enter():
            self.is_in_state = True
            clip = CameraAnimationClip(self.BI_CLIP_LIST[self.ENTER_INDEX])
            clip.SetupCameraParameters()

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {}
        events.update(list(zip(self.BI_EVENT_LIST, [self.on_enter_state, self.on_leave_state])))
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_enter_state(self):
        if not self.check_can_enter():
            return
        self.is_in_state = True
        clip = CameraAnimationClip(self.BI_CLIP_LIST[self.ENTER_INDEX])
        clip.Play()

    def on_leave_state(self):
        if not self.is_in_state:
            return
        self.is_in_state = False
        clip = CameraAnimationClip(self.BI_CLIP_LIST[self.LEAVE_INDEX])
        clip.Play()

    def check_can_enter(self):
        return True

    def recheck_state(self):
        if self.check_is_in_state():
            self.on_enter_state()


class RunCam(BiStateAniCam):
    BI_EVENT_LIST = [
     'player_enter_run_camera_event', 'player_leave_run_camera_event']
    BI_CLIP_LIST = ['run_start', 'run_stop']
    CHECK_ENTER_STATE_EVENT_NAME = 'G_IS_IN_RUN_CAM'

    def process_bind_events(self, is_bind):
        super(RunCam, self).process_bind_events(is_bind)
        if is_bind:
            global_data.emgr.on_leave_room_camera_event += self.recheck_state
            global_data.emgr.on_enter_room_camera_event += self.on_leave_state
        else:
            global_data.emgr.on_leave_room_camera_event -= self.recheck_state
            global_data.emgr.on_enter_room_camera_event -= self.on_leave_state

    def get_is_in_room(self):
        return self.cam_state.get_cam_state_data('is_in_room')

    def check_can_enter(self):
        return not self.get_is_in_room()


class ShotCam(BiStateAniCam):
    BI_EVENT_LIST = [
     'player_enter_shot_camera_event', 'player_leave_shot_camera_event']
    BI_CLIP_LIST = ['shot_start', 'shot_end']
    CHECK_ENTER_STATE_EVENT_NAME = 'G_IS_IN_SHOT_CAM'


class ShoulderCannonCam(BiStateAniCam):
    BI_EVENT_LIST = [
     'player_enter_shoulder_cannon_camera_event', 'player_leave_shoulder_cannon_camera_event']
    BI_CLIP_LIST = ['shouldercannon_start', 'shouldercannon_end']
    CHECK_ENTER_STATE_EVENT_NAME = 'G_IS_IN_SHOULDER_CANNON_CAM'

    def is_control_target_state(self):
        return True


class ClipCameraCom(CamCom):

    def on_init(self):
        self.init_event()

    def init_event(self):
        self.process_bind_events(True)

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'player_enter_camera_clip_state_event': self.enter_clip,
           'player_exit_camera_clip_state_event': self.leave_clip
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_cam_destroy(self):
        self.process_bind_events(False)

    def on_get_enter_parameters(self):
        run_clips = self.get_all_running_clip()
        if not run_clips:
            return
        for clip_state in run_clips:
            fEnterClip = confmgr.get('c_camera_ani_state', str(clip_state), default={}).get('fEnterClip', 0)
            clip = CameraAnimationClip(fEnterClip)
            clip.SetupCameraParameters()

    def get_all_running_clip(self):
        if not global_data.cam_lplayer:
            return []
        else:
            control_target = global_data.cam_lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                return control_target.logic.ev_g_running_cam_clip()
            return []

    def enter_clip(self, clip_state):
        fEnterClip = confmgr.get('c_camera_ani_state', str(clip_state), default={}).get('fEnterClip', 0)
        clip = CameraAnimationClip(fEnterClip)
        clip.Play()

    def leave_clip(self, clip_state):
        fExitClip = confmgr.get('c_camera_ani_state', str(clip_state), default={}).get('fExitClip', 0)
        clip = CameraAnimationClip(fExitClip)
        clip.Play()


class ObserveCameraCom(CamCom):
    FOLLOW_TYPE = FOLLOW_SYNC_NONE

    def on_init(self):
        self.init_follow_type()
        self.regist_event()

    def init_follow_type(self):
        self.FOLLOW_TYPE = get_camera_state_sync_type(self.cam_state.TYPE)
        if self.FOLLOW_TYPE == FOLLOW_SYNC_CAM:
            self.set_sync_state(True)

    def set_sync_state(self, sync_state):
        if self.FOLLOW_TYPE == FOLLOW_SYNC_CAM:
            return

    def regist_event(self):
        emgr = global_data.emgr
        if self.FOLLOW_TYPE == FOLLOW_SYNC_TARGET:
            emgr.sync_cam_yaw_with_role += self.on_spectate_yaw_normal_change
            emgr.sync_cam_pitch_with_role += self.on_spectate_pitch_normal_change
        elif self.FOLLOW_TYPE == FOLLOW_SYNC_CAM:
            emgr.sync_cam_yaw_with_remote += self.on_spectate_yaw_change
            emgr.sync_cam_pitch_with_remote += self.on_spectate_pitch_change

    def unregist_event(self):
        emgr = global_data.emgr
        if self.FOLLOW_TYPE == FOLLOW_SYNC_TARGET:
            emgr.sync_cam_yaw_with_role -= self.on_spectate_yaw_normal_change
            emgr.sync_cam_pitch_with_role -= self.on_spectate_pitch_normal_change
        elif self.FOLLOW_TYPE == FOLLOW_SYNC_CAM:
            emgr.sync_cam_yaw_with_remote -= self.on_spectate_yaw_change
            emgr.sync_cam_pitch_with_remote -= self.on_spectate_pitch_change

    def on_spectate_yaw_normal_change(self, to_yaw):
        if math.isnan(to_yaw) or math.isinf(to_yaw) or math.isnan(self.cam_state._yaw) or math.isinf(self.cam_state._yaw) or abs(to_yaw) > 20000:
            return
        if to_yaw - self.cam_state._yaw:
            self.cam_state.yaw(to_yaw - self.cam_state._yaw)

    def on_spectate_pitch_normal_change(self, to_pitch):
        if math.isnan(to_pitch) or math.isinf(to_pitch) or math.isnan(self.cam_state._pitch) or math.isinf(self.cam_state._pitch) or abs(to_pitch) > 20000:
            return
        if to_pitch - self.cam_state._pitch:
            self.cam_state.pitch(to_pitch - self.cam_state._pitch)

    def on_spectate_yaw_change(self, yaw, need_slerp=True, cost_time=0.3):
        if math.isnan(yaw) or math.isinf(yaw) or abs(yaw) > 20000:
            return
        else:
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(yaw, None, need_slerp, cost_time)
            return

    def on_spectate_pitch_change(self, pitch, need_slerp=True, cost_time=0.3):
        if math.isnan(pitch) or math.isinf(pitch) or abs(pitch) > 20000:
            return
        else:
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(None, pitch, need_slerp, cost_time)
            return

    def on_cam_destroy(self):
        if self.FOLLOW_TYPE == FOLLOW_SYNC_CAM:
            self.set_sync_state(False)
        self.unregist_event()

    def report_outside_error(self, *args):
        import traceback
        stack = traceback.extract_stack()
        import exception_hook
        err_msg = 'Check input value!\n' + str(stack) + '\n' + str(args)
        exception_hook.post_error(err_msg)