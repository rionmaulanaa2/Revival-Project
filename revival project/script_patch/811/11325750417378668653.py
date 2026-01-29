# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCamSyncSender.py
from __future__ import absolute_import
from logic.gutils.sync.TriggerBoxCam import TriggerBoxCam
from logic.gutils.sync.TriggerBox import TriggerBox
from ..UnitCom import UnitCom
import time
from logic.gcommon import time_utility as t_util
from data import camera_state_const as csconst
import world

class ComCamSyncSender(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_CAM_YAW': '_dt_f_cam_yaw',
       'E_ACTION_SYNC_CAM_PITCH': '_dt_f_cam_pitch',
       'E_CAM_STATE': '_set_cam_state',
       'E_OB_SYNC_CAM_STATE': '_set_ob_sync_cam_state',
       'E_DEATH': '_on_death',
       'E_SET_HAS_SPECTATOR': '_set_has_spectator',
       'E_HAS_PARACHUTE_FOLLOWER': '_set_has_parachute_follower'
       }

    def __init__(self):
        super(ComCamSyncSender, self).__init__(need_update=True)
        self._box_cam_yaw = TriggerBoxCam(min_itvl=0.1, min_delta=0.05, max_stay=0.25)
        self._box_cam_yaw.set_callback(self.on_tri_cam_yaw)
        self._box_cam_pitch = TriggerBoxCam(min_itvl=0.1, min_delta=0.05, max_stay=0.25)
        self._box_cam_pitch.set_callback(self.on_tri_cam_pitch)
        self.need_update = True
        self.last_dt = 0

    def destroy(self):
        self._box_cam_yaw.destroy()
        self._box_cam_pitch.destroy()
        super(ComCamSyncSender, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComCamSyncSender, self).init_from_dict(unit_obj, bdict)
        self._has_spectator = bdict.get('has_spectator', False)
        self._cam_state = csconst.THIRD_PERSON_MODEL
        self._has_follower = False
        is_avatar = self.is_unit_obj_type('LAvatar')
        if is_avatar and self._cam_state == csconst.FREE_MODEL:
            self.send_event('E_FREE_CAMERA_STATE', False)

    def tick(self, dt):
        cur_time = global_data.game_time
        if self._box_cam_yaw:
            self._box_cam_yaw.check_trigger(cur_time)
        if self._box_cam_pitch:
            self._box_cam_pitch.check_trigger(cur_time)

    def _dt_f_cam_yaw(self, f_cam_yaw):
        f_cam_yaw = self._get_cam_yaw()
        self._box_cam_yaw.input(time.time(), f_cam_yaw)

    def _dt_f_cam_pitch(self, f_cam_pitch):
        f_pitch = self._get_cam_pitch()
        self._box_cam_pitch.input(time.time(), f_pitch)

    def _set_cam_state(self, cam_state):
        self._cam_state = cam_state
        self.send_event('S_ATTR_SET', 'cam_state', cam_state)
        if not self._need_send():
            return
        self.send_event('E_CALL_SYNC_METHOD', 'cam_state', (cam_state,), True, True, False)

    def _set_ob_sync_cam_state(self, ob_sync_cam_state):
        if not self._need_send():
            return
        self.send_event('E_CALL_SYNC_METHOD', 'ob_sync_cam_state', (ob_sync_cam_state,), True, True, False)

    def on_tri_cam_yaw(self, dt, f_cam_yaw):
        if not self._need_send():
            self.send_event('E_CALL_SYNC_METHOD', 'sync_ack_check', (), True, True, False)
            return
        self.send_event('E_CALL_SYNC_METHOD', 'acc_cam_yaw', (f_cam_yaw, dt), True, True, False)

    def on_tri_cam_pitch(self, dt, f_cam_pitch):
        if not self._need_send():
            self.send_event('E_CALL_SYNC_METHOD', 'sync_ack_check', (), True, True, False)
            return
        self.send_event('E_CALL_SYNC_METHOD', 'acc_cam_pitch', (f_cam_pitch, dt), True, True, False)

    def _on_death(self, *arg):
        self.need_update = False

    def _need_send(self):
        from logic.gutils import judge_utils
        if judge_utils.has_judges_in_battle():
            return True
        return self._has_spectator or self._has_follower or global_data.need_replay

    def _set_has_spectator(self, has_spectator):
        self._has_spectator = has_spectator
        if self._need_send():
            f_pitch = self._get_cam_pitch()
            self.on_tri_cam_pitch(0, f_pitch)
            f_cam_yaw = self._get_cam_yaw()
            self.on_tri_cam_yaw(0, f_cam_yaw)
            self._set_cam_state(self._cam_state)

    def _set_has_parachute_follower(self, has_follower):
        self._has_follower = has_follower
        if self._need_send():
            f_pitch = self._get_cam_pitch()
            self.on_tri_cam_pitch(0, f_pitch)
            f_cam_yaw = self._get_cam_yaw()
            self.on_tri_cam_yaw(0, f_cam_yaw)
            self._set_cam_state(self._cam_state)

    def _get_cam_pitch(self):
        return global_data.cam_data.pitch

    def _get_cam_yaw(self):
        return global_data.cam_data.yaw