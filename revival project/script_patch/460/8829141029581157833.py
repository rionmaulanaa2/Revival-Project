# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWaterMotorcycle.py
from __future__ import absolute_import
from __future__ import print_function
from .ComWater import ComWater
from logic.gcommon.common_const import water_const, scene_const, collision_const
from logic.gcommon.common_const.collision_const import WATER_GROUP, WATER_MASK
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import common.utils.timer as timer
from logic.gcommon.cdata import speed_physic_arg
from logic.gcommon.cdata import mecha_status_config
water_mtl_set = set((scene_const.MTL_WATER, scene_const.MTL_DEEP_WATER))
UP_OFFSET_Y = 4 * NEOX_UNIT_SCALE
LOW_OFFSET_Y = 2 * NEOX_UNIT_SCALE
LOWER_ABOVE_WATER_HEIGHT = 10
UPPER_ABOVE_WATER_HEIGHT = 30
FOOT_TO_WATER_DIST = 40

class ComWaterMotorcycle(ComWater):
    BIND_EVENT = ComWater.BIND_EVENT.copy()
    BIND_EVENT.update({'G_CHECK_IS_IN_WATER': 'check_is_in_water',
       'G_CUR_WATER_HEIGHT': '_get_cur_water_height',
       'E_SET_STATIC_COLLISON': 'change_driver',
       'E_CHARACTER_ACTIVE': 'change_driver',
       'E_CHECK_WATER_AREA': 'check_water_tick',
       'E_CHARACTER_ATTR': '_change_character_attr'
       })

    def __init__(self):
        super(ComWaterMotorcycle, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComWaterMotorcycle, self).init_from_dict(unit_obj, bdict)
        self._check_water_timer_id = None
        self._cur_water_height = 0
        self._is_float_up = False
        return

    def on_init_complete(self):
        super(ComWaterMotorcycle, self).on_init_complete()
        self.need_update = True
        self.change_driver()

    def _change_character_attr(self, name, *arg):
        if name == 'dump_character':
            print(('test--ComWaterMotorcycle.dump_character--_is_in_water_area =', self._is_in_water_area, '--_cur_water_height =', self._cur_water_height, '--_check_water_timer_id =', self._check_water_timer_id, '--unit_obj =', self.unit_obj))

    def destroy(self):
        super(ComWaterMotorcycle, self).destroy()
        if self._check_water_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._check_water_timer_id)
            self._check_water_timer_id = None
        return

    def get_pos(self):
        return self.ev_g_position()

    def check_material_index(self, material_index):
        if material_index == scene_const.MTL_DEEP_WATER or material_index == scene_const.MTL_WATER:
            scn = self.scene
            if not scn:
                return scene_const.MTL_SAND
            pos = self.get_pos()
            if not pos:
                return scene_const.MTL_SAND
            p1 = math3d.vector(pos.x, pos.y + UP_OFFSET_Y, pos.z)
            p2 = math3d.vector(pos.x, pos.y - LOW_OFFSET_Y, pos.z)
            if p1.y <= self.DEFAULT_WATER_HEIGHT:
                p1.y = self.DEFAULT_WATER_HEIGHT + NEOX_UNIT_SCALE
            result = scn.scene_col.hit_by_ray(p1, p2, 0, collision_const.WATER_GROUP, collision_const.WATER_MASK, collision.EQUAL_FILTER)
            if not result[0]:
                if global_data.debug_water_motorcycle and self.ev_g_is_avatar():
                    self.send_event('E_DRAW_LINE', [(p1, p2, 16776960)])
                return scene_const.MTL_SAND
        return material_index

    def change_driver(self, *args, **kwargs):
        if not self.ev_g_is_character_active():
            return
        else:
            if global_data.player and self.sd.ref_driver_id == global_data.player.id:
                self.check_water_tick()
                if self._check_water_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self._check_water_timer_id)
                    self._check_water_timer_id = None
                self._check_water_timer_id = global_data.game_mgr.register_logic_timer(self.check_water_tick, 0.1, times=-1, mode=timer.CLOCK)
            elif self._check_water_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._check_water_timer_id)
                self._check_water_timer_id = None
            return

    def _get_cur_water_height(self):
        return self._cur_water_height

    def check_water_tick(self, is_log=False):
        old_is_in_water_area = self._is_in_water_area
        self._is_in_water_area = self.check_is_in_water()
        if not self._is_in_water_area and (self.ev_g_is_limit_lower_height() or self.ev_g_is_limit_height()):
            self.send_event('E_UNLIMIT_LOWER_HEIGHT')
            self.send_event('E_UNLIMIT_HEIGHT')
        if global_data.debug_water_motorcycle and self.ev_g_is_avatar():
            print(('test--ComWaterMotorcycle.check_water_tick--step1--_is_in_water_area =', self._is_in_water_area, '--old_is_in_water_area =', old_is_in_water_area, '--position =', self.ev_g_position(), '--unit_obj =', self.unit_obj))
        if not self._is_in_water_area and old_is_in_water_area:
            char_ctrl = self.sd.ref_character
            if not char_ctrl:
                return
            gravity = char_ctrl.getGravity()
            if gravity == 0:
                self.send_event('E_RESET_GRAVITY')
            self.send_event('E_UNLIMIT_LOWER_HEIGHT')
            self.send_event('E_UNLIMIT_HEIGHT')
        elif self._is_in_water_area and not old_is_in_water_area:
            foot_position = self.ev_g_foot_position()
            if not foot_position:
                self._is_in_water_area = False
                return
            min_height = self._cur_water_height + FOOT_TO_WATER_DIST
            if foot_position.y - self._cur_water_height > FOOT_TO_WATER_DIST:
                self._is_in_water_area = False
            else:
                self.send_event('E_PLAY_DROP_WATER', self.ev_g_position(), self.ev_g_vertical_speed())
                self.send_event('E_LIMIT_LOWER_HEIGHT', self._cur_water_height)
                min_height = self._cur_water_height + UPPER_ABOVE_WATER_HEIGHT
                if self.ev_g_is_float_jump():
                    self.send_event('E_LOGIC_ON_GROUND', self.ev_g_vertical_speed())
                self.send_event('E_VERTICAL_SPEED', 0)
                self.send_event('E_GRAVITY', 0)
        self.float_up_in_water_tick()

    def float_up_in_water_tick(self, *args):
        if not self._is_in_water_area:
            return
        foot_position = self.ev_g_foot_position()
        if not foot_position:
            return
        min_height = self._cur_water_height + UPPER_ABOVE_WATER_HEIGHT
        if foot_position.y >= min_height:
            if self._is_float_up:
                self._is_float_up = False
                self.send_event('E_VERTICAL_SPEED', 0)
            return
        self._is_float_up = True
        vertical_speed = self.ev_g_vertical_speed()
        if vertical_speed <= 0:
            self.send_event('E_VERTICAL_SPEED', speed_physic_arg.swim_vertical_speed)

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