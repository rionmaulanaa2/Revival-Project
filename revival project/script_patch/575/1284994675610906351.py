# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_field/ComFieldShieldCollision.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
from common.cfg import confmgr
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT, GROUP_SHIELD, GROUP_GRENADE
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import MECHA_STAND_HEIGHT
import collision
from common.utils.sfxmgr import CREATE_SRC_SIMPLE

class ComFieldShieldCollision(UnitCom):
    BIND_EVENT = {'E_HIT_FIELD_SHIELD': 'on_check_shield_hit',
       'E_POS_CHANGED': 'on_shield_collison_moved',
       'G_IS_PIERCED': 'on_is_pierced'
       }
    SHIELD_SFX = 'effect/fx/robot/autobot/pinzhang_hit.sfx'
    FIELD_SFX_BEGIN = 'effect/fx/robot/common/huzhao_qiu_start.sfx'
    FIELD_SFX_END = 'effect/fx/robot/common/huzhao_qiu_end.sfx'

    def __init__(self):
        super(ComFieldShieldCollision, self).__init__()
        self.shield_col = None
        self.shield_radius = 0
        self.shield_pos = None
        self.shield_sfx = None
        self.creator_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFieldShieldCollision, self).init_from_dict(unit_obj, bdict)
        npc_id = bdict.get('npc_id', 0)
        self.creator_id = bdict.get('creator_id', None)
        field_conf = confmgr.get('field_data', str(npc_id), default={})
        need_collision = field_conf.get('iNeedShieldCollision', False)
        scn_col = self.scene.scene_col if self.scene else None
        if need_collision and scn_col:
            self.shield_radius = bdict.get('range', 0)
            self.shield_col = collision.col_object(collision.SPHERE, math3d.vector(self.shield_radius, 0, 0), 0, 0, 0)
            self.shield_col.mask = GROUP_GRENADE
            self.shield_col.group = GROUP_SHOOTUNIT | GROUP_SHIELD
            self.shield_pos = math3d.vector(*bdict['position'])
            self.shield_col.position = self.shield_pos
            self.shield_col.position += math3d.vector(0, MECHA_STAND_HEIGHT * 0.5, 0)
            scn_col.add_object(self.shield_col)
            if self.creator_id:
                from mobile.common.EntityManager import EntityManager
                entity = EntityManager.getentity(self.creator_id)
                if entity and entity.logic:
                    entity.logic.send_event('E_MODIFY_MECHA_RELATIVE_COLS', True, self.shield_col.cid)
            global_data.emgr.scene_add_field_shield_event.emit(self.shield_col.cid, self.unit_obj)
            global_data.sfx_mgr.create_sfx_in_scene(self.FIELD_SFX_BEGIN, self.shield_pos, on_create_func=self._create_shield_sfx)
        return

    def on_check_shield_hit(self, begin=None, end=None):
        if begin == None and self.shield_col is not None:
            begin = self.shield_col.position
            hit_dir = end - begin
            if hit_dir.is_zero:
                return
            hit_dir.normalize()
            hit_pos = begin + hit_dir * self.shield_radius
            hit_normal = hit_dir
            global_data.sfx_mgr.create_sfx_in_scene(self.SHIELD_SFX, hit_pos, int_check_type=CREATE_SRC_SIMPLE)
            return
        else:
            scn = global_data.game_mgr.scene
            if scn and self.shield_col:
                shield_pos = self.shield_col.position
                if self.shield_radius >= (shield_pos - begin).length:
                    return
                result = scn.scene_col.hit_by_ray(begin, end + (end - begin) * 2, 0, GROUP_GRENADE, GROUP_SHIELD | GROUP_SHOOTUNIT, collision.EQUAL_FILTER, True)
                if result[0]:
                    hit_pos = None
                    hit_normal = None
                    for cobj_info in result[1]:
                        if cobj_info[4].cid == self.shield_col.cid:
                            hit_pos = cobj_info[0]
                            hit_normal = cobj_info[1]
                            break

                    if not hit_pos or not hit_normal:
                        return

                    def create_cb(sfx):
                        sfx.scale = math3d.vector(1.5, 1.5, 1.5)
                        global_data.sfx_mgr.set_rotation_by_normal(sfx, hit_normal)

                    global_data.sfx_mgr.create_sfx_in_scene(self.SHIELD_SFX, hit_pos, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            return

    def on_shield_collison_moved(self, pos):
        if pos:
            if self.shield_col and self.shield_col.valid:
                self.shield_col.position = math3d.vector(pos)
                self.shield_col.position += math3d.vector(0, MECHA_STAND_HEIGHT * 0.5, 0)
            if self.shield_sfx and self.shield_sfx.valid:
                self.shield_sfx.position = pos

    def _create_shield_sfx(self, sfx):
        if self.is_valid():
            self.shield_sfx = sfx
        else:
            global_data.sfx_mgr.remove_sfx(sfx)

    def destroy(self):
        if self.shield_col:
            global_data.emgr.scene_remove_field_shield_event.emit(self.shield_col.cid)
            if self.creator_id:
                from mobile.common.EntityManager import EntityManager
                entity = EntityManager.getentity(self.creator_id)
                if entity and entity.logic:
                    entity.logic.send_event('E_MODIFY_MECHA_RELATIVE_COLS', False, self.shield_col.cid)
            scn_col = self.scene.scene_col if self.scene else None
            if scn_col:
                scn_col.remove_object(self.shield_col)
            shield_pos = self.shield_pos
            if self.shield_sfx and self.shield_sfx.valid:
                shield_pos = self.shield_sfx.position
            if shield_pos:
                global_data.sfx_mgr.create_sfx_in_scene(self.FIELD_SFX_END, shield_pos, int_check_type=CREATE_SRC_SIMPLE)
        if self.shield_sfx:
            global_data.sfx_mgr.remove_sfx(self.shield_sfx)
            self.shield_sfx = None
        self.creator_id = None
        self.shield_col = None
        self.shield_radius = 0
        super(ComFieldShieldCollision, self).destroy()
        return

    def on_is_pierced(self):
        return False