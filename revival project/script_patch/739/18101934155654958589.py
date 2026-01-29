# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/ObserveCameraStates.py
from __future__ import absolute_import
from data.camera_state_const import *
from logic.client.const.camera_const import FOLLOW_SYNC_TARGET, FOLLOW_SYNC_CAM, FOLLOW_SYNC_NONE

def get_camera_state_sync_type(cam_ty):
    from common.cfg import confmgr
    observe_camera_sync_type = confmgr.get('c_camera_setting', str(cam_ty), default={})
    return observe_camera_sync_type.get('iSyncMode', FOLLOW_SYNC_CAM)


def get_prefer_cam_state_pitch_and_yaw(cam_ty, lplayer):
    if not (lplayer and lplayer.is_valid()):
        return (0, 0)
    else:
        f_yaw = 0
        f_pitch = 0
        f_cam_yaw = lplayer.ev_g_action_sync_rc_cam_yaw() or 0
        f_cam_pitch = lplayer.ev_g_action_sync_rc_cam_pitch() or 0
        con_target = lplayer.ev_g_control_target()
        if con_target and con_target.logic:
            seat_logic = con_target.logic.ev_g_seat_logic_by_id(lplayer.id)
            if seat_logic:
                f_yaw = seat_logic.ev_g_yaw() or 0
                f_pitch = seat_logic.ev_g_cam_pitch() or 0
            else:
                f_yaw = con_target.logic.ev_g_yaw() or 0
                f_pitch = con_target.logic.ev_g_cam_pitch() or 0
        follow_type = get_camera_state_sync_type(cam_ty)
        if follow_type == FOLLOW_SYNC_CAM:
            return (f_cam_yaw, f_cam_pitch)
        if follow_type == FOLLOW_SYNC_TARGET:
            return (f_yaw, f_pitch)
        if follow_type == FOLLOW_SYNC_NONE:
            return (f_yaw, f_pitch)
        return (0, 0)


def check_sync_cam_state_rot_helper(lplayer, old_cam_state, new_cam_state):
    old_sync_type = get_camera_state_sync_type(old_cam_state)
    new_sync_type = get_camera_state_sync_type(new_cam_state)
    if old_sync_type != new_sync_type and new_sync_type != FOLLOW_SYNC_NONE:
        return get_prefer_cam_state_pitch_and_yaw(new_cam_state, lplayer)
    else:
        return None
        return None