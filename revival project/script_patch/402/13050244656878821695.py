# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_shop/ComNeutralShopAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
from mobile.common.EntityManager import EntityManager
import world
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
USE_SUBWAY_CAR = False

class ComNeutralShopAppearance(ComBaseModelAppearance):
    TRI_RADIUS = 8
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'E_ENTER_INTERACTION_ZONE': '_enter_interaction_zone',
       'E_LEAVE_INTERACTION_ZONE': '_leave_interaction_zone',
       'E_SHOP_SELL_GOODS_CHANGE': '_on_shop_sell_goods_change'
       })

    def __init__(self):
        super(ComNeutralShopAppearance, self).__init__()
        self._trigger_radius = self.TRI_RADIUS * NEOX_UNIT_SCALE

    def init_from_dict(self, unit_obj, bdict):
        super(ComNeutralShopAppearance, self).init_from_dict(unit_obj, bdict)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        if USE_SUBWAY_CAR:
            model_path = confmgr.get('script_gim_ref')['item_subway_car']
        else:
            model_path = confmgr.get('script_gim_ref')['item_shop_car']
        return (model_path, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, userdata):
        import math3d
        import collision
        import render
        import game3d
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        model.world_position = pos
        from logic.gcommon.common_utils.building_utils import get_bounding_box_slope_rot_mat
        rot_mat = get_bounding_box_slope_rot_mat(model, 0.7)
        if USE_SUBWAY_CAR:
            model.lod_config = (500, -1)
        model.rotation_matrix = rot_mat
        model.active_collision = True
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())

    def on_model_destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            length = lpos.length
            if length <= self._trigger_radius:
                return (True, length)
        return (False, None)

    def _enter_interaction_zone(self, eid):
        if eid:
            self.send_event('E_CALL_SYNC_METHOD', 'enter_shop', (eid,))

    def _leave_interaction_zone(self, eid):
        if eid:
            self.send_event('E_CALL_SYNC_METHOD', 'leave_shop', (eid,))