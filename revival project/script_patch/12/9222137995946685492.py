# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/ObserveFreeCameraSwitchChecker.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.client.const.camera_const import THIRD_PERSON_MODEL, MECHA_MODE_TWO, VEHICLE_MODE, FREE_CAM_ACT_FALLBACK, FREE_CAM_ACT_KEEP
from logic.gutils.CameraHelper import get_mecha_camera_type

class ObserveFreeCameraSwitchChecker(object):

    @staticmethod
    def check_can_switch(lplayer, lctarget, to_camera_state):
        if not lplayer:
            return False
        act = ObserveFreeCameraSwitchChecker.get_free_camera_action(to_camera_state)
        if act == FREE_CAM_ACT_KEEP:
            return True
        def_state = ObserveFreeCameraSwitchChecker.get_state_default_camera(lplayer, lctarget)
        if to_camera_state == def_state:
            return True
        return False

    @staticmethod
    def get_state_default_camera(lplayer, lctarget):
        if not lplayer or not lctarget:
            return None
        else:
            mecha_type = lplayer.ev_g_get_bind_mecha_type()
            if mecha_type and lplayer.ev_g_ctrl_mecha():
                valid_camera_state = get_mecha_camera_type(str(mecha_type), lctarget.ev_g_mecha_fashion_id())
                return valid_camera_state
            if lctarget and lctarget.ev_g_is_mechatran():
                from logic.gcommon.common_const import mecha_const
                if lctarget.ev_g_pattern() == mecha_const.MECHA_TYPE_VEHICLE:
                    return VEHICLE_MODE
                else:
                    return MECHA_MODE_TWO

            else:
                if lctarget and lctarget.ev_g_is_vehicle():
                    return lctarget.ev_g_state_default_camera(lplayer)
                return THIRD_PERSON_MODEL
            return None

    @staticmethod
    def get_target_camera_state(lplayer, lctarget, to_camera_state):
        if not lplayer:
            return THIRD_PERSON_MODEL
        act = ObserveFreeCameraSwitchChecker.get_free_camera_action(to_camera_state)
        if act == FREE_CAM_ACT_KEEP:
            return to_camera_state
        def_state = ObserveFreeCameraSwitchChecker.get_state_default_camera(lplayer, lctarget)
        return def_state

    @staticmethod
    def get_free_camera_action(camera_state):
        cam_setting = confmgr.get('c_camera_setting', str(camera_state), default={})
        iFreeCamAction = cam_setting.get('iFreeCamAction', FREE_CAM_ACT_FALLBACK)
        return iFreeCamAction