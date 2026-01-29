# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComObserveMechaControlTargetGReceiver.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComObserveMechaControlTargetGReceiver(UnitCom):

    def init_from_dict(self, unit_obj, bdict):
        super(ComObserveMechaControlTargetGReceiver, self).init_from_dict(unit_obj, bdict)
        self.init_global_event()

    def init_global_event(self):
        emgr = global_data.emgr
        emgr.camera_switch_to_state_event += self.switch_camera_state
        emgr.free_camera_switch_finish_event += self.free_camera_switch_finish

    def switch_camera_state(self, *args):
        self.send_event('E_SWITCH_CAMERA_STATE_TO_MECHA_TARGET', *args)

    def free_camera_switch_finish(self):
        self.send_event('E_FREE_CAMERA_SWITCH_FINISH')