# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAimLockedUI.py
from __future__ import absolute_import
import math3d
import world
import render
from ..UnitCom import UnitCom
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref

class ComAimLockedUI(UnitCom):
    MAX_GRADE = 5
    BIND_EVENT = {'E_BEING_LOCK_TARGET': 'on_being_aim_target'
       }

    def __init__(self):
        super(ComAimLockedUI, self).__init__()
        self._warning_ui = None
        self._warning_bg = None
        self._aim_source = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAimLockedUI, self).init_from_dict(unit_obj, bdict)

    def tick(self, delta):
        if self._warning_ui:
            model = self.ev_g_model()
            if model:
                pos = model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                max_dist = 300
                scale = (max_dist - dist) * 1.0 / max_dist
                self._warning_ui.scale = (scale, scale)

    def _create_warning_ui(self):
        pass

    def _destroy_warning_ui(self):
        if self._warning_ui and self._warning_ui.valid:
            self._warning_ui.destroy()
        self._warning_ui = None
        self._warning_bg = None
        self.need_update = False
        return

    def destroy(self):
        self._destroy_warning_ui()
        self._aim_source = {}
        super(ComAimLockedUI, self).destroy()

    def on_being_aim_target(self, from_entity_id, is_target):
        if not self.ev_g_is_cam_target():
            return
        import time
        if is_target:
            self._aim_source[from_entity_id] = time.time()
        elif from_entity_id in self._aim_source:
            del self._aim_source[from_entity_id]
        self.check_aim_source()

    def check_aim_source(self):
        if len(self._aim_source) > 0:
            self._create_warning_ui()
        else:
            self._destroy_warning_ui()