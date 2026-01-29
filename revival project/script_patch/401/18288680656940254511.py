# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComClusterGrenadeCollision.py
from __future__ import absolute_import
import time
import math3d
from math import pi, sin, cos, tan, radians, degrees
from common.cfg import confmgr
from logic.gutils.scene_utils import is_break_obj
from logic.gutils.team_utils import ignore_expolosion
from .ComGrenadeCollision import ComGrenadeCollision, UP_VECTOR
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.mecha_const import SELF_DESTRUCT
import collision
HIDE_STAGE = 0
SHOW_STAGE = 1

class ComClusterGrenadeCollision(ComGrenadeCollision):

    def init_from_dict(self, unit_obj, bdict):
        super(ComClusterGrenadeCollision, self).init_from_dict(unit_obj, bdict)
        self.stage = HIDE_STAGE
        self.first_hit_obj = None
        self.can_explode_ts = 0
        self._split_sound_id = None
        return

    def init_physical_parameters(self):
        conf = self.throw_info
        cobj = self._col_obj
        item_type = self.item_type
        if self.stage == HIDE_STAGE:
            item_type -= 1
        item_type = str(item_type)
        item_conf = confmgr.get('grenade_config', item_type)
        if self.stage == HIDE_STAGE:
            self._left_time = item_conf.get('fTimeFly', 2.0)
        else:
            self._left_time = item_conf.get('cCustomParam', {}).get('sec_fly_time', 1.5)
        self._trigger_type = item_conf['iTriggerType']
        self._sink_speed = item_conf['fSinkSpeed']
        self._max_distance = item_conf['fMaxDistance']
        self._max_height = item_conf.get('bMaxHeight', 0)
        harm_config = confmgr.get('break_data', item_type, default={})
        self._impulse_power = harm_config.get('cBreakPower', 0) if harm_config else 0
        self._impulse_range = harm_config.get('fBreakRange', 0) * NEOX_UNIT_SCALE
        dir_data = conf.get('dir', (0, 0, 1))
        direction = math3d.vector(*dir_data)
        throw_speed_add_rate = conf.get('throw_speed_add_rate', 0)
        throw_speed_add_rate = throw_speed_add_rate if throw_speed_add_rate else 0
        speed_factor = 1 + throw_speed_add_rate
        speed = direction * item_conf['fSpeed'] * speed_factor
        cobj.mass = item_conf['fMass']
        gravity = item_conf['fGravity']
        cobj.disable_gravity(True)
        if gravity <= 0:
            cobj.disable_gravity(True)
            self._gravity = None
        else:
            self._gravity = math3d.vector(0, -gravity * item_conf['fMass'] * 1.8, 0)
            self._distance_for_gravity = item_conf['DistanceForGravity']
            if self._distance_for_gravity == 0:
                cobj.apply_force(self._gravity)
        cobj.static_friction = item_conf['fStaticFriction']
        cobj.dynamic_friction = item_conf['fDynamicFriction']
        cobj.restitution = 1
        cobj.enable_ccd = True
        self._restitution = item_conf['fRestitution']
        custom_param = item_conf.get('cCustomParam', {})
        self.is_pierced = custom_param.get('pierced', 0)
        self._col_obj.set_damping(item_conf['fLinearDamp'], item_conf['fLangularDamp'])
        cobj.set_linear_velocity(speed)
        special_sfx_path_list = confmgr.get('break_data', item_type, default={}).get('cBreakBulletHit')
        if special_sfx_path_list:
            cobj.enable_ccd = True
        return

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
                    col_is_pierced = unit.ev_g_is_pierced()
                    if self.is_pierced and (col_is_pierced is None or col_is_pierced is True):
                        self.send_harm_info(unit, cobj.cid, point)
                        self.complete_model_pos_interpolation()
                        return
                    contact_info['target_type'] = target_type
            self.complete_model_pos_interpolation()
            if self.stage == HIDE_STAGE:
                self.first_hit_target_id = target_id
                self.enter_show_stage(normal if target_id is None else math3d.vector(0, 1, 0))
            elif self._left_time <= 0.0 or time.time() >= self.can_explode_ts and target_id != self.first_hit_target_id:
                if self._col_obj:
                    self.need_update = False
                    self._col_obj.set_notify_contact(False)
                self.stop_post_contact_timer()
                explosive_info = (cobj, point, model, normal, target_id, self.throw_info)
                contact_info['explosive_info'] = explosive_info
                self._col_objs.append(contact_info)
                self.post_on_contact()
            return

    def play_fly_sound(self, cobj):
        if self.stage == HIDE_STAGE:
            return
        super(ComClusterGrenadeCollision, self).play_fly_sound(cobj)

    def play_split_sound(self, cobj):
        split_sound = confmgr.get('grenade_res_config', str(self.item_type), 'cCustomParam', 'split_sound', default='')
        if not split_sound:
            return
        self._split_sound_id = global_data.sound_mgr.post_event(split_sound, self._gernade_id, cobj.position)

    def enter_show_stage(self, hit_plane_normal):
        self.stage = SHOW_STAGE
        sub_idx = self.throw_info.get('sub_idx', 0)
        firearm_config = confmgr.get('firearm_config', str(self.item_type))
        pellets = firearm_config.get('iPellets', 1)
        custom_param = confmgr.get('grenade_config', str(self.item_type), 'cCustomParam', default={})
        direction = math3d.vector(0, 0, 1)
        if 'up_angle' in custom_param:
            up_angle = radians(custom_param['up_angle'])
            yaw = pi * 2.0 * sub_idx / pellets
            ua_sin = sin(up_angle)
            direction = math3d.vector(sin(yaw) * cos(up_angle), ua_sin, cos(yaw) * ua_sin)
            direction.normalize()
        elif 'split_angle' in custom_param:
            move_dir = self._col_obj.position - self._last_check_pos
            if not move_dir.is_zero:
                move_dir.normalize()
                new_move_dir = move_dir + hit_plane_normal * abs(move_dir.dot(hit_plane_normal)) * 2.0
                new_move_dir.normalize()
                right = new_move_dir.cross(hit_plane_normal)
                if right.is_zero:
                    right = math3d.vector(1, 0, 0)
                up = right.cross(new_move_dir)
                roll = pi * 2.0 * sub_idx / pellets
                split = right * cos(roll) + up * sin(roll)
                split.normalize()
                split *= tan(radians(custom_param['split_angle']))
                direction = new_move_dir + split
                direction.normalize()
        self.can_explode_ts = custom_param.get('can_explode_time', 0.0) + time.time()
        self.throw_info['dir'] = (direction.x, direction.y, direction.z)
        self.init_physical_parameters()
        if sub_idx == 0:
            self.play_split_sound(self._col_obj)
        self.play_fly_sound(self._col_obj)
        self.send_event('E_SHOW')

    def _stop_sound(self):
        super(ComClusterGrenadeCollision, self)._stop_sound()
        if self._split_sound_id:
            global_data.sound_mgr.stop_playing_id(self._split_sound_id)
            self._split_sound_id = None
        return