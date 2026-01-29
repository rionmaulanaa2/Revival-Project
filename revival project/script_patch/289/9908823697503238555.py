# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartProfile.py
from __future__ import absolute_import
from .ScenePart import ScenePart
import math
import math3d

class PartProfile(ScenePart):

    def __init__(self, scene, name):
        super(PartProfile, self).__init__(scene, name, True)
        self._ui = None
        self._update_step = 100
        return

    def on_load(self):
        pass

    def on_exit(self):
        self.destroy_ui()

    def create_ui(self):
        if self._ui is None:
            from logic.comsys.profile_logger.ProfileUI import ProfileUI
            self._ui = ProfileUI()
        return

    def destroy_ui(self):
        self._ui = None
        global_data.ui_mgr.close_ui('ProfileUI')
        return

    def on_update(self, dt):
        if self._ui:
            if self._update_step:
                self._update_step -= 1
                return
            self._update_step = 100
            count = len(self.scene().get_models())
            self._ui.set_model_count(count)