# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartArtCheckCtrl.py
from __future__ import absolute_import
from .PartLobbyCtrl import PartLobbyCtrl

class PartArtCheckCtrl(PartLobbyCtrl):

    def __init__(self, scene, name):
        super(PartArtCheckCtrl, self).__init__(scene, name)
        global_data.in_artcheck_scene = True

    def register_keys(self):
        from .keyboard import ArtCheckKeyboard
        self.key_ctrls = [
         ArtCheckKeyboard.ArtCheckKeyboard()]
        for key_ctrl in self.key_ctrls:
            key_ctrl.install()
            key_ctrl.enable()

    def unregister_keys(self):
        for key_ctrl in self.key_ctrls:
            key_ctrl.disable()
            key_ctrl.uninstall()

        self.key_ctrls = []

    def on_touch_begin(self, touches):
        super(PartArtCheckCtrl, self).on_touch_begin(touches)
        global_data.emgr.scene_on_touched.emit(True)

    def on_touch_end(self, touches):
        super(PartArtCheckCtrl, self).on_touch_end(touches)
        global_data.emgr.scene_on_touched.emit(False)