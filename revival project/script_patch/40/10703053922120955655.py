# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWaterHuman.py
from __future__ import absolute_import
from .ComWater import ComWater
from logic.gcommon.common_const import water_const, scene_const
from logic.gcommon.common_const.collision_const import WATER_GROUP, WATER_MASK
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import common.utils.timer as timer
from logic.gcommon.common_utils import parachute_utils
water_mtl_set = set((scene_const.MTL_WATER, scene_const.MTL_DEEP_WATER))
UP_OFFSET_Y = 4 * NEOX_UNIT_SCALE
LOW_OFFSET_Y = 2 * NEOX_UNIT_SCALE

class ComWaterHuman(ComWater):
    BIND_EVENT = ComWater.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BOARD_SKATE': '_on_board_skate',
       'E_LEAVE_SKATE': '_on_leave_skate',
       'E_ON_JOIN_VEHICLE': '_on_join_vehicle',
       'E_ON_LEAVE_VEHICLE': '_on_leave_vehicle',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_ON_SAVED': '_on_saved',
       'G_CHECK_IS_IN_WATER': 'check_is_in_water',
       'G_CUR_WATER_HEIGHT': '_get_cur_water_height'
       })

    def __init__(self):
        super(ComWaterHuman, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComWaterHuman, self).init_from_dict(unit_obj, bdict)
        self._is_in_mecha_first = bdict.get('is_in_mecha', False)
        self._is_on_skate = False
        self._check_water_timer_id = None
        self._cur_water_height = 0
        return

    def on_init_complete(self):
        super(ComWaterHuman, self).on_init_complete()
        is_avatar = self.ev_g_is_avatar()
        if self._is_in_mecha_first:
            self.need_update = False
        if self.ev_g_is_avatar() or self.unit_obj.is_robot():
            self._check_water_timer_id = global_data.game_mgr.register_logic_timer(self.check_water_tick, 0.1, times=-1, mode=timer.CLOCK)

    def destroy(self):
        super(ComWaterHuman, self).destroy()
        if self._check_water_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._check_water_timer_id)
            self._check_water_timer_id = None
        return

    def _get_cur_water_height(self):
        return self._cur_water_height

    def check_water_tick(self, *args):
        old_is_in_water_area = self._is_in_water_area
        self._is_in_water_area = self.check_is_in_water()
        if not self._is_in_water_area and old_is_in_water_area:
            char_ctrl = self.sd.ref_character
            if not char_ctrl:
                return
            gravity = char_ctrl.getGravity()
            if gravity == 0:
                self.send_event('E_RESET_GRAVITY', True)
            char_ctrl.unlimitHeight()
            char_ctrl.unLimitLowerHeight()

    def _enable_update(self, value):
        if self._is_in_mecha_first and value:
            self._is_in_mecha_first = False
            return
        self.need_update = value
        if not value:
            self.sd.ref_water_status = water_const.WATER_NONE
            self.change_status(self.sd.ref_water_status)

    def check_is_in_water(self, up_offset=UP_OFFSET_Y, low_offset=LOW_OFFSET_Y, query_pos=None):
        scn = self.scene
        if not scn:
            return False
        pos = query_pos
        if not pos:
            pos = self.get_pos()
        if not pos:
            return False
        material_index = scn.get_scene_info_2d(pos.x, pos.z)
        material_index = self.check_material_index(material_index)
        if material_index not in water_mtl_set:
            return False
        chect_begin = math3d.vector(pos.x, pos.y + up_offset, pos.z)
        check_end = math3d.vector(pos.x, pos.y - low_offset, pos.z)
        is_multi_select = False
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, WATER_GROUP, WATER_MASK, collision.EQUAL_FILTER, is_multi_select)
        if not result[0]:
            return False
        col_obj = result[5]
        if not col_obj:
            return False
        if col_obj.group == WATER_GROUP and col_obj.mask == WATER_MASK:
            hit_point = result[1]
            if hit_point:
                self._cur_water_height = hit_point.y
            return True
        return False

    def sort_cmp(self, c1, c2):
        if c1[0].y > c2[0].y:
            return 1
        else:
            if c1[0].y < c2[0].y:
                return -1
            return 0

    def _on_board_skate(self, *args):
        self._is_on_skate = True

    def _on_leave_skate(self, *args):
        self._is_on_skate = False

    def _on_join_vehicle(self, vehicle_id, driver, passenger):
        self.need_update = False

    def _on_leave_vehicle(self, vehicle_info):
        self._is_in_mecha_first = False
        self.need_update = True

    def _on_join_mecha(self, *args, **kwargs):
        self.need_update = False
        self.sd.ref_water_status = water_const.WATER_NONE
        self.change_status(self.sd.ref_water_status)

    def _on_leave_mecha(self, *args):
        self._is_in_mecha_first = False
        self.need_update = True

    def get_pos(self):
        pos = self.ev_g_position()
        if self._is_on_skate:
            pos.y -= 1
        return pos

    def change_status(self, last_status, water_height=None, water_depth=0):
        super(ComWaterHuman, self).change_status(last_status, water_height)
        if last_status > water_const.WATER_NONE and self.sd.ref_parachute_stage != parachute_utils.STAGE_LAND and not self.ev_g_in_mecha():
            self.send_event('E_LAND')
        self.send_event('E_WATER_EVENT', last_status, water_height)
        self.send_event('E_CALL_SYNC_METHOD', 'change_water_status', (last_status, water_height, water_depth), True)

    def _on_saved(self):
        self.change_status(self.sd.ref_water_status, self.last_water_height)