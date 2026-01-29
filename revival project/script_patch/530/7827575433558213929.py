# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLoginTrkCamera.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import weakref
import time
import math
import math3d
import logic.vscene.parts.camera.SlerpAction as slerpaction
DEFAULT_FORWARD = math3d.vector(0, 0, 1)
DEFAULT_UP = math3d.vector(0, 1, 0)
SLERP_LINEAR = 0
SLERP_EASE_IN = 1
SLERP_EASE_OUT = 2
SLERP_EASE_IN_OUT = 3

class PartLoginTrkCamera(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartLoginTrkCamera, self).__init__(scene, name, need_update=True)

    def reset_data(self):
        self._cnt_track = None
        self._track_start_time = 0
        self._track_reverse = False
        self._track_callback = None
        self._track_time_scale = 1.0
        self._MODES = [
         slerpaction.linear,
         slerpaction.easein,
         slerpaction.easeout,
         slerpaction.easeinout]
        self._mode_arg = None
        self._mode_func = self._MODES[SLERP_LINEAR]
        self._fix_forward = None
        self._fix_up = None
        return

    def on_pre_load(self):
        self._camera = weakref.ref(self.scene().active_camera)
        self.reset_data()

    def init_event(self):
        event_mgr = global_data.emgr
        event_mgr.play_camera_trk_event += self.play_track
        print('init_event', event_mgr.play_camera_trk_event)

    def _slerp_mode(self, mode, mode_arg):
        if mode > 0 and mode < len(self._MODES):
            self._mode_func = self._MODES[mode]
            self._mode_arg = mode_arg

    def play_track(self, trk, callback=None, revert=False, time_scale=1.0, mode=SLERP_LINEAR, mode_arg=2.0, fix_forward=None, fix_up=None):
        self._slerp_mode(mode, mode_arg)
        self._fix_forward = fix_forward
        self._fix_up = fix_up
        self._cnt_track = trk
        if not self._cnt_track:
            log_error('track file %s not exists' % track_name)
            return False
        self._track_start_time = time.time()
        self._track_reverse = revert
        self._track_time_scale = time_scale
        if callback:
            self._track_callback = callback
        return True

    def cancel_track(self):
        self.reset_data()

    def on_update(self, dt):
        self.on_track_update()

    def update_camera(self, dt):
        pos = self._cnt_track.get_position(dt)
        rot = self._cnt_track.get_rotation(dt)
        forward = rot.forward if self._fix_forward is None else self._fix_forward
        up = rot.up if self._fix_up is None else self._fix_up
        if math.isnan(forward.x):
            forward = DEFAULT_FORWARD
        if math.isnan(up.x):
            up = DEFAULT_UP
        self.camera.set_placement(pos, forward, up)
        return

    def on_track_update(self):
        if self._cnt_track is None:
            return
        else:
            from common.utils.timer import RELEASE
            cnt_time = time.time()
            track_duration = self._cnt_track.duration
            time_gap = (cnt_time - self._track_start_time) * 1000 * self._track_time_scale
            cnt_interval = min(track_duration, time_gap)
            cnt_interval = self._mode_func(cnt_interval / track_duration, self._mode_arg) * track_duration
            if self._track_reverse:
                cnt_interval = track_duration - cnt_interval
            self.update_camera(cnt_interval)
            if time_gap >= track_duration:
                cb = self._track_callback
                self.reset_data()
                if cb:
                    cb()
                return
            return

    @property
    def camera(self):
        return self._camera()

    def on_exit(self):
        self._cnt_track = None
        return