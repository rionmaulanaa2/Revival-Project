# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComCameraTarget.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d

class ComCameraTarget(UnitCom):
    BIND_EVENT = {'G_IS_CAM_TARGET': '_get_is_cam_target',
       'E_TRY_SWITCH_CAM_STATE': '_try_switch_cam_state',
       'E_ON_LEAVE_MECHA': ('_on_leave_mecha', -10),
       'E_USE_MECHA_SPECIAL_FORM_SENSITIVITY': 'update_mecha_sp_form_sensitivity'
       }

    def __init__(self):
        super(ComCameraTarget, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComCameraTarget, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_use_mecha_special_form_sensitivity = False

    def _get_is_cam_target(self):
        if not self.unit_obj:
            return False
        else:
            if global_data.is_in_judge_camera:
                return False
            cam_player_id = None
            if global_data.player and global_data.player.logic:
                cam_player_id = global_data.player.logic.ev_g_spectate_target_id()
            if not cam_player_id and global_data.player:
                cam_player_id = global_data.player.id
            if self.unit_obj.id == cam_player_id:
                return True
            if global_data.cam_lplayer:
                control_target = global_data.cam_lplayer.sd.ref_ctrl_target
                if control_target and control_target.id == self.unit_obj.id:
                    return True
            return False

    def _try_switch_cam_state(self, cam_state, *args, **kwargs):
        if self._get_is_cam_target():
            if global_data.cam_lplayer:
                global_data.cam_lplayer.send_event(cam_state, *args, **kwargs)

    def _on_leave_mecha(self):
        if self.ev_g_is_cam_target() and not self.ev_g_is_avatar():
            ctrl_target = self.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:

                def cancel_failed_cb(tag, run_callback):
                    global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, True)

                ctrl_target.logic.send_event('E_CANCEL_CAMERA_STATE_TRK', 'C_MECHA_BOARD', self.ev_g_get_bind_mecha_type(), True, cancel_failed_cb)
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_State_Offset', None)
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_Step_back', None)
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_Step_back2', None)
            global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, False)
        return

    def update_mecha_sp_form_sensitivity(self, flag):
        if self.sd.ref_use_mecha_special_form_sensitivity ^ flag:
            self.sd.ref_use_mecha_special_form_sensitivity = flag
            global_data.emgr.update_mecha_sensitivity_type.emit()