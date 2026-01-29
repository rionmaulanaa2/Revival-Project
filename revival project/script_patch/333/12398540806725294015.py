# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartBreakableManager.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import math
import random
import time
import weakref
import math3d
from . import ScenePart
import world
from common.cfg import confmgr
import common.utils.timer
from data.constant_break_data import data as constant_break_list
from logic.gcommon.common_const import collision_const, scene_const, battle_const
from logic.gcommon.common_const.collision_const import GLASS_GROUP, METAL_GROUP, STONE_GROUP, TERRAIN_GROUP, WOOD_GROUP
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.scene_utils import get_break_info_by_full_name, is_break_model, recycle_affiliate_break_models, enable_dynamic_physics, active_breakable, get_dynamic_physics_cids
from common.utils.sfxmgr import CREATE_SRC_SIMPLE

class PartBreakableManager(ScenePart.ScenePart):
    MAX_BREAK_MODEL_TIME = 10
    FALLDOWN_TIME = 1
    RAGDOLL_PART_IMPACT_RANGE = 3.0 * NEOX_UNIT_SCALE
    RAGDOLL_PART_DESTROY_RATIO = 0.6
    RAGDOLL_BREAK_SFX = 'effect/fx/scenes/common/destroy/billborad_hit_end.sfx'
    break_sound_name_map = {scene_const.MTL_METAL: 'iron_hit',
       scene_const.MTL_WOOD: 'wood_hit',
       scene_const.MTL_STONE: 'stone_hit'
       }
    INIT_EVENT = {'scene_add_break_objs': 'handle_break_objs',
       'scene_handle_break_ragdoll_part': 'handle_break_ragdoll_part',
       'scene_add_dynamic_box': 'add_dynamic_box',
       'scene_del_dynamic_box': 'del_dynamic_box'
       }

    def __init__(self, scene, name):
        super(PartBreakableManager, self).__init__(scene, name, need_update=True)
        self.loaded_break_models = {}
        self.dynamic_box_info = {}
        self.break_model_triggerd_ragdoll_part = {}
        self.break_origin_name_map = {}
        self.ragdoll_collision_sfx = constant_break_list.get(1, {}).get('cResSoot', None)
        return

    def add_dynamic_box(self, eid, model_name, box_npc):
        self.dynamic_box_info[model_name] = weakref.ref(box_npc)

    def del_dynamic_box(self, eid, model_name):
        self.dynamic_box_info.pop(model_name, None)
        return

    def get_dynamic_box(self, model_name):
        return self.dynamic_box_info.get(model_name, None)

    def _process_dynamic_box(self, model_name, center, impulse_factor):
        box = self.get_dynamic_box(model_name)
        if not box:
            return
        if box() and box().logic:
            box().logic.send_event('E_BOOM_IMPULSE', center, impulse_factor)

    def get_origin_model_name(self, break_name):
        return self.break_origin_name_map.get(break_name, None)

    def _apply_impulse_break(self, break_model, break_obj_type, impulse_force, point, is_ragdoll_part):
        if not (break_model and break_model.valid):
            return
        if global_data.game_mode and global_data.game_mode.is_pve() or break_obj_type not in (
         collision_const.BREAK_OBJ_TYPE_BUILDING,
         collision_const.BREAK_OBJ_TYPE_HP_BOX,
         collision_const.BREAK_OBJ_TYPE_HP_STATIC):
            rotate_radian = 0.5 * math.pi * random.uniform(-1, 1)
            rotate_mat = math3d.matrix.make_rotation_y(rotate_radian)
            impulse_force_unit = math3d.vector(impulse_force.x, 0, impulse_force.z)
            rand_impulse = math3d.vector(0, 0, 0)
            if not impulse_force_unit.is_zero:
                impulse_force_unit.normalize()
                scalar = 0.25 * impulse_force.length
                rand_impulse = math3d.vector(scalar, scalar, scalar) * impulse_force_unit * rotate_mat
            impulse = (impulse_force + rand_impulse) * math3d.vector(NEOX_UNIT_SCALE, NEOX_UNIT_SCALE, NEOX_UNIT_SCALE)
            center = point
            if is_ragdoll_part:
                affect_radius = self.RAGDOLL_PART_IMPACT_RANGE
            else:
                affect_radius = 0.0
            break_model.enable_ccd(True)
            if break_model.physics:
                break_model.physics.apply_impulse(impulse, center, affect_radius)

    def _process_break_model(self, model_name, break_info, impulse_force, point, normal, is_part_break, no_scale, break_entity_id, is_call_server):
        scn = self.scene()
        old_model = scn.get_model(model_name)
        if not old_model:
            return
        else:
            is_first_touched = old_model.get_attr('first_touched') == '1'
            break_obj_type = int(break_info.get('iBreakType', 0))
            stay_time = float(break_info.get('fExistTime', self.MAX_BREAK_MODEL_TIME))
            cSize = break_info.get('cSize', None)
            ragdoll_collision_sfx = break_info.get('cRagdollCollisionSfx', None)
            if stay_time == 0:
                stay_time = self.MAX_BREAK_MODEL_TIME
            sound_name = break_info.get('sBreakSound', None)
            if not sound_name:
                col_type = confmgr.get('scene_model_inf', old_model.get_attr('model_name'), default={}).get('iColType', None)
                sound_name = self.break_sound_name_map.get(col_type, 'iron_hit')
            global_data.sound_mgr.play_sound('Play_amb_impact', old_model.world_position, ('amb_impact', sound_name))
            break_model_pre = collision_const.BREAK_MODEL_PREFIX
            if global_data.battle and global_data.battle.get_scene_name() == battle_const.BATTLE_SCENE_KONGDAO:
                break_model_pre = collision_const.KONGDAO_BREAK_MODEL_PREFIX
            break_model_path = collision_const.BREAK_MODEL_PATTERN % (break_model_pre, break_info.get('name', ''))
            uinfo = {}
            uinfo['break_info'] = break_info
            uinfo['break_obj_type'] = break_obj_type
            uinfo['is_part_break'] = is_part_break
            uinfo['model_name'] = model_name
            uinfo['is_call_server'] = is_call_server
            uinfo['impulse_force'] = impulse_force
            uinfo['point'] = point
            uinfo['normal'] = normal
            uinfo['first_touched'] = is_first_touched
            uinfo['no_scale'] = no_scale
            uinfo['break_entity_id'] = break_entity_id
            if break_obj_type == collision_const.BREAK_OBJ_TYPE_BUILDING:
                world.create_model_async(break_model_path, self._on_create_break_model, uinfo)
            elif break_obj_type in (collision_const.BREAK_OBJ_TYPE_HP_BOX, collision_const.BREAK_OBJ_TYPE_HP_STATIC, collision_const.BREAK_OBJ_TYPE_HP_DYNAMIC):
                if not is_first_touched:
                    active_breakable(model_name)
                    return
                if is_break_model(old_model):
                    break_model = old_model
                    uinfo['is_break_model'] = True
                    self._on_create_break_model(break_model, uinfo, None)
            else:
                world.create_model_async(break_model_path, self._on_create_break_model, uinfo)
            old_model.set_attr('first_touched', '1')
            return

    def sync_transformation(self, break_model, old_model, no_scale, use_orig_scale=False):
        if use_orig_scale or global_data.game_mode and global_data.game_mode.is_pve():
            if break_model and break_model.valid and old_model and old_model.valid:
                break_model.position = old_model.world_position
                break_model.rotation_matrix = old_model.world_rotation_matrix
                break_model.scale = old_model.scale
            return
        break_model.position = old_model.world_position
        break_model.rotation_matrix = old_model.world_rotation_matrix
        if no_scale:
            return
        ratio = old_model.bounding_radius_w / break_model.bounding_radius_w
        scale = math3d.vector(ratio, ratio, ratio)
        if scale.x < 0 or scale.y < 0 or scale.z < 0:
            log_error('Scale of breakable model should not be negative, please check model:', old_model)
            scale = math3d.vector(abs(scale.x), abs(scale.y), abs(scale.z))
        break_model.scale = scale

    def _on_create_break_model(self, break_model, uinfo, current_task):
        scn = self.scene()
        if not (scn and scn.valid):
            return
        else:
            is_first_touched = uinfo.get('first_touched', None)
            break_info = uinfo.get('break_info', None)
            model_name = uinfo.get('model_name', None)
            break_obj_type = uinfo.get('break_obj_type', None)
            is_part_break = uinfo.get('is_part_break', None)
            point = uinfo.get('point', None)
            normal = uinfo.get('normal', None)
            impulse_force = uinfo.get('impulse_force', None)
            is_call_server = uinfo.get('is_call_server', None)
            is_break_model = uinfo.get('is_break_model', False)
            no_scale = uinfo.get('no_scale', False)
            use_orig_scale = uinfo.get('use_orig_scale', False)
            break_entity_id = uinfo.get('break_entity_id', None)
            if not break_model:
                print('No break_model existed....failed..', model_name)
                return
            old_model = scn.get_model(model_name)
            if not old_model:
                return
            if not is_break_model:
                scn.add_object(break_model)
            if break_model and break_model.valid:
                if not (global_data.game_mode and global_data.game_mode.is_pve()):
                    break_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
                else:
                    break_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'TRUE')
                break_model.all_materials.rebuild_tech()
            pos = old_model.world_position
            break_obj_type = int(break_info.get('iBreakType', 0))
            stay_time = float(break_info.get('fExistTime', self.MAX_BREAK_MODEL_TIME))
            ragdoll_collision_sfx = break_info.get('cRagdollCollisionSfx', None)
            if stay_time == 0:
                stay_time = self.MAX_BREAK_MODEL_TIME
            if break_obj_type == collision_const.BREAK_OBJ_TYPE_BUILDING:
                self.sync_transformation(break_model, old_model, no_scale, use_orig_scale)
                break_model.set_max_depenetration_velocity(200.0)
                break_model.set_no_mutual_ragdoll(True)
                break_ratio = old_model.bounding_box.x / break_model.bounding_box.x
                break_model.scale = math3d.vector(break_ratio, break_ratio, break_ratio)
                break_model.world_position = break_model.world_position - break_model.scale * break_model.center + math3d.vector(0, break_model.center.y * break_ratio, 0)
            else:
                if break_obj_type in (collision_const.BREAK_OBJ_TYPE_HP_BOX, collision_const.BREAK_OBJ_TYPE_HP_STATIC, collision_const.BREAK_OBJ_TYPE_HP_DYNAMIC):
                    return is_first_touched or None
                if break_obj_type in (collision_const.BREAK_OBJ_TYPE_HP_BOX,):
                    stay_time = 65535 if 1 else stay_time
                    self.sync_transformation(break_model, old_model, no_scale, use_orig_scale)
                    if break_obj_type in (collision_const.BREAK_OBJ_TYPE_DYNAMIC,):
                        pass
                    else:
                        break_model.active_collision = True
                    if break_obj_type in (collision_const.BREAK_OBJ_TYPE_HP_DYNAMIC,):
                        cids = get_dynamic_physics_cids(break_model)
                        for cid in cids:
                            scn.add_breakable_hp_obj_cid(old_model.name, cid)

                    else:
                        col_id = break_model.get_col_id()
                        scn.add_breakable_hp_obj_cid(old_model.name, col_id)
                else:
                    self.sync_transformation(break_model, old_model, no_scale, use_orig_scale)
            break_model.cast_shadow = True
            break_model.receive_shadow = True
            recycle_affiliate_break_models(scn, model_name, old_model.world_position)
            self.break_origin_name_map[break_model.name] = old_model.name
            enable_dynamic_physics(break_model)
            if not is_break_model:
                old_model.destroy()
            if break_obj_type == collision_const.BREAK_OBJ_TYPE_HP_DYNAMIC:
                mask = (collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_GRENADE) & ~collision_const.GROUP_CAMERA_COLL
                group = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
            else:
                mask = (collision_const.GROUP_CHARACTER_EXCLUDE | collision_const.GROUP_GRENADE) & ~collision_const.GROUP_CAMERA_COLL
                group = collision_const.GROUP_CHARACTER_EXCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
            break_model.set_mask_and_group(mask, group)
            if break_obj_type == collision_const.BREAK_OBJ_TYPE_HP_STATIC:
                sfx_once = True if 1 else False
                fall_now = int(break_info.get('iFallNow', 0))
                forbid_fall_parts = break_info.get('iForbidFallParts', ())
                ragdoll_hit_sfx = break_info.get('cBreakFx', ())
                break_ragdoll = break_model.physics
                if break_ragdoll:
                    break_ragdoll.set_rigid_body_contact_callback(lambda *args: self.on_ragdoll_rigidbody_contact(break_model.name, ragdoll_collision_sfx, sfx_once, fall_now, forbid_fall_parts, *args))
                if fall_now and ragdoll_hit_sfx:
                    for rsfx in ragdoll_hit_sfx:
                        global_data.sfx_mgr.create_sfx_in_scene(rsfx, break_model.world_position, int_check_type=CREATE_SRC_SIMPLE)

                if is_part_break:
                    break_model.set_no_mutual_ragdoll(True)
                    break_ragdoll.set_all_rigid_body_kinematic(True)
                self._apply_impulse_break(break_model, break_obj_type, impulse_force, point, is_part_break)
                binfo = self.loaded_break_models.get(break_model.name, None)
                if binfo:
                    pass
                else:
                    self.loaded_break_models[break_model.name] = {'break_model': break_model,'start_time': time.time(),'stay_time': stay_time,'is_part_break': is_part_break}
                global_data.game_mode and global_data.game_mode.is_pve() or scn.del_model_in_cache(model_name, break_model.world_position)
            if is_call_server:
                euler = 0
                if break_info:
                    col_size = break_info.get('cSize')
                    if col_size:
                        from logic.gcommon.common_utils.math3d_utils import v3d_to_tp
                        euler = v3d_to_tp(math3d.matrix_to_euler(break_model.world_rotation_matrix))
                self._break_model_sync(model_name, break_obj_type, pos, point, normal, euler, break_entity_id)
            return

    def _break_model_sync(self, model_name, break_obj_type, pos, point, normal, euler=0, break_entity_id=None):
        if global_data.player and global_data.player.logic and not (global_data.game_mode and global_data.game_mode.is_pve()):
            break_id = model_name
            lpos = (pos.x, pos.y, pos.z)
            lpoint = (point.x, point.y, point.z)
            lnormal = (normal.x, normal.y, normal.z)
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'do_break', (break_id, break_obj_type, lpos, [lpoint, lnormal, euler], break_entity_id), False, False)

    def handle_break_ragdoll_part(self, break_list):
        if not break_list:
            return
        else:
            scn = self.scene()
            pos = None
            break_obj_type = collision_const.BREAK_OBJ_TYPE_NONE
            stay_time = self.MAX_BREAK_MODEL_TIME
            break_model = None
            if scn and scn.valid:
                for break_item_info in break_list:
                    model_full_name = break_item_info.get('model_col_name', '')
                    point = break_item_info.get('point', None)
                    normal = break_item_info.get('normal', None)
                    force = break_item_info.get('power', None)
                    break_type = break_item_info.get('break_type', None)
                    if '@' in model_full_name:
                        model_name, col_name = model_full_name.split('@')
                    else:
                        model_name = model_full_name
                        col_name = model_full_name
                    break_model = scn.get_model(model_name)
                    if not (break_model and break_model.valid):
                        continue
                    if force is None:
                        force = 800
                    normal.normalize()
                    force = int(force)
                    impulse_force = -normal * force
                    self._apply_impulse_break(break_model, break_obj_type, impulse_force, point, True)

                if not break_model:
                    return
                break_ragdoll = break_model.physics
                if break_ragdoll:
                    tot_cnt = break_ragdoll.rigid_body_count
                    stable_cnt = break_ragdoll.get_rigid_body_kinematic_count()
                    break_cnt = tot_cnt - stable_cnt
                    break_ratio = break_cnt / float(tot_cnt)
                    origin_model_name = self.get_origin_model_name(model_name)
                    break_info = get_break_info_by_full_name(origin_model_name)
                    is_part_break = break_info.get('iPartBreak', None)
                    if is_part_break and break_ratio > self.RAGDOLL_PART_DESTROY_RATIO:
                        if break_model.valid:
                            global_data.sfx_mgr.create_sfx_in_scene(self.RAGDOLL_BREAK_SFX, point, int_check_type=CREATE_SRC_SIMPLE)
                            break_model.destroy()
            return

    def handle_break_objs(self, break_list, is_call_server=False):
        if not break_list:
            return
        else:
            scn = self.scene()
            if scn and scn.valid:
                for break_item_info in break_list:
                    model_full_name = break_item_info.get('model_col_name', '')
                    point = break_item_info.get('point', None)
                    normal = break_item_info.get('normal', None)
                    force = break_item_info.get('power', None)
                    break_type = break_item_info.get('break_type', None)
                    no_scale = break_item_info.get('no_scale', False)
                    break_entity_id = break_item_info.get('break_entity_id', None)
                    bullet_type = break_item_info.get('bullet_type', None)
                    if bullet_type:
                        harm_info = confmgr.get('break_data', str(bullet_type), default={})
                        if harm_info:
                            break_chance = float(harm_info.get('fBreakChance', '0')) * 100
                            if break_chance < random.uniform(0, 1) * 100:
                                continue
                    if '@' in model_full_name:
                        model_name, col_name = model_full_name.split('@')
                    else:
                        model_name = model_full_name
                        col_name = model_full_name
                    break_info = get_break_info_by_full_name(model_full_name)
                    is_part_break = break_info.get('iPartBreak', None)
                    if break_type == collision_const.BREAK_TRIGGER_TYPE_MECHA_MOVE and not break_info.get('iMechaBreak', 0):
                        continue
                    elif break_type == collision_const.BREAK_TRIGGER_TYPE_MECHA_DASH and not break_info.get('iDashBreak', 0):
                        continue
                    elif break_type == collision_const.BREAK_TRIGGER_TYPE_WEAPON and not break_info.get('iWeaponBreak', 0):
                        continue
                    elif break_type == collision_const.BREAK_TRIGGER_TYPE_VEHICLE_MOVE and not break_info.get('iVehicleBreak', 0):
                        continue
                    has_break_res = break_info.get('iBreakRes', None)
                    if force is None:
                        force = 800
                    self._process_dynamic_box(model_name, point, force)
                    if normal.is_zero:
                        normal = math3d.vector(0, 1, 0)
                    normal.normalize()
                    force = int(force)
                    impulse_force = -normal * force
                    if has_break_res:
                        self._process_break_model(model_name, break_info, impulse_force, point, normal, is_part_break, no_scale, break_entity_id, is_call_server)
                    scn.add_filter_model_name(model_name)
                    if hasattr(scn, 'enable_indices_by_name'):
                        scn.enable_indices_by_name(model_name, False)

            return

    def on_ragdoll_rigidbody_contact(self, break_name, ragdoll_collision_sfx, sfx_once, fall_now, forbid_fall_parts, *args):
        if len(args) == 3:
            cobj, point, normal = args
        else:
            my_obj, cobj, touch, hit_info = args
            if not touch:
                return
            point = hit_info.position
            normal = hit_info.normal
        if sfx_once:
            if self.break_model_triggerd_ragdoll_part.get(break_name, {}).get(cobj.cid, None):
                return
            self.break_model_triggerd_ragdoll_part.setdefault(break_name, {})
            self.break_model_triggerd_ragdoll_part[break_name][cobj.cid] = True
        if ragdoll_collision_sfx:
            ragdoll_collision_sfx = ragdoll_collision_sfx if 1 else self.ragdoll_collision_sfx
            if ragdoll_collision_sfx and cobj and cobj.group in (TERRAIN_GROUP, GLASS_GROUP, WOOD_GROUP, METAL_GROUP, STONE_GROUP):

                def create_cb(sfx):
                    global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

                global_data.sfx_mgr.create_sfx_in_scene(ragdoll_collision_sfx, point, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
        if fall_now:
            scn = self.scene()
            parent_model = scn.get_model(my_obj.model_col_name)
            if parent_model:

                def _rigid_body_clear_mask_and_group(rigid_body):
                    if rigid_body:
                        rigid_body.mask = 0
                        rigid_body.group = 0

                for i in range(parent_model.physics.rigid_body_count):
                    rigid_body = parent_model.physics.get_rigid_body(i)
                    if i not in forbid_fall_parts:
                        global_data.game_mgr.register_logic_timer(lambda _rigid_body=rigid_body: _rigid_body_clear_mask_and_group(_rigid_body), interval=1, times=1, mode=common.utils.timer.CLOCK)

        return

    def on_update(self, dt):
        now = time.time()
        to_del = []
        for break_name, break_info in six.iteritems(self.loaded_break_models):
            break_model = break_info.get('break_model', None)
            start_time = break_info.get('start_time', None)
            stay_time = break_info.get('stay_time', None)
            is_part_break = break_info.get('is_part_break', None)
            has_triggered = break_info.get('has_triggered', None)
            if not break_model.valid:
                to_del.append(break_name)
                continue
            if now - start_time > stay_time:
                to_del.append(break_name)
            if now - start_time > stay_time - self.FALLDOWN_TIME:
                has_triggered = self.loaded_break_models[break_name].get('has_triggered', False)
                if has_triggered:
                    continue
                self.loaded_break_models[break_name]['has_triggered'] = True
                if is_part_break:
                    break_ragdoll = break_model.physics
                    if break_ragdoll:
                        break_ragdoll.set_all_rigid_body_kinematic(False)
                    x = random.randint(-100, 100)
                    y = random.randint(-100, 0)
                    z = random.randint(-100, 100)
                    force = math3d.vector(x, y, z) * math3d.vector(NEOX_UNIT_SCALE, NEOX_UNIT_SCALE, NEOX_UNIT_SCALE)
                    break_model.physics.apply_impulse(force, break_model.world_position, 0)
                    pos = math3d.vector(break_model.world_position.x, break_model.world_position.y + break_model.center.y, break_model.world_position.z)
                    global_data.sfx_mgr.create_sfx_in_scene(self.RAGDOLL_BREAK_SFX, pos, int_check_type=CREATE_SRC_SIMPLE)
                else:
                    break_model.set_mask_and_group(0, 0)

        for break_name in to_del:
            binfo = self.loaded_break_models.get(break_name, None)
            if binfo:
                break_model = binfo.get('break_model', None)
                if break_model.valid:
                    break_model.destroy()
            self.loaded_break_models.pop(break_name, None)
            self.break_model_triggerd_ragdoll_part.pop(break_name, None)
            self.break_origin_name_map.pop(break_name, None)

        return

    def on_exit(self):
        for binfo in six.itervalues(self.loaded_break_models):
            break_model = binfo.get('break_model', None)
            if break_model and break_model.valid:
                break_model.destroy()

        self.loaded_break_models = {}
        self.break_model_triggerd_ragdoll_part = {}
        self.break_origin_name_map = {}
        self.dynamic_box_info.clear()
        return