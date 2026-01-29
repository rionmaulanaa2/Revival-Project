# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComMechaTransparentCam.py
from __future__ import absolute_import
from common.utils import timer
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.ui_operation_const import MECHA_JUMP_OPACITY_ENABLED_KEY
JUMP_STAGE_MASK = 1
FLY_STAGE_MASK = 2

class ComMechaTransparentCam(UnitCom):
    BIND_EVENT = {'E_ON_TOUCH_GROUND': 'on_ground',
       'E_LOGIC_ON_GROUND': 'on_ground',
       'E_JUMP': 'on_jump',
       'E_FALL': 'on_fall',
       'E_FLY': 'on_fly',
       'E_ENABLE_MECHA_JUMP_OPACITY': 'enable_jump_opacity',
       'E_DISABLE_MECHA_JUMP_OPACITY': 'disable_jump_opacity',
       'E_RESET_MECHA_JUMP_OPACITY': 'reset_jump_opacity',
       'E_FORCE_ENABLE_MECHA_OPACITY': 'force_enable_mecha_opacity'
       }

    def __init__(self):
        super(ComMechaTransparentCam, self).__init__()
        self._is_in_opacity = False
        self._opacity = 255
        self._timer = 0
        self._force_opacity = None
        self._fade_opacity = 153.0
        self._pitch_opactiy = 255
        self._air_stage_mask = 0
        self._cur_opacity = 255
        self._jump_opacity_enable = False
        self._cur_jump_opacity_enable = False
        self._jump_opacity_in_temp_state = False
        self._event_registered = False
        self._opacity_distance = 5.5 * NEOX_UNIT_SCALE
        return

    def clear_timer(self):
        if self._timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self._timer)
        self._timer = 0

    def destroy(self):
        self.clear_timer()
        if self._event_registered:
            global_data.emgr.mecha_jump_opacity_enabled_changed -= self.mecha_jump_opacity_enabled_changed
            self.unregist_event('E_ACTION_PITCH', self.on_pitch)
            self._event_registered = False
        if self._is_in_opacity:
            self.leave_opacity_mode()
        super(ComMechaTransparentCam, self).destroy()

    def on_init_complete(self):
        self._mecha_id = self.sd.ref_mecha_id
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(self._mecha_id))
        thres_angle, must_angle = mecha_conf.get('opacity_angle_range', (None, None))
        max_opacity, min_opacity = mecha_conf.get('transparent_val_range', (0.8, 0.4))
        if None in [thres_angle, must_angle]:
            return
        else:
            self._jump_opacity_enable = global_data.player.get_setting_2(MECHA_JUMP_OPACITY_ENABLED_KEY)
            self._cur_jump_opacity_enable = self._jump_opacity_enable
            self._jump_opacity_in_temp_state = False
            global_data.emgr.mecha_jump_opacity_enabled_changed += self.mecha_jump_opacity_enabled_changed
            self.unit_obj.regist_event('E_ACTION_PITCH', self.on_pitch)
            self._event_registered = True
            if must_angle < thres_angle:
                must_angle = thres_angle
            self._max_opacity = max_opacity
            self._min_opacity = min_opacity
            self._angle_threshold = math.radians(thres_angle)
            self._angle_must = math.radians(must_angle)
            self._angle_range = abs(self._angle_must - self._angle_threshold) + 0.001
            self._opacity_range = self._max_opacity - self._min_opacity
            self.clear_timer()
            self._timer = global_data.game_mgr.get_post_logic_timer().register(func=self.check_update_opacity, mode=timer.CLOCK, interval=0.1)
            return

    def _cal_dist_opacity(self, part_cam):
        dist = part_cam.get_camera_to_focus_hoz_length() or 0
        if dist >= self._opacity_distance:
            return 255
        if not dist:
            return 255
        percent = dist / self._opacity_distance
        opacity = self._fade_opacity * percent
        return opacity

    def check_update_opacity(self, *args):
        if self._force_opacity is not None:
            if not self._is_in_opacity:
                self.enter_opacity_mode(self._force_opacity)
            return
        else:
            opacity = 255
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
            if part_cam:
                opacity = self._cal_dist_opacity(part_cam)
            if self._cur_jump_opacity_enable and self._air_stage_mask and part_cam:
                opacity = min(self._fade_opacity, opacity)
            opacity = min(opacity, self._pitch_opactiy)
            if opacity >= 255:
                if self._is_in_opacity:
                    self.leave_opacity_mode()
            else:
                self.enter_opacity_mode(opacity)
            return

    def on_pitch(self, delta):
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            cur_pitch = abs(partcam.get_pitch())
            pitch_delta = cur_pitch - self._angle_threshold
            if pitch_delta <= 0:
                self._pitch_opactiy = 255
            else:
                percent = min(max((cur_pitch - self._angle_threshold) / self._angle_range, 0), 1)
                opacity = self._max_opacity - self._opacity_range * percent
                self._pitch_opactiy = opacity * 255

    def enable_jump_opacity(self):
        self._jump_opacity_in_temp_state = True
        self._cur_jump_opacity_enable = True

    def disable_jump_opacity(self):
        self._jump_opacity_in_temp_state = True
        self._cur_jump_opacity_enable = False

    def reset_jump_opacity(self):
        self._jump_opacity_in_temp_state = False
        self._cur_jump_opacity_enable = self._jump_opacity_enable

    def on_ground(self, *args):
        self._air_stage_mask &= FLY_STAGE_MASK

    def on_jump(self, *args):
        self._air_stage_mask |= JUMP_STAGE_MASK

    def on_fall(self, *args):
        self._air_stage_mask |= JUMP_STAGE_MASK

    def on_fly(self, flag):
        if flag:
            self._air_stage_mask |= FLY_STAGE_MASK
        else:
            self._air_stage_mask &= JUMP_STAGE_MASK

    def enter_opacity_mode(self, opacity):
        self._is_in_opacity = True
        if self._cur_opacity != opacity:
            self.send_event('E_SET_MODEL_OPACITY', opacity)
            self._cur_opacity = opacity

    def leave_opacity_mode(self):
        self._is_in_opacity = False
        self._cur_opacity = 255
        self.send_event('E_LEAVE_MODEL_OPACITY')

    def force_enable_mecha_opacity(self, enable, opacity=120.0):
        if enable:
            self._force_opacity = opacity
        else:
            self._force_opacity = None
        return

    def mecha_jump_opacity_enabled_changed(self, enabled):
        if self._jump_opacity_enable ^ enabled:
            self._jump_opacity_enable = enabled
            if not self._jump_opacity_in_temp_state:
                self._cur_jump_opacity_enable = enabled