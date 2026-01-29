# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/ComBunkerSidewaysShot.py
from __future__ import absolute_import
import math3d
from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
from logic.gcommon.cdata import status_config as st_const
from logic.gcommon.component.UnitCom import UnitCom
SW_RIGHT = POSTURE_RIGHT_SIDEWAYS
SW_LEFT = POSTURE_LEFT_SIDEWAYS
SW_UP = POSTURE_UP_SIDEWAYS
HOZ_VECTOR = math3d.vector(1, 0, 1)
FORWARD_DIR = math3d.vector(0, 0, 1)
SW_BY_AIM = 1
SW_BY_SHOT = 2
SW_BY_RIGHT_AIM = 3

class ComBunkerSidewaysShot(UnitCom):
    BIND_EVENT = {'E_START_FIRE_ROCKER': 'on_start_fire_rocker',
       'E_END_FIRE_ROCKER': 'on_end_fire_rocker',
       'G_SIDEWAYS_ACTION': 'on_sideways_shot',
       'E_TOUCH_AIM_ROCKER': 'on_touch_aim',
       'E_RELEASE_AIM_ROCKER': 'on_release_aim',
       'E_TOUCH_RIGHT_AIM_ROCKER': 'on_touch_right_aim',
       'E_RELEASE_RIGHT_AIM_ROCKER': 'on_release_right_aim',
       'E_QUIT_AIM': 'on_quit_all_aim',
       'E_QUIT_RIGHT_AIM': 'on_quit_all_aim'
       }

    def __init__(self):
        super(ComBunkerSidewaysShot, self).__init__()
        self._is_sideways_action = False
        self._is_lean_action = False
        self._is_sideways_shot_real_start = True
        self._sideways_cause = None
        self.init_parameters()
        return

    def init_parameters(self):
        from common.cfg import confmgr
        conf = confmgr.get('sideways_conf')
        self.start_sideways_move_time = conf.get('START_SIDEWAYS_MOVE_TIME', 0.3)
        self.back_sideways_move_time = conf.get('BACK_SIDEWAYS_MOVE_TIME', 0.3)

    def on_start_fire_rocker(self):

        def into_shot():
            if self.ev_g_status_check_pass(st_const.ST_SHOOT):
                self.send_event('S_BUNKER_CAMERA_OFFSET', None)
                self._is_sideways_shot_real_start = True
                self.send_event('E_START_AUTO_FIRE')
            return

        if not self.ev_g_in_bunker_camera():
            into_shot()
        elif self._sideways_cause != SW_BY_SHOT:
            self._is_sideways_action = True
            self._sideways_cause = SW_BY_SHOT
            offset = self.ev_g_bunker_camera_target_offset()
            cur_pos = self.ev_g_position()
            bksw_cam_dir = self.ev_g_last_bunker_camera_offset_dir()
            self.send_event('E_SIDEWAYS_OVERLAP')
            self.send_event('E_START_BUNK_SHOT_MOVE', bksw_cam_dir, offset, lambda : into_shot(), cost_time=self.start_sideways_move_time)

    def on_end_fire_rocker(self):
        if self._is_sideways_shot_real_start:
            self.send_event('E_STOP_AUTO_FIRE')
            self._is_sideways_shot_real_start = False
        if self._sideways_cause == SW_BY_SHOT:
            if self._is_sideways_action:
                self.check_recover_to_sideways()
                self._is_sideways_action = False
            self._sideways_cause = None
        return

    def check_recover_to_sideways(self):
        result, _ = self.ev_g_check_bunker_front()
        if result[0]:
            bksw_cam_dir = self.ev_g_last_bunker_camera_offset_dir()

            def recover_callback(re_cam_dir=bksw_cam_dir):
                offset = self.ev_g_bunker_camera_target_offset()
                self.send_event('S_BUNKER_CAMERA_OFFSET', offset)

            if bksw_cam_dir in [SW_LEFT, SW_RIGHT]:
                self.send_event('E_RECOVER_BUNKER_CAMERA_TARGET_OFFSET', bksw_cam_dir)
                offset = self.ev_g_player_sideways_offset()
                self.send_event('E_INTERRUPT_BUNKER_SHOT_MOVE')
                self.send_event('E_START_BUNK_SHOT_MOVE', bksw_cam_dir, -offset, lambda : recover_callback(), self.back_sideways_move_time)
            elif bksw_cam_dir == SW_UP:
                self.send_event('E_RECOVER_BUNKER_CAMERA_TARGET_OFFSET', bksw_cam_dir)
                self.send_event('E_CTRL_SQUAT')
                self.send_event('E_INTERRUPT_BUNKER_SHOT_MOVE')
                self.send_event('S_BUNKER_CAMERA_SMOOTH_OFFSET', self.back_sideways_move_time)
            else:
                log_error("When Recover to sideways, can't find correct dir")
        else:
            self.send_event('E_STOP_BUNKER_SHOT_MOVE')
            self.send_event('S_LEAVE_BUNKER')

    def on_sideways_shot(self):
        return self._is_sideways_action

    def on_touch_aim(self):

        def into_aim():
            self.send_event('S_BUNKER_CAMERA_OFFSET', None)
            if not self.sd.ref_in_aim and self.ev_g_status_check_pass('ST_AIM'):
                self.send_event('E_TRY_AIM')
            return

        if not self.ev_g_in_bunker_camera():
            into_aim()
        elif self._sideways_cause is None:
            self._sideways_cause = SW_BY_AIM
            self._is_sideways_action = True
            offset = self.ev_g_bunker_camera_target_offset()
            bksw_cam_dir = self.ev_g_last_bunker_camera_offset_dir()
            self.send_event('E_SIDEWAYS_OVERLAP')
            self.send_event('E_START_BUNK_SHOT_MOVE', bksw_cam_dir, offset, lambda : into_aim(), cost_time=self.start_sideways_move_time)
        return

    def on_release_aim(self):
        if self._sideways_cause == SW_BY_AIM:
            self.check_recover_to_sideways()
            self._sideways_cause = None
            self._is_sideways_action = False
        if self.sd.ref_in_aim:
            self.send_event('E_QUIT_AIM')
        return

    def on_touch_right_aim(self):

        def into_aim():
            self.send_event('S_BUNKER_CAMERA_OFFSET', None)
            if not self.ev_g_in_right_aim() and self.ev_g_status_check_pass('ST_RIGHT_AIM'):
                self.send_event('E_TRY_RIGHT_AIM')
            return

        if not self.ev_g_in_bunker_camera():
            into_aim()
        elif self._sideways_cause is None:
            self._sideways_cause = SW_BY_RIGHT_AIM
            self._is_sideways_action = True
            offset = self.ev_g_bunker_camera_target_offset()
            bksw_cam_dir = self.ev_g_last_bunker_camera_offset_dir()
            self.send_event('E_SIDEWAYS_OVERLAP')
            self.send_event('E_START_BUNK_SHOT_MOVE', bksw_cam_dir, offset, lambda : into_aim(), cost_time=self.start_sideways_move_time)
        return

    def on_release_right_aim(self):
        if self._sideways_cause == SW_BY_RIGHT_AIM:
            self.check_recover_to_sideways()
            self._sideways_cause = None
            self._is_sideways_action = False
        if self.ev_g_in_right_aim():
            self.send_event('E_QUIT_RIGHT_AIM')
        return

    def on_quit_all_aim(self):
        if self._sideways_cause in [SW_BY_AIM, SW_BY_RIGHT_AIM]:
            self.send_event('E_STOP_BUNKER_SHOT_MOVE')
            self.send_event('S_LEAVE_BUNKER')
            self._sideways_cause = None
            self._is_sideways_action = False
        return