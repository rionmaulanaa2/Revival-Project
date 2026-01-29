# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFlagBuildingCollision.py
from __future__ import absolute_import
import math3d
import collision
import world
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import building_const as b_const
from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_AUTO_AIM, GROUP_GRENADE, GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT, GROUP_CAMERA_COLL
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr

class ComFlagBuildingCollision(ComCommonShootCollision):

    def __init__(self):
        super(ComFlagBuildingCollision, self).__init__()
        self.timer_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlagBuildingCollision, self).init_from_dict(unit_obj, bdict)
        self._building_no = bdict.get('building_no', None)
        self._hitable = bdict.get('hitable', False)
        self._owner_id = bdict.get('owner_id', None)
        self._destruction_timer = None
        self._building_conf = confmgr.get('c_building_res', str(self._building_no))
        return

    def destroy(self):
        super(ComFlagBuildingCollision, self).destroy()
        if self._destruction_timer:
            global_data.game_mgr.unregister_logic_timer(self._destruction_timer)
            self._destruction_timer = None
        return

    def _on_model_loaded(self, m):
        start, end = (None, None)
        self.col = collision.col_object(collision.MESH, m, 0, 0, 0, True)
        start, end = m.world_position, m.world_position
        start.y -= m.bounding_box.y * 2
        self.col.mask = 0
        self.col.group = 0
        self.col.position = end
        self.col.rotation_matrix = m.rotation_matrix
        self._raise_up(start, end)
        scn = self.scene
        scn.scene_col.add_object(self.col)
        if self._hitable:
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        if self.non_explosion_dis:
            global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
        self.send_event('E_COLLSION_LOADED', m, self.col)
        return None

    def _raise_up(self, start, end, tick_count=20):
        self.cnt = 0

        def _raise():
            if not self or not self.is_valid():
                return
            else:
                self.cnt += 1
                pos = math3d.vector(0, 0, 0)
                u = self.cnt * 1.0 / tick_count
                if u > 1.0:
                    u = 1.0
                    global_data.game_mgr.get_logic_timer().unregister(self.timer_id)
                    self.timer_id = None
                pos.intrp(start, end, u)
                if self.col:
                    self.col.position = pos
                return

        if self.timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self.timer_id)
            self.timer_id = None
        self.timer_id = global_data.game_mgr.get_logic_timer().register(func=_raise, interval=0.03, times=-1, mode=CLOCK)
        return

    def _self_destruction(self):
        if self._owner_id is None:
            return
        else:
            parent = EntityManager.getentity(self._owner_id)
            if parent and parent.logic:
                parent.logic.send_event('E_CALL_SYNC_METHOD', 'disable_building', (self.unit_obj.id,), True)
            return