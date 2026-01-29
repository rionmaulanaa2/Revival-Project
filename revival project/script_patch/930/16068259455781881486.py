# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_field/ComFogFieldLogic.py
from __future__ import absolute_import
import six
import world
import math3d
import collision
import render
import game3d
import random
from math import sqrt, pi, sin, cos, tan
from common.utilities import lerp
from common.cfg import confmgr
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE, GROUP_DYNAMIC_SHOOTUNIT, TERRAIN_MASK
from common.utils.timer import CLOCK, RELEASE
from mobile.common.EntityManager import EntityManager
from common.framework import Functor
SFX_COUNT = 3
BORDER_RATE = 0.7
RAND_RANGE = (0.2, 0.8)
BORDER_SFX_CNT = 30
INSIDE_SFX_CNT = 50
SIZE_RAND_RANGE = (0.8, 1.2)
FOG_FLOAT_SPEED_RANGE = (0.8, 1.2)
FOG_TECH = render.technique(1, 'shader/g93shader/vfx_particle_fog.fx', 'TShader')
FOG_VAR_HASH = {'Tex0': game3d.calc_string_hash('Tex0'),
   '_EmissionColor': game3d.calc_string_hash('_EmissionColor'),
   '_SprTexRowCnt': game3d.calc_string_hash('_SprTexRowCnt'),
   '_SprTexSpeed': game3d.calc_string_hash('_SprTexSpeed')
   }
SFX_HEIGHT = 100
SFX_INTER = 50
RAY_INTER = 5 * NEOX_UNIT_SCALE
PLANE_HEIGHT = 0.5 * NEOX_UNIT_SCALE
RAY_COUNT = 10
RAY_THETA = 2.0 * pi / RAY_COUNT
TAN_THETA = tan(RAY_THETA)
RAY_DIR_LIST = [
 math3d.vector(0, 0, 1)]
for i in range(1, RAY_COUNT):
    theta = RAY_THETA * i
    ray_vec = math3d.vector(sin(theta), 0, cos(theta))
    RAY_DIR_LIST.append(ray_vec)

def get_related_ray_idx(center_to_pos_dir):
    if center_to_pos_dir.is_zero:
        return (None, None)
    else:
        if center_to_pos_dir.x == 0:
            return (0 if center_to_pos_dir.z > 0 else RAY_COUNT // 2, None)
        if center_to_pos_dir.x > 0:
            if center_to_pos_dir.z > RAY_DIR_LIST[1].z:
                return (0, 1)
            if center_to_pos_dir.z < RAY_DIR_LIST[RAY_COUNT // 2 - 1].z:
                return (RAY_COUNT // 2 - 1, RAY_COUNT // 2)
            for idx in range(1, RAY_COUNT // 2):
                if center_to_pos_dir.z == RAY_DIR_LIST[idx].z:
                    return (idx, None)
                if center_to_pos_dir.z > RAY_DIR_LIST[idx].z:
                    return (idx - 1, idx)

        if center_to_pos_dir.x < 0:
            if center_to_pos_dir.z > RAY_DIR_LIST[-1].z:
                return (0, RAY_COUNT - 1)
            if center_to_pos_dir.z < RAY_DIR_LIST[RAY_COUNT // 2 + 1].z:
                return (RAY_COUNT // 2, RAY_COUNT // 2 + 1)
            for idx in range(RAY_COUNT - 1, RAY_COUNT // 2, -1):
                if center_to_pos_dir.z == RAY_DIR_LIST[idx].z:
                    return (idx, None)
                if center_to_pos_dir.z > RAY_DIR_LIST[idx].z:
                    return (idx, idx + 1)

        return None


def ray_check_from_to(from_pos, to_pos):
    scn = global_data.game_mgr.scene
    if not scn:
        return
    else:
        result = scn.scene_col.hit_by_ray(from_pos, to_pos, -1, GROUP_DEFAULT_VISIBLE, TERRAIN_MASK, collision.EQUAL_FILTER, False)
        if result[0]:
            return (result[3], result[1])
        return (
         1.0, to_pos)


def get_nearby_enemy_unit(pos, radius):
    scn = global_data.game_mgr.scene
    if not scn:
        return
    check_obj = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius))
    check_obj.position = pos
    result = scn.scene_col.static_test(check_obj, 65535, GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER)
    if not result:
        return
    units = []
    for cobj in result:
        cid = cobj.cid
        unit_obj = global_data.emgr.scene_find_unit_event.emit(cid)[0]
        if not unit_obj or unit_obj in units:
            continue
        units.append(unit_obj)

    return units


def create_pri(x, y, tex_info):
    pri = world.primitives(world.get_active_scene())
    r = random.random()
    pri.create_poly4([
     (
      (
       1.0 * x, 1.0 * y, 0.0, 1.0, 1.0, r, 1.0, 1.0),
      (
       1.0 * x, -1.0 * y, 0.0, 1.0, 0.0, r, 1.0, 1.0),
      (
       -1.0 * x, -1.0 * y, 0.0, 0.0, 0.0, r, 1.0, 1.0),
      (
       -1.0 * x, 1.0 * y, 0.0, 0.0, 1.0, r, 1.0, 1.0),
      16777215)])
    mat = render.material(FOG_TECH)
    pri.set_material(mat)
    pri.render_group = world.RENDER_GROUP_TRANSPARENT
    for var_name, value in six.iteritems(tex_info):
        if var_name == 'Tex0':
            mat.set_texture(FOG_VAR_HASH[var_name], var_name, value)
        else:
            mat.set_var(FOG_VAR_HASH[var_name], var_name, value)

    mat.transparent_mode = render.TRANSPARENT_MODE_ALPHA_R_Z
    return pri


class ComFogFieldLogic(UnitCom):
    BIND_EVENT = {'E_ON_AGENT': 'on_begin_agent'
       }

    def __init__(self):
        super(ComFogFieldLogic, self).__init__(True)

    def init_from_dict(self, unit_obj, bdict):
        super(ComFogFieldLogic, self).init_from_dict(unit_obj, bdict)
        self.agent_id = None
        self._create_id = bdict['creator_id']
        field_inf = confmgr.get('field_data', str(bdict['npc_id']))
        custom_param = field_inf['cCustomParam'] or {}
        self.is_mini_fog = custom_param.get('mini_fog', 0)
        height = bdict['height']
        self._pos = math3d.vector(*bdict['position'])
        up_frac, _ = ray_check_from_to(self._pos, self._pos + math3d.vector(0, height, 0))
        down_frac, _ = ray_check_from_to(self._pos, self._pos - math3d.vector(0, height, 0))
        down_frac = min(0.5, max(0.0, down_frac))
        self._pos.y -= down_frac * height
        self.total_height = height * min(up_frac + down_frac, 1.0)
        self.half_height = self.total_height * 0.5
        self.radius = bdict['fog_range'] * NEOX_UNIT_SCALE
        self.smoke_sfx_path = custom_param.get('smoke_sfx', 'effect/fx/mecha/8034/8034_smoke.sfx')
        self.smoke_sfx_path_enemy = custom_param.get('smoke_sfx_enemy', 'effect/fx/mecha/8034/8034_smoke_enemy.sfx')
        self.tex_info = {'Tex0': custom_param.get('tex_path', 'effect/textures/smoke/smoke14.tga'),
           '_SprTexRowCnt': float(custom_param.get('tex_row_cnt', 4.0)),
           '_SprTexSpeed': float(custom_param.get('tex_speed', 1.5))
           }
        sound_event = custom_param.get('sound_event', '')
        if sound_event:
            self.send_event('E_INIT_FIELD_SOUND', sound_event, self._pos)
            self.sound_id = global_data.sound_mgr.play_event(sound_event, self._pos)
        self.inside_units = set()
        self.need_do_init_upload = False
        self.init_fog_border_data()
        if global_data.show_fog_border:
            self.create_border()
        self.sfx_id_list = [ {'center': None,'border': None} for i in range(RAY_COUNT) ]
        self.center_sfx_id = []
        self.pri_list = []
        self.cur_sfx_is_campmate = None
        self.center_sfx_scale = 5
        self.create_fog_sfx()
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': lambda *args: self.create_fog_sfx()
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_fog_border_data(self):
        if self.is_mini_fog:
            return
        self.border_data = []
        for ray_dir in RAY_DIR_LIST:
            border_data = []
            self.border_data.append(border_data)
            y_offset = 0
            cur_height = 0
            while y_offset <= self.total_height:
                ray_start = self._pos + math3d.vector(0, y_offset, 0)
                frac_h, border_bot = ray_check_from_to(ray_start, ray_start + ray_dir * self.radius)
                dist = self.radius * frac_h
                if cur_height >= y_offset and border_data and border_data[-1][0] >= dist:
                    y_max = cur_height
                    dist = border_data[-1][0]
                else:
                    frac_v_u = 0.0
                    up_dist = self.total_height - y_offset
                    if up_dist > 0.0:
                        frac_v_u, border_top = ray_check_from_to(border_bot, border_bot + math3d.vector(0, up_dist, 0))
                    frac_v_d = 0.0
                    if y_offset > 0:
                        frac_v_d, border_bot = ray_check_from_to(border_bot, border_bot - math3d.vector(0, y_offset, 0))
                    y_min = max(0.0, y_offset * (1.0 - frac_v_d))
                    y_max = y_offset + frac_v_u * up_dist
                    if not border_data or border_data[-1][1] < y_min:
                        border_data.append([dist, y_min])
                    else:
                        i = 0
                        inserted = False
                        while True:
                            if i >= len(border_data):
                                break
                            d, h = border_data[i]
                            if h >= y_min:
                                if not inserted:
                                    border_data.insert(i, [dist, y_min])
                                    inserted = True
                                elif d < dist:
                                    border_data[i][0] = dist
                                    last_d, last_h = border_data[i - 1]
                                    if last_d <= dist:
                                        del border_data[i]
                                        i -= 1
                            i += 1

                if y_offset == self.total_height:
                    break
                cur_height = y_max
                if dist >= self.radius:
                    y_offset = y_max + 1
                    if y_offset >= self.total_height:
                        break
                else:
                    y_offset += PLANE_HEIGHT
                    if self.total_height < y_offset or self.total_height - y_offset < PLANE_HEIGHT * 0.5:
                        y_offset = self.total_height

    def create_border--- This code section failed: ---

 270       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'enumerate'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 271      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 272      16  BUILD_LIST_0          0 
          19  STORE_FAST            1  'pt_list'

 273      22  SETUP_LOOP          438  'to 463'
          25  LOAD_GLOBAL           1  'enumerate'
          28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             2  'border_data'
          34  CALL_FUNCTION_1       1 
          37  GET_ITER         
          38  FOR_ITER            421  'to 462'
          41  UNPACK_SEQUENCE_2     2 
          44  STORE_FAST            2  'idx'
          47  STORE_FAST            3  'border_data'

 274      50  LOAD_GLOBAL           3  'RAY_DIR_LIST'
          53  LOAD_FAST             2  'idx'
          56  BINARY_SUBSCR    
          57  STORE_FAST            4  'ray_dir'

 275      60  LOAD_FAST             1  'pt_list'
          63  LOAD_ATTR             4  'append'
          66  LOAD_FAST             0  'self'
          69  LOAD_ATTR             5  '_pos'
          72  LOAD_ATTR             6  'x'
          75  LOAD_FAST             0  'self'
          78  LOAD_ATTR             5  '_pos'
          81  LOAD_ATTR             7  'y'
          84  LOAD_FAST             0  'self'
          87  LOAD_ATTR             5  '_pos'
          90  LOAD_ATTR             8  'z'
          93  LOAD_CONST            2  16711680
          96  BUILD_TUPLE_4         4 
          99  CALL_FUNCTION_1       1 
         102  POP_TOP          

 276     103  SETUP_LOOP          207  'to 313'
         106  LOAD_GLOBAL           1  'enumerate'
         109  LOAD_FAST             3  'border_data'
         112  CALL_FUNCTION_1       1 
         115  GET_ITER         
         116  FOR_ITER            193  'to 312'
         119  UNPACK_SEQUENCE_2     2 
         122  STORE_FAST            5  'i'
         125  UNPACK_SEQUENCE_2     2 
         128  STORE_FAST            6  'dist'
         131  STORE_FAST            7  'height'

 277     134  LOAD_FAST             5  'i'
         137  LOAD_CONST            3  ''
         140  COMPARE_OP            4  '>'
         143  POP_JUMP_IF_FALSE   239  'to 239'

 278     146  LOAD_FAST             3  'border_data'
         149  LOAD_FAST             5  'i'
         152  LOAD_CONST            4  1
         155  BINARY_SUBTRACT  
         156  BINARY_SUBSCR    
         157  UNPACK_SEQUENCE_2     2 
         160  STORE_FAST            8  'last_dist'
         163  STORE_FAST            9  '_'

 279     166  LOAD_FAST             0  'self'
         169  LOAD_ATTR             5  '_pos'
         172  LOAD_GLOBAL           9  'math3d'
         175  LOAD_ATTR            10  'vector'
         178  LOAD_CONST            3  ''
         181  LOAD_FAST             7  'height'
         184  LOAD_CONST            3  ''
         187  CALL_FUNCTION_3       3 
         190  BINARY_ADD       
         191  LOAD_FAST             4  'ray_dir'
         194  LOAD_FAST             8  'last_dist'
         197  BINARY_MULTIPLY  
         198  BINARY_ADD       
         199  STORE_FAST           10  'pt'

 280     202  LOAD_FAST             1  'pt_list'
         205  LOAD_ATTR             4  'append'
         208  LOAD_FAST            10  'pt'
         211  LOAD_ATTR             6  'x'
         214  LOAD_FAST            10  'pt'
         217  LOAD_ATTR             7  'y'
         220  LOAD_FAST            10  'pt'
         223  LOAD_ATTR             8  'z'
         226  LOAD_CONST            2  16711680
         229  BUILD_TUPLE_4         4 
         232  CALL_FUNCTION_1       1 
         235  POP_TOP          
         236  JUMP_FORWARD          0  'to 239'
       239_0  COME_FROM                '236'

 281     239  LOAD_FAST             0  'self'
         242  LOAD_ATTR             5  '_pos'
         245  LOAD_GLOBAL           9  'math3d'
         248  LOAD_ATTR            10  'vector'
         251  LOAD_CONST            3  ''
         254  LOAD_FAST             7  'height'
         257  LOAD_CONST            3  ''
         260  CALL_FUNCTION_3       3 
         263  BINARY_ADD       
         264  LOAD_FAST             4  'ray_dir'
         267  LOAD_FAST             6  'dist'
         270  BINARY_MULTIPLY  
         271  BINARY_ADD       
         272  STORE_FAST           10  'pt'

 282     275  LOAD_FAST             1  'pt_list'
         278  LOAD_ATTR             4  'append'
         281  LOAD_FAST            10  'pt'
         284  LOAD_ATTR             6  'x'
         287  LOAD_FAST            10  'pt'
         290  LOAD_ATTR             7  'y'
         293  LOAD_FAST            10  'pt'
         296  LOAD_ATTR             8  'z'
         299  LOAD_CONST            2  16711680
         302  BUILD_TUPLE_4         4 
         305  CALL_FUNCTION_1       1 
         308  POP_TOP          
         309  JUMP_BACK           116  'to 116'
         312  POP_BLOCK        
       313_0  COME_FROM                '103'

 283     313  LOAD_FAST             0  'self'
         316  LOAD_ATTR             5  '_pos'
         319  LOAD_GLOBAL           9  'math3d'
         322  LOAD_ATTR            10  'vector'
         325  LOAD_CONST            3  ''
         328  LOAD_FAST             0  'self'
         331  LOAD_ATTR            11  'total_height'
         334  LOAD_CONST            3  ''
         337  CALL_FUNCTION_3       3 
         340  BINARY_ADD       
         341  LOAD_FAST             4  'ray_dir'
         344  LOAD_FAST             3  'border_data'
         347  LOAD_CONST            5  -1
         350  BINARY_SUBSCR    
         351  LOAD_CONST            3  ''
         354  BINARY_SUBSCR    
         355  BINARY_MULTIPLY  
         356  BINARY_ADD       
         357  STORE_FAST           10  'pt'

 284     360  LOAD_FAST             1  'pt_list'
         363  LOAD_ATTR             4  'append'
         366  LOAD_FAST            10  'pt'
         369  LOAD_ATTR             6  'x'
         372  LOAD_FAST            10  'pt'
         375  LOAD_ATTR             7  'y'
         378  LOAD_FAST            10  'pt'
         381  LOAD_ATTR             8  'z'
         384  LOAD_CONST            2  16711680
         387  BUILD_TUPLE_4         4 
         390  CALL_FUNCTION_1       1 
         393  POP_TOP          

 285     394  LOAD_FAST             0  'self'
         397  LOAD_ATTR             5  '_pos'
         400  LOAD_GLOBAL           9  'math3d'
         403  LOAD_ATTR            10  'vector'
         406  LOAD_CONST            3  ''
         409  LOAD_FAST             0  'self'
         412  LOAD_ATTR            11  'total_height'
         415  LOAD_CONST            3  ''
         418  CALL_FUNCTION_3       3 
         421  BINARY_ADD       
         422  STORE_FAST           10  'pt'

 286     425  LOAD_FAST             1  'pt_list'
         428  LOAD_ATTR             4  'append'
         431  LOAD_FAST            10  'pt'
         434  LOAD_ATTR             6  'x'
         437  LOAD_FAST            10  'pt'
         440  LOAD_ATTR             7  'y'
         443  LOAD_FAST            10  'pt'
         446  LOAD_ATTR             8  'z'
         449  LOAD_CONST            2  16711680
         452  BUILD_TUPLE_4         4 
         455  CALL_FUNCTION_1       1 
         458  POP_TOP          
         459  JUMP_BACK            38  'to 38'
         462  POP_BLOCK        
       463_0  COME_FROM                '22'

 287     463  LOAD_GLOBAL          12  'world'
         466  LOAD_ATTR            13  'primitives'
         469  LOAD_GLOBAL          12  'world'
         472  LOAD_ATTR            14  'get_active_scene'
         475  CALL_FUNCTION_0       0 
         478  CALL_FUNCTION_1       1 
         481  LOAD_FAST             0  'self'
         484  STORE_ATTR           15  'border_pri'

 288     487  LOAD_FAST             0  'self'
         490  LOAD_ATTR            15  'border_pri'
         493  LOAD_ATTR            16  'create_line_strip'
         496  LOAD_FAST             1  'pt_list'
         499  CALL_FUNCTION_1       1 
         502  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def create_fog_sfx(self):
        if not self._is_valid or self.is_mini_fog:
            return
        last_dir_create_center = False
        center_pos = self._pos + math3d.vector(0, self.half_height, 0)
        for ray_idx, ray in enumerate(RAY_DIR_LIST):
            dist = self.get_dist_with_dir_idx(ray_idx, self.half_height)
            if dist < self.radius * 0.3:
                last_dir_create_center = False
                continue
            w = self.radius * 0.6
            if not last_dir_create_center:
                w = min(dist, self.radius * 0.6) * lerp(0.9, 1.1, random.random())
                pri_pos = center_pos + ray * w * 0.5
                pri = create_pri(w, self.total_height, self.tex_info)
                self.pri_list.append(pri)
                pri.position = pri_pos
            last_dir_create_center = not last_dir_create_center
            if dist >= self.radius * 0.8:
                w2 = (dist - w) * lerp(0.9, 1.1, random.random())
                pri_pos = center_pos + ray * (w + w2 * 0.5) * lerp(0.7, 0.9, random.random())
                pri_pos = center_pos + ray * w * 0.5
                pri = create_pri(w2, self.total_height, self.tex_info)
                self.pri_list.append(pri)
                pri.position = pri_pos

        self.refresh_fog_color()

    def refresh_fog_color(self):
        for pri in self.pri_list:
            mat = pri.get_material()
            mat.set_var(FOG_VAR_HASH['_EmissionColor'], '_EmissionColor', (0.9, 0.15,
                                                                           0.0, 0.08) if self.is_campmate() else (0.9,
                                                                                                                  0.0,
                                                                                                                  0.0,
                                                                                                                  0.08))

    def is_campmate(self):
        if not global_data.cam_lplayer:
            return False
        creator = EntityManager.getentity(self._create_id)
        if not (creator and creator.logic):
            return False
        return global_data.cam_lplayer.ev_g_is_campmate(creator.logic.ev_g_camp_id())

    def tick(self, delta):
        self.update_sfx_visible()
        self.check_inside_unit()

    def update_sfx_visible(self):
        if not global_data.cam_world_transform:
            return
        cam_pos = global_data.cam_world_transform.translation
        center_to_cam = cam_pos - self._pos
        y_diff = abs(center_to_cam.y - self.half_height)
        h_dist = center_to_cam.length
        if h_dist > 0.1:
            center_to_cam.normalize()
        near_fog = h_dist < 50 * NEOX_UNIT_SCALE
        in_center = h_dist < self.radius * 0.3
        y_diff_max = 20 * NEOX_UNIT_SCALE
        show_all = near_fog and y_diff > self.half_height or y_diff > y_diff_max
        far_dot_threshold = min(1, max(0.2, (y_diff - self.half_height) / y_diff_max))
        for ray_idx, sfx_id_dict in enumerate(self.sfx_id_list):
            if show_all:
                show_center = show_border = True
            elif in_center:
                show_center = True
                show_border = False
            else:
                ray = RAY_DIR_LIST[ray_idx]
                dot_val = ray.dot(center_to_cam)
                show_center = dot_val > 0
                show_border = dot_val > 0 if near_fog else abs(dot_val) < far_dot_threshold
            center_sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id_dict['center'])
            if center_sfx and center_sfx.valid:
                center_sfx.visible = show_center
            border_sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id_dict['border'])
            if border_sfx and border_sfx.valid:
                border_sfx.visible = show_border

    def check_inside_unit(self):
        if not self.agent_id:
            return
        pos = self._pos
        nearby_units = get_nearby_enemy_unit(pos, self.radius) or []
        valid_units = set()
        for unit in nearby_units:
            if self.is_unit_inside(unit):
                valid_units.add(unit)

        if self.need_do_init_upload:
            self.send_event('E_CALL_SYNC_METHOD', 'begin_agent_fog', (self.agent_id, {'affect_entities': [ vu.id for vu in valid_units ]}), True)
            self.need_do_init_upload = False
        else:
            new_enter_units = valid_units - self.inside_units
            for unit in new_enter_units:
                self.send_event('E_CALL_SYNC_METHOD', 'client_sync_enter_fog', (self.agent_id, unit.id), True)

        exit_units = self.inside_units - valid_units
        for unit in exit_units:
            self.send_event('E_CALL_SYNC_METHOD', 'client_sync_leave_fog', (self.agent_id, unit.id), True)

        self.inside_units = valid_units

    def get_dist_with_dir_idx(self, dir_idx, height):
        if len(self.border_data) <= dir_idx or len(self.border_data[dir_idx]) == 0:
            return 0
        for i in range(len(self.border_data[dir_idx]) - 1, -1, -1):
            dist, y_min = self.border_data[dir_idx][i]
            if y_min > height:
                continue
            return dist

        return self.border_data[dir_idx][0][0]

    def is_unit_inside(self, unit):
        model = unit.ev_g_model()
        if not model:
            return False
        else:
            is_human = not unit.sd.ref_is_mecha
            mat = None
            if is_human and model.has_socket('neck'):
                mat = model.get_socket_matrix('neck', world.SPACE_TYPE_WORLD)
            else:
                if model.has_socket('part_point1'):
                    mat = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
                if mat:
                    unit_pos = mat.translation
                else:
                    unit_pos = unit.ev_g_model_position() + math3d.vector(0, 0.5 * NEOX_UNIT_SCALE, 0)
                center_unit_dir = unit_pos - self._pos
                unit_pos_y = center_unit_dir.y
                if unit_pos_y < 0 or unit_pos_y > self.total_height:
                    return False
                center_unit_dir.y = 0
                center_unit_dist = center_unit_dir.length
                if center_unit_dist > self.radius:
                    return False
                if self.is_mini_fog:
                    return True
                if center_unit_dist < 0.1:
                    return True
                if center_unit_dir.is_zero:
                    return True
            center_unit_dir.normalize()
            test_dir_idx1, test_dir_idx2 = get_related_ray_idx(center_unit_dir)
            if test_dir_idx2 is None:
                unit_valid = test_dir_idx1 is None or self.get_dist_with_dir_idx(test_dir_idx1, unit_pos_y) >= center_unit_dist
            else:
                dist1 = self.get_dist_with_dir_idx(test_dir_idx1, unit_pos_y)
                dist2 = self.get_dist_with_dir_idx(test_dir_idx2, unit_pos_y)
                ray_dir1 = RAY_DIR_LIST[test_dir_idx1]
                cos_alpha = min(max(ray_dir1.dot(center_unit_dir), 0), 1)
                tan_alpha = sqrt(1 - cos_alpha ** 2) / cos_alpha
                blend = tan_alpha / TAN_THETA
                dist = lerp(dist1, dist2, blend)
                unit_valid = dist >= center_unit_dist
            return unit_valid

    def on_begin_agent(self):
        self.need_do_init_upload = True
        self.agent_id = global_data.player.logic.id if global_data.player and global_data.player.logic else None
        return

    def destroy--- This code section failed: ---

 487       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'ComFogFieldLogic'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'destroy'
          15  CALL_FUNCTION_0       0 
          18  POP_TOP          

 512      19  SETUP_LOOP           45  'to 67'
          22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             3  'pri_list'
          28  GET_ITER         
          29  FOR_ITER             34  'to 66'
          32  STORE_FAST            1  'pri'

 513      35  LOAD_FAST             1  'pri'
          38  POP_JUMP_IF_FALSE    29  'to 29'
          41  LOAD_FAST             1  'pri'
          44  LOAD_ATTR             4  'valid'
        47_0  COME_FROM                '38'
          47  POP_JUMP_IF_FALSE    29  'to 29'

 514      50  LOAD_FAST             1  'pri'
          53  LOAD_ATTR             2  'destroy'
          56  CALL_FUNCTION_0       0 
          59  POP_TOP          
          60  JUMP_BACK            29  'to 29'
          63  JUMP_BACK            29  'to 29'
          66  POP_BLOCK        
        67_0  COME_FROM                '19'

 515      67  LOAD_CONST            0  ''
          70  LOAD_FAST             0  'self'
          73  STORE_ATTR            3  'pri_list'

 517      76  LOAD_GLOBAL           6  'getattr'
          79  LOAD_GLOBAL           1  'ComFogFieldLogic'
          82  LOAD_CONST            0  ''
          85  CALL_FUNCTION_3       3 
          88  STORE_FAST            2  'border_pri'

 518      91  LOAD_FAST             2  'border_pri'
          94  POP_JUMP_IF_FALSE   119  'to 119'

 519      97  LOAD_FAST             2  'border_pri'
         100  LOAD_ATTR             2  'destroy'
         103  CALL_FUNCTION_0       0 
         106  POP_TOP          

 520     107  LOAD_CONST            0  ''
         110  LOAD_FAST             0  'self'
         113  STORE_ATTR            7  'border_pri'
         116  JUMP_FORWARD          0  'to 119'
       119_0  COME_FROM                '116'

 522     119  LOAD_GLOBAL           6  'getattr'
         122  LOAD_GLOBAL           2  'destroy'
         125  LOAD_CONST            0  ''
         128  CALL_FUNCTION_3       3 
         131  POP_JUMP_IF_FALSE   165  'to 165'

 523     134  LOAD_GLOBAL           8  'global_data'
         137  LOAD_ATTR             9  'sound_mgr'
         140  LOAD_ATTR            10  'stop_playing_id'
         143  LOAD_FAST             0  'self'
         146  LOAD_ATTR            11  'sound_id'
         149  CALL_FUNCTION_1       1 
         152  POP_TOP          

 524     153  LOAD_CONST            0  ''
         156  LOAD_FAST             0  'self'
         159  STORE_ATTR           11  'sound_id'
         162  JUMP_FORWARD          0  'to 165'
       165_0  COME_FROM                '162'

 526     165  LOAD_FAST             0  'self'
         168  LOAD_ATTR            12  'process_event'
         171  LOAD_GLOBAL          13  'False'
         174  CALL_FUNCTION_1       1 
         177  POP_TOP          
         178  LOAD_CONST            0  ''
         181  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 85