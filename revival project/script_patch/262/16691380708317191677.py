# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComClawGrenadeCollision.py
from __future__ import absolute_import
from .ComGrenadeCollision import ComGrenadeCollision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.scene_utils import is_break_obj
from logic.gutils.team_utils import ignore_expolosion
from logic.gcommon.common_const.collision_const import GROUP_MECHA_BALL
import collision
import math3d
import world
UP_VECTOR = math3d.vector(0, 1, 0)

class ComClawGrenadeCollision(ComGrenadeCollision):
    STATE_HOOK_RELEASE = 1

    def init_from_dict(self, unit_obj, bdict):
        super(ComClawGrenadeCollision, self).init_from_dict(unit_obj, bdict)
        self._is_explosive = False
        self._intrp_duration = 0.15

    def cache(self):
        super(ComClawGrenadeCollision, self).cache()
        self._is_explosive = False

    def tick(self, dt):
        super(ComClawGrenadeCollision, self).tick(dt)

    def init_physical_parameters(self):
        super(ComClawGrenadeCollision, self).init_physical_parameters()
        custom_param = self.throw_info.get('custom_params', {})
        if 'weapon_max_dist_factor' in custom_param:
            self._max_distance += custom_param['weapon_max_dist_factor'] * self._max_distance
        if 'weapon_max_dist_scale' in custom_param:
            self._max_distance *= custom_param['weapon_max_dist_scale']

    def set_group_and_mask(self, obj):
        super(ComGrenadeCollision, self).set_group_and_mask(obj)
        obj.group |= GROUP_MECHA_BALL
        obj.mask |= GROUP_MECHA_BALL

    def check_is_owner_mecha(self):
        if not global_data.mecha or not global_data.mecha.logic:
            return False
        return global_data.mecha.logic.id == self._owner_id

    def _create_col_obj(self):
        super(ComClawGrenadeCollision, self)._create_col_obj()
        if not self._col_obj or not self.is_enable():
            return
        if self.check_is_owner_mecha():
            global_data.mecha.logic.send_event('E_UPDATE_HOOK_STATE', self.STATE_HOOK_RELEASE, {'target': self._col_obj})

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            if not self._is_collision_enable:
                return
            if len(args) == 3:
                cobj, point, normal = args
            else:
                my_obj, cobj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            is_ignore, cobj, point, normal = self.collision_check(cobj, point, normal, **kwargs)
            if is_ignore:
                return
            if self._hit_sfx_use_dir_normal:
                normal = self._last_check_pos - self._col_obj.position
                if normal.is_zero:
                    normal = UP_VECTOR
                else:
                    normal.normalize()
            if cobj:
                if cobj.cid in self._col_ids:
                    return
            is_trigger = self.is_trigger(cobj)
            if not is_trigger and not is_break_obj(cobj.model_col_name):
                self._contact_other_col_times += 1
                if not (self._max_contact_other_col_times > 0 and self._contact_other_col_times >= self._max_contact_other_col_times):
                    if self._col_obj.linear_velocity.length > self.COLLIDE_SOUND_SPEED_LIMIT:
                        self.play_collisions_sound(point)
                    return
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                contact_info = {}
                target_id = None
                if cobj:
                    unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                    if unit:
                        if unit.__class__.__name__ == 'LPuppet':
                            return
                        target_id = unit.id
                        if unit.ev_g_is_campmate(self.faction_id):
                            start_pos = self._col_obj.position - self._col_obj.rotation_matrix.forward * 3 * NEOX_UNIT_SCALE
                            end_pos = self._col_obj.position + self._col_obj.rotation_matrix.forward * 2 * NEOX_UNIT_SCALE
                            result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
                            overlapped_col = False
                            if result[0]:
                                for col_info in result[1]:
                                    if col_info[4] == self._col_obj:
                                        continue
                                    hit_unit = global_data.emgr.scene_find_unit_event.emit(col_info[4].cid)[0]
                                    if not hit_unit or hit_unit == unit:
                                        continue
                                    if hit_unit.ev_g_is_shield() or not hit_unit.ev_g_is_campmate(self.faction_id):
                                        target_id = hit_unit.id
                                        overlapped_col = True
                                        break

                            if not overlapped_col:
                                return
                        if self._ignore_unit_tag:
                            is_through_unit = unit.MASK & self._ignore_unit_tag
                            can_through = is_through_unit and unit.ev_g_can_through(self.faction_id)
                            if can_through:
                                overlapped_col = False
                                start_pos = self._col_obj.position - self._col_obj.rotation_matrix.forward * 3 * NEOX_UNIT_SCALE
                                end_pos = self._col_obj.position + self._col_obj.rotation_matrix.forward * 2 * NEOX_UNIT_SCALE
                                result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
                                if result[0]:
                                    for col_info in result[1]:
                                        if col_info[4] == self._col_obj:
                                            continue
                                        hit_unit = global_data.emgr.scene_find_unit_event.emit(col_info[4].cid)[0]
                                        if not hit_unit or hit_unit == unit:
                                            continue
                                        if hit_unit.ev_g_is_shield() or not hit_unit.ev_g_is_campmate(self.faction_id):
                                            target_id = hit_unit.id
                                            point = col_info[0]
                                            overlapped_col = True
                                            break

                                return overlapped_col or None
                    if is_trigger:
                        if ignore_expolosion(self._owner_id, target_id):
                            return
                    elif unit.ev_g_is_campmate(self.faction_id):
                        return
                    target_type = global_data.emgr.scene_find_unit_type_event.emit(cobj.cid)[0]
                    if self._check_pierce(unit, cobj.cid, point):
                        return
                    contact_info['target_type'] = target_type
            if self._intrp_time < self._intrp_duration:
                initial_position = math3d.vector(*self.throw_info['position'])
                self.set_model_end_pos(point)
                if (point - initial_position).length < self._col_obj.linear_velocity.length * 0.015:
                    self.hide_model()
            if self._col_obj:
                self.need_update = False
                self._col_obj.set_notify_contact(False)
                self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
            self.stop_post_contact_timer()
            explosive_info = (cobj, point, model, normal, target_id, self.throw_info)
            contact_info['explosive_info'] = explosive_info
            self._col_objs.append(contact_info)
            self.post_on_contact()
            return

    def post_on_contact(self):
        if self._is_explosive:
            return
        self._is_expolosive = True
        if global_data.cam_lctarget and global_data.cam_lctarget.id == self._owner_id:
            global_data.cam_lctarget.send_event('E_CLAW_TARGET', self._col_objs[0]['explosive_info'])
        super(ComClawGrenadeCollision, self).post_on_contact()