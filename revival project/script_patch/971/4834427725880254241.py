# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveGhostLogicClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
import world

class ComMoveGhostLogicClient(UnitCom):
    BIND_EVENT = {'E_POSITION': '_on_pos_change',
       'G_POSITION': '_get_position'
       }

    def __init__(self):
        super(ComMoveGhostLogicClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveGhostLogicClient, self).init_from_dict(unit_obj, bdict)
        self._bind_avt = bdict.get('bind_avt', None)
        self._pos = math3d.vector(*bdict.get('position', (0, 0, 0)))
        self._human_model = None
        return

    def on_init_complete(self):
        self._human_model = world.model('character/11/2000/l.gim', self.scene)
        self._human_model.world_position = self._pos
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_pos_change)

    def _get_position(self):
        return self._pos

    def destroy(self):
        if self._human_model:
            self.scene.remove_object(self._human_model)
            self._human_model.destroy()
        super(ComMoveGhostLogicClient, self).destroy()

    def _on_pos_change(self, pos):
        self._human_model.world_position = pos