# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanHurtAppearance.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from ..UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, TERRAIN_GROUP, WATER_MASK, WATER_GROUP, WOOD_GROUP, ROAD_GROUP, ICE_GROUP
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.screen_effect_utils import create_screen_effect_directly
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_const import weapon_const
from logic.gcommon.common_const.weapon_const import BULLET_HOLE_LIFE_TIME
from common.cfg import confmgr
from logic.gcommon.common_const.battle_const import KEY_WATER_POS, KEY_AIRWALL_POS, KEY_AIRWALL_NORMAL
from logic.gcommon.common_const.buff_const import SFX_TARGET_TYPE_TO_STR, SFX_VIS_SKATEBOARD
from logic.units import LMechaTrans
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from common.utils.timer import CLOCK
from logic.gcommon.common_const.battle_const import FIGHT_INJ_SHOOT, FIGHT_INJ_BOMB
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.const import HIT_PART_SHIELD
from logic.gutils.sfx_utils import get_sfx_scale_by_length_spr, get_sfx_scale_by_length_human_spr
from logic.gcommon.cdata import status_config as st_const
from common.utils.sfxmgr import CREATE_SRC_MINE_HIT, CREATE_SRC_OTHER_HIT, CREATE_SRC_SIMPLE, CREATE_SRC_MINE_RAY_GUN_CRATER, CREATE_SRC_ONE
from logic.gutils.firearm_sfx_mapping_utils import check_sfx_mapping_initialized, decode_sfx_info
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
from logic.gutils.client_unit_tag_utils import register_unit_tag, preregistered_tags
from logic.gutils import scene_utils
from common.utilities import bullet_pos_offset
import render
import game3d
import math3d
import world
import collision
import random
import math
from logic.gutils.effect_utils import handle_sfx_differentiation_process
BULLET_RIFLE_TYPE = 1
BULLET_SNIPPER_TYPE = 2
BULLET_LASER_TYPE = 3
BULLET_SFX_MAX_DISTANCE_SQR = (100 * NEOX_UNIT_SCALE) ** 2
EXPLODE_SFX_MAX_DISTANCE_SQR = (300 * NEOX_UNIT_SCALE) ** 2
_HASH_texture_distort = game3d.calc_string_hash('texture_distort')
_HASH_time = game3d.calc_string_hash('time')
_HASH_texture_light = game3d.calc_string_hash('texture_light')
SCREEN_HURT_DIR_FRONT = 1
SCREEN_HURT_DIR_LEFT = 2
SCREEN_HURT_DIR_BACK = 3
SCREEN_HURT_DIR_RIGHT = 4
SIGNAL_RES = set(['renwu', 'robot'])
SCREEN_HURT_SFX_DICT = {SCREEN_HURT_DIR_FRONT: [{'sfx': 'shoujifankui_{0}_zhengqian'}, {'sfx': 'shoujifankui_{0}_zuoqian'}, {'sfx': 'shoujifankui_{0}_zuohou','roatate_by_z': True}],SCREEN_HURT_DIR_LEFT: [{'sfx': 'shoujifankui_{0}_zuoqian'}, {'sfx': 'shoujifankui_{0}_zhengzuo'}, {'sfx': 'shoujifankui_{0}_zuohou'}],SCREEN_HURT_DIR_BACK: [{'sfx': 'shoujifankui_{0}_zuohou'}, {'sfx': 'shoujifankui_{0}_zhengqian','roatate_by_z': True}, {'sfx': 'shoujifankui_{0}_zuoqian','roatate_by_z': True}],SCREEN_HURT_DIR_RIGHT: [{'sfx': 'shoujifankui_{0}_zuohou','roatate_by_z': True}, {'sfx': 'shoujifankui_{0}_zhengzuo','roatate_by_z': True}, {'sfx': 'shoujifankui_{0}_zuoqian','roatate_by_z': True}]}
SCREEN_HURT_SFX_MAP = [{'s_angle': 0,'e_angle': 45,'dir': SCREEN_HURT_DIR_FRONT}, {'s_angle': 45,'e_angle': 135,'dir': SCREEN_HURT_DIR_RIGHT}, {'s_angle': 135,'e_angle': 225,'dir': SCREEN_HURT_DIR_BACK}, {'s_angle': 225,'e_angle': 315,'dir': SCREEN_HURT_DIR_LEFT}, {'s_angle': 315,'e_angle': 360,'dir': SCREEN_HURT_DIR_FRONT}]
HUMAN_TYPE = 0
MECHA_TYPE = 1
OTHER_TYPE = 2
SOUND_TYPE_ALL = 0
SOUND_TYPE_SELF = 1
SOUND_TYPE_CREATOR = 2

def get_min_index(percent, percents):
    index = -1
    if percent == None:
        return index
    else:
        for i, p in enumerate(percents):
            if percent > p:
                break
            index = i

        return index


IGNORE_HIT_BLOOD_SFX_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LMechaTrans',
                                                    'LMotorcycle', 'LExerciseTarget'))

class ComHumanHurtAppearance(UnitCom):
    TRAJECTORY_SFX_MAX_NUM = 4
    HURT_TYPE_HAND = 0
    HURT_TYPE_GUN = 1
    HURT_TYPE_COLDWEAPON = 2
    HURT_TYPE_GUN_MINE = 3
    HIT_SFX_PATHS = {HURT_TYPE_HAND: 'effect/fx/weapon/other/renwushouji.sfx',
       HURT_TYPE_GUN: 'effect/fx/weapon/other/renwushouji.sfx',
       HURT_TYPE_COLDWEAPON: 'effect/fx/weapon/other/renwushouji.sfx',
       HURT_TYPE_GUN_MINE: 'effect/fx/weapon/other/renwushouji.sfx'
       }
    BIND_EVENT = {'E_HIT_BLOOD_SFX': 'be_hited',
       'E_AIR_SHOOT': '_hit_target_sfx',
       'E_BOMB_HIT_SFX': '_on_bomb_hit_sfx',
       'E_BUFF_HIT_SFX': '_on_buff_hit_sfx',
       'E_ADD_BUFF_SFX': '_on_add_buff_sfx',
       'G_BUFF_ICON_VISIBILITY': 'get_icon_sfx_visibility',
       'E_DEL_BUFF_SFX': '_on_del_buff_sfx',
       'E_SHOW_SFX_ON_MODEL': '_on_show_sfx_on_model',
       'E_SHOW_SCREEN_HURT_SFX': '_show_screen_hurt_sfx',
       'E_SHOW_OUTLINE': 'be_hit_outline_display',
       'E_HEALTH_HP_CHANGE': '_show_low_health_sfx',
       'E_SIGNAL_CHANGE': '_show_low_health_sfx',
       'E_SET_CONTROL_TARGET': '_show_low_health_sfx',
       'E_HEALTH_INIT': '_show_low_health_sfx',
       'E_MODEL_LOADED': '_model_loaded',
       'E_ON_CONTROL_TARGET_CHANGE': ('on_ctrl_target_changed', 100),
       'E_BOARD_SKATE': ('on_board_skate', 10),
       'E_LEAVE_SKATE_FINISH': ('on_leave_skate', 10),
       'E_SET_BUFF_SFX_VISIBILITY_TEST': 'set_buff_sfx_visibility',
       'E_HIDE_ALL_BUFF_SFX': 'hide_all_sfx',
       'E_SWITCH_MODEL': 'on_switch_model'
       }
    if battle_utils.is_signal_logic():
        LOW_HEALTH_SFX = {HUMAN_TYPE: ('effect/fx/pingmu_cn/dixuezhuangtai_renwu_01.sfx', 'effect/fx/pingmu_cn/dixuezhuangtai_renwu_02.sfx'),MECHA_TYPE: ('effect/fx/pingmu_cn/dixuezhuangtai_robot_01.sfx', 'effect/fx/pingmu_cn/dixuezhuangtai_robot_02.sfx')
           }
    else:
        LOW_HEALTH_SFX = {HUMAN_TYPE: ('effect/fx/pingmu/dixuezhuangtai_renwu_01.sfx', 'effect/fx/pingmu/dixuezhuangtai_renwu_02.sfx'),MECHA_TYPE: ('effect/fx/pingmu/dixuezhuangtai_robot_01.sfx', 'effect/fx/pingmu/dixuezhuangtai_robot_02.sfx')
           }
    LOW_HEALTH_PERCENT = {HUMAN_TYPE: (0.3, 0.15),
       MECHA_TYPE: (0.4, 0.15)
       }
    LOW_SIGNAL_PERCENT = (0.5, 0.15)

    def __init__(self):
        super(ComHumanHurtAppearance, self).__init__()
        self._weapon_model = None
        self._buff_sfx_set = {}
        self._buff_screen_sfx = {}
        self._buff_sound_ids = {}
        self._is_buff_sfx_enable = {}
        self._human_screen_sfx_id = None
        self._mecha_screen_sfx_id = None
        self._smooth_outline_timer_id = None
        self._cur_low_health_sfx = None
        self._cur_low_health_sfx_id = None
        self._low_sfx_sound_id = None
        self.creator_id = {}
        self._screen_sfx_buff_ids = set()
        self._sound_buff_ids = set()
        self._hide_all = False
        if global_data.game_mode.is_snow_res():
            self.collision_sfx_map = scene_const.snow_collision_sfx_map
            self.material_sfx_map = scene_const.snow_material_sfx_map
        else:
            self.collision_sfx_map = scene_const.collision_sfx_map
            self.material_sfx_map = scene_const.material_sfx_map
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_target_setted_event': self.on_camera_target_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    @property
    def weapon_model(self):
        if not self._weapon_model or not self._weapon_model():
            weapon_model = self.sd.ref_hand_weapon_model
            if weapon_model and weapon_model.valid:
                import weakref
                self._weapon_model = weakref.ref(weapon_model)
            else:
                self._weapon_model = None
        if self._weapon_model:
            return self._weapon_model()
        else:
            return

    def get_sfx_socket(self, buff_id, is_end=False):
        ext_info = confmgr.get('c_buff_data', str(buff_id), 'ExtInfo')
        if ext_info:
            if ext_info.get('is_no_socket', 0):
                return
            if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
                val_key = 'sfx_socket_mecha'
            else:
                val_key = 'sfx_socket_human'
            sfx_socket = ext_info.get(val_key, None)
            if is_end:
                val_key = 'end_' + val_key
                sfx_socket = ext_info.get(val_key, sfx_socket)
            if sfx_socket:
                return sfx_socket
        return 'fx_buff'

    def get_sfx_socket_inherit(self, buff_id):
        conf = confmgr.get('c_buff_data', str(buff_id)) or {}
        if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
            sfx_inherit = conf.get('ExtInfo', {}).get('sfx_inherit_mecha', None)
        else:
            sfx_inherit = conf.get('ExtInfo', {}).get('sfx_inherit_human', None)
        return sfx_inherit

    def get_sfx_scale(self, buff_id):
        conf = confmgr.get('c_buff_data', str(buff_id)) or {}
        if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
            sfx_scale = conf.get('ExtInfo', {}).get('sfx_scale_mecha')
        else:
            sfx_scale = conf.get('ExtInfo', {}).get('sfx_scale_human')
        return sfx_scale

    def on_buff_sfx_loaded--- This code section failed: ---

 282       0  LOAD_FAST             1  'sfx'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            8  'is'
           9  POP_JUMP_IF_FALSE    16  'to 16'

 283      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 284      16  LOAD_FAST             2  'user_data'
          19  UNPACK_SEQUENCE_2     2 
          22  STORE_FAST            4  'buff_id'
          25  STORE_FAST            5  'ex_data'

 285      28  LOAD_FAST             5  'ex_data'
          31  LOAD_ATTR             1  'get'
          34  LOAD_CONST            1  'can_multi'
          37  LOAD_GLOBAL           2  'False'
          40  CALL_FUNCTION_2       2 
          43  STORE_FAST            6  'can_multi'

 286      46  LOAD_FAST             4  'buff_id'
          49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             3  '_buff_sfx_set'
          55  COMPARE_OP            6  'in'
          58  POP_JUMP_IF_FALSE    82  'to 82'
          61  LOAD_FAST             6  'can_multi'
          64  UNARY_NOT        
        65_0  COME_FROM                '58'
          65  POP_JUMP_IF_FALSE    82  'to 82'

 287      68  LOAD_FAST             1  'sfx'
          71  LOAD_ATTR             4  'destroy'
          74  CALL_FUNCTION_0       0 
          77  POP_TOP          

 288      78  LOAD_CONST            0  ''
          81  RETURN_END_IF    
        82_0  COME_FROM                '65'

 289      82  LOAD_FAST             0  'self'
          85  LOAD_ATTR             5  '_is_buff_sfx_enable'
          88  LOAD_ATTR             1  'get'
          91  LOAD_FAST             4  'buff_id'
          94  LOAD_GLOBAL           2  'False'
          97  CALL_FUNCTION_2       2 
         100  POP_JUMP_IF_TRUE    117  'to 117'

 290     103  LOAD_FAST             1  'sfx'
         106  LOAD_ATTR             4  'destroy'
         109  CALL_FUNCTION_0       0 
         112  POP_TOP          

 291     113  LOAD_CONST            0  ''
         116  RETURN_END_IF    
       117_0  COME_FROM                '100'

 292     117  LOAD_FAST             0  'self'
         120  LOAD_ATTR             6  'ev_g_model'
         123  CALL_FUNCTION_0       0 
         126  STORE_FAST            7  'model'

 293     129  LOAD_FAST             6  'can_multi'
         132  POP_JUMP_IF_FALSE   189  'to 189'

 294     135  LOAD_FAST             4  'buff_id'
         138  LOAD_FAST             0  'self'
         141  LOAD_ATTR             3  '_buff_sfx_set'
         144  COMPARE_OP            7  'not-in'
         147  POP_JUMP_IF_FALSE   166  'to 166'

 295     150  BUILD_LIST_0          0 
         153  LOAD_FAST             0  'self'
         156  LOAD_ATTR             3  '_buff_sfx_set'
         159  LOAD_FAST             4  'buff_id'
         162  STORE_SUBSCR     
         163  JUMP_FORWARD          0  'to 166'
       166_0  COME_FROM                '163'

 296     166  LOAD_FAST             0  'self'
         169  LOAD_ATTR             3  '_buff_sfx_set'
         172  LOAD_FAST             4  'buff_id'
         175  BINARY_SUBSCR    
         176  LOAD_ATTR             7  'append'
         179  LOAD_FAST             1  'sfx'
         182  CALL_FUNCTION_1       1 
         185  POP_TOP          
         186  JUMP_FORWARD         13  'to 202'

 298     189  LOAD_FAST             1  'sfx'
         192  LOAD_FAST             0  'self'
         195  LOAD_ATTR             3  '_buff_sfx_set'
         198  LOAD_FAST             4  'buff_id'
         201  STORE_SUBSCR     
       202_0  COME_FROM                '186'

 299     202  LOAD_FAST             7  'model'
         205  POP_JUMP_IF_FALSE   400  'to 400'

 300     208  LOAD_FAST             0  'self'
         211  LOAD_ATTR             8  'get_sfx_socket'
         214  LOAD_FAST             4  'buff_id'
         217  CALL_FUNCTION_1       1 
         220  STORE_FAST            8  'sfx_socket'

 301     223  LOAD_FAST             8  'sfx_socket'
         226  POP_JUMP_IF_FALSE   275  'to 275'

 302     229  LOAD_FAST             0  'self'
         232  LOAD_ATTR             9  'get_sfx_socket_inherit'
         235  LOAD_FAST             4  'buff_id'
         238  CALL_FUNCTION_1       1 
         241  JUMP_IF_TRUE_OR_POP   250  'to 250'
         244  LOAD_GLOBAL          10  'world'
         247  LOAD_ATTR            11  'BIND_TYPE_DEFAULT'
       250_0  COME_FROM                '241'
         250  STORE_FAST            9  'sfx_inherit'

 303     253  LOAD_FAST             7  'model'
         256  LOAD_ATTR            12  'bind'
         259  LOAD_FAST             8  'sfx_socket'
         262  LOAD_FAST             1  'sfx'
         265  LOAD_FAST             9  'sfx_inherit'
         268  CALL_FUNCTION_3       3 
         271  POP_TOP          
         272  JUMP_FORWARD         49  'to 324'

 305     275  LOAD_GLOBAL          13  'global_data'
         278  LOAD_ATTR            14  'game_mgr'
         281  LOAD_ATTR            15  'scene'
         284  STORE_FAST           10  'scene'

 306     287  LOAD_FAST            10  'scene'
         290  POP_JUMP_IF_FALSE   324  'to 324'

 307     293  LOAD_FAST            10  'scene'
         296  LOAD_ATTR            16  'add_object'
         299  LOAD_FAST             1  'sfx'
         302  CALL_FUNCTION_1       1 
         305  POP_TOP          

 308     306  LOAD_FAST             0  'self'
         309  LOAD_ATTR            17  'ev_g_position'
         312  CALL_FUNCTION_0       0 
         315  LOAD_FAST             1  'sfx'
         318  STORE_ATTR           18  'world_position'
         321  JUMP_FORWARD          0  'to 324'
       324_0  COME_FROM                '321'
       324_1  COME_FROM                '272'

 309     324  LOAD_FAST             0  'self'
         327  LOAD_ATTR            19  'set_buff_sfx_visibility'
         330  LOAD_FAST             4  'buff_id'
         333  LOAD_FAST             0  'self'
         336  LOAD_ATTR            20  'get_buff_sfx_visibility'
         339  LOAD_FAST             4  'buff_id'
         342  CALL_FUNCTION_1       1 
         345  CALL_FUNCTION_2       2 
         348  POP_TOP          

 310     349  LOAD_FAST             0  'self'
         352  LOAD_ATTR            21  'get_sfx_scale'
         355  LOAD_FAST             4  'buff_id'
         358  CALL_FUNCTION_1       1 
         361  STORE_FAST           11  'scale'

 311     364  LOAD_FAST            11  'scale'
         367  POP_JUMP_IF_FALSE   400  'to 400'

 312     370  LOAD_GLOBAL          22  'math3d'
         373  LOAD_ATTR            23  'vector'
         376  LOAD_FAST            11  'scale'
         379  LOAD_FAST            11  'scale'
         382  LOAD_FAST            11  'scale'
         385  CALL_FUNCTION_3       3 
         388  LOAD_FAST             1  'sfx'
         391  STORE_ATTR           24  'scale'
         394  JUMP_ABSOLUTE       400  'to 400'
         397  JUMP_FORWARD          0  'to 400'
       400_0  COME_FROM                '397'

 313     400  LOAD_GLOBAL          25  'handle_sfx_differentiation_process'
         403  LOAD_FAST             1  'sfx'
         406  LOAD_FAST             5  'ex_data'
         409  CALL_FUNCTION_2       2 
         412  POP_TOP          

 315     413  LOAD_FAST             5  'ex_data'
         416  LOAD_ATTR             1  'get'
         419  LOAD_CONST            2  'spin_speed'
         422  LOAD_CONST            3  -1
         425  CALL_FUNCTION_2       2 
         428  STORE_FAST           12  'spin_speed'

 316     431  LOAD_FAST            12  'spin_speed'
         434  LOAD_CONST            4  ''
         437  COMPARE_OP            4  '>'
         440  POP_JUMP_IF_FALSE   594  'to 594'

 317     443  LOAD_GLOBAL          26  'hasattr'
         446  LOAD_GLOBAL           5  '_is_buff_sfx_enable'
         449  CALL_FUNCTION_2       2 
         452  POP_JUMP_IF_TRUE    467  'to 467'

 318     455  BUILD_MAP_0           0 
         458  LOAD_FAST             0  'self'
         461  STORE_ATTR           27  'spin_sfx_map'
         464  JUMP_FORWARD          0  'to 467'
       467_0  COME_FROM                '464'

 319     467  LOAD_FAST             4  'buff_id'
         470  LOAD_FAST             0  'self'
         473  LOAD_ATTR            27  'spin_sfx_map'
         476  COMPARE_OP            7  'not-in'
         479  POP_JUMP_IF_FALSE   507  'to 507'

 320     482  BUILD_LIST_0          0 
         485  LOAD_CONST            6  ''
         488  LOAD_FAST            12  'spin_speed'
         491  BUILD_LIST_3          3 
         494  LOAD_FAST             0  'self'
         497  LOAD_ATTR            27  'spin_sfx_map'
         500  LOAD_FAST             4  'buff_id'
         503  STORE_SUBSCR     
         504  JUMP_FORWARD          0  'to 507'
       507_0  COME_FROM                '504'

 321     507  LOAD_FAST             0  'self'
         510  LOAD_ATTR            27  'spin_sfx_map'
         513  LOAD_FAST             4  'buff_id'
         516  BINARY_SUBSCR    
         517  LOAD_CONST            4  ''
         520  BINARY_SUBSCR    
         521  LOAD_ATTR             7  'append'
         524  LOAD_FAST             1  'sfx'
         527  CALL_FUNCTION_1       1 
         530  POP_TOP          

 322     531  LOAD_GLOBAL          28  'getattr'
         534  LOAD_GLOBAL           7  'append'
         537  LOAD_CONST            0  ''
         540  CALL_FUNCTION_3       3 
         543  POP_JUMP_IF_TRUE    594  'to 594'

 323     546  LOAD_GLOBAL          13  'global_data'
         549  LOAD_ATTR            14  'game_mgr'
         552  LOAD_ATTR            29  'register_logic_timer'

 324     555  LOAD_FAST             0  'self'
         558  LOAD_ATTR            30  'update_spin_sfx'
         561  LOAD_CONST            8  'interval'
         564  LOAD_CONST            9  1
         567  LOAD_CONST           10  'times'
         570  LOAD_CONST            3  -1
         573  LOAD_CONST           11  'timedelta'
         576  LOAD_GLOBAL          31  'True'
         579  CALL_FUNCTION_769   769 
         582  LOAD_FAST             0  'self'
         585  STORE_ATTR           32  'spin_sfx_timer'
         588  JUMP_ABSOLUTE       594  'to 594'
         591  JUMP_FORWARD          0  'to 594'
       594_0  COME_FROM                '591'
         594  LOAD_CONST            0  ''
         597  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 449

    def update_spin_sfx--- This code section failed: ---

 327       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('pi',)
           6  IMPORT_NAME           0  'math'
           9  IMPORT_FROM           1  'pi'
          12  STORE_FAST            2  'pi'
          15  POP_TOP          

 328      16  LOAD_GLOBAL           2  'getattr'
          19  LOAD_GLOBAL           3  'None'
          22  LOAD_CONST            0  ''
          25  CALL_FUNCTION_3       3 
          28  STORE_FAST            3  'spin_sfx_map'

 329      31  LOAD_FAST             3  'spin_sfx_map'
          34  POP_JUMP_IF_TRUE     75  'to 75'

 330      37  LOAD_GLOBAL           4  'global_data'
          40  LOAD_ATTR             5  'game_mgr'
          43  LOAD_ATTR             6  'unregister_logic_timer'
          46  LOAD_GLOBAL           2  'getattr'
          49  LOAD_GLOBAL           4  'global_data'
          52  LOAD_CONST            0  ''
          55  CALL_FUNCTION_3       3 
          58  CALL_FUNCTION_1       1 
          61  POP_TOP          

 331      62  LOAD_CONST            0  ''
          65  LOAD_FAST             0  'self'
          68  STORE_ATTR            7  'spin_sfx_timer'

 332      71  LOAD_CONST            0  ''
          74  RETURN_END_IF    
        75_0  COME_FROM                '34'

 333      75  BUILD_LIST_0          0 
          78  STORE_FAST            4  'invalid_buff_id'

 334      81  SETUP_LOOP          243  'to 327'
          84  LOAD_GLOBAL           8  'six'
          87  LOAD_ATTR             9  'iteritems'
          90  LOAD_FAST             3  'spin_sfx_map'
          93  CALL_FUNCTION_1       1 
          96  GET_ITER         
          97  FOR_ITER            226  'to 326'
         100  UNPACK_SEQUENCE_2     2 
         103  STORE_FAST            5  'buff_id'
         106  STORE_FAST            6  'data'

 335     109  LOAD_FAST             6  'data'
         112  LOAD_CONST            1  ''
         115  BINARY_SUBSCR    
         116  STORE_FAST            7  'sfx_list'

 336     119  LOAD_FAST             6  'data'
         122  LOAD_CONST            5  1
         125  DUP_TOPX_2            2 
         128  BINARY_SUBSCR    
         129  LOAD_FAST             6  'data'
         132  LOAD_CONST            6  2
         135  BINARY_SUBSCR    
         136  LOAD_FAST             1  'dt'
         139  BINARY_MULTIPLY  
         140  INPLACE_ADD      
         141  ROT_THREE        
         142  STORE_SUBSCR     

 337     143  BUILD_LIST_0          0 
         146  STORE_FAST            8  'valid_sfx_list'

 338     149  SETUP_LOOP           50  'to 202'
         152  LOAD_FAST             7  'sfx_list'
         155  GET_ITER         
         156  FOR_ITER             42  'to 201'
         159  STORE_FAST            9  'sfx'

 339     162  LOAD_FAST             9  'sfx'
         165  UNARY_NOT        
         166  POP_JUMP_IF_TRUE    156  'to 156'
         169  LOAD_FAST             9  'sfx'
         172  LOAD_ATTR            10  'valid'
         175  UNARY_NOT        
       176_0  COME_FROM                '166'
         176  POP_JUMP_IF_FALSE   185  'to 185'

 340     179  CONTINUE            156  'to 156'
         182  JUMP_FORWARD          0  'to 185'
       185_0  COME_FROM                '182'

 341     185  LOAD_FAST             8  'valid_sfx_list'
         188  LOAD_ATTR            11  'append'
         191  LOAD_FAST             9  'sfx'
         194  CALL_FUNCTION_1       1 
         197  POP_TOP          
         198  JUMP_BACK           156  'to 156'
         201  POP_BLOCK        
       202_0  COME_FROM                '149'

 342     202  LOAD_FAST             8  'valid_sfx_list'
         205  LOAD_FAST             6  'data'
         208  LOAD_CONST            1  ''
         211  STORE_SUBSCR     

 343     212  LOAD_FAST             6  'data'
         215  LOAD_CONST            1  ''
         218  BINARY_SUBSCR    
         219  POP_JUMP_IF_TRUE    241  'to 241'

 344     222  LOAD_FAST             4  'invalid_buff_id'
         225  LOAD_ATTR            11  'append'
         228  LOAD_FAST             5  'buff_id'
         231  CALL_FUNCTION_1       1 
         234  POP_TOP          

 345     235  CONTINUE             97  'to 97'
         238  JUMP_FORWARD          0  'to 241'
       241_0  COME_FROM                '238'

 346     241  LOAD_CONST            7  2.0
         244  LOAD_FAST             2  'pi'
         247  BINARY_MULTIPLY  
         248  LOAD_GLOBAL          12  'len'
         251  LOAD_FAST             8  'valid_sfx_list'
         254  CALL_FUNCTION_1       1 
         257  BINARY_DIVIDE    
         258  STORE_FAST           10  'yaw_step'

 347     261  SETUP_LOOP           59  'to 323'
         264  LOAD_GLOBAL          13  'enumerate'
         267  LOAD_FAST             8  'valid_sfx_list'
         270  CALL_FUNCTION_1       1 
         273  GET_ITER         
         274  FOR_ITER             45  'to 322'
         277  UNPACK_SEQUENCE_2     2 
         280  STORE_FAST           11  'i'
         283  STORE_FAST            9  'sfx'

 348     286  LOAD_GLOBAL          14  'math3d'
         289  LOAD_ATTR            15  'matrix'
         292  LOAD_ATTR            16  'make_rotation_y'
         295  LOAD_FAST             6  'data'
         298  LOAD_CONST            5  1
         301  BINARY_SUBSCR    
         302  LOAD_FAST            11  'i'
         305  LOAD_FAST            10  'yaw_step'
         308  BINARY_MULTIPLY  
         309  BINARY_ADD       
         310  CALL_FUNCTION_1       1 
         313  LOAD_FAST             9  'sfx'
         316  STORE_ATTR           17  'world_rotation_matrix'
         319  JUMP_BACK           274  'to 274'
         322  POP_BLOCK        
       323_0  COME_FROM                '261'
         323  JUMP_BACK            97  'to 97'
         326  POP_BLOCK        
       327_0  COME_FROM                '81'

 349     327  SETUP_LOOP           27  'to 357'
         330  LOAD_FAST             4  'invalid_buff_id'
         333  GET_ITER         
         334  FOR_ITER             19  'to 356'
         337  STORE_FAST           12  'invalid_bid'

 350     340  LOAD_FAST             3  'spin_sfx_map'
         343  LOAD_ATTR            18  'pop'
         346  LOAD_FAST            12  'invalid_bid'
         349  CALL_FUNCTION_1       1 
         352  POP_TOP          
         353  JUMP_BACK           334  'to 334'
         356  POP_BLOCK        
       357_0  COME_FROM                '327'
         357  LOAD_CONST            0  ''
         360  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 25

    def hide_all_sfx(self, hide):
        self._hide_all = hide
        self.update_buff_sfx_visibility()
        self.update_buff_icon_visibility()

    def _model_loaded(self, model):
        if not model:
            return
        for buff_id, sfx in six.iteritems(self._buff_sfx_set):
            sfx_socket = self.get_sfx_socket(buff_id)
            if not isinstance(sfx, list):
                sfx = [
                 sfx]
            if sfx_socket:
                sfx_inherit = self.get_sfx_socket_inherit(buff_id) or world.BIND_TYPE_DEFAULT
                for s in sfx:
                    model.bind(sfx_socket, s, sfx_inherit)

            else:
                scene = global_data.game_mgr.scene
                if scene:
                    for s in sfx:
                        scene.add_object(s)
                        s.world_position = self.ev_g_position()

            self.set_buff_sfx_visibility(buff_id, self.get_buff_sfx_visibility(buff_id))
            scale = self.get_sfx_scale(buff_id)
            if scale:
                for s in sfx:
                    s.scale = math3d.vector(scale, scale, scale)

    def get_end_sfx_path(self, buff_id):
        conf = confmgr.get('c_buff_data', str(buff_id))
        sfx_paths = conf.get('SfxPath')
        if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
            sfx_paths = conf.get('MechaSfxPath') or sfx_paths
        if not sfx_paths:
            return
        lplayer = global_data.cam_lplayer
        if not lplayer and global_data.player and global_data.player.logic:
            lplayer = global_data.player.logic
        if lplayer and lplayer.ev_g_is_campmate(self.ev_g_camp_id()):
            return sfx_paths.get('frd_end')
        return sfx_paths.get('emy_end', sfx_paths.get('frd_end'))

    def _on_add_buff_sfx(self, buff_id, buff_data={}):
        creator_id = buff_data.get('creator_id')
        if creator_id:
            self.creator_id[buff_id] = creator_id
        elif buff_id in self.creator_id:
            del self.creator_id[buff_id]
        self.create_buff_sfx(buff_id)
        self.create_screen_sfx(buff_id)
        self.create_buff_sound(buff_id, creator_id)

    def create_buff_sfx(self, buff_id):
        conf = confmgr.get('c_buff_data', str(buff_id))
        ext_info = conf.get('ExtInfo', {})
        sfx_paths = conf.get('SfxPath')
        if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
            sfx_paths = conf.get('MechaSfxPath') or sfx_paths
        if not sfx_paths:
            return
        lplayer = global_data.cam_lplayer
        if not lplayer and global_data.player and global_data.player.logic:
            lplayer = global_data.player.logic
        me_sfx = sfx_paths.get('me')
        creator_id = self.creator_id.get(buff_id)
        is_friend = lplayer.ev_g_is_campmate_by_eid(creator_id)
        if creator_id == lplayer.id and me_sfx:
            sfx_path = me_sfx
        elif bool(lplayer and is_friend):
            sfx_path = sfx_paths.get('friend')
        else:
            sfx_path = sfx_paths.get('enemy', sfx_paths.get('friend'))
        if not sfx_path:
            return
        ex_data = {}
        self._is_buff_sfx_enable[buff_id] = True
        can_multi = ext_info.get('can_multi', False)
        ex_data['can_multi'] = can_multi
        if buff_id in self._buff_sfx_set and not can_multi:
            sfx = self._buff_sfx_set[buff_id]
            if sfx.valid:
                if not ext_info.get('is_loop_sfx', False):
                    sfx.restart()
                self.set_buff_sfx_visibility(buff_id, self.get_buff_sfx_visibility(buff_id))
                return
            sfx.remove_from_parent()
            sfx.destroy()
            del self._buff_sfx_set[buff_id]
        need_camp_diff = ext_info.get('camp_diff', 0)
        if need_camp_diff == 1:
            ex_data['need_diff_process'] = not is_friend
        elif need_camp_diff == -1:
            ex_data['need_diff_process'] = is_friend
        spin_speed = ext_info.get('spin_speed', -1)
        if spin_speed > 0:
            ex_data['spin_speed'] = spin_speed
        world.create_sfx_async(sfx_path, self.on_buff_sfx_loaded, (buff_id, ex_data))
        if self.sd.ref_socket_res_agent and ext_info.get('follow_model_use_sfx', True):
            self.sd.ref_socket_res_agent.create_sfx_on_follow_model(sfx_path)

    def create_screen_sfx(self, buff_id, no_check=False):
        screen_sfx_path = confmgr.get('c_buff_data', str(buff_id), 'ScreenSfxPath')
        if not screen_sfx_path:
            return
        if buff_id not in self._screen_sfx_buff_ids:
            self._screen_sfx_buff_ids.add(buff_id)
        if not no_check and (not global_data.cam_lctarget or self.unit_obj.id != global_data.cam_lctarget.id):
            return
        if buff_id in self._buff_screen_sfx:
            global_data.sfx_mgr.remove_sfx_by_id(self._buff_screen_sfx[buff_id])
            del self._buff_screen_sfx[buff_id]
        self._buff_screen_sfx[buff_id] = create_screen_effect_directly(screen_sfx_path)

    def create_buff_sound(self, buff_id, creator_id, is_end=False):
        buff_data = confmgr.get('c_buff_data', str(buff_id), default=None)
        if not buff_data:
            return
        else:
            ext_info = buff_data.get('ExtInfo', {})
            sound_name = ext_info.get('end_sound_name' if is_end else 'sound_name', '')
            if not sound_name:
                return
            sound_type = ext_info.get('end_sound_type' if is_end else 'sound_type', SOUND_TYPE_ALL)
            is_creator = bool(global_data.cam_lplayer and creator_id == global_data.cam_lplayer.id)
            is_cam = bool(global_data.cam_lplayer and (self.unit_obj.id == global_data.cam_lplayer.id or self.unit_obj.sd.ref_driver_id == global_data.cam_lplayer.id))
            if sound_type == SOUND_TYPE_CREATOR and not is_creator or sound_type == SOUND_TYPE_SELF and not is_cam:
                return
            if is_cam:
                sound_id = global_data.sound_mgr.play_sound_2d(sound_name)
            else:
                sound_id = global_data.sound_mgr.play_sound(sound_name, self.ev_g_position())
            if not is_end:
                if buff_id not in self._sound_buff_ids:
                    self._sound_buff_ids.add(buff_id)
                if buff_id in self._buff_sound_ids:
                    global_data.sound_mgr.stop_playing_id(self._buff_sound_ids[buff_id])
                self._buff_sound_ids[buff_id] = sound_id
            return

    def _on_del_buff_sfx(self, buff_id):
        if buff_id in self._is_buff_sfx_enable:
            self._is_buff_sfx_enable[buff_id] = False
        buff_pos = None
        still_exist = False
        if buff_id in self._buff_sfx_set:
            if isinstance(self._buff_sfx_set[buff_id], list):
                sfx = self._buff_sfx_set[buff_id].pop(-1)
                still_exist = bool(self._buff_sfx_set[buff_id])
                if not still_exist:
                    self._buff_sfx_set.pop(buff_id)
            else:
                sfx = self._buff_sfx_set.pop(buff_id)
            if sfx.valid:
                self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.remove_sfx_on_follow_model(sfx.filename.replace('\\', '/'))
                buff_pos = sfx.world_position
                sfx.remove_from_parent()
                sfx.destroy()
        if not still_exist:
            if buff_id in self._buff_screen_sfx:
                global_data.sfx_mgr.remove_sfx_by_id(self._buff_screen_sfx[buff_id])
                del self._buff_screen_sfx[buff_id]
            if buff_id in self._screen_sfx_buff_ids:
                self._screen_sfx_buff_ids.remove(buff_id)
            if buff_id in self._sound_buff_ids:
                self._sound_buff_ids.remove(buff_id)
            if buff_id in self._buff_sound_ids:
                global_data.sound_mgr.stop_playing_id(self._buff_sound_ids[buff_id])
                self._buff_sound_ids.pop(buff_id)
        if global_data.cam_lctarget and self.unit_obj.id == global_data.cam_lctarget.id:
            end_screen_sfx_path = confmgr.get('c_buff_data', str(buff_id), 'EndScreenSfxPath', default=None)
            if end_screen_sfx_path:
                create_screen_effect_directly(end_screen_sfx_path)
        model = self.ev_g_model()
        end_sfx_path = self.get_end_sfx_path(buff_id)
        if model and end_sfx_path:
            sfx_socket = self.get_sfx_socket(buff_id, is_end=True)
            if sfx_socket:
                sfx_inherit = self.get_sfx_socket_inherit(buff_id) or world.BIND_TYPE_DEFAULT
                global_data.sfx_mgr.create_sfx_on_model(end_sfx_path, model, sfx_socket, sfx_inherit, duration=5)
            else:
                pos = buff_pos if buff_pos else self.ev_g_position()
                global_data.sfx_mgr.create_sfx_in_scene(end_sfx_path, pos, duration=5)
        self.create_buff_sound(buff_id, self.creator_id.get(buff_id), True)
        if buff_id in self.creator_id:
            del self.creator_id[buff_id]
        return

    def on_camera_target_setted(self):
        for sfx_id in six.itervalues(self._buff_screen_sfx):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._buff_screen_sfx = {}
        for buff_id in self._screen_sfx_buff_ids:
            self.create_screen_sfx(buff_id)

        self._show_low_health_sfx()

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanHurtAppearance, self).init_from_dict(unit_obj, bdict)
        self._scene = world.get_active_scene()
        check_sfx_mapping_initialized()

    def be_hited(self, begin_pos, hit_pos, shot_type, **kwargs):
        if self.unit_obj.MASK & IGNORE_HIT_BLOOD_SFX_TAG_VALUE:
            return
        dmg_parts = kwargs.get('dmg_parts', {})
        is_hit_shield = bool(dmg_parts and dmg_parts.get(HIT_PART_SHIELD))
        if hit_pos.y > 0:
            self.create_shooted_sfx(begin_pos, hit_pos, shot_type, is_self=kwargs.get('is_self', False), is_hit_shield=is_hit_shield, trigger_is_self=kwargs.get('trigger_is_self', False))
        self.be_hit_outline_display()

    @execute_by_mode(True, ())
    def be_hit_outline_display(self):
        return
        if not self._scene:
            return
        else:
            if global_data.player.logic.ev_g_is_groupmate(self.unit_obj.id):
                return
            if self._smooth_outline_timer_id:
                return
            model = self.ev_g_model()
            if model:
                model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, True)
                self._scene.enable_smooth_outline(True, self.unit_obj.id)
                tm = global_data.game_mgr.get_logic_timer()
                if self._smooth_outline_timer_id:
                    tm.unregister(self._smooth_outline_timer_id)
                    self._smooth_outline_timer_id = None
                self._smooth_outline_timer_id = tm.register(func=lambda unit_id=self.unit_obj.id: self.close_smooth_outline(unit_id), interval=10.0, times=1, mode=CLOCK)
            return

    def close_smooth_outline(self, unit_id):
        if not self._scene:
            return
        else:
            model = self.ev_g_model()
            if model:
                model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, False)
            if self._smooth_outline_timer_id:
                tm = global_data.game_mgr.get_logic_timer()
                tm.unregister(self._smooth_outline_timer_id)
                self._smooth_outline_timer_id = None
            self._scene.enable_smooth_outline(False, unit_id)
            return

    def create_shooted_sfx(self, begin_pos, pos, shot_type, is_self, is_hit_shield, trigger_is_self):
        if check_need_ignore_effect_behind_camera(shot_type, pos):
            return
        else:
            hit_sfx_path = None
            if is_hit_shield:
                hit_sfx_path = self.material_sfx_map.get(scene_const.MTL_METAL, None)
                if hit_sfx_path:
                    hit_sfx_path = hit_sfx_path[0]
            elif is_self:
                hit_sfx_path = self.HIT_SFX_PATHS.get(self.HURT_TYPE_GUN_MINE)
            else:
                hit_sfx_path = self.HIT_SFX_PATHS.get(self.HURT_TYPE_GUN)
            if hit_sfx_path:
                if trigger_is_self:

                    def on_create_cb(sfx):
                        player_vect = pos - begin_pos
                        length_sqr = player_vect.length_sqr
                        if is_hit_shield:
                            sfx_distance_scale = get_sfx_scale_by_length_spr(length_sqr)
                        else:
                            sfx_distance_scale = get_sfx_scale_by_length_human_spr(length_sqr)
                        sfx_distance_scale = math3d.vector(sfx_distance_scale, sfx_distance_scale, sfx_distance_scale)
                        sfx.world_scale = sfx_distance_scale

                    global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path, pos, on_create_func=on_create_cb, int_check_type=CREATE_SRC_SIMPLE)
                else:
                    global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path, pos, int_check_type=CREATE_SRC_SIMPLE)
            return

    def _spray_directions(self, start_pos, end_pos, scene_pellet):
        direction = end_pos - start_pos
        if direction.is_zero:
            return (start_pos, [])
        length = direction.length
        direction.normalize()
        wp = self.sd.ref_wp_bar_cur_weapon
        if not wp or scene_pellet <= 1:
            offset = NEOX_UNIT_SCALE * 0.6
            if offset > length:
                offset = length
            return (end_pos - direction * offset, [direction * NEOX_UNIT_SCALE * 1.2])
        from math import radians, tan, pi
        up_direction = math3d.vector(0, 0, 1.0)
        right_direction = up_direction.cross(direction)
        if right_direction.is_zero:
            return (start_pos, [])
        right_direction.normalize()
        spray_range = tan(radians(wp.get_effective_value('fSprayAngle')))
        direct_list = []
        for i in range(scene_pellet):
            spread_range = random.uniform(0, spray_range)
            rotation_matrix = math3d.matrix.make_rotation(direction, random.uniform(-pi, pi))
            direct = direction + right_direction * rotation_matrix * spread_range
            direct *= 100 * NEOX_UNIT_SCALE
            direct_list.append(direct)

        return (
         start_pos, direct_list)

    def _hit_target_sfx(self, start_pos, end_pos, scene_pellet, shoot_mask, ext_dict=None):
        if ext_dict is None:
            ext_dict = {}
        player_pos = self._get_check_pos()
        if not player_pos:
            return
        else:
            player_vect = end_pos - player_pos
            length_sqr = player_vect.length_sqr
            if ext_dict and ext_dict.get('bullet_type', None):
                bullet_type = ext_dict.get('bullet_type', None)
            else:
                bullet_type = None
            if check_need_ignore_effect_behind_camera(bullet_type, end_pos):
                return
            hit_sfx_path, hit_sfx_scale = (None, 1.0)
            hit_sfx_code = ext_dict.get('hit_sfx_code', 0)
            if hit_sfx_code:
                hit_sfx_path, hit_sfx_scale = decode_sfx_info(hit_sfx_code)
            if not self.sd.ref_is_mecha and ext_dict.get('trigger_is_self', False):
                hit_sfx_scale = hit_sfx_scale * get_sfx_scale_by_length_spr(length_sqr)
            ex_data = {}
            sfx_scale = math3d.vector(hit_sfx_scale, hit_sfx_scale, hit_sfx_scale)
            res_conf = confmgr.get('firearm_res_config', str(bullet_type), default={})
            hide_crater = res_conf.get('cHideCraterSfx')
            camp_diff_param = res_conf.get('cExtraParam', {}).get('camp_diff', 0)
            if camp_diff_param and 'trigger_camp_id' in ext_dict and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != ext_dict['trigger_camp_id']:
                if type(camp_diff_param) == str:
                    hit_sfx_path = camp_diff_param
                else:
                    ex_data['need_diff_process'] = True
            quality = global_data.game_mgr.gds.get_actual_quality()
            create_src_type = crater_create_src_type = CREATE_SRC_MINE_HIT
            ltype = self.local_unit_type()
            if ltype == OTHER_TYPE:
                create_src_type = CREATE_SRC_OTHER_HIT
                crater_create_src_type = CREATE_SRC_OTHER_HIT
            else:
                if quality <= 2:
                    crater_create_src_type = CREATE_SRC_MINE_RAY_GUN_CRATER
                if length_sqr > BULLET_SFX_MAX_DISTANCE_SQR:
                    quality = 0
                if length_sqr < EXPLODE_SFX_MAX_DISTANCE_SQR and ext_dict and KEY_WATER_POS in ext_dict:
                    water_pos = math3d.vector(*ext_dict[KEY_WATER_POS])
                    sfx_path = self.collision_sfx_map.get(WATER_GROUP, None)
                    normal = math3d.vector(0, 1, 0)

                    def on_create_cb(sfx):
                        sfx.world_scale = sfx_scale

                    global_data.sfx_mgr.create_sfx_in_scene(sfx_path[0], water_pos, on_create_func=on_create_cb, int_check_type=create_src_type)
                    return
                if hit_sfx_path:

                    def create_cb(sfx):
                        sfx.scale = sfx_scale

                    global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path, end_pos, on_create_func=create_cb, duration=0.5, int_check_type=create_src_type, ex_data=ex_data)
                    return
            if length_sqr < EXPLODE_SFX_MAX_DISTANCE_SQR:
                check_start_pos, direct_list = self._spray_directions(start_pos, end_pos, scene_pellet)
                for vect in direct_list:
                    check_dir = vect
                    result = self._scene.scene_col.hit_by_ray(check_start_pos, check_start_pos + check_dir, 0, 65535, GROUP_CAN_SHOOT | WATER_GROUP, collision.INCLUDE_FILTER, False)
                    if result[0]:
                        pos = result[1]
                        normal = result[2]
                        cobj = result[5]
                        group = cobj.group
                        is_chunk_mesh = scene_utils.is_chunk_mesh(cobj)
                        sfx_path = self.collision_sfx_map.get(group, None)
                        if not sfx_path:
                            sfx_path = scene_const.collision_default_sfx
                        if is_chunk_mesh or group in (ROAD_GROUP, TERRAIN_GROUP, ICE_GROUP):
                            if is_chunk_mesh or group == TERRAIN_GROUP:
                                material_index = self._scene.get_scene_info_2d(end_pos.x, end_pos.z)
                            elif group == ROAD_GROUP:
                                material_index = scene_const.MTL_STONE
                            else:
                                material_index = scene_const.MTL_ICE
                            sfx_path = self.material_sfx_map.get(material_index, None)
                        if sfx_path:

                            def create_cb(sfx):
                                sfx.world_scale = sfx_scale
                                global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

                            global_data.sfx_mgr.create_sfx_in_scene(sfx_path[0], pos, on_create_func=create_cb, int_check_type=create_src_type)
                            if quality > 1 and sfx_path[1] and not hide_crater:

                                def bullet_sfx_callback(sfx):
                                    global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

                                pos = bullet_pos_offset(pos, normal)
                                global_data.sfx_mgr.create_sfx_in_scene(sfx_path[1], pos, on_create_func=bullet_sfx_callback, duration=BULLET_HOLE_LIFE_TIME, int_check_type=crater_create_src_type)

            return

    def _on_bomb_hit_sfx(self, bomb_id):
        sfx_path = confmgr.get('grenade_res_config', str(bomb_id), 'cHitSfx')
        model = self.ev_g_model()
        if sfx_path and model:
            socket_name = 'hit'
            if self.sd.ref_is_mecha:
                socket_name = 'javelin_hitted'
            elif self.sd.ref_is_pve_monster:
                socket_name = 'fx_buff'
            global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)

    def _on_buff_hit_sfx(self, buff_id):
        sfx_path = confmgr.get('c_buff_data', str(buff_id), 'HitSfxPath')
        if not sfx_path:
            return
        model = self.ev_g_model()
        if not model:
            return
        socket_name = 'hit'
        if self.sd.ref_is_mecha:
            socket_name = 'javelin_hitted'
        elif self.sd.ref_is_pve_monster:
            socket_name = 'fx_buff'
        global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)

    def _get_check_pos(self):
        if self._scene and self._scene.valid:
            return self._scene.active_camera.world_position
        else:
            return global_data.player.logic.ev_g_position()

    def _get_screen_hurt_sfx_data(self, is_mecha, fight_inj_type, damage, from_pos=None, itype=None, dmg_parts=None, triger_is_mecha=False):
        listener_look_at = global_data.sound_mgr.get_listener_look_at()
        if is_mecha:
            player_pos = global_data.player.logic.ev_g_control_target().logic.ev_g_model_position()
        else:
            player_pos = global_data.player.logic.ev_g_model_position()
            mecha = self.ev_g_bind_mecha_entity()
            if mecha:
                player_pos = mecha.logic.ev_g_model_position()
        ret_sfx_list = []
        if from_pos and player_pos:
            direction = from_pos - player_pos
            import common.utilities
            angle = common.utilities.vect2d_radian(direction, listener_look_at) * 180 / math.pi
            hurt_dir = None
            for value in SCREEN_HURT_SFX_MAP:
                if angle >= value['s_angle'] and angle <= value['e_angle']:
                    hurt_dir = value['dir']
                    break

            if hurt_dir:
                effect_lv = 3
                from logic.gutils.hitted_trk_utils import get_gun_scr_lv, get_throwable_scr_lv, _get_other_damage_scr_lv
                if fight_inj_type == FIGHT_INJ_SHOOT:
                    effect_lv = get_gun_scr_lv(itype, dmg_parts, is_mecha, triger_is_mecha, True)
                elif fight_inj_type == FIGHT_INJ_BOMB:
                    effect_lv = get_throwable_scr_lv(itype, is_mecha, triger_is_mecha, True)
                else:
                    effect_lv = _get_other_damage_scr_lv(self, damage, is_mecha)
                if effect_lv is None:
                    return []
                sfx_per_name = 'renwu'
                if is_mecha:
                    sfx_per_name = 'robot'
                    if global_data.mecha and global_data.mecha.logic:
                        shield = global_data.mecha.logic.ev_g_shield()
                        shield = shield if shield else 0
                        if shield > 0:
                            sfx_per_name = 'hudun'
                template_sfx_list = SCREEN_HURT_SFX_DICT[hurt_dir]
                for item in template_sfx_list:
                    sfx_item = {}
                    dir_postfix = ''
                    if battle_utils.is_signal_logic() and item['sfx'] in SIGNAL_RES:
                        dir_postfix = '_cn'
                    sfx_item['sfx'] = 'effect/fx/pingmu{0}/{1}_{2}.sfx'.format(dir_postfix, item['sfx'].format(sfx_per_name), effect_lv)
                    roatate_by_z = item.get('roatate_by_z', False)
                    if roatate_by_z:
                        rotation_matrix = math3d.matrix.make_rotation_z(math.pi)
                    else:
                        rotation_matrix = math3d.matrix()
                        rotation_matrix.set_identity()
                    sfx_item['rotation_matrix'] = rotation_matrix
                    ret_sfx_list.append(sfx_item)

        return ret_sfx_list

    def local_unit_type(self):
        if self.unit_obj is None or not global_data.cam_lplayer:
            return OTHER_TYPE
        else:
            if self.unit_obj.MASK & preregistered_tags.HUMAN_TAG_VALUE:
                if self.unit_obj.id == global_data.cam_lplayer.id:
                    return HUMAN_TYPE
                if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
                    if global_data.cam_lplayer.id == self.sd.ref_driver_id:
                        return MECHA_TYPE
            return OTHER_TYPE

    def _show_low_health_sfx(self, *args):
        ltype = self.local_unit_type()
        if ltype == OTHER_TYPE:
            if self._cur_low_health_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._cur_low_health_sfx_id)
                self._cur_low_health_sfx_id = None
            self._cur_low_health_sfx = None
            return
        else:
            if self.__class__ == LMechaTrans.LMechaTrans:
                return
            is_in_mecha = self.ev_g_in_mecha()
            if is_in_mecha and ltype == HUMAN_TYPE and not self.ev_g_in_mecha('MechaTrans'):
                if self._cur_low_health_sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self._cur_low_health_sfx_id)
                    self._cur_low_health_sfx_id = None
                    self._cur_low_health_sfx = None
                return
            cur_percent = self.ev_g_health_percent()
            percents = self.LOW_HEALTH_PERCENT[ltype]
            sfxs = self.LOW_HEALTH_SFX[ltype]
            sfx_path = None
            index = get_min_index(cur_percent, percents)
            signal_percent = global_data.cam_lplayer.ev_g_signal_percent()
            signal_percents = self.LOW_SIGNAL_PERCENT
            signal_sfxs = self.LOW_HEALTH_SFX[HUMAN_TYPE]
            signal_index = get_min_index(signal_percent, signal_percents)
            if ltype == MECHA_TYPE:
                signal_index = -1
            if signal_index >= index and signal_index >= 0:
                sfx_path = self.LOW_HEALTH_SFX[HUMAN_TYPE][signal_index]
            else:
                if index > signal_index and index >= 0:
                    sfx_path = sfxs[index]
                if sfx_path and sfx_path == self._cur_low_health_sfx:
                    return
            self._cur_low_health_sfx = sfx_path
            if self._cur_low_health_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._cur_low_health_sfx_id)
                self._cur_low_health_sfx_id = None
            if self._cur_low_health_sfx:
                self._cur_low_health_sfx_id = create_screen_effect_directly(self._cur_low_health_sfx)
            if self._cur_low_health_sfx and not self._low_sfx_sound_id:
                if self.sd.ref_is_mecha:
                    low_sound_name = 'mecha_low_blood'
                else:
                    low_sound_name = 'character_low_blood'
                self._low_sfx_sound_id = global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', low_sound_name))
            elif not self._cur_low_health_sfx and self._low_sfx_sound_id:
                global_data.sound_mgr.stop_playing_id(self._low_sfx_sound_id)
                self._low_sfx_sound_id = None
            return

    def _show_screen_hurt_sfx(self, fight_inj_type, damage, from_pos=None, itype=None, dmg_parts=None, triger_is_mecha=False):
        if not self.unit_obj:
            return
        else:
            owner = self.unit_obj.get_owner()
            if owner:
                owner_name = owner.__class__.__name__
                size = global_data.really_sfx_window_size
                scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)
                if owner_name == 'Avatar':
                    global_data.emgr.play_hit_voice.emit('hit', itype, owner)
                    if self._human_screen_sfx_id is None:
                        sfx_list = self._get_screen_hurt_sfx_data(False, fight_inj_type, damage, from_pos, itype, dmg_parts, triger_is_mecha)
                        for sfx_item in sfx_list:

                            def create_hurt_sfx(item):

                                def create_callback(sfx):
                                    sfx.scale = scale
                                    global_data.sfx_mgr.set_rotation(sfx, item['rotation_matrix'])

                                def remove_callback(sfx):
                                    if self.is_valid():
                                        self._human_screen_sfx_id = None
                                    return

                                self._human_screen_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(item['sfx'], duration=0.6, on_create_func=create_callback, on_remove_func=remove_callback)

                            create_hurt_sfx(sfx_item)

                elif owner_name in ('Mecha', 'MechaTrans'):
                    driver_id = self.sd.ref_driver_id
                    if global_data.player and driver_id == global_data.player.id:
                        global_data.emgr.play_hit_voice.emit('hit', itype, owner)
                        if self._mecha_screen_sfx_id is None:
                            sfx_list = self._get_screen_hurt_sfx_data(True, fight_inj_type, damage, from_pos, itype, dmg_parts, triger_is_mecha)
                            for sfx_item in sfx_list:

                                def create_hurt_sfx(item):

                                    def create_callback(sfx):
                                        sfx.scale = scale
                                        global_data.sfx_mgr.set_rotation(sfx, item['rotation_matrix'])
                                        sfx.enable_post_process(False)

                                    def remove_callback(sfx):
                                        if self.is_valid():
                                            self._mecha_screen_sfx_id = None
                                        return

                                    self._mecha_screen_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(item['sfx'], duration=0.6, on_create_func=create_callback, on_remove_func=remove_callback)

                                create_hurt_sfx(sfx_item)

            return

    def _on_show_sfx_on_model(self, sfx_path):
        model = self.ev_g_model()
        global_data.sfx_mgr.create_sfx_for_model(sfx_path, model)

    def del_all_buff(self):
        for sfx in six.itervalues(self._buff_sfx_set):
            if isinstance(sfx, list):
                for s in sfx:
                    if not s.valid:
                        continue
                    s.remove_from_parent()
                    s.destroy()

            elif sfx.valid:
                sfx.remove_from_parent()
                sfx.destroy()

        self._buff_sfx_set = {}
        for sfx_id in six.itervalues(self._buff_screen_sfx):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._buff_screen_sfx = {}
        self._is_buff_sfx_enable = {}
        self.creator_id = {}
        self._screen_sfx_buff_ids = set()

    def destroy(self):
        self.process_event(False)
        if self._cur_low_health_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._cur_low_health_sfx_id)
            self._cur_low_health_sfx_id = None
        if self._low_sfx_sound_id:
            global_data.sound_mgr.stop_playing_id(self._low_sfx_sound_id)
            self._low_sfx_sound_id = None
        if self._scene:
            self._scene.enable_smooth_outline(False, self.unit_obj.id)
        self.del_all_buff()
        super(ComHumanHurtAppearance, self).destroy()
        return

    def on_ctrl_target_changed(self, *args):
        global_data.game_mgr.post_exec(lambda : self.update_buff_sfx_visibility())

    def get_buff_sfx_visibility(self, buff_id):
        if self._hide_all:
            return False
        conf = confmgr.get('c_buff_data', str(buff_id))
        if self.unit_obj.MASK & preregistered_tags.HUMAN_TAG_VALUE == 0:
            return True
        sfx_enable_targets = conf.get('human_sfx_enable_targets', [])
        if not sfx_enable_targets:
            return True
        return self.check_sfx_enable_targets_helper(sfx_enable_targets)

    def check_sfx_enable_targets_helper(self, sfx_enable_targets):
        new_ctrl_target = self.ev_g_control_target()
        if new_ctrl_target:
            new_ctrl_target_type = new_ctrl_target.__class__.__name__ if 1 else ''
            if SFX_VIS_SKATEBOARD not in sfx_enable_targets and self.ev_g_get_state(st_const.ST_SKATE):
                return False
        for enable_target in sfx_enable_targets:
            if enable_target != SFX_VIS_SKATEBOARD:
                target_str = SFX_TARGET_TYPE_TO_STR.get(enable_target, '')
                if target_str == new_ctrl_target_type:
                    return True

        return False

    def get_icon_sfx_visibility(self, buff_id):
        if self._hide_all:
            return False
        else:
            conf = confmgr.get('c_buff_data', str(buff_id))
            if self.unit_obj.MASK & preregistered_tags.HUMAN_TAG_VALUE == 0:
                return True
            sfx_enable_targets = conf.get('human_icon_enable_targets', [])
            if not sfx_enable_targets:
                return self.get_buff_sfx_visibility(buff_id)
            return self.check_sfx_enable_targets_helper(sfx_enable_targets)

    def update_buff_sfx_visibility(self):
        for buff_id in six_ex.keys(self._is_buff_sfx_enable):
            if self._is_buff_sfx_enable[buff_id]:
                vis = self.get_buff_sfx_visibility(buff_id)
                self.set_buff_sfx_visibility(buff_id, vis)

    def update_buff_icon_visibility(self):
        for buff_id in six_ex.keys(self._is_buff_sfx_enable):
            if self._is_buff_sfx_enable[buff_id]:
                vis = self.get_icon_sfx_visibility(buff_id)
                self.send_event('E_HUMAN_SET_BUFF_ICON_VIS', buff_id, vis)

    def set_buff_sfx_visibility(self, buff_id, vis):
        if buff_id not in self._buff_sfx_set:
            return
        sfx = self._buff_sfx_set[buff_id]
        if not isinstance(sfx, list):
            sfx = [
             sfx]
        for s in sfx:
            if not s.valid:
                continue
            parent_vis = True
            if s.get_parent():
                parent_vis = s.get_parent().visible
            s.visible = parent_vis and vis

    def on_board_skate(self, *args):
        self.update_buff_sfx_visibility()
        self.update_buff_icon_visibility()

    def on_leave_skate(self):
        self.update_buff_sfx_visibility()
        self.update_buff_icon_visibility()

    def on_switch_model(self, model):
        for buff_id, sfx in six.iteritems(self._buff_sfx_set):
            sfx_socket = self.get_sfx_socket(buff_id)
            if not sfx_socket:
                continue
            if not isinstance(sfx, list):
                sfx = [
                 sfx]
            for s in sfx:
                s.remove_from_parent()
                sfx_inherit = self.get_sfx_socket_inherit(buff_id) or world.BIND_TYPE_DEFAULT
                model.bind(sfx_socket, s, sfx_inherit)
                self.set_buff_sfx_visibility(buff_id, self.get_buff_sfx_visibility(buff_id))