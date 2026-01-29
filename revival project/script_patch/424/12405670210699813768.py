# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComOilBottleBulletCollision.py
from __future__ import absolute_import
from .ComGrenadeCollision import ComGrenadeCollision
from common.cfg import confmgr
from logic.gutils.scene_utils import is_break_obj
from logic.gutils import team_utils
from logic.vscene.parts.PartShootManager import SHOOT_OBJ_TYPE_FIELD_SHIELD
from logic.gcommon.const import NEOX_UNIT_SCALE
from math import pi
import math3d
from .ComObjCollision import ignore_lod_collisions

class ComOilBottleBulletCollision(ComGrenadeCollision):

    def init_from_dict(self, unit_obj, bdict):
        super(ComOilBottleBulletCollision, self).init_from_dict(unit_obj, bdict)
        info = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        self._bounce_cnt = 0
        self._max_bounces = info.get('bounces', -1)
        self._att_pitch = info.get('attenuation_pitch', 30)
        self._att_dist = info.get('attenuation_dist', 20)
        self._fire_cam_pitch = bdict.get('fire_cam_pitch', 0)
        self._first_contact_dis = bdict.get('first_contact_dis', 20)
        self._first_contact_dis /= NEOX_UNIT_SCALE

    def _create_col_obj(self):
        super(ComOilBottleBulletCollision, self)._create_col_obj()
        forward = math3d.vector(*self.throw_info['dir'])
        if not forward.is_zero:
            forward.normalize()
            right = math3d.vector(0, 1, 0).cross(forward) * 100
            self._col_obj.set_angular_velocity(math3d.vector(right.x, 0, right.z))

    def on_model_load_complete(self, unit):
        super(ComOilBottleBulletCollision, self).on_model_load_complete(unit)

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
            self._bounce_cnt += 1
            bounc_time_out = False
            if self._max_bounces > 0:
                bounc_time_out = self._bounce_cnt >= self._max_bounces
            if cobj:
                if cobj.cid in self._col_ids:
                    return
            global_data.sfx_mgr.create_sfx_in_scene('effect/fx/scenes/common/destroy/cuihui_03.sfx', point)
            self._distance_for_gravity = 0
            is_trigger = self.is_trigger(cobj)
            if not is_trigger and not is_break_obj(cobj.model_col_name) and not bounc_time_out:
                self.play_collisions_sound(point)
                return
            if self._model:
                model = self._model() if 1 else None
                return model or None
            self.complete_model_pos_interpolation()
            contact_info = {}
            target_id = None
            if cobj:
                unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                if unit:
                    target_id = unit.id
                    if unit.ev_g_is_campmate(self.faction_id) or unit.ev_g_is_campmate(self.faction_id):
                        self._bounce_cnt -= 1
                        return
                    if is_trigger:
                        if team_utils.ignore_expolosion(self._owner_id, target_id):
                            self._bounce_cnt -= 1
                            return
                    elif team_utils.is_teammate(self._owner_id, unit):
                        self._bounce_cnt -= 1
                        return
                    target_type = global_data.emgr.scene_find_unit_type_event.emit(cobj.cid)[0]
                    if self.is_pierced and target_type != SHOOT_OBJ_TYPE_FIELD_SHIELD:
                        self.send_harm_info(unit, cobj.cid, point)
                        return
                    contact_info['target_type'] = target_type
                else:
                    if self._col_obj.linear_velocity.length / NEOX_UNIT_SCALE > 3 and normal.pitch * 180 / pi > -30:
                        self._bounce_cnt -= 1
                        return
                    if self._bounce_cnt < self._max_bounces:
                        self.play_collisions_sound(point)
                        return
            if self._col_obj:
                self.need_update = False
                self._col_obj.set_notify_contact(False)
            self.stop_post_contact_timer()
            explosive_info = (
             cobj, point, model, normal, target_id, self.throw_info)
            contact_info['explosive_info'] = explosive_info
            self._col_objs.append(contact_info)
            self.post_on_contact()
            return

    def restitution(self):
        if self._col_obj:
            cur_velocity = self._col_obj.linear_velocity
            coe_pitch, coe_dist = (0.4, 0.6)
            if self._fire_cam_pitch > 30:
                coe_pitch *= (90.0 - self._att_pitch - (self._fire_cam_pitch - self._att_pitch)) / (90 - self._att_pitch)
                coe_pitch = max(coe_pitch, 0)
            if self._first_contact_dis < self._att_dist:
                coe_dist *= 1 - (15.0 - self._first_contact_dis) / self._att_dist
                coe_dist = max(coe_dist, 0)
            coe = coe_dist + coe_pitch
            coe *= self._restitution
            v_y = max(cur_velocity.y * coe, 3 * NEOX_UNIT_SCALE)
            cur_velocity = math3d.vector(cur_velocity.x * coe, v_y, cur_velocity.z * coe)
            self._col_obj.set_linear_velocity(cur_velocity)