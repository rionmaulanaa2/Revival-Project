# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/ICameraTrkPlayer.py
from __future__ import absolute_import
import cython

class ILinearPolaHelper(object):

    def __init__(self):
        super(ILinearPolaHelper, self).__init__()

    def cal(self, t):
        pass


class ICameraTrkPlayer(object):

    def __init__(self):
        super(ICameraTrkPlayer, self).__init__()

    def on_start(self):
        pass

    def on_finish(self):
        pass

    def on_track_update(self):
        pass

    def has_start(self):
        return False

    def is_finish(self):
        return True

    def get_trk_fov(self, cnt_time):
        pass

    def get_track(self, cnt_time):
        pass

    def play_track(self, track_name, callback, revert=False, time_scale=1.0, is_additive=True, is_left_hand=False, finish_callback=None):
        return False

    def get_left_hand_trans(self, dt):
        pass

    def get_left_hand_from_trk(self, trans):
        pass

    def get_trk_transformation(self, dt):
        pass