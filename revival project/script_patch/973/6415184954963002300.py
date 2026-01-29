# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/camctrl_base.py
from __future__ import absolute_import
from common.framework import Singleton

class CameraCtrl(Singleton):

    def init(self):
        pass

    def on_update(self, dt, yaw, pitch):
        raise NotImplementedError

    def on_enter(self):
        pass