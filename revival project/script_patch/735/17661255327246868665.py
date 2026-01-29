# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDynamicBoxAppearance.py
from __future__ import absolute_import
import math3d
import collision
import world
import random
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_CAMERA_INCLUDE, GROUP_CAN_SHOOT
from data.c_item_flown_data import data as flown_data_list

class ComDynamicBoxAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_COL_POS': '_on_pos_changed',
       'E_BOOM_IMPULSE': '_boom_impulse',
       'E_ENABLE_PHYSICS': 'enable_dynamic_phy'
       })
    STABLE_TICK_CNT_LIMIT = 10

    def __init__(self):
        super(ComDynamicBoxAppearance, self).__init__()
        self.item_id = None
        self._col_obj = None
        self.is_in_impulse = False
        self.flown_info = None
        self.stable_tick_cnt = 0
        self.col_name = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComDynamicBoxAppearance, self).init_from_dict(unit_obj, bdict)
        self.item_id = bdict.get('item_id', None)
        trans_info = bdict.get('trans_info', None)
        if trans_info:
            idx = 12
            self._position = math3d.vector(*trans_info[idx:idx + 3])
        else:
            self._position = math3d.vector(0, 0, 0)
        return

    def get_model_info(self, unit_obj, bdict):
        item_id = int(bdict.get('item_id', 1))
        self.flown_info = flown_data_list.get(item_id, None)
        mpath = self.flown_info.get('cRes', '')
        self.col_name = mpath.split('.gim')[0].split('/')[-1]
        return (
         mpath, None, None)

    def on_load_model_complete(self, model, userdata):
        model.position = self._position
        bnpc = self.unit_obj.get_owner()
        eid = self.unit_obj.id
        global_data.emgr.scene_add_dynamic_box.emit(eid, model.name, bnpc)
        model.world_position = model.world_position - model.center + math3d.vector(130, 0, 0)
        self.init_col()
        self.enable_dynamic_phy(False)
        self.need_update = True

    def on_model_destroy(self):
        if self._col_obj:
            self.scene.scene_col.remove_object(self._col_obj)
        self._col_obj = None
        eid = self.unit_obj.id
        global_data.emgr.scene_del_dynamic_box.emit(eid, self.model.name)
        self.is_in_impulse = False
        if self.model:
            self.model.destroy()
        return

    def _on_pos_changed--- This code section failed: ---

  92       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  '_col_obj'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    39  'to 39'

  93      12  LOAD_FAST             1  'position'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  '_col_obj'
          21  STORE_ATTR            2  'position'

  94      24  LOAD_FAST             2  'rot_mat'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             1  '_col_obj'
          33  STORE_ATTR            3  'rotation_matrix'
          36  JUMP_FORWARD          0  'to 39'
        39_0  COME_FROM                '36'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def tick(self, dt):
        m = self.model
        if not m or not m.valid:
            self.need_update = False
            return
        if not self._col_obj:
            return
        cpos = self._col_obj.position + self._col_obj.rotation_matrix.mulvec3x3(math3d.vector(0, -0.5 * self.model.center.y, 0))
        m.position = cpos
        m.rotation_matrix = self._col_obj.rotation_matrix
        if self.is_in_impulse and self._col_obj.linear_velocity.length < 0.0001:
            self.stable_tick_cnt += 1
            if self.stable_tick_cnt >= self.STABLE_TICK_CNT_LIMIT:
                self.stable_tick_cnt = 0
                self.is_in_impulse = False
                self.enable_dynamic_phy(False)
                self.send_event('E_DYBOX_TRI_STATIC_TRANSFORM')

    def init_col(self):
        _scn = world.get_active_scene()
        mask = GROUP_CHARACTER_INCLUDE | GROUP_CAMERA_INCLUDE | GROUP_CAN_SHOOT
        group = GROUP_CHARACTER_INCLUDE | GROUP_CAMERA_INCLUDE | GROUP_CAN_SHOOT
        col_shape = collision.BOX
        mass = self.flown_info.get('fmass', 10000)
        shape = self.flown_info.get('iType', 0)
        col_size = self.flown_info.get('cSize', (1, 1, 1))
        if not shape:
            return
        if shape == 1:
            col_shape = collision.BOX
            col_size = math3d.vector(self.model.bounding_box.x, self.model.bounding_box.y, self.model.bounding_box.z)
        elif shape == 2:
            col_shape = collision.BOX
            col_size = math3d.vector(col_size[0], col_size[1], col_size[2])
            col_size = col_size * math3d.vector(NEOX_UNIT_SCALE, NEOX_UNIT_SCALE, NEOX_UNIT_SCALE)
        elif shape == 3:
            col_shape = collision.SPHERE
            col_size = math3d.vector(col_size[0], col_size[1], col_size[2])
            col_size = col_size * math3d.vector(NEOX_UNIT_SCALE, NEOX_UNIT_SCALE, NEOX_UNIT_SCALE)
        self._col_obj = collision.col_object(col_shape, col_size, mask, group, mass)
        self._col_obj.position = self.model.center_w
        self._col_obj.rotation_matrix = self.model.world_rotation_matrix
        special_name = '@'.join((self.model.name, self.col_name))
        self.model.set_col_name(special_name)
        self._col_obj.model_col_name = special_name

    def enable_dynamic_phy(self, flag):
        if not self._col_obj:
            return
        _scn = world.get_active_scene()
        if not _scn:
            return
        if self.model:
            self.model.active_collision = not flag
            special_name = '@'.join((self.model.name, self.col_name))
            self.model.set_col_name(special_name)
        if flag:
            _scn.scene_col.add_object(self._col_obj)
        else:
            _scn.scene_col.remove_object(self._col_obj)

    def remove_col(self):
        if self._col_obj:
            _scn = world.get_active_scene()
            _scn.scene_col.remove_object(self._col_obj)
            self._col_obj = None
        return

    def _boom_impulse(self, center, impulse_factor):
        if not self._col_obj:
            return
        if not self.model:
            return
        impulse_dir = self.model.world_position - center
        impulse_dir.y = 0.0
        if impulse_dir.is_zero:
            return
        self.is_in_impulse = True
        self.enable_dynamic_phy(True)
        impulse_dir.normalize()
        impulse_res = math3d.vector(impulse_factor, impulse_factor, impulse_factor) * impulse_dir + math3d.vector(0, 15000 * random.uniform(0.8, 1.5), 0)
        self._col_obj.apply_impulse(impulse_res * math3d.vector(NEOX_UNIT_SCALE, NEOX_UNIT_SCALE, NEOX_UNIT_SCALE))