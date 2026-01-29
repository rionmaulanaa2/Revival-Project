# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPosRareMove.py
from __future__ import absolute_import
from six.moves import range
from ..UnitCom import UnitCom
import logic.gcommon.time_utility as t_util
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
MAX_DIS_SYNC_STATIC_POS = 200.0 * NEOX_UNIT_SCALE

class ComPosRareMove(UnitCom):
    BIND_EVENT = {'G_MOVE_ID': '_get_move_id',
       'E_DYBOX_ON_STATIC_TRANSFORM_SYNC': '_on_static_pos_sync',
       'E_DYBOX_TRI_STATIC_TRANSFORM': '_tri_static_transform'
       }

    def __init__(self):
        super(ComPosRareMove, self).__init__()
        self._move_id = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPosRareMove, self).init_from_dict(unit_obj, bdict)
        self._move_id = bdict.get('move_id', 0)
        self._trans_info = bdict.get('trans_info', None) or [ 0 for x in range(0, 16) ]
        return

    def on_init_complete(self):
        self._fit_trans()

    def _get_move_id(self):
        return self._move_id

    def _on_static_pos_sync(self, move_id, lst_transform_info):
        self._move_id = move_id
        self._trans_info = lst_transform_info
        self._fit_trans()

    def _fit_trans(self):
        m = self.ev_g_model()
        if m:
            mat = math3d.matrix()
            mat.set_all(self._trans_info)
            m.world_transformation = mat
            self.send_event('E_COL_POS', m.world_position - m.rotation_matrix.mulvec3x3(math3d.vector(0, -0.5 * m.center.y, 0)), m.rotation_matrix)

    def _tri_static_transform(self):
        m = self.ev_g_model()
        if m:
            mat = m.world_transformation
            lst = [ mat.get(i, j) for i in range(0, 4) for j in range(0, 4) ]
        AvatarSend = global_data.player.logic.send_event
        move_id = self._move_id
        obj_id = self.unit_obj.id
        lst_transform_info = lst
        AvatarSend('E_CALL_SYNC_METHOD', 'dy_box_static_transform', (obj_id, move_id, lst_transform_info))