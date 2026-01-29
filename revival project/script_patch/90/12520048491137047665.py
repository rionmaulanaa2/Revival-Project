# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRainGrenadeCollision.py
from __future__ import absolute_import
from logic.gutils.scene_utils import is_break_obj
from logic.gutils.team_utils import ignore_expolosion
from .ComGrenadeCollision import UP_VECTOR
from logic.gcommon.const import NEOX_UNIT_SCALE
from .ComGrenadeCollision import ComGrenadeCollision
from common.cfg import confmgr
import collision
import math3d
import random
import math
import time
HIDE_STAGE = 0
SHOW_STAGE = 1
SPREAD_STAGE = 2

class ComRainGrenadeCollision(ComGrenadeCollision):

    def init_from_dict(self, unit_obj, bdict):
        super(ComRainGrenadeCollision, self).init_from_dict(unit_obj, bdict)
        self.stage = HIDE_STAGE
        self._hide_left_time = 0.0
        self._spread_left_time = 0.0
        self._linear_velocity = None
        self._show_time = 0
        return

    def update_left_time(self, dt):
        self._left_time -= dt
        self._hide_left_time -= dt
        self._spread_left_time -= dt
        if self._hide_left_time <= 0.5 and self.stage == HIDE_STAGE:
            self.enter_show_stage()
        elif self._spread_left_time <= 0.5 and self.stage == SHOW_STAGE:
            self.enter_spread_stage()

    def on_model_load_complete(self, model):
        super(ComRainGrenadeCollision, self).on_model_load_complete(model)
        self._show_time = time.time() + self._hide_left_time - 0.5

    def init_physical_parameters(self):
        conf = self.throw_info
        cobj = self._col_obj
        item_type = str(self.item_type)
        item_conf = confmgr.get('grenade_config', item_type)
        self._spread_left_time = item_conf.get('cCustomParam', {}).get('spread_left_time', 1.5)
        self._left_time = item_conf['fTimeFly']
        parent_item_conf = confmgr.get('grenade_config', str(self.item_type - 1))
        self._hide_left_time = parent_item_conf.get('fTimeFly', 3)
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
            self._gravity = 0
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

    def on_contact(self, *args, **kwargs):
        is_show = time.time() - self._show_time >= 0.0
        if is_show and self.stage == HIDE_STAGE:
            self.enter_show_stage()
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

                            if not overlapped_col:
                                return
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
                if self._col_obj:
                    self.need_update = False
                    self._col_obj.set_notify_contact(False)
                if not is_show:
                    player = global_data.player
                    return player and player.logic or None
                uniq_key = self.throw_info['uniq_key']
                player.logic.send_event('E_CALL_SYNC_METHOD', 'destroy_explosive_item', ((uniq_key,),), True)
                self.throw_info['need_sync'] = False
                self.throw_info['ignore_bomb_sfx'] = True
            else:
                self.throw_info['need_sync'] = True
                self.throw_info['ignore_bomb_sfx'] = False
            self.stop_post_contact_timer()
            explosive_info = (cobj, point, model, normal, target_id, self.throw_info)
            contact_info['explosive_info'] = explosive_info
            self._col_objs.append(contact_info)
            self.post_on_contact()
            return

    def play_fly_sound(self, cobj):
        if self.stage == HIDE_STAGE:
            return
        super(ComRainGrenadeCollision, self).play_fly_sound(cobj)

    def enter_show_stage(self):
        self.stage = SHOW_STAGE
        self.play_fly_sound(self._col_obj)
        self.send_event('E_SHOW')
        item_conf = confmgr.get('grenade_config', str(self.item_type))
        division_range = item_conf.get('cCustomParam', {}).get('division_range', 100)
        cur_v = self._col_obj.linear_velocity
        cur_v.normalize()
        y_v = math3d.vector(0, 1, 0)
        right_v = cur_v.cross(y_v)
        right_v.normalize()
        up_v = cur_v.cross(right_v)
        up_v.normalize()
        mat = math3d.matrix.make_orient(cur_v, up_v)
        self._linear_velocity = self._col_obj.linear_velocity
        sub_idx = self.throw_info.get('sub_idx', 0)
        firearm_config = confmgr.get('firearm_config', str(self.item_type))
        pellets = firearm_config.get('iPellets', 1)
        if sub_idx > 0:
            rate = 1.0 * (sub_idx - 1) / (pellets - 1)
            self._col_obj.set_linear_velocity(self._col_obj.linear_velocity + y_v * math3d.matrix.make_rotation_z(2 * math.pi * rate) * mat * division_range)

    def enter_spread_stage(self):
        self.stage = SPREAD_STAGE
        if self._linear_velocity is not None:
            self._col_obj.set_linear_velocity(self._linear_velocity)
        return