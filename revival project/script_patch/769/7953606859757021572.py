# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEDynamicDoorCollision.py
from __future__ import absolute_import
import math3d
from logic.gcommon.common_const.collision_const import REGION_BOUNDARY_SCENE_GROUP, REGION_BOUNDARY_SCENE_MASK, TERRAIN_MASK, TERRAIN_GROUP, GROUP_CHARACTER_EXCLUDE, GROUP_STATIC_SHOOTUNIT, GROUP_CHARACTER_INCLUDE
from ..UnitCom import UnitCom
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComPVEDynamicDoorCollision(UnitCom):
    BIND_EVENT = {}
    RES_PATH = 'model_new/scene/box/pve_door_1.gim'
    UP = math3d.vector(0, 1, 0)
    RIGHT = math3d.vector(1, 0, 0)
    SIZE_Z = 50
    SCALE_Z = 0.02

    def __init__(self):
        super(ComPVEDynamicDoorCollision, self).__init__()
        self.model_id = None
        self.col_model = None
        self.col = None
        self.col_2 = None
        self.sweeper = None
        self.sweep_cnt = 0
        self.ori_pos = math3d.vector(0, 0, 0)
        self.tick_dt = 0
        self.col_tag = True
        self.last_check_pos = math3d.vector(0, 0, 0)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEDynamicDoorCollision, self).init_from_dict(unit_obj, bdict)
        self.pos_left = math3d.vector(*bdict.get('pos_left'))
        self.pos_right = math3d.vector(*bdict.get('pos_right'))
        self.scale = bdict.get('scale')
        self.height = 300 * NEOX_UNIT_SCALE
        self.offset = bdict.get('offset')
        self.face_pos = math3d.vector(*bdict.get('face_point'))

    def on_post_init_complete(self, bdict):
        self.init_col_model()

    def init_col_model(self):
        self.model_id = global_data.model_mgr.create_model_in_scene(self.RES_PATH, on_create_func=self.init_col)

    def init_col(self, model):
        model.visible = False
        pos = (self.pos_left + self.pos_right) * 0.5
        pos.y += self.offset - 30
        diff = self.pos_left - self.pos_right
        diff.y = 0
        diff.normalize()
        dire = self.face_pos - pos
        dire.normalize()
        r = diff.cross(self.UP)
        r.normalize()
        r_matrix = math3d.matrix.make_orient(r, self.UP)
        if r_matrix.forward.dot(dire) < 0:
            r_matrix = math3d.matrix.make_orient(-r, self.UP)
        scale_x = (self.pos_left - self.pos_right).length / (model.bounding_box.x * 2.0)
        scale_x *= self.scale
        scale_z = self.SCALE_Z
        scale_y = self.height / (model.bounding_box.y * 2.0)
        model.world_scale = math3d.vector(scale_x, scale_y, scale_z)
        model.rotation_matrix = r_matrix
        model.world_position = pos
        model.set_col_group_mask(TERRAIN_MASK, TERRAIN_MASK)
        model.active_collision = True
        self.col_model = model
        self.init_shoot_col()

    def init_shoot_col(self):
        diff = self.pos_left - self.pos_right
        size_x = diff.length * 0.5
        size_y = self.height
        size_z = self.SIZE_Z * 0.5
        size_x *= self.scale
        self.col = collision.col_object(collision.BOX, math3d.vector(size_x, size_y, size_z))
        self.col.group = GROUP_STATIC_SHOOTUNIT
        self.col.mask = GROUP_CHARACTER_EXCLUDE
        pos = (self.pos_left + self.pos_right) * 0.5
        pos.y += self.offset
        diff.y = 0
        diff.normalize()
        r = diff.cross(self.UP)
        r.normalize()
        r_matrix = math3d.matrix.make_orient(r, self.UP)
        scene = global_data.game_mgr.get_cur_scene()
        scene.scene_col.add_object(self.col)
        fix_dire = r_matrix.forward
        dire = self.face_pos - pos
        dire.normalize()
        if fix_dire.dot(dire) < 0:
            fix_dire = -fix_dire
        fix_pos = pos - fix_dire * self.SIZE_Z * 0.5
        self.col.position = fix_pos
        self.col.rotation_matrix = r_matrix
        self.col_2 = collision.col_object(collision.BOX, math3d.vector(size_x, size_y, size_z))
        self.col_2.group = GROUP_STATIC_SHOOTUNIT
        self.col_2.mask = GROUP_CHARACTER_EXCLUDE
        scene.scene_col.add_object(self.col_2)
        fix_pos = pos - fix_dire * self.SIZE_Z * 1.1
        self.col_2.position = fix_pos
        self.col_2.rotation_matrix = r_matrix
        self.need_update = True

    def tick(self, dt):
        if not self.col_tag and self.col_model:
            self.col_model.active_collision = True
            self.col_tag = True
            return
        else:
            self.tick_dt += dt
            if self.tick_dt > 2.0 and self.col_tag and self.col_model:
                if global_data.mecha and global_data.mecha.logic:
                    cur_pos = global_data.mecha.logic.ev_g_position() if 1 else None
                    if not cur_pos:
                        return
                    if (cur_pos - self.last_check_pos).length < 0.05:
                        S1 = cur_pos - self.pos_left
                        S1.y = 0
                        S2 = self.pos_right - self.pos_left
                        S2.y = 0
                        cross = S1.cross(S2)
                        dis = cross.length / S2.length
                        if dis < 3.0 * NEOX_UNIT_SCALE:
                            self.col_model.active_collision = False
                            self.col_tag = False
                            self.tick_dt = 0
                    self.last_check_pos = cur_pos
            return

    def destroy(self):
        self.model_id and global_data.model_mgr.remove_model_by_id(self.model_id)
        self.model_id = None
        self.col_model = None
        scene = global_data.game_mgr.get_cur_scene()
        self.col and scene.scene_col.remove_object(self.col)
        self.col = None
        self.col_2 and scene.scene_col.remove_object(self.col_2)
        self.col_2 = None
        self.sweeper and scene.scene_col.remove_object(self.sweeper)
        self.sweeper = None
        super(ComPVEDynamicDoorCollision, self).destroy()
        return