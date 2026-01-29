# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComAttachableData.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from logic.gcommon.common_const.building_const import B_SKATE, SKATE_BOUNDING_BOX_TUPLE

class ComAttachableData(UnitCom):
    BIND_EVENT = {'G_ATTACHABLE_ID': '_get_attach_id',
       'G_COLLISION_INFO': '_get_collision_info'
       }

    def __init__(self):
        super(ComAttachableData, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComAttachableData, self).init_from_dict(unit_obj, bdict)
        self._attachable_id = bdict.get('atch_id', 0)

    def get_client_dict(self):
        cdict = {'atch_id': self._attachable_id
           }
        return cdict

    def _get_attach_id(self):
        return self._attachable_id

    def _get_collision_info(self):
        if self._attachable_id == B_SKATE:
            return {'custom_box': SKATE_BOUNDING_BOX_TUPLE,'is_ori_size': True}
        else:
            return None
            return None