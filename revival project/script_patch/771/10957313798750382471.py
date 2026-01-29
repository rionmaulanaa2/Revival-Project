# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartThrowableManager.py
from __future__ import absolute_import
import six
import collision
from . import ScenePart
import weakref
import math3d
import world
import math
from mobile.common.EntityManager import EntityManager
from mobile.common.IdManager import IdManager
from logic.gcommon import time_utility as t_util
from logic.gcommon.common_const.weapon_const import WP_GRENADES_GUN, WP_TRACK_GUN, WP_NAVIGATE_GUN, WP_GRENADES_GROUP_GUN, WP_MULTI_PART_SHOOT, WP_CONVOLUTE_BIRD, WP_TOWER, WP_SUMMON_GRENADES_GUN, WP_OIL_BOTTLE, WP_TRACK_NAVIGATE_GUN, THROWABLE_TRIGGER_ATTACH, WP_RADIAL_GRENADE_GUN, WP_GRENADES_CROWD_GUN, WP_SWORD_LIGHT, WP_ATTACHABLE_RADIAL_GRENADES_GUN, WP_COMMON_RADIAL_GRENADES_GUN, WP_FLYING_ATTACH_GRENADES, WP_NAVIGATE_EXTRA_TRIGGER_EXPLODE_GRENADES_GUN, WP_TRACK_NAVIGATE_EXTRA_TRIGGER_EXPLODE_GRENADES_GUN, WP_NAVIGATE_SWORD_LIGHT, WP_EXTRA_TRIGGER_EXPLODE_GRENADES_GUN, WP_CLUSTER_GRENADE_GUN, WP_RAIN_GRENADE_GUN, WP_ARRAY_BARRAGE, WP_ROUND_BARRAGE, WP_COLUMN_BARRAGE, WP_SPHERE_BARRAGE, WP_INFINITE_RADIAL_GRENADES_GUN, WP_SHIRANUI_FAN_GRENADES_GUN, WP_CLAW_GRENADES_GUN
from logic.gcommon.common_const.collision_const import TERRAIN_GROUP, WOOD_GROUP, GROUP_CAN_SHOOT, WATER_GROUP, WATER_MASK, GROUP_CHARACTER_INCLUDE, BREAK_TRIGGER_TYPE_WEAPON
from logic.gutils.scene_utils import is_break_obj, process_hit_sfx, trigger_show_outline, get_camera_effect_scale
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gutils import team_utils
from logic.gutils.client_unit_tag_utils import register_unit_tag, preregistered_tags
from logic.gcommon.common_const.collision_const import WATER_GROUP, WATER_MASK
import common.cfg.confmgr as confmgr
from logic.gutils import weapon_skin_utils
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path
from logic.gcommon.cdata import status_config
from common.utils.sfxmgr import CREATE_SRC_OTHER_EXPLODE, CREATE_SRC_MINE_EXPLODE, CREATE_SRC_OTHER_EX_EXPLODE, CREATE_SRC_MINE_EX_EXPLODE
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
WATER_EXPLODE_SFX = 'effect/fx/robot/common/water_baozha.sfx'
WEIRD_MECHA_VEHICLE_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaTrans'))
IGNORE_CRATER_DISTANCE = 100 * NEOX_UNIT_SCALE
NEED_EX_SFX_INTENSITY_WEAPON_ID_SET = {
 802502, 802503, 801007, 801008, 801009, 801010, 801011}

class PartThrowableManager(ScenePart.ScenePart):
    SPECIAL_WEAPON_ITEM = {WP_GRENADES_GUN: 'Grenade',
       WP_GRENADES_GROUP_GUN: 'Grenade',
       WP_SUMMON_GRENADES_GUN: 'Grenade',
       WP_TRACK_GUN: 'TrackBullet',
       WP_NAVIGATE_GUN: 'NavigateBullet',
       WP_MULTI_PART_SHOOT: 'MulitPartGrenade',
       WP_CONVOLUTE_BIRD: 'ConvoluteBird',
       WP_TOWER: 'TowerBullet',
       WP_OIL_BOTTLE: 'OilBottleBullet',
       WP_TRACK_NAVIGATE_GUN: 'TrackNavigateBullet',
       WP_RADIAL_GRENADE_GUN: 'RadialGrenade',
       WP_GRENADES_CROWD_GUN: 'Grenade',
       WP_SWORD_LIGHT: 'SwordLight',
       WP_ATTACHABLE_RADIAL_GRENADES_GUN: 'AttachableRadialGrenade',
       WP_INFINITE_RADIAL_GRENADES_GUN: 'InfiniteRadialGrenade',
       WP_COMMON_RADIAL_GRENADES_GUN: 'CommonRadialGrenade',
       WP_NAVIGATE_EXTRA_TRIGGER_EXPLODE_GRENADES_GUN: 'NavigateExtraTriggerExplodeGrenade',
       WP_TRACK_NAVIGATE_EXTRA_TRIGGER_EXPLODE_GRENADES_GUN: 'TrackNavigateExtraTriggerExplodeGrenade',
       WP_FLYING_ATTACH_GRENADES: 'FlyingAttachGrenade',
       WP_NAVIGATE_SWORD_LIGHT: 'NavigateSwordLight',
       WP_EXTRA_TRIGGER_EXPLODE_GRENADES_GUN: 'ExtraTriggerExplodeGrenade',
       WP_CLUSTER_GRENADE_GUN: 'ClusterGrenade',
       WP_RAIN_GRENADE_GUN: 'RainGrenade',
       WP_ARRAY_BARRAGE: 'Barrage',
       WP_ROUND_BARRAGE: 'Barrage',
       WP_COLUMN_BARRAGE: 'Barrage',
       WP_SPHERE_BARRAGE: 'Barrage',
       WP_SHIRANUI_FAN_GRENADES_GUN: 'ShiranuiFanGrenade',
       WP_CLAW_GRENADES_GUN: 'ClawGrenade'
       }
    INIT_EVENT = {'scene_add_throw_item_event': 'add_throw_item',
       'scene_throw_item_explosion_event': 'throw_item_explosion',
       'scene_remove_throw_item_event': 'remove_throw_item',
       'scene_remove_throw_items_event': 'remove_throw_items',
       'scene_find_throw_item_event': 'find_throw_item',
       'scene_throw_item_stage_changed': 'on_throw_item_stage_changed',
       'net_reconnect_event': 'on_net_reconnect',
       'net_login_reconnect_event': 'on_net_reconnect',
       'display_quality_change': 'on_display_quality_change'
       }
    IGNORE_CRATER_TARGET_TAG_VALUE = register_unit_tag(('LMonster', 'LParadrop', 'LSnowman',
                                                        'LHittableBox', 'LPvePuzzle')) | preregistered_tags.HUMAN_TAG_VALUE | preregistered_tags.MECHA_VEHICLE_TAG_VALUE

    def __init__(self, scene, name):
        super(PartThrowableManager, self).__init__(scene, name, True)
        self.throw_items = {}
        self.explosive_sfx_info = {}
        from logic.vscene.global_display_setting import GlobalDisplaySeting
        gds = GlobalDisplaySeting()
        self.cur_display_quality = gds.get_actual_quality()

    def on_update(self, dt):
        throw_items = self.throw_items
        explosive_sfx_info = self.explosive_sfx_info
        if not throw_items and not explosive_sfx_info:
            return self.REMOVE_UPDATE_AFTER_LOOP
        else:
            now = t_util.time()
            wait_sfx = {}
            sfx_mgr = global_data.bullet_sfx_mgr
            for iid, sfx_list in six.iteritems(explosive_sfx_info):
                left_sfx = []
                for sfx_path, pos, normal, begin_time, life_time, scale, need_diff_process, create_src_type, weapon_id in sfx_list:
                    if now < begin_time:
                        left_sfx.append((sfx_path, pos, normal, begin_time, life_time, scale, need_diff_process, create_src_type, weapon_id))
                    else:
                        if check_need_ignore_effect_behind_camera(weapon_id, pos):
                            continue

                        def create_cb(sfx):
                            sfx_mgr.set_rotation_by_normal(sfx, normal)
                            sfx.scale = math3d.vector(scale, scale, scale)

                        ex_data = {'need_diff_process': need_diff_process}
                        sfx_mgr.create_sfx_in_scene(sfx_path, pos, duration=life_time / 1000.0, on_create_func=create_cb, ex_data=ex_data, int_check_type=create_src_type)

                if left_sfx:
                    wait_sfx[iid] = left_sfx

            self.explosive_sfx_info = wait_sfx
            explosive_items = {}
            explosive_info_items = {}
            for uniq_key, (eid, item_info) in six.iteritems(throw_items):
                explose_time = item_info['explose_time']
                if item_info['upload_pos'] and now >= explose_time - 0.5:
                    entity = EntityManager.getentity(eid)
                    if not entity or not entity.logic:
                        continue
                    model = entity.logic.ev_g_model()
                    if model is None:
                        continue
                    item_itype = confmgr.get('firearm_config', str(item_info['item_itype']), 'iKind')
                    grenade_conf = confmgr.get('grenade_config', str(item_info['item_itype']))
                    if item_itype in (WP_CLUSTER_GRENADE_GUN,):
                        continue
                    pos = model.position
                    item_info['upload_pos'] = False
                    upload_data = {}
                    upload_data['pos'] = (
                     pos.x, pos.y, pos.z)
                    mat = model.rotation_matrix
                    forward = mat.forward
                    up = mat.up
                    nmat = math3d.matrix.make_orient(forward, up)
                    upload_data['forward'] = (forward.x, forward.y, forward.z)
                    upload_data['up'] = (up.x, up.y, up.z)
                    upload_data['timeout'] = now
                    explosive_items[uniq_key] = upload_data
                    trigger_type = None
                    if grenade_conf:
                        trigger_type = grenade_conf['iTriggerType']
                    if item_itype == WP_GRENADES_GUN and trigger_type != THROWABLE_TRIGGER_ATTACH:
                        item_info['position'] = upload_data['pos']
                        explosive_info_items[uniq_key] = item_info

            if explosive_items and global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'update_explosive_item_info', (explosive_items,))
            for uniq_key, item_info in six.iteritems(explosive_info_items):
                self.throw_item_explosion({uniq_key: {'item': item_info}})

            return

    def add_throw_item(self, item_info):
        uniq_key = item_info['uniq_key']
        if uniq_key in self.throw_items or not global_data.battle:
            return
        item_info['upload_pos'] = True
        item_itype = confmgr.get('firearm_config', str(item_info['item_itype']), 'iKind')
        etype = self.SPECIAL_WEAPON_ITEM.get(item_itype, 'Grenade')
        if 'explose_time' not in item_info:
            if 'last_time' not in item_info:
                conf = confmgr.get('grenade_config', str(item_info['item_itype']))
                item_info['last_time'] = conf['fTimeFly']
            item_info['explose_time'] = item_info['last_time'] + item_info['begin_time']
        entity_id = IdManager.genid()
        entity = global_data.battle.create_entity(etype, entity_id, -1, item_info)
        self.throw_items[uniq_key] = (entity.id, item_info)
        self.need_update = True

    @staticmethod
    def check_show_explosive_effect--- This code section failed: ---

 232       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('game_mode_utils',)
           6  IMPORT_NAME           0  'logic.gutils'
           9  IMPORT_FROM           1  'game_mode_utils'
          12  STORE_FAST            1  'game_mode_utils'
          15  POP_TOP          

 233      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  BINARY_SUBSCR    
          20  STORE_FAST            2  'itype'

 234      23  LOAD_GLOBAL           2  'confmgr'
          26  LOAD_ATTR             3  'get'
          29  LOAD_CONST            4  'grenade_config'
          32  LOAD_GLOBAL           4  'str'
          35  LOAD_FAST             2  'itype'
          38  CALL_FUNCTION_1       1 
          41  LOAD_CONST            5  'default'
          44  BUILD_MAP_0           0 
          47  CALL_FUNCTION_258   258 
          50  STORE_FAST            3  'item_conf'

 235      53  LOAD_FAST             1  'game_mode_utils'
          56  LOAD_ATTR             5  'get_custom_param_by_mode'
          59  LOAD_FAST             3  'item_conf'
          62  LOAD_CONST            6  'fRange'
          65  CALL_FUNCTION_2       2 
          68  LOAD_GLOBAL           6  'NEOX_UNIT_SCALE'
          71  BINARY_MULTIPLY  
          72  STORE_FAST            4  'frange'

 237      75  LOAD_GLOBAL           7  'world'
          78  LOAD_ATTR             8  'get_active_scene'
          81  CALL_FUNCTION_0       0 
          84  STORE_FAST            5  'scn'

 238      87  LOAD_FAST             5  'scn'
          90  LOAD_ATTR             9  'get_com'
          93  LOAD_CONST            7  'PartCamera'
          96  CALL_FUNCTION_1       1 
          99  STORE_FAST            6  'part_camera'

 239     102  LOAD_FAST             6  'part_camera'
         105  UNARY_NOT        
         106  POP_JUMP_IF_TRUE    119  'to 119'
         109  LOAD_FAST             6  'part_camera'
         112  LOAD_ATTR            10  'cam'
         115  UNARY_NOT        
       116_0  COME_FROM                '106'
         116  POP_JUMP_IF_FALSE   123  'to 123'

 240     119  LOAD_GLOBAL          11  'False'
         122  RETURN_END_IF    
       123_0  COME_FROM                '116'

 241     123  LOAD_FAST             6  'part_camera'
         126  LOAD_ATTR            10  'cam'
         129  STORE_FAST            7  'camera'

 243     132  STORE_FAST            8  'pos'
         135  BINARY_SUBSCR    
         136  STORE_FAST            8  'pos'

 244     139  LOAD_GLOBAL          12  'math3d'
         142  LOAD_ATTR            13  'vector'
         145  LOAD_FAST             8  'pos'
         148  CALL_FUNCTION_VAR_0     0 
         151  STORE_FAST            8  'pos'

 245     154  LOAD_CONST            0  ''
         157  STORE_FAST            9  'self_pos'

 248     160  LOAD_GLOBAL          15  'global_data'
         163  LOAD_ATTR            16  'cam_lplayer'
         166  POP_JUMP_IF_FALSE   187  'to 187'

 249     169  LOAD_GLOBAL          15  'global_data'
         172  LOAD_ATTR            16  'cam_lplayer'
         175  LOAD_ATTR            17  'ev_g_position'
         178  CALL_FUNCTION_0       0 
         181  STORE_FAST            9  'self_pos'
         184  JUMP_FORWARD          0  'to 187'
       187_0  COME_FROM                '184'

 251     187  LOAD_FAST             9  'self_pos'
         190  POP_JUMP_IF_TRUE    205  'to 205'

 252     193  LOAD_FAST             7  'camera'
         196  LOAD_ATTR            18  'world_position'
         199  STORE_FAST            9  'self_pos'
         202  JUMP_FORWARD          0  'to 205'
       205_0  COME_FROM                '202'

 255     205  LOAD_FAST             8  'pos'
         208  LOAD_FAST             9  'self_pos'
         211  BINARY_SUBTRACT  
         212  STORE_FAST           10  'dvec'

 256     215  LOAD_FAST            10  'dvec'
         218  LOAD_ATTR            19  'length_sqr'
         221  LOAD_FAST             4  'frange'
         224  LOAD_FAST             4  'frange'
         227  BINARY_MULTIPLY  
         228  COMPARE_OP            5  '>='
         231  POP_JUMP_IF_FALSE   238  'to 238'

 257     234  LOAD_GLOBAL          11  'False'
         237  RETURN_END_IF    
       238_0  COME_FROM                '231'

 259     238  LOAD_GLOBAL          20  'True'
         241  RETURN_VALUE     

Parse error at or near `POP_TOP' instruction at offset 16

    @staticmethod
    def get_explode_sfx_info(item_id, pos, is_time_out, hit_target_id, item_info):
        skin_id = item_info.get('skin_id', None)
        shiny_weapon_id = item_info.get('shiny_weapon_id', None)
        faction_id = item_info.get('faction_id', None)
        accumulate_rate = item_info.get('accumulate_rate', 0.0)
        puzzle_id = item_info.get('puzzle_id', None)
        item_conf = confmgr.get('grenade_res_config', str(item_id))
        if not item_conf:
            return ([], 1.0, False)
        else:
            sfx_diff = item_conf.get('cCustomParam', {}).get('camp_diff', 0)
            need_diff_process = sfx_diff and faction_id is not None and global_data.cam_lplayer and faction_id != global_data.cam_lplayer.ev_g_camp_id()
            while True:
                if is_time_out:
                    sfx_list = item_conf['cTimeOutSfx']
                    if sfx_list:
                        break
                sfx_key = 'cSfx'
                if 'cAirSfx' in item_conf:
                    start_pos = math3d.vector(pos.x, pos.y + 1, pos.z)
                    end_pos = math3d.vector(pos.x, pos.y - 1, pos.z)
                    result = world.get_active_scene().scene_col.hit_by_ray(start_pos, end_pos, 0, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
                    if not result[0]:
                        sfx_key = 'cAirSfx'
                if puzzle_id:
                    sfx_list = weapon_skin_utils.get_pve_bomb_puzzle_sfx_path(puzzle_id)
                    if sfx_list:
                        break
                sfx_list = weapon_skin_utils.get_weapon_skin_grenade_weapon_sfx_path(skin_id, sfx_key)
                if sfx_list:
                    break
                sfx_list = get_mecha_skin_grenade_weapon_sfx_path(skin_id, shiny_weapon_id, item_id, sfx_key)
                if sfx_list:
                    break
                if sfx_key == 'cSfx':
                    if need_diff_process and type(sfx_diff) != int:
                        sfx_list = sfx_diff
                        need_diff_process = False
                        break
                sfx_list = item_conf[sfx_key]
                break

            sfx_scale = item_conf.get('fScale', 1.0)
            mainplayer = global_data.cam_lplayer
            if not mainplayer:
                return ([], 1.0, False)
            control_target = mainplayer.ev_g_control_target()
            control_target_id = 0
            if control_target and control_target.logic and control_target.logic.MASK & WEIRD_MECHA_VEHICLE_TAG_VALUE:
                control_target_id = control_target.id
            if hit_target_id:
                if control_target_id == hit_target_id:
                    if control_target.logic.sd.ref_in_open_aim:
                        main_open_aim_scale = item_conf.get('fMainOpenAimScale', 0)
                        if main_open_aim_scale:
                            sfx_scale = main_open_aim_scale
                    else:
                        main_normal_scale = item_conf.get('fMechaNormaScale', 0)
                        if main_normal_scale:
                            sfx_scale = main_normal_scale
                elif hit_target_id == mainplayer.id:
                    if mainplayer.ev_g_get_state(status_config.ST_AIM):
                        main_open_aim_scale = item_conf.get('fMainOpenAimScale', 0)
                        if main_open_aim_scale:
                            sfx_scale = main_open_aim_scale
                    else:
                        main_normal_scale = item_conf.get('fMainNormalScale', 0)
                        if main_normal_scale:
                            sfx_scale = main_normal_scale
            conf = confmgr.get('grenade_config', str(item_id), 'cCustomParam', default={})
            add_rate = conf.get('max_acc_add_range_rate', 0.0) * accumulate_rate
            sfx_scale *= 1.0 + add_rate
            return (
             sfx_list, sfx_scale, need_diff_process)

    @staticmethod
    def handle_explode_sound(item_id, owner_id, pos):
        item_conf = confmgr.get('grenade_res_config', str(item_id))
        if not item_conf:
            return
        sound_name = item_conf['cSoundName']
        if sound_name:
            if isinstance(sound_name, str):
                global_data.sound_mgr.play_sound_optimize('Play_grenade', owner_id, pos, ('grenade', sound_name))
            elif isinstance(sound_name, list) and sound_name[1] == 'nf':
                if len(sound_name) > 2 and sound_name[2]:
                    global_data.sound_mgr.play_sound(sound_name[0], pos, (sound_name[0], 'nf'))
                else:
                    global_data.sound_mgr.play_sound_optimize(sound_name[0], owner_id, pos, (sound_name[0], 'nf'))

    def find_throw_item(self, uniq_key):
        if self.throw_items:
            eid, tinfo = self.throw_items.get(uniq_key, (None, None))
            return (
             EntityManager.getentity(eid), tinfo)
        else:
            return (None, None)

    def on_throw_item_stage_changed(self, unique_key, stage, *args):
        if unique_key in self.throw_items:
            eid, _ = self.throw_items[unique_key]
            entity = global_data.battle.get_entity(eid)
            if entity and entity.logic:
                entity.logic.send_event('E_ON_THROWABLE_STAGE_CHANGED', stage, *args)

    def throw_item_explosion(self, explose_info, is_time_out=False):
        battle = global_data.battle
        if battle is None:
            return
        else:
            del_ids = []
            throw_items = self.throw_items
            now = t_util.time()
            for oid, einfo in six.iteritems(explose_info):
                item_info = einfo['item']
                if not item_info:
                    continue
                eid, tinfo = throw_items.get(oid, (None, None))
                if eid is not None:
                    battle.destroy_entity(eid)
                elif item_info['last_time'] > 0:
                    continue
                del_ids.append(oid)
                if item_info.get('ignore_bomb_sfx', False):
                    continue
                owner_id = item_info.get('owner_id', None)
                if owner_id:
                    if global_data.player and global_data.player.id == owner_id:
                        global_data.mecha and global_data.mecha.logic and global_data.mecha.logic.send_event('E_GRENADE_EXPLODED', item_info)
                    elif global_data.mecha and owner_id == global_data.mecha.id:
                        global_data.mecha.logic and global_data.mecha.logic.send_event('E_GRENADE_EXPLODED', item_info)
                hit_target_id = item_info.get('target', None)
                hit_target_player = None
                if hit_target_id:
                    hit_target_player = EntityManager.getentity(hit_target_id)
                if team_utils.ignore_expolosion(owner_id, hit_target_id):
                    continue
                if item_info.get('dummy_exploder', False):
                    continue
                pos = item_info['position']
                if pos is None:
                    continue
                pos = math3d.vector(*pos)
                use_rot_mat = item_info.get('use_rot_mat', 0)
                if use_rot_mat:
                    if tinfo:
                        up = tinfo.get('up', (0, 1, 0))
                        up = math3d.vector(*up)
                    else:
                        up = math3d.vector(0, 1, 0)
                    fdir = item_info.get('dir', (0, 0, 1))
                    fdir = math3d.vector(*fdir)
                else:
                    up = None
                    fdir = None
                impulse_power = item_info.get('impulse_power', 0.0)
                impulse_range = item_info.get('impulse_range', 0.0)
                group = item_info.get('cobj_group', 0)
                mask = item_info.get('cobj_mask', 0)
                normal = item_info.get('normal', (0, 1, 0))
                normal = math3d.vector(normal[0], normal[1], normal[2])
                model_col_name = item_info.get('model_col_name', '')
                is_ragdoll_part = item_info.get('is_ragdoll_part', None)
                item_id = item_info['item_itype']
                accumulate_rate = item_info.get('accumulate_rate', 0.0)
                self.handle_explode_sound(item_id, owner_id, pos)
                skin_id = item_info.get('skin_id', None)
                shiny_weapon_id = item_info.get('shiny_weapon_id', None)
                faction_id = item_info.get('faction_id', None)
                sfx_list, scale, need_diff_process = self.get_explode_sfx_info(item_id, pos, is_time_out, hit_target_id, item_info)
                if sfx_list:
                    self.add_explosion_sfx(oid, item_info, sfx_list, now, pos, normal, scale, need_diff_process)
                self.check_explode_camera_effect(einfo)
                self._trigger_boom_effect(item_id, group, mask, pos, normal, fdir, up, model_col_name, impulse_range, impulse_power, is_ragdoll_part, owner_id, hit_target_player)

            for oid in del_ids:
                if oid in throw_items:
                    del throw_items[oid]

            if not throw_items and not self.explosive_sfx_info:
                self.need_update = False
            return

    def check_explode_in_water(self, pos):
        return
        scn = world.get_active_scene()
        results = scn.scene_col.hit_by_ray(pos + math3d.vector(0, 999, 0), pos + math3d.vector(0, -999, 0), 0, WATER_MASK, WATER_GROUP, collision.EQUAL_FILTER, True, False)
        water_pos = None
        if results[0]:
            dis = 9999
            for col_info in results[1]:
                if (col_info[0] - pos).length < dis:
                    water_pos = col_info[0]

        if water_pos and water_pos.y > pos.y:
            return
        else:
            return

    def remove_throw_item(self, uniq_key):
        eid, tinfo = self.throw_items.pop(uniq_key, (None, None))
        if eid is not None:
            global_data.battle.destroy_entity(eid)
        return

    def remove_throw_items(self, uniq_key_list):
        for uniq_key in uniq_key_list:
            self.remove_throw_item(uniq_key)

    def _trigger_boom_effect(self, item_id, group, mask, pos, normal, forward_dir, up_dir, model_col_name, impulse_range, impulse_power, is_ragdoll_part, owner_id, hit_target_player):
        scn = world.get_active_scene()
        if not scn:
            return
        else:
            sfx_pos = pos
            sfx_normal = normal
            sfx_group = group
            sfx_mask = mask
            if group is None:
                ret_cobj, ret_pos, ret_normal = self._get_ray_check_collision_info(pos, pos - math3d.vector(0, 3 * NEOX_UNIT_SCALE, 0))
                if ret_cobj and ret_pos and ret_normal:
                    if ret_cobj.group:
                        sfx_group = ret_cobj.group
                        sfx_mask = ret_cobj.mask
                    sfx_pos = ret_pos
                    sfx_normal = ret_normal
            if self.cur_display_quality > 1 and not check_need_ignore_effect_behind_camera(item_id, pos) and (scn.active_camera.world_position - pos).length < IGNORE_CRATER_DISTANCE and (not hit_target_player or hit_target_player.logic.MASK & self.IGNORE_CRATER_TARGET_TAG_VALUE == 0):
                process_hit_sfx(item_id, sfx_group, sfx_mask, sfx_pos, sfx_normal, forward_dir, up_dir, model_col_name)
            self._trigger_outline_display(owner_id, item_id, pos)
            if not impulse_range > 0:
                return
            break_obj_list = []
            break_ragdoll_list = []
            result = self._get_explode_objs(pos, impulse_range)
            if result:
                for affect_cobj in result:
                    break_item_info = {'model_col_name': affect_cobj.model_col_name,'point': pos,
                       'normal': normal,
                       'power': impulse_power,
                       'break_type': BREAK_TRIGGER_TYPE_WEAPON,
                       'bullet_type': item_id
                       }
                    if is_break_obj(affect_cobj.model_col_name):
                        break_obj_list.append(break_item_info)
                    if affect_cobj.__class__.__name__ == 'rigid_body' or is_ragdoll_part:
                        break_ragdoll_list.append(break_item_info)

                if break_obj_list:
                    global_data.emgr.scene_add_break_objs.emit(break_obj_list, True)
                if break_ragdoll_list:
                    global_data.emgr.scene_handle_break_ragdoll_part.emit(break_ragdoll_list)
            return

    def _get_explode_objs(self, point, radius):
        scn = world.get_active_scene()
        check_obj = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius))
        check_obj.position = point
        result = scn.scene_col.static_test(check_obj, 65535, GROUP_CAN_SHOOT, collision.INCLUDE_FILTER)
        return result

    def _get_ray_check_collision_info(self, start_pos, end_pos):
        scn = world.get_active_scene()
        result = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, 65535, GROUP_CAN_SHOOT, collision.INCLUDE_FILTER, True)
        if result[0]:
            for col_info in result[1]:
                return (
                 col_info[4], col_info[0], col_info[1])

        return (None, None, None)

    @execute_by_mode(True, ())
    def _trigger_outline_display(self, owner_id, item_id, pos):
        return
        item_conf = confmgr.get('grenade_config', str(item_id), default={})
        frange = game_mode_utils.get_custom_param_by_mode(item_conf, 'fRange') * NEOX_UNIT_SCALE
        result = self._get_explode_objs(pos, frange)
        if result:
            for affect_cobj in result:
                res = global_data.emgr.scene_find_unit_event.emit(affect_cobj.cid)
                if res:
                    trigger_show_outline(res[0], owner_id)

    def add_explosion_sfx(self, oid, item_info, explose_sfx_path_list, now, pos, normal, scale, need_diff_process):
        if not explose_sfx_path_list:
            return
        else:
            if self.check_show_explosive_effect(item_info):
                sfx_path_list = explose_sfx_path_list
            else:
                sfx_path_list = explose_sfx_path_list[:1]
            is_simple_format = isinstance(sfx_path_list[0], str)
            is_mine = True
            if global_data.cam_lplayer:
                is_mine = item_info.get('owner_id', 0) == global_data.cam_lplayer.id
            if global_data.cam_lctarget:
                is_mine = is_mine or item_info.get('owner_id', 0) == global_data.cam_lctarget.id
            weapon_id = item_info.get('item_itype')
            shiny_weapon_id = item_info.get('shiny_weapon_id', None)
            if weapon_id in NEED_EX_SFX_INTENSITY_WEAPON_ID_SET and shiny_weapon_id:
                create_src_type = CREATE_SRC_MINE_EX_EXPLODE if is_mine else CREATE_SRC_OTHER_EX_EXPLODE
            else:
                create_src_type = CREATE_SRC_MINE_EXPLODE if is_mine else CREATE_SRC_OTHER_EXPLODE
            if is_simple_format:
                self.explosive_sfx_info[oid] = [(sfx_path_list[0], pos, normal, now - 0.5, 10000, scale, need_diff_process, create_src_type, weapon_id)]
            else:
                sfx_info = []
                for sfx_path in sfx_path_list:
                    if len(sfx_path) > 3:
                        sfx, begin, life_time, only_self_can_see = sfx_path
                        if only_self_can_see and global_data.cam_lplayer and item_info['owner_id'] != global_data.cam_lplayer.id:
                            continue
                    else:
                        sfx, begin, life_time = sfx_path
                    sfx_info.append((sfx, pos, normal, begin + now, life_time, scale, need_diff_process, create_src_type, weapon_id))

                self.explosive_sfx_info[oid] = sfx_info
            self.need_update = True
            return

    def on_net_reconnect(self, *args):
        self.throw_items = {}

    def on_exit(self, *args):
        self.throw_items = {}
        super(PartThrowableManager, self).on_exit()

    def check_explode_camera_effect(self, explose_info):
        item_info = explose_info.get('item')
        trigger_id = item_info.get('trigger_id')
        position = item_info.get('position')
        item_itype = item_info.get('item_itype')
        if position:
            position = math3d.vector(*position)
        is_camera_target = global_data.cam_lplayer and global_data.cam_lplayer.id == trigger_id
        is_ctraget = global_data.cam_lctarget and global_data.cam_lctarget.id == trigger_id
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(item_itype), {})
        trk_tag = trk_conf.get('explosion_trk_tag')
        if trk_tag:
            if is_camera_target or is_ctraget:
                player_position = global_data.cam_lctarget.ev_g_position()
                if player_position and position:
                    scale = get_camera_effect_scale(position, player_position)
                else:
                    scale = 1
                global_data.cam_lctarget.send_event('E_PLAY_CAMERA_TRK', trk_tag, None, {'rot_mul': scale})
        trk_tag = trk_conf.get('explosion_hit_trk_tag', None)
        if trk_tag:
            hit_target_id = item_info.get('target', None)
            if (is_camera_target or is_ctraget) and hit_target_id:
                player_position = global_data.cam_lctarget.ev_g_position()
                if player_position and position:
                    scale = get_camera_effect_scale(position, player_position)
                else:
                    scale = 1
                global_data.cam_lctarget.send_event('E_PLAY_CAMERA_TRK', trk_tag, None, {'rot_mul': scale})
        return

    def on_display_quality_change(self, quality):
        self.cur_display_quality = quality