# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCommonShootCollision.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT, GROUP_GRENADE
from logic.gcommon.const import NEOX_UNIT_SCALE
import collision

class ComCommonShootCollision(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'G_CHECK_SHOOT_INFO': '_check_shoot_info',
       'G_CID': '_get_cid',
       'G_COL': 'get_col',
       'G_COL_ID': 'get_col_id',
       'E_DESTROY_SHOOT_COLLISION': '_destroy_shoot_collision',
       'G_IS_PIERCED': 'on_is_pierced'
       }

    def __init__(self):
        super(ComCommonShootCollision, self).__init__()
        self.non_explosion_dis = False
        self.col = None
        self.offset = None
        return

    def cache(self):
        self._destroy_shoot_collision()
        self.non_explosion_dis = False
        self.offset = None
        super(ComCommonShootCollision, self).cache()
        return

    def _on_pos_changed(self, pos):
        if self.col and pos:
            self.col.position = pos + self.offset if self.offset else pos

    def _get_offset_by_str(self, offset, v):
        if offset == 'half_y':
            offset = math3d.vector(0, v.y, 0)
        elif offset == 'half_x':
            offset = math3d.vector(v.x, 0, 0)
        elif offset == 'half_z':
            offset = math3d.vector(0, 0, v.z)
        else:
            offset = math3d.vector(0, 0, 0)
        return offset

    def _col_load_complete(self):
        pass

    def _check_shoot_info(self, begin, pdir, hit_pos=None):
        return 0

    def _on_model_loaded(self, model, custom_pos=None, custom_col_group=None):
        if custom_col_group and self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        if self.col:
            return
        else:
            if not self.scene:
                return
            v = model.bounding_box
            scale = model.world_scale
            rot = model.world_rotation_matrix
            self.offset = math3d.vector(0, 0, 0)
            need_update_pos = False
            collision_info = self.ev_g_collision_info()
            if collision_info:
                scale = collision_info.get('scale', scale)
                rot = collision_info.get('rotation', rot)
                self.offset = collision_info.get('offset', self.offset)
                self.offset = self._get_offset_by_str(self.offset, v) if type(self.offset) is str else self.offset
                need_update_pos = collision_info.get('need_update', need_update_pos)
                self.non_explosion_dis = collision_info.get('non_explosion_dis', False)
                custom_box = collision_info.get('custom_box', None)
                if custom_box:
                    is_ori_size = collision_info.get('is_ori_size', False)
                    if is_ori_size:
                        v = math3d.vector(custom_box[0], custom_box[1], custom_box[2])
                    else:
                        v = math3d.vector(custom_box[0] * NEOX_UNIT_SCALE, custom_box[1] * NEOX_UNIT_SCALE, custom_box[2] * NEOX_UNIT_SCALE)
            self.col = collision.col_object(collision.BOX, v * scale)
            self.col.rotation_matrix = rot
            self.col.mask = GROUP_GRENADE
            self.col.group = GROUP_SHOOTUNIT
            self.col.model_col_name = model.name
            if custom_col_group:
                self.col.group |= custom_col_group
            if collision_info:
                bind_bone = collision_info.get('bind_bone', None)
            else:
                bind_bone = None
            if bind_bone:
                model.bind_col_obj(self.col, bind_bone)
            else:
                self.scene.scene_col.add_object(self.col)
            if need_update_pos:
                if G_POS_CHANGE_MGR:
                    self.regist_pos_change(self._on_pos_changed)
                else:
                    self._bind_event({'E_POSITION': '_on_pos_changed'})
            if custom_pos:
                self.col.position = custom_pos + self.offset
            else:
                self.col.position = self.ev_g_position() + self.offset
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
            if self.non_explosion_dis:
                global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
            self._col_load_complete()
            return

    def _get_cid(self):
        if not self.col:
            return None
        else:
            return self.col.cid

    def get_col(self):
        return self.col

    def get_col_id(self):
        if not self.col:
            return None
        else:
            return self.col.cid

    def _destroy_shoot_collision(self):
        if self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            if self.non_explosion_dis:
                global_data.war_non_explosion_dis_objs.pop(self.col.cid)
            self.col = None
        return

    def destroy(self):
        self._destroy_shoot_collision()
        super(ComCommonShootCollision, self).destroy()

    def on_is_pierced(self):
        return True