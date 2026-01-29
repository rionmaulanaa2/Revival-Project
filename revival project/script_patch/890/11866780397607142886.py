# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSyncReceiverData.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from ..system import ComSystemMgr

class ComSyncReceiverData(UnitCom):

    def __init__(self):
        super(ComSyncReceiverData, self).__init__()
        self.yaw = 0
        self.yaw_diff = 0
        self.pitch = 0
        self.pitch_diff = 0
        self.cam_yaw = 0
        self.cam_pitch = 0
        self.dirty = False
        self._in_system = False
        self.force_turn_body = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComSyncReceiverData, self).init_from_dict(unit_obj, bdict)
        unit_obj.sd.ref_rotatedata = self
        self.dirty = False
        self._add_to_system()

    def cache(self):
        self._remove_from_system()
        self.unit_obj.sd.ref_rotatedata = None
        self.yaw = 0
        self.yaw_diff = 0
        self.pitch = 0
        self.cam_yaw = 0
        self.cam_pitch = 0
        self.dirty = False
        super(ComSyncReceiverData, self).cache()
        return

    def destroy(self):
        self._remove_from_system()
        if self.unit_obj.sd.ref_rotatedata:
            self.unit_obj.sd.ref_rotatedata = None
        super(ComSyncReceiverData, self).destroy()
        return

    def mark_dirty(self):
        self.dirty = True

    def _add_to_system(self):
        ComSystemMgr.g_com_sysmgr.add_data(self)
        self._in_system = True

    def _remove_from_system(self):
        if self._in_system:
            ComSystemMgr.g_com_sysmgr.remove_data(self)
            self._in_system = False