# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/CameraData.py
from __future__ import absolute_import
from common.framework import Singleton
from data.camera_state_const import THIRD_PERSON_MODEL
from logic.client.const.camera_const import FREE_MODEL, DEBUG_MODE, OBSERVE_FREE_MODE
import world
FREE_CAMERA_MODE = (
 FREE_MODEL, DEBUG_MODE, OBSERVE_FREE_MODE)

class CameraData(Singleton):
    __slots__ = {
     'yaw', 'pitch', 'fov', 'camera_state_type'}
    ALIAS_NAME = 'cam_data'

    def init(self):
        self.process_event(True)
        self.reset()

    def on_finalize(self):
        self.reset()
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'camera_switch_to_state_event': self.set_camera_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def reset(self):
        self.yaw = 0
        self.pitch = 0
        self.fov = 45
        self.camera_state_type = THIRD_PERSON_MODEL
        self.cam_yaw_before_enter_free = None
        return

    def update_camera_data_by_dict(self, yaw, pitch, fov, camera_state_type):
        self.yaw = yaw
        self.pitch = pitch
        self.fov = fov
        self.camera_state_type = camera_state_type

    def set_camera_state(self, state, old_cam_type, is_finish_switch):
        if state in FREE_CAMERA_MODE and old_cam_type not in FREE_CAMERA_MODE and not is_finish_switch:
            self.cam_yaw_before_enter_free = world.get_active_scene().active_camera.world_rotation_matrix.yaw
        elif old_cam_type in FREE_CAMERA_MODE and state not in FREE_CAMERA_MODE and is_finish_switch:
            self.cam_yaw_before_enter_free = None
            global_data.emgr.free_camera_switch_finish_event.emit()
        if state not in FREE_CAMERA_MODE and self.cam_yaw_before_enter_free and is_finish_switch:
            self.cam_yaw_before_enter_free = None
            global_data.emgr.free_camera_switch_finish_event.emit()
        return