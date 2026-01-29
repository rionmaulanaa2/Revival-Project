# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBarrageCollision.py
from __future__ import absolute_import
from . import ComWeaponCollisionBase
import math3d
import collision
from logic.gcommon.common_const.weapon_const import WP_ARRAY_BARRAGE, WP_ROUND_BARRAGE, WP_COLUMN_BARRAGE, WP_SPHERE_BARRAGE
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.team_utils import ignore_expolosion
from logic.gcommon.common_const.collision_const import GROUP_AUTO_AIM
from logic.gcommon.common_const.weapon_const import THROWABLE_TRIGGER_COLLISION, THROWABLE_TRIGGER_ENTITY
from logic.gutils import barrage_utils
from math import sin, cos

class ComBarrageCollision(ComWeaponCollisionBase.ComWeaponCollisionBase):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'E_POSITION': '_on_position_changed',
       'S_DIRECTION': '_on_direction_changed',
       'G_POSITION': 'get_position'
       }
    UP_VECTOR = math3d.vector(0, 1, 0)

    def init_from_dict(self, unit, bdict):
        self.throw_info = {}
        self.throw_info.update(bdict)
        self.idx = self.throw_info.get('sub_idx', 0)
        self.item_type = self.throw_info['item_itype']
        self.item_kind = self.throw_info.get('item_kind', None)
        self._trigger_type = None
        self._target_logic = None
        self._is_col_enable = True
        self.conf = confmgr.get('grenade_config', str(self.item_type))
        self.params = {}
        self.sd.ref_col_obj = None
        self._left_time = 1000
        self._max_distance = 0.0
        self._restitution = 1
        self._gravity = None
        self._distance_for_gravity = 0
        self._impulse_power = 0
        self._impulse_range = 0
        self._col_objs = []
        self._col_ids = []
        self.update_col_ids(self.throw_info)
        self._owner_id = bdict['owner_id']
        self._original_pos = None
        self._last_check_pos = None
        self._ignore_fire_pos = False
        self.INIT_FUNC = {WP_ARRAY_BARRAGE: self.init_array,
           WP_ROUND_BARRAGE: self.init_round,
           WP_COLUMN_BARRAGE: self.init_colume,
           WP_SPHERE_BARRAGE: self.init_sphere
           }
        self.TICK_FUNC = {WP_ARRAY_BARRAGE: self.tick_array,
           WP_ROUND_BARRAGE: self.tick_round,
           WP_COLUMN_BARRAGE: self.tick_colume,
           WP_SPHERE_BARRAGE: self.tick_sphere
           }
        super(ComBarrageCollision, self).init_from_dict(unit, bdict)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_position_changed)
        return

    def update_col_ids(self, data):
        if data.get('trigger_id', None):
            trigger_id = data['trigger_id']
            target = EntityManager.getentity(trigger_id)
            self._target_logic = target.logic
            self._col_ids = self._target_logic.ev_g_human_col_id()
            shield_id = self._target_logic.share_data.ref_mecha_shield_col_id
            if shield_id:
                self._col_ids.append(shield_id)
            relative_ids = target.logic.share_data.ref_mecha_relative_cols
            if relative_ids:
                self._col_ids.extend(relative_ids)
        else:
            self._col_ids = []
        return

    def cache(self):
        self._is_col_enable = False
        super(ComBarrageCollision, self).cache()

    def on_model_load_complete(self, model):
        super(ComBarrageCollision, self).on_model_load_complete(model)
        if not self._col_obj or not self.is_enable():
            return
        cobj = self._col_obj
        self.need_update = True
        cobj.set_notify_contact(True)

    def _create_col_obj(self):
        if not self.is_enable():
            return
        else:
            self.sd.ref_col_obj = self._col_obj
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                col_type = collision.SPHERE
                radius = self.conf['fCollisionRadius']
                bounding_box = math3d.vector(radius, radius, radius)
                self._col_obj = collision.col_object(col_type, bounding_box, 0, 0, 1)
                self.sd.ref_col_obj = self._col_obj
                self.set_group_and_mask(self._col_obj)
                pos = self.throw_info['position']
                self._col_obj.position = pos
                self._original_pos = self._col_obj.position
                self._last_check_pos = self._original_pos
                if not self._ignore_fire_pos and self._target_logic and self._target_logic.sd.ref_is_mecha:
                    direction = self.throw_info['dir']
                    direction = math3d.vector(direction[0], direction[1], direction[2])
                    direction.is_zero or direction.normalize()
                    self._last_check_pos = self._original_pos - direction * 4.0 * NEOX_UNIT_SCALE
            self._col_obj.rotation_matrix = model.rotation_matrix
            self._col_obj.is_explodable = True
            self.scene.scene_col.add_object(self._col_obj)
            return

    def get_col_radius_rate(self):
        pass

    def init_physical_parameters(self):
        self.params = self.conf.get('cCustomParam', {})
        self._trigger_type = self.conf['iTriggerType']
        self._max_distance = self.conf['fMaxDistance']
        dir_data = self.throw_info.get('dir', (0, 0, 1))
        direction = math3d.vector(*dir_data)
        self._col_obj.mass = self.throw_info['mass']
        self._col_obj.disable_gravity(True)
        gravity = self.throw_info['gravity']
        if gravity > 0:
            self._gravity = math3d.vector(0, -gravity * self.throw_info['mass'] * 1.8, 0)
            self._distance_for_gravity = self.conf['DistanceForGravity']
            if self._distance_for_gravity == 0:
                self._col_obj.apply_force(self._gravity)
        self._col_obj.static_friction = self.conf['fStaticFriction']
        self._col_obj.dynamic_friction = self.conf['fDynamicFriction']
        self._col_obj.restitution = 1
        self._restitution = self.conf['fRestitution']
        self._col_obj.set_damping(self.conf['fLinearDamp'], self.conf['fLangularDamp'])
        speed = direction * self.throw_info['speed']
        self._col_obj.set_linear_velocity(speed)
        self.INIT_FUNC[self.item_kind](direction)

    def init_array(self, direction):
        self.t_array = self.params.get('t_array')
        self.ori_seq = barrage_utils.get_array_seq(self.t_array, self.idx)
        self.seq = barrage_utils.calc_array_seq(self.t_array, self.ori_seq)
        self.init_time = self.params.get('init_time')
        self.init_speed = self.params.get('init_speed')
        self.hold_time = self.params.get('hold_time', 0)
        self.spread_time = self.params.get('spread_time', 0)
        self.spread_speed = self.params.get('spread_speed', 0)
        self.spin_begin_time = self.params.get('spin_begin_time', 0)
        self.spin_time = self.params.get('spin_time', 0)
        self.spin_speed = self.params.get('spin_speed', 0)
        self.spin_spread_time = self.params.get('spin_spread_time', 0)
        self.spin_spread_speed = self.params.get('spin_spread_speed', 0)
        self.radian = barrage_utils.calc_array_radian(self.seq)
        self.radius = 0
        self.center = None
        self.forward = direction
        self.forward.normalize()
        self.right = self.UP_VECTOR.cross(self.forward)
        self.right.normalize()
        self.up = self.forward.cross(self.right)
        self.up.normalize()
        self.fly_time = 0
        self.dur_hold = self.init_time + self.hold_time
        self.dur_spread = self.dur_hold + self.spread_time
        self.dur_spin = self.spin_begin_time + self.spin_time
        self.dur_spin_spread = self.spin_begin_time + self.spin_spread_time
        return

    def tick_array(self, dt):
        self.fly_time += dt
        if self.fly_time < self.init_time:
            r, u, f = self.seq
            sr, su, sf = self.init_speed
            r_inc = self.right * sr * dt * r
            u_inc = self.up * su * dt * u
            f_inc = self.forward * sf * dt * f
            self._col_obj.position = self._col_obj.position + r_inc + u_inc + f_inc
            self.radius += (r_inc + u_inc).length
        elif self.fly_time < self.dur_hold:
            pass
        elif self.fly_time < self.dur_spread:
            r, u, f = self.seq
            sr, su, sf = self.spread_speed
            r_inc = self.right * sr * dt * r
            u_inc = self.up * su * dt * u
            f_inc = self.forward * sf * dt * f
            self._col_obj.position = self._col_obj.position + r_inc + u_inc + f_inc
            self.radius += (r_inc + u_inc).length
        if self.fly_time > self.spin_begin_time:
            self.center = self._col_obj.position - (self.right * cos(self.radian) + self.up * sin(self.radian)) * self.radius
            if self.fly_time < self.dur_spin_spread:
                self.radius += self.spin_spread_speed * dt * (abs(self.seq[0]) + abs(self.seq[1]))
            if self.fly_time < self.dur_spin:
                self.radian += self.spin_speed * dt
                self._col_obj.position = self.center + (self.right * cos(self.radian) + self.up * sin(self.radian)) * self.radius

    def init_round(self, direction):
        self.t_round = self.params.get('t_round')
        self.size, self.series = self.t_round[:2]
        self.seq = barrage_utils.calc_round_seq(self.t_round, self.idx)
        self.init_time = self.params.get('init_time')
        self.init_speed = self.params.get('init_speed')
        self.radian = barrage_utils.calc_round_radian(self.seq, self.series)
        self.radius = 0
        self.center = None
        self.hold_time = self.params.get('hold_time', 0)
        self.spread_time = self.params.get('spread_time', 0)
        self.spread_speed = self.params.get('spread_speed', 0)
        self.spin_begin_time = self.params.get('spin_begin_time', 0)
        self.spin_time = self.params.get('spin_time', 0)
        self.spin_speed = self.params.get('spin_speed', 0)
        self.spin_spread_time = self.params.get('spin_spread_time', 0)
        self.spin_spread_speed = self.params.get('spin_spread_speed', 0)
        self.forward = direction
        self.forward.normalize()
        self.right = self.UP_VECTOR.cross(self.forward)
        self.right.normalize()
        self.up = self.forward.cross(self.right)
        self.up.normalize()
        self.fly_time = 0
        self.dur_hold = self.init_time + self.hold_time
        self.dur_spread = self.dur_hold + self.spread_time
        self.dur_spin = self.spin_begin_time + self.spin_time
        self.dur_spin_spread = self.spin_begin_time + self.spin_spread_time
        return

    def tick_round(self, dt):
        self.fly_time += dt
        if self.fly_time < self.init_time:
            r, t, f = self.seq
            sr, sf = self.init_speed
            radius_inc = sr * dt * r
            self.radius += radius_inc
            f_inc = self.forward * sf * dt * f
            self._col_obj.position = self._col_obj.position + (self.right * cos(self.radian) + self.up * sin(self.radian)) * radius_inc + f_inc
        elif self.fly_time < self.dur_hold:
            pass
        elif self.fly_time < self.dur_spread:
            r, t, f = self.seq
            sr, sf = self.spread_speed
            radius_inc = sr * dt * r
            self.radius += radius_inc
            f_inc = self.forward * sf * dt * f
            self._col_obj.position = self._col_obj.position + (self.right * cos(self.radian) + self.up * sin(self.radian)) * radius_inc + f_inc
        if self.fly_time > self.spin_begin_time:
            self.center = self._col_obj.position - (self.right * cos(self.radian) + self.up * sin(self.radian)) * self.radius
            if self.fly_time < self.dur_spin_spread:
                self.radius += self.spin_spread_speed * dt * abs(self.seq[0])
            if self.fly_time < self.dur_spin:
                self.radian += self.spin_speed * dt
                self._col_obj.position = self.center + (self.right * cos(self.radian) + self.up * sin(self.radian)) * self.radius

    def init_colume(self, direction):
        self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
        self.t_colume = self.params.get('t_colume')
        self.scope, self.count = self.t_colume[:2]
        self.ori_seq = barrage_utils.get_colume_seq(self.t_colume, self.idx)
        self.seq = barrage_utils.calc_colume_seq(self.t_colume, self.ori_seq)
        self.z_gap = self.params.get('z_gap')
        self.ori_dir = direction
        self.fix_dir = math3d.vector(self.ori_dir.x, 0, self.ori_dir.z)
        self.radian = barrage_utils.calc_colume_radian(self.scope, self.count, self.seq)
        self.tar_dir = barrage_utils.calc_colume_dir(self.fix_dir, self.radian)
        self.tar_dir.normalize()
        self._col_obj.position += math3d.vector(0, self.z_gap[int(self.seq[1])], 0)
        speed = self.tar_dir * self.throw_info['speed']
        self._col_obj.set_linear_velocity(speed)

    def tick_colume(self, dt):
        pass

    def init_sphere(self, direction):
        self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
        self.t_sphere = self.params.get('t_sphere')
        self.t_theta, self.t_phi, self.series, self.size = self.t_sphere
        self.ori_seq = barrage_utils.get_sphere_seq(self.t_sphere, self.idx)
        self.seq = barrage_utils.calc_sphere_seq(self.t_sphere, self.ori_seq)
        self.forward = direction
        self.forward.normalize()
        self.right = self.UP_VECTOR.cross(self.forward)
        self.right.normalize()
        self.up = self.forward.cross(self.right)
        self.up.normalize()
        self.ori_dir = direction
        self.theta, self.phi = barrage_utils.calc_sphere_radian(self.t_sphere, self.seq)
        self.tar_dir = barrage_utils.calc_sphere_dir(self.ori_dir, self.right, self.up, self.theta, self.phi)
        self.tar_dir.normalize()
        speed = self.tar_dir * self.throw_info['speed']
        self._col_obj.set_linear_velocity(speed)

    def tick_sphere(self, dt):
        pass

    def tick(self, dt):
        if not self._col_obj:
            self.need_update = False
            return
        else:
            if not self._col_obj.valid:
                return
            if self._gravity:
                if self._distance_for_gravity == 0 or self._distance_for_gravity <= (self._col_obj.position - self._original_pos).length:
                    self._col_obj.apply_force(self._gravity)
            model = self._model() if self._model else None
            if not model or not model.valid:
                self.need_update = False
                return
            self._left_time -= dt
            if self._left_time <= 0:
                self.on_contact(None, model.position, self.UP_VECTOR)
            if self._max_distance and self._max_distance <= (self._col_obj.position - self._original_pos).length:
                self.on_contact(None, model.position, self.UP_VECTOR)
            self.TICK_FUNC[self.item_kind](dt)
            if self._need_ray_check:
                self.ray_check(self._col_obj.position)
            else:
                self._last_check_pos = self._col_obj.position
            if self._ignore_fire_pos:
                self.intrp_model_pos(dt)
            else:
                self.directly_set_model_pos()
            return

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            if not self._is_col_enable:
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
            if cobj:
                if cobj.cid in self._col_ids:
                    return
            is_trigger = self.is_trigger(cobj)
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                contact_info = {}
                target_id = None
                if cobj:
                    unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                    if unit:
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

                            return overlapped_col or None
                    if is_trigger:
                        if ignore_expolosion(self._owner_id, target_id):
                            return
                    elif unit.ev_g_is_campmate(self.faction_id):
                        return
                    target_type = global_data.emgr.scene_find_unit_type_event.emit(cobj.cid)[0]
                    contact_info['target_type'] = target_type
            self.complete_model_pos_interpolation()
            if self._col_obj:
                self.need_update = False
                self._col_obj.set_notify_contact(False)
            explosive_info = (cobj, point, model, normal, target_id, self.throw_info)
            contact_info['explosive_info'] = explosive_info
            self._col_objs.append(contact_info)
            self.post_on_contact()
            return

    def is_trigger(self, cobj):
        if cobj is None:
            return True
        else:
            if cobj.group == GROUP_AUTO_AIM:
                return False
            if self._trigger_type == THROWABLE_TRIGGER_COLLISION:
                return True
            global_data.game_mgr.post_exec(self.restitution)
            return False

    def post_on_contact(self):
        if not self._col_objs:
            return

        def get_target_type(elem):
            return elem.get('target_type', -1)

        self._col_objs.sort(key=get_target_type, reverse=True)
        self.update_explosive_info(*self._col_objs[0]['explosive_info'])
        self._col_objs = []

    def restitution(self):
        if self._col_obj:
            self._col_obj.set_linear_velocity(self._col_obj.linear_velocity * self._restitution)

    def destroy_col(self):
        if self.sd.ref_col_obj:
            self.sd.ref_col_obj = None
        super(ComBarrageCollision, self).destroy_col()
        return

    def destroy(self):
        if not self._is_valid:
            return
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._on_position_changed)
        super(ComBarrageCollision, self).destroy()

    def _on_position_changed--- This code section failed: ---

 595       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  '_col_obj'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    27  'to 27'

 596      12  LOAD_FAST             1  'position'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  '_col_obj'
          21  STORE_ATTR            2  'position'
          24  JUMP_FORWARD          0  'to 27'
        27_0  COME_FROM                '24'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def _on_direction_changed--- This code section failed: ---

 599       0  LOAD_GLOBAL           0  'isinstance'
           3  LOAD_FAST             1  'direction'
           6  LOAD_GLOBAL           1  'math3d'
           9  LOAD_ATTR             2  'matrix'
          12  CALL_FUNCTION_2       2 
          15  POP_JUMP_IF_TRUE     22  'to 22'

 601      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 602      22  LOAD_GLOBAL           3  'getattr'
          25  LOAD_GLOBAL           1  'math3d'
          28  CALL_FUNCTION_2       2 
          31  POP_JUMP_IF_FALSE    49  'to 49'

 603      34  LOAD_FAST             1  'direction'
          37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             4  '_col_obj'
          43  STORE_ATTR            5  'rotation_matrix'
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 28

    def get_position(self):
        if self._col_obj and self._col_obj.valid:
            return self._col_obj.position