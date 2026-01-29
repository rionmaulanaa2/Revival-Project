# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCamSyncReceiver.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gutils.sync.ReceiveBoxCam import ReceiveBoxCam
from logic.client.const.camera_const import THIRD_PERSON_MODEL

class ComCamSyncReceiver(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_RC_CAM_YAW': '_action_sync_cam_yaw',
       'E_ACTION_SYNC_RC_CAM_PITCH': '_action_sync_cam_pitch',
       'G_ACTION_SYNC_RC_CAM_YAW': '_get_sync_cam_yaw',
       'G_ACTION_SYNC_RC_CAM_PITCH': '_get_sync_cam_pitch',
       'E_CAM_STATE': '_set_cam_state',
       'G_CAM_STATE': '_get_cam_state',
       'E_ACTION_SYNC_CAM_STATE': '_set_cam_state',
       'E_SET_PARACHUTE_FOLLOWED': '_set_parachute_followed'
       }

    def __init__(self):
        super(ComCamSyncReceiver, self).__init__(need_update=True)
        self._last_sync_cam_yaw = 0
        self._last_sync_cam_pitch = 0
        self._cam_state = None
        self.need_update = True
        self._yaw_receive_box = ReceiveBoxCam(self._yaw_handler)
        self._pitch_receive_box = ReceiveBoxCam(self._pitch_handler)
        self._parachute_followed = False
        return

    def destroy(self):
        self._yaw_receive_box.destroy()
        self._pitch_receive_box.destroy()
        super(ComCamSyncReceiver, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComCamSyncReceiver, self).init_from_dict(unit_obj, bdict)
        self._last_sync_cam_yaw = self.ev_g_attr_get('cam_yaw', 0)
        self._last_sync_cam_pitch = self.ev_g_attr_get('cam_pitch', 0)
        self._cam_state = self.ev_g_attr_get('cam_state', None)
        return

    def _action_sync_cam_yaw(self, f_yaw, f_dt):
        self._last_sync_cam_yaw = f_yaw
        self._yaw_receive_box.input(f_yaw, f_dt)

    def _action_sync_cam_pitch(self, f_pitch, f_dt):
        self._last_sync_cam_pitch = f_pitch
        self._pitch_receive_box.input(f_pitch, f_dt)

    def _get_sync_cam_yaw(self):
        return self._last_sync_cam_yaw

    def _get_sync_cam_pitch(self):
        return self._last_sync_cam_pitch

    def _yaw_handler(self, reach_time, reach_yaw):
        self.send_event('E_SYNC_CAM_YAW', reach_yaw, True, reach_time)
        if self._parachute_followed and global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_SYNC_CAM_YAW', reach_yaw, True, reach_time)

    def _pitch_handler(self, reach_time, reach_pitch):
        self.send_event('E_SYNC_CAM_PITCH', reach_pitch, True, reach_time)
        if self._parachute_followed and global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_SYNC_CAM_PITCH', reach_pitch, True, reach_time)

    def tick(self, dt):
        self._yaw_receive_box.tick(dt)
        self._pitch_receive_box.tick(dt)

    def _set_cam_state(self, cam_state):
        self._cam_state = cam_state
        self._on_set_cam()

    def _get_cam_state(self):
        return self._cam_state

    def _on_set_cam(self):
        if self.ev_g_in_mecha('Mecha'):
            target = self.ev_g_control_target()
            if target and target.logic:
                target.logic.send_event('E_ON_SYNC_CAM_STATE_CHANGE')

    def _set_parachute_followed(self, flag):
        self._parachute_followed = flag