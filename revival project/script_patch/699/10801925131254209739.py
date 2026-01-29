# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/ShotChecker.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.framework import Singleton
from logic.client.const import camera_const

class ShotChecker(Singleton):

    def init(self):
        self.do_not_reset_camera_on_fire = False

    def check_camera_can_shot(self, lplayer=None):
        if self.do_not_reset_camera_on_fire:
            return False
        else:
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
            if not part_cam:
                return True
            cur_camera_state = part_cam.get_cur_camera_state_type()
            can_shoot = confmgr.get('c_camera_setting', str(cur_camera_state), default={}).get('bSupportShoot', False)
            if not can_shoot and cur_camera_state in camera_const.FREE_CAMERA_TYPE:
                cam_switch_back = True
                if lplayer:
                    stage = lplayer.share_data.ref_parachute_stage
                    from logic.gcommon.common_utils import parachute_utils
                    if parachute_utils.is_preparing(stage) or parachute_utils.is_sortie_stage(stage) or parachute_utils.is_parachuting(stage):
                        cam_switch_back = False
                if cam_switch_back:
                    global_data.emgr.switch_to_last_camera_state_event.emit()
                return True
            if part_cam and part_cam.is_in_cam_slerp():
                slerp_cam_states = list(part_cam.get_slerp_cam_states())
                can_shoot = True
                for state in slerp_cam_states:
                    if state is None:
                        continue
                    state_shoot = confmgr.get('c_camera_setting', str(state), default={}).get('bSupportShoot', False)
                    can_shoot = can_shoot and state_shoot

                if not can_shoot:
                    return True
            return False