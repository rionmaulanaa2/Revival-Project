# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWeaponCollisionBase.py
from __future__ import absolute_import
import six
from .ComObjCollision import ComObjCollision
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import time_utility as t_util
from logic.gcommon.common_const import collision_const, weapon_const, buff_const
from common.const.common_const import VEC3D_TEMP, VEC3D_UP, FORCE_DELTA_TIME, FORCE_DELTA_TIME_MS
import collision
import math3d
from logic.gcommon import const
from logic.gutils import team_utils
from logic.gutils.client_unit_tag_utils import register_unit_tag
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.buff_const import BEAT_BACK_BUFF_ID
from .ComObjCollision import ignore_lod_collisions
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils import game_mode_utils
from math import isnan
import world
COLLISION_MASK_SCENE_IGNORE_RADIUS = 1
COLLISION_MASK_UNIT_IGNORE_COLLISION = 2
WATER_SUFFACE_SFX = 'effect/fx/robot/common/water_zidan.sfx'
CHECK_MODEL_COL_SAME_DIR_COUNT = 2
ATTACHABLE_UNIT_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LMechaTrans',
                                               'LMotorcycle', 'LMonster', 'LSkillWall'))

class ComWeaponCollisionBase(ComObjCollision):

    def __init__(self):
        super(ComWeaponCollisionBase, self).__init__()
        self.collision_type_mask = 0
        self.item_type = None
        self._last_check_pos = None
        self._trigger_type = None
        self.pierced_targets = set()
        self.throw_info = {}
        self.has_attached = False
        self.raycheck_on_contact = None
        self._radius = 0.0
        self._need_ray_check = False
        self._ray_check_count = 0
        self._is_explosive = False
        self._intrp_time = 0.0
        self._intrp_duration = 1.0
        self._col_obj_last_pos = None
        self._check_model_col_same_dir_count = CHECK_MODEL_COL_SAME_DIR_COUNT
        self._contact_phantom = set()
        if global_data.low_fps_switch_on:
            self.intrp_model_pos = self._intrp_model_pos2
            self.directly_set_model_pos = self._directly_set_model_pos2
        else:
            self.intrp_model_pos = self._intrp_model_pos
            self.directly_set_model_pos = self._directly_set_model_pos
        return

    def init_from_dict(self, unit, bdict):
        self.throw_info.update(bdict)
        self.client_extra = self.throw_info.get('client_extra', {})
        self.faction_id = bdict.get('faction_id', 0)
        grenade_conf = confmgr.get('grenade_config', str(bdict['item_itype']))
        if grenade_conf:
            self._trigger_type = grenade_conf['iTriggerType']
            self._radius = grenade_conf['fCollisionRadius']
            self._gravity = grenade_conf.get('fGravity', 0)
        self._intrp_time = 0.0
        self._intrp_duration = 1.0
        self._col_obj_last_pos = None
        self._check_model_col_same_dir_count = CHECK_MODEL_COL_SAME_DIR_COUNT
        super(ComWeaponCollisionBase, self).init_from_dict(unit, bdict)
        return

    def cache(self):
        super(ComWeaponCollisionBase, self).cache()
        self.collision_type_mask = 0
        self.item_type = None
        self._last_check_pos = None
        self._trigger_type = None
        self.pierced_targets = set()
        self.throw_info = {}
        self.has_attached = False
        self._is_explosive = False
        self._need_ray_check = False
        self._contact_phantom = set()
        return

    def on_model_load_complete(self, model):
        super(ComWeaponCollisionBase, self).on_model_load_complete(model)
        if not self._col_obj or not self.is_enable():
            return
        self.need_update = True
        self.init_physical_parameters()
        cobj = self._col_obj
        if self._trigger_type == weapon_const.THROWABLE_TRIGGER_ATTACH:
            cobj.set_contact_callback(self.on_contact_by_attach_throwable)
            self.raycheck_on_contact = self.on_contact_by_attach_throwable
        else:
            cobj.set_contact_callback(self.on_contact_by_other)
            self.raycheck_on_contact = self.on_contact_by_other
        self._col_obj_last_pos = cobj.position

    def init_physical_parameters(self):
        log_error('err init_physical_parameters not exist')

    def on_contact_by_other(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            cobj = None
            point = None
            if len(args) == 3:
                cobj, point, normal = args
            else:
                my_obj, cobj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            if cobj and cobj.group == collision_const.WATER_GROUP:
                if point:
                    global_data.game_mgr.post_exec(lambda : global_data.sfx_mgr.create_sfx_in_scene(WATER_SUFFACE_SFX, point, int_check_type=CREATE_SRC_SIMPLE))
                    return
            if cobj and cobj.cid in global_data.phantoms:
                self.do_hit_phantom(cobj)
                return
            self.on_contact(*args, **kwargs)
            return

    def _on_grenade_attached(self, bullet_model=None, hit_point=None, attach_unit=None):
        if self._col_obj and not self.has_attached:
            self.has_attached = True
            if bullet_model and hit_point:
                bullet_model.position = hit_point
                bullet_model.rotation_matrix = self._col_obj.rotation_matrix
            self.need_update = False
            self._col_obj.set_notify_contact(False)
            self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
            self.send_event('E_ON_PLAY_HIT_SFX', attach_unit)

    def on_contact_by_attach_throwable(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
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
            if cobj and cobj.group == collision_const.WATER_GROUP:
                if point:
                    global_data.game_mgr.post_exec(lambda : global_data.sfx_mgr.create_sfx_in_scene(WATER_SUFFACE_SFX, point, int_check_type=CREATE_SRC_SIMPLE))
                return
            if cobj and cobj.cid in global_data.phantoms:
                self.do_hit_phantom(cobj)
                return
            if not kwargs.get('ray_check', False):
                check_hit_cobj, check_hit_point, check_hit_normal = self.through_wall_check(point)
                if check_hit_point:
                    cobj, point, normal = check_hit_cobj, check_hit_point, check_hit_normal
            if self._model:
                model = self._model() if 1 else None
                if not model or not model.valid:
                    return
                if cobj and cobj.cid in self._col_ids:
                    return
            mecha_entity = None
            uniq_key = self.throw_info['uniq_key']
            attach_type = weapon_const.THROWABLE_ATTACH_SCENE
            attach_info = {}
            velocity = self._col_obj.linear_velocity
            mrot = model.rotation_matrix.forward
            attach_info['rot_euler'] = (mrot.x, mrot.y, mrot.z)
            attach_info['normal'] = (normal.x, normal.y, normal.z)
            unit_objs = global_data.emgr.scene_find_unit_event.emit(cobj.cid)
            item_conf = confmgr.get('grenade_config', str(self.item_type))
            if unit_objs and unit_objs[0]:
                unit_obj = unit_objs[0] if 1 else None
                if unit_obj:
                    owner_id = self.throw_info['owner_id']
                    if unit_obj.ev_g_is_campmate(self.faction_id):
                        return
                    if team_utils.ignore_expolosion(owner_id, unit_obj.id):
                        return
                    attach_info['id_attached'] = unit_obj.id
                    if unit_obj.MASK & ATTACHABLE_UNIT_TAG_VALUE:
                        mecha_pos = unit_obj.ev_g_position()
                        if mecha_pos:
                            attach_type = weapon_const.THROWABLE_ATTACH_TARGET
                            mecha_model = unit_obj.ev_g_model()
                            if mecha_model:
                                sock_mat = mecha_model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
                                if sock_mat:
                                    offset = sock_mat.translation - mecha_pos
                                else:
                                    offset = math3d.vector(0, mecha_model.bounding_box.y, 0) - mecha_pos
                            else:
                                offset = point - mecha_pos
                            attach_info['offset'] = (
                             offset.x, offset.y, offset.z)
                            if item_conf and item_conf['iDifferentPartDamage'] and mecha_model:
                                explode_target_data = global_data.emgr.scene_explode_event.emit(point, game_mode_utils.get_custom_param_by_mode(item_conf, 'fRange') * NEOX_UNIT_SCALE, mrot)
                                if explode_target_data and explode_target_data[0]:
                                    is_right = (point - mecha_pos).cross(mecha_model.rotation_matrix.forward).y < 0
                                    for part_info in six.itervalues(explode_target_data[0]):
                                        part_info['is_right'] = is_right

                                    attach_info['extra_info'] = explode_target_data[0]
                hit_point = point
                if self._last_check_pos:
                    direction = point - self._last_check_pos
                    point = direction.is_zero or point - direction * 0.2
            attach_info['position'] = (
             point.x, point.y, point.z)
            player = global_data.player
            if player and player.logic:
                if cobj:
                    attach_info['cobj_group'] = cobj.group
                    attach_info['cobj_mask'] = cobj.mask
                    attach_info['impulse_range'] = self._impulse_range
                    attach_info['impulse_power'] = self._impulse_power
                    attach_info['normal'] = (normal.x, normal.y, normal.z)
                    attach_info['model_col_name'] = cobj.model_col_name
                player.logic.send_event('E_CALL_SYNC_METHOD', 'attach_explosive_item', (uniq_key, attach_type, attach_info))
            self._on_grenade_attached(model, hit_point, unit_obj)
            self.check_collision_camera_effect(attach_info.get('id_attached', False))
            return

    def set_group_and_mask(self, obj):
        obj.group = collision_const.GROUP_GRENADE
        obj.mask = collision_const.GROUP_CAN_SHOOT | collision_const.GROUP_SHIELD | collision_const.WATER_GROUP
        if self.collision_type_mask & COLLISION_MASK_UNIT_IGNORE_COLLISION:
            obj.ignore_collision = True

    def do_hit_phantom(self, cobj):
        if cobj in self._contact_phantom:
            return
        if not global_data.player or not global_data.player.logic:
            return
        unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
        if unit:
            camp_id = unit.sd.ref_camp_id
            atk_id = self.throw_info.get('owner_id')
            if atk_id and global_data.battle:
                atk_entity = global_data.battle.get_entity(atk_id)
                if not atk_entity or not atk_entity.logic or not atk_entity.logic.ev_g_is_campmate(camp_id):
                    is_avatar = global_data.mecha and atk_id == global_data.mecha.id or global_data.player and atk_id == global_data.player.id
                    unit.send_event('E_CALL_SYNC_METHOD', 'on_hit_phantom', (atk_id, is_avatar))
            self._contact_phantom.add(cobj)

    def update_explosive_info(self, cobj, point, model, normal, target, throw_info, aff_list=None):
        if not model or not model.valid:
            return
        else:
            player = global_data.player
            if not player or not player.logic:
                return
            if self._is_explosive:
                return
            self._is_explosive = True
            player_id = player.id
            mecha_id = global_data.mecha.id if global_data.mecha else None
            trigger_id = throw_info['trigger_id']
            if self.throw_info.get('call_sync_id', None) == global_data.battle_idx:
                need_sync = True
            elif target and (target == player_id or target == mecha_id):
                need_sync = True
            elif trigger_id == player_id or trigger_id == mecha_id:
                need_sync = True
            else:
                need_sync = False
            if self.throw_info.get('need_sync') is False:
                need_sync = False
            forward = model.rotation_matrix.forward
            upload_data = {'pos': (
                     point.x, point.y, point.z),
               'up': (
                    normal.x, normal.y, normal.z),
               'forward': (
                         forward.x, forward.y, forward.z)
               }
            harm_config = confmgr.get('break_data', str(self.item_type), default={})
            impulse_range = harm_config.get('fBreakRange', 0) * NEOX_UNIT_SCALE
            if harm_config:
                impulse_power = harm_config.get('cBreakPower', 0) if 1 else 0
                item_conf = confmgr.get('grenade_config', str(self.item_type))
                if target:
                    upload_data['target'] = target
                ignore_bomb_sfx = throw_info.get('ignore_bomb_sfx', False)
                if not ignore_bomb_sfx:
                    ignore_bomb_sfx = item_conf.get('cCustomParam', {}).get('no_target_no_sfx', False) and not target
                if ignore_bomb_sfx:
                    upload_data['ignore_bomb_sfx'] = True
                if cobj and cobj.__class__.__name__ == 'rigid_body':
                    upload_data['is_ragdoll_part'] = True
                else:
                    upload_data['is_ragdoll_part'] = False
                if need_sync:
                    upload_data['col_pos'] = upload_data['pos']
                    if aff_list:
                        upload_data['aff_list'] = aff_list
                    if throw_info.get('rise_building', None) is not None:
                        upload_data['rise_building'] = throw_info.get('rise_building')
                    buff_datas = None
                    iBuffAdd = item_conf.get('iBuffAdd')
                    if iBuffAdd and BEAT_BACK_BUFF_ID in iBuffAdd:
                        trigger = EntityManager.getentity(trigger_id)
                        if trigger:
                            trigger_pos = trigger.logic.ev_g_position()
                            buff_datas = {BEAT_BACK_BUFF_ID: {'pos': [trigger_pos.x, trigger_pos.y, trigger_pos.z]}}
                if buff_datas:
                    upload_data['buff_datas'] = buff_datas
                if item_conf:
                    if item_conf['iDifferentPartDamage']:
                        explode_target_data = global_data.emgr.scene_explode_event.emit(point, game_mode_utils.get_custom_param_by_mode(item_conf, 'fRange') * NEOX_UNIT_SCALE, forward)
                        if explode_target_data:
                            upload_data['extra_info'] = explode_target_data[0]
                    fExplosionOffset = item_conf.get('fExplosionOffset', 0) or 1.0
                    real_pos = point + normal * fExplosionOffset
                    upload_data['pos'] = (real_pos.x, real_pos.y, real_pos.z)
                if cobj:
                    upload_data['cobj_group'] = cobj.group
                    upload_data['cobj_mask'] = cobj.mask
                    upload_data['impulse_range'] = impulse_range
                    upload_data['impulse_power'] = impulse_power
                    upload_data['normal'] = (normal.x, normal.y, normal.z)
                    upload_data['model_col_name'] = cobj.model_col_name
                if 'is_in_death_door' in throw_info:
                    upload_data['is_in_death_door'] = throw_info['is_in_death_door']
                explosive_items = {throw_info['uniq_key']: upload_data}
                player.logic.send_event('E_CALL_SYNC_METHOD', 'update_explosive_item_info', (explosive_items,))
            explosive_item = throw_info
            explosive_item['position'] = upload_data['pos']
            explosive_item['up'] = upload_data['up']
            explosive_item['forward'] = upload_data['forward']
            explosive_item['explose_time'] = t_util.time()
            explosive_item['hit_target_id'] = upload_data.get('target', None)
            explosive_item['ignore_bomb_sfx'] = upload_data.get('ignore_bomb_sfx', False)
            explosive_item['target'] = upload_data.get('target', None)
            explosive_item['dummy_reason'] = upload_data.get('dummy_reason', None)
            if cobj:
                explosive_item['cobj_group'] = cobj.group
                explosive_item['cobj_mask'] = cobj.mask
                explosive_item['impulse_range'] = impulse_range
                explosive_item['impulse_power'] = impulse_power
                explosive_item['normal'] = (normal.x, normal.y, normal.z)
                explosive_item['model_col_name'] = cobj.model_col_name
                explosive_item['is_ragdoll_part'] = upload_data['is_ragdoll_part']
            global_data.game_mgr.post_exec(global_data.emgr.scene_throw_item_explosion_event.emit, {explosive_item['uniq_key']: {'item': explosive_item}})
            return

    def send_harm_info(self, unit, cid, point, different_part_damage=True, buff_datas=None):
        if unit.id in self.pierced_targets:
            return False
        pierced_info = {'target': unit.id,'uniq_key': self.throw_info['uniq_key']}
        if point:
            pierced_info['position'] = (
             point.x, point.y, point.z)
        if different_part_damage:
            part = {'part': const.HIT_PART_BODY,'off': (0, 0, 0)}
            if unit.sd.ref_is_mecha or unit.sd.ref_is_pve_monster:
                model = unit.ev_g_model()
                if model:
                    part = global_data.emgr.scene_get_mecha_explode_part.emit(cid, point)[0]
            pierced_info['part'] = part
        if buff_datas:
            pierced_info['buff_datas'] = buff_datas
        player = global_data.player
        if player and player.logic:
            player.logic.send_event('E_CALL_SYNC_METHOD', 'update_multi_calc_explosive', (pierced_info,))
        self.pierced_targets.add(unit.id)
        return True

    def collision_check(self, cobj_in, point_in, normal_in, **kwargs):
        is_ignore = False
        cobj = cobj_in
        point = point_in
        normal = normal_in
        if cobj and cobj.cid in self.client_extra.get('ignore_cobj_ids', []):
            return (True, cobj, point, normal)
        if cobj and self.client_extra.get('ignore_unit_ids', []):
            unit_obj = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
            if unit_obj and unit_obj.id in self.client_extra.get('ignore_unit_ids', []):
                return (True, cobj, point, normal)
        if cobj and cobj.cid in global_data.war_ignored_shoot_col:
            return (True, cobj, point, normal)
        is_ray_check_result = kwargs.get('ray_check', False)
        if not is_ray_check_result:
            cobj_temp, point_temp, normal_temp = self.through_wall_check(point)
            if point_temp:
                cobj, point, normal = cobj_temp, point_temp, normal_temp
            if self.check_ignore_scene_collision(cobj):
                is_ignore = True
        if not is_ignore and cobj and ignore_lod_collisions(cobj):
            is_ignore = True
        return (
         is_ignore, cobj, point, normal)

    def through_wall_check(self, hit_pos):
        check_group = collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP
        if self.collision_type_mask:
            result = self.scene.scene_col.hit_by_ray(self._last_check_pos, hit_pos, 0, check_group, check_group, collision.INCLUDE_FILTER, True)
            direction = hit_pos - self._last_check_pos
            if result[0]:
                for cobj in result[1]:
                    col_obj = cobj[4]
                    if col_obj.group == collision_const.REGION_BOUNDARY_SCENE_GROUP and col_obj.mask == collision_const.REGION_BOUNDARY_SCENE_MASK:
                        continue
                    if col_obj.cid in global_data.war_ignored_shoot_col:
                        continue
                    if col_obj.group != collision_const.WATER_GROUP:
                        if not direction.is_zero:
                            direction.normalize()
                        return (col_obj, cobj[0] - direction * 1, cobj[1])

        return (None, None, None)

    def check_ignore_scene_collision(self, hit_cobj):
        if not hit_cobj:
            return False
        group = hit_cobj.group
        position = self._col_obj.position
        if self.collision_type_mask & COLLISION_MASK_SCENE_IGNORE_RADIUS and group & collision_const.GROUP_STATIC_SHOOTUNIT and not group & collision_const.GROUP_DYNAMIC_SHOOTUNIT and self._last_check_pos:
            velocity = position - self._last_check_pos
            velocity_value = velocity.length
            if velocity_value <= 0.001:
                return True
            velocity.normalize()
            result = self.scene.scene_col.hit_by_ray(self._last_check_pos, position + velocity * 500, 0, collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP, collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP, collision.INCLUDE_FILTER, False)
            if result[0]:
                point = result[1]
                dist = (point - position).length
                count_off = 4 if self._gravity < 90 else 6
                ray_check_count = int(dist / velocity_value) + count_off
                self._ray_check_count = ray_check_count | 1
                self._need_ray_check = True
            return True
        return False

    def ray_check(self, cur_pos):
        if self._last_check_pos and self._last_check_pos != cur_pos and self._ray_check_count & 1:
            result = self.scene.scene_col.hit_by_ray(self._last_check_pos, cur_pos, 0, collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP, collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP, collision.INCLUDE_FILTER, False)
            if result[0]:
                direction = cur_pos - self._last_check_pos
                direction.normalize()
                self.raycheck_on_contact(result[5], result[1] - direction * 1, result[2], ray_check=True)
            self._ray_check_count -= 1
            if self._ray_check_count <= 0:
                self._need_ray_check = False
            self._last_check_pos = cur_pos
        else:
            self._ray_check_count -= 1

    def on_contact(self, *args):
        log_error('err on_contact not exist')

    def complete_model_pos_interpolation(self):
        self._intrp_time = self._intrp_duration
        self.intrp_model_pos(self._intrp_time)

    def set_model_end_pos(self, pos):
        self._intrp_time = self._intrp_duration
        m = self._model_cache
        if m and m.valid:
            m.position = pos

    def hide_model(self):
        m = self._model_cache
        if m and m.valid:
            m.visible = False

    @staticmethod
    def _check_nan_vec3(pos):
        return isnan(pos.x) or isnan(pos.y) or isnan(pos.z)

    def _intrp_model_pos(self, dt, rotation_matrix=None, auto_intrp_rot=False, try_stop_intrp_in_advance=True):
        self._intrp_time += dt
        m = self._model_cache
        if m and m.valid:
            if self._intrp_time < self._intrp_duration:
                VEC3D_TEMP.intrp(m.position, self._col_obj.position, self._intrp_time / self._intrp_duration)
                if try_stop_intrp_in_advance:
                    col_fly_dir = self._col_obj.position - self._col_obj_last_pos
                    if not col_fly_dir.is_zero:
                        col_fly_dir.normalize()
                        model_fly_dir = VEC3D_TEMP - m.position
                        model_fly_dir.is_zero or model_fly_dir.normalize()
                    if model_fly_dir.dot(col_fly_dir) >= 0.9999999:
                        self._check_model_col_same_dir_count -= 1
                        if self._check_model_col_same_dir_count == 0:
                            self._intrp_time = self._intrp_duration
                    else:
                        self._check_model_col_same_dir_count = CHECK_MODEL_COL_SAME_DIR_COUNT
            m.position = VEC3D_TEMP
        else:
            m.position = self._col_obj.position
        if auto_intrp_rot:
            if rotation_matrix is not None:
                rotation_matrix = rotation_matrix if 1 else self._col_obj.rotation_matrix
                new_dir = self._col_obj.position - self._col_obj_last_pos
                if not new_dir.is_zero and not self._check_nan_vec3(new_dir):
                    new_dir.normalize()
                    if not self._check_nan_vec3(new_dir) and not abs(new_dir.y) == 1.0:
                        rotation_matrix = math3d.matrix.make_orient(new_dir, VEC3D_UP)
                m.rotation_matrix = rotation_matrix
            self._col_obj_last_pos = self._col_obj.position
        else:
            self._model_cache = None
        return

    def _intrp_model_pos2(self, dt, rotation_matrix=None, auto_intrp_rot=False, try_stop_intrp_in_advance=True):
        self._intrp_time += dt
        m = self._model_cache
        if m and m.valid:
            if self._intrp_time < self._intrp_duration:
                VEC3D_TEMP.intrp(m.position, self._col_obj.position, (self._intrp_time + FORCE_DELTA_TIME) / self._intrp_duration)
                m.move_to_in_time(VEC3D_TEMP, FORCE_DELTA_TIME_MS, None, None, None, auto_intrp_rot)
            else:
                m.move_to_in_time(self._col_obj.position, FORCE_DELTA_TIME_MS, None, None, None, auto_intrp_rot)
        else:
            self._model_cache = None
        return

    def _directly_set_model_pos(self):
        m = self._model_cache
        if m and m.valid:
            m.position = self._col_obj.position
        else:
            self._model_cache = None
        return

    def _directly_set_model_pos2(self):
        m = self._model_cache
        if m and m.valid:
            m.move_to_in_time(self._col_obj.position, FORCE_DELTA_TIME_MS, None, None, None, False)
        else:
            self._model_cache = None
        return

    def check_collision_camera_effect(self, has_hit):
        from logic.gutils.scene_utils import get_camera_effect_scale
        if not has_hit or not global_data.cam_lctarget or not self._col_obj:
            return
        else:
            item_itype = self.item_type
            trigger_id = self.throw_info.get('trigger_id', None)
            is_ctraget = global_data.cam_lctarget.id == trigger_id
            trk_tag = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig', 'Content', str(item_itype), 'collision_hit_trk_tag', default='')
            if trk_tag:
                if is_ctraget:
                    player_position = global_data.cam_lctarget.ev_g_position()
                    scale = get_camera_effect_scale(self._col_obj.position, player_position)
                    global_data.cam_lctarget.send_event('E_PLAY_CAMERA_TRK', trk_tag, None, {'rot_mul': scale})
            return