# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/ISlerpCamera.py
from __future__ import absolute_import
import cython

class ISlerpCamera(object):

    def on_update(self, dt):
        pass

    def on_target_pos_changed(self, diff_vec):
        pass

    def set_camera_setting(self, transform, fov):
        pass

    def check_slerp_mid_action(self, cur_percent):
        pass