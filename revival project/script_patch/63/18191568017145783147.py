# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/scene_utils.py
from __future__ import absolute_import
from six.moves import range
import random
import math
import math3d
import collision
import world
from common.cfg import confmgr
from logic.gcommon.common_const import scene_const
from logic.client.const import game_mode_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from data.room_break_data import data as room_break_list
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const.collision_const import ROAD_GROUP, DIRT_GROUP, GRASS_GROUP, SAND_GROUP, GROUP_BREAK, GROUP_STATIC_SHOOTUNIT, TERRAIN_GROUP, GLASS_GROUP, WOOD_GROUP, GROUP_CAMERA_COLL, WATER_GROUP, WATER_MASK, GROUP_CHARACTER_INCLUDE, GROUP_STATIC_SHOOTUNIT, GROUP_AUTO_AIM, METAL_GROUP, STONE_GROUP, BUILDING_GROUP, BREAK_OBJ_TYPE_HP_BOX, BREAK_OBJ_TYPE_HP_STATIC, BREAK_OBJ_TYPE_HP_DYNAMIC, GROUP_MECHA_BALL
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import poison_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
import game3d
import render
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gutils import tech_pass_utils
from logic.caches import fun_cache
from common.utils.cocos_utils import cocos_pos_to_neox
import os
UI_SCENE_BOX_PREFIX = 'bw_box_'
AIRWALL_COL_EFFECT_PATH = 'effect/fx/scenes/common/pve/pve_stop.sfx'
MODEL_PREFIX_CACHE = {}
SNOW_SCENE_BOX_MODEL_ENT_MAP = {}
RAGDOLL_DIE_FORCE_RANGES = (
 (10000, 30000), (1000000, 1100000), (10000, 30000))
RAGDOLL_CUSTOM_GRAVITY_VAL = math3d.vector(0, -9.8 * NEOX_UNIT_SCALE * 200, 0)

def screen_pos_to_world_pos(x, y):
    scene = world.get_active_scene()
    if not scene:
        return
    else:
        start_pt, dir = scene.active_camera.screen_to_world(x, y)
        end_pt = start_pt + dir * 300.0
        result = scene.scene_col.hit_by_ray(start_pt, end_pt, 0, GROUP_CAMERA_COLL, GROUP_CAMERA_COLL, collision.INCLUDE_FILTER)
        if result is None or not result[0]:
            return
        pos = math3d.vector(result[1].x, result[1].y, result[1].z)
        return pos
        return


def cocos_pos_to_ui_world_pos(cocos_pos):

    def get_ray_to_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal, distance):
        epsilon = 0.0001
        d = ray_direction.dot(plane_normal)
        if abs(d) < epsilon:
            t = distance
        else:
            t = (plane_point - ray_origin).dot(plane_normal) / d
            if t < epsilon:
                t = distance
            if t > distance:
                t = distance
        return ray_direction * t + ray_origin

    def screen_to_world_point(screen_x, screen_y, plane_normal, plane_point, distance):
        scene = world.get_active_scene()
        camera = scene.active_camera
        ray_origin, ray_direction = camera.screen_to_world(screen_x, screen_y)
        ray_direction.normalize()
        return get_ray_to_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal, distance)

    normal = math3d.vector(0, 0, 1)
    point = math3d.vector(0, 0, 0)
    scene = world.get_active_scene()
    camera = scene.active_camera
    distance = 1000
    screen_x, screen_y = cocos_pos_to_neox(cocos_pos.x, cocos_pos.y)
    pos = screen_to_world_point(screen_x, screen_y, normal, point, distance)
    return pos


def get_land_height--- This code section failed: ---

 132       0  LOAD_GLOBAL           0  'world'
           3  LOAD_ATTR             1  'get_active_scene'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  'scene'

 133      12  LOAD_FAST             2  'scene'
          15  POP_JUMP_IF_TRUE     22  'to 22'

 134      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 135      22  LOAD_GLOBAL           3  'math3d'
          25  LOAD_ATTR             4  'vector'
          28  LOAD_ATTR             1  'get_active_scene'
          31  LOAD_FAST             1  'z'
          34  CALL_FUNCTION_3       3 
          37  STORE_FAST            3  'tp1'

 136      40  LOAD_GLOBAL           3  'math3d'
          43  LOAD_ATTR             4  'vector'
          46  LOAD_ATTR             2  'None'
          49  LOAD_FAST             1  'z'
          52  CALL_FUNCTION_3       3 
          55  STORE_FAST            4  'tp2'

 137      58  LOAD_FAST             2  'scene'
          61  LOAD_ATTR             5  'scene_col'
          64  LOAD_ATTR             6  'hit_by_ray'

 138      67  LOAD_FAST             3  'tp1'
          70  LOAD_FAST             4  'tp2'
          73  LOAD_CONST            3  ''

 139      76  LOAD_GLOBAL           7  'collision_const'
          79  LOAD_ATTR             8  'LAND_GROUP'
          82  LOAD_GLOBAL           7  'collision_const'
          85  LOAD_ATTR             8  'LAND_GROUP'

 140      88  LOAD_GLOBAL           9  'collision'
          91  LOAD_ATTR            10  'INCLUDE_FILTER'
          94  CALL_FUNCTION_6       6 
          97  STORE_FAST            5  'ret'

 141     100  LOAD_FAST             5  'ret'
         103  POP_JUMP_IF_FALSE   131  'to 131'
         106  LOAD_FAST             5  'ret'
         109  LOAD_CONST            3  ''
         112  BINARY_SUBSCR    
       113_0  COME_FROM                '103'
         113  POP_JUMP_IF_FALSE   131  'to 131'

 142     116  LOAD_FAST             5  'ret'
         119  LOAD_CONST            4  1
         122  BINARY_SUBSCR    
         123  LOAD_ATTR            11  'y'
         126  LOAD_CONST            4  1
         129  BINARY_ADD       
         130  RETURN_END_IF    
       131_0  COME_FROM                '113'

 143     131  LOAD_CONST            0  ''
         134  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 34


def init_ui_scene_camera(scene_part, flag=False):
    scn = scene_part.scene()
    active_camera = scn.active_camera
    local_m = None
    if flag:
        local_m = scn.get_preset_camera('cam_ziji')
    else:
        local_m = scn.get_preset_camera('cam2')
    if local_m:
        active_camera.transformation = local_m
    else:
        active_camera.transformation = math3d.matrix()
    return


def enable_dynamic_physics(model):
    model.physics_enable = True
    break_ragdoll = model.physics
    if break_ragdoll:
        for i in range(break_ragdoll.rigid_body_count):
            rigid_body = break_ragdoll.get_rigid_body(i)
            rigid_body.model_col_name = model.name


def get_dynamic_physics_cids(model):
    ret = []
    break_ragdoll = model.physics
    if break_ragdoll:
        for i in range(break_ragdoll.rigid_body_count):
            rigid_body = break_ragdoll.get_rigid_body(i)
            ret.append(rigid_body.cid)

    return ret


def get_model_check_name(model_name, use_orig=True):
    scn = world.get_active_scene()
    if not scn:
        return ''
    else:
        check_name = ''
        break_model = scn.get_model(model_name)
        if break_model:
            if use_orig:
                orig_break_id = break_model.get_attr('orig_break_id')
                if orig_break_id:
                    return orig_break_id
            check_name = break_model.get_attr('model_name')
            if not check_name and global_data.game_mode and global_data.game_mode.is_pve():
                try:
                    check_name = break_model.filename
                    check_name = os.path.split(check_name)[-1].split('.')[0]
                except:
                    check_name = None

            if not check_name:
                check_name = model_name
        else:
            prefix = get_break_obj_prefix_auto(model_name)
            check_name = prefix
        return check_name


def get_break_info_by_full_name(model_full_name):
    from logic.gcommon.cdata.item_break_data import data as IBD
    if not global_data.battle:
        return {}
    check_name = get_model_check_name(model_full_name)
    binfo = IBD.get(check_name, {})
    ban_scenes = binfo.get('iBanBreak', ())
    if ban_scenes:
        map_id = global_data.battle.map_id
        if map_id in ban_scenes:
            return {}
    return binfo


def get_break_obj_prefix(model_name, delimiter_idx=1):
    if not model_name:
        return ''
    else:
        col_name_split = model_name.split('@')
        sign_cnt = len(col_name_split)
        col_name_prefix = col_name_split[-1]
        if sign_cnt > 1:
            return col_name_prefix
        for i in range(delimiter_idx):
            last_idx = col_name_prefix.rfind('_')
            last_phase_str = col_name_prefix[last_idx + 1:]
            prefix_phase_str = col_name_prefix[0:last_idx]
            if last_phase_str.isdigit():
                col_name_prefix = prefix_phase_str
            else:
                return col_name_prefix

        return col_name_prefix


def get_break_obj_prefix_auto(model_name):
    if not model_name:
        return ''
    else:
        if model_name in MODEL_PREFIX_CACHE:
            return MODEL_PREFIX_CACHE[model_name]
        col_name_split = model_name.split('@')
        sign_cnt = len(col_name_split)
        col_name_prefix = col_name_split[-1]
        if sign_cnt > 1:
            return col_name_prefix
        for i in range(5):
            last_idx = col_name_prefix.rfind('_')
            last_phase_str = col_name_prefix[last_idx + 1:]
            prefix_phase_str = col_name_prefix[0:last_idx]
            pre_idx = prefix_phase_str.rfind('_')
            pre_digit_cut = prefix_phase_str[pre_idx + 1:]
            if last_phase_str.isdigit() and not pre_digit_cut.isdigit():
                MODEL_PREFIX_CACHE[model_name] = col_name_prefix
                return col_name_prefix
            if last_phase_str.isdigit():
                col_name_prefix = prefix_phase_str
            else:
                MODEL_PREFIX_CACHE[model_name] = col_name_prefix
                return col_name_prefix

        MODEL_PREFIX_CACHE[model_name] = col_name_prefix
        return col_name_prefix


def is_break_obj(model_name):
    from logic.gcommon.cdata.item_break_data import data as IBD
    if not global_data.battle:
        return False
    check_name = get_model_check_name(model_name)
    binfo = IBD.get(check_name, {})
    ban_scenes = binfo.get('iBanBreak', ())
    if ban_scenes:
        map_id = global_data.battle.map_id
        if map_id in ban_scenes:
            return False
    return check_name in IBD


@fun_cache(128)
def is_break_obj_orig(model_name):
    from logic.gcommon.cdata.item_break_data import data as IBD
    if not global_data.battle:
        return False
    if global_data.game_mode.is_pve() and not global_data.enable_pve_breakable:
        return False
    check_name = get_model_check_name(model_name, False)
    binfo = IBD.get(check_name, {})
    ban_scenes = binfo.get('iBanBreak', ())
    if ban_scenes:
        map_id = global_data.battle.map_id
        if map_id in ban_scenes:
            return False
    return check_name in IBD


def break_obj_should_activiate(model_name):
    if not is_break_obj_orig(model_name):
        return False
    if is_break_obj_first_touched(model_name):
        return False
    return True


@fun_cache(128)
def break_obj_bullet_trigger(model_name):
    from logic.gcommon.cdata.item_break_data import data as IBD
    prefix_name = get_model_check_name(model_name, False)
    if not is_break_obj_orig(prefix_name):
        return False
    binfo = IBD.get(prefix_name, {})
    return bool(binfo.get('iBulletBreak', 0))


def is_break_obj_first_touched(model_name):
    scn = world.get_active_scene()
    if not scn:
        return True
    model = scn.get_model(model_name)
    if not model:
        return True
    return model.get_attr('first_touched')


def is_break_model(model):
    if global_data.game_mode.is_pve() and not global_data.enable_pve_breakable:
        return False
    return model.get_attr('orig_break_id') and model.get_attr('orig_break_id') != model.name


def active_breakable(break_id):
    import world
    scn = world.get_active_scene()
    if not scn:
        return
    else:
        if global_data.game_mode.is_pve() and not global_data.enable_pve_breakable:
            return
        break_info = get_break_info_by_full_name(break_id)
        break_obj_type = int(break_info.get('iBreakType', 0))
        if break_obj_type not in (BREAK_OBJ_TYPE_HP_BOX, BREAK_OBJ_TYPE_HP_STATIC, BREAK_OBJ_TYPE_HP_DYNAMIC):
            return
        model = scn.get_model(break_id)
        if not model:
            return
        if model.get_attr('first_touched') == '1':
            return
        pos = model.world_position
        ws = model.world_scale
        wrm = model.world_rotation_matrix
        cSize = break_info.get('cSize', None)
        cSize = tuple(cSize) if cSize else None
        if cSize is None and model:
            cSize = (
             model.bounding_box.x * 2.0, model.bounding_box.y * 2.0, model.bounding_box.z * 2.0)
        cSize = (
         cSize[0] * ws.x, cSize[1] * ws.y, cSize[2] * ws.z)
        cPosOff = break_info.get('cPosOffset', (0, 0, 0))
        cPosOff = wrm.forward * cPosOff[0] + wrm.up * cPosOff[1] + wrm.right * cPosOff[2]
        cPosOff = cPosOff * ws * NEOX_UNIT_SCALE
        cPos = pos + cPosOff
        model.set_attr('first_touched', '1')
        global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'active_breakable', (BREAK_OBJ_TYPE_HP_BOX, break_id, (cPos.x, cPos.y, cPos.z), {'col_size': cSize}, break_info.get('name', None)))
        return


def is_airwall_model(model_name):
    return model_name and model_name.startswith('kq_pve')


def get_airwall_sfx():
    return AIRWALL_COL_EFFECT_PATH


def use_special_hit_sfx(bullet_type, group):
    harm_info = confmgr.get('break_data', str(bullet_type), default=None)
    if not harm_info:
        return False
    else:
        special_sfx_path_list = harm_info.get('cBreakBulletHit', None)
        if special_sfx_path_list and len(special_sfx_path_list) == 4:
            if group in (TERRAIN_GROUP, DIRT_GROUP, GRASS_GROUP, SAND_GROUP):
                sfx_idx = 0
            elif group in (METAL_GROUP, STONE_GROUP, BUILDING_GROUP):
                sfx_idx = 1
            elif group == WOOD_GROUP:
                sfx_idx = 2
            elif group == GLASS_GROUP:
                sfx_idx = 1
            else:
                return False
        else:
            return False
        return len(special_sfx_path_list[sfx_idx]) > 0


def recycle_affiliate_break_models(scn, break_id, center_pos):
    break_info = get_break_info_by_full_name(break_id)
    if not break_info:
        return
    else:
        aff_model_prefix_group = break_info.get('cRecoveryRes', None)
        aff_model_range = break_info.get('cRecoveryRange', None)
        aff_trigger_sfx_path = break_info.get('cAffTriggerSfxPath', None)
        if not (aff_model_prefix_group and aff_model_range):
            return
        for aff_model_prefix in aff_model_prefix_group:
            aff_models = scn.get_models_by_prefix(aff_model_prefix)
            if not aff_models:
                continue
            for m_name in aff_models:
                m = scn.get_model(m_name)
                if not (m and m.valid):
                    scn.hide_async_model(m_name)
                    continue
                old_world_position = m.world_position
                world_pos_2d = math3d.vector(m.world_position.x, 0, m.world_position.z)
                center_pos_2d = math3d.vector(center_pos.x, 0, center_pos.z)
                if (world_pos_2d - center_pos_2d).length < int(aff_model_range) * NEOX_UNIT_SCALE:
                    if aff_trigger_sfx_path:
                        for aff_sfx in aff_trigger_sfx_path:
                            global_data.sfx_mgr.create_sfx_in_scene(aff_sfx, m.world_position)

                    m.destroy()
                    if not (global_data.game_mode and global_data.game_mode.is_pve()):
                        scn.del_model_in_cache(m_name, old_world_position)

        return


def process_hit_sfx(bullet_type, group, mask, pos, normal, forward_dir, up_dir, model_name=''):
    if group in (WATER_GROUP,):
        return
    else:
        if mask & GROUP_BREAK and group & GROUP_STATIC_SHOOTUNIT:
            return
        harm_info = confmgr.get('break_data', str(bullet_type), default={})
        break_chance = float(harm_info.get('fBreakChance', '0')) * 100
        if break_chance < random.uniform(0, 1) * 100:
            return
        display_range_limit = float(harm_info.get('fDisplayRangeLimit', '0')) * NEOX_UNIT_SCALE
        if bullet_type:
            special_sfx_path_list = harm_info.get('cBreakBulletHit', None)
        else:
            special_sfx_path_list = None
        sfx_path = scene_const.collision_sfx_map.get(group, None)
        if sfx_path is not None:
            sfx_path = sfx_path[1]
        decal_tex_size = (0, 0)
        sfx_idx = 0
        if special_sfx_path_list and len(special_sfx_path_list) == 4:
            if group in (TERRAIN_GROUP, ROAD_GROUP, DIRT_GROUP, GRASS_GROUP, SAND_GROUP):
                sfx_idx = 0
            elif group in (METAL_GROUP, STONE_GROUP, BUILDING_GROUP):
                sfx_idx = 1
            elif group == WOOD_GROUP:
                sfx_idx = 2
            elif group == GLASS_GROUP:
                sfx_idx = 1
            else:
                return
            sfx_path = special_sfx_path_list[sfx_idx]
        if not sfx_path:
            sfx_path = scene_const.collision_default_sfx[1]
        harm_info = confmgr.get('break_data', str(bullet_type), default=None)
        if harm_info:
            sfx_lifetime = float(harm_info.get('cExisttime', 1.5))
            sfx_scale_min = harm_info.get('cMinRatio', (1.0, 1.0, 1.0, 1.0))[sfx_idx]
            sfx_scale_max = harm_info.get('cMaxRatio', (1.0, 1.0, 1.0, 1.0))[sfx_idx]
            sfx_scale = random.uniform(sfx_scale_min, sfx_scale_max)
        else:
            sfx_lifetime = 10.0
            sfx_scale = random.uniform(0.3, 3)
        if not normal.is_zero:
            normal.normalize()
        else:
            return
        if forward_dir and up_dir and not (forward_dir.is_zero or up_dir.is_zero):
            rot_mat = math3d.matrix.make_orient(forward_dir, up_dir)
        else:
            rot_mat = None

        def create_cb_2(sfx):
            sfx.scale = math3d.vector(sfx_scale, sfx_scale, sfx_scale)
            if rot_mat:
                global_data.sfx_mgr.set_rotation_by_pivot(sfx, normal, rot_mat.yaw)
            else:
                global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, duration=sfx_lifetime, on_create_func=create_cb_2, ex_data={'col_group': group,'display_range_limit': display_range_limit}, int_check_type=CREATE_SRC_SIMPLE)
        return


def trigger_show_outline(unit, trigger_id):
    if not unit:
        return
    if unit.__class__.__name__ == 'LMecha':
        mecha = unit
        driver_id = mecha.sd.ref_driver_id
        driver = EntityManager.getentity(driver_id)
        if driver and not driver.logic.ev_g_is_groupmate(trigger_id):
            mecha.send_event('E_SHOW_OUTLINE')
    elif not unit.ev_g_is_groupmate(trigger_id):
        unit.send_event('E_SHOW_OUTLINE')


def random_pos_by_circle(x, z, range):
    angle = random.randint(0, 360)
    range = random.randint(1, range)
    off_x = range * math.cos(math.pi * angle / 180.0)
    off_z = range * math.sin(math.pi * angle / 180.0)
    return (
     int(off_x + x), int(off_z + z))


def show_scene_collision(pos=None):
    import world
    show_col = getattr(global_data, 'show_col', False)
    scene = world.get_active_scene()
    scol = scene.scene_col
    if show_col:
        scol.drawing = False
    else:
        scol.drawing = True
        scol.drawing_radius = 1000
        pos = pos or global_data.player.logic.ev_g_position()
        scol.drawing_center = pos
    global_data.show_col = not bool(show_col)


def add_region_scene_collision(center, length, width, height=None, rot_mat=None):
    x, y, z = center
    mass = 0
    mask = collision_const.TERRAIN_MASK
    group = collision_const.REGION_SCENE_GROUP
    _scn = world.get_active_scene()
    size = math3d.vector(10, 4000, width)
    col_l = collision.col_object(collision.BOX, size, mask, group, mass)
    if rot_mat:
        col_l.rotation_matrix = rot_mat
        position = math3d.vector(x, y, z) + math3d.vector(-length, 0, 0) * rot_mat
    else:
        position = math3d.vector(x - length, y, z)
    col_l.position = position
    _scn.scene_col.add_object(col_l)
    col_r = collision.col_object(collision.BOX, size, mask, group, mass)
    if rot_mat:
        col_r.rotation_matrix = rot_mat
        position = math3d.vector(x, y, z) + math3d.vector(length, 0, 0) * rot_mat
    else:
        position = math3d.vector(x + length, y, z)
    col_r.position = position
    _scn.scene_col.add_object(col_r)
    size = math3d.vector(length, 4000, 10)
    col_d = collision.col_object(collision.BOX, size, mask, group, mass)
    if rot_mat:
        col_d.rotation_matrix = rot_mat
        position = math3d.vector(x, y, z) + math3d.vector(0, 0, -width) * rot_mat
    else:
        position = math3d.vector(x, y, z - width)
    col_d.position = position
    _scn.scene_col.add_object(col_d)
    col_u = collision.col_object(collision.BOX, size, mask, group, mass)
    if rot_mat:
        col_u.rotation_matrix = rot_mat
        position = math3d.vector(x, y, z) + math3d.vector(0, 0, width) * rot_mat
    else:
        position = math3d.vector(x, y, z + width)
    col_u.position = position
    _scn.scene_col.add_object(col_u)
    if height:
        size = math3d.vector(length, 10, width)
        col_top = collision.col_object(collision.BOX, size, mask, group, mass)
        if rot_mat:
            col_d.rotation_matrix = rot_mat
            position = math3d.vector(x, y, z) + math3d.vector(0, height, 0) * rot_mat
        else:
            position = math3d.vector(x, y + height, z)
        col_top.position = position
        _scn.scene_col.add_object(col_top)
        return [
         col_l, col_r, col_d, col_u, col_top]
    return [col_l, col_r, col_d, col_u]


def add_region_scene_collision_box(center, length, width, height=2000, rotate_y=0.0, cull=True, col_group=collision_const.REGION_BOUNDARY_SCENE_GROUP):
    if type(center) is math3d.vector:
        pos = center
        x, y, z = center.x, center.y, center.z
    else:
        x, y, z = center
        pos = math3d.vector(x, y, z)
    if height is None:
        height = 2000

    def create_cb(model):
        model.visible = False
        model.set_col_group_mask(col_group, col_group)
        model.active_collision = True
        model.scale = math3d.vector(length / model.bounding_box.x, (height - y) * 0.5 / model.bounding_box.y, width / model.bounding_box.z)
        if rotate_y:
            model.rotate_y(rotate_y / 180.0 * math.pi)

    collision_box_res = confmgr.get('script_gim_ref')['region_collision_box']
    model_id = global_data.model_mgr.create_model_in_scene(collision_box_res, pos, on_create_func=create_cb)
    if not cull:
        collision_box_res = confmgr.get('script_gim_ref')['region_collision_box_no_cull']
        model_id_l = global_data.model_mgr.create_model_in_scene(collision_box_res, pos, on_create_func=create_cb)
        return (
         model_id, model_id_l)
    else:
        return model_id


def is_hit_region_scene_collision(start_pos, end_pos):
    _scn = world.get_active_scene()
    if not _scn:
        return
    mask = collision_const.REGION_BOUNDARY_SCENE_MASK
    group = collision_const.REGION_BOUNDARY_SCENE_GROUP
    res = _scn.scene_col.hit_by_ray(start_pos, end_pos, 0, mask, group, collision.EQUAL_FILTER, True)
    return res


HERO_OUTLINE_MASK = 1
INFRARED_DETECTOR_MASK = 2
GAME_MODE_OUTLINE_MASK = 16
g_outline_process_mask = 0
_ENABLE_HERO_OUTLINE = game3d.calc_string_hash('enable_hero_outline')
_ENABLE_FX_TARGET = game3d.calc_string_hash('enable_fx_target')
_HASH_outline_wide = game3d.calc_string_hash('outline_wide')

def need_game_mode_outline():
    return global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.Need_OutLine)


def set_outline_process_enable(enable, mask):
    global g_outline_process_mask
    old_mask = g_outline_process_mask
    if enable:
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        g_outline_process_mask |= mask
    else:
        g_outline_process_mask &= ~mask
    if bool(old_mask) == bool(g_outline_process_mask):
        return
    reset_outline_process()


def reset_outline_process():
    if global_data.battle and global_data.battle.is_in_island():
        return
    if global_data.is_ue_model:
        global_data.display_agent.set_longtime_post_process_active('hero_outlinehero_outline', bool(g_outline_process_mask))
        flag = 1.0 if bool(g_outline_process_mask) else 0.0
        global_data.display_agent.update_longtime_post_process_params('hdr_tonemap', {0: {_ENABLE_HERO_OUTLINE: ('var', 'enable_hero_outline', flag)}})
    else:
        flag = 1.0 if bool(g_outline_process_mask) else 0.0
        outline_wide = 2.0 if game3d.get_platform() == game3d.PLATFORM_WIN32 else 1.0
        global_data.display_agent.update_longtime_post_process_params('hdr_tonemap', {0: {_ENABLE_HERO_OUTLINE: (
                                    'var', 'enable_hero_outline', flag),
               _HASH_outline_wide: (
                                  'var', 'outline_wide', outline_wide)
               },
           1: {_ENABLE_HERO_OUTLINE: ('var', 'enable_hero_outline', flag)}})
        global_data.display_agent.update_longtime_post_process_params('hdr', {5: {_ENABLE_HERO_OUTLINE: (
                                    'var', 'enable_hero_outline', flag),
               _HASH_outline_wide: (
                                  'var', 'outline_wide', outline_wide)
               },
           6: {_ENABLE_HERO_OUTLINE: ('var', 'enable_hero_outline', flag)}})


def pause_outline_process():
    if global_data.is_ue_model:
        global_data.display_agent.set_longtime_post_process_active('hero_outlinehero_outline', False)
        flag = 0.0
        global_data.display_agent.update_longtime_post_process_params('hdr_tonemap', {0: {_ENABLE_HERO_OUTLINE: ('var', 'enable_hero_outline', flag)}})
    else:
        flag = 0.0
        global_data.display_agent.update_longtime_post_process_params('hdr_tonemap', {0: {_ENABLE_HERO_OUTLINE: (
                                    'var', 'enable_hero_outline', flag)
               },
           1: {_ENABLE_HERO_OUTLINE: ('var', 'enable_hero_outline', flag)}})
        global_data.display_agent.update_longtime_post_process_params('hdr', {5: {_ENABLE_HERO_OUTLINE: (
                                    'var', 'enable_hero_outline', flag)
               },
           6: {_ENABLE_HERO_OUTLINE: ('var', 'enable_hero_outline', flag)}})


def clear_outline_process():
    global g_outline_process_mask
    g_outline_process_mask = 0
    reset_outline_process()


def is_lobby_relatived_scene(scene_type):
    scene_conf = confmgr.get('scenes', scene_type)
    lobby_relatived_scene = scene_conf.get('lobby_relatived_scene', '')
    if lobby_relatived_scene:
        return True
    else:
        return False


def is_in_lobby(scene_type):
    if scene_type == scene_const.SCENE_LOBBY or is_lobby_relatived_scene(scene_type) or scene_type == scene_const.SCENE_LOBBY_MIRROR:
        return True
    else:
        return False


def env_path(env_name):
    return 'scene/scene_env_confs/{}'.format(env_name)


def get_poison_type():
    if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
        return poison_const.CIRCLE_POISON
    return poison_const.NONE_POISON


def is_circle_poison():
    return get_poison_type() == poison_const.CIRCLE_POISON


def is_fixed_rect_poison():
    return get_poison_type() == poison_const.FIXED_RECT_POISON


def set_col_scale(col, scale):
    if not col or not scale:
        return
    shape = col.get_shape(0)
    if not shape:
        return
    if isinstance(scale, math3d.vector):
        shape.scale = scale
    else:
        shape.scale = math3d.vector(scale, scale, scale)


def get_camera_effect_scale(position, player_position):
    dist = (position - player_position).length
    meter_dist = dist / NEOX_UNIT_SCALE
    if meter_dist > 100:
        return 1
    else:
        if meter_dist > 10:
            return 2
        return 3


def model_outline(model, parent):
    if not model or not model.valid:
        return
    if not global_data.cam_lctarget:
        return
    driver_id = parent.ev_g_driver()
    if not (global_data.cam_lplayer and (global_data.cam_lplayer.id == driver_id or global_data.cam_lplayer.id == parent.id)):
        outline_by_camp(model, parent)
        outline_by_team(model, parent)


@execute_by_mode(True, game_mode_const.OutLine_ByCamp)
def outline_by_camp(model, parent):
    from logic.gutils import mecha_utils
    side = parent.ev_g_camp_show_side()
    mecha_utils.model_add_outline(model, side)


@execute_by_mode(True, game_mode_const.OutLine_ByTeam)
def outline_by_team(model, parent):
    from logic.gutils import mecha_utils
    if global_data.cam_lplayer.ev_g_is_groupmate(parent.id):
        side = game_mode_const.MY_SIDE
    else:
        side = game_mode_const.E_ONE_SIDE
    mecha_utils.model_add_outline(model, side)


def is_chunk_mesh--- This code section failed: ---

 924       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  STORE_FAST            1  'model_col_name'

 925      15  LOAD_FAST             1  'model_col_name'
          18  LOAD_ATTR             2  'find'
          21  LOAD_CONST            2  'chunk_mesh'
          24  CALL_FUNCTION_1       1 
          27  LOAD_CONST            3  -1
          30  COMPARE_OP            3  '!='
          33  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9


def dash_filtrate_hit(self_obj, target_obj):
    target_model = target_obj.ev_g_model()
    start_pos = None
    if target_model and target_model.valid:
        if target_obj.sd.ref_is_mecha:
            start_pos = target_model.position + math3d.vector(0, target_model.bounding_box.y * target_model.scale.y, 0)
        else:
            start_pos = target_model.center_w
    mecha_model = self_obj.ev_g_model()
    end_pos = None
    if mecha_model and mecha_model.valid:
        end_pos = mecha_model.position + math3d.vector(0, mecha_model.bounding_box.y * mecha_model.scale.y, 0)
    if not (start_pos and end_pos):
        return False
    else:
        scn = global_data.game_mgr.scene
        if not scn:
            return False
        check_group = collision_const.GROUP_SHOOTUNIT
        result = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, 65535, check_group, collision.INCLUDE_FILTER, True)
        if result and result[0]:
            for r in result[1]:
                group = r[4].group
                if bool(group & collision_const.GROUP_DYNAMIC_SHOOTUNIT) and group not in (collision_const.REGION_SCENE_GROUP, collision_const.REGION_SCENE_GROUP & ~GROUP_CAMERA_COLL):
                    continue
                return True

        return False


def apply_ragdoll_explosion(model, last_behit_info):
    if global_data.feature_mgr.is_supoort_ragdoll_normal_scale() and global_data.enable_ragdoll_explosion and model and model.physics:
        tech_pass_utils.hide_ragdoll_submesh(model)
        mask = (collision_const.GROUP_CHARACTER_EXCLUDE | collision_const.GROUP_GRENADE) & ~collision_const.GROUP_CAMERA_COLL
        group = collision_const.GROUP_CHARACTER_EXCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
        model.set_mask_and_group(mask, group)
        model.physics_enable = True
        attacker_pos = model.world_position
        hit_pos = model.world_position
        impulse_random_x = random.randint(*RAGDOLL_DIE_FORCE_RANGES[0])
        impulse_random_y = random.randint(*RAGDOLL_DIE_FORCE_RANGES[1])
        impulse_random_z = random.randint(*RAGDOLL_DIE_FORCE_RANGES[2])
        impulse = math3d.vector(impulse_random_x, impulse_random_y, impulse_random_z)
        if last_behit_info:
            attacker_id, weapon_id, final_hit_pos = last_behit_info
            if final_hit_pos is None:
                final_hit_pos = hit_pos
            attacker = EntityManager.getentity(attacker_id)
            if attacker and attacker.logic:
                attacker_pos = attacker.logic.ev_g_position()
            break_data_config = confmgr.get('break_data', str(weapon_id))
            if break_data_config:
                impulse_power = break_data_config.get('cBreakPower', 50)
            else:
                impulse_power = 50
            hit_dir = final_hit_pos - attacker_pos
            if not hit_dir.is_zero:
                hit_dir.normalize()
                impulse = hit_dir * impulse_power * 50
        print '!ryf ..................................impulse:%s' % (impulse,)
        model.physics.apply_impulse(impulse, math3d.vector(0, 0, 0), 0.0)
    return


def apply_ragdoll_custom_gravity(model):
    if not model:
        return
    if not model.physics_enable:
        return
    if not model.physics:
        return
    if not global_data.feature_mgr.is_supoort_ragdoll_normal_scale():
        return
    impulse = RAGDOLL_CUSTOM_GRAVITY_VAL


@fun_cache(128)
def get_ignore_rate(scn, model_col_name):
    model = scn.get_model(model_col_name)
    if model:
        model_name = model.get_attr('model_name')
        return confmgr.get('scene_model_inf', model_name, default={}).get('cIgnoreRate')
    else:
        return None


def clear_cache():
    is_break_obj_orig.cache_clear()
    break_obj_bullet_trigger.cache_clear()
    get_ignore_rate.cache_clear()


def scene_replace_res(path):
    from logic.gutils.tv_panel_utils import is_collaborate
    from logic.gcommon.common_const import ui_operation_const as uoc
    if is_collaborate():
        replace_res = confmgr.get('script_gim_ref').get('replace_res_HEA', {})
        path = path.replace('\\', '/')
        if path in replace_res:
            path = replace_res[path]
    if global_data.game_mode and global_data.game_mode.is_pve() and global_data.player and global_data.player.get_setting_2(uoc.WEAKEN_PVE_SFX_TYPE_8013):
        res_replace_conf = confmgr.get('res_replace_conf', 'Common', 'Content', default={})
        path = path.replace('\\', '/')
        if path in res_replace_conf:
            new_path = res_replace_conf[path].get('PVE')
            if new_path:
                path = new_path
    return path


def get_fireworks_path():
    return []
    from logic.gcommon import time_utility
    import six
    fireworks_config = confmgr.get('fireworks_config')
    now = time_utility.get_server_time()
    all_path = []
    for k, v in six.iteritems(fireworks_config):
        if k == '__doc__':
            continue
        begin_time = v.get('cBeginTime', 0)
        end_time = v.get('cEndTime', 0)
        if begin_time <= now <= end_time:
            all_path.append(v.get('cRes', []))

    return all_path