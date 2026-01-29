# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainCollision.py
from __future__ import absolute_import
import math3d
import collision
import world
from logic.gcommon.common_const import collision_const
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.framework import Functor
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import building_const as b_const
from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_AUTO_AIM, GROUP_GRENADE, GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT, GROUP_CAMERA_COLL
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr

class ComTrainCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SET_COL_POS_AND_ROT': 'set_pos_and_rot',
       'G_COL': 'get_col'
       })

    def __init__(self):
        super(ComTrainCollision, self).__init__()
        self.timer_id = None
        self.col = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainCollision, self).init_from_dict(unit_obj, bdict)
        self._carriage_idx = bdict.get('carriage_idx')
        self._destruction_timer = None
        return

    def get_col(self):
        return self.col

    def destroy(self):
        super(ComTrainCollision, self).destroy()
        if self._destruction_timer:
            global_data.game_mgr.unregister_logic_timer(self._destruction_timer)
            self._destruction_timer = None
        return

    def _on_model_loaded(self, m):
        start, end = (None, None)
        self._model = m
        self.col = collision.col_object(collision.MESH, m, 0, 0, 0, True)
        self.col.mask = collision_const.GROUP_MECHA_BALL | collision_const.GROUP_GRENADE | collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_CAMERA_COLL | collision_const.GROUP_AUTO_AIM | collision_const.GROUP_SHOOTUNIT
        self.col.group = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_CAMERA_INCLUDE
        self.col.position = m.world_position
        self.col.rotation_matrix = m.rotation_matrix
        scn = self.scene
        scn.scene_col.add_object(self.col)
        self.send_event('E_COLLSION_LOADED', m, self.col)
        return None

    def set_pos_and_rot(self, pos, rot):
        self.col.position = pos
        self.col.rotation_matrix = rot

    def train_trigger_call_back(self, *args):
        carriage_no, col_obj, tri_obj, is_in = args
        if is_in:
            self.send_event('E_PLAYER_ENTER_TRAIN', tri_obj)
        else:
            self.send_event('E_PLAYER_LEAVE_TRAIN', tri_obj)