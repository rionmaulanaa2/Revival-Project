# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/ComBunkerSidewaysCamState.py
from __future__ import absolute_import
import math3d
from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_utils.local_text import get_text_by_id
SW_RIGHT = POSTURE_RIGHT_SIDEWAYS
SW_LEFT = POSTURE_LEFT_SIDEWAYS
SW_UP = POSTURE_UP_SIDEWAYS
HOZ_VECTOR = math3d.vector(1, 0, 1)
FORWARD_DIR = math3d.vector(0, 0, 1)
from .BunkerCheckHelper import get_bunker_shot_world_offset

class ComBunkerSidewaysCamState(UnitCom):
    BIND_EVENT = {'E_TO_RIGHT_SIDEWAYS_CAMERA': 'on_right_camera_offset',
       'E_TO_LEFT_SIDEWAYS_CAMERA': 'on_left_camera_offset',
       'E_TO_UP_SIDEWAYS_CAMERA': 'on_up_camera_offset',
       'E_LEAVE_SIDEWAYS_CAMERA': 'on_leave_sideways_offset',
       'E_LEAVE_SIDEWAYS': 'on_leave_sideways',
       'E_SIDEWAYS_OVERLAP': 'on_sideways_shot',
       'G_IN_BUNKER_CAMERA': 'get_in_bunker_camera',
       'G_LAST_BUNKER_CAMERA_OFFSET_DIR': 'get_bunker_camera_offset_dir',
       'G_BUNKER_CAMERA_TARGET_OFFSET': 'get_bunker_target_cam_offset',
       'E_RECOVER_BUNKER_CAMERA_TARGET_OFFSET': 'set_bunker_target_cam_offset_dir',
       'G_BUNKER_CAM_OFFSET_BY_DIR': 'get_bunker_cam_offset_by_dir'
       }

    def __init__(self):
        super(ComBunkerSidewaysCamState, self).__init__()
        self._is_in_bksw_cam = False
        self._bksw_cam_dir = None
        self._cur_bksw_target_offset = math3d.vector(0, 0, 0)
        self.init_parameters()
        return

    def init_parameters(self):
        from common.cfg import confmgr
        conf = confmgr.get('sideways_conf')
        self.sideways_cam_smooth_time = conf.get('SIDEWAYS_CAM_SMOOTH_TIME', 0.3)

    def on_right_camera_offset(self):
        global_data.game_mgr.show_tip(get_text_by_id(18188))
        self.on_set_camera_offset(SW_RIGHT)

    def on_left_camera_offset(self):
        global_data.game_mgr.show_tip(get_text_by_id(18189))
        self.on_set_camera_offset(SW_LEFT)

    def on_up_camera_offset(self):
        global_data.game_mgr.show_tip(get_text_by_id(18190))
        self.on_set_camera_offset(SW_UP)

    def on_set_camera_offset(self, offset_dir, need_set_camera=True):
        offset = get_bunker_shot_world_offset(offset_dir)
        self._is_in_bksw_cam = True
        self._bksw_cam_dir = offset_dir
        self._cur_bksw_target_offset = offset
        if need_set_camera:
            self.send_event('S_BUNKER_CAMERA_SMOOTH_OFFSET', self.sideways_cam_smooth_time)

    def on_leave_sideways_offset(self):
        self._is_in_bksw_cam = False
        self._cur_bksw_target_offset = math3d.vector(0, 0, 0)
        self.send_event('S_BUNKER_CAMERA_SMOOTH_OFFSET', self.sideways_cam_smooth_time)

    def get_in_bunker_camera(self):
        return self._is_in_bksw_cam

    def get_bunker_camera_offset_dir(self):
        return self._bksw_cam_dir

    def get_bunker_target_cam_offset(self):
        return self._cur_bksw_target_offset

    def on_sideways_shot(self):
        self._is_in_bksw_cam = False
        if self._cur_bksw_target_offset.length - 0 > 0.001:
            self._cur_bksw_target_offset = math3d.vector(0, 0, 0)
        else:
            self._cur_bksw_target_offset = math3d.vector(0, 0, 0)

    def on_leave_sideways(self):
        self._is_in_bksw_cam = False
        self._bksw_cam_dir = None
        self._cur_bksw_target_offset = math3d.vector(0, 0, 0)
        self.send_event('S_BUNKER_CAMERA_SMOOTH_OFFSET', self.sideways_cam_smooth_time)
        return

    def set_bunker_target_cam_offset_dir(self, new_offset_dir):
        self.on_set_camera_offset(new_offset_dir, False)

    def get_bunker_cam_offset_by_dir(self, offset_dir):
        if offset_dir in [SW_UP, SW_LEFT, SW_RIGHT]:
            offset = get_bunker_shot_world_offset(offset_dir)
            return offset
        else:
            return math3d.vector(0, 0, 0)