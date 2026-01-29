# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraAnimation.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE

class CameraAnimationClip(object):
    __slots__ = ('_clip_name', 'cam_ani_conf', '_last_time', '_cNextClip', '_bEnableForwardOffset',
                 '_fForwardOffset', '_lAbsOffset', '_bPersistOffset', '_lSupModeList',
                 '_bAdd', '_fovOffset')

    def __init__(self, clip_name):
        self._clip_name = clip_name
        cam_ani_conf = confmgr.get('c_camera_ani', clip_name, default={})
        self.cam_ani_conf = cam_ani_conf
        self._last_time = cam_ani_conf.get('fCostTime', 0)
        self._cNextClip = cam_ani_conf.get('cNextClip', '')
        self._bEnableForwardOffset = cam_ani_conf.get('bEnableForwardOffset', False)
        if self._bEnableForwardOffset:
            self._fForwardOffset = cam_ani_conf.get('fForwardOffset', 0) * NEOX_UNIT_SCALE
        else:
            self._fForwardOffset = None
        self._lAbsOffset = cam_ani_conf.get('lAbsOffset', [])
        self._bPersistOffset = cam_ani_conf.get('bPersistOffset', False)
        self._lSupModeList = [ str(mode) for mode in cam_ani_conf.get('lSupModeList', []) ]
        self._bAdd = cam_ani_conf.get('bAdd', False)
        self._fovOffset = cam_ani_conf.get('fFovOffset', None)
        return

    def Play(self):

        def end_callback(is_finish):
            if is_finish and self._cNextClip:
                next_clip = CameraAnimationClip(self._cNextClip)
                next_clip.Play()

        partcame = global_data.game_mgr.scene.get_com('PartCamera')
        if partcame.get_cur_camera_state_type() in self._lSupModeList:
            global_data.emgr.play_camera_animation_event.emit(self._fForwardOffset, [], self._fovOffset, self._last_time, end_callback, not self._bPersistOffset, self._bAdd)

    def SetupCameraParameters(self):
        partcame = global_data.game_mgr.scene.get_com('PartCamera')
        if partcame.get_cur_camera_state_type() in self._lSupModeList:
            forward_offset = self._fForwardOffset if self._bPersistOffset else None
            global_data.emgr.set_up_camera_pos_parameters_event.emit(forward_offset, self._lAbsOffset, self._fovOffset)
        return