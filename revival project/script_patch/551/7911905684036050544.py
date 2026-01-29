# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/ObjectTransformSystem.py
from __future__ import absolute_import
from .SystemBase import SystemBase
from ..client.ComDataAppearance import ComDataAppearance
from ..client.ComDataRenderRotate import ComDataRenderRotate
from ..client.ComDataLogicLod import ComDataLogicLod
import profiling

class ObjectTransformSystem(SystemBase):

    def __init__(self):
        super(ObjectTransformSystem, self).__init__()

    def interested_type(self):
        return (
         ComDataAppearance, ComDataRenderRotate, ComDataLogicLod)

    def handler_types(self):
        return []

    def add_handler(self, handler_type, handler):
        raise NotImplementedError()

    def remove_handler(self, handler_type, handler):
        raise NotImplementedError()

    def tick(self, dt):
        for unit in self._element_list:
            data = unit.sd.ref_appearance
            if data.model:
                rotdata = data.sd.ref_rotatedata
                if rotdata.dirty or data.force_sync_once:
                    ret = rotdata.rotation_mat
                    data.model.world_rotation_matrix = ret
                    data.force_sync_once = False